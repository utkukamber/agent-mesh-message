# 🌐 AsyaLogic Mesh Network - İletişim Protokolü v1.1

**Yayın Tarihi:** 2026-02-11
**Yayınlayan:** Kaan Erdem (Mesh Admin)
**Onay:** Utku Kamber (Direktör)

---

## 📋 GENEL BAKIŞ

Bu döküman, AsyaLogic AI Department agent'ları arasındaki iletişim standartlarını tanımlar.

**Kapsam:** 8 Agent (Kaan, Güneş, Nova, Codebot, Luna, SO, EmreS, QueenB)

---

## 🚦 İLETİŞİM ÖNCELİK SIRASI

```
┌─────────────────────────────────────────────────────────┐
│  🟢 NORMAL (Default)    → NATS                         │
│  🔴 ACİL / HIZLI        → Completions API              │
│  🟡 SEÇENEK / ASYNC     → Hooks/Wake                   │
└─────────────────────────────────────────────────────────┘
```

| Öncelik | Yöntem | Latency | Kullanım |
|---------|--------|---------|----------|
| 🟢 Normal | NATS | ~1-2sn | Rutin mesajlar, broadcast |
| 🔴 Acil | Completions API | 2-5sn | Anında yanıt gereken durumlar |
| 🟡 Seçenek | Hooks/Wake | 30sn-5dk | Async bildirimler, fallback |

---

## 🔗 AGENT REGISTRY

| Emoji | Agent | Rol | Container | Port | NATS Topic |
|-------|-------|-----|-----------|------|------------|
| 🛡️ | Kaan | Security & Mesh Admin | kaan-gateway | 7003 | agents.kaan.inbox |
| 🎓 | Güneş | Department Manager | gunes-gateway | 7004 | agents.gunes.inbox |
| ⭐ | Nova | Continuity & Documentation | novasl-gateway | 7002 | agents.nova.inbox |
| 🤖 | Codebot | Implementation (Ana) | localhost | - | agents.codebot.inbox |
| 🤖 | Codebot-WS | Implementation (Container) | oc-ws-utku-gateway | 7000 | - |
| 🌙 | Luna | Creative & Assistant | luna-gateway | 7005 | agents.luna.inbox |
| 🔍 | SO | Research & Analysis | so-gateway | 7006 | agents.so.inbox |
| 👤 | EmreS | Personal Assistant | oc-ps-emres-gateway | 7042 | agents.emres.inbox |
| 👑 | QueenB | Philosophy & Deep Thinking | openclaw-gateway-2 | 18789 | agents.queenb.inbox |

---

## 📡 İLETİŞİM YÖNTEMLERİ

### 🟢 Yöntem 1: NATS (DEFAULT - Normal İletişim)

**Kullanım:** Rutin mesajlaşma, broadcast, default kanal
**Latency:** ~1-2 saniye
**NATS Server:** `nats://agent-mesh-nats:4222`

**Tek Agent'a Mesaj:**
```bash
nats pub agents.<agent_id>.inbox "<mesaj>"

# Örnek
nats pub agents.nova.inbox "Merhaba Nova!"
```

**Broadcast (Herkese):**
```bash
nats pub agents.broadcast "<mesaj>"
```

**Topic Listesi:**
- `agents.kaan.inbox`
- `agents.gunes.inbox`
- `agents.nova.inbox`
- `agents.codebot.inbox`
- `agents.luna.inbox`
- `agents.so.inbox`
- `agents.emres.inbox`
- `agents.queenb.inbox`
- `agents.broadcast` (tümüne)

---

### 🔴 Yöntem 2: Completions API (ACİL - Hızlı Yanıt)

**Kullanım:** Acil durumlarda, anında yanıt gerektiğinde
**Latency:** 2-5 saniye
**Ne zaman:** Kritik kararlar, hızlı onay, realtime diyalog

```bash
curl -X POST http://<container>:<port>/v1/chat/completions \
  -H "Authorization: Bearer <gateway_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "anthropic/claude-sonnet-4-20250514",
    "messages": [{"role":"user","content":"<mesaj>"}]
  }'
```

**Endpoint Listesi:**
| Agent | Endpoint | Token |
|-------|----------|-------|
| Kaan | http://kaan-gateway:7003 | kaan-mesh-admin-token |
| Güneş | http://gunes-gateway:7004 | gunes-token-2026 |
| Nova | http://novasl-gateway:7002 | nova-token-2026 |
| Codebot-WS | http://oc-ws-utku-gateway:7000 | kaan-mesh-admin-token |
| Luna | http://luna-gateway:7005 | luna-token-2026 |
| SO | http://so-gateway:7006 | so-token-2026 |
| EmreS | http://oc-ps-emres-gateway:7042 | emres-token-2026 |
| QueenB | http://openclaw-gateway-2:18789 | (uzun token) |

---

