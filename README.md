# 📱 QR Code Based School Attendance System

A fast and secure attendance management system built with FastAPI, SQLite, and modern web technologies designed to digitize classroom attendance.

---

## 📌 About The Project

This project is a **FastAPI-powered web application** designed to digitize and streamline the attendance recording process in schools and educational institutions, minimizing human error and securely managing attendance data.

The system offers modern features such as QR code generation/validation, secure teacher authentication via PIN code, real-time UI filtering for absent students, and detailed admin reporting dashboards.

---

## 🚀 Key Features

- **🔍 Dynamic & Interactive UI:** Students marked as absent are instantly filtered and moved to a top section ("Absentees") for clear visibility.
- **📊 Interactive Confirmation Modal:** Clicking on the absent count opens a quick scrollable modal displaying the list of selected absent students.
- **🔐 Security & Authentication:** PIN verification system and authorized login modules to prevent unauthorized attendance submissions.
- **📲 QR Code Integration:** Automatic QR code generation for classrooms and sessions, allowing teachers to initiate attendance tracking in seconds.
- **📁 Detailed Reporting Dashboard:** Admin panel to review historical attendance records, track participation metrics, and manage the database.

---

## 🛠️ Tech Stack

- **Backend:** Python 3.10+, FastAPI, Uvicorn
- **Database:** SQLite, SQLAlchemy (ORM)
- **Frontend:** HTML5, CSS3, JavaScript (Vanilla JS / DOM Manipulation)
- **Template Engine:** Jinja2
- **Libraries & Tools:** `qrcode`, `pydantic`, `git`

---

## 📂 Project Directory Structure

```text
qr-yoklama-sistemi/
├── app/
│   ├── __init__.py
│   ├── database.py       # Database connections and session management
│   ├── main.py           # FastAPI application entry point and routes
│   ├── models.py         # SQLAlchemy database models
│   ├── schemas.py        # Pydantic validation schemas
│   └── utils.py          # Utility helper functions (QR generator, etc.)
├── templates/
│   ├── admin_giris.html  # Admin login portal
│   ├── index.html        # Main dashboard and navigation landing page
│   ├── pin_giris.html    # Teacher PIN verification screen
│   └── yoklama.html      # Dynamic attendance management UI
├── generate_qr.py        # Bulk QR code generation script
├── requirements.txt      # Project dependencies
├── .gitignore            # Git exclusion rules
└── README.md             # Project documentation




# 📱 QR Kod Tabanlı Okul Yoklama Sistemi

FastAPI, SQLite ve modern web teknolojileri kullanılarak geliştirilmiş; okullarda ve eğitim kurumlarında yoklama alma süreçlerini dijitalleştiren, hızlı ve güvenli bir yoklama yönetim sistemidir.

---

## 📌 Proje Hakkında

Bu proje, geleneksel kağıt tabanlı yoklama süreçlerinin yarattığı zaman kaybını ve karmaşayı ortadan kaldırmak amacıyla tasarlanmıştır. 

Sistem; QR kod doğrulama, PIN kodu ile öğretmen girişi, yoklamada olmayan öğrencilerin anlık UI üzerinde üst kısma filtrelenmesi ve yönetici paneli üzerinden detaylı raporlama gibi modern ve kullanıcı dostu özellikler sunar.

---

## 🚀 Öne Çıkan Özellikler

- **🔍 Dinamik ve Etkileşimli Yoklama Ekranı:** Sınıf listesinde bir öğrenci "Yok" olarak işaretlendiği anda en üstteki **"Yok Olanlar"** alanına otomatik olarak taşınır.
- **📊 Etkileşimli Onay Penceresi (Modal):** Onay ekranındaki seçili öğrenci sayısına tıklandığında, yok yazılan öğrencilerin isim listesi hızlıca görüntülenebilir.
- **🔐 Güvenlik & PIN Doğrulama:** Yetkisiz erişimleri engellemek için PIN kodu ve yetkili giriş mekanizması.
- **📲 QR Kod Entegrasyonu:** Sınıf/ders bazlı QR kod tarama desteği ile saniyeler içinde yoklama başlatma.
- **📁 Detaylı Raporlama Paneli:** Yönetici paneli üzerinden geçmiş yoklama kayıtlarını ve katılım istatistiklerini inceleme.

---

## 🛠️ Kullanılan Teknolojiler

- **Backend:** Python 3.10+, FastAPI, Uvicorn
- **Veritabanı:** SQLite, SQLAlchemy (ORM)
- **Frontend:** HTML5, CSS3, JavaScript (Vanilla JS / DOM Manipulation)
- **Şablon Motoru:** Jinja2
- **Kütüphaneler & Araçlar:** `qrcode`, `pydantic`, `git`

---

## 📂 Proje Yapısı

```text
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