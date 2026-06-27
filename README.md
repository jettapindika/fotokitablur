# Foto Kita Blur

Aplikasi Python sederhana yang memakai webcam, OpenCV, dan MediaPipe Hands. Saat kamera mendeteksi peace sign / tanda V, tampilan kamera akan diblur. Saat tanda tidak terdeteksi, tampilan kembali normal. Aplikasi juga menampilkan overlay landmark tangan, trail yang mengikuti ujung jari telunjuk, serta glow dan sparkle saat peace sign aktif. Tekan `q` untuk keluar.

## Cara install

```bash
pip install -r requirements.txt
```

## Cara jalanin

```bash
python main.py
```

## Pilih / switch kamera

Pakai flag `--camera` untuk pilih kamera saat start:

```bash
# Kamera bawaan (default)
python main.py --camera 0

# Kamera eksternal (webcam USB, dll.)
python main.py --camera 1

# Indeks lain
python main.py --camera 2
```

Saat aplikasi sedang jalan, tekan **`c`** untuk cycle ke kamera berikutnya tanpa keluar dari aplikasi. Kalau kamera berikutnya tidak tersedia, otomatis kembali ke kamera sebelumnya.

## Atur resolusi capture

```bash
python main.py --width 1280 --height 720
```

Default 640×480 (ringan untuk CPU). Naikkan untuk kualitas, turunkan kalau masih berat.

## Catatan

- Pastikan webcam tersedia dan izin akses kamera sudah diberikan oleh sistem operasi.
- Di Linux headless / VPS tanpa display dan tanpa webcam, aplikasi tidak bisa diuji langsung karena `cv2.imshow()` membutuhkan display GUI dan `cv2.VideoCapture(0)` membutuhkan kamera.
- Kalau kamera eksternal tidak terbaca, coba `--camera 1` atau `--camera 2`.
- Butuh Python 3.10–3.12 (MediaPipe belum support Python 3.14).
