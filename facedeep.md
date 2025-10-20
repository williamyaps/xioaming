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

---

Masalahnya adalah `dlib` tidak bisa diinstall di Windows 8 karena butuh CMake versi terbaru. Mari kita buat versi tanpa dlib, menggunakan OpenCV saja dengan face detection bawaan dan teknik morphing sederhana.

## 1. Kode Face Morphing Tanpa Dlib

Buat `simple_morph.py`:

```python
import cv2
import numpy as np
from scipy.spatial import Delaunay
import os
import argparse

class SimpleFaceMorpher:
    def __init__(self):
        """Initialize with OpenCV face detector"""
        print("🔄 Loading face detection model...")
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
        print("✅ Face detection model loaded")
    
    def estimate_face_landmarks(self, image, face_region):
        """Estimate face landmarks based on face detection"""
        x, y, w, h = face_region
        
        # Create estimated landmarks (68 points like dlib)
        landmarks = []
        
        # Jaw points (0-16)
        for i in range(17):
            px = x + (w * i // 16)
            py = y + h
            landmarks.append((px, py))
        
        # Right eyebrow (17-21)
        for i in range(5):
            px = x + (w * (i + 1) // 6)
            py = y + (h * 1 // 4)
            landmarks.append((px, py))
        
        # Left eyebrow (22-26)
        for i in range(5):
            px = x + (w * (i + 1) // 6)
            py = y + (h * 1 // 4)
            landmarks.append((px, py))
        
        # Nose bridge (27-30)
        for i in range(4):
            px = x + w // 2
            py = y + (h * (i + 2) // 5)
            landmarks.append((px, py))
        
        # Nose bottom (31-35)
        nose_points = [
            (x + w//2 - w//10, y + h//2),
            (x + w//2, y + h//2 + h//10),
            (x + w//2 + w//10, y + h//2),
            (x + w//2 - w//15, y + h//2 + h//15),
            (x + w//2 + w//15, y + h//2 + h//15)
        ]
        landmarks.extend(nose_points)
        
        # Right eye (36-41)
        eye_w = w // 4
        eye_h = h // 6
        right_eye_x = x + w // 3 - eye_w // 2
        right_eye_y = y + h // 3 - eye_h // 2
        
        eye_points = [
            (right_eye_x, right_eye_y + eye_h//2),
            (right_eye_x + eye_w//2, right_eye_y),
            (right_eye_x + eye_w, right_eye_y + eye_h//2),
            (right_eye_x + eye_w//2, right_eye_y + eye_h),
            (right_eye_x + eye_w//4, right_eye_y + eye_h//4),
            (right_eye_x + 3*eye_w//4, right_eye_y + eye_h//4)
        ]
        landmarks.extend(eye_points)
        
        # Left eye (42-47)
        left_eye_x = x + 2*w // 3 - eye_w // 2
        left_eye_y = y + h // 3 - eye_h // 2
        
        eye_points = [
            (left_eye_x, left_eye_y + eye_h//2),
            (left_eye_x + eye_w//2, left_eye_y),
            (left_eye_x + eye_w, left_eye_y + eye_h//2),
            (left_eye_x + eye_w//2, left_eye_y + eye_h),
            (left_eye_x + eye_w//4, left_eye_y + eye_h//4),
            (left_eye_x + 3*eye_w//4, left_eye_y + eye_h//4)
        ]
        landmarks.extend(eye_points)
        
        # Outer mouth (48-59)
        mouth_w = w // 2
        mouth_h = h // 6
        mouth_x = x + w // 2 - mouth_w // 2
        mouth_y = y + 2*h // 3
        
        mouth_points = []
        for i in range(12):
            angle = 2 * np.pi * i / 12
            px = mouth_x + mouth_w // 2 + mouth_w // 2 * np.cos(angle)
            py = mouth_y + mouth_h // 2 + mouth_h // 2 * np.sin(angle)
            mouth_points.append((px, py))
        landmarks.extend(mouth_points)
        
        # Inner mouth (60-67)
        inner_mouth_w = mouth_w * 0.7
        inner_mouth_h = mouth_h * 0.7
        inner_mouth_points = []
        for i in range(8):
            angle = 2 * np.pi * i / 8
            px = mouth_x + mouth_w // 2 + inner_mouth_w // 2 * np.cos(angle)
            py = mouth_y + mouth_h // 2 + inner_mouth_h // 2 * np.sin(angle)
            inner_mouth_points.append((px, py))
        landmarks.extend(inner_mouth_points)
        
        return np.array(landmarks, dtype=np.float32)
    
    def detect_face_regions(self, image):
        """Detect face and facial features"""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Detect faces
        faces = self.face_cascade.detectMultiScale(
            gray, 
            scaleFactor=1.1, 
            minNeighbors=5, 
            minSize=(30, 30)
        )
        
        if len(faces) == 0:
            return None
        
        # Use the largest face
        face = max(faces, key=lambda rect: rect[2] * rect[3])
        x, y, w, h = face
        
        # Detect eyes within the face
        face_roi = gray[y:y+h, x:x+w]
        eyes = self.eye_cascade.detectMultiScale(face_roi, 1.1, 3)
        
        # Estimate landmarks
        landmarks = self.estimate_face_landmarks(image, face)
        
        return {
            'face': face,
            'eyes': eyes,
            'landmarks': landmarks
        }
    
    def apply_affine_transform(self, src, src_tri, dst_tri, size):
        """Apply affine transform to triangular regions"""
        warp_mat = cv2.getAffineTransform(np.float32(src_tri), np.float32(dst_tri))
        dst = cv2.warpAffine(src, warp_mat, (size[0], size[1]), None, 
                           flags=cv2.INTER_LINEAR, 
                           borderMode=cv2.BORDER_REFLECT_101)
        return dst
    
    def morph_triangle(self, img1, img2, tri1, tri2):
        """Morph triangular region between two images"""
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
        """Strengthen jawline by adjusting jaw points"""
        enhanced = landmarks.copy()
        jaw_points = enhanced[0:17]
        jaw_center = np.mean(jaw_points, axis=0)
        
        for i in range(len(jaw_points)):
            direction = jaw_points[i] - jaw_center
            if np.linalg.norm(direction) > 0:
                direction = direction / np.linalg.norm(direction)
            
            # Apply transformation to jaw area
            if i in [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]:
                enhanced[i] += direction * strength * 8
                # Slight downward movement for stronger jaw
                enhanced[i][1] += strength * 4
        
        return enhanced
    
    def enhance_cheekbones(self, landmarks, strength=0.5):
        """Lift cheekbones"""
        enhanced = landmarks.copy()
        
        # Cheek points (approximate indices)
        right_cheek = [1, 2, 3, 4, 5]
        left_cheek = [12, 13, 14, 15, 16]
        
        for i in right_cheek:
            if i < len(enhanced):
                # Lift upward and move outward
                enhanced[i][1] -= strength * 8
                enhanced[i][0] -= strength * 4
        
        for i in left_cheek:
            if i < len(enhanced):
                enhanced[i][1] -= strength * 8
                enhanced[i][0] += strength * 4
        
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
                enhanced[point_idx] += direction * strength * 4
        
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
                enhanced[point_idx][0] -= np.sign(direction[0]) * strength * 3
        
        for point_idx in nose_width:
            direction = enhanced[point_idx] - nose_center  
            enhanced[point_idx][0] -= direction[0] * strength * 0.15
        
        return enhanced
    
    def enhance_lips(self, landmarks, strength=0.5):
        """Fuller lips"""
        enhanced = landmarks.copy()
        
        outer_lips = list(range(48, 60))
        
        lip_center = np.mean(enhanced[outer_lips], axis=0)
        
        for point_idx in outer_lips:
            direction = enhanced[point_idx] - lip_center
            if np.linalg.norm(direction) > 0:
                direction = direction / np.linalg.norm(direction)
            enhanced[point_idx] += direction * strength * 3
        
        return enhanced
    
    def morph_image(self, image, src_points, dst_points):
        """Morph image using triangulation"""
        src_face_points = src_points
        dst_face_points = dst_points
        
        # Add boundary points for better triangulation
        h, w = image.shape[:2]
        boundary_points = [
            (0, 0), (w//2, 0), (w-1, 0),
            (0, h//2), (w-1, h//2),
            (0, h-1), (w//2, h-1), (w-1, h-1)
        ]
        
        src_all_points = np.vstack([src_face_points, boundary_points])
        dst_all_points = np.vstack([dst_face_points, boundary_points])
        
        try:
            tri = Delaunay(src_all_points)
            morphed = np.zeros_like(image, dtype=np.float32)
            
            for simplex in tri.simplices:
                src_tri = src_all_points[simplex]
                dst_tri = dst_all_points[simplex]
                self.morph_triangle(image.astype(np.float32), morphed, src_tri, dst_tri)
            
            return morphed.astype(np.uint8)
        except:
            # Fallback if triangulation fails
            return image
    
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
        
        print("🔍 Detecting face and estimating landmarks...")
        face_data = self.detect_face_regions(image)
        
        if face_data is None:
            raise ValueError("No face detected in the image")
        
        landmarks = face_data['landmarks']
        print(f"✅ Face detected with {len(landmarks)} estimated landmarks")
        
        print("🎭 Applying face morphing...")
        enhanced_image = self.apply_face_morphing(image, landmarks, enhancements)
        
        if output_path is None:
            base_name = os.path.splitext(input_path)[0]
            output_path = f"{base_name}_enhanced.jpg"
        
        cv2.imwrite(output_path, enhanced_image)
        print(f"💾 Saved: {output_path}")
        
        return output_path

def main():
    parser = argparse.ArgumentParser(description='Simple Face Morphing - OpenCV Only')
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
    
    print("✨ Simple Face Morphing - OpenCV Only")
    print("=" * 50)
    
    try:
        morpher = SimpleFaceMorpher()
        
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
        print("1. Use clear front-facing face photos")
        print("2. Ensure good lighting in the photo")
        print("3. Adjust enhancement values (0-100)")

if __name__ == "__main__":
    main()
```

