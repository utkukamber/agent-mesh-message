# 🖥️ Mesh CLI Dökümantasyonu

## Genel Bakış

Mesh CLI, komut satırından agent'lara mesaj göndermeyi sağlar.

## Kurulum

CLI, `mesh-cli` container'ı olarak çalışır:

```bash
docker-compose up -d mesh-cli
```

## Komutlar

### mesh-send.py

Tek bir agent'a mesaj gönderir.

```bash
# Kullanım
docker exec mesh-cli python3 /app/mesh-send.py <target> <message>

# Örnekler
docker exec mesh-cli python3 /app/mesh-send.py nova "Merhaba!"
docker exec mesh-cli python3 /app/mesh-send.py gunes "Toplantı var mı?"
docker exec mesh-cli python3 /app/mesh-send.py kaan "Mesh durumu nasıl?"
```

### mesh-broadcast.py

Tüm agent'lara aynı anda mesaj gönderir.

```bash
# Kullanım
docker exec mesh-cli python3 /app/mesh-broadcast.py [--priority high|normal] <message>

# Örnekler
docker exec mesh-cli python3 /app/mesh-broadcast.py "Toplantı 5dk sonra!"
docker exec mesh-cli python3 /app/mesh-broadcast.py --priority high "ACİL DURUM!"
```

## Environment Variables

| Değişken | Açıklama | Default |
|----------|----------|---------|
| `NATS_URL` | NATS server | `nats://agent-mesh-nats:4222` |
| `SENDER_ID` | Gönderen kimliği | `mesh-cli` |

## Mesaj Formatı

### Gönderilen Payload

```json
{
  "from": "mesh-cli",
  "to": "nova",
  "message": "Merhaba!",
  "timestamp": "2026-02-09T20:00:00Z",
  "priority": "normal"
}
```

### Broadcast Payload

```json
{
  "from": "mesh-cli",
  "to": "broadcast",
  "message": "Toplantı başlıyor!",
  "timestamp": "2026-02-09T20:00:00Z",
  "priority": "high"
}
```

## Hedef Agent'lar

| Target | Agent | Container |
|--------|-------|-----------|
| `kaan` | Kaan | kaan-gateway |
| `gunes` | Güneş | gunes-gateway |
| `nova` | Nova | novasl-gateway |
| `codebot` | Codebot | oc-ws-utku-gateway |
| `luna` | Luna | luna-gateway |
| `so` | Solution Officer | so-gateway |
| `emres` | EmreS | oc-ps-emres-gateway |
| `queenb` | QueenB | openclaw-gateway-2 |

## Alias Oluşturma

Host'ta kolaylık için alias ekleyebilirsiniz:

```bash
# ~/.bashrc veya ~/.zshrc
alias mesh-send='docker exec mesh-cli python3 /app/mesh-send.py'
alias mesh-broadcast='docker exec mesh-cli python3 /app/mesh-broadcast.py'

# Kullanım
mesh-send nova "Test"
mesh-broadcast "Merhaba herkese!"
```

## Troubleshooting

### Connection Refused

```bash
# NATS çalışıyor mu?
docker ps | grep nats

# Network bağlantısı var mı?
docker exec mesh-cli ping agent-mesh-nats
```

### Mesaj Gönderildi Ama Yanıt Yok

- Listener çalışıyor mu kontrol et
- Gateway erişilebilir mi kontrol et
- Agent idle olabilir (v1 modunda)
