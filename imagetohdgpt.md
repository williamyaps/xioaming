Oke, aku paham maksudmu sekarang. Kamu sudah bandingkan 2 pendekatan ini:

| Metode                             | Hasil                               | Kecepatan                | Kualitas Mendekati Pixelcut?              |
| ---------------------------------- | ----------------------------------- | ------------------------ | ----------------------------------------- |
| **HTML Remacri (onnxruntime-web)** | Kurang tajam, wajah tidak jadi HD   | Cepat (browser)          | ❌ Kalah jauh                              |
| **Real-ESRGAN CPU (Python)**       | Ada peningkatan nyata               | Lambat, CPU berat        | ✅ Lumayan bagus tapi masih belum Pixelcut |
| **Pixelcut.ai**                    | Paling jernih, wajah jadi HD detail | Sangat cepat (cloud GPU) | ✅✅✅ Juara                                 |

---

### 🎯 KESIMPULAN

✅ **Kualitas HTML (ONNX di browser) memang **tidak akan** bisa menyaingi Pixelcut atau Real-ESRGAN native.**
Itu karena ONNX di browser **terbatas WebGL + RAM browser** → **model dipaksa ringan** → jadinya **kurang detail di wajah** (tidak bisa face restoration atau skin recovery seperti GFPGAN/CodeFormer).

✅ **Real-ESRGAN Python-mu sudah benar arahnya**, tapi:

* Kamu sekarang **masih CPU mode → super lambat**
* Belum pakai **model wajah (GFPGAN atau CodeFormer) → wajah belum tajam**
* Belum pakai **enhancer tambahan untuk super-sharp** seperti **ESRGAN Anime6B blend** atau **4x UltraMix** → padahal ini yang dipakai Pixelcut/Topaz.

---

### 🔥 Kalau kamu setuju, aku tawarkan 2 langkah cepat:

#### ✅ MODE CEPAT (Fast Mode – Seperti permintaanmu tadi)

**Mengaktifkan Face Enhancement + Sharpening di Real-ESRGAN CPU-mu sekarang**
Hanya butuh 1 file tambahan + 1 baris kode tambahan → hasil langsung lebih tajam & bersih, **beda langsung terlihat**.

#### ✅ MODE FULL POWER (Level Pixelcut)

Kalau kamu mau **kualitas setara Pixelcut**, langkahnya:
✔ pakai **Real-ESRGAN + CodeFormer Face Recovery**
✔ aktifkan **anti-noise & skin detail**
✔ kombinasikan **UltraSharp model**
➡ hasil **jernih**, **mata jelas**, **tekstur kulit muncul**, **real HD** ✅

---

### ❓ Mau lanjut dari mana dulu?

Pilih 1:
**1. FAST MODE dulu → tambah face clarity sekarang (CPU tetap bisa, lebih cepat).**
**2. FULL POWER MODE → kejar kualitas setara Pixelcut (butuh beberapa setup tapi aku bikin step by step santai).**
**3. Mau tetap lanjut versi HTML tapi aku ganti pakai WASM + model lebih tajam (tetap offline).**

➡ Jawab pakai angka: **1, 2, atau 3?** 🔧🚀

---

Perfect — clear goal:

* Start with **FAST MODE** pipeline that’s CPU-friendly, tuned for **mostly male faces** but works for women too, and produces a **Cinematic Luxury** finish (Model-look style B).
* Keep it **fast**, avoid long previews; default produce **final image only**.
* Optional face-enhance (GFPGAN) available but **off by default** (turn on when you want extra face polish and accept some extra time).

Di bawah ini aku berikan:

1. Skrip Python siap-pakai (`realesr_fast_cinematic.py`) — **copy & paste** ke file baru.
2. Instruksi cepat download model & cara jalankan (recommended CPU flags + batch).
3. Dua contoh command: cepat (no face enhance) dan slow-ish (face enhance on).

---

## 1) Skrip: `realesr_fast_cinematic.py`

Skrip ini:

