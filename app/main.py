import os
import sys
from datetime import date, datetime, timezone

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI, Depends, Request, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import func
from sqlalchemy.orm import Session
from starlette.middleware.sessions import SessionMiddleware

from database import engine, Base, SessionLocal, ensure_schema
from models import Sinif, Ogrenci, Yoklama
from schemas import YoklamaGuncelle, YoklamaKaydetIstek
from utils import veli_sms_gonder_simule, pin_dogrula, sinif_pin_anahtari

ADMIN_PIN = os.getenv("ADMIN_PIN", "9999")

Base.metadata.create_all(bind=engine)
ensure_schema()

app = FastAPI(title="QR Okul Yoklama Sistemi")

SECRET_KEY = os.getenv("SECRET_KEY", "qr-yoklama-gizli-anahtar-degistirin")
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "app", "static")), name="static")
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

DEMO_OGRENCI_SABLONU = [
    ("101", "Ali Yılmaz", "5551010101"),
    ("102", "Ayşe Kaya", "5551010102"),
    ("103", "Mehmet Demir", "5551010103"),
    ("104", "Zeynep Çelik", "5551010104"),
]


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def sinif_pin_dogrulandi(request: Request, sinif_kodu: str) -> bool:
    return request.session.get(sinif_pin_anahtari(sinif_kodu), False) is True


def admin_pin_dogrulandi(request: Request) -> bool:
    return request.session.get("admin_auth", False) is True


def admin_pin_dogrula(pin: str) -> bool:
    return pin == ADMIN_PIN


def sinif_durumlari_olustur(db: Session, grade_filter: str = None) -> list[dict]:
    """Sınıf durumlarını getir, opsiyonel olarak sınıf seviyesine göre filtrele."""
    bugun = date.today()
    siniflar = db.query(Sinif).order_by(Sinif.kod).all()
    
    # Grade filter: "9", "10", "11", "12"
    if grade_filter:
        siniflar = [s for s in siniflar if s.kod.startswith(grade_filter)]
    
    sonuclar = []

    for sinif in siniflar:
        ogrenci_ids = [ogrenci.id for ogrenci in sinif.ogrenciler]
        toplam_ogrenci = len(ogrenci_ids)

        if not ogrenci_ids:
            sonuclar.append({
                "kod": sinif.kod,
                "durum": "bekliyor",
                "gelmeyen": None,
                "toplam": 0,
                "son_tarih": None,
            })
            continue

        bugunun_yoklamalari = (
            db.query(Yoklama)
            .filter(
                Yoklama.ogrenci_id.in_(ogrenci_ids),
                func.date(Yoklama.tarih) == bugun,
            )
            .all()
        )

        if not bugunun_yoklamalari:
            sonuclar.append({
                "kod": sinif.kod,
                "durum": "bekliyor",
                "gelmeyen": None,
                "toplam": toplam_ogrenci,
                "son_tarih": None,
            })
            continue

        gelmeyen = sum(1 for kayit in bugunun_yoklamalari if not kayit.durum)
        son_tarih = max(kayit.tarih for kayit in bugunun_yoklamalari)

        sonuclar.append({
            "kod": sinif.kod,
            "durum": "tamamlandi",
            "gelmeyen": gelmeyen,
            "toplam": toplam_ogrenci,
            "son_tarih": son_tarih,
        })

    return sonuclar


def demo_ogrenciler_olustur(sinif_kodu: str, sinif_id: int) -> list[Ogrenci]:
    prefix = sinif_kodu.replace("-", "")
    return [
        Ogrenci(
            okul_no=f"{prefix}-{no}",
            ad_soyad=ad_soyad,
            veli_tel=f"+90{tel}",
            sinif_id=sinif_id,
        )
        for no, ad_soyad, tel in DEMO_OGRENCI_SABLONU
    ]


def veli_tel_al(ogrenci: Ogrenci) -> str:
    if ogrenci.veli_tel:
        return ogrenci.veli_tel
    return f"+9055510{ogrenci.id:04d}"


def sinif_getir_veya_olustur(db: Session, sinif_kodu: str) -> Sinif:
    """Sınıfı varsa getir, yoksa oluştur ve demo öğrenciler ekle."""
    sinif = db.query(Sinif).filter(Sinif.kod == sinif_kodu).first()
    if sinif:
        return sinif

    yeni_sinif = Sinif(kod=sinif_kodu)
    db.add(yeni_sinif)
    db.commit()
    db.refresh(yeni_sinif)

    db.add_all(demo_ogrenciler_olustur(sinif_kodu, yeni_sinif.id))
    db.commit()
    return yeni_sinif


@app.get("/")
def idare_canli_takip(request: Request, db: Session = Depends(get_db), grade: str = None):
    """İdare Canlı Takip Paneli"""
    if not admin_pin_dogrulandi(request):
        return RedirectResponse(url="/admin-giris", status_code=302)
    
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "sinif_durumlari": sinif_durumlari_olustur(db, grade),
            "bugun": date.today(),
            "selected_grade": grade,
        },
    )


@app.get("/admin-giris")
def admin_giris(request: Request):
    """Admin PIN girişi sayfası"""
    return templates.TemplateResponse(
        request=request,
        name="admin_giris.html",
        context={"hata": None},
    )


