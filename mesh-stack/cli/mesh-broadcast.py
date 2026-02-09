#!/usr/bin/env python3
"""
Mesh Broadcast - Tüm agent'lara mesaj gönder

Kullanım:
    mesh-broadcast.py <message>
    mesh-broadcast.py "Toplantı başlıyor!"
    mesh-broadcast.py --priority high "ACİL DURUM!"

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
BROADCAST_TOPIC = "agents.broadcast"

async def broadcast(message: str, priority: str = "normal"):
    payload = {
        "from": SENDER_ID,
        "to": "broadcast",
        "message": message,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "priority": priority
    }
    
    try:
        nc = await nats.connect(NATS_URL)
        await nc.publish(BROADCAST_TOPIC, json.dumps(payload).encode())
        await nc.flush()
        await nc.close()
        
        print(f"📢 Broadcast sent!")
        print(f"   Topic: {BROADCAST_TOPIC}")
        print(f"   Priority: {priority}")
        print(f"   Message: {message[:50]}{'...' if len(message) > 50 else ''}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: mesh-broadcast.py [--priority high|normal] <message>")
        print("Example: mesh-broadcast.py 'Toplantı başlıyor!'")
        sys.exit(1)
    
    priority = "normal"
    args = sys.argv[1:]
    
    if args[0] == "--priority" and len(args) > 2:
        priority = args[1]
        args = args[2:]
    
    message = " ".join(args)
    asyncio.run(broadcast(message, priority))