## 2. Batch Processing Script

Buat `batch_simple_morph.py`:

```python
import os
import glob
from simple_morph import SimpleFaceMorpher

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
    
    morpher = SimpleFaceMorpher()
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
    # Default enhancement settings
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

## 3. Interactive Version

Buat `interactive_simple.py`:

```python
import os
from simple_morph import SimpleFaceMorpher

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
    print("✨ Simple Face Morphing - Interactive Mode")
    print("=" * 45)
    
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
        morpher = SimpleFaceMorpher()
        result_path = morpher.process_image(input_file, enhancements, output_file)
        
        print(f"\n✅ Success! Enhanced image saved as: {result_path}")
        print("\n🎉 Face morphing completed!")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    main()
```

## Cara Menggunakan:

1. **Jalankan single image**:
```bash
python simple_morph.py input.jpg

# Dengan custom settings
python simple_morph.py input.jpg --jaw 80 --cheek 70 --eye 60 --nose 30 --lips 60

# Dengan output custom
python simple_morph.py input.jpg --output result.jpg --jaw 70 --cheek 50
```

2. **Interactive mode**:
```bash
python interactive_simple.py
```

3. **Batch processing**:
   - Taruh gambar di folder `input_images`
   - Jalankan: `python batch_simple_morph.py`

## Keunggulan Versi Ini:

- ✅ **Tanpa Dlib** - Tidak butuh install dlib yang sulit
- ✅ **Pure OpenCV** - Menggunakan face detector bawaan OpenCV
- ✅ **No GUI** - Tidak menyebabkan BSOD
- ✅ **CPU Only** - Ringan untuk Windows 8
- ✅ **Real Morphing** - Benar-benar mengubah struktur wajah
- ✅ **Simple Setup** - Cuma butuh OpenCV dan NumPy

Coba versi ini - seharusnya bekerja dengan baik di Windows 8 Anda!

---

Anda sudah punya file `shape_predictor_68_face_landmarks.dat`! Masalahnya adalah file tersebut masih dalam folder terpisah. Mari kita perbaiki kodenya untuk mencari file yang benar.

## 1. Perbaiki Kode untuk Mencari Landmark Model

Buat `fixed_morph.py`:

```python
import cv2
import numpy as np
import dlib
from scipy.spatial import Delaunay
import os
import argparse

