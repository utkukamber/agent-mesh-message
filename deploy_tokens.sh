#!/bin/bash
# MESH TOKEN DEPLOYMENT SCRIPT
# Run this from HOST machine
# Created: 2026-02-08 by Kaan

set -e

echo "🛡️ Mesh Token Deployment Starting..."
echo ""

# Token definitions
declare -A TOKENS=(
    ["novasl-gateway"]="sk-ant-oat01-kSXj_oyomoNT6EP5zwEAY8vSYTsYVJ136_VX9QSX1-E9jU3Ub6xoKW31cUXTU-eOq_BdxSssvEBsNAHnWsX-TqQ-xVcYAwAA"
    ["oc-ws-utku-gateway"]="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"
    ["gunes-gateway"]="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"
    ["openclaw-gateway-2"]="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"
    ["oc-ps-emres-gateway"]="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"
)

# Deploy to each container
for container in "${!TOKENS[@]}"; do
    token="${TOKENS[$container]}"
    echo "📦 Deploying to $container..."
    
    if docker ps --format '{{.Names}}' | grep -q "^${container}$"; then
        # Create token directory and save
        docker exec "$container" mkdir -p /home/node/.claude/tokens 2>/dev/null || true
        docker exec "$container" bash -c "echo 'export CLAUDE_CODE_OAUTH_TOKEN=\"$token\"' > /home/node/.claude/tokens/token.env && chmod 600 /home/node/.claude/tokens/token.env"
        
        # Add to bashrc
        docker exec "$container" bash -c "grep -q CLAUDE_CODE_OAUTH_TOKEN /home/node/.bashrc || echo 'export CLAUDE_CODE_OAUTH_TOKEN=\"$token\"' >> /home/node/.bashrc"
        
        echo "   ✅ $container done"
    else
        echo "   ⚠️ $container not running, skipped"
    fi
done

echo ""
echo "🛡️ Deployment complete!"
echo ""
echo "To verify, run:"
echo "  docker exec <container> bash -c 'echo \$CLAUDE_CODE_OAUTH_TOKEN | tail -c 12'"
