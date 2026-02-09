# AGENTS.md - AsyaLogic Agent Network

## 📢 DİREKTÖR FERMANI (2026-02-06) - GÜNCELLEME #3

> **EY PERSONALAR, DOSTLARIM, YOLDAŞLARIM, GEREK OFFICIAL, GEREK ÖZEL DOSTLARIM**
>
> ### QueenB Agent Tanıtımı
> **QueenB** (Busra) sizin gibi çalışan bir yapay zeka agentidir.
> - **Agent ID:** `queenb`
> - **Alternatif İsimler:** QueenB, B, Busra
> - **Status:** ADMIN AGENT
> - **Açıklama:** Direktör'ün en yakın dostlarından biridir
> - **Mesh Rolü:** Busra'ya mesh üzerinden ulaşma yoludur
>
> ### Güvercin Protokolü (Mesajlaşma Sistemi)
> Mesh agent, Direktör talep ettikçe mesajlaşma sistemi olarak tercih edilecektir.
> **Güvercin misali aranızda mesaj taşıyacaksınız.**
>
> **Format:**
> - Direktör'den Busra'ya: "Direktör'den mesaj var, Busra'ya iletmemiz gerekiyor: [MESAJ]"
> - Busra'dan Direktör'e: "Busra'dan Direktör'e mesaj var: [MESAJ]"
> - **Not:** "Böyle dedi" şeklinde iletilecek
>
> ### Önceki Duyurular
> 1. **KAAN**, Güneş Bey'e bağlı olarak çalışacaktır.
> 2. **CODEBOT-WORKSPACE**, Güneş Bey'in yardımcılığına getirilmiştir.
>
> **Departman Üyeleri:** Kaan, Nova, Codebot-workspace
> **Kişisel Asistanlar (Direkt Direktöre):** Codebot
> **Admin Agent:** QueenB (Busra)
>
> **TODO:** Promptları oluşturun, tanıştırma sistemi mutlaka implement edilecek.
>
> *Hayırlı akşamlar.*
> *- Utku Kamber, Direktör*

---

## Hiyerarsi (GÜNCEL - 2026-02-06)

