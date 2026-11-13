from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image as KivyImage
from kivy.core.window import Window
from kivy.clock import Clock
from PIL import Image as PILImage, ImageStat
import os
import time
import math

Window.clearcolor = (0.01, 0.03, 0.07, 1)

class SiberKalkanApp(App):
    def build(self):
        self.title = "SIBER-KALKAN"
        ana_duzen = BoxLayout(orientation='vertical', padding=25, spacing=15)

        self.lbl_baslik = Label(
            text="SIBER-KALKAN\nOTONOM KORUMA",
            font_size='22sp',
            bold=True,
            color=(0, 1, 0.4, 1),
            halign='center',
            size_hint=(1, 0.15)
        )
        ana_duzen.add_widget(self.lbl_baslik)

        self.btn_tara = Button(
            text="SON INEN DOSYAYI INCELE",
            font_size='18sp',
            bold=True,
            background_normal='',
            background_color=(0, 1, 0.4, 1),
            color=(0.01, 0.03, 0.07, 1),
            size_hint=(1, 0.15)
        )
        self.btn_tara.bind(on_press=self.taramayi_baslat)
        ana_duzen.add_widget(self.btn_tara)

        self.img_onizleme = KivyImage(
            source='',
            size_hint=(1, 0.35),
            opacity=0
        )
        ana_duzen.add_widget(self.img_onizleme)

        self.lbl_durum = Label(
            text="Sistem Hazir.\n\nInstagram, WhatsApp veya Galeriye\ninen son dosyayi incelemek icin\nyukaridaki yesil butona basin.",
            font_size='16sp',
            bold=True,
            color=(1, 1, 1, 1),
            halign='center',
            valign='middle',
            size_hint=(1, 0.35)
        )
        self.lbl_durum.bind(size=self.lbl_durum.setter('text_size'))
        ana_duzen.add_widget(self.lbl_durum)

        return ana_duzen

    def en_son_inen_dosyayi_bul(self):
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

    def dosya_sahte_mi(self, dosya_yolu):
        uzanti = os.path.splitext(dosya_yolu).lower()
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
                std_piksel = ImageStat.Stat(img_gri).stddev
                return 42 < std_piksel < 78
            except Exception:
                return False

    def taramayi_baslat(self, instance):
        self.img_onizleme.opacity = 0
        self.lbl_durum.color = (0.22, 0.74, 0.97, 1)
        self.lbl_durum.text = "[*] GALERI VE INDIRILENLER\nTARANIYOR...\n\nLutfen bekleyin..."
        Clock.schedule_once(self.analizi_bitir, 0.5)

    def analizi_bitir(self, dt):
        hedef_dosya = self.en_son_inen_dosyayi_bul()
        if not hedef_dosya:
            self.lbl_durum.color = (1, 0.2, 0.2, 1)
            self.lbl_durum.text = "[X] DOSYA BULUNAMADI!\n\nAyarlardan uygulamanin\nMedya/Depolama iznini acin."
            return

        dosya_adi = os.path.basename(hedef_dosya)
        if len(dosya_adi) > 22:
            dosya_adi = dosya_adi[:19] + "..."

        uzanti = os.path.splitext(hedef_dosya).lower()
        if uzanti in ['.png', '.jpg', '.jpeg']:
            self.img_onizleme.source = hedef_dosya
            self.img_onizleme.reload()
            self.img_onizleme.opacity = 1

        if self.dosya_sahte_mi(hedef_dosya):
            self.lbl_durum.color = (1, 0.2, 0.2, 1)
            self.lbl_durum.text = f"[ ! ] TEHLIKE [ ! ]\nSAHTE ICERIK TESPIT EDILDI!\n\nDosya: {dosya_adi}\nKESINLIKLE GUVENMEYIN!"
        else:
            self.lbl_durum.color = (0.22, 1, 0.08, 1)
            self.lbl_durum.text = f"[ + ] GUVENLI [ + ]\nBU ICERIK GERCEKTIR.\n\nDosya: {dosya_adi}\nGuvenle izleyebilirsiniz."

if __name__ == '__main__':
    SiberKalkanApp().run()
