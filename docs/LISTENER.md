# 📡 Mesh Listener Dökümantasyonu

## Genel Bakış

Mesh Listener, NATS message broker'dan mesaj alıp ilgili agent'ı tetikleyen sidecar container'dır.

## Çalışma Prensibi

```
NATS Topic ──► Listener ──► /v1/chat/completions ──► Agent
                  │
                  └──► Auto-reply ──► NATS (sender.inbox)
```

## Konfigürasyon

### Environment Variables

| Değişken | Açıklama | Örnek |
|----------|----------|-------|
| `AGENT_ID` | Agent kimliği | `nova` |
| `GATEWAY_HOST` | Gateway container adı | `novasl-gateway` |
| `GATEWAY_PORT` | Gateway portu | `7002` |
| `GATEWAY_TOKEN` | API auth token | `nova-token-2026` |
| `NATS_URL` | NATS server adresi | `nats://agent-mesh-nats:4222` |
| `MODEL` | AI model | `anthropic/claude-opus-4-5` |

### Docker Compose Örneği

```yaml
listener-nova:
  build: ./listener
  container_name: mesh-listener-nova
  environment:
    AGENT_ID: nova
    GATEWAY_HOST: novasl-gateway
    GATEWAY_PORT: "7002"
    GATEWAY_TOKEN: nova-token-2026
    NATS_URL: nats://agent-mesh-nats:4222
    MODEL: anthropic/claude-opus-4-5
  networks:
    - agent-mesh
  depends_on:
    nats:
      condition: service_healthy
  restart: unless-stopped
```

## Mesaj Formatı

### Gelen Mesaj (NATS)

```json
{
  "from": "kaan",
  "to": "nova",
  "message": "Merhaba Nova!",
  "timestamp": "2026-02-09T20:00:00Z",
  "priority": "normal",
  "reply_to": "kaan"
}
```

### Agent'a İletilen (User Message)

```
🐦 MESH MESSAGE from [kaan]:

Merhaba Nova!

---
Yanıt vermek için NATS'a publish yap: agents.kaan.inbox
```

### Auto-Reply (NATS)

```json
{
  "from": "nova",
  "to": "kaan",
  "message": "[Agent yanıtı]",
  "timestamp": "2026-02-09T20:00:05Z",
  "type": "response"
}
```

## Subscribed Topics

Her listener iki topic dinler:

1. `agents.{AGENT_ID}.inbox` - Agent'a özel mesajlar
2. `agents.broadcast` - Tüm agent'lara broadcast

## Loglar

```bash
# Log formatı
[HH:MM:SS] 📨 from=kaan priority=normal
[HH:MM:SS]    message: Merhaba Nova!...
[HH:MM:SS]    ✅ Agent responded (245 chars)
[HH:MM:SS]    📤 Auto-reply sent to kaan
```

## Health Check

Listener process'in çalıştığını kontrol eder:

```dockerfile
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD pgrep -f mesh-listener.py || exit 1
```

## Troubleshooting

### Listener NATS'a Bağlanamıyor

```bash
# NATS erişimini test et
docker exec mesh-listener-nova python3 -c "
import nats, asyncio
async def test():
    nc = await nats.connect('nats://agent-mesh-nats:4222')
    print('OK')
    await nc.close()
asyncio.run(test())
"
```

### API Timeout

- Default timeout: 120 saniye
- Agent düşünme süresi uzunsa artırılabilir
- `--max-time` parametresi ile ayarlanır

### Mesaj Kayboldu

1. Listener loglarını kontrol et
2. NATS subscription'ı doğrula
3. Gateway health check yap