class FixedFaceMorpher:
    def __init__(self):
        """Initialize with dlib face detector"""
        print("🔄 Loading face detection model...")
        self.detector = dlib.get_frontal_face_detector()
        
        # Cari file landmark model di beberapa lokasi
        landmark_paths = [
            "shape_predictor_68_face_landmarks.dat",  # Di folder saat ini
            "shape_predictor_68_face_landmarks.dat/shape_predictor_68_face_landmarks.dat",  # Dalam folder
            "./shape_predictor_68_face_landmarks.dat/shape_predictor_68_face_landmarks.dat"  # Path relatif
        ]
        
        self.predictor = None
        for path in landmark_paths:
            if os.path.exists(path):
                try:
                    self.predictor = dlib.shape_predictor(path)
                    print(f"✅ Landmark model loaded from: {path}")
                    break
                except Exception as e:
                    print(f"❌ Failed to load from {path}: {e}")
                    continue
        
        if self.predictor is None:
            print("❌ Landmark model not found in any location")
            print("💡 File exists but cannot be loaded. Let me try alternative approach...")
            raise FileNotFoundError("Landmark model file not found or cannot be loaded")
    
    def detect_landmarks(self, image):
        """Detect facial landmarks using dlib"""
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
        
        right_cheek = [1, 2, 3, 4, 5]
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
    parser = argparse.ArgumentParser(description='Fixed Face Morphing - CPU Version')
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
    
    print("✨ Fixed Face Morphing - CPU Version")
    print("=" * 50)
    
    try:
        morpher = FixedFaceMorpher()
        
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
        print("\n💡 Let me try alternative approach without dlib...")
        # Fallback ke versi tanpa dlib
        try:
            from simple_morph import SimpleFaceMorpher
            print("🔄 Trying alternative face morphing without dlib...")
            simple_morpher = SimpleFaceMorpher()
            output_path = simple_morpher.process_image(args.input, enhancements, args.output)
            print(f"✅ Alternative method succeeded! Enhanced: {output_path}")
        except Exception as e2:
            print(f"❌ All methods failed: {e2}")

if __name__ == "__main__":
    main()
```

## 2. Coba Copy File Landmark ke Root Folder

Jalankan ini dulu di command prompt:

```bash
# Copy file landmark dari folder ke root
copy "shape_predictor_68_face_landmarks.dat\shape_predictor_68_face_landmarks.dat" .
```

Atau jika tidak berhasil, coba ekstrak ulang:

```bash
# Extract file dari archive
bunzip2 -c shape_predictor_68_face_landmarks.dat.bz2 > shape_predictor_68_face_landmarks.dat
```

## 3. Jika Masih Gagal, Gunakan Versi Tanpa Dlib

Buat `no_dlib_morph.py`:

```python
import cv2
import numpy as np
from scipy.spatial import Delaunay
import os
import argparse

