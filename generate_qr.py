import os
import socket
import qrcode

OUTPUT_DIR = "qrcodes"
os.makedirs(OUTPUT_DIR, exist_ok=True)

SINIFLAR = ["9-A", "10-A", "11-A", "11-B", "11-C", "12-A", "12-B"]

# Bilgisayarının yerel ağ IP adresini otomatik bulur (Örn: 192.168.1.35)
def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

# Telefondan test ederken yerel IP, bilgisayardan test ederken localhost kullanabilirsin
HOST = get_local_ip() 
PORT = 8000
BASE_URL = f"http://{HOST}:{PORT}/sinif/"

print("🚀 Sınıf QR Kodları üretiliyor...\n")
print(f"📡 Sunucu Adresi: {BASE_URL}\n")

for sinif in SINIFLAR:
    target_url = f"{BASE_URL}{sinif}"
    
    qr = qrcode.QRCode(
        version=1, 
        error_correction=qrcode.constants.ERROR_CORRECT_H, 
        box_size=10, 
        border=4
    )
    qr.add_data(target_url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    filepath = os.path.join(OUTPUT_DIR, f"{sinif}_QR.png")
    img.save(filepath)
    print(f"✅ [{sinif}] -> {target_url} -> Saved: {filepath}")

print(f"\n🎉 İşlem tamamlandı! QR kod görselleri '{OUTPUT_DIR}' klasörüne kaydedildi.")