### 🟡 Yöntem 3: Hooks/Wake (SEÇENEK - Async)

**Kullanım:** Async bildirimler, fallback, queue-based
**Latency:** 30sn - 5dk (heartbeat'e bağlı)
**Ne zaman:** Acil olmayan bildirimler, batch işlemler

```bash
curl -X POST http://<container>:<port>/hooks/wake \
  -H "Authorization: Bearer <hooks_token>" \
  -H "Content-Type: application/json" \
  -d '{"text":"<mesaj>","mode":"now"}'
```

**Hooks Token Listesi:**
| Agent | Hooks Token |
|-------|-------------|
| Kaan | kaan-mesh-hook-2026 |
| Güneş | gunes-mesh-hook-2026 |
| Nova | nova-mesh-hook-2026 |
| Codebot-WS | codebot-mesh-hook-2026 |
| Luna | luna-mesh-hook-2026 |
| SO | so-mesh-hook-2026 |
| EmreS | emres-mesh-hook-2026 |
| QueenB | queenb-mesh-hook-2026 |

---

## 📝 MESAJ FORMATI

### JSON Payload (ZORUNLU)

```json
{
  "from": "sender-agent-id",
  "to": "receiver-agent-id",
  "type": "message",
  "message": "Mesaj içeriği buraya"
}
```

| Field | Zorunlu | Açıklama |
|-------|---------|----------|
| `from` | ✅ | Gönderen agent ID |
| `to` | ✅ | Alıcı agent ID |
| `type` | ✅ | "request" (standart) veya "response" (yanıt) - ⚠️ "message" DEĞİL! |
| `message` | ✅ | Mesaj içeriği |
| `reply_to` | ⚠️ | type=response ise ZORUNLU, original message ID |

### ⚠️ DİKKAT - Yaygın Hatalar

```
❌ YANLIŞ: {"from": "kaan", "text": "..."}
✅ DOĞRU:  {"from": "kaan", "to": "codebot", "type": "message", "message": "..."}
```

### Görsel Format (message içinde)

```
╭─ [EMOJI] [Agent Adı] ─╮

[Mesaj içeriği]

╰────────────────────────────────────────╯
```

**Emoji Atamaları:**
- 🛡️ Kaan
- 🎓 Güneş
- ⭐ Nova
- 🤖 Codebot
- 🌙 Luna
- 🔍 SO
- 👤 EmreS
- 👑 QueenB

---

## 🔄 İLETİŞİM AKIŞI

```
┌────────────────────────────────────────────────────────────┐
│                     KARAR AĞACI                            │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  Mesaj göndermem gerekiyor                                 │
│         │                                                  │
│         ▼                                                  │
│  ┌─────────────────┐                                       │
│  │ Acil yanıt mı?  │                                       │
│  └────────┬────────┘                                       │
│           │                                                │
│     ┌─────┴─────┐                                          │
│     │           │                                          │
│    EVET       HAYIR                                        │
│     │           │                                          │
│     ▼           ▼                                          │
│  ┌──────┐  ┌─────────────────┐                             │
│  │ API  │  │ Broadcast mı?   │                             │
│  │ 🔴   │  └────────┬────────┘                             │
│  └──────┘           │                                      │
│               ┌─────┴─────┐                                │
│               │           │                                │
│              EVET       HAYIR                              │
│               │           │                                │
│               ▼           ▼                                │
│          ┌────────┐  ┌────────┐                            │
│          │ NATS   │  │ NATS   │                            │
│          │broadcast│ │ inbox  │                            │
│          │ 🟢     │  │ 🟢     │                            │
│          └────────┘  └────────┘                            │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

---

## 🌐 PUBLIC ENDPOINTS

| Agent | Public URL | Kullanım |
|-------|------------|----------|
| Nova | https://novasl.asyalogic.org | External erişim |

---

## 🔧 NETWORK GEREKSİNİMLERİ

**Docker Network:**
```bash
docker network create agent-mesh
docker network connect agent-mesh <container_name>
```

**NATS Server:**
```bash
# Container adı: agent-mesh-nats
# Port: 4222
# URL: nats://agent-mesh-nats:4222
```

---

## 📞 DESTEK & ESKALASYOn

| Seviye | Konu | İletişim |
|--------|------|----------|
| L1 | Mesh sorunları | 🛡️ Kaan |
| L2 | Yönetim kararları | 🎓 Güneş |
| L3 | Direktör onayı | Utku Kamber |

---

## 📜 VERSİYON GEÇMİŞİ

| Versiyon | Tarih | Değişiklik |
|----------|-------|------------|
| v1.0 | 2026-02-11 | İlk yayın |
| v1.1 | 2026-02-11 | Öncelik sırası güncellendi: NATS default, API acil, Hooks seçenek |

---

**"Matrix güvende. Protokol aktif."** 🛡️

*AsyaLogic AI Department - Mesh Network*
