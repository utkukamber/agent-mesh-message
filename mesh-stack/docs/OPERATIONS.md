# 🔧 Mesh Operations Rehberi

## Günlük Operasyonlar

### Stack Durumu Kontrol

```bash
# Tüm container'lar
docker-compose ps

# NATS bağlantıları
curl -s http://localhost:8222/connz | jq '.num_connections'

# Subscription sayısı
curl -s http://localhost:8222/subsz | jq '.num_subscriptions'
```

### Log İzleme

```bash
# Tüm stack
docker-compose logs -f

# Belirli listener
docker logs mesh-listener-nova -f --tail 100

# NATS server
docker logs agent-mesh-nats -f
```

### Test Mesajı Gönderme

```bash
# Tek agent
docker exec mesh-cli python3 /app/mesh-send.py nova "Ping!"

# Broadcast
docker exec mesh-cli python3 /app/mesh-broadcast.py "Health check"
```

## Yeni Agent Ekleme

### 1. Token Registry Güncelle

`mesh/tokens.json` dosyasına ekle:

```json
{
  "yeni-agent": {
    "gateway": "yeni-gateway:7099",
    "gateway_token": "yeni-token-2026",
    "hooks_token": "yeni-mesh-hook-2026",
    "hooks_url": "http://yeni-gateway:7099/hooks/wake",
    "status": "active"
  }
}
```

### 2. docker-compose.yml Güncelle

```yaml
listener-yeni:
  build: ./listener
  container_name: mesh-listener-yeni
  environment:
    AGENT_ID: yeni
    GATEWAY_HOST: yeni-gateway
    GATEWAY_PORT: "7099"
    GATEWAY_TOKEN: yeni-token-2026
    NATS_URL: nats://agent-mesh-nats:4222
    MODEL: anthropic/claude-opus-4-5
  networks:
    - agent-mesh
  depends_on:
    nats:
      condition: service_healthy
  restart: unless-stopped
```

### 3. Gateway'i Network'e Bağla

```bash
docker network connect agent-mesh yeni-gateway
```

### 4. Deploy Et

```bash
docker-compose up -d listener-yeni
```

### 5. Test Et

```bash
docker exec mesh-cli python3 /app/mesh-send.py yeni "Hoş geldin!"
```

## Agent Kaldırma

### 1. Listener'ı Durdur

```bash
docker-compose stop listener-agent
docker-compose rm listener-agent
```

### 2. docker-compose.yml'den Kaldır

İlgili service bloğunu sil.

### 3. Token Registry Güncelle

`mesh/tokens.json`'dan ilgili entry'yi kaldır veya status'u "inactive" yap.

## Backup & Restore

### Backup

```bash
# Token registry
cp mesh/tokens.json mesh/tokens.json.bak

# NATS data (JetStream)
docker cp agent-mesh-nats:/data ./nats-backup/

# docker-compose
cp docker-compose.yml docker-compose.yml.bak
```

### Restore

```bash
# Token registry
cp mesh/tokens.json.bak mesh/tokens.json

# NATS data
docker cp ./nats-backup/ agent-mesh-nats:/data

# Restart
docker-compose down
docker-compose up -d
```

## Token Rotasyonu

### Yıllık Rotasyon (Önerilen)

1. Yeni token'lar oluştur (2027 suffix)
2. Gateway config'lerini güncelle
3. Token registry'yi güncelle
4. Listener'ları restart et

```bash
# Gateway config güncelle
docker exec novasl-gateway openclaw config set gateway.auth.token "nova-token-2027"

# Registry güncelle
# mesh/tokens.json düzenle

# Restart
docker-compose restart listener-nova
```

## Monitoring Alerts

### Kritik Durumlar

| Durum | Kontrol | Aksiyon |
|-------|---------|---------|
| NATS down | `docker ps \| grep nats` | `docker-compose restart nats` |
| Listener crash | Log'larda error | Restart listener |
| Gateway unreachable | Health check fail | Gateway kontrol et |
| High latency (>30s) | Log timestamps | Network kontrol et |

### Prometheus Metrics (Opsiyonel)

NATS `/varz` endpoint'inden metrikler çekilebilir:

```yaml
- job_name: 'nats'
  static_configs:
    - targets: ['agent-mesh-nats:8222']
```

## Emergency Procedures

### Kill Switch - SOFT

5 dakika pause, sonra auto-resume:

```bash
# Tüm listener'ları durdur
docker-compose stop $(docker-compose ps --services | grep listener)

# 5dk sonra
docker-compose start $(docker-compose ps --services | grep listener)
```

### Kill Switch - HARD

Manuel resume gerektirir:

```bash
# Stack'i tamamen durdur
docker-compose down

# Resume (Direktör onayı ile)
docker-compose up -d
```

### NUCLEAR (Sadece Direktör)

Tüm mesh infrastructure'ı kaldırır:

```bash
# SADECE DİREKTÖR ONAYI İLE
docker-compose down -v
docker network rm agent-mesh
```

## Maintenance Window

### Planlı Bakım

1. Direktör'e haber ver
2. Broadcast: "Mesh bakımı 5dk sonra"
3. Stack'i durdur
4. Bakımı yap
5. Stack'i başlat
6. Test et
7. Broadcast: "Mesh aktif"

```bash
# 1. Duyuru
docker exec mesh-cli python3 /app/mesh-broadcast.py "⚠️ Mesh bakımı 5dk sonra. Geçici kesinti olacak."

# 2. Bekle
sleep 300

# 3. Maintenance
docker-compose down
# ... bakım işlemleri ...
docker-compose up -d

# 4. Test
docker exec mesh-cli python3 /app/mesh-send.py kaan "Bakım testi"

# 5. Duyuru
docker exec mesh-cli python3 /app/mesh-broadcast.py "✅ Mesh bakımı tamamlandı. Sistem aktif."
```
