Oke William, kita cari solusi yang tetap transparan, efisien, dan bebas dari software yang kamu tidak suka. Kalau kamu mengalami **critical kernel error** dan **bluescreen** saat browsing dengan hardware acceleration aktif, itu menandakan ada interaksi bermasalah antara Chrome, driver GPU, dan sistem file. Kita akan fokus pada 3 area: **stabilitas driver**, **konsistensi disk**, dan **pengaturan sistem**.

---

### 🔧 Langkah-Langkah Pencegahan BSOD Tanpa CrystalDiskInfo

#### 1. **Nonaktifkan Hardware Acceleration di Chrome**
Karena ini pemicu langsung saat scrolling panjang:
- Buka `chrome://settings/system`
- Matikan opsi **"Use hardware acceleration when available"**
- Restart Chrome

#### 2. **Perbaiki File Sistem dan Bad Sector**
Karena kamu sudah tahu `chkdsk /f /r` efektif, kita bisa jadwalkan otomatis saat idle:
- Buka Command Prompt sebagai Administrator
- Jalankan:
  ```cmd
  schtasks /create /tn "DiskCheck" /tr "cmd /c chkdsk C: /f /r" /sc weekly /d SUN /st 03:00 /ru SYSTEM
  ```
  Ini akan menjalankan `chkdsk /f /r` setiap Minggu jam 3 pagi.

#### 3. **Perbaiki File Windows yang Rusak**
Jalankan dua perintah ini:
```cmd
sfc /scannow
DISM /Online /Cleanup-Image /RestoreHealth
```
Ini akan memperbaiki file sistem yang rusak tanpa software tambahan.

#### 4. **Update Driver GPU Secara Manual**
Tanpa software pihak ketiga:
- Buka `Device Manager`
- Klik kanan GPU → **Update driver** → **Browse my computer** → arahkan ke folder driver terbaru dari situs resmi (NVIDIA/AMD/Intel)

#### 5. **Matikan Fitur Privacy Sandbox di Chrome**
Walau tidak langsung menyebabkan BSOD, ini bisa mengurangi beban sistem:
- Buka `chrome://settings/privacySandbox`
- Nonaktifkan semua opsi

#### 6. **Cegah Paging Error dan Kernel Panic**
Ubah pengaturan virtual memory:
- Buka **System Properties** → Advanced → Performance → Settings → Advanced → Virtual Memory
- Set ke **Custom size**:
  - Initial size: sama dengan RAM kamu (misal 4096 MB untuk 4 GB)
  - Maximum size: 1.5x RAM (misal 6144 MB untuk 4 GB)

---

### 🧠 Tambahan Opsional: Automasi Deteksi & Pemulihan
Kamu bisa buat skrip di Tasker atau MacroDroid untuk:
- Deteksi freeze saat Chrome aktif + scrolling panjang
- Kirim perintah shell untuk logoff atau restart ringan
- Jadwalkan `sfc /scannow` mingguan saat idle

Kalau kamu mau, aku bisa bantu buat blueprint-nya. Mau kita lanjut ke automasi anti-BSOD berbasis shell + Tasker?