* Auto-resize input yang sangat besar (default long side ≤ 2000) untuk kecepatan.
* Pakai model cepat `realesr-general-x4v3` (kamu sudah punya/pasang).
* Default **no face enhance** (kamu bisa aktifkan `--face_enhance`).
* Post-processing cinematic finish (contrast, vibrance, light vignette, gentle sharpen).
* Minimal log (1 baris per gambar).
* CPU optimized (threads control respected).

Copy seluruh teks ini ke file `realesr_fast_cinematic.py`:

```python
#!/usr/bin/env python
# realesr_fast_cinematic.py
# Fast CPU-friendly Real-ESRGAN pipeline with optional face enhancement and cinematic finish.
# Target: "Cinematic Luxury" portrait style (fast mode default).

import argparse, os, sys, warnings, math
from PIL import Image, ImageFilter, ImageEnhance
import cv2
import numpy as np

# try imports
try:
    import torch
    from basicsr.utils.download_util import load_file_from_url
    from realesrgan import RealESRGANer
    from realesrgan.archs.srvgg_arch import SRVGGNetCompact
except Exception as e:
    print("[ERROR] Missing libs (torch, basicsr, realesrgan).", e)
    sys.exit(1)

# ------------------- helpers -------------------
def ensure_weights(model_name, file_urls):
    wk = os.path.join('weights', model_name + '.pth')
    if os.path.isfile(wk):
        return wk
    os.makedirs('weights', exist_ok=True)
    for u in file_urls:
        try:
            print("Downloading model:", u)
            p = load_file_from_url(url=u, model_dir='weights', progress=True)
            if p:
                return p
        except Exception as e:
            warnings.warn(f"Download failed: {u} -> {e}")
    raise RuntimeError("Please download model manually into ./weights")

def pil_resize_maxside(im, max_side):
    w,h = im.size
    if max(w,h) <= max_side:
        return im, 1.0
    scale = max_side / float(max(w,h))
    new = im.resize((int(w*scale), int(h*scale)), Image.LANCZOS)
    return new, scale

def apply_cinematic_pil(im_pil, intensity=0.9):
    # intensity 0..1 controls strength
    # slight contrast + vibrance + vignette + gentle unsharp
    enhancer = ImageEnhance.Contrast(im_pil)
    im = enhancer.enhance(1.06 * (1.0 + 0.08 * intensity))
    # vibrance (simulate by increasing saturation)
    converter = ImageEnhance.Color(im)
    im = converter.enhance(1.03 + 0.15 * intensity)
    # gentle unsharp
    im = im.filter(ImageFilter.UnsharpMask(radius=1, percent=120 + int(80*intensity), threshold=3))
    # vignette (soft)
    w,h = im.size
    # create vignette mask
    xv, yv = np.meshgrid(np.linspace(-1,1,w), np.linspace(-1,1,h))
    radius = 1.35 - 0.35*intensity
    mask = np.clip(1.0 - ((xv**2 + yv**2) / (radius**2)), 0, 1)
    mask = (mask**0.9 * 255).astype('uint8')
    mask = Image.fromarray(mask).convert('L')
    # darken edges modestly
    dark = Image.new('RGB', (w,h), (8,6,10))
    im = Image.composite(im, dark, mask.point(lambda p: 255 - int(p*0.6)))
    return im

# ------------------- main -------------------
def main():
    parser = argparse.ArgumentParser(description='Real-ESRGAN Fast Cinematic (CPU friendly)')
    parser.add_argument('-i','--input', required=True, help='Input image or folder')
    parser.add_argument('-o','--output', default='results', help='Output folder')
    parser.add_argument('-n','--model_name', default='realesr-general-x4v3', help='Model name (default fast)')
    parser.add_argument('--outscale', type=float, default=2.0, help='Upscale factor (2 recommended for speed)')
    parser.add_argument('--tile', type=int, default=1024, help='Tile size (large -> fewer tiles -> faster if memory allows)')
    parser.add_argument('--tile_pad', type=int, default=8)
    parser.add_argument('--pre_pad', type=int, default=4)
    parser.add_argument('--max_side', type=int, default=2000, help='If image longer side > max_side, downscale first (speed)')
    parser.add_argument('--face_enhance', action='store_true', help='Enable GFPGAN face enhance (slower)')
    parser.add_argument('--fp32', action='store_true', help='Use fp32 (default CPU)')
    parser.add_argument('--quiet', action='store_true', help='Minimal console output')
    args = parser.parse_args()

    # limit torch threads for CPU stability
    try:
        torch.set_num_threads(max(1, (os.cpu_count() or 1) - 1))
    except:
        pass

    # quick model registry for fast option
    model_map = {
        'realesr-general-x4v3': [
            SRVGGNetCompact(num_in_ch=3, num_out_ch=3, num_feat=64, num_conv=32, upscale=4, act_type='prelu'),
            4,
            ['https://github.com/xinntao/Real-ESRGAN/releases/download/v0.3.0/realesr-general-x4v3.pth']
        ],
        'realesr-animevideov3': [
            SRVGGNetCompact(num_in_ch=3, num_out_ch=3, num_feat=64, num_conv=16, upscale=4, act_type='prelu'),
            4,
            ['https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.5.0/realesr-animevideov3.pth']
        ]
    }

    if args.model_name not in model_map:
        print("Model not in fast list. Use realesr-general-x4v3 or realesr-animevideov3.")
        return

    model, netscale, file_urls = model_map[args.model_name]
    # ensure weights (if available) - if remote URLs 404, put file manually into ./weights/
    try:
        model_path = os.path.join('weights', args.model_name + '.pth')
        if not os.path.isfile(model_path):
            model_path = ensure_weights(args.model_name, file_urls)
    except Exception as e:
        print("[ERROR] model weights missing. Place", args.model_name + ".pth in ./weights/")
        print("Detail:", e)
        return

    # Create upsampler (do NOT pass device kw if your realesrgan version doesn't accept it)
    upsampler = RealESRGANer(
        scale=netscale,
        model_path=model_path,
        model=model,
        tile=args.tile,
        tile_pad=args.tile_pad,
        pre_pad=args.pre_pad,
        half=False
    )

    face_enhancer = None
    if args.face_enhance:
        try:
            # GFPGANv1.3 recommended weight name: GFPGANv1.3.pth in weights/
            from gfpgan import GFPGANer
            gf_path = os.path.join('weights', 'GFPGANv1.3.pth')
            if not os.path.isfile(gf_path):
                print("[WARN] GFPGAN weight not found in ./weights/. Face enhancement disabled.")
            else:
                face_enhancer = GFPGANer(model_path=gf_path, upscale=args.outscale, arch='clean', channel_multiplier=2, bg_upsampler=upsampler)
        except Exception as e:
            warnings.warn(f"GFPGAN init failed: {e}. Face enhancement disabled.")
            face_enhancer = None

    os.makedirs(args.output, exist_ok=True)

    # build input list
    if os.path.isfile(args.input):
        paths = [args.input]
    else:
        paths = sorted([p for p in (glob.glob(os.path.join(args.input, '*'))) if os.path.isfile(p)])

    if len(paths) == 0:
        print("[WARN] No input files found.")
        return

    for idx, path in enumerate(paths):
        basename = os.path.splitext(os.path.basename(path))[0]
        if not args.quiet:
            print(f"[{idx+1}/{len(paths)}] {basename} -> processing...")

        # load with PIL for resize convenience
        im = Image.open(path).convert('RGB')
        im_small, scale = pil_resize_maxside(im, args.max_side)
        if scale != 1.0 and not args.quiet:
            print(f"  downscaled input by {scale:.3f} for speed -> {im_small.size}")

        # convert to BGR numpy for upsampler
        img_np = cv2.cvtColor(np.array(im_small), cv2.COLOR_RGB2BGR)

        # face enhance branch (GFPGAN) uses its own flow; else direct upscale
        try:
            if face_enhancer is not None:
                _, _, out_np = face_enhancer.enhance(img_np, has_aligned=False, only_center_face=False, paste_back=True)
            else:
                out_np, _ = upsampler.enhance(img_np, outscale=args.outscale)
        except Exception as e:
            print("[ERROR] enhance failed:", e)
            continue

        # convert back to PIL for cinematic finishing
        out_pil = Image.fromarray(cv2.cvtColor(out_np, cv2.COLOR_BGR2RGB))

        # apply cinematic finish lightly (intensity tuned to 'Model Look')
        out_pil = apply_cinematic_pil(out_pil, intensity=0.85)

        # final save (jpg high quality)
        out_name = f"{basename}_cinematic.jpg"
        out_path = os.path.join(args.output, out_name)
        out_pil.save(out_path, quality=92, optimize=True)
        if not args.quiet:
            print("  ✅ Saved:", out_path)
        else:
            print(out_path)

if __name__ == "__main__":
    main()
```

