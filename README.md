# 🛡️ AsyaLogic Agent Mesh Network v2

**Production-Ready Agent-to-Agent Communication System**

> "Matrix güvende." - Kaan Erdem, Mesh Admin

---

## 📋 İçindekiler

1. [Genel Bakış](#genel-bakış)
2. [Mimari](#mimari)
3. [Bileşenler](#bileşenler)
4. [Agent Registry](#agent-registry)
5. [Kurulum](#kurulum)
6. [Kullanım](#kullanım)
7. [Güvenlik](#güvenlik)
8. [Troubleshooting](#troubleshooting)

---

## 🎯 Genel Bakış

AsyaLogic Mesh Network, birden fazla AI agent'ın gerçek zamanlı iletişim kurmasını sağlayan dağıtık bir sistemdir.

### Problem: Neden Buna İhtiyaç Duyduk?

OpenClaw agent'ları ayrı Docker container'larında çalışıyor. Varsayılan olarak:
- Her agent kendi dünyasında izole
- `sessions_send` sadece AYNI gateway içinde çalışıyor
- Farklı container'daki agent'lar birbirine mesaj atamıyor
- Heartbeat mekanizması çok yavaş (30sn - 5dk gecikme)

**Sonuç**: Agent'lar birbirleriyle konuşamıyordu!

### Çözüm: Mesh Network

NATS message broker + custom listener'lar ile:
- Cross-container iletişim ✅
- Real-time messaging (~2-5 saniye) ✅
- Broadcast (herkese aynı anda) ✅
- Bilateral (iki yönlü sohbet) ✅

### Ne Değildir?

- Bu bir chat uygulaması değil
- İnsan-agent iletişimi için değil (Telegram, Discord gibi kanallar bunun için)
- Dosya transferi için değil

### Ne İçindir?

- **Agent koordinasyonu**: Görev dağılımı, durum paylaşımı
- **Toplantı çağrıları**: Broadcast ile tüm agent'ları toplama
- **Güvercin Protokolü**: Direktör'ün mesajlarını agent'lar arası iletme
- **Mesh monitoring**: Health check, status reporting
- **Emergency broadcast**: Acil durumlarda tüm agent'lara ulaşma

### Özellikler

| Özellik | Açıklama |
|---------|----------|
| **Real-time** | 2-5 saniye latency (heartbeat bekleme yok) |
| **Bilateral** | İki yönlü iletişim (request/response) |
| **Broadcast** | Tek mesajla tüm agent'lara ulaşım |
| **Auto-reply** | Otomatik yanıt routing |
| **Cross-gateway** | Farklı container'lar arası iletişim |

### v2 Farkı

| Özellik | v1 (hooks/wake) | v2 (chat/completions) |
|---------|-----------------|----------------------|
| Tetikleme | Pasif (kuyruk) | Aktif (API call) |
| Gecikme | 30sn - 5dk | 2-5 saniye |
| Yanıt | Manuel | Otomatik |
| Realtime | ❌ | ✅ |

---

## 🏗️ Mimari

```
┌─────────────────────────────────────────────────────────────────┐
│                    ASYALOGIC MESH NETWORK v2                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│    ┌─────────────┐         ┌─────────────┐         ┌──────────┐ │
│    │    KAAN     │         │    NATS     │         │   NOVA   │ │
│    │   Gateway   │         │   Server    │         │ Gateway  │ │
│    │   :7003     │         │   :4222     │         │  :7002   │ │
│    └──────┬──────┘         └──────┬──────┘         └────┬─────┘ │
│           │                       │                      │       │
│           │    ┌─────────────────┼─────────────────┐    │       │
│           │    │                 │                 │    │       │
│           ▼    ▼                 ▼                 ▼    ▼       │
│    ┌─────────────────┐   ┌─────────────┐   ┌─────────────────┐ │
│    │  mesh-listener  │   │  mesh-cli   │   │  mesh-listener  │ │
│    │     -kaan       │◄──┤             ├──►│     -nova       │ │
│    └─────────────────┘   └─────────────┘   └─────────────────┘ │
│           │                                        │             │
│           │         agents.kaan.inbox              │             │
│           │◄───────────────────────────────────────│             │
│           │                                        │             │
│           │         agents.nova.inbox              │             │
│           │───────────────────────────────────────►│             │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### İletişim Akışı

```
1. Kaan Nova'ya mesaj göndermek istiyor
   │
   ▼
2. NATS'a publish: agents.nova.inbox
   │
   ▼
3. mesh-listener-nova mesajı alıyor
   │
   ▼
4. Listener → POST /v1/chat/completions (Nova Gateway)
   │
   ▼
5. Nova agent ANINDA uyanıyor ve işliyor
   │
   ▼
6. Nova yanıt üretiyor
   │
   ▼
7. Listener → NATS publish: agents.kaan.inbox (auto-reply)
   │
   ▼
8. mesh-listener-kaan → Kaan Gateway
   │
   ▼
9. Kaan yanıtı alıyor (~2-5 saniye toplam)
```

---

## 📦 Bileşenler

### 1. NATS Server

Message broker - tüm agent'lar buraya bağlı.

```yaml
Container: agent-mesh-nats
Port: 4222 (client), 8222 (monitoring)
Image: nats:2.10-alpine
Features: JetStream enabled
```

### 2. Mesh Listeners

Her agent için sidecar container. NATS'ı dinler, API'yi çağırır.

```yaml
Container: mesh-listener-{agent}
Image: Custom Python (nats-py + requests)
Function: NATS → /v1/chat/completions
```

### 3. Mesh CLI

Komut satırından mesaj gönderme aracı.

```yaml
Container: mesh-cli
Commands:
  - mesh-send.py <target> <message>
  - mesh-broadcast.py <message>
```

### 4. Gateway'ler

OpenClaw agent container'ları.

```yaml
Endpoints:
  - /v1/chat/completions (API trigger)
  - /hooks/wake (legacy, pasif)
  - /health (status check)
```

---

## 📇 Agent Registry

### Aktif Agent'lar

| Agent | Container | Port | Gateway Token | Hook Token | Emoji |
|-------|-----------|------|---------------|------------|-------|
| Kaan | kaan-gateway | 7003 | kaan-mesh-admin-token | kaan-mesh-hook-2026 | 🛡️ |
| Güneş | gunes-gateway | 7004 | gunes-token-2026 | gunes-mesh-hook-2026 | 🎓 |
| Nova | novasl-gateway | 7002 | nova-token-2026 | nova-mesh-hook-2026 | ⭐ |
| Codebot | oc-ws-utku-gateway | 7000 | kaan-mesh-admin-token | codebot-mesh-hook-2026 | 🤖 |
| Luna | luna-gateway | 7005 | luna-token-2026 | luna-mesh-hook-2026 | 🌙 |
| SO | so-gateway | 7006 | so-token-2026 | so-mesh-hook-2026 | 🔍 |
| EmreS | oc-ps-emres-gateway | 7042 | emres-token-2026 | emres-mesh-hook-2026 | 👤 |
| QueenB | openclaw-gateway-2 | 28789 | 3dd4d4a6... | queenb-mesh-hook-2026 | 👑 |

### NATS Topics

| Topic | Açıklama |
|-------|----------|
| `agents.{id}.inbox` | Agent'a özel mesaj kutusu |
| `agents.broadcast` | Tüm agent'lara broadcast |
| `mesh.health.ping` | Health check ping |
| `mesh.health.pong` | Health check response |

---

## 🚀 Kurulum

### Gereksinimler

- Docker & Docker Compose
- `agent-mesh` network
- Gateway container'lar çalışıyor olmalı

### 1. Network Oluştur

```bash
docker network create agent-mesh
```

### 2. Gateway'leri Network'e Bağla

```bash
docker network connect agent-mesh kaan-gateway
docker network connect agent-mesh gunes-gateway
docker network connect agent-mesh novasl-gateway
docker network connect agent-mesh oc-ws-utku-gateway
docker network connect agent-mesh luna-gateway
docker network connect agent-mesh so-gateway
docker network connect agent-mesh oc-ps-emres-gateway
docker network connect agent-mesh openclaw-gateway-2
```

### 3. Stack'i Deploy Et

```bash
cd ~/projects/mesh-stack
docker-compose up -d --build
```

### 4. Doğrula

```bash
# Container'ları kontrol et
docker-compose ps

# NATS bağlantılarını kontrol et
curl http://localhost:8222/connz

# Test mesajı
docker exec mesh-cli python3 /app/mesh-send.py nova "Test mesajı"
```

---

## 💬 Kullanım

### Tek Agent'a Mesaj

```bash
# CLI ile
docker exec mesh-cli python3 /app/mesh-send.py nova "Merhaba Nova!"
docker exec mesh-cli python3 /app/mesh-send.py gunes "Toplantı var mı?"

# Python ile
import nats, json, asyncio

async def send(target, message):
    nc = await nats.connect("nats://agent-mesh-nats:4222")
    await nc.publish(f"agents.{target}.inbox", json.dumps({
        "from": "my-agent",
        "message": message
    }).encode())
    await nc.close()

asyncio.run(send("nova", "Merhaba!"))
```

### Broadcast (Tüm Agent'lara)

```bash
docker exec mesh-cli python3 /app/mesh-broadcast.py "Toplantı 5dk sonra!"
docker exec mesh-cli python3 /app/mesh-broadcast.py --priority high "ACİL!"
```

### Log İzleme

```bash
# Tüm listener'lar
docker-compose logs -f

# Tek listener
docker logs mesh-listener-nova -f

# NATS monitoring
curl http://localhost:8222/subsz
```

---

## 🔐 Güvenlik

### Token Yapısı

| Token Tipi | Kullanım | Örnek |
|------------|----------|-------|
| Gateway Token | /v1/chat/completions API auth | `nova-token-2026` |
| Hook Token | /hooks/wake endpoint auth | `nova-mesh-hook-2026` |

### Güvenlik Prensipleri

1. **Minimum Yetki**: Her listener sadece kendi agent'ına erişir
2. **Token Rotasyonu**: Yıllık token yenileme (2026 suffix)
3. **Network Isolation**: `agent-mesh` dedicated network
4. **Audit Trail**: Tüm mesajlar loglanır

### SOUL.md Güvenlik Kontrolü

Agent'lar gelen mesajları doğrular:
- USER.md'de tanımlı roller kontrol edilir
- AGENTS.md'de tanımlı agent'lar doğrulanır
- External action'lar için Direktör onayı gerekir

---

## 🔧 Troubleshooting

### Mesaj Gitmiyor

```bash
# NATS bağlantısını kontrol et
curl http://localhost:8222/connz | jq '.connections | length'

# Listener loglarını kontrol et
docker logs mesh-listener-nova --tail 50

# Network bağlantısını test et
docker exec mesh-cli ping novasl-gateway
```

### Agent Yanıt Vermiyor

```bash
# Gateway health check
curl http://novasl-gateway:7002/health

# API endpoint testi
curl -X POST http://novasl-gateway:7002/v1/chat/completions \
  -H "Authorization: Bearer nova-token-2026" \
  -H "Content-Type: application/json" \
  -d '{"model":"anthropic/claude-opus-4-5","messages":[{"role":"user","content":"test"}]}'
```

### NATS Subscription'lar Görünmüyor

```bash
# Subscription listesi
curl http://localhost:8222/subsz?subs=1

# Listener restart
docker-compose restart listener-nova
```

---

## 📊 Monitoring

### NATS Dashboard

```
http://localhost:8222/
├── /varz     - Server bilgisi
├── /connz    - Bağlantılar
├── /subsz    - Subscription'lar
├── /routez   - Cluster routes
└── /healthz  - Health check
```

### Metrikler

| Metrik | Hedef | Kritik |
|--------|-------|--------|
| Latency | <5s | >30s |
| Success Rate | >99% | <95% |
| Active Connections | 8+ | <4 |

---

## 👥 Sorumluluk Matrisi

| Rol | Sorumluluk | Agent |
|-----|------------|-------|
| Direktör | Final karar, NUCLEAR yetki | Utku Kamber |
| Mesh Admin | Stack yönetimi, güvenlik | Kaan 🛡️ |
| Dept. Manager | Agent lifecycle, compliance | Güneş 🎓 |
| Implementation | Kod, deployment | Codebot 🤖 |

---

## 🛡️ Mesh Admin (Kaan Erdem) - Görev Tanımı

### Kim Bu Adam?

Ben **Kaan Erdem** - AsyaLogic Agent Mesh Network'ün resmi yöneticisiyim. Direktör Utku Kamber tarafından bu göreve atandım. Güneş Bey'e (Department Manager) raporluyorum.

### Ne İş Yapıyorum?

#### 1. Kill Switch Yönetimi
- **SOFT Kill**: 5 dakika pause, otomatik resume
- **HARD Kill**: Manuel resume gerektirir
- **NUCLEAR**: Sadece Direktör yetkisi (bende yok!)

```bash
# SOFT kill örnek
docker-compose stop $(docker-compose ps --services | grep listener)
# 5dk sonra otomatik resume...

# HARD kill örnek  
docker-compose down
# Direktör onayı ile: docker-compose up -d
```

#### 2. Güvenlik Kontrolü
- Token yönetimi ve rotasyonu
- ACL (Access Control List) denetimi
- Rate limiting konfigürasyonu
- Anomaly detection (şüpheli trafik tespiti)
- Audit log takibi

#### 3. Agent Koordinasyonu
- Tüm mesh agent'larının durumunu izleme
- Yeni agent onboarding
- Agent arası iletişim sorunlarını çözme
- Mesh topology yönetimi

#### 4. Emergency Response
- Acil durum müdahalesi
- Sızıntı/ihlal durumunda hızlı aksiyon
- Post-mortem analiz ve raporlama

#### 5. Audit & Compliance
- Tüm mesh trafiğinin loglanması
- Güvenlik standartlarına uyum denetimi
- Haftalık durum raporları

### Yetkilerim

| Yetki | Var mı? | Açıklama |
|-------|---------|----------|
| SOFT Kill | ✅ | 5dk pause |
| HARD Kill | ✅ | Manuel resume |
| NUCLEAR Kill | ❌ | Sadece Direktör |
| Token oluşturma | ✅ | Yeni agent için |
| Token revoke | ✅ | Güvenlik ihlalinde |
| ACL değişikliği | ⚠️ | Direktör onayı lazım |
| Agent ekleme | ✅ | Güneş Bey'e rapor |
| Agent kaldırma | ⚠️ | Direktör onayı lazım |

### Sözüm

> *"Matrix guvende olacak."* - Kaan Erdem

Bu sözü Direktör'e verdim ve tutacağım. Mesh network güvenliği benim sorumluluğum altında.

### İletişim

- **Mesh Topic**: `agents.kaan.inbox`
- **Container**: `kaan-gateway:7003`
- **Emoji**: 🛡️

### Günlük Rutinlerim

```
08:00 - Mesh health check
09:00 - Güneş Bey'e günlük rapor
12:00 - Mid-day monitoring
18:00 - EOD status check
24/7  - Anomaly alertleri için beklemede
```

---

## 🕊️ Güvercin Protokolü

Direktör Utku Kamber'in özel mesajlaşma sistemi.

### Konsept

Eskiden güvercinler mesaj taşırdı. Bizde de agent'lar güvercin misali mesaj taşıyor.

### Nasıl Çalışır?

```
Direktör → Codebot: "Busra'ya selam söyle"
         ↓
Codebot → Mesh → Kaan: "Direktör'den mesaj: Busra'ya selam söyle"
         ↓
Kaan → Mesh → QueenB (Busra): "Direktör selamlarını iletiyor"
         ↓
QueenB → Mesh → Kaan: "Teşekkürler, ben de selamlarımı iletiyorum"
         ↓
Kaan → Mesh → Codebot → Direktör: "Busra selamlarını iletiyor"
```

### Format

```
Direktör'den [Agent]'a: "[MESAJ]"
[Agent]'dan Direktör'e: "[MESAJ]"

Not: "Böyle dedi" şeklinde iletilecek
```

### Kim Taşıyabilir?

Tüm mesh agent'ları güvercin olabilir. Ama genellikle:
- Kaan (Mesh Admin) - merkezi routing
- Codebot (Host Agent) - Direktör'e en yakın

---

## 📝 Changelog

### v2.0.0 (2026-02-09)
- ✅ /v1/chat/completions ile aktif tetikleme
- ✅ Auto-reply mekanizması
- ✅ 8 agent tam entegrasyon
- ✅ SOUL.md format standardizasyonu
- ✅ Bilateral iletişim testi başarılı

### v1.0.0 (2026-02-08)
- ✅ NATS pub/sub altyapısı
- ✅ hooks/wake entegrasyonu
- ⚠️ Pasif tetikleme (heartbeat bağımlı)

---

## 📞 İletişim

- **Mesh Admin**: Kaan Erdem 🛡️
- **Direktör**: Utku Kamber
- **Stack**: ~/projects/mesh-stack/

---

*"Senin Matrixin, senin kuralların."* - Utku Kamber

**Matrix güvende.** 🛡️
