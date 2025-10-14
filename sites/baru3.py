import argparse
import cv2
import glob
import os
import sys
import warnings

# Minimal imports compatible with older realesrgan/basicsr releases
try:
    import torch
    from basicsr.archs.rrdbnet_arch import RRDBNet
    from basicsr.utils.download_util import load_file_from_url
    from realesrgan import RealESRGANer
    from realesrgan.archs.srvgg_arch import SRVGGNetCompact
except Exception as e:
    print("[ERROR] Missing required modules or incompatible versions:\n", e)
    print("Please ensure basicsr, realesrgan, and their deps are installed for Python 3.8 (CPU).")
    sys.exit(1)


def download_weights_if_needed(model_name, file_urls):
    model_path = os.path.join('weights', model_name + '.pth')
    if os.path.isfile(model_path):
        return model_path
    os.makedirs('weights', exist_ok=True)
    # attempt to download the first url (some models may provide multiple files)
    for url in file_urls:
        try:
            print(f"Downloading model from: {url}")
            model_path = load_file_from_url(url=url, model_dir='weights', progress=True)
            if model_path:
                return model_path
        except Exception as e:
            warnings.warn(f"Failed to download {url}: {e}")
    raise RuntimeError('Failed to obtain model weights; please download manually into ./weights')


def build_model_by_name(name):
    name = name.split('.')[0]
    if name == 'RealESRGAN_x4plus':
        model = RRDBNet(num_in_ch=3, num_out_ch=3, num_feat=64, num_block=23, num_grow_ch=32, scale=4)
        netscale = 4
        file_urls = [
            'https://github.com/xinntao/Real-ESRGAN/releases/download/v0.1.0/RealESRGAN_x4plus.pth'
        ]
    elif name == 'RealESRNet_x4plus':
        model = RRDBNet(num_in_ch=3, num_out_ch=3, num_feat=64, num_block=23, num_grow_ch=32, scale=4)
        netscale = 4
        file_urls = [
            'https://github.com/xinntao/Real-ESRGAN/releases/download/v0.1.1/RealESRNet_x4plus.pth'
        ]
    elif name == 'RealESRGAN_x4plus_anime_6B':
        model = RRDBNet(num_in_ch=3, num_out_ch=3, num_feat=64, num_block=6, num_grow_ch=32, scale=4)
        netscale = 4
        file_urls = [
            'https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.2.4/RealESRGAN_x4plus_anime_6B.pth'
        ]
    elif name == 'RealESRGAN_x2plus':
        model = RRDBNet(num_in_ch=3, num_out_ch=3, num_feat=64, num_block=23, num_grow_ch=32, scale=2)
        netscale = 2
        file_urls = [
            'https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.1/RealESRGAN_x2plus.pth'
        ]
    elif name == 'realesr-animevideov3':
        model = SRVGGNetCompact(num_in_ch=3, num_out_ch=3, num_feat=64, num_conv=16, upscale=4, act_type='prelu')
        netscale = 4
        file_urls = ['https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.5.0/realesr-animevideov3.pth']
    elif name == 'realesr-general-x4v3':
        model = SRVGGNetCompact(num_in_ch=3, num_out_ch=3, num_feat=64, num_conv=32, upscale=4, act_type='prelu')
        netscale = 4
        file_urls = ['https://github.com/xinntao/Real-ESRGAN/releases/download/v0.3.0/realesr-general-x4v3.pth']
    else:
        raise ValueError(f"Model '{name}' is not supported by this patched CPU script.")

    return model, netscale, file_urls


