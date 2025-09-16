# Mini ChatBot V1

Terminal üzerinden çalışan, kural tabanlı basit bir sohbet botu.  
Türkçe etkileşim destekler ve küçük ek özellikler içerir: yapılacaklar listesi, basit hesap makinesi, tarih–saat bilgisi gibi.

---

## Özellikler
- **Selamlaşma:** `selam`, `merhaba`, `naber` gibi kelimelere dostça cevap verir.
- **Zaman Bilgisi:** `saat`, `tarih`, `zaman` gibi komutlarla anlık tarih ve saati gösterir.
- **Yardım Menüsü:** `yardım` yazarak tüm komutların listesini görebilirsiniz.
- **Basit Hesap Makinesi:**
  - `2+3*4` gibi matematiksel ifadeleri güvenli şekilde hesaplar.
  - Sadece sayısal karakter ve `+ - * / % ** ()` işleçlerini destekler.
- **Todo (Yapılacaklar) Listesi:**
  - `todo ekle <metin>` → yeni yapılacak ekler.
  - `todo liste` → mevcut yapılacakları listeler.
  - `hepsini sil` → listeyi temizler.
- **Küçük Bilgi Cevapları:**  
  - `python nedir`, `pandas nedir`, `hava` gibi hazır mini FAQ.
- **Duygu Tepkisi:** “üzgün”, “moralim bozuk” gibi ifadelere kısa destek mesajı döner.
- **Çıkış:** `q`, `çık`, `exit` yazarak sohbeti sonlandırabilirsiniz.

---

## Kurulum

1. Python 3.8+ kurulu olmalı.
2. Depoyu klonlayın:
   ```bash
   git clone https://github.com/<kullanici-adiniz>/miniChatBot.git
   cd miniChatBot
