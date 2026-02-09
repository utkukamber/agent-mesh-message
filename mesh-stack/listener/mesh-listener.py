#!/usr/bin/env python3
"""
Mesh NATS Listener v2 - REALTIME
Agent'ı /v1/chat/completions ile GERÇEKTEN tetikler.

ENV VARS:
  AGENT_ID      - Agent kimliği (kaan, nova, gunes, vb.)
  GATEWAY_HOST  - Gateway hostname (default: localhost)
  GATEWAY_PORT  - Gateway portu (default: 7000)
  GATEWAY_TOKEN - Gateway auth token
  NATS_URL      - NATS server (default: nats://nats:4222)
"""

import asyncio
import os
import sys
import json
import signal
from datetime import datetime, timezone

try:
    import nats
    import requests
except ImportError:
    print("❌ Missing deps. Run: pip install nats-py requests")
    sys.exit(1)

# Config from ENV
AGENT_ID = os.environ.get("AGENT_ID", "unknown")
GATEWAY_HOST = os.environ.get("GATEWAY_HOST", "localhost")
GATEWAY_PORT = os.environ.get("GATEWAY_PORT", "7000")
GATEWAY_TOKEN = os.environ.get("GATEWAY_TOKEN", "")
NATS_URL = os.environ.get("NATS_URL", "nats://nats:4222")
MODEL = os.environ.get("MODEL", "anthropic/claude-opus-4-5")

API_URL = f"http://{GATEWAY_HOST}:{GATEWAY_PORT}/v1/chat/completions"
INBOX_TOPIC = f"agents.{AGENT_ID}.inbox"
BROADCAST_TOPIC = "agents.broadcast"

running = True

def log(msg):
    ts = datetime.now(timezone.utc).strftime("%H:%M:%S")
    print(f"[{ts}] {msg}", flush=True)

async def handle_message(msg, nc):
    """Process incoming NATS message - TRIGGER AGENT"""
    try:
        data = json.loads(msg.data.decode())
        sender = data.get("from", "mesh")
        message = data.get("message", "")
        reply_to = data.get("reply_to", sender)  # Yanıt nereye gidecek
        
        log(f"📨 from={sender} reply_to={reply_to}")
        log(f"   message: {message[:60]}...")
        
        # Format message for agent
        user_message = f"🐦 MESH MESSAGE from [{sender}]:\n\n{message}\n\n---\nYanıt vermek için NATS'a publish yap: agents.{reply_to}.inbox"
        
        # Call agent via chat completions API
        resp = requests.post(
            API_URL,
            headers={
                "Authorization": f"Bearer {GATEWAY_TOKEN}",
                "Content-Type": "application/json"
            },
            json={
                "model": MODEL,
                "messages": [{"role": "user", "content": user_message}],
                "max_tokens": 2000
            },
            timeout=120  # Agent düşünme süresi için uzun timeout
        )
        
        if resp.status_code == 200:
            result = resp.json()
            agent_response = result.get("choices", [{}])[0].get("message", {}).get("content", "")
            log(f"   ✅ Agent responded ({len(agent_response)} chars)")
            
            # Auto-reply: Agent yanıtını sender'a geri gönder
            if reply_to and agent_response:
                reply_payload = {
                    "from": AGENT_ID,
                    "to": reply_to,
                    "message": agent_response,
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "type": "response"
                }
                await nc.publish(f"agents.{reply_to}.inbox", json.dumps(reply_payload).encode())
                await nc.flush()
                log(f"   📤 Auto-reply sent to {reply_to}")
        else:
            log(f"   ⚠️ API returned {resp.status_code}: {resp.text[:100]}")
            
    except json.JSONDecodeError:
        log(f"   ⚠️ invalid JSON: {msg.data[:100]}")
    except requests.exceptions.Timeout:
        log(f"   ⚠️ API timeout (agent düşünüyor olabilir)")
    except requests.exceptions.RequestException as e:
        log(f"   ❌ API error: {e}")
    except Exception as e:
        log(f"   ❌ error: {e}")

async def main():
    global running
    
    log(f"🚀 Mesh Listener v2 (REALTIME) starting...")
    log(f"   Agent: {AGENT_ID}")
    log(f"   API: {API_URL}")
    log(f"   NATS: {NATS_URL}")
    log(f"   Topics: {INBOX_TOPIC}, {BROADCAST_TOPIC}")
    
    if not GATEWAY_TOKEN:
        log("❌ GATEWAY_TOKEN not set!")
        sys.exit(1)
    
    # Connect to NATS with retry
    nc = None
    for attempt in range(5):
        try:
            nc = await nats.connect(NATS_URL)
            log("✅ Connected to NATS")
            break
        except Exception as e:
            log(f"⚠️ NATS connect attempt {attempt+1}/5: {e}")
            await asyncio.sleep(2)
    
    if not nc:
        log("❌ Failed to connect to NATS")
        sys.exit(1)
    
    # Handler with nc reference
    async def handler(msg):
        await handle_message(msg, nc)
    
    # Subscribe to inbox and broadcast
    await nc.subscribe(INBOX_TOPIC, cb=handler)
    await nc.subscribe(BROADCAST_TOPIC, cb=handler)
    log(f"✅ Subscribed to topics")
    
    # Graceful shutdown
    def shutdown(sig, frame):
        global running
        log(f"🛑 Shutdown signal received")
        running = False
    
    signal.signal(signal.SIGTERM, shutdown)
    signal.signal(signal.SIGINT, shutdown)
    
    # Keep alive
    log("👂 Listening for messages (REALTIME mode)...")
    while running:
        await asyncio.sleep(1)
    
    await nc.close()
    log("👋 Stopped")

if __name__ == "__main__":
    asyncio.run(main())
