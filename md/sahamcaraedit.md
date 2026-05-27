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

---

**Jawaban singkat:**  
Ya, **cukup tambahkan `"SEA"` di dalam array `BANK_SYMBOLS`** (kira‑kira baris 1613 di file `saham.html`), asalkan posisinya **sesuai dengan urutan kolom** di Google Sheets Anda.

---

## 🔍 Penjelasan teknis

Di dalam file `saham.html` yang sekarang, fungsi `loadCSV()` membaca data dengan asumsi:

- Kolom **pertama** = tanggal  
- Kolom **kedua, ketiga, dst** = harga saham sesuai urutan `BANK_SYMBOLS`  

Contoh potongan kode yang relevan:

```javascript
for (let i = 0; i < BANK_SYMBOLS.length; i++) {
    const sym = BANK_SYMBOLS[i];
    const colName = headers[i + 1];   // ambil kolom ke-(i+1)
    let price = parsePrice(row[colName]);
    priceMap[sym].push(price);
}
```

Jadi jika Anda menambahkan saham **SEA** di kolom terbaru (misal kolom AW), maka Anda hanya perlu:

1. **Tambahkan `"SEA"` di akhir array `BANK_SYMBOLS`** (setelah kode saham terakhir yang sudah ada).
2. **Simpan file** dan **refresh** halaman dashboard.

Semua fitur lain (grafik, portofolio, BEP, volatilitas, dll) akan otomatis mengenali saham baru karena semuanya menggunakan array `BANK_SYMBOLS` yang sudah diperbarui.

---

## ⚠️ Hal penting yang perlu diperhatikan

- **Urutan harus sama persis** antara kolom di CSV dan urutan di `BANK_SYMBOLS`.  
  - Jika Anda menambahkan SEA di kolom AW (paling kanan), maka `"SEA"` harus menjadi **elemen terakhir** di array.
- **Jangan ubah nama kolom** di CSV. Biarkan tetap "Close" – kode tetap berfungsi karena membaca berdasarkan urutan, bukan nama kolom.
- **Tidak perlu** mengganti `CSV_URL` atau `PROXY`.

---

## 📝 Contoh perubahan di file `saham.html`

Cari baris yang kurang lebih seperti ini (bisa di baris 1613):

```javascript
const BANK_SYMBOLS = [
    "BBCA", "BMRI", "BBRI", "BBNI", "SUPA", "ARTO", "BBYB", "BANK", "AGRO", "AMAR",
    "BRIS", "BNGA", "NISP", "BDMN", "BNLI", "PNBN", "BBTN", "MEGA", "BNII", "BTPN",
    "BTPS", "BSIM", "BBKP", "BABP", "NOBU", "BINA", "BGTG", "BMAS", "MAYA", "BNBA",
    "BACA", "INPC", "BVIC", "BCIC", "DNAR", "BKSW", "BJBR", "BJTM", "BEKS", "BSWD",
    "BBHI", "CFIN", "DNET", "MCOR", "MREI", "PANS"
];
```

Ubah menjadi (tambahkan `"SEA"` di akhir, setelah `"PANS"`):

```javascript
const BANK_SYMBOLS = [
    "BBCA", "BMRI", "BBRI", "BBNI", "SUPA", "ARTO", "BBYB", "BANK", "AGRO", "AMAR",
    "BRIS", "BNGA", "NISP", "BDMN", "BNLI", "PNBN", "BBTN", "MEGA", "BNII", "BTPN",
    "BTPS", "BSIM", "BBKP", "BABP", "NOBU", "BINA", "BGTG", "BMAS", "MAYA", "BNBA",
    "BACA", "INPC", "BVIC", "BCIC", "DNAR", "BKSW", "BJBR", "BJTM", "BEKS", "BSWD",
    "BBHI", "CFIN", "DNET", "MCOR", "MREI", "PANS",
    "SEA"   // <-- tambahkan di sini
];
```

Setelah itu **simpan** dan **refresh** halaman. Data SEA akan langsung muncul di selector, grafik, dan seluruh analisis.

---

## 🧠 Kesimpulan

> **Cukup edit satu baris (tambah nama saham di array `BANK_SYMBOLS` sesuai urutan kolom), tanpa perlu mengubah bagian lain dari kode.**  

Dengan cara ini, Anda bebas menambah/mengurangi saham kapan pun, selama urutan array selalu sama dengan urutan kolom di Google Sheets.

Jika nanti Anda ingin benar‑benar **otomatis 100%** (tanpa perlu edit array setiap kali tambah kolom), silakan minta saya buatkan versi dengan **deteksi header otomatis** – tapi untuk kebutuhan Anda saat ini, solusi manual di atas sudah cukup dan paling simpel.
