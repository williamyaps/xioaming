Tanpa install apa-apa pun bisa Bro, Windows 11 emang udah ada alat ukurnya sendiri. Antutu itu aslinya buat HP, di PC malah nggak akurat.

Lu kan PC baru, coba 3 cara bawaan ini aja:

### 1. Cara paling mirip Antutu - pakai `WinSAT` (ini skor resmi Windows)

Ini yang dulu namanya Windows Experience Index. Di Windows 11 nggak ditampilin di Setting, tapi datanya masih ada.

- Klik Start > ketik `CMD` > klik kanan > **Run as Administrator**
- Ketik:
  ```
  winsat formal
  ```
  Tunggu 2-3 menit, dia bakal tes CPU, GPU, RAM, Disk.

- Abis beres, di CMD yang sama ketik:
  ```
  powershell Get-CimInstance Win32_WinSAT
  ```

Nanti keluar skornya kayak gini:
- **CPUScore** - skor processor
- **D3DScore** - skor gaming / GPU
- **DiskScore** - kecepatan SSD lu
- **GraphicsScore** - grafis desktop
- **MemoryScore** - RAM

Nilai 9.9 itu paling tinggi. Kalau SSD NVMe baru biasanya DiskScore 9++.

### 2. Cara paling cepat - Task Manager

Tekan `Ctrl + Shift + Esc` > tab **Performance**

Di situ keliatan live:
- CPU speed berapa GHz jalan
- RAM kepake berapa / speed DDR4 atau DDR5
- GPU lu apa (Intel / Nvidia / AMD)
- Disk SSD read/write berapa MB/s

Ini bukan skor, tapi lu bisa langsung liat PC lu kenceng atau ketahan di mana.

### 3. Cara paling lengkap - `dxdiag` + About

- Tekan `Win + R` > ketik `dxdiag` > Enter
  Di tab System keliatan processor + RAM, di tab Display keliatan VRAM VGA lu.

- Atau `Settings > System > About` - di situ ada Device specifications lengkap.

**Saran gue buat PC baru lu:**
Jalanin yang nomor 1 dulu `winsat formal`. Itu satu-satunya yang ngasih angka kayak Antutu tapi tanpa install apa-apa. Abis itu screenshot hasilnya sini, gue bantu bacain, SSD lu udah kenceng belum, RAM lu dual channel apa nggak.

Lu mau cek karena ngerasa lemot atau cuma pengen tau aja spek PC baru lu, Bri?