@app.post("/admin-giris")
async def admin_giris_post(request: Request):
    """Admin PIN doğrulama"""
    form = await request.form()
    pin = (form.get("pin") or "").strip()

    if not admin_pin_dogrula(pin):
        return templates.TemplateResponse(
            request=request,
            name="admin_giris.html",
            context={"hata": "Geçersiz PIN. Tekrar deneyin."},
            status_code=401,
        )

    request.session["admin_auth"] = True
    return RedirectResponse(url="/", status_code=303)


@app.get("/admin-logout")
def admin_logout(request: Request):
    """Admin Logout"""
    request.session.clear()
    return RedirectResponse(url="/admin-giris", status_code=302)


@app.post("/api/tum-yoklamalari-sifirla")
def tum_yoklamalari_sifirla(request: Request, db: Session = Depends(get_db)):
    """Tüm yoklama verilerini siler ve baştan başlatır."""
    if not admin_pin_dogrulandi(request):
        raise HTTPException(status_code=401, detail="Admin doğrulaması gerekli.")
    
    # Tüm yoklamaları sil
    db.query(Yoklama).delete()
    db.commit()
    
    return {
        "status": "success",
        "message": "Tüm yoklamalar sıfırlandı. Tüm sınıflar 'Yoklama Bekleniyor' durumuna döndü."
    }


@app.get("/sinif/{sinif_kodu}")
def sinif_yoklama_sayfasi(request: Request, sinif_kodu: str, db: Session = Depends(get_db)):
    """Öğretmenin QR okutunca açacağı mobil ekran"""
    sinif_getir_veya_olustur(db, sinif_kodu)

    if not sinif_pin_dogrulandi(request, sinif_kodu):
        return templates.TemplateResponse(
            request=request,
            name="pin_giris.html",
            context={"sinif_kodu": sinif_kodu, "hata": None},
        )

    sinif = db.query(Sinif).filter(Sinif.kod == sinif_kodu).first()
    ogrenciler = db.query(Ogrenci).filter(Ogrenci.sinif_id == sinif.id).all()

    return templates.TemplateResponse(
        request=request,
        name="yoklama.html",
        context={"sinif_kodu": sinif_kodu, "ogrenciler": ogrenciler},
    )


@app.post("/sinif/{sinif_kodu}/giris")
async def sinif_pin_giris(request: Request, sinif_kodu: str, db: Session = Depends(get_db)):
    """Öğretmen PIN doğrulama"""
    sinif_getir_veya_olustur(db, sinif_kodu)

    form = await request.form()
    pin = (form.get("pin") or "").strip()

    if not pin_dogrula(pin):
        return templates.TemplateResponse(
            request=request,
            name="pin_giris.html",
            context={"sinif_kodu": sinif_kodu, "hata": "Geçersiz PIN. Tekrar deneyin."},
            status_code=401,
        )

    request.session[sinif_pin_anahtari(sinif_kodu)] = True
    return RedirectResponse(url=f"/sinif/{sinif_kodu}", status_code=303)


@app.post("/api/yoklama-kaydet")
def yoklama_kaydet(
    request: Request,
    istek: YoklamaKaydetIstek,
    db: Session = Depends(get_db),
):
    """Toplu yoklama kayıt ve SMS simülasyon rotası"""
    sinif_kodu = istek.sinif_kodu
    liste = istek.liste
    
    if not sinif_pin_dogrulandi(request, sinif_kodu):
        raise HTTPException(status_code=401, detail="Öğretmen PIN doğrulaması gerekli.")

    sinif = db.query(Sinif).filter(Sinif.kod == sinif_kodu).first()
    if not sinif:
        raise HTTPException(status_code=404, detail="Sınıf bulunamadı.")

    sinif_ogrenci_ids = {
        ogrenci.id
        for ogrenci in db.query(Ogrenci).filter(Ogrenci.sinif_id == sinif.id).all()
    }

    gonderilen_sms_sayisi = 0
    gelmeyen_sayisi = 0
    bugun = date.today()

    for item in liste:
        if item.ogrenci_id not in sinif_ogrenci_ids:
            raise HTTPException(status_code=403, detail="Geçersiz öğrenci kaydı.")

        ogrenci = db.query(Ogrenci).filter(Ogrenci.id == item.ogrenci_id).first()
        if not ogrenci:
            continue

        if not item.durum:
            gelmeyen_sayisi += 1

        mevcut_kayit = (
            db.query(Yoklama)
            .filter(
                Yoklama.ogrenci_id == ogrenci.id,
                func.date(Yoklama.tarih) == bugun,
            )
            .first()
        )

        onceki_durum = mevcut_kayit.durum if mevcut_kayit else None

        if mevcut_kayit:
            mevcut_kayit.durum = item.durum
            mevcut_kayit.tarih = datetime.now(timezone.utc)
        else:
            db.add(Yoklama(ogrenci_id=ogrenci.id, durum=item.durum))

        if not item.durum and onceki_durum is not False:
            veli_sms_gonder_simule(ogrenci.ad_soyad, veli_tel=veli_tel_al(ogrenci))
            gonderilen_sms_sayisi += 1

    db.commit()
    return {
        "status": "success",
        "message": f"Yoklama kaydedildi. {gonderilen_sms_sayisi} veliye SMS gönderildi.",
        "sms_sayisi": gonderilen_sms_sayisi,
        "gelmeyen_sayisi": gelmeyen_sayisi,
    }
