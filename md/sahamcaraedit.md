Kamu bisa mengubah daftar saham pantauan sendiri tanpa perlu minta saya (DeepSeek) menulis ulang file HTML-nya. Caranya cukup edit satu bagian di dalam file `saham.html` menggunakan teks editor biasa (Notepad, VS Code, dll).

## 📌 Lokasi yang perlu diedit

Cari baris kode JavaScript yang berisi **`const BANK_SYMBOLS = [`** (kira-kira di bagian tengah file). Di dalam tanda kurung siku `[ ... ]` itulah daftar semua kode saham yang muncul di dashboard.

Contoh potongan kode aslinya:

```javascript
const BANK_SYMBOLS = [
    "BBCA", "BMRI", "BBRI", "BBNI", "SUPA", "ARTO", "BBYB", "BANK", "AGRO", "AMAR",
    "BRIS", "BNGA", "NISP", "BDMN", "BNLI", "PNBN", "BBTN", "MEGA", "BNII", "BTPN",
    "BTPS", "BSIM", "BBKP", "BABP", "NOBU", "BINA", "BGTG", "BMAS", "MAYA", "BNBA",
    "BACA", "INPC", "BVIC", "BCIC", "DNAR", "BKSW", "BJBR", "BJTM", "BEKS", "BSWD",
    "BBHI", "CFIN", "DNET", "MCOR", "MREI", "PANS"
];
```

## ✏️ Cara menambahkan saham baru

1. **Buka file** `saham.html` dengan teks editor.
2. **Cari** `const BANK_SYMBOLS = [` (bisa pakai fitur pencarian Ctrl+F).
3. **Tambahkan** kode saham baru di dalam kurung siku, misal `"TLKM"`, `"ASII"`, `"UNVR"`.
   - Gunakan tanda petik dua `"` di sekitar kode saham.
   - Pisahkan dengan koma `,` setelah item sebelumnya.
4. **Simpan** file.

Contoh hasil setelah menambah `"TLKM"` dan `"ASII"`:

```javascript
const BANK_SYMBOLS = [
    "BBCA", "BMRI", "BBRI", "BBNI", "SUPA", "ARTO", "BBYB", "BANK", "AGRO", "AMAR",
    "BRIS", "BNGA", "NISP", "BDMN", "BNLI", "PNBN", "BBTN", "MEGA", "BNII", "BTPN",
    "BTPS", "BSIM", "BBKP", "BABP", "NOBU", "BINA", "BGTG", "BMAS", "MAYA", "BNBA",
    "BACA", "INPC", "BVIC", "BCIC", "DNAR", "BKSW", "BJBR", "BJTM", "BEKS", "BSWD",
    "BBHI", "CFIN", "DNET", "MCOR", "MREI", "PANS",
    "TLKM", "ASII"          // <-- tambahkan di sini
];
```

## ⚠️ Hal penting yang harus diperhatikan

- **Google Sheets kamu harus punya kolom dengan header yang sama persis** dengan kode saham yang ditambahkan.  
  Misal kamu tambah `"TLKM"`, maka di file CSV/Spreadsheet harus ada kolom bernama `TLKM` yang berisi data harga saham TLKM.

- **Urutan kolom di CSV tidak masalah** karena kode akan membaca berdasarkan nama header. Asalkan nama header cocok dengan salah satu `BANK_SYMBOLS`, data akan muncul.

- **Hapus saham** cukup hapus baris kode saham yang tidak diinginkan dari array `BANK_SYMBOLS` (jangan lupa hapus koma yang berlebih).

## 🧠 Alternatif jika ingin lebih fleksibel (tanpa edit file)

Kalau kamu merasa akan sering menambah/mengubah daftar saham, kamu bisa minta saya untuk memodifikasi HTML agar daftar saham dibaca otomatis dari **baris pertama CSV** (header). Dengan begitu, cukup edit Google Sheets (tambah/hapus kolom) dan dashboard akan menyesuaikan tanpa perlu sentuh file HTML sama sekali.

Silakan bilang jika mau saya buatkan versi yang **auto-detect kolom** dari CSV. Saya bisa tulis ulang bagian kodenya sekali saja, dan selanjutnya kamu hanya perlu edit spreadsheet.

---

**Kesimpulan:**  
Cukup edit array `BANK_SYMBOLS` di file HTML seperti contoh di atas, pastikan Google Sheets-mu memiliki kolom sesuai kode saham yang ditambahkan, lalu reload halaman. Selesai.
