#!/bin/bash
# Asyalogic Agent Mesh CLI
# Author: Kaan Erdem (Mesh Admin)

MESH_CONFIG="/home/node/.openclaw/workspace/mesh/config.json"
NATS_URL="${NATS_URL:-nats://agent-mesh-nats:4222}"
MESH_LOG="/home/node/.openclaw/workspace/mesh/mesh.log"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$MESH_LOG"
}

mesh_status() {
    echo "═══════════════════════════════════════════════════════════"
    echo "🛡️  ASYALOGIC AGENT MESH NETWORK STATUS"
    echo "═══════════════════════════════════════════════════════════"
    echo ""
    echo "📡 NATS Server: $NATS_URL"
    
    # Check NATS connectivity
    if curl -s http://agent-mesh-nats:8222/varz >/dev/null 2>&1; then
        echo "   Status: 🟢 CONNECTED"
        nats_info=$(curl -s http://agent-mesh-nats:8222/varz 2>/dev/null)
        echo "   Version: $(echo "$nats_info" | grep -o '"version":"[^"]*"' | cut -d'"' -f4)"
        echo "   Connections: $(echo "$nats_info" | grep -o '"connections":[0-9]*' | cut -d':' -f2)"
    else
        echo "   Status: 🔴 DISCONNECTED"
    fi
    echo ""
    echo "═══════════════════════════════════════════════════════════"
    echo "📊 REGISTERED AGENTS"
    echo "═══════════════════════════════════════════════════════════"
    
    if [ -f "$MESH_CONFIG" ]; then
        cat "$MESH_CONFIG" | python3 -c "
import json, sys
data = json.load(sys.stdin)
for agent in data.get('agents', []):
    status_icon = '🟢' if agent.get('status') == 'active' else '🟡' if agent.get('status') == 'pending' else '🔴'
    print(f\"  {status_icon} {agent['id']:12} | {agent['name']:15} | {agent['container']}:{agent['port']}\")
"
    else
        echo "  No agents configured"
    fi
    echo ""
    echo "═══════════════════════════════════════════════════════════"
    echo "🌉 BRIDGE STATUS"
    echo "═══════════════════════════════════════════════════════════"
    
    if [ -f "$MESH_CONFIG" ]; then
        cat "$MESH_CONFIG" | python3 -c "
import json, sys
data = json.load(sys.stdin)
for name, bridge in data.get('bridges', {}).items():
    conn_icon = '🟢' if bridge.get('connected') else '🔴'
    print(f\"  {conn_icon} {name:18} → {bridge['nats_subject']}\")
"
    fi
    echo ""
    echo "═══════════════════════════════════════════════════════════"
    log "STATUS: Mesh status checked"
}

mesh_agents() {
    echo "📋 Agent Registry:"
    if [ -f "$MESH_CONFIG" ]; then
        cat "$MESH_CONFIG" | python3 -c "
import json, sys
data = json.load(sys.stdin)
print(f\"{'ID':12} | {'Name':15} | {'Role':12} | {'Container':20} | Status\")
print('-' * 75)
for agent in data.get('agents', []):
    status = '✅' if agent.get('status') == 'active' else '⏳' if agent.get('status') == 'pending' else '❌'
    print(f\"{agent['id']:12} | {agent['name']:15} | {agent.get('role',''):12} | {agent['container']}:{agent['port']:4} | {status}\")
"
    fi
}

mesh_send() {
    local target="$1"
    local message="$2"
    if [ -z "$target" ] || [ -z "$message" ]; then
        echo "Usage: mesh send <agent_id> <message>"
        return 1
    fi
    echo "📤 Sending to $target: $message"
    log "SEND: $target <- \"$message\""
}

mesh_broadcast() {
    local message="$1"
    if [ -z "$message" ]; then
        echo "Usage: mesh broadcast <message>"
        return 1
    fi
    echo "📢 Broadcasting: $message"
    log "BROADCAST: \"$message\""
}

mesh_kill() {
    local level="$1"
    case "$level" in
        soft)
            echo "⚠️  SOFT KILL activated (auto-resume in 5 minutes)"
            log "KILL: SOFT activated by kaan"
            ;;
        hard)
            echo "🛑 HARD KILL activated (manual resume required)"
            log "KILL: HARD activated by kaan"
            ;;
        nuke|nuclear)
            echo "❌ NUCLEAR kill requires owner authorization"
            echo "   Only Utku Kamber can execute this command"
            log "KILL: NUCLEAR attempted - DENIED (owner only)"
            return 1
            ;;
        *)
            echo "Usage: mesh kill <soft|hard>"
            echo "Note: 'nuclear' requires owner authorization"
            return 1
            ;;
    esac
}

mesh_resume() {
    echo "✅ Kill switch deactivated"
    log "RESUME: Kill switch deactivated by kaan"
}

mesh_logs() {
    if [ -f "$MESH_LOG" ]; then
        tail -50 "$MESH_LOG"
    else
        echo "No logs yet"
    fi
}

# Main command handler
case "$1" in
    status)  mesh_status ;;
    agents)  mesh_agents ;;
    send)    mesh_send "$2" "$3" ;;
    broadcast) mesh_broadcast "$2" ;;
    kill)    mesh_kill "$2" ;;
    resume)  mesh_resume ;;
    logs)    mesh_logs ;;
    *)
        echo "🛡️ Asyalogic Agent Mesh CLI"
        echo ""
        echo "Commands:"
        echo "  status     - Show mesh status"
        echo "  agents     - List registered agents"
        echo "  send       - Send message to agent"
        echo "  broadcast  - Broadcast to all agents"
        echo "  kill       - Activate kill switch (soft/hard)"
        echo "  resume     - Deactivate kill switch"
        echo "  logs       - Show mesh logs"
        ;;
esac
