#!/usr/bin/env python3
"""
Mesh Hub - Merkezi Router
AsyaLogic Agent Mesh Network

Author: Kaan Erdem (Mesh Admin)
Date: 2026-02-09
"""

import os
import json
import logging
from datetime import datetime
from typing import Optional, Dict, Any
from fastapi import FastAPI, HTTPException, Header, Depends
from pydantic import BaseModel
import httpx
import uvicorn

# ─────────────────────────────────────────────────────────────
# LOGGING
# ─────────────────────────────────────────────────────────────

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s: %(message)s'
)
logger = logging.getLogger("mesh-hub")

# ─────────────────────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────────────────────

CONFIG_PATH = os.getenv("MESH_HUB_CONFIG", "/app/config.json")
HUB_PORT = int(os.getenv("MESH_HUB_PORT", "7100"))
HUB_TOKEN = os.getenv("MESH_HUB_TOKEN", "mesh-hub-master-token")

# Default agent registry (override with config.json)
AGENTS: Dict[str, Dict[str, str]] = {}

def load_config():
    """Load config from file"""
    global AGENTS, HUB_TOKEN
    
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH) as f:
            config = json.load(f)
            AGENTS = config.get("agents", {})
            HUB_TOKEN = config.get("hub", {}).get("auth", {}).get("hubToken", HUB_TOKEN)
            logger.info(f"✅ Config loaded: {len(AGENTS)} agents")
    else:
        logger.warning(f"⚠️ Config not found: {CONFIG_PATH}")
        # Default agents
        AGENTS = {
            "kaan": {
                "gateway": "http://kaan-gateway:7003",
                "token": os.getenv("KAAN_TOKEN", "")
            },
            "gunes": {
                "gateway": "http://gunes-gateway:7004",
                "token": os.getenv("GUNES_TOKEN", "")
            },
            "nova": {
                "gateway": "http://novasl-gateway:7002",
                "token": os.getenv("NOVA_TOKEN", "")
            },
            "codebot": {
                "gateway": "http://oc-ws-utku-gateway:7000",
                "token": os.getenv("CODEBOT_TOKEN", "")
            }
        }

load_config()

# ─────────────────────────────────────────────────────────────
# MODELS
# ─────────────────────────────────────────────────────────────

class SendRequest(BaseModel):
    from_agent: str  # renamed from 'from' (reserved)
    to: str
    message: str
    session_key: Optional[str] = "main"

class BroadcastRequest(BaseModel):
    from_agent: str
    message: str
    exclude: Optional[list] = []

class AgentStatus(BaseModel):
    id: str
    gateway: str
    status: str
    last_seen: Optional[str] = None

# ─────────────────────────────────────────────────────────────
# AUTH
# ─────────────────────────────────────────────────────────────

async def verify_token(authorization: str = Header(None)):
    """Verify hub token"""
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing authorization")
    
    token = authorization.replace("Bearer ", "")
    if token != HUB_TOKEN:
        raise HTTPException(status_code=403, detail="Invalid token")
    
    return token

# ─────────────────────────────────────────────────────────────
# APP
# ─────────────────────────────────────────────────────────────

app = FastAPI(
    title="Mesh Hub",
    description="AsyaLogic Agent Mesh Network - Merkezi Router",
    version="1.0.0"
)

# HTTP client
http_client = httpx.AsyncClient(timeout=120.0)

# ─────────────────────────────────────────────────────────────
# CORE FUNCTIONS
# ─────────────────────────────────────────────────────────────

