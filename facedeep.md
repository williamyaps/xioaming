Oke, mari buat versi command-line saja tanpa GUI. Berikut kodenya:

## 1. Install Dependencies

Buat `install_cpu.py`:
```python
import subprocess
import sys

def install_package(package):
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"✅ {package} installed successfully")
    except subprocess.CalledProcessError:
        print(f"❌ Failed to install {package}")

packages = [
    "opencv-python==4.5.5.64",
    "numpy==1.21.6", 
    "pillow==9.5.0",
    "scipy==1.7.3",
    "dlib==19.22.1"
]

print("Installing CPU-only dependencies...")

for package in packages:
    install_package(package)

print("\n✅ All dependencies installed!")
print("\n📥 Download landmark model from:")
print("http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2")
print("Extract and rename to: shape_predictor_68_face_landmarks.dat")
```

## 2. Kode Face Morphing CPU-Only

Buat `face_morph_cli.py`:

```python
import cv2
import numpy as np
import dlib
from scipy.spatial import Delaunay
import os
import argparse

class CPUFaceMorpher:
    def __init__(self):
        """Initialize with dlib face detector"""
        print("🔄 Loading face detection model...")
        self.detector = dlib.get_frontal_face_detector()
        try:
            self.predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
            print("✅ Landmark model loaded successfully")
        except:
            print("❌ Landmark model not found. Please download:")
            print("http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2")
            raise
    
    def detect_landmarks(self, image):
        """Detect facial landmarks"""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = self.detector(gray)
        
        if len(faces) == 0:
            return None
        
        face = faces[0]
        landmarks = self.predictor(gray, face)
        
        points = []
        for i in range(68):
            x = landmarks.part(i).x
            y = landmarks.part(i).y
            points.append((x, y))
        
        return np.array(points, dtype=np.float32)
    
    def apply_affine_transform(self, src, src_tri, dst_tri, size):
        """Apply affine transform"""
        warp_mat = cv2.getAffineTransform(np.float32(src_tri), np.float32(dst_tri))
        dst = cv2.warpAffine(src, warp_mat, (size[0], size[1]), None, 
                           flags=cv2.INTER_LINEAR, 
                           borderMode=cv2.BORDER_REFLECT_101)
        return dst
    
    def morph_triangle(self, img1, img2, tri1, tri2):
        """Morph triangular region"""
        r1 = cv2.boundingRect(np.float32([tri1]))
        r2 = cv2.boundingRect(np.float32([tri2]))
        
        tri1_rect = []
        tri2_rect = []
        
        for i in range(3):
            tri1_rect.append(((tri1[i][0] - r1[0]), (tri1[i][1] - r1[1])))
            tri2_rect.append(((tri2[i][0] - r2[0]), (tri2[i][1] - r2[1])))
        
        mask = np.zeros((r2[3], r2[2], 3), dtype=np.float32)
        cv2.fillConvexPoly(mask, np.int32(tri2_rect), (1.0, 1.0, 1.0))
        
        img1_rect = img1[r1[1]:r1[1] + r1[3], r1[0]:r1[0] + r1[2]]
        img2_rect = img2[r2[1]:r2[1] + r2[3], r2[0]:r2[0] + r2[2]]
        
        size = (r2[2], r2[3])
        warp_image1 = self.apply_affine_transform(img1_rect, tri1_rect, tri2_rect, size)
        
        img_rect = warp_image1
        
        img2[r2[1]:r2[1] + r2[3], r2[0]:r2[0] + r2[2]] = \
            img2[r2[1]:r2[1] + r2[3], r2[0]:r2[0] + r2[2]] * (1 - mask) + img_rect * mask
    
    def enhance_jawline(self, landmarks, strength=0.5):
        """Strengthen jawline"""
        enhanced = landmarks.copy()
        jaw_points = enhanced[0:17]
        jaw_center = np.mean(jaw_points, axis=0)
        
        for i in range(len(jaw_points)):
            direction = jaw_points[i] - jaw_center
            if np.linalg.norm(direction) > 0:
                direction = direction / np.linalg.norm(direction)
            
            if i in [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]:
                enhanced[i] += direction * strength * 12
                enhanced[i][1] += strength * 6
        
        return enhanced
    
    def enhance_cheekbones(self, landmarks, strength=0.5):
        """Lift cheekbones"""
        enhanced = landmarks.copy()
        
        # Right cheek points
        right_cheek = [1, 2, 3, 4, 5]
        # Left cheek points
        left_cheek = [12, 13, 14, 15, 16]
        
        for i in right_cheek:
            if i < len(enhanced):
                enhanced[i][1] -= strength * 10
                enhanced[i][0] -= strength * 6
        
        for i in left_cheek:
            if i < len(enhanced):
                enhanced[i][1] -= strength * 10
                enhanced[i][0] += strength * 6
        
        return enhanced
    
    def enhance_eyes(self, landmarks, strength=0.5):
        """Enlarge eyes"""
        enhanced = landmarks.copy()
        
        right_eye = list(range(36, 42))
        left_eye = list(range(42, 48))
        
        def expand_eye(eye_points):
            center = np.mean(enhanced[eye_points], axis=0)
            for point_idx in eye_points:
                direction = enhanced[point_idx] - center
                if np.linalg.norm(direction) > 0:
                    direction = direction / np.linalg.norm(direction)
                enhanced[point_idx] += direction * strength * 6
        
        expand_eye(right_eye)
        expand_eye(left_eye)
        
        return enhanced
    
    def slim_nose(self, landmarks, strength=0.5):
        """Slim nose"""
        enhanced = landmarks.copy()
        
        nose_bridge = list(range(27, 31))
        nose_width = list(range(31, 36))
        
        nose_center = np.mean(enhanced[nose_bridge], axis=0)
        for point_idx in nose_bridge:
            direction = enhanced[point_idx] - nose_center
            if abs(direction[0]) > 0.1:
                enhanced[point_idx][0] -= np.sign(direction[0]) * strength * 4
        
        for point_idx in nose_width:
            direction = enhanced[point_idx] - nose_center  
            enhanced[point_idx][0] -= direction[0] * strength * 0.2
        
        return enhanced
    
    def enhance_lips(self, landmarks, strength=0.5):
        """Fuller lips"""
        enhanced = landmarks.copy()
        
        outer_lips = list(range(48, 60))
        inner_lips = list(range(60, 68))
        
        lip_center = np.mean(enhanced[outer_lips], axis=0)
        
        for point_idx in outer_lips:
            direction = enhanced[point_idx] - lip_center
            if np.linalg.norm(direction) > 0:
                direction = direction / np.linalg.norm(direction)
            enhanced[point_idx] += direction * strength * 5
        
        for point_idx in inner_lips:
            direction = enhanced[point_idx] - lip_center
            if np.linalg.norm(direction) > 0:
                direction = direction / np.linalg.norm(direction)
            enhanced[point_idx] += direction * strength * 3
        
        return enhanced
    
    def morph_image(self, image, src_points, dst_points):
        """Morph image using triangulation"""
        src_face_points = src_points[:68]
        dst_face_points = dst_points[:68]
        
        tri = Delaunay(src_face_points)
        morphed = np.zeros_like(image, dtype=np.float32)
        
        for simplex in tri.simplices:
            src_tri = src_face_points[simplex]
            dst_tri = dst_face_points[simplex]
            self.morph_triangle(image.astype(np.float32), morphed, src_tri, dst_tri)
        
        return morphed.astype(np.uint8)
    
    def apply_face_morphing(self, image, landmarks, enhancements):
        """Apply all morphing effects"""
        current_landmarks = landmarks.copy()
        
        if enhancements.get('jaw', 0) > 0:
            strength = enhancements['jaw'] / 100.0
            current_landmarks = self.enhance_jawline(current_landmarks, strength)
            print(f"  ✅ Jaw enhancement applied: {enhancements['jaw']}%")
        
        if enhancements.get('cheek', 0) > 0:
            strength = enhancements['cheek'] / 100.0  
            current_landmarks = self.enhance_cheekbones(current_landmarks, strength)
            print(f"  ✅ Cheekbone lift applied: {enhancements['cheek']}%")
        
        if enhancements.get('eye', 0) > 0:
            strength = enhancements['eye'] / 100.0
            current_landmarks = self.enhance_eyes(current_landmarks, strength)
            print(f"  ✅ Eye enlargement applied: {enhancements['eye']}%")
        
        if enhancements.get('nose', 0) > 0:
            strength = enhancements['nose'] / 100.0
            current_landmarks = self.slim_nose(current_landmarks, strength)
            print(f"  ✅ Nose refinement applied: {enhancements['nose']}%")
        
        if enhancements.get('lips', 0) > 0:
            strength = enhancements['lips'] / 100.0
            current_landmarks = self.enhance_lips(current_landmarks, strength)
            print(f"  ✅ Lip enhancement applied: {enhancements['lips']}%")
        
        morphed_image = self.morph_image(image, landmarks, current_landmarks)
        return morphed_image
    
    def process_image(self, input_path, enhancements, output_path=None):
        """Process single image"""
        print(f"📁 Processing: {input_path}")
        
        image = cv2.imread(input_path)
        if image is None:
            raise ValueError(f"Cannot load image: {input_path}")
        
        print("🔍 Detecting face landmarks...")
        landmarks = self.detect_landmarks(image)
        
        if landmarks is None:
            raise ValueError("No face detected in the image")
        
        print("🎭 Applying face morphing...")
        enhanced_image = self.apply_face_morphing(image, landmarks, enhancements)
        
        if output_path is None:
            base_name = os.path.splitext(input_path)[0]
            output_path = f"{base_name}_enhanced.jpg"
        
        cv2.imwrite(output_path, enhanced_image)
        print(f"💾 Saved: {output_path}")
        
        return output_path

def main():
    parser = argparse.ArgumentParser(description='Advanced Face Morphing - CPU Version')
    parser.add_argument('input', help='Input image path')
    parser.add_argument('--output', '-o', help='Output image path')
    parser.add_argument('--jaw', type=int, default=70, help='Jaw enhancement (0-100)')
    parser.add_argument('--cheek', type=int, default=60, help='Cheekbone lift (0-100)')
    parser.add_argument('--eye', type=int, default=50, help='Eye enlargement (0-100)')
    parser.add_argument('--nose', type=int, default=40, help='Nose refinement (0-100)')
    parser.add_argument('--lips', type=int, default=50, help='Lip enhancement (0-100)')
    
    args = parser.parse_args()
    
    enhancements = {
        'jaw': args.jaw,
        'cheek': args.cheek,
        'eye': args.eye,
        'nose': args.nose,
        'lips': args.lips
    }
    
    print("✨ Advanced Face Morphing - CPU Version")
    print("=" * 50)
    
    try:
        morpher = CPUFaceMorpher()
        
        print("\n🎯 Enhancement Settings:")
        for key, value in enhancements.items():
            print(f"  {key}: {value}%")
        
        print()
        output_path = morpher.process_image(args.input, enhancements, args.output)
        
        print("\n✅ Face morphing completed successfully!")
        print(f"📊 Original: {args.input}")
        print(f"📊 Enhanced: {output_path}")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\n💡 Tips:")
        print("1. Make sure landmark model file exists")
        print("2. Use clear front-facing face photos")
        print("3. Adjust enhancement values (0-100)")

if __name__ == "__main__":
    main()
```

