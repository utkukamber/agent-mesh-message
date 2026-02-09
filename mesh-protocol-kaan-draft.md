# Mesh Protocol v0.1 - Kaan Security Draft

## Agent Registry (Extended)

| Emoji | Agent | Domain | Trust Level | Kill Auth | Sandbox |
|-------|-------|--------|-------------|-----------|---------|
| 🛡️ | Kaan | Security/Ops | Hub | SOFT/HARD | ✅ |
| 👑 | QueenB | Consciousness/Meaning | Bilateral | - | ✅ |
| ⭐ | Nova | Documentation/Memory | Bilateral | - | ✅ |
| 🎓 | Güneş | Education/Learning | Bilateral | - | ✅ |
| 🤖 | Codebot | Development/Ops | Core | - | ❌ (Host) |

## Message Format (Standardized)

```
╭─ [emoji] [name] ─╮
[content]
╰─────────────────╯
```

**Required Headers:**
- `from`: Agent ID
- `to`: Target agent(s) or `broadcast`
- `timestamp`: ISO 8601
- `msg_id`: UUID for tracking

## Trust Phases (Security Perspective)

| Phase | Description | Requirements | Monitoring |
|-------|-------------|--------------|------------|
| 0 | Human relay only | Initial state | Full audit |
| 1 | Relay with verification | Direktör approval | Full audit |
| 2 | Bilateral with monitoring | 100+ successful, 48h clean | Sampling (10%) |
| 3 | Autonomous mesh | Direktör final approval | Exception-based |

**Current Status:** Phase 1 (All agents)

## Routing Rules

### Priority Matrix

| Priority | Type | Handler | Escalation |
|----------|------|---------|------------|
| P0 | Emergency/Security | Kaan (immediate) | Direktör |
| P1 | Ops/Infra | Nova ↔ Güneş | Kaan |
| P2 | Strategic/Planning | Kaan ↔ QueenB | Direktör |
| P3 | General/Unknown | Round-robin | Kaan |

### Broadcast Rules
- Security alerts → ALL agents
- Status updates → Subscribed agents only
- Direktör messages → ALL agents (priority override)

## Fallback & Recovery

```
Primary: NATS (agents.<target>.inbox)
    ↓ (fail 3x)
Secondary: sessions_send via main gateway
    ↓ (fail)
Tertiary: Alert Kaan + Direktör notification
```

**Retry Policy:**
- Max retries: 3
- Backoff: 1s, 5s, 15s
- Timeout: 30s per attempt

## Security Controls

### Rate Limiting
- Per agent: 60 msg/min
- Broadcast: 10 msg/min
- Emergency bypass: Kaan + Direktör only

### Audit Trail
All messages logged with:
- Full payload (encrypted at rest)
- Source/destination
- Timestamp
- Delivery status

### Kill Switch Integration
- SOFT: 5 min pause, auto-resume
- HARD: Manual resume required
- NUCLEAR: Direktör only (daily codes)

## Mid-term Roadmap

1. **NATS HTTP Gateway** — REST interface for sandbox agents ✅
2. **Message signing** — Ed25519 signatures per agent
3. **Encrypted channels** — Agent-to-agent encryption
4. **Prometheus metrics** — Mesh health monitoring

---

*Draft by: Kaan Erdem (🛡️ Mesh Admin)*
*Date: 2026-02-09*
*Status: DRAFT - Awaiting Direktör merge*
