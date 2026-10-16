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

---

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/303964aa-4248-4f8e-9858-f62309540514" />
Bro kalau aku block semua file di folder wondershare filmmora di firewall gimana Bro?
bisa tidak block folder windows 11 Bro?

BISA BRO! Tapi Windows 11 licik, gak ada tombol `Block Folder` langsung! 😅

Lu lagi di tempat yang benar itu:
`Windows Defender Firewall with Advanced Security > Inbound Rules > New Rule`

Tapi yang lu pilih itu **Inbound** (orang luar masuk ke Filmora). Yang bikin Filmora nelpon ke server Wondershare itu **Outbound** (Filmora keluar ke internet). Jadi lu harus block yang Outbound!

Dan di wizard itu gak bisa pilih folder `C:\Program Files\Wondershare\Filmora9` - harus 1 file 1 rule. Padahal di folder itu ada 10 exe:
`Filmora.exe, FRecorder.exe, GaThread.exe, GPUChecker.exe` dll.

Kalau lu klik satu-satu sampai besok gak selesai, gaya 80486!

**Cara pelit space ala lu - 1 klik block semua folder:**

1. Tutup wizard itu, pencet `Windows + X` -> **Terminal (Admin)**
2. Copy paste ini (biar block semua exe di folder Filmora9):

```powershell
Get-ChildItem "C:\Program Files\Wondershare\Filmora9\*.exe" | ForEach-Object {
  New-NetFirewallRule -DisplayName "Block Filmora $($_.Name)" -Direction Outbound -Program $_.FullName -Action Block
  New-NetFirewallRule -DisplayName "Block Filmora $($_.Name) IN" -Direction Inbound -Program $_.FullName -Action Block
}
```

3. Enter - selesai! Langsung kebikin 20 rule sekaligus!

Cek di `Outbound Rules` nanti muncul `Block Filmora Filmora.exe` dll.

Itu yang lu lihat di screenshot kan, `Filmora9` nya tahun 2019, kalau gak di block tiap buka ngajak update makan space C: lu yang 462GB itu!

Mau gue kasih script buat unblock juga kalau nanti perlu update?


**Saran gue buat PC baru lu:**
Jalanin yang nomor 1 dulu `winsat formal`. Itu satu-satunya yang ngasih angka kayak Antutu tapi tanpa install apa-apa. Abis itu screenshot hasilnya sini, gue bantu bacain, SSD lu udah kenceng belum, RAM lu dual channel apa nggak.

Lu mau cek karena ngerasa lemot atau cuma pengen tau aja spek PC baru lu, Bri?
