import os
import socket

import qrcode

OGRETMEN_PIN = os.getenv("OGRETMEN_PIN", "1234")


def pin_dogrula(pin: str) -> bool:
    return pin == OGRETMEN_PIN


def sinif_pin_anahtari(sinif_kodu: str) -> str:
    return f"sinif_{sinif_kodu}_auth"


def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"


def qr_kod_uret(sinif_kodu: str, hedef_klasor: str = "qrcodes", port: int = 8000):
    """Sınıf için QR kod üretir ve qrcodes/ klasörüne kaydeder."""
    if not os.path.exists(hedef_klasor):
        os.makedirs(hedef_klasor)

    host = get_local_ip()
    url = f"http://{host}:{port}/sinif/{sinif_kodu}"

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    dosya_yolu = os.path.join(hedef_klasor, f"{sinif_kodu}_QR.png")
    img.save(dosya_yolu)
    return dosya_yolu


def veli_sms_gonder_simule(ogrenci_ad: str, veli_tel: str):
    """Gerçek SMS API'si yerine konsola log basar."""
    mesaj = f"[SMS SIMÜLASYONU] Sayın Veli, öğrencimiz {ogrenci_ad} bugün derse katılmamıştır."
    print("=" * 60)
    print(f"ALICI: {veli_tel}")
    print(f"İÇERİK: {mesaj}")
    print("=" * 60)
    return True
