# Mesh Hub - Merkezi Router

## Mimari

```
┌─────────────────────────────────────────────────────────┐
│                      MESH HUB                            │
│                   (mesh-hub:7100)                        │
│                                                          │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │
│  │ Token Store │  │   Router    │  │  Broadcast  │     │
│  └─────────────┘  └─────────────┘  └─────────────┘     │
└──────────┬──────────────┬──────────────┬────────────────┘
           │              │              │
     ┌─────┴─────┐  ┌─────┴─────┐  ┌─────┴─────┐
     │   Kaan    │  │   Güneş   │  │   Nova    │
     │   :7003   │  │   :7004   │  │   :7002   │
     └───────────┘  └───────────┘  └───────────┘
```

## API Endpoints

### POST /api/send
Bir agent'tan diğerine mesaj gönder.

```json
{
  "from": "kaan",
  "to": "gunes",
  "message": "Selam Güneş Bey!"
}
```

### POST /api/broadcast
Tüm agent'lara mesaj gönder.

```json
{
  "from": "kaan",
  "message": "Herkese duyuru!"
}
```

### GET /api/status
Mesh durumunu göster.

### GET /api/agents
Kayıtlı agent listesi.

## Konfigürasyon

`config.json`:
```json
{
  "hub": {
    "port": 7100,
    "auth": {
      "mode": "token",
      "hubToken": "mesh-hub-master-token"
    }
  },
  "agents": {
    "kaan": {
      "gateway": "http://kaan-gateway:7003",
      "token": "kaan-mesh-admin-token"
    },
    "gunes": {
      "gateway": "http://gunes-gateway:7004",
      "token": "gunes-token"
    },
    "nova": {
      "gateway": "http://novasl-gateway:7002",
      "token": "nova-token"
    },
    "codebot": {
      "gateway": "http://oc-ws-utku-gateway:7000",
      "token": "codebot-token"
    }
  }
}
```

## Kullanım

Agent'lar sadece Hub'a istek atar:

```python
# Kaan'dan Güneş'e mesaj
requests.post("http://mesh-hub:7100/api/send", json={
    "from": "kaan",
    "to": "gunes", 
    "message": "Merhaba!"
}, headers={"Authorization": "Bearer mesh-hub-master-token"})
```

Hub, target agent'ın token'ını bilir ve onun gateway'ine iletir.

## Avantajlar

1. **Tek Nokta Token Yönetimi** - Token'lar sadece Hub'da
2. **Basit Agent Config** - Agent'lar sadece Hub URL'i biliyor
3. **Merkezi Logging** - Tüm mesh trafiği loglanıyor
4. **Rate Limiting** - Hub'da throttle yapılabilir

## Dezavantajlar

1. **Single Point of Failure** - Hub çökerse mesh durur
2. **Latency** - Extra hop ekleniyor

## Kurulum

```bash
docker-compose -f docker-compose.mesh-hub.yml up -d
```