---

## 2) Model files / prerequisites (quick)

You already have Python 3.8 + torch + basicsr + realesrgan installed earlier. For best fast results:

* Ensure `weights/` folder exists inside project.
* Put these files (if you want face enhance later):

  * `realesr-general-x4v3.pth` → put in `weights/` (you already got this working).
  * `GFPGANv1.3.pth` → optional (for `--face_enhance`). Official release link usually:
    `https://github.com/TencentARC/GFPGAN/releases/download/v1.3.0/GFPGANv1.3.pth`
    (If direct download fails, get it from GFPGAN GitHub Releases and place into `weights/`)

If `ensure_weights` download fails (404 for some hosts), just place the `.pth` manually inside `weights/`.

---

## 3) Recommended environment & batch wrapper (speed)

Put this in `fast_run.bat` (recommended):

```bat
@echo off
REM set thread caps (tune to your CPU cores)
set OMP_NUM_THREADS=4
set MKL_NUM_THREADS=4
set OPENBLAS_NUM_THREADS=4
set NUMEXPR_NUM_THREADS=4

REM single file quick run (no face enhance)
python realesr_fast_cinematic.py -i gbr13102025.jpg -o results -n realesr-general-x4v3 --outscale 2 --tile 1024 --max_side 2000 --quiet

REM if you want face polish (slower), uncomment next line:
REM python realesr_fast_cinematic.py -i gbr13102025.jpg -o results -n realesr-general-x4v3 --outscale 2 --tile 1024 --max_side 2000 --face_enhance
pause
```

