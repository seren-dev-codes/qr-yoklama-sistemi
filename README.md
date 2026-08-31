# 📱 QR Kod Tabanlı Okul Yoklama Sistemi

FastAPI, SQLite ve modern web teknolojileri kullanılarak geliştirilmiş; okullarda ve eğitim kurumlarında yoklama alma süreçlerini dijitalleştiren, hızlı ve güvenli bir yoklama yönetim sistemidir.

[![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![SQLite](https://img.shields.io/badge/SQLite-3-003B57?style=flat-square&logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![JavaScript](https://img.shields.io/badge/JavaScript-ES6+-F7DF1E?style=flat-square&logo=javascript&logoColor=black)](https://developer.mozilla.org/en-US/docs/Web/JavaScript)

---

##  Proje Hakkında

Bu proje, geleneksel kağıt tabanlı yoklama süreçlerinin yarattığı zaman kaybını ve karmaşayı ortadan kaldırmak amacıyla tasarlanmıştır. 

Sistem; QR kod doğrulama, PIN kodu ile öğretmen girişi, yoklamada olmayan öğrencilerin anlık UI üzerinde üst kısma filtrelenmesi ve yönetici paneli üzerinden detaylı raporlama gibi modern ve kullanıcı dostu özellikler sunar.

---

##  Öne Çıkan Özellikler

- ** Dinamik ve Etkileşimli Yoklama Ekranı:** Sınıf listesinde bir öğrenci "Yok" olarak işaretlendiği anda en üstteki **"Yok Olanlar"** alanına otomatik olarak taşınır.
- **📊 Etkileşimli Onay Penceresi (Modal):** Onay ekranındaki seçili öğrenci sayısına tıklandığında, yok yazılan öğrencilerin isim listesi hızlıca görüntülenebilir.
- ** Güvenlik & PIN Doğrulama:** Yetkisiz erişimleri engellemek için PIN kodu ve yetkili giriş mekanizması.
- ** QR Kod Entegrasyonu:** Sınıf/ders bazlı QR kod tarama desteği ile saniyeler içinde yoklama başlatma.
- ** Detaylı Raporlama Paneli:** Yönetici paneli üzerinden geçmiş yoklama kayıtlarını ve katılım istatistiklerini inceleme.

---

## 🛠️ Kullanılan Teknolojiler

- **Backend:** Python 3.10+, FastAPI, Uvicorn
- **Veritabanı:** SQLite, SQLAlchemy (ORM)
- **Frontend:** HTML5, CSS3, JavaScript (Vanilla JS / DOM Manipulation)
- **Şablon Motoru:** Jinja2
- **Kütüphaneler & Araçlar:** `qrcode`, `pydantic`, `git`

---

git clone [https://github.com/seren-dev-codes/qr-yoklama-sistemi.git](https://github.com/seren-dev-codes/qr-yoklama-sistemi.git)
cd qr-yoklama-sistemi

## 💻 Kurulum ve Çalıştırma

Projeyi kendi bilgisayarınızda çalıştırmak için terminalinizde sırasıyla aşağıdaki komutları çalıştırın:

```bash
# 1. Depoyu klonlayın ve klasöre girin
git clone [https://github.com/seren-dev-codes/qr-yoklama-sistemi.git](https://github.com/seren-dev-codes/qr-yoklama-sistemi.git)
cd qr-yoklama-sistemi

# 2. Sanal ortamı oluşturun ve aktif edin (Windows)
python -m venv venv
venv\Scripts\activate

# (macOS/Linux kullanıyorsanız 2. adım yerine bunu çalıştırın:)
# python3 -m venv venv && source venv/bin/activate

# 3. Gerekli kütüphaneleri yükleyin
pip install -r requirements.txt

# 4. Sunucuyu başlatın
uvicorn app.main:app --reload

qr-yoklama-sistemi/
├── app/
│   ├── __init__.py
│   ├── database.py       # Veritabanı bağlantısı ve oturum yönetimi
│   ├── main.py           # FastAPI ana uygulama ve rotalar (routes)
│   ├── models.py         # SQLAlchemy veritabanı modelleri
│   ├── schemas.py        # Pydantic doğrulama şemaları
│   └── utils.py          # Yardımcı fonksiyonlar (QR üretimi vb.)
├── templates/
│   ├── admin_giris.html  # Yönetici giriş paneli
│   ├── index.html        # Ana sayfa ve genel yönlendirmeler
│   ├── pin_giris.html    # Öğretmen PIN doğrulama ekranı
│   └── yoklama.html      # Dinamik yoklama alma ekranı
├── generate_qr.py        # Toplu QR kod üretme betiği
├── requirements.txt      # Proje bağımlılıkları
├── .gitignore            # Git tarafından yoksayılacak dosyalar
└── README.md             # Proje dokümantasyonu