## 3. Batch Processing Script

Buat `batch_morph.py` untuk proses banyak gambar:

```python
import os
import glob
from face_morph_cli import CPUFaceMorpher

def batch_process(input_folder, output_folder, enhancements):
    """Process all images in folder"""
    
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Supported image formats
    image_extensions = ['*.jpg', '*.jpeg', '*.png', '*.bmp']
    image_files = []
    
    for extension in image_extensions:
        image_files.extend(glob.glob(os.path.join(input_folder, extension)))
        image_files.extend(glob.glob(os.path.join(input_folder, extension.upper())))
    
    if not image_files:
        print("❌ No images found in input folder")
        return
    
    print(f"📁 Found {len(image_files)} images to process")
    
    morpher = CPUFaceMorpher()
    processed_count = 0
    
    for image_path in image_files:
        try:
            filename = os.path.basename(image_path)
            name, ext = os.path.splitext(filename)
            output_path = os.path.join(output_folder, f"{name}_enhanced{ext}")
            
            print(f"\n🔄 Processing: {filename}")
            morpher.process_image(image_path, enhancements, output_path)
            processed_count += 1
            
        except Exception as e:
            print(f"❌ Failed to process {filename}: {e}")
            continue
    
    print(f"\n✅ Batch processing completed!")
    print(f"📊 Processed: {processed_count}/{len(image_files)} images")
    print(f"📁 Output folder: {output_folder}")

if __name__ == "__main__":
    # Enhancement settings
    enhancements = {
        'jaw': 70,    # Strong jawline
        'cheek': 60,  # Prominent cheekbones  
        'eye': 50,    # Larger eyes
        'nose': 40,   # Slimmer nose
        'lips': 50    # Fuller lips
    }
    
    input_folder = "input_images"
    output_folder = "output_images"
    
    batch_process(input_folder, output_folder, enhancements)
```

