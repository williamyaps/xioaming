saya mau tanya kamu, apa kamu tau kalau control D memiliki banyak settingannya?
saya check di:
https://wlmyaps.github.io/adblock/

untuk settingan DOH:
https://freedns.controld.com/p2
Ads & Tracking Configuration

(ini block 98%)

Hasil
https://www.grc.com/dns/dns.htm

![Logo](https://raw.githubusercontent.com/williamyaps/xioaming/refs/heads/master/images/controlDp2.jpg)

![cmdnscontrolDp2](https://github.com/user-attachments/assets/ec77b943-7833-4c3e-9471-880de22c4def)

---

Oke William 👍
Aku bantu jelaskan hasil test dari **Gibson Research Corporation (GRC) DNS Benchmark** yang kamu jalankan ke DoH ControlD (`https://freedns.controld.com/p2`).

GRC DNS Benchmark itu ngecek **kualitas dan keamanan DNS resolver** yang dipakai sistem kamu. Hasil yang kamu kasih sudah cukup detail, kita bahas bagian per bagian ya:

---

### 🔎 **Ringkasan Hasil**

* **Jumlah Nameserver Terpakai:**
  Ditemukan **2 server DNS** yang dipakai (`43.245.50.152` dan `23.171.240.157`).
  Artinya ControlD pakai **redundant resolver** biar kalau satu sibuk/down, ada backup.

* **Total Query:**
  379 query terkirim, semuanya dijawab (stabil).

---

### 🛡️ **Anti-Spoofing Safety**

> **Excellent**
> DNS spoofing itu trik orang jahat yang pura-pura jadi DNS server untuk kasih jawaban palsu.
> Hasil “Excellent” berarti ControlD punya **proteksi kuat terhadap spoofing**.

---

### 🎲 **Query Source Port Analysis**

* **Max Entropy:** 15.97 (Excellent)
* **Dir Bias:** 7.78% (Excellent)
* **Lost Entropy:** 0
* **Stuck Bits:** 0

🔹 Artinya:
ControlD **mengacak port asal** ketika mengirim query.
Ini penting, karena kalau port selalu sama, attacker bisa lebih gampang nebak query DNS → rentan spoofing.

Hasil kamu **sangat aman (Excellent).**

---

### 🔑 **Query Transaction ID Analysis**

* **Max Entropy:** 15.99 (Excellent)
* **Dir Bias:** 2.99% (Excellent)
* **Lost Entropy:** 0
* **Stuck Bits:** 0

🔹 Transaction ID = semacam “nomor seri” unik untuk tiap query.
Kalau nilainya random, attacker susah memalsukan balasan.
Hasil kamu juga **Excellent** → acakan ID bekerja dengan baik.

---

### 🌍 **DNS Nameserver Access Details**

**Server 1 → `43.245.50.152`**

* External Ping: replied → Server menjawab ping (lebih kelihatan di internet).
* External Query: ignored → Bagus, tidak melayani query publik (lebih aman).
* DNSSEC: supported → Mendukung DNSSEC (validasi kriptografi supaya jawaban DNS tidak bisa dipalsukan).
* Alphabetic Case: all lower → Semua huruf lower case. Idealnya mixed-case (0x20 encoding) lebih baik, tapi ini opsional.
* Extra Anti-Spoofing: unknown → GRC tidak bisa cek fingerprint tambahan.

**Server 2 → `23.171.240.157`**

* External Ping: ignored → Lebih tersembunyi, lebih aman.
* External Query: ignored → Sama, lebih spoof-resistant.
* DNSSEC: supported → Juga mendukung DNSSEC.
* Alphabetic Case: all lower.
* Extra Anti-Spoofing: unknown.

---

### 📌 **Kesimpulan**

* **ControlD DoH (p2)** yang kamu pakai **sangat aman** menurut GRC.
* Query randomness (port & ID) **Excellent** → hampir mustahil di-spoof.
* DNSSEC **aktif** → validasi aman.
* Ada 2 server (redundant) → stabil.
* Bedanya: satu server balas ping, satu tidak (lebih stealth).
* Kekurangan kecil: tidak pakai mixed-case encoding (bisa dianggap minor).

👉 Jadi, hasil kamu **aman banget** buat dipakai harian, terutama buat browsing + adblock (karena p2 = Ads & Tracking Block 98%).

---

Mau aku bikinin **tabel ringkas** per server biar gampang bandingkan `43.245.50.152` vs `23.171.240.157`?

---

Sip, aku bikinin tabel ringkas dari hasil GRC DNS Benchmark kamu untuk **ControlD DoH (p2)**.

---

### 📊 Perbandingan Hasil 2 DNS Server ControlD

| Fitur / Analisis              | `43.245.50.152`           | `23.171.240.157`            |
| ----------------------------- | ------------------------- | --------------------------- |
| **Status Anti-Spoofing**      | Excellent                 | Excellent                   |
| **Source Port Randomness**    | Excellent                 | Excellent                   |
| **Transaction ID Randomness** | Excellent                 | Excellent                   |
| **External Ping**             | Replied (terlihat publik) | Ignored (lebih tersembunyi) |
| **External Query**            | Ignored (aman)            | Ignored (aman)              |
| **DNSSEC Support**            | ✅ Supported               | ✅ Supported                 |
| **Alphabetic Case Encoding**  | All Lower Case            | All Lower Case              |
| **Extra Anti-Spoofing Check** | Unknown                   | Unknown                     |
| **Total Query Diuji**         | 335 query                 | 44 query                    |

---

### 📝 Catatan

* **Keduanya sama-sama aman & mendukung DNSSEC.**
* Perbedaan kecil:

  * `43.245.50.152` **bisa diping** (jadi lebih mudah terlihat di internet).
  * `23.171.240.157` **ignore ping** → lebih “stealth” alias susah dideteksi publik.
* Sisanya hampir identik (randomness Excellent, anti-spoofing oke).

---

Mau sekalian aku kasih **rekomendasi setting** (misalnya kalau pilih satu server utama, backup server mana lebih ideal)?

Yang ini dulu.
Bisa kamu bantu aku jelaskan hasil dari:
https://www.grc.com/dns/dns.htm

---
Oke William 👍 aku kasih rekomendasi berdasarkan hasil tes kamu:

---

## 🔧 **Rekomendasi Setting ControlD DoH (p2)**

| Server             | Kelebihan                                                                                           | Kekurangan                                                      | Cocok Dijadikan                                       |
| ------------------ | --------------------------------------------------------------------------------------------------- | --------------------------------------------------------------- | ----------------------------------------------------- |
| **43.245.50.152**  | Respon ping cepat (lebih mudah cek konektivitas), stabil, mendukung DNSSEC, anti-spoofing Excellent | Terlihat publik (balas ping) → lebih mudah dipetakan orang luar | **Primary (utama)** kalau mau lebih cepat tes koneksi |
| **23.171.240.157** | Stealth (tidak balas ping), mendukung DNSSEC, sama-sama aman, anti-spoofing Excellent               | Tidak bisa diping (jadi susah cek manual koneksi)               | **Secondary (backup)** karena lebih tersembunyi       |

---

### 📌 **Saran Konfigurasi**

1. **Primary:** `43.245.50.152`
   (lebih cepat terdeteksi aktif oleh sistem kamu karena balas ping).
2. **Secondary:** `23.171.240.157`
   (sebagai cadangan, lebih aman & stealth).

👉 Dengan kombinasi ini, kamu dapat **stabilitas + keamanan + fallback**.

---

Mau aku bikinin juga **versi konfigurasi siap pakai** untuk Windows / Android / Router (DoH / DoT / DNS IP)?

---

versi buatan ringkasan gpt

Sip 🔥 aku bikinin versi dengan **Daftar Isi (TOC)** otomatis, biar siapa pun buka langsung bisa klik ke bagian yang mau dipelajari.

---

# 🛡️ ControlD p2 – Ads & Tracking Block (98%)

## 📑 Daftar Isi

* [📌 Pendahuluan](#-pendahuluan)
* [📸 Hasil Uji (Screenshot)](#-hasil-uji-screenshot)
* [📊 Ringkasan Uji GRC DNS Benchmark](#-ringkasan-uji-grc-dns-benchmark)
* [📊 Perbandingan Server](#-perbandingan-server)
* [🔧 Rekomendasi Konfigurasi](#-rekomendasi-konfigurasi)
* [📘 Catatan Belajar](#-catatan-belajar)

---

## 📌 Pendahuluan

Dokumen ini adalah arsip pembelajaran tentang penggunaan **ControlD DoH (Profile p2)**, yang berfungsi memblokir **Iklan & Tracking (98%)**.
Hasil uji dilakukan dengan **GRC DNS Benchmark** untuk mengecek **keamanan & stabilitas resolver**.

---

## 📸 Hasil Uji (Screenshot)

![Hasil Benchmark](images/controlDp2.jpg)

---

## 📊 Ringkasan Uji GRC DNS Benchmark

### Jumlah Server

* **2 Server DNS** terdeteksi:

  * `43.245.50.152`
  * `23.171.240.157`

### Anti-Spoofing

* Status: **Excellent**
* Artinya server DNS tahan terhadap serangan **spoofing** (pemalsuan jawaban DNS).

### Randomness & Security

* **Source Port Randomness:** Excellent
* **Transaction ID Randomness:** Excellent
* **DNSSEC Support:** ✅ Supported (jawaban DNS tervalidasi kriptografi)

---

## 📊 Perbandingan Server

| Fitur / Analisis              | `43.245.50.152`           | `23.171.240.157`            |
| ----------------------------- | ------------------------- | --------------------------- |
| **Anti-Spoofing**             | Excellent                 | Excellent                   |
| **Source Port Randomness**    | Excellent                 | Excellent                   |
| **Transaction ID Randomness** | Excellent                 | Excellent                   |
| **External Ping**             | Replied (terlihat publik) | Ignored (lebih tersembunyi) |
| **External Query**            | Ignored (aman)            | Ignored (aman)              |
| **DNSSEC Support**            | ✅ Supported               | ✅ Supported                 |
| **Alphabetic Case Encoding**  | All Lower Case            | All Lower Case              |
| **Extra Anti-Spoofing Check** | Unknown                   | Unknown                     |
| **Total Query Diuji**         | 335 query                 | 44 query                    |

---

## 🔧 Rekomendasi Konfigurasi

* **Primary DNS:** `43.245.50.152`
  (Balas ping → lebih cepat dideteksi, stabil untuk koneksi utama).
* **Secondary DNS:** `23.171.240.157`
  (Stealth mode → lebih tersembunyi, sebagai cadangan).

Dengan kombinasi ini, pengguna mendapatkan:

* **Stabilitas** (primary aktif cepat)
* **Keamanan** (backup stealth + DNSSEC)
* **Proteksi iklan & tracking 98%**

---

## 📘 Catatan Belajar

* Arsip ini dibuat sebagai bahan pembelajaran & dokumentasi.
* Metode pembelajaran dengan **meng-archive** hasil percobaan → memudahkan review di kemudian hari.
* GRC DNS Benchmark bisa dipakai untuk mengecek kualitas resolver lain.

---

✨ Versi ini sudah ada **TOC klik-able** di GitHub (otomatis link ke section).

Mau aku sekalian tambahin **highlight code block konfigurasi DNS (Windows / Android / Router)** supaya praktis diingat langsung dari sini?

---

ini penggunaan dari:
DOH
https://freedns.controld.com/no-ads-malware-typo

Hasil:
https://www.grc.com/dns/dns.htm

Query                                                      Servers  Queries
Round  Receiving Nameserver Queries...(per round results)   Found   Received
-----  --------------------------------------------------  -------  --------
   1   ••••••••••                                             2         204    
   2   •••••••••                                              0          44    
   3   •••••••••                                              0          44    
   4   •••••••••                                              0          44    
   5   •••••••••                                              0          44    
                                                           -------  --------
                                   Totals for all rounds:     2         380   

Analysis of 336 queries from nameserver opens in separate window at [ 43.245.50.152 ]
Anti-Spoofing Safety: Excellent
Server Name: xsp-h04.int.controld.com

Query Source Port Analysis (worst case)
Max Entropy:	15.97	Excellent	Dir Bias:	0.9%	Excellent
Lost Entropy:	0.01	Excellent	Stuck Bits:	0	Excellent
 	 	
Query Transaction ID Analysis (worst case)
Max Entropy:	15.98	Excellent	Dir Bias:	5.07%	Excellent
Lost Entropy:	0	Excellent	Stuck Bits:	0	Excellent
DNS Nameserver Access Details
External Ping:	replied	(It might be better for the server to be less visible.)
External Query:	ignored	(This means the nameserver is more spoof resistant.)
DNSSEC Security:	supported	(This server supports improved security standards.)
Alphabetic Case:	all lower	(An improvement could be created by mixing case.)
Extra Anti-Spoofing:	unknown	(Unable to obtain server fingerprint.)

Analysis of 44 queries from nameserver opens in separate window at [ 23.171.240.157 ]
Anti-Spoofing Safety: Moderate (See Spoofability Mitigation Note below)

Query Source Port Analysis (worst case)
Max Entropy:	15.92	Excellent	Dir Bias:	20.93%	Moderate
Lost Entropy:	0	Excellent	Stuck Bits:	0	Excellent
 	 	
Query Transaction ID Analysis (worst case)
Max Entropy:	15.92	Excellent	Dir Bias:	2.33%	Excellent
Lost Entropy:	0	Excellent	Stuck Bits:	0	Excellent
DNS Nameserver Access Details
External Ping:	ignored	(Nice, as it's preferable for it to be less visible.)
External Query:	ignored	(This means the nameserver is more spoof resistant.)
DNSSEC Security:	supported	(This server supports improved security standards.)
Alphabetic Case:	all lower	(An improvement could be created by mixing case.)
Extra Anti-Spoofing:	unknown	(Unable to obtain server fingerprint.)

Kalau hasil dari github saya:
 https://wlmyaps.github.io/adblock/
78% block adblock.
jadi kalau dalam masalah adbock:
https://freedns.controld.com/no-ads-malware-typo
kalah melawan:
https://freedns.controld.com/p2

kalau dalam grc bagaimana?
kesayangan @gpt jangan buat tabel ringkasan dulu,
nanti setelah saya test controlD yang hagezi,
baru kita buat perbandingan 3 jenis DOH dari ControlD

Oke siap William 👍 aku pahami alurnya: sekarang kita baru tes `ControlD No-Ads-Malware-Typo` (DoH), hasil GRC keluar → nanti kalau sudah tes juga `ControlD Hagezi` baru kita bikin tabel ringkas 3 jenis.

Jadi sekarang aku bantu **jelaskan hasil GRC** untuk `no-ads-malware-typo` tanpa tabel dulu:

---

### 📊 Analisis GRC untuk `https://freedns.controld.com/no-ads-malware-typo`

**1. Jumlah nameserver yang terdeteksi**

* Ada **2 server aktif**:

  * `43.245.50.152 (xsp-h04.int.controld.com)`
  * `23.171.240.157`

**2. Kualitas anti-spoofing & keamanan**

* Server `43.245.50.152`:

  * Anti-Spoofing: **Excellent**
  * Source Port Analysis: Entropy 15.97 (Excellent), Bias rendah (0.9%) → sangat aman.
  * Transaction ID Analysis: Entropy 15.98 (Excellent), Bias 5.07% → masih Excellent.
  * DNSSEC: **supported**
  * Ping: replied (kurang ideal, lebih baik ignored).
  * External Query: ignored (bagus, lebih spoof resistant).

* Server `23.171.240.157`:

  * Anti-Spoofing: **Moderate** (ada catatan mitigasi)
  * Source Port Analysis: Entropy 15.92 (Excellent), tapi Bias 20.93% → bikin status Moderate.
  * Transaction ID Analysis: Excellent semua.
  * DNSSEC: **supported**
  * Ping: ignored (bagus)
  * External Query: ignored (bagus).

**3. Catatan teknis**

* Secara umum, `no-ads-malware-typo` punya **kombinasi server Excellent + Moderate**.
* Server utama (`43.245.50.152`) tampil lebih kuat dari sisi keamanan anti-spoofing.
* Server kedua (`23.171.240.157`) masih aman tapi ada bias lebih tinggi pada source port.
* Jadi dibandingkan dengan hasil `p2` kemarin (Ads & Tracking Configuration, block 98%), dari sisi GRC sebenarnya kualitas proteksi hampir sama **(Excellent)**, hanya beda sedikit pada satu server di sini yang Moderate.

---

📝 Kesimpulan sementara:

* Dari sisi GRC (keamanan DNS), **`p2` dan `no-ads-malware-typo` hampir sama kuat**, dengan keunggulan kecil di `p2` karena kedua servernya sama-sama Excellent.
* Dari sisi adblock (berdasarkan test di github kamu), jelas **`p2` menang jauh (98% vs 78%)**.

---

Mau aku tungguin kamu tes yang Hagezi dulu, baru kita bikin tabel perbandingan **P2 vs No-Ads-Malware-Typo vs Hagezi**?