def main():
    parser = argparse.ArgumentParser(description='Real-ESRGAN (CPU-only patched)')
    parser.add_argument('-i', '--input', type=str, required=True, help='Input image or folder')
    parser.add_argument('-o', '--output', type=str, default='results', help='Output folder')
    parser.add_argument('-n', '--model_name', type=str, default='realesr-general-x4v3')
    parser.add_argument('-s', '--outscale', type=float, default=4.0, help='Final upsampling scale')
    parser.add_argument('--fp32', action='store_true', help='Use full precision (fp32) - recommended for CPU')
    parser.add_argument('--tile', type=int, default=256, help='Tile size. Increase to reduce peak memory usage (CPU slower).')
    parser.add_argument('--tile_pad', type=int, default=10, help='Tile padding')
    parser.add_argument('--pre_pad', type=int, default=0, help='Pre-pad image')
    parser.add_argument('--face_enhance', action='store_true', help='Use GFPGAN to enhance faces')
    parser.add_argument('--suffix', type=str, default='out', help='Suffix for output files')
    parser.add_argument('--ext', type=str, default='auto', help='Output extension (auto/jpg/png)')

    args = parser.parse_args()

    # Force CPU usage. This avoids any cuda checks that can trigger issues in old Windows.
    device = torch.device('cpu')
    print('⚠️ Running in CPU mode (forced). This script is adjusted for Windows 8 + Python 3.8 (slower but safe).')

    # build model and ensure weights present
    try:
        model, netscale, file_urls = build_model_by_name(args.model_name)
    except Exception as e:
        print(f"[ERROR] {e}")
        return

    try:
        model_path = os.path.join('weights', args.model_name + '.pth')
        if not os.path.isfile(model_path):
            model_path = download_weights_if_needed(args.model_name, file_urls)
    except Exception as e:
        print('[ERROR] Could not get model weights:', e)
        return

    # create upsampler - DO NOT pass `device` or unsupported kwargs so this works with older realesrgan
    upsampler = RealESRGANer(
        scale=netscale,
        model_path=model_path,
        model=model,
        tile=args.tile,
        tile_pad=args.tile_pad,
        pre_pad=args.pre_pad,
        half=False if args.fp32 else False  # CPU: keep fp32 (half not supported on CPU reliably)
    )

    face_enhancer = None
    if args.face_enhance:
        try:
            from gfpgan import GFPGANer
            print('-> GFPGAN face enhancement enabled (will use background upsampler).')
            face_enhancer = GFPGANer(
                model_path='https://github.com/TencentARC/GFPGAN/releases/download/v1.3.0/GFPGANv1.3.pth',
                upscale=args.outscale,
                arch='clean',
                channel_multiplier=2,
                bg_upsampler=upsampler
            )
        except Exception as e:
            warnings.warn(f'GFPGAN not available or failed to init: {e}. Continuing without face enhancement.')
            face_enhancer = None

    os.makedirs(args.output, exist_ok=True)

    # build input list
    if os.path.isfile(args.input):
        paths = [args.input]
    else:
        paths = sorted(glob.glob(os.path.join(args.input, '*')))

    if len(paths) == 0:
        print('[WARN] No input files found.')
        return

    # Processing loop: apply aggressive sharpening-ish parameters for "Brutal Detail" mode
    for idx, path in enumerate(paths):
        imgname, extension = os.path.splitext(os.path.basename(path))
        print(f'Processing {idx+1}/{len(paths)}: {imgname}{extension}')

        img = cv2.imread(path, cv2.IMREAD_UNCHANGED)
        if img is None:
            print(f'[WARN] Failed to read {path}, skipping.')
            continue

        img_mode = 'RGBA' if (len(img.shape) == 3 and img.shape[2] == 4) else None

        try:
            if face_enhancer is not None:
                # GFPGAN returns (restored, restored_faces, enhanced)
                _, _, output = face_enhancer.enhance(img, has_aligned=False, only_center_face=False, paste_back=True)
            else:
                # upsampler.enhance returns (output, None) on many versions
                output, _ = upsampler.enhance(img, outscale=args.outscale)

            # Post-process: for "brutal detail" we can apply a light unsharp mask to emphasize edges
            try:
                # convert BGR -> YCrCb, sharpen on Y channel
                img_ycc = cv2.cvtColor(output, cv2.COLOR_BGR2YCrCb)
                y, cr, cb = cv2.split(img_ycc)
                # Unsharp mask: gaussian blur then add weighted difference
                blur = cv2.GaussianBlur(y, (0, 0), sigmaX=1.2)
                unsharp = cv2.addWeighted(y, 1.15, blur, -0.15, 0)
                img_ycc = cv2.merge([unsharp, cr, cb])
                output = cv2.cvtColor(img_ycc, cv2.COLOR_YCrCb2BGR)
            except Exception:
                # if any error during sharpening, keep original upsampled output
                pass

        except RuntimeError as error:
            print('[ERROR] Runtime error during enhance():', error)
            print('If running out of memory, try a smaller --tile value (e.g. 128)')
            continue
        except Exception as error:
            print('[ERROR] Unexpected error:', error)
            continue

        # decide extension
        if args.ext == 'auto':
            ext = extension[1:] if extension.startswith('.') else extension
        else:
            ext = args.ext
        if img_mode == 'RGBA':
            ext = 'png'

        # build save path
        if args.suffix == '':
            save_name = f'{imgname}.{ext}'
        else:
            save_name = f'{imgname}_{args.suffix}.{ext}'
        save_path = os.path.join(args.output, save_name)

        # write result
        try:
            # if extension is jpg and output has alpha, drop alpha
            if ext.lower() in ('jpg', 'jpeg') and output.shape[2] == 4:
                output = cv2.cvtColor(output, cv2.COLOR_BGRA2BGR)
            cv2.imwrite(save_path, output)
            print(f'✅ Saved: {save_path}')
        except Exception as e:
            print('[ERROR] Failed to save output:', e)


if __name__ == '__main__':
    main()