## 4. Simple Interactive Version

Buat `interactive_morph.py`:

```python
import os
from face_morph_cli import CPUFaceMorpher

def get_enhancement_value(feature_name, default=50):
    """Get enhancement value from user"""
    while True:
        try:
            value = input(f"Enter {feature_name} enhancement (0-100) [{default}]: ").strip()
            if value == "":
                return default
            value = int(value)
            if 0 <= value <= 100:
                return value
            else:
                print("Please enter value between 0-100")
        except ValueError:
            print("Please enter a valid number")

def main():
    print("✨ Interactive Face Morphing")
    print("=" * 40)
    
    # Get input file
    while True:
        input_file = input("\nEnter image file path: ").strip()
        if os.path.exists(input_file):
            break
        print("❌ File not found. Please try again.")
    
    # Get enhancement values
    print("\n🎯 Set Enhancement Levels (0-100):")
    print("0 = No change, 50 = Moderate, 100 = Maximum")
    print("-" * 50)
    
    enhancements = {
        'jaw': get_enhancement_value("jawline", 70),
        'cheek': get_enhancement_value("cheekbones", 60),
        'eye': get_enhancement_value("eyes", 50),
        'nose': get_enhancement_value("nose", 40),
        'lips': get_enhancement_value("lips", 50)
    }
    
    # Get output file
    base_name = os.path.splitext(input_file)[0]
    default_output = f"{base_name}_enhanced.jpg"
    output_file = input(f"\nEnter output file path [{default_output}]: ").strip()
    if not output_file:
        output_file = default_output
    
    # Process image
    print("\n🔄 Starting face morphing...")
    try:
        morpher = CPUFaceMorpher()
        result_path = morpher.process_image(input_file, enhancements, output_file)
        
        print(f"\n✅ Success! Enhanced image saved as: {result_path}")
        print("\n🎉 Face morphing completed!")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    main()
```

## Cara Menggunakan:

1. **Install dependencies**:
```bash
python install_cpu.py
```

2. **Download landmark model**:
   - Download: http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2
   - Extract dan rename ke `shape_predictor_68_face_landmarks.dat`

3. **Single image processing**:
```bash
# Basic usage
python face_morph_cli.py input.jpg

# Custom enhancements
python face_morph_cli.py input.jpg --jaw 80 --cheek 70 --eye 60 --nose 30 --lips 60

# With custom output
python face_morph_cli.py input.jpg --output result.jpg --jaw 70 --cheek 50
```

4. **Interactive mode**:
```bash
python interactive_morph.py
```

5. **Batch processing**:
   - Taruh semua gambar di folder `input_images`
   - Jalankan: `python batch_morph.py`

## Keunggulan:

- ✅ **Pure CPU** - Tidak butuh GPU
- ✅ **No GUI** - Tidak menyebabkan BSOD
- ✅ **Advanced morphing** - Ubah struktur wajah
- ✅ **Command line** - Cepat dan efisien
- ✅ **Batch processing** - Bisa proses banyak gambar
- ✅ **Customizable** - Kontrol penuh enhancement levels

Coba versi ini - seharusnya lebih stabil dan tidak menyebabkan BSOD!