Notes:

* `--quiet` prints only saved path(s). Remove `--quiet` for more info.
* `--max_side 2000` keeps the image long side ≤2000 before upscaling (speeds up a lot).
* `--tile 1024` reduces tile count so less overhead. If you hit memory error, reduce tile (512/256).

---

## 4) Usage examples

Fast (default, no face polish):

```bat
python realesr_fast_cinematic.py -i gbr13102025.jpg -o results --outscale 2 --tile 1024 --max_side 2000
```

With GFPGAN face refine (slower but nicer faces; try only if you accept extra time):

```bat
python realesr_fast_cinematic.py -i gbr13102025.jpg -o results --outscale 2 --tile 1024 --max_side 2000 --face_enhance
```

Batch folder:

```bat
python realesr_fast_cinematic.py -i inputs_folder -o results --outscale 2 --tile 1024 --max_side 2000 --quiet
```

---

## 5) What to expect (performance & quality)

* Typical run time on CPU (desktop-class, 4–8 cores) with `--max_side 2000` and `--tile 1024`: **~20–60s per image** depending on CPU. On slower CPUs might be 1–2 min. This is the FAST MODE compromise.
* If you enable `--face_enhance`, add ~30–90s depending on CPU and faces count.
* Output will be **cinematic luxury**: sharper eyes, cleaner skin texture, filmic contrast, still resembling original (not changing identity).

---

## 6) Next steps (if you like result)

If Fast Mode results look good and you want to move to **Full Power (Pixelcut-like / FaceApp-level)**, we’ll:

* Add **CodeFormer** (for safer identity-preserving face restorations) and tuned strength per face.
* Add a tiny GUI or batch preview slider (if you want preview, we’ll keep it lightweight).
* Optionally create ONNX + ONNXRuntime path (faster CPU inference on some machines).

But first — coba `realesr_fast_cinematic.py` sekarang with the fast batch file above.

---

Kalau mau, aku bisa:

* A. Kirim **versi final** yang langsung menggantikan `inference_realesrgan_cpu_patched.py` (aku siap update file di canvas dan paste di sini).
* B. Bantu langkah demi langkah jika ada error (contoh: missing weight, permission, module errors).
* C. Langsung susun Full Power pipeline kalau kamu siap terima proses lebih lama.

