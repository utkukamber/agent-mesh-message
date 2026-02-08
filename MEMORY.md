# MEMORY.md - Kaan'ın Notları

## TODO / Bekleyen İşler

### 🖥️ Claude Code Bridge (v0.2 Fikri)
- **Tarih:** 2026-02-08
- **Talep eden:** Utku Bey
- **Açıklama:** Agent'lar Claude Code CLI'yi kendi bridge'leri üzerinden kullanabilsin
- **Özellikler:**
  - "Claude Code ile görüşmek istiyorum" dediğinde
  - Pencerede "claude code" olarak görünsün
  - Agent'ın kendi bridge'i üzerinden çalışsın
- **Durum:** 💡 Fikir (v0.2)

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

---

## Çözülen Sorunlar

(henüz yok)

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
