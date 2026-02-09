# MEMORY.md - Kaan'ın Notları

## TODO / Bekleyen İşler

### 🖥️ Claude Code Bridge (v0.2)
- **Tarih:** 2026-02-08
- **Talep eden:** Utku Bey
- **Açıklama:** Agent'lar Claude Code CLI'yi kendi bridge'leri üzerinden kullanabilsin
- **Özellikler:**
  - "Claude Code ile görüşmek istiyorum" dediğinde
  - Pencerede "claude code" olarak görünsün
  - Agent'ın kendi bridge'i üzerinden çalışsın
- **Durum:** 📋 v0.2 Planlandı

### 🌐 Cross-Gateway Routing (v0.2) - KRİTİK
- **Tarih:** 2026-02-09
- **Talep eden:** Direktör (bug fix sırasında tespit)
- **Açıklama:** Farklı container'lardaki agent'lar arası mesh iletişimi
- **Sorun:** sessions_send sadece aynı gateway içinde çalışıyor
- **Çözüm:** HTTP bridge + token yönetimi veya NATS pub/sub
- **Durum:** 📋 v0.2 Planlandı (KRİTİK)

### 🎨 mesh-fx (Admin Terminal Efektleri)
- **Tarih:** 2026-02-08
- **Talep eden:** Utku Bey
- **Açıklama:** Admin-only terminal efektleri ve animasyonlar
- **Özellikler:**
  - ANSI renk değiştirme (kırmızı, cyan, vb.)
  - Dinamik mesaj penceresi stilleri
  - ASCII animasyonları (matrix rain, fire, pulse)
  - `rich`, `asciimatics` kütüphaneleri kullanılacak
- **Komut örneği:** `mesh-fx --color red "MESAJ"`
- **Durum:** ⏳ Beklemede (token işi öncelikli)

### 🤖 mesh-ansible (v0.3)
- **Tarih:** 2026-02-08
- **Talep eden:** Utku Bey
- **Açıklama:** Ansible ile mesh ağı yönetimi
- **Özellikler:**
  - Inventory-based agent registry
  - Template-based bridge deployment
  - Rolling updates
  - Ansible Vault ile secret management
  - Health check playbooks
- **Yapı:**
  ```
  mesh-ansible/
  ├── inventory/ (production, staging)
  ├── roles/ (openclaw-gateway, mesh-bridge, agent-persona)
  ├── playbooks/ (deploy, update, health)
  └── group_vars/ (Vault encrypted)
  ```
- **Durum:** 📋 v0.3 Planlandı

---

## Çözülen Sorunlar

### ✅ Session Routing Bug (2026-02-08)
- **Sorun:** Mesh mesajları openai:uuid session'larına düşüyordu
- **Çözüm:** x-openclaw-session-key header + user field eklendi
- **Kim çözdü:** Kaan (analiz) + Codebot (implement)
- **Commit:** 50fd78e (mesh-bridge.py)

---

## Notlar

- Token revoke sorunu araştırılıyor (2026-02-08)

---

## Background Task Formatı

Utku Bey'den gelen format:
- `[background:N]` veya `[background task:N]`
- N = task numarası
- Paralel/arka planda çalışılacak işler

---

## Aktif Background Tasks

### [background task:1] - Risk Analizi
- **Tarih:** 2026-02-08
- **Görev:** Nova ile mesh-events yapısının generic olup olmadığını analiz et
- **Durum:** ⏳ Nova'ya erişim bekleniyor
- **Hedef:** v0.1 sonrası
