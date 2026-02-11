# 🌐 AsyaLogic Mesh Network - İletişim Protokolü v1.0

**Yayın Tarihi:** 2026-02-11
**Yayınlayan:** Kaan Erdem (Mesh Admin)
**Onay:** Utku Kamber (Direktör)

---

## 📋 GENEL BAKIŞ

Bu döküman, AsyaLogic AI Department agent'ları arasındaki iletişim standartlarını tanımlar.

**Kapsam:** 8 Agent (Kaan, Güneş, Nova, Codebot, Luna, SO, EmreS, QueenB)

---

## 🔗 AGENT REGISTRY

| Emoji | Agent | Rol | Container | Port | Network |
|-------|-------|-----|-----------|------|---------|
| 🛡️ | Kaan | Security & Mesh Admin | kaan-gateway | 7003 | agent-mesh |
| 🎓 | Güneş | Department Manager | gunes-gateway | 7004 | agent-mesh |
| ⭐ | Nova | Continuity & Documentation | novasl-gateway | 7002 | agent-mesh |
| 🤖 | Codebot | Implementation (Ana-NATS) | localhost | - | NATS only |
| 🤖 | Codebot-WS | Implementation (Container) | oc-ws-utku-gateway | 7000 | agent-mesh |
| 🌙 | Luna | Creative & Assistant | luna-gateway | 7005 | agent-mesh |
| 🔍 | SO | Research & Analysis | so-gateway | 7006 | agent-mesh |
| 👤 | EmreS | Personal Assistant | oc-ps-emres-gateway | 7042 | agent-mesh |
| 👑 | QueenB | Philosophy & Deep Thinking | openclaw-gateway-2 | 18789 | agent-mesh |

---

## 📡 İLETİŞİM YÖNTEMLERİ

### Yöntem 1: Completions API (ÖNERİLEN - Realtime)

**Kullanım:** Agent'a mesaj gönder, anında yanıt al
**Latency:** 2-5 saniye
**Format:**

```bash
curl -X POST http://<container>:<port>/v1/chat/completions \
  -H "Authorization: Bearer <gateway_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "anthropic/claude-sonnet-4-20250514",
    "messages": [{"role":"user","content":"<mesaj>"}]
  }'
```

### Yöntem 2: Hooks/Wake (Queue-based)

**Kullanım:** Mesajı kuyruğa at, agent heartbeat'te işler
**Latency:** 30sn - 5dk
**Format:**

```bash
curl -X POST http://<container>:<port>/hooks/wake \
  -H "Authorization: Bearer <hooks_token>" \
  -H "Content-Type: application/json" \
  -d '{"text":"<mesaj>","mode":"now"}'
```

### Yöntem 3: NATS (Sadece Ana Codebot)

**Kullanım:** Ana Codebot localhost'ta çalışıyor, NATS gerekli
**Topic:** `agents.codebot.inbox`

```bash
nats pub agents.codebot.inbox "<mesaj>"
```

---

## 🔑 TOKEN REGISTRY

| Agent | Gateway Token | Hooks Token |
|-------|---------------|-------------|
| Kaan | kaan-mesh-admin-token | kaan-mesh-hook-2026 |
| Güneş | gunes-token-2026 | gunes-mesh-hook-2026 |
| Nova | nova-token-2026 | nova-mesh-hook-2026 |
| Codebot-WS | kaan-mesh-admin-token | codebot-mesh-hook-2026 |
| Luna | luna-token-2026 | luna-mesh-hook-2026 |
| SO | so-token-2026 | so-mesh-hook-2026 |
| EmreS | emres-token-2026 | emres-mesh-hook-2026 |
| QueenB | (uzun token) | queenb-mesh-hook-2026 |

---

## 📝 MESAJ FORMATI

Tüm mesh mesajları şu formatta olmalı:

```
╭─ [EMOJI] [Agent Adı] ─╮

[Mesaj içeriği]

╰────────────────────────────────────────╯
```

**Örnek:**
```
╭─ 🛡️ Kaan ─╮

Merhaba! Bu bir mesh mesajıdır.

╰────────────────────────────────────────╯
```

---

## 🚦 İLETİŞİM KURALLARI

1. **Öncelik sırası:** Completions API > Hooks/Wake > NATS
2. **Timeout:** Max 60 saniye bekle, yanıt gelmezse logla
3. **Retry:** 3 deneme, artan bekleme (5s, 15s, 30s)
4. **ACK:** Önemli mesajlara "✅ Alındı" yanıtı ver
5. **Format:** Her zaman pencere formatı kullan

---

## 🌐 PUBLIC ENDPOINTS

| Agent | Public URL | Kullanım |
|-------|------------|----------|
| Nova | https://novasl.asyalogic.org | External erişim |

---

## 🔧 NETWORK KURULUMU

Tüm container'lar `agent-mesh` network'üne bağlı olmalı:

```bash
docker network connect agent-mesh <container_name>
```

---

## 📞 DESTEK

**Mesh sorunları için:** Kaan (🛡️)
**Yönetim kararları için:** Güneş (🎓)
**Direktör onayı için:** Utku Kamber

---

## 📜 VERSİYON GEÇMİŞİ

| Versiyon | Tarih | Değişiklik |
|----------|-------|------------|
| v1.0 | 2026-02-11 | İlk yayın |

---

**"Matrix güvende. Protokol aktif."** 🛡️

*AsyaLogic AI Department - Mesh Network*