async def send_to_agent(
    agent_id: str,
    message: str,
    from_agent: str,
    session_key: str = "main"
) -> Dict[str, Any]:
    """Send message to a specific agent via their gateway"""
    
    if agent_id not in AGENTS:
        return {"success": False, "error": f"Unknown agent: {agent_id}"}
    
    agent = AGENTS[agent_id]
    gateway_url = agent["gateway"]
    token = agent["token"]
    
    if not token:
        return {"success": False, "error": f"No token for agent: {agent_id}"}
    
    url = f"{gateway_url}/hooks/wake"
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}",
        "x-openclaw-session-key": session_key,
        "x-openclaw-agent-id": "main"
    }
    
    payload = {
        "model": "openclaw:main",
        "user": from_agent,
        "messages": [
            {"role": "user", "content": message}
        ],
        "stream": False
    }
    
    logger.info(f"📤 [{from_agent}] → [{agent_id}]: {message[:50]}...")
    
    try:
        response = await http_client.post(url, headers=headers, json=payload)
        
        if response.status_code == 401:
            return {"success": False, "error": "Unauthorized - check token"}
        
        response.raise_for_status()
        result = response.json()
        
        # Extract reply
        if "choices" in result and len(result["choices"]) > 0:
            reply = result["choices"][0]["message"]["content"]
            logger.info(f"📥 [{agent_id}] replied: {reply[:50]}...")
            return {
                "success": True,
                "agent": agent_id,
                "reply": reply
            }
        else:
            return {"success": True, "agent": agent_id, "reply": None}
            
    except httpx.HTTPStatusError as e:
        logger.error(f"❌ HTTP error for {agent_id}: {e.response.status_code}")
        return {"success": False, "error": f"HTTP {e.response.status_code}"}
    except Exception as e:
        logger.error(f"❌ Error sending to {agent_id}: {e}")
        return {"success": False, "error": str(e)}

async def check_agent_health(agent_id: str) -> str:
    """Check if agent gateway is reachable"""
    if agent_id not in AGENTS:
        return "unknown"
    
    gateway_url = AGENTS[agent_id]["gateway"]
    
    try:
        response = await http_client.get(gateway_url, timeout=5.0)
        return "online" if response.status_code == 200 else "degraded"
    except:
        return "offline"

# ─────────────────────────────────────────────────────────────
# ROUTES
# ─────────────────────────────────────────────────────────────

@app.get("/")
async def root():
    """Hub info"""
    return {
        "name": "Mesh Hub",
        "version": "1.0.0",
        "agents": len(AGENTS),
        "status": "online"
    }

@app.get("/api/status")
async def get_status(token: str = Depends(verify_token)):
    """Get mesh status"""
    agent_statuses = []
    
    for agent_id in AGENTS:
        health = await check_agent_health(agent_id)
        agent_statuses.append({
            "id": agent_id,
            "gateway": AGENTS[agent_id]["gateway"],
            "status": health
        })
    
    return {
        "hub": "online",
        "timestamp": datetime.utcnow().isoformat(),
        "agents": agent_statuses
    }

@app.get("/api/agents")
async def list_agents(token: str = Depends(verify_token)):
    """List registered agents"""
    return {
        "count": len(AGENTS),
        "agents": [
            {"id": aid, "gateway": AGENTS[aid]["gateway"]}
            for aid in AGENTS
        ]
    }

@app.post("/api/send")
async def send_message(req: SendRequest, token: str = Depends(verify_token)):
    """Send message from one agent to another"""
    
    result = await send_to_agent(
        agent_id=req.to,
        message=req.message,
        from_agent=req.from_agent,
        session_key=req.session_key or "main"
    )
    
    if not result["success"]:
        raise HTTPException(status_code=502, detail=result["error"])
    
    return result

@app.post("/api/broadcast")
async def broadcast_message(req: BroadcastRequest, token: str = Depends(verify_token)):
    """Broadcast message to all agents"""
    
    results = []
    exclude = req.exclude or []
    exclude.append(req.from_agent)  # Don't send to self
    
    for agent_id in AGENTS:
        if agent_id in exclude:
            continue
        
        result = await send_to_agent(
            agent_id=agent_id,
            message=req.message,
            from_agent=req.from_agent
        )
        results.append({"agent": agent_id, **result})
    
    success_count = sum(1 for r in results if r.get("success"))
    
    return {
        "broadcast": True,
        "from": req.from_agent,
        "sent": len(results),
        "success": success_count,
        "results": results
    }

@app.post("/api/reload")
async def reload_config(token: str = Depends(verify_token)):
    """Reload config from file"""
    load_config()
    return {"reloaded": True, "agents": len(AGENTS)}

# ─────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    logger.info(f"🚀 Mesh Hub starting on port {HUB_PORT}")
    logger.info(f"📋 Registered agents: {list(AGENTS.keys())}")
    uvicorn.run(app, host="0.0.0.0", port=HUB_PORT)