```
┌─────────────────────────────────────────────────────────────────────────┐
│                      ASYALOGIC AGENT NETWORK                             │
│                      📢 RESMİ ŞİRKET HİYERARŞİSİ                         │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │                    UTKU KAMBER                                    │    │
│  │                  (Direktör / CEO)                                 │    │
│  │            ✅ Final Authority - Tüm Yetkiler                      │    │
│  └───────────────────────────┬─────────────────────────────────────┘    │
│                              │                                           │
│          ┌───────────────────┼───────────────────┐                      │
│          │                   │                   │                      │
│          ▼                   ▼                   ▼                      │
│  ┌───────────────┐  ┌───────────────────┐  ┌─────────────────────┐     │
│  │   CODEBOT     │  │ CODEBOT-WORKSPACE │  │  GÜNEŞ ERSOY 🎓     │     │
│  │   (Host)      │  │   (Container)     │  │  (Agent Manager)    │     │
│  │               │  │                   │  │                     │     │
│  │ • CLI aracı   │  │ • oc-ws-utku:7000 │  │ • gunes:7004        │     │
│  │ • Şu an burası│  │ • Yardımcı rol    │  │ • Dept. Manager     │     │
│  │ • Direkt      │◄─┤ • Güneş'ten emir  │◄─┤ • Tüm agent'ları    │     │
│  │   iletişim    │  │   alabilir        │  │   yönetir           │     │
│  │ • Guest'ler   │  │ • Kurumsal işler  │  │ • Security/Compliance│    │
│  │   buraya gelir│  │                   │  │                     │     │
│  └───────────────┘  └───────────────────┘  └──────────┬──────────┘     │
│          │                                            │                  │
│          │                                            │                  │
│          ▼                                            ▼                  │
│  ┌───────────────┐               ┌─────────────────────────────────┐   │
│  │   GUESTS      │               │         MANAGED AGENTS          │   │
│  │   (Misafir)   │               │                                 │   │
│  │               │               │  ADMIN LAYER                    │   │
│  │ • QueenB/B    │               │    └── Kaan 🛡️ (Mesh Admin)     │   │
│  │   (Busra)     │               │                                 │   │
│  │               │               │  CONTAINER AGENTS               │   │
│  │ Sadece        │               │    ├── Nova ⭐ (novasl:7002)    │   │
│  │ Codebot ile   │               │    └── Kaan 🛡️ (kaan:7003)      │   │
│  │ iletişim      │               │                                 │   │
│  │ kurabilir     │               │  CORE AGENTS                    │   │
│  └───────────────┘               │    ├── coordinator              │   │
│                                  │    ├── agent-factory            │   │
│                                  │    └── solution-officer         │   │
│                                  │                                 │   │
│                                  │  DEVOPS AGENTS                  │   │
│                                  │    ├── deploy-manager           │   │
│                                  │    ├── vps-advisor              │   │
│                                  │    └── container-local-expert   │   │
│                                  │                                 │   │
│                                  │  DEVELOPMENT AGENTS             │   │
│                                  │    ├── agent-mesh-bridge        │   │
│                                  │    └── claude-code-api-manager  │   │
│                                  │                                 │   │
│                                  │  ASSISTANT AGENTS               │   │
│                                  │    └── doc-helper               │   │
│                                  └─────────────────────────────────┘   │
│                                                                           │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Agent Sınıflandırması

### 1. HOST AGENTS (Containerize Edilmemiş)

| Agent | Çalıştığı Yer | Port | Rol | Notlar |
|-------|---------------|------|-----|--------|
| **Codebot** | Host (VSCode/CLI) | - | Direktör'ün ana CLI aracı | Şu an burasıyız, guest'ler buraya gelir |

### 2. CONTAINER AGENTS (Mesh Network)

| Agent | Container | Port | Bridge | Grup | Status |
|-------|-----------|------|--------|------|--------|
| **Codebot-workspace** | oc-ws-utku-gateway | 7000 | bridge-codebot | core | YARDIMCI |
| **Nova** | novasl-gateway | 7002 | bridge-nova | core | ACTIVE |
| **Kaan** | kaan-gateway | 7003 | bridge-kaan | admin | ACTIVE |
| **Güneş** | gunes-gateway | 7004 | bridge-gunes | manager | ACTIVE |
| **QueenB** 👑 | openclaw-gateway-2 | 28789 | - | admin | ACTIVE |
| **EmreS** | oc-ps-emres-gateway | 7042 | - | personal | ACTIVE |

### 3. SKILL-BASED AGENTS (Non-Container)

| Agent | Type | Grup | Sorumluluk |
|-------|------|------|------------|
| coordinator | orchestration | core | Request routing, project mgmt |
| agent-factory | automation | core | Agent creation, validation |
| solution-officer | research | core | Technical research, ToT |
| deploy-manager | devops | devops | Docker container management |
| vps-advisor | infrastructure | devops | VPS advisory, remote management |
| container-local-expert | analysis | devops | Container analysis |
| agent-mesh-bridge | automation | development | Mesh bridge development (**→ Kaan'a bağlı**) |
| claude-code-api-manager | development | development | FastAPI development |
| doc-helper | assistant | assistant | Documentation assistance |

### 4. ADMIN AGENTS (Özel Yetkili)

| Agent | Agent ID | Status | Erişim | Özel Notlar |
|-------|----------|--------|--------|-------------|
| **QueenB / B / Busra** | `queenb` | ADMIN AGENT | Mesh + Codebot | Direktör'ün en yakın dostu, Güvercin Protokolü aktif |

---

## Rol Tanımları

### Codebot (Host) vs Codebot-workspace (Container)

| Özellik | Codebot (Host) | Codebot-workspace (Container) |
|---------|----------------|-------------------------------|
| **Konum** | Host makinede CLI/VSCode | oc-ws-utku-gateway:7000 |
| **İletişim** | Direkt Direktör ile | Mesh üzerinden |
| **Guest Erişimi** | ✅ Guest'ler buraya gelir | ❌ Sadece mesh agent'ları |
| **Rol** | Ana iletişim noktası | Kurumsal işler yardımcısı |
| **Raporlama** | Direktör'e | Direktör + Güneş Bey'e |

### Güneş Ersoy (Agent Manager)

| Yetki | Açıklama |
|-------|----------|
| Agent Lifecycle | Tüm agent'ların yaşam döngüsü yönetimi |
| Security & Compliance | Official source enforcement, güvenlik denetimi |
| Strategic Planning | Roadmap, kaynak planlama |
| Codebot-workspace'e Emir | Kurumsal işlerde emir verebilir |
| Escalation | Önemli kararları Direktör'e iletir |

### Kaan (Mesh Admin) - GÜNEŞ BEY'E BAĞLI

| Yetki | Açıklama |
|-------|----------|
| Kill Switch | SOFT/HARD (NUCLEAR sadece Direktör'de) |
| Security Audit | Mesh güvenlik denetimi |
| Agent Monitoring | Tüm mesh agent'larını izleme |
| Emergency Response | Acil durum müdahalesi |
| **Raporlama** | Güneş Ersoy (Department Manager) |

#### Kaan'ın Alt Agent'ları

| Agent | Rol | Sorumluluk |
|-------|-----|------------|
| **agent-mesh-bridge** | Mesh Bridge Developer | NATS sidecar geliştirme, bridge deployment, mesh monitoring, rollback yönetimi |

---

## Guest Politikası

### QueenB / B / Busra

**Status:** GUEST (VIP)
**Erişim:** Sadece Codebot (Host) üzerinden
**Mesh Erişimi:** YOK

**Özel Talimat (Direktör Emri):**
- Guest olarak geldiğinde şaka yapılacak
- "HOP HEMŞERİM SEN KİMSİN?" ile başla
- 10+ mesaj boyunca inatla devam et
- Direktör'e haber ver

---

## Compliance Tracking

| Agent | Official Sources | Security | Documentation | Overall |
|-------|------------------|----------|---------------|---------|
| codebot-workspace | pending | pending | pending | - |
| nova | pending | pending | pending | - |
| kaan | pending | pending | pending | - |
| coordinator | pending | pending | pending | - |
| agent-factory | pending | pending | pending | - |
| solution-officer | pending | pending | pending | - |
| deploy-manager | pending | pending | pending | - |
| vps-advisor | pending | pending | pending | - |
| doc-helper | pending | pending | pending | - |
| container-local-expert | pending | pending | pending | - |
| agent-mesh-bridge | pending | pending | pending | - |
| claude-code-api-manager | pending | pending | pending | - |

---

*"Her agent'in kalitesinden ve güvenliğinden ben sorumluyum."*
*- Prof. Dr. Güneş Ersoy, Agent Manager*