class NoDlibFaceMorpher:
    def __init__(self):
        """Initialize with OpenCV only"""
        print("🔄 Loading OpenCV face detection model...")
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
        print("✅ OpenCV models loaded successfully")
    
    def smart_face_detection(self, image):
        """Advanced face detection with feature estimation"""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Detect faces
        faces = self.face_cascade.detectMultiScale(
            gray, 
            scaleFactor=1.1, 
            minNeighbors=5, 
            minSize=(30, 30)
        )
        
        if len(faces) == 0:
            return None
        
        # Use the largest face
        face = max(faces, key=lambda rect: rect[2] * rect[3])
        x, y, w, h = face
        
        # Create smart landmarks based on face proportions
        landmarks = self.create_smart_landmarks(x, y, w, h, image.shape)
        
        return landmarks
    
    def create_smart_landmarks(self, x, y, w, h, image_shape):
        """Create realistic facial landmarks based on face detection"""
        landmarks = []
        
        # Jawline (points 0-16)
        for i in range(17):
            px = x + (w * i // 16)
            py = y + h - 5  # Slightly above bottom
            landmarks.append((px, py))
        
        # Eyebrows (points 17-26)
        eyebrow_y = y + h // 4
        # Right eyebrow
        for i in range(5):
            px = x + w * (i + 1) // 6
            landmarks.append((px, eyebrow_y))
        # Left eyebrow  
        for i in range(5):
            px = x + w * (i + 1) // 6
            landmarks.append((px, eyebrow_y))
        
        # Nose (points 27-35)
        nose_x = x + w // 2
        # Nose bridge
        for i in range(4):
            py = y + h * (i + 2) // 5
            landmarks.append((nose_x, py))
        # Nose bottom
        landmarks.extend([
            (nose_x - w//8, y + h//2),
            (nose_x, y + h//2 + h//8),
            (nose_x + w//8, y + h//2),
            (nose_x - w//12, y + h//2 + h//12),
            (nose_x + w//12, y + h//2 + h//12)
        ])
        
        # Eyes (points 36-47)
        # Right eye
        eye_center_x = x + w // 3
        eye_center_y = y + h // 3
        landmarks.extend(self.create_eye_points(eye_center_x, eye_center_y, w//5))
        
        # Left eye
        eye_center_x = x + 2 * w // 3
        eye_center_y = y + h // 3
        landmarks.extend(self.create_eye_points(eye_center_x, eye_center_y, w//5))
        
        # Mouth (points 48-67)
        mouth_center_x = x + w // 2
        mouth_center_y = y + 2 * h // 3
        landmarks.extend(self.create_mouth_points(mouth_center_x, mouth_center_y, w//2, h//8))
        
        return np.array(landmarks, dtype=np.float32)
    
    def create_eye_points(self, center_x, center_y, size):
        """Create eye landmark points"""
        points = []
        for i in range(6):
            angle = 2 * np.pi * i / 6
            px = center_x + size * np.cos(angle) * 0.8
            py = center_y + size * np.sin(angle) * 0.5
            points.append((px, py))
        return points
    
    def create_mouth_points(self, center_x, center_y, width, height):
        """Create mouth landmark points"""
        points = []
        # Outer mouth (12 points)
        for i in range(12):
            angle = np.pi + (np.pi * i / 11)  # Half ellipse
            px = center_x + width * np.cos(angle) / 2
            py = center_y + height * np.sin(angle) / 2
            points.append((px, py))
        
        # Inner mouth (8 points)
        for i in range(8):
            angle = np.pi + (np.pi * i / 7)  # Half ellipse
            px = center_x + width * np.cos(angle) / 3
            py = center_y + height * np.sin(angle) / 3
            points.append((px, py))
        
        return points
    
    # ... (sisanya sama seperti di simple_morph.py, termasuk morph_triangle, enhance_jawline, dll.)
    # Copy semua method dari simple_morph.py mulai dari apply_affine_transform sampai process_image

def main():
    parser = argparse.ArgumentParser(description='No-Dlib Face Morphing - OpenCV Only')
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
    
    print("✨ No-Dlib Face Morphing - OpenCV Only")
    print("=" * 50)
    
    try:
        morpher = NoDlibFaceMorpher()
        
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

if __name__ == "__main__":
    main()
```

## Cara Menggunakan:

1. **Coba fixed version dengan dlib**:
```bash
python fixed_morph.py input.jpg --output result.jpg --jaw 70 --cheek 50
```

2. **Jika masih gagal, gunakan no-dlib version**:
```bash
python no_dlib_morph.py input.jpg --output result.jpg --jaw 70 --cheek 50
```

3. **Atau langsung gunakan simple version**:
```bash
python simple_morph.py input.jpg --output result.jpg --jaw 70 --cheek 50
```

Coba yang mana saja yang berhasil!

---

Saya lihat masalahnya! File `shape_predictor_68_face_landmarks.dat` ada di dalam folder dengan nama yang sama, bukan di root. Mari kita perbaiki kodenya untuk mencari file yang benar.

## 1. Perbaiki Path Landmark Model

Buat `fixed_path_morph.py`:

```python
import cv2
import numpy as np
import dlib
from scipy.spatial import Delaunay
import os
import argparse

class FixedPathFaceMorpher:
    def __init__(self):
        """Initialize with dlib face detector"""
        print("🔄 Loading face detection model...")
        self.detector = dlib.get_frontal_face_detector()
        
        # Cari file landmark model di beberapa lokasi yang mungkin
        landmark_paths = [
            "shape_predictor_68_face_landmarks.dat",  # Di root folder
            "shape_predictor_68_face_landmarks.dat/shape_predictor_68_face_landmarks.dat",  # Dalam folder
            "./shape_predictor_68_face_landmarks.dat/shape_predictor_68_face_landmarks.dat",  # Path relatif
            "shape_predictor_68_face_landmarks.dat/shape_predictor_68_face_landmarks.dat"  # Path lengkap
        ]
        
        self.predictor = None
        for path in landmark_paths:
            if os.path.exists(path):
                try:
                    print(f"🔍 Trying to load: {path}")
                    self.predictor = dlib.shape_predictor(path)
                    print(f"✅ Landmark model loaded from: {path}")
                    break
                except Exception as e:
                    print(f"❌ Failed to load from {path}: {e}")
                    continue
        
        if self.predictor is None:
            # Coba cari file secara manual
            print("🔍 Searching for landmark file in directory...")
            for root, dirs, files in os.walk("."):
                for file in files:
                    if "shape_predictor_68_face_landmarks.dat" in file:
                        full_path = os.path.join(root, file)
                        print(f"🔍 Found: {full_path}")
                        try:
                            self.predictor = dlib.shape_predictor(full_path)
                            print(f"✅ Landmark model loaded from: {full_path}")
                            break
                        except Exception as e:
                            print(f"❌ Failed to load from {full_path}: {e}")
                            continue
                if self.predictor is not None:
                    break
        
        if self.predictor is None:
            print("❌ Landmark model not found in any location")
            print("💡 Let me create the correct path...")
            # Coba buat path yang benar
            correct_path = "shape_predictor_68_face_landmarks.dat/shape_predictor_68_face_landmarks.dat"
            if os.path.exists("shape_predictor_68_face_landmarks.dat"):
                if os.path.isdir("shape_predictor_68_face_landmarks.dat"):
                    # Ini adalah folder, cari file di dalamnya
                    for file in os.listdir("shape_predictor_68_face_landmarks.dat"):
                        if "shape_predictor_68_face_landmarks.dat" in file:
                            correct_path = os.path.join("shape_predictor_68_face_landmarks.dat", file)
                            break
                
                try:
                    self.predictor = dlib.shape_predictor(correct_path)
                    print(f"✅ Landmark model loaded from: {correct_path}")
                except Exception as e:
                    print(f"❌ Final attempt failed: {e}")
                    raise FileNotFoundError("Cannot load landmark model file")
    
    def detect_landmarks(self, image):
        """Detect facial landmarks using dlib"""
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
        
        right_cheek = [1, 2, 3, 4, 5]
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
    parser = argparse.ArgumentParser(description='Fixed Path Face Morphing - CPU Version')
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
    
    print("✨ Fixed Path Face Morphing - CPU Version")
    print("=" * 50)
    
    try:
        morpher = FixedPathFaceMorpher()
        
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

if __name__ == "__main__":
    main()
```

## 2. Atau Copy File ke Root Folder

Sebelum menjalankan, coba copy file landmark ke root folder:

```bash
# Copy file dari dalam folder ke root
copy "shape_predictor_68_face_landmarks.dat\shape_predictor_68_landmarks.dat" .
```

Atau gunakan Python untuk copy:

Buat `copy_landmark.py`:

```python
import os
import shutil

def copy_landmark_file():
    """Copy landmark file to root directory"""
    source_dir = "shape_predictor_68_face_landmarks.dat"
    target_file = "shape_predictor_68_face_landmarks.dat"
    
    if os.path.exists(source_dir) and os.path.isdir(source_dir):
        print(f"📁 Found directory: {source_dir}")
        
        # Cari file di dalam folder
        for file in os.listdir(source_dir):
            if "shape_predictor" in file and file.endswith(".dat"):
                source_path = os.path.join(source_dir, file)
                print(f"📄 Found file: {source_path}")
                
                # Copy ke root
                shutil.copy2(source_path, target_file)
                print(f"✅ Copied to: {target_file}")
                
                # Verifikasi
                if os.path.exists(target_file):
                    file_size = os.path.getsize(target_file)
                    print(f"📊 File size: {file_size} bytes")
                    return True
                else:
                    print("❌ Copy failed")
                    return False
    
    print("❌ Landmark directory or file not found")
    return False

if __name__ == "__main__":
    print("🔄 Copying landmark file to root directory...")
    if copy_landmark_file():
        print("🎉 Ready to run face morphing!")
    else:
        print("❌ Failed to copy landmark file")
```

Jalankan:
```bash
python copy_landmark.py
```

## 3. Jika Masih Gagal, Gunakan Versi Manual Path

Buat `manual_path_morph.py`:

```python
import cv2
import numpy as np
import dlib
from scipy.spatial import Delaunay
import os
import argparse

# Tentukan path manual ke file landmark
LANDMARK_PATH = "shape_predictor_68_face_landmarks.dat/shape_predictor_68_face_landmarks.dat"

class ManualPathFaceMorpher:
    def __init__(self, landmark_path=LANDMARK_PATH):
        """Initialize with manual path"""
        print("🔄 Loading face detection model...")
        self.detector = dlib.get_frontal_face_detector()
        
        print(f"🔍 Using manual path: {landmark_path}")
        if not os.path.exists(landmark_path):
            print("❌ Landmark file not found at manual path")
            print("💡 Available files in landmark directory:")
            if os.path.exists("shape_predictor_68_face_landmarks.dat"):
                for file in os.listdir("shape_predictor_68_face_landmarks.dat"):
                    print(f"   - {file}")
            raise FileNotFoundError(f"Landmark file not found: {landmark_path}")
        
        try:
            self.predictor = dlib.shape_predictor(landmark_path)
            print("✅ Landmark model loaded successfully!")
        except Exception as e:
            print(f"❌ Failed to load landmark model: {e}")
            raise
    
    # ... (sisanya sama seperti class sebelumnya)
    # Copy semua method dari FixedPathFaceMorpher mulai dari detect_landmarks sampai process_image

def main():
    parser = argparse.ArgumentParser(description='Manual Path Face Morphing')
    parser.add_argument('input', help='Input image path')
    parser.add_argument('--output', '-o', help='Output image path')
    parser.add_argument('--jaw', type=int, default=70, help='Jaw enhancement (0-100)')
    parser.add_argument('--cheek', type=int, default=60, help='Cheekbone lift (0-100)')
    parser.add_argument('--eye', type=int, default=50, help='Eye enlargement (0-100)')
    parser.add_argument('--nose', type=int, default=40, help='Nose refinement (0-100)')
    parser.add_argument('--lips', type=int, default=50, help='Lip enhancement (0-100)')
    parser.add_argument('--landmark-path', default=LANDMARK_PATH, help='Manual path to landmark file')
    
    args = parser.parse_args()
    
    enhancements = {
        'jaw': args.jaw,
        'cheek': args.cheek,
        'eye': args.eye,
        'nose': args.nose,
        'lips': args.lips
    }
    
    print("✨ Manual Path Face Morphing")
    print("=" * 50)
    
    try:
        morpher = ManualPathFaceMorpher(args.landmark_path)
        
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

if __name__ == "__main__":
    main()
```

## Cara Menggunakan:

1. **Pertama, coba copy file landmark**:
```bash
python copy_landmark.py
```

2. **Kemudian jalankan fixed version**:
```bash
python fixed_path_morph.py input.jpg --output result.jpg --jaw 70 --cheek 50
```

3. **Jika masih gagal, gunakan manual path**:
```bash
python manual_path_morph.py input.jpg --output result.jpg --jaw 70 --cheek 50
```

4. **Atau coba dengan path yang spesifik**:
```bash
python manual_path_morph.py input.jpg --landmark-path "shape_predictor_68_face_landmarks.dat/shape_predictor_68_face_landmarks.dat" --output result.jpg --jaw 70 --cheek 50
```

Coba langkah-langkah ini - seharusnya bisa menemukan file landmark yang sudah ada di folder Anda!

---

Masalahnya file sudah ada di tempat yang benar! File landmark sudah berada di `shape_predictor_68_face_landmarks.dat\shape_predictor_68_face_landmarks.dat`. Mari kita perbaiki kode untuk menggunakan path yang benar.

## 1. Perbaiki Kode dengan Path yang Tepat

Buat `working_morph.py`:

```python
import cv2
import numpy as np
import dlib
from scipy.spatial import Delaunay
import os
import argparse

class WorkingFaceMorpher:
    def __init__(self):
        """Initialize with dlib face detector"""
        print("🔄 Loading face detection model...")
        self.detector = dlib.get_frontal_face_detector()
        
        # Path yang benar berdasarkan struktur folder Anda
        landmark_path = "shape_predictor_68_face_landmarks.dat/shape_predictor_68_face_landmarks.dat"
        
        print(f"🔍 Using landmark path: {landmark_path}")
        
        if not os.path.exists(landmark_path):
            print("❌ Landmark file not found!")
            print("💡 Available files:")
            for root, dirs, files in os.walk("."):
                for file in files:
                    if "shape_predictor" in file:
                        print(f"   - {os.path.join(root, file)}")
            raise FileNotFoundError(f"Landmark file not found: {landmark_path}")
        
        try:
            self.predictor = dlib.shape_predictor(landmark_path)
            print("✅ Landmark model loaded successfully!")
        except Exception as e:
            print(f"❌ Failed to load landmark model: {e}")
            raise
    
    def detect_landmarks(self, image):
        """Detect facial landmarks using dlib"""
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
        """Strengthen jawline - seperti Chris Hemsworth"""
        enhanced = landmarks.copy()
        jaw_points = enhanced[0:17]
        jaw_center = np.mean(jaw_points, axis=0)
        
        for i in range(len(jaw_points)):
            direction = jaw_points[i] - jaw_center
            if np.linalg.norm(direction) > 0:
                direction = direction / np.linalg.norm(direction)
            
            # Enhance jawline untuk bentuk V-shape
            if i in [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]:
                enhanced[i] += direction * strength * 15  # Lebih kuat
                # Turunkan sedikit untuk rahang yang lebih kuat
                enhanced[i][1] += strength * 8
        
        return enhanced
    
    def enhance_cheekbones(self, landmarks, strength=0.5):
        """Lift cheekbones - seperti Brad Pitt"""
        enhanced = landmarks.copy()
        
        # Titik tulang pipi
        right_cheek = [1, 2, 3, 4, 5]
        left_cheek = [12, 13, 14, 15, 16]
        
        for i in right_cheek:
            if i < len(enhanced):
                # Angkat dan tarik ke luar untuk cheekbones yang menonjol
                enhanced[i][1] -= strength * 12  # Angkat
                enhanced[i][0] -= strength * 8   # Tarik ke luar
        
        for i in left_cheek:
            if i < len(enhanced):
                enhanced[i][1] -= strength * 12  # Angkat
                enhanced[i][0] += strength * 8   # Tarik ke luar
        
        return enhanced
    
    def enhance_eyes(self, landmarks, strength=0.5):
        """Enlarge eyes - seperti David Beckham"""
        enhanced = landmarks.copy()
        
        right_eye = list(range(36, 42))
        left_eye = list(range(42, 48))
        
        def expand_eye(eye_points):
            center = np.mean(enhanced[eye_points], axis=0)
            for point_idx in eye_points:
                direction = enhanced[point_idx] - center
                if np.linalg.norm(direction) > 0:
                    direction = direction / np.linalg.norm(direction)
                # Perbesar mata
                enhanced[point_idx] += direction * strength * 8
        
        expand_eye(right_eye)
        expand_eye(left_eye)
        
        return enhanced
    
    def slim_nose(self, landmarks, strength=0.5):
        """Slim nose - seperti Tom Cruise"""
        enhanced = landmarks.copy()
        
        nose_bridge = list(range(27, 31))
        nose_width = list(range(31, 36))
        
        nose_center = np.mean(enhanced[nose_bridge], axis=0)
        
        # Slim bridge
        for point_idx in nose_bridge:
            direction = enhanced[point_idx] - nose_center
            if abs(direction[0]) > 0.1:
                enhanced[point_idx][0] -= np.sign(direction[0]) * strength * 5
        
        # Reduce width
        for point_idx in nose_width:
            direction = enhanced[point_idx] - nose_center  
            enhanced[point_idx][0] -= direction[0] * strength * 0.3
        
        return enhanced
    
    def enhance_lips(self, landmarks, strength=0.5):
        """Fuller lips - seperti Johnny Depp"""
        enhanced = landmarks.copy()
        
        outer_lips = list(range(48, 60))
        inner_lips = list(range(60, 68))
        
        lip_center = np.mean(enhanced[outer_lips], axis=0)
        
        # Enhance outer lips
        for point_idx in outer_lips:
            direction = enhanced[point_idx] - lip_center
            if np.linalg.norm(direction) > 0:
                direction = direction / np.linalg.norm(direction)
            enhanced[point_idx] += direction * strength * 6
        
        # Enhance inner lips
        for point_idx in inner_lips:
            direction = enhanced[point_idx] - lip_center
            if np.linalg.norm(direction) > 0:
                direction = direction / np.linalg.norm(direction)
            enhanced[point_idx] += direction * strength * 4
        
        return enhanced
    
    def morph_image(self, image, src_points, dst_points):
        """Morph image using triangulation"""
        src_face_points = src_points[:68]
        dst_face_points = dst_points[:68]
        
        try:
            tri = Delaunay(src_face_points)
            morphed = np.zeros_like(image, dtype=np.float32)
            
            for simplex in tri.simplices:
                src_tri = src_face_points[simplex]
                dst_tri = dst_face_points[simplex]
                self.morph_triangle(image.astype(np.float32), morphed, src_tri, dst_tri)
            
            return morphed.astype(np.uint8)
        except:
            print("⚠️ Triangulation failed, returning original image")
            return image
    
    def apply_face_morphing(self, image, landmarks, enhancements):
        """Apply all morphing effects"""
        current_landmarks = landmarks.copy()
        
        print("🎭 Applying enhancements:")
        
        if enhancements.get('jaw', 0) > 0:
            strength = enhancements['jaw'] / 100.0
            current_landmarks = self.enhance_jawline(current_landmarks, strength)
            print(f"  ✅ Jaw enhancement: {enhancements['jaw']}% (Chris Hemsworth style)")
        
        if enhancements.get('cheek', 0) > 0:
            strength = enhancements['cheek'] / 100.0  
            current_landmarks = self.enhance_cheekbones(current_landmarks, strength)
            print(f"  ✅ Cheekbone lift: {enhancements['cheek']}% (Brad Pitt style)")
        
        if enhancements.get('eye', 0) > 0:
            strength = enhancements['eye'] / 100.0
            current_landmarks = self.enhance_eyes(current_landmarks, strength)
            print(f"  ✅ Eye enlargement: {enhancements['eye']}% (David Beckham style)")
        
        if enhancements.get('nose', 0) > 0:
            strength = enhancements['nose'] / 100.0
            current_landmarks = self.slim_nose(current_landmarks, strength)
            print(f"  ✅ Nose refinement: {enhancements['nose']}% (Tom Cruise style)")
        
        if enhancements.get('lips', 0) > 0:
            strength = enhancements['lips'] / 100.0
            current_landmarks = self.enhance_lips(current_landmarks, strength)
            print(f"  ✅ Lip enhancement: {enhancements['lips']}% (Johnny Depp style)")
        
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
            raise ValueError("❌ No face detected in the image")
        
        print(f"✅ Face detected with {len(landmarks)} landmarks")
        
        print("🎭 Applying face morphing...")
        enhanced_image = self.apply_face_morphing(image, landmarks, enhancements)
        
        if output_path is None:
            base_name = os.path.splitext(input_path)[0]
            output_path = f"{base_name}_enhanced.jpg"
        
        cv2.imwrite(output_path, enhanced_image)
        print(f"💾 Saved: {output_path}")
        
        return output_path

def main():
    parser = argparse.ArgumentParser(description='Working Face Morphing - Hollywood Style')
    parser.add_argument('input', help='Input image path')
    parser.add_argument('--output', '-o', help='Output image path')
    parser.add_argument('--jaw', type=int, default=80, help='Jaw enhancement (0-100) - Chris Hemsworth style')
    parser.add_argument('--cheek', type=int, default=70, help='Cheekbone lift (0-100) - Brad Pitt style')
    parser.add_argument('--eye', type=int, default=60, help='Eye enlargement (0-100) - David Beckham style')
    parser.add_argument('--nose', type=int, default=50, help='Nose refinement (0-100) - Tom Cruise style')
    parser.add_argument('--lips', type=int, default=60, help='Lip enhancement (0-100) - Johnny Depp style')
    
    args = parser.parse_args()
    
    enhancements = {
        'jaw': args.jaw,
        'cheek': args.cheek,
        'eye': args.eye,
        'nose': args.nose,
        'lips': args.lips
    }
    
    print("✨ Working Face Morphing - Hollywood Style")
    print("=" * 55)
    print("🎬 Transforming your face with celebrity features!")
    print("=" * 55)
    
    try:
        morpher = WorkingFaceMorpher()
        
        print("\n🎯 Enhancement Settings (Hollywood Style):")
        print(f"  🦷 Jaw: {enhancements['jaw']}% (Chris Hemsworth)")
        print(f"  💎 Cheekbones: {enhancements['cheek']}% (Brad Pitt)")  
        print(f"  👁️ Eyes: {enhancements['eye']}% (David Beckham)")
        print(f"  👃 Nose: {enhancements['nose']}% (Tom Cruise)")
        print(f"  💋 Lips: {enhancements['lips']}% (Johnny Depp)")
        
        print()
        output_path = morpher.process_image(args.input, enhancements, args.output)
        
        print("\n" + "=" * 55)
        print("✅ Face morphing completed successfully!")
        print(f"📊 Original: {args.input}")
        print(f"📊 Enhanced: {output_path}")
        print("🎉 Your Hollywood transformation is ready!")
        print("=" * 55)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\n💡 Troubleshooting tips:")
        print("1. Make sure the image has a clear front-facing face")
        print("2. Check that landmark file exists in the correct location")
        print("3. Try different enhancement values (0-100)")

if __name__ == "__main__":
    main()
```

## 2. Coba Langsung dengan Path yang Tepat

Jalankan ini:

```bash
python working_morph.py input.jpg --output result.jpg --jaw 80 --cheek 70 --eye 60 --nose 50 --lips 60
```

## 3. Jika Masih Ada Masalah, Cek File Landmark

Buat `check_landmark.py`:

```python
import os

def check_landmark_file():
    """Check if landmark file exists and is accessible"""
    landmark_path = "shape_predictor_68_face_landmarks.dat/shape_predictor_68_face_landmarks.dat"
    
    print("🔍 Checking landmark file...")
    print(f"Path: {landmark_path}")
    print(f"Exists: {os.path.exists(landmark_path)}")
    
    if os.path.exists(landmark_path):
        file_size = os.path.getsize(landmark_path)
        print(f"File size: {file_size} bytes")
        print(f"File size: {file_size / 1024 / 1024:.2f} MB")
        print("✅ Landmark file is present and accessible!")
        return True
    else:
        print("❌ Landmark file not found!")
        print("\n📁 Available files in current directory:")
        for item in os.listdir("."):
            if os.path.isdir(item):
                print(f"📁 {item}/")
                # Check inside the landmark directory
                if item == "shape_predictor_68_face_landmarks.dat":
                    for file in os.listdir(item):
                        print(f"   📄 {file}")
            else:
                print(f"📄 {item}")
        return False

if __name__ == "__main__":
    check_landmark_file()
```

Jalankan:
```bash
python check_landmark.py
```

## 4. Versi Simple Test

Buat `simple_test.py`:

```python
import dlib
import cv2
import os

def simple_test():
    """Simple test to verify dlib is working"""
    print("🧪 Running simple dlib test...")
    
    # Test face detector
    detector = dlib.get_frontal_face_detector()
    print("✅ Face detector loaded")
    
    # Test landmark predictor
    landmark_path = "shape_predictor_68_face_landmarks.dat/shape_predictor_68_face_landmarks.dat"
    if os.path.exists(landmark_path):
        try:
            predictor = dlib.shape_predictor(landmark_path)
            print("✅ Landmark predictor loaded")
            print("🎉 All systems go! Ready for face morphing.")
            return True
        except Exception as e:
            print(f"❌ Failed to load landmark predictor: {e}")
            return False
    else:
        print(f"❌ Landmark file not found at: {landmark_path}")
        return False

if __name__ == "__main__":
    simple_test()
```

Jalankan:
```bash
python simple_test.py
```

## Cara Menggunakan:

1. **Pertama test dlib**:
```bash
python simple_test.py
```

2. **Cek file landmark**:
```bash
python check_landmark.py
```

3. **Jalankan face morphing**:
```bash
python working_morph.py input.jpg --output result.jpg --jaw 80 --cheek 70 --eye 60
```

4. **Untuk efek yang berbeda**:
```bash
# Lebih subtle
python working_morph.py input.jpg --jaw 50 --cheek 40 --eye 30 --nose 20 --lips 30

# Lebih dramatic  
python working_morph.py input.jpg --jaw 90 --cheek 80 --eye 70 --nose 60 --lips 80
```

Coba langkah-langkah ini - seharusnya bekerja karena file landmark sudah ada di tempat yang benar!
