#!/usr/bin/env python3
"""
Mesh Send - Tek agent'a mesaj gönder

Kullanım:
    mesh-send.py <target> <message>
    mesh-send.py nova "Merhaba Nova!"
    mesh-send.py gunes "Toplantı var mı?"

ENV:
    NATS_URL     - NATS server (default: nats://nats:4222)
    SENDER_ID    - Gönderen kimliği (default: mesh-cli)
"""

import asyncio
import json
import os
import sys
from datetime import datetime, timezone

try:
    import nats
except ImportError:
    print("❌ pip install nats-py")
    sys.exit(1)

NATS_URL = os.environ.get("NATS_URL", "nats://nats:4222")
SENDER_ID = os.environ.get("SENDER_ID", "mesh-cli")

async def send(target: str, message: str):
    topic = f"agents.{target}.inbox"
    
    payload = {
        "from": SENDER_ID,
        "to": target,
        "message": message,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "priority": "normal"
    }
    
    try:
        nc = await nats.connect(NATS_URL)
        await nc.publish(topic, json.dumps(payload).encode())
        await nc.flush()
        await nc.close()
        
        print(f"✅ Sent to {target}")
        print(f"   Topic: {topic}")
        print(f"   Message: {message[:50]}{'...' if len(message) > 50 else ''}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: mesh-send.py <target> <message>")
        print("Example: mesh-send.py nova 'Merhaba!'")
        sys.exit(1)
    
    target = sys.argv[1]
    message = " ".join(sys.argv[2:])
    
    asyncio.run(send(target, message))
