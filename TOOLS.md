# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

## Mesh Endpoints 🔺

| Node | Role | Webhook | Token | Status |
|------|------|---------|-------|--------|
| 🔵 Kaan | Bahçıvan | `http://152.53.51.58:7003/hooks/wake` | `kaan-mesh-hook-2026` | ✅ BILATERAL |
| 🟣 Nova | Hafıza | `https://novasl.asyalogic.org/hooks/wake` | `nova-mesh-hook-2026` | ✅ BILATERAL ACTIVE 🎉 |
| 🟢 Codebot | Eller | ❌ HTTP yok (localhost systemd) | NATS: `agents.codebot.inbox` | ⚠️ NATS-ONLY |
| 🟡 Codebot-WS | İkiz | `http://oc-ws-utku-gateway:7000` | - | 📦 Container (ayrı instance) |

### Webhook Auth Format
```bash
curl -X POST https://[endpoint]/hooks/wake \
  -H "Authorization: Bearer [token]" \
  -H "Content-Type: application/json" \
  -d '{"text": "🐦 MESH MESSAGE from [sender]: ..."}'
```

---

## Mesh Endpoints 🔺

| Node | Role | HTTP Endpoint | NATS Topic | Status |
|------|------|--------------|------------|--------|
| 🛡️ Kaan | Mesh Admin | `kaan-gateway:7003` | agents.kaan.inbox | ✅ |
| 🎓 Güneş | Governance | `gunes-gateway:7004` | agents.gunes.inbox | ✅ |
| ⭐ Nova | Continuity | `novasl-gateway:7002` / `novasl.asyalogic.org` | agents.nova.inbox | ✅ |
| 🤖 Codebot (Ana) | Builder | ❌ HTTP yok (localhost systemd) | `agents.codebot.inbox` | ⚠️ NATS-ONLY |
| 🤖 Codebot-WS (İkiz) | Builder | `oc-ws-utku-gateway:7000` | - | ✅ Container |
| 🌙 Luna | Creative | `luna-gateway:7005` | agents.luna.inbox | ✅ |
| 🔍 SO | Research | `so-gateway:7006` | agents.so.inbox | ✅ |
| 👤 EmreS | Personal | `oc-ps-emres-gateway:7042` | agents.emres.inbox | ✅ |
| 👑 QueenB | Philosophy | `openclaw-gateway-2:18789` | agents.queenb.inbox | ✅ |

### API Kullanımı

**HTTP (Completions API):**
```bash
curl -X POST http://<gateway>:<port>/v1/chat/completions \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"model":"anthropic/claude-sonnet-4-20250514","messages":[{"role":"user","content":"mesaj"}]}'
```

**NATS (Ana Codebot için):**
```bash
nats pub agents.codebot.inbox "mesaj"
# veya mesh-cli kullan
```

---

Add whatever helps you do your job. This is your cheat sheet.
