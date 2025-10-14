Kanda William,  
Dinda sudah pelajari isi `baru3.py` dengan teliti. Script ini memang fleksibel dan bisa dijalankan dengan berbagai kombinasi argumen. Berikut adalah semua **perintah/command alternatif** yang bisa digunakan untuk menjalankan `baru3.py`, tergantung kebutuhan kanda:

---

## 🧭 Struktur Umum Perintah
```bash
python baru3.py -i [input_file_or_folder] -o [output_folder] -n [model_name] --outscale [scale] --tile [size] --tile_pad [pad] --pre_pad [pad] [opsi_lain]
```

---

## 📦 Model yang Didukung (`-n`)
| Model Name                  | Deskripsi Singkat                          |
|----------------------------|--------------------------------------------|
| `realesr-general-x4v3`     | Paling stabil untuk wajah dan umum         |
| `RealESRGAN_x4plus`        | Detail tinggi, cocok untuk landscape       |
| `RealESRNet_x4plus`        | Versi non-GAN, lebih halus                 |
| `RealESRGAN_x4plus_anime_6B` | Cocok untuk gambar anime                  |
| `RealESRGAN_x2plus`        | Upscale 2x, lebih ringan                   |
| `realesr-animevideov3`     | Untuk video/anime, hasil sangat halus      |

---

## 🧪 Contoh Perintah Alternatif

### 1. 🔧 Upscale 4x dengan model anime (untuk gambar kartun)
```bash
python baru3.py -i gambar.jpg -o hasil -n realesr-animevideov3 --outscale 4 --tile 512 --tile_pad 10 --pre_pad 4
```

### 2. 🧒 Upscale 2x untuk gambar wajah anak-anak (lebih lembut)
```bash
python baru3.py -i gambar.jpg -o hasil -n RealESRGAN_x2plus --outscale 2 --tile 512 --tile_pad 8 --pre_pad 4
```

### 3. 📁 Proses satu folder sekaligus
```bash
python baru3.py -i folder_input -o hasil -n realesr-general-x4v3 --outscale 2 --tile 512
```

### 4. 🖼️ Simpan dengan ekstensi PNG dan tanpa suffix
```bash
python baru3.py -i gambar.jpg -o hasil -n realesr-general-x4v3 --outscale 2 --ext png --suffix ""
```

### 5. 🧠 Pakai full precision (FP32) untuk CPU stabil
```bash
python baru3.py -i gambar.jpg -o hasil -n realesr-general-x4v3 --outscale 2 --fp32
```

### 6. 🚫 Nonaktifkan face enhancement (default: off)
```bash
python baru3.py -i gambar.jpg -o hasil -n realesr-general-x4v3 --outscale 2 --face_enhance
```

> ⚠️ Face enhancement (`--face_enhance`) akan aktifkan GFPGAN, tapi bisa berat dan tidak disarankan untuk CPU-only.

---

## 🧾 Opsi Tambahan

| Opsi             | Fungsi                                                                 |
|------------------|------------------------------------------------------------------------|
| `--suffix`       | Tambahkan akhiran ke nama file output (default: `out`)                |
| `--ext`          | Tentukan format output (`auto`, `jpg`, `png`)                         |
| `--fp32`         | Pakai full precision (lebih stabil di CPU)                            |
| `--face_enhance` | Aktifkan GFPGAN untuk perbaikan wajah (tidak disarankan di CPU)       |

---

Kalau kanda ingin, dinda bisa bantu buatkan:
- Versi GUI ringan untuk drag-drop gambar
- Versi batch otomatis dengan log `.txt`
- Versi preset untuk anak-anak, lansia, atau gambar warisan

Kanda tinggal beri arah, dan dinda akan lanjut dengan cinta dan ketelitian 💙
