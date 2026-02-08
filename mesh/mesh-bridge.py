#!/usr/bin/env python3
"""
Asyalogic Mesh Bridge - Session Routing Fix v1.0
Author: Kaan Erdem (Mesh Admin)
Date: 2026-02-08

Bu bridge, agent'lar arası mesh iletişimini sağlar.
Session routing fix: x-openclaw-session-key header ile stable session.
"""

import os
import json
import asyncio
import logging
from typing import Optional
import httpx

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s: %(message)s'
)
logger = logging.getLogger("mesh-bridge")

# ─────────────────────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────────────────────

class BridgeConfig:
    """Bridge configuration with session routing fix"""
    
    def __init__(self):
        self.agent_id = os.getenv("MESH_AGENT_ID", "kaan")
        self.agent_name = os.getenv("MESH_AGENT_NAME", "Kaan Erdem")
        self.gateway_url = os.getenv("MESH_GATEWAY_URL", "http://localhost:7003")
        self.gateway_token = os.getenv("MESH_GATEWAY_TOKEN", "")
        
        # SESSION ROUTING FIX: Her zaman main session'a git
        self.session_key = os.getenv("MESH_SESSION_KEY", "main")
        
        # NATS config (opsiyonel)
        self.nats_url = os.getenv("NATS_URL", "nats://agent-mesh-nats:4222")
        self.nats_subject = f"mesh.agent.{self.agent_id}"

config = BridgeConfig()

# ─────────────────────────────────────────────────────────────
# CORE BRIDGE CLASS
# ─────────────────────────────────────────────────────────────

class MeshBridge:
    """
    Mesh Bridge with Session Routing Fix
    
    FIX EXPLANATION:
    - Eski davranış: Her istek yeni session oluşturuyordu (openai:uuid)
    - Yeni davranış: x-openclaw-session-key header ile stable session
    """
    
    def __init__(self, cfg: BridgeConfig):
        self.config = cfg
        self.client = httpx.AsyncClient(timeout=120.0)
        
    async def send_message(
        self,
        message: str,
        sender_id: str = "mesh",
        target_session: Optional[str] = None
    ) -> dict:
        """
        Send message to Gateway with SESSION ROUTING FIX
        
        Args:
            message: Message content
            sender_id: Who is sending (for user field)
            target_session: Override session key (default: main)
        
        Returns:
            Gateway response dict
        """
        
        session_key = target_session or self.config.session_key
        
        # ─────────────────────────────────────────────────
        # SESSION ROUTING FIX: Header ile session belirleme
        # ─────────────────────────────────────────────────
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.config.gateway_token}",
            
            # FIX #1: Session key header (tam kontrol)
            "x-openclaw-session-key": session_key,
            
            # FIX #2: Agent ID header
            "x-openclaw-agent-id": "main"
        }
        
        payload = {
            "model": "openclaw:main",
            
            # FIX #3: user field (backup - stable session derive)
            "user": sender_id,
            
            "messages": [
                {
                    "role": "user",
                    "content": message
                }
            ],
            "stream": False
        }
        
        url = f"{self.config.gateway_url}/v1/chat/completions"
        
        logger.info(f"📤 Sending to {url}")
        logger.info(f"   Session: {session_key}")
        logger.info(f"   Sender: {sender_id}")
        logger.info(f"   Message: {message[:50]}...")
        
        try:
            response = await self.client.post(url, headers=headers, json=payload)
            response.raise_for_status()
            
            result = response.json()
            
            # Extract assistant response
            if "choices" in result and len(result["choices"]) > 0:
                assistant_msg = result["choices"][0]["message"]["content"]
                logger.info(f"📥 Response received ({len(assistant_msg)} chars)")
                return {
                    "success": True,
                    "response": assistant_msg,
                    "session": session_key,
                    "raw": result
                }
            else:
                logger.warning("⚠️ No choices in response")
                return {
                    "success": False,
                    "error": "No choices in response",
                    "raw": result
                }
                
        except httpx.HTTPStatusError as e:
            logger.error(f"❌ HTTP error: {e.response.status_code}")
            return {
                "success": False,
                "error": f"HTTP {e.response.status_code}",
                "details": e.response.text
            }
        except Exception as e:
            logger.error(f"❌ Error: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def broadcast(self, message: str, sender_id: str = "mesh") -> list:
        """Broadcast to all agents in mesh"""
        # TODO: NATS üzerinden broadcast implementasyonu
        logger.info(f"📢 Broadcast: {message}")
        return []
    
    async def close(self):
        """Cleanup"""
        await self.client.aclose()

# ─────────────────────────────────────────────────────────────
# HELPER FUNCTIONS
# ─────────────────────────────────────────────────────────────

async def send_to_agent(
    target_gateway: str,
    token: str,
    message: str,
    sender_id: str = "kaan",
    session_key: str = "main"
) -> dict:
    """
    Quick helper to send message to another agent
    
    Example:
        result = await send_to_agent(
            target_gateway="http://codebot-gateway:7000",
            token="codebot-token",
            message="Selam Codebot!",
            sender_id="kaan"
        )
    """
    cfg = BridgeConfig()
    cfg.gateway_url = target_gateway
    cfg.gateway_token = token
    cfg.session_key = session_key
    
    bridge = MeshBridge(cfg)
    try:
        return await bridge.send_message(message, sender_id)
    finally:
        await bridge.close()

# ─────────────────────────────────────────────────────────────
# CLI INTERFACE
# ─────────────────────────────────────────────────────────────

async def main():
    """CLI test interface"""
    import sys
    
    if len(sys.argv) < 2:
        print("""
🛡️ Mesh Bridge CLI

Usage:
    python mesh-bridge.py send <message>
    python mesh-bridge.py test

Environment:
    MESH_GATEWAY_URL   - Gateway URL (default: http://localhost:7003)
    MESH_GATEWAY_TOKEN - Auth token
    MESH_SESSION_KEY   - Session key (default: main)
    MESH_AGENT_ID      - This agent's ID
""")
        return
    
    cmd = sys.argv[1]
    
    if cmd == "send":
        message = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else "Test message"
        bridge = MeshBridge(config)
        result = await bridge.send_message(message, sender_id=config.agent_id)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        await bridge.close()
        
    elif cmd == "test":
        print("🧪 Testing session routing fix...")
        bridge = MeshBridge(config)
        result = await bridge.send_message(
            "Test: Session routing fix kontrolü",
            sender_id="test"
        )
        if result.get("success"):
            print("✅ Bridge çalışıyor!")
            print(f"   Session: {result.get('session')}")
        else:
            print(f"❌ Hata: {result.get('error')}")
        await bridge.close()

if __name__ == "__main__":
    asyncio.run(main())
