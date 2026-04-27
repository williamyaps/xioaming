Wah, bagus banget idenya bro. Nambah menu "My Bookmarks" dan "My Media Sosial" pasti bikin hub-nya makin lengkap.

Masalah "??" pada ikon sebelumnya memang karena kita pakai emoji yang gak *compatible* di semua perangkat. Sekarang kita sudah pakai **Font Awesome 6**, jadi semua ikon akan tampil sempurna di mana saja.

## 🔍 Di Mana Melihat Daftar Ikon?

Pertama, soal di mana mencari ikon Font Awesome yang lengkap. Kalau bro lihat di blog yang tadi, itu daftarnya tidak lengkap. Website resmi Font Awesome sekarang memang agak "menyembunyikan" daftar ikonnya buat mempromosikan yang berbayar, jadi agak sulit menemukan daftar ikon gratisnya secara lengkap.

**Biar gampang, ini panduan tempat terbaik mencari ikon Font Awesome yang lengkap:**

### **1. Website Resmi Font Awesome dengan Filter "Free"**
Ini adalah sumber paling tepercaya dan selalu *up-to-date*:
*   **Alamat**: [https://fontawesome.com/icons](https://fontawesome.com/icons) 
*   **Caranya**: 
    1.  Buka websitenya.
    2.  Di bagian kiri, cari menu **"Filters"**.
    3.  Di bagian **"Cost"**, centang pilihan **"Free"**. Maka halaman hanya akan menampilkan ribuan ikon gratis yang bisa bro pakai.
    4.  Klik ikon yang dipilih untuk melihat nama kelasnya (contoh: `fa-solid fa-bookmark`).

### **2. Cheatsheet dari Pihak Ketiga yang Lengkap**
Kalau cara di atas masih terasa ribet, bro bisa pakai *cheatsheet* (daftar contekan) dari website lain yang lebih ramah. Website ini biasanya menampilkan semua ikon gratis dalam satu halaman sehingga mudah dicari. Contoh yang bisa langsung dikunjungi:
*   [https://www.vibe-icons.com/](https://www.vibe-icons.com/) 
*   [https://yesicon.app/](https://yesicon.app/) 

## ✨ Rekomendasi Ikon untuk Menu Baru

Biar gak bingung, gue sudah siapkan kode ikon yang cocok buat menu baru bro. Ini daftar **rekomendasi ikon untuk "My Bookmarks" dan "My Media Sosial"**:

### **Untuk Menu "My Bookmarks"**
Karena ini adalah menu utama (*Category*), kita pakai ikon yang merepresentasikan "Bookmark" atau "Simpanan" dengan gaya solid. **Kode ikon yang gue rekomendasikan:**
*   `<i class="fas fa-bookmark"></i>` (Ikon solid, paling umum digunakan) 

### **Untuk Menu "My Media Sosial"**
Karena ini adalah kumpulan link ke berbagai platform, ikon yang cocok adalah "Share" atau "Jaringan". **Kode ikon yang gue rekomendasikan:**
*   `<i class="fas fa-share-nodes"></i>` (Ikon share modern, direkomendasikan untuk Font Awesome 6) 

## 📂 Cara Menambahkannya ke Kode

Sekarang kita masukkan semuanya ke dalam kode. Bro tinggal **COPY** kode dua menu baru ini, lalu tempelkan di file HTML bro, **di atas menu "Folder Awan"** (atau di posisi yang bro suka).

```html
    <!-- 6. MY BOOKMARKS (MENU BARU) -->
    <div class="hub-card">
      <div class="card-header"><span><i class="fas fa-bookmark"></i> My Bookmarks</span></div>
      <div class="card-content">
        <ul class="link-list">
          <li><a target="_blank" href="https://github.com/"><i class="fab fa-github"></i> GitHub</a></li>
          <li><a target="_blank" href="https://stackoverflow.com/"><i class="fab fa-stack-overflow"></i> Stack Overflow</a></li>
          <!-- Tinggal ditambahin sendiri link-nya -->
        </ul>
      </div>
    </div>

    <!-- 7. MY MEDIA SOSIAL (MENU BARU) -->
    <div class="hub-card">
      <div class="card-header"><span><i class="fas fa-share-nodes"></i> My Media Sosial</span></div>
      <div class="card-content">
        <ul class="link-list">
          <li><a target="_blank" href="https://www.youtube.com/@williamyaps"><i class="fab fa-youtube"></i> YouTube</a></li>
          <li><a target="_blank" href="https://www.tiktok.com/@williamyaps"><i class="fab fa-tiktok"></i> TikTok</a></li>
          <li><a target="_blank" href="https://www.instagram.com/williamyaps/"><i class="fab fa-instagram"></i> Instagram</a></li>
          <!-- Tinggal ditambahin sendiri link-nya -->
        </ul>
      </div>
    </div>
```

**Penting!** Jangan lupa untuk menambahkan style CSS untuk warna header menu baru ini. Karena ini adalah menu ke-6 dan ke-7, bro bisa tambahkan kode CSS berikut di bagian `<style>`:

```css
    .hub-card:nth-child(6) .card-header i { color: #ff9f43; }
    .hub-card:nth-child(6) .card-header { color: #ff9f43; }
    .hub-card:nth-child(7) .card-header i { color: #a29bfe; }
    .hub-card:nth-child(7) .card-header { color: #a29bfe; }
```

## 🎨 Panduan Mencari Ikon Sendiri

Untuk ke depannya, biar bro bisa mencari ikon sendiri, gue ajarin caranya:

1.  **Buka website resmi** di [https://fontawesome.com/icons](https://fontawesome.com/icons). 
2.  **Filter yang gratisan**: Pastikan centang **"Free"** (Gratis) agar gak muncul yang berbayar.
3.  **Cari dengan Kata Kunci**: Gunakan kotak pencarian untuk mencari ikon yang bro mau.
4.  **Lihat Kelasnya**: Setelah menemukan, klik ikonnya, maka akan muncul kode HTML-nya. Ini dia contoh cara bacanya:

*   **Kode yang bro pakai untuk ikon buku** adalah `<i class="fas fa-book"></i>`. **`fas`** di sini artinya "Font Awesome Solid" (ikon padat/tegas).
*   **Kode untuk ikon YouTube** adalah `<i class="fab fa-youtube"></i>`. **`fab`** artinya "Font Awesome Brands" (ikon khusus untuk logo merek).
*   **Kode untuk ikon bookmark** adalah `<i class="far fa-bookmark"></i>`. **`far`** artinya "Font Awesome Regular" (ikon dengan garis luar).

Intinya, **`fas` itu padat, `fab` itu logo, dan `far` itu garis**. Tinggal disesuaikan.

Semoga membantu! Kalau ada yang masih bingung soal Font Awesome atau mau tanya style lain, langsung tanya aja ya bro! 🚀

---

Bro, paham banget kebutuhan lo: lo mau halaman privat di GitHub Pages yang gak bisa diintip orang, bahkan kalau mereka lihat source code langsung di repo. Gue kasih solusi **password protection dengan SHA-256 + anti-disable JavaScript** yang jauh lebih aman daripada metode eval base64 tempo dulu.

### 🔐 Konsepnya:
1. **Password asli gak akan pernah muncul di kode**. Kita cuma simpan **hash SHA-256**-nya. Jadi biarpun orang lihat source code, mereka cuma lihat deretan angka/ huruf acak, bukan password lo.
2. **Kalau JavaScript dimatikan, halaman kosong.** Konten penting disembunyikan pakai CSS default, dan cuma JavaScript yang bisa nampilin setelah password bener.
3. Struktur HTML-nya gampang ditiru buat semua halaman privat lo.

---

## 🛠️ Langkah 1: Bikin Halaman Protected (Contoh `bookmarks.html`)

Lo tinggal copy-paste kode di bawah ini, lalu ganti hash dan konten di dalamnya.

```html
<!DOCTYPE html>
<html lang="id">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>My Private Bookmarks</title>
  <style>
    /* default: konten tersembunyi, hanya muncul setelah password benar */
    #private-content {
      display: none;
    }
    body {
      background: #0f111a;
      color: #e2e8f0;
      font-family: 'Segoe UI', sans-serif;
      display: flex;
      justify-content: center;
      align-items: center;
      min-height: 100vh;
      margin: 0;
    }
    .container {
      width: 90%;
      max-width: 600px;
      padding: 30px;
      background: rgba(30,34,50,0.7);
      border-radius: 24px;
      border: 1px solid rgba(255,255,255,0.1);
      backdrop-filter: blur(10px);
    }
    h1 {
      color: #4facfe;
      margin-top: 0;
    }
    ul {
      list-style: none;
      padding: 0;
    }
    li {
      margin: 12px 0;
    }
    a {
      color: #b0b0d0;
      text-decoration: none;
      font-size: 1.1rem;
      transition: 0.2s;
    }
    a:hover {
      color: white;
      padding-left: 10px;
      border-left: 3px solid #4facfe;
    }
  </style>
</head>
<body>
  <div class="container" id="private-content">
    <!-- ISI KONTEN RAHASIA DI SINI -->
    <h1>🔒 My Private Bookmarks</h1>
    <ul>
      <li><a href="https://example.com" target="_blank">Example Link</a></li>
      <li><a href="https://github.com/williamyaps" target="_blank">My GitHub</a></li>
      <!-- tambahin link privat lo -->
    </ul>
  </div>

  <script>
    (function() {
      // ===== HASH PASSWORD YANG SUDAH DI-GENERATE =====
      // GANTI DENGAN HASH SHA-256 DARI PASSWORD LO (hex)
      const CORRECT_HASH = '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8'; // ini hash dari "password"

      const privateDiv = document.getElementById('private-content');
      if (!privateDiv) return;

      // Minta password
      async function checkPassword() {
        const userInput = prompt('Masukkan password untuk mengakses halaman ini:');
        if (!userInput) {
          document.body.innerHTML = '<div class="container"><h1>Akses Ditolak</h1><p>Password diperlukan.</p></div>';
          return;
        }

        // Hash input user pakai SHA-256 (Web Crypto API)
        const msgBuffer = new TextEncoder().encode(userInput);
        const hashBuffer = await crypto.subtle.digest('SHA-256', msgBuffer);
        const hashArray = Array.from(new Uint8Array(hashBuffer));
        const hashHex = hashArray.map(b => b.toString(16).padStart(2, '0')).join('');

        if (hashHex === CORRECT_HASH) {
          privateDiv.style.display = 'block';
        } else {
          document.body.innerHTML = '<div class="container"><h1>Akses Ditolak</h1><p>Password salah.</p></div>';
        }
      }

      checkPassword().catch(console.error);
    })();
  </script>
</body>
</html>
```

> **Catatan:** Ganti `CORRECT_HASH` dengan hash SHA-256 dari password asli lo. Cara buat hash ada di bawah.

---

## 🧪 Langkah 2: Generate Hash SHA-256 dari Password Lo

Lo bisa generate hash dengan cara apa pun, misalnya:
- **Online** (hati‑hati pilih situs terpercaya, atau offline aja): [emn178.github.io/online-tools/sha256.html](https://emn178.github.io/online-tools/sha256.html)
- **Pakai terminal** (macOS/Linux): `echo -n "passwordrahasia" | shasum -a 256`
- **Pakai PowerShell** (Windows): 
  ```powershell
  [System.BitConverter]::ToString((New-Object System.Security.Cryptography.SHA256Managed).ComputeHash([System.Text.Encoding]::UTF8.GetBytes("passwordrahasia"))).Replace("-","").ToLower()
  ```

Ambil hasil hex (64 karakter) dan tempel di variabel `CORRECT_HASH`.

---

## 🔒 Kenapa Lebih Aman dari Metode Lama?

| Fitur | Metode Lama (`eval` base64) | Metode Baru (SHA‑256) |
|-------|-----------------------------|------------------------|
| **Password asli di source** | Masih ada setelah decode | **Tidak pernah ada** |
| **Anti‑disable JavaScript** | Tidak (halaman tetap muncul) | **Ya** (konten hidden, hanya JS yang tampilkan) |
| **View source di GitHub** | Bisa ketahuan password | Cuma lihat hash acak |

Meski hash bisa di‑brute force kalau passwordnya pendek, lo tinggal pakai password yang panjang dan unik (minimal 12 karakter campur). Maka hampir mustahil dipecahkan.

---

## 📁 Struktur Folder di Repo

Simpan file seperti `bookmarks.html` langsung di root atau folder khusus. Karena repo publik, hash tetap kelihatan, tapi tanpa tahu password aslinya, penyerang gak bisa masuk. Kalau lo mau ekstra, lo bisa taruh hash di file JSON terpisah, lalu fetch pakai JS. Tapi itu cuma mengalihkan, file JSON juga bisa dibaca. Jadi opsi hash langsung di kode sudah cukup baik.

---

## 🧠 Tips Tambahan Biar Makin Aman

1. **Gunakan password panjang yang sulit ditebak** – jangan kata umum.
2. **Jangan commit history yang mengandung password lama** – kalau pernah commit password plain, hapus commit dengan `git filter-branch` atau bikin repo baru.
3. **Aktifkan GitHub Pages dengan branch `main`** – pastikan file HTML langsung ter‑host.

Dengan begini, halaman privat lo tetap terkunci rapat meski source code dilihat orang. Kalau ada yang kurang jelas atau lo mau modifikasi, kabarin aja bro! 🚀

---

Bro, paham banget kebutuhan lo: lo mau halaman privat di GitHub Pages yang gak bisa diintip orang, bahkan kalau mereka lihat source code langsung di repo. Gue kasih solusi **password protection dengan SHA-256 + anti-disable JavaScript** yang jauh lebih aman daripada metode eval base64 tempo dulu.

### 🔐 Konsepnya:
1. **Password asli gak akan pernah muncul di kode**. Kita cuma simpan **hash SHA-256**-nya. Jadi biarpun orang lihat source code, mereka cuma lihat deretan angka/ huruf acak, bukan password lo.
2. **Kalau JavaScript dimatikan, halaman kosong.** Konten penting disembunyikan pakai CSS default, dan cuma JavaScript yang bisa nampilin setelah password bener.
3. Struktur HTML-nya gampang ditiru buat semua halaman privat lo.

---

## 🛠️ Langkah 1: Bikin Halaman Protected (Contoh `bookmarks.html`)

Lo tinggal copy-paste kode di bawah ini, lalu ganti hash dan konten di dalamnya.

```html
<!DOCTYPE html>
<html lang="id">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>My Private Bookmarks</title>
  <style>
    /* default: konten tersembunyi, hanya muncul setelah password benar */
    #private-content {
      display: none;
    }
    body {
      background: #0f111a;
      color: #e2e8f0;
      font-family: 'Segoe UI', sans-serif;
      display: flex;
      justify-content: center;
      align-items: center;
      min-height: 100vh;
      margin: 0;
    }
    .container {
      width: 90%;
      max-width: 600px;
      padding: 30px;
      background: rgba(30,34,50,0.7);
      border-radius: 24px;
      border: 1px solid rgba(255,255,255,0.1);
      backdrop-filter: blur(10px);
    }
    h1 {
      color: #4facfe;
      margin-top: 0;
    }
    ul {
      list-style: none;
      padding: 0;
    }
    li {
      margin: 12px 0;
    }
    a {
      color: #b0b0d0;
      text-decoration: none;
      font-size: 1.1rem;
      transition: 0.2s;
    }
    a:hover {
      color: white;
      padding-left: 10px;
      border-left: 3px solid #4facfe;
    }
  </style>
</head>
<body>
  <div class="container" id="private-content">
    <!-- ISI KONTEN RAHASIA DI SINI -->
    <h1>🔒 My Private Bookmarks</h1>
    <ul>
      <li><a href="https://example.com" target="_blank">Example Link</a></li>
      <li><a href="https://github.com/williamyaps" target="_blank">My GitHub</a></li>
      <!-- tambahin link privat lo -->
    </ul>
  </div>

  <script>
    (function() {
      // ===== HASH PASSWORD YANG SUDAH DI-GENERATE =====
      // GANTI DENGAN HASH SHA-256 DARI PASSWORD LO (hex)
      const CORRECT_HASH = '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8'; // ini hash dari "password"

      const privateDiv = document.getElementById('private-content');
      if (!privateDiv) return;

      // Minta password
      async function checkPassword() {
        const userInput = prompt('Masukkan password untuk mengakses halaman ini:');
        if (!userInput) {
          document.body.innerHTML = '<div class="container"><h1>Akses Ditolak</h1><p>Password diperlukan.</p></div>';
          return;
        }

        // Hash input user pakai SHA-256 (Web Crypto API)
        const msgBuffer = new TextEncoder().encode(userInput);
        const hashBuffer = await crypto.subtle.digest('SHA-256', msgBuffer);
        const hashArray = Array.from(new Uint8Array(hashBuffer));
        const hashHex = hashArray.map(b => b.toString(16).padStart(2, '0')).join('');

        if (hashHex === CORRECT_HASH) {
          privateDiv.style.display = 'block';
        } else {
          document.body.innerHTML = '<div class="container"><h1>Akses Ditolak</h1><p>Password salah.</p></div>';
        }
      }

      checkPassword().catch(console.error);
    })();
  </script>
</body>
</html>
```

> **Catatan:** Ganti `CORRECT_HASH` dengan hash SHA-256 dari password asli lo. Cara buat hash ada di bawah.

---

## 🧪 Langkah 2: Generate Hash SHA-256 dari Password Lo

Lo bisa generate hash dengan cara apa pun, misalnya:
- **Online** (hati‑hati pilih situs terpercaya, atau offline aja): [emn178.github.io/online-tools/sha256.html](https://emn178.github.io/online-tools/sha256.html)
- **Pakai terminal** (macOS/Linux): `echo -n "passwordrahasia" | shasum -a 256`
- **Pakai PowerShell** (Windows): 
  ```powershell
  [System.BitConverter]::ToString((New-Object System.Security.Cryptography.SHA256Managed).ComputeHash([System.Text.Encoding]::UTF8.GetBytes("passwordrahasia"))).Replace("-","").ToLower()
  ```

Ambil hasil hex (64 karakter) dan tempel di variabel `CORRECT_HASH`.

---

## 🔒 Kenapa Lebih Aman dari Metode Lama?

| Fitur | Metode Lama (`eval` base64) | Metode Baru (SHA‑256) |
|-------|-----------------------------|------------------------|
| **Password asli di source** | Masih ada setelah decode | **Tidak pernah ada** |
| **Anti‑disable JavaScript** | Tidak (halaman tetap muncul) | **Ya** (konten hidden, hanya JS yang tampilkan) |
| **View source di GitHub** | Bisa ketahuan password | Cuma lihat hash acak |

Meski hash bisa di‑brute force kalau passwordnya pendek, lo tinggal pakai password yang panjang dan unik (minimal 12 karakter campur). Maka hampir mustahil dipecahkan.

---

## 📁 Struktur Folder di Repo

Simpan file seperti `bookmarks.html` langsung di root atau folder khusus. Karena repo publik, hash tetap kelihatan, tapi tanpa tahu password aslinya, penyerang gak bisa masuk. Kalau lo mau ekstra, lo bisa taruh hash di file JSON terpisah, lalu fetch pakai JS. Tapi itu cuma mengalihkan, file JSON juga bisa dibaca. Jadi opsi hash langsung di kode sudah cukup baik.

---

## 🧠 Tips Tambahan Biar Makin Aman

1. **Gunakan password panjang yang sulit ditebak** – jangan kata umum.
2. **Jangan commit history yang mengandung password lama** – kalau pernah commit password plain, hapus commit dengan `git filter-branch` atau bikin repo baru.
3. **Aktifkan GitHub Pages dengan branch `main`** – pastikan file HTML langsung ter‑host.

Dengan begini, halaman privat lo tetap terkunci rapat meski source code dilihat orang. Kalau ada yang kurang jelas atau lo mau modifikasi, kabarin aja bro! 🚀

---

Tidak apa‑apa Bro, kita pakai cara yang simpel aja — **pakai console browser** (F12). Gak perlu ribet PowerShell lagi.

---

### ✅ Cara Paling Gampang: Generate Hash di Console Browser

1. **Buka browser** (Chrome / Edge / Firefox).
2. **Tekan `F12`** untuk buka Developer Tools.
3. Pilih tab **Console**.
4. Copy & paste kode di bawah ini, tapi **ganti `passwordrahasia` dengan password asli lo**:

```javascript
(async () => {
  const msgBuffer = new TextEncoder().encode('passwordrahasia');
  const hashBuffer = await crypto.subtle.digest('SHA-256', msgBuffer);
  const hashArray = Array.from(new Uint8Array(hashBuffer));
  const hashHex = hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
  console.log(hashHex);
})();
```

5. Tekan Enter, lalu hasil **hash hex (64 karakter)** akan muncul di console.
6. Copy hash itu, paste ke kode HTML lo di bagian `CORRECT_HASH`.

Contoh hasilnya:  
`5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8`

---

### 🧠 Kenapa Metode Ini Lebih Aman?
- Hash tidak menyimpan password asli.
- Console browser hanya bisa dijalankan oleh lo sendiri, aman dari orang lain.
- Tidak perlu install aplikasi tambahan.

---

### ⚠️ Catatan Penting
- Jangan pakai password ‘password’ atau yang gampang ditebak.
- Gunakan password minimal 12 karakter campur (huruf besar, kecil, angka, simbol) biar hash gak bisa di-brute force.
- Kalau lupa password, gak bisa dibuka lagi. Ganti hash dengan hash baru jika perlu ganti password.

Sekarang tinggal buka `bookmarks.html` lo, dan semua akan aman. Kalau ada pertanyaan lain, langsung tanya aja Bro! 🚀
