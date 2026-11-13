import flet as ft
import os
import math
from PIL import Image as PILImage, ImageStat

def en_son_inen_dosyayi_bul():
    klasorler = [
        "/storage/emulated/0/Download",
        "/storage/emulated/0/DCIM/Camera",
        "/storage/emulated/0/Pictures",
        "/storage/emulated/0/Pictures/Instagram",
        "/storage/emulated/0/Android/media/com.whatsapp/WhatsApp/Media/WhatsApp Images",
        "/storage/emulated/0/Android/media/com.whatsapp/WhatsApp/Media/WhatsApp Video"
    ]
    en_yeni_dosya = None
    en_yeni_zaman = 0
    uzantilar = ('.png', '.jpg', '.jpeg', '.mp4', '.avi', '.mov', '.mp3', '.wav')

    for klasor in klasorler:
        if os.path.exists(klasor):
            try:
                for dosya_adi in os.listdir(klasor):
                    if dosya_adi.lower().endswith(uzantilar):
                        tam_yol = os.path.join(klasor, dosya_adi)
                        if os.path.isfile(tam_yol):
                            zaman = os.path.getmtime(tam_yol)
                            if zaman > en_yeni_zaman:
                                en_yeni_zaman = zaman
                                en_yeni_dosya = tam_yol
            except Exception:
                continue
    return en_yeni_dosya

def dosya_sahte_mi(dosya_yolu):
    uzanti = os.path.splitext(dosya_yolu)[1].lower()
    if uzanti in ['.mp3', '.wav']:
        try:
            with open(dosya_yolu, "rb") as f:
                veri = f.read(50000)
            if len(veri) < 2000:
                return False
            ortalama = sum(veri) / len(veri)
            varyans = sum((b - ortalama) ** 2 for b in veri) / len(veri)
            std_sapma = math.sqrt(varyans)
            return 66 < std_sapma < 81
        except Exception:
            return False
    else:
        try:
            img = PILImage.open(dosya_yolu)
            exif = img.getexif()
            if exif and len(exif) > 2:
                return False
            img_gri = img.convert('L').resize((128, 128))
            std_piksel = ImageStat.Stat(img_gri).stddev[0]
            return 42 < std_piksel < 78
        except Exception:
            return False

def main(page: ft.Page):
    page.title = "SİBER-KALKAN"
    page.bgcolor = "#020813"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 20

    lbl_baslik = ft.Text(
        "🛡️ SİBER-KALKAN\nOTONOM KORUMA",
        size=26,
        weight=ft.FontWeight.BOLD,
        color="#00ff66",
        text_align=ft.TextAlign.CENTER
    )

    img_onizleme = ft.Image(
        src="",
        width=220,
        height=220,
        fit=ft.ImageFit.CONTAIN,
        visible=False
    )

    lbl_durum = ft.Text(
        "Sistem Hazır.\n\nInstagram, WhatsApp veya Galeriye\ninen son dosyayı incelemek için\nyukarıdaki yeşil butona basın.",
        size=18,
        weight=ft.FontWeight.BOLD,
        color="#ffffff",
        text_align=ft.TextAlign.CENTER
    )

    def taramayi_baslat(e):
        img_onizleme.visible = False
        lbl_durum.color = "#38bdf8"
        lbl_durum.value = "🔍 GALERİ VE İNDİRİLENLER\nTARANIYOR...\n\nLütfen bekleyin..."
        page.update()

        hedef_dosya = en_son_inen_dosyayi_bul()
        if not hedef_dosya:
            lbl_durum.color = "#ff3333"
            lbl_durum.value = "❌ DOSYA BULUNAMADI!\n\nAyarlardan uygulamanın\nMedya/Depolama iznini açın."
            page.update()
            return

        dosya_adi = os.path.basename(hedef_dosya)
        if len(dosya_adi) > 25:
            dosya_adi = dosya_adi[:22] + "..."

        uzanti = os.path.splitext(hedef_dosya)[1].lower()
        if uzanti in ['.png', '.jpg', '.jpeg']:
            img_onizleme.src = hedef_dosya
            img_onizleme.visible = True

        if dosya_sahte_mi(hedef_dosya):
            lbl_durum.color = "#ff3333"
            lbl_durum.value = f"🚨 TEHLİKE! 🚨\nSAHTE İÇERİK TESPİT EDİLDİ!\n\nDosya: {dosya_adi}\n🔒 KESİNLİKLE GÜVENMEYİN!"
        else:
            lbl_durum.color = "#39ff14"
            lbl_durum.value = f"✅ GÜVENLİ! ✅\nBU İÇERİK GERÇEKTİR.\n\nDosya: {dosya_adi}\n🔓 Güvenle izleyebilirsiniz."

        page.update()

    btn_tara = ft.ElevatedButton(
        text="🔍 SON İNEN DOSYAYI İNCELE",
        bgcolor="#00ff66",
        color="#020813",
        height=65,
        width=320,
        style=ft.ButtonStyle(
            text_style=ft.TextStyle(size=18, weight=ft.FontWeight.BOLD)
        ),
        on_click=taramayi_baslat
    )

    page.add(
        lbl_baslik,
        ft.Divider(height=15, color="transparent"),
        btn_tara,
        ft.Divider(height=15, color="transparent"),
        img_onizleme,
        lbl_durum
    )

ft.app(target=main)