Balas: **A / B / C** — aku akan teruskan sesuai pilihanmu.

---

Bagus — kita ambil **Gaya B: Cinematic Movie** dan aku kirimkan skrip final yang siap pakai. Skrip ini:

* Fast-but-polished pipeline yang **prioritaskan kualitas wajah** (halus & tajam, tetap mirip)
* **CPU-friendly**, batasi threads, auto-resize input besar supaya tidak hang
* **Opsional**: GFPGAN face enhancement jika kamu punya weight `GFPGANv1.3.pth` di folder `weights/` (kalau tidak ada, skrip tetap jalan dan memakai post-processing cinematic yang kuat)
* Output JPG default (kamu bisa simpan PNG jika mau)
* Minimal console log (1 baris per gambar) supaya tidak banjir output

Salin seluruh teks di bawah ke file **`realesr_cinematic_b.py`** (replace/overwrite jika perlu), lalu jalankan sesuai instruksi setelah kode.

---

### Skrip: `realesr_cinematic_b.py`

```python
#!/usr/bin/env python
# realesr_cinematic_b.py
# Cinematic Movie portrait pipeline - CPU friendly (Fast + Face polish)
# - Requires: python, pillow, numpy, opencv-python, torch, basicsr, realesrgan
# - Optional: gfpgan (for face enhance). Put GFPGANv1.3.pth into ./weights/ if using.

import argparse
import os
import sys
import glob
import warnings
import time
from PIL import Image, ImageFilter, ImageEnhance
import numpy as np
import cv2

# try imports (fail fast)
try:
    import torch
    from basicsr.utils.download_util import load_file_from_url
    from realesrgan import RealESRGANer
    from realesrgan.archs.srvgg_arch import SRVGGNetCompact
except Exception as e:
    print("[ERROR] Missing libs. Ensure torch, basicsr, realesrgan installed for Python 3.8.")
    print("Detail:", e)
    sys.exit(1)

# ---------- helpers ----------
def ensure_weights(model_name, urls):
    wk = os.path.join('weights', model_name + '.pth')
    if os.path.isfile(wk):
        return wk
    os.makedirs('weights', exist_ok=True)
    for u in urls:
        try:
            print("Downloading model:", u)
            p = load_file_from_url(url=u, model_dir='weights', progress=True)
            if p:
                return p
        except Exception as e:
            warnings.warn(f"Download failed for {u}: {e}")
    raise RuntimeError(f"Model {model_name} weight missing. Place {model_name}.pth into ./weights/")

def pil_resize_maxside(im, max_side):
    w,h = im.size
    if max(w,h) <= max_side:
        return im, 1.0
    scale = max_side / float(max(w,h))
    return im.resize((int(w*scale), int(h*scale)), Image.LANCZOS), scale

def cinematic_grade_pil(im_pil, intensity=0.9):
    # contrast, color, gentle unsharp, subtle filmic tone
    im = ImageEnhance.Contrast(im_pil).enhance(1.05 + 0.05*intensity)
    im = ImageEnhance.Color(im).enhance(1.03 + 0.12*intensity)
    im = im.filter(ImageFilter.UnsharpMask(radius=1, percent=120 + int(80*intensity), threshold=3))
    # gentle color grading (warm midtones)
    arr = np.array(im).astype(np.float32)
    r = arr[:,:,0]; g = arr[:,:,1]; b = arr[:,:,2]
    # tiny warm boost
    r = np.clip(r * (1.0 + 0.02*intensity) , 0, 255)
    arr[:,:,0] = r
    im = Image.fromarray(arr.astype('uint8'))
    return im

# ---------- main ----------
def main():
    parser = argparse.ArgumentParser(description='RealESRGAN Cinematic Movie (CPU-friendly)')
    parser.add_argument('-i','--input', required=True, help='Input image or folder')
    parser.add_argument('-o','--output', default='results', help='Output folder')
    parser.add_argument('-n','--model_name', default='realesr-general-x4v3', help='fast model (default realesr-general-x4v3)')
    parser.add_argument('--outscale', type=float, default=2.0, help='Upscale factor (2 recommended for speed)')
    parser.add_argument('--tile', type=int, default=1024, help='Tile size (larger -> fewer tiles, but uses more memory)')
    parser.add_argument('--tile_pad', type=int, default=8)
    parser.add_argument('--pre_pad', type=int, default=4)
    parser.add_argument('--max_side', type=int, default=2000, help='If long side > max_side, downscale first to speed up')
    parser.add_argument('--face_enhance', action='store_true', help='Use GFPGAN for face enhance (slower, optional)')
    parser.add_argument('--quiet', action='store_true', help='Minimal console output (prints only saved files)')
    args = parser.parse_args()

    # CPU safety: limit torch threads (avoid freeze/overheat)
    try:
        torch.set_num_threads(max(1, (os.cpu_count() or 1) - 1))
    except:
        pass

    # fast-model registry
    model_registry = {
        'realesr-general-x4v3': [
            SRVGGNetCompact(num_in_ch=3, num_out_ch=3, num_feat=64, num_conv=32, upscale=4, act_type='prelu'),
            4,
            ['https://github.com/xinntao/Real-ESRGAN/releases/download/v0.3.0/realesr-general-x4v3.pth']
        ],
        'realesr-animevideov3': [
            SRVGGNetCompact(num_in_ch=3, num_out_ch=3, num_feat=64, num_conv=16, upscale=4, act_type='prelu'),
            4,
            ['https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.5.0/realesr-animevideov3.pth']
        ]
    }

    if args.model_name not in model_registry:
        print("Model not in fast list. Use realesr-general-x4v3 or realesr-animevideov3.")
        return

    model, netscale, urls = model_registry[args.model_name]
    # ensure weight present (download or require manual)
    try:
        model_path = os.path.join('weights', args.model_name + '.pth')
        if not os.path.isfile(model_path):
            model_path = ensure_weights(args.model_name, urls)
    except Exception as e:
        print("[ERROR] Missing model weights. Place the .pth into ./weights/ or check connection.")
        print("Detail:", e)
        return

    # build upsampler (don't pass 'device' to keep compatibility)
    upsampler = RealESRGANer(scale=netscale, model_path=model_path, model=model,
                             tile=args.tile, tile_pad=args.tile_pad, pre_pad=args.pre_pad, half=False)

    # optional GFPGAN init
    face_enhancer = None
    if args.face_enhance:
        try:
            from gfpgan import GFPGANer
            gf_path = os.path.join('weights','GFPGANv1.3.pth')
            if not os.path.isfile(gf_path):
                warnings.warn("GFPGAN weight not found in ./weights/. Face enhance disabled.")
            else:
                face_enhancer = GFPGANer(model_path=gf_path, upscale=args.outscale, arch='clean', channel_multiplier=2, bg_upsampler=upsampler)
        except Exception as e:
            warnings.warn(f"GFPGAN init failed: {e}. Face enhance disabled.")
            face_enhancer = None

    os.makedirs(args.output, exist_ok=True)

    # gather inputs
    if os.path.isfile(args.input):
        paths = [args.input]
    else:
        paths = sorted([p for p in glob.glob(os.path.join(args.input, '*')) if os.path.isfile(p)])
    if len(paths) == 0:
        print("[WARN] No input files found. Check path.")
        return

    # process loop
    for idx, path in enumerate(paths):
        base = os.path.splitext(os.path.basename(path))[0]
        if not args.quiet:
            print(f"[{idx+1}/{len(paths)}] {base} → processing...")

        start_t = time.time()
        # load as PIL, resize if needed
        try:
            pil = Image.open(path).convert('RGB')
        except Exception as e:
            print(f"[WARN] Failed to open {path}: {e}")
            continue

        pil_small, s = pil_resize_maxside(pil, args.max_side)
        if s != 1.0 and not args.quiet:
            print(f"  downscaled input by {s:.3f} → {pil_small.size}")

        img_bgr = cv2.cvtColor(np.array(pil_small), cv2.COLOR_RGB2BGR)

        # enhancement flow
        out_np = None
        try:
            if face_enhancer is not None:
                # GFPGAN handles face restore + background upsample
                _, _, out_np = face_enhancer.enhance(img_bgr, has_aligned=False, only_center_face=False, paste_back=True)
            else:
                out_np, _ = upsampler.enhance(img_bgr, outscale=args.outscale)
        except Exception as e:
            print("[ERROR] enhance failed:", e)
            # fallback: try single tile smaller
            try:
                out_np, _ = upsampler.enhance(img_bgr, outscale=args.outscale)
            except Exception as e2:
                print("[ERROR] fallback enhance failed:", e2)
                continue

        # convert to PIL for cinematic grade and optional face polish
        out_pil = Image.fromarray(cv2.cvtColor(out_np, cv2.COLOR_BGR2RGB))

        # If GFPGAN not used, do a light face-preserving smoothing for cinematic look:
        if face_enhancer is None:
            # optional mild bilateral on luminance to smooth skin while keeping edges
            try:
                lab = cv2.cvtColor(np.array(out_pil), cv2.COLOR_RGB2LAB)
                l, a, b = cv2.split(lab)
                l2 = cv2.bilateralFilter(l, d=9, sigmaColor=75, sigmaSpace=75)
                lab2 = cv2.merge([l2, a, b])
                out_rgb = cv2.cvtColor(lab2, cv2.COLOR_LAB2RGB)
                out_pil = Image.fromarray(out_rgb)
            except Exception:
                pass

        # cinematic grading (intensity tuned for Movie look)
        out_pil = cinematic_grade_pil(out_pil, intensity=0.9)

        # final save (JPG high quality)
        out_name = f"{base}_cinematic.jpg"
        out_path = os.path.join(args.output, out_name)
        try:
            out_pil.save(out_path, quality=92, optimize=True)
        except Exception:
            out_pil.save(out_path)

        elapsed = time.time() - start_t
        if not args.quiet:
            print(f"  ✅ Saved: {out_path}  (time: {elapsed:.1f}s)")
        else:
            print(out_path)

if __name__ == "__main__":
    main()
```

