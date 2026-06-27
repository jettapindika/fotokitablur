# Foto Kita Blur

Aplikasi Python webcam sederhana pakai OpenCV + MediaPipe Hands. Saat kamera mendeteksi peace sign (tanda V), layar di-blur dan teks "FOTO KITA BLUR" muncul di kiri atas. Saat peace sign dilepas, layar kembali jernih.

## Cara install

```bash
git clone https://github.com/jettapindika/fotokitablur.git
cd fotokitablur
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Cara jalanin

```bash
python main.py
```

Tekan `q` untuk keluar, `c` untuk cycle kamera.

## Pilih / switch kamera

```bash
# Kamera bawaat (default)
python main.py --camera 0

# Kamera eksternal
python main.py --camera 1
```

Saat aplikasi jalan, tekan `c` untuk cycle ke kamera berikutnya.

## Atur resolusi

```bash
python main.py --width 1280 --height 720
```

Default 640×480 (ringan untuk CPU).

## Catatan

- Butuh Python 3.10–3.12 (MediaPipe belum support Python 3.14).
- Di Mac dengan Python 3.14 saja, install Python 3.11 dulu: `brew install python@3.11`
- Kalau kamera tidak terbaca, coba `--camera 1` atau `--camera 2`.