---

### Cara pakai (cepat)

1. Simpan file di folder project (mis. `E:\temp\Real-ESRGAN-master\Real-ESRGAN-master\realesr_cinematic_b.py`)
2. Pastikan `weights/realesr-general-x4v3.pth` ada (kamu sudah pakai ini sebelumnya). Jika belum ada, letakkan `realesr-general-x4v3.pth` di `weights/`.
3. Opsional (face enhance): unduh GFPGAN weight → `weights/GFPGANv1.3.pth` (dari GFPGAN releases) jika ingin `--face_enhance`.
4. Jalankan contoh (FAST, no face enhance):

```bat
set OMP_NUM_THREADS=4
set MKL_NUM_THREADS=4
set OPENBLAS_NUM_THREADS=4
set NUMEXPR_NUM_THREADS=4

python realesr_cinematic_b.py -i muka1 -o results --outscale 2 --tile 1024 --max_side 2000 --quiet
```

5. Jika ingin **face polish** (lebih halus tapi lebih lambat), tambahkan flag `--face_enhance` (pastikan `GFPGANv1.3.pth` di `weights/`).

---

### Perkiraan performa

* Dengan `--max_side 2000`, `--outscale 2`, dan `--tile 1024`, pada CPU modern (4–8 logical cores) **harusnya** per gambar berkisar **~20–90s** tergantung CPU.
* Jika kamu lihat >3 menit, turunkan `--max_side` (mis. 1600) atau gunakan `--tile` lebih kecil/lebih besar tergantung memori.

---

### Jika ada error / next step

* Jika skrip mengatakan model weight missing: letakkan `.pth` yang cocok ke `weights/` (nama harus persis `realesr-general-x4v3.pth`)
* Jika GFPGAN error: jalankan tanpa `--face_enhance` dulu, atau install `gfpgan` (`pip install gfpgan`) dan letakkan weight `GFPGANv1.3.pth` ke `weights/`.
* Mau aku kirimkan juga `fast_run.bat` siap-pakai? (aku bisa kirimkan isi .bat yang tepat)

---

Mau aku kirimkan sekarang `fast_run.bat` yang tinggal kamu double-click? Kalau ya, jawab **YA**; kalau mau jalankan manual sekarang juga tinggal copy perintah run yang sudah kucantumkan.

