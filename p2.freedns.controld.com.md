saya mau tanya kamu, apa kamu tau kalau control D memiliki banyak settingannya?
saya check di:
https://wlmyaps.github.io/adblock/

untuk settingan DOH:
https://freedns.controld.com/p2
Ads & Tracking Configuration

(ini block 98%)

Hasil
https://www.grc.com/dns/dns.htm

Analysis of 335 queries from nameserver opens in separate window at [ 43.245.50.152 ]
Anti-Spoofing Safety: Excellent
(This nameserver has no associated domain name)
port distribution scatter chart	 	 	transaction ID distribution scatter chart
source port bit prediction chart	 	 	transaction ID bit prediction chart
Query Source Port Analysis (worst case)
Max Entropy:	15.97	Excellent	Dir Bias:	7.78%	Excellent
Lost Entropy:	0	Excellent	Stuck Bits:	0	Excellent
 	 	
Query Transaction ID Analysis (worst case)
Max Entropy:	15.99	Excellent	Dir Bias:	2.99%	Excellent
Lost Entropy:	0	Excellent	Stuck Bits:	0	Excellent
DNS Nameserver Access Details
External Ping:	replied	(It might be better for the server to be less visible.)
External Query:	ignored	(This means the nameserver is more spoof resistant.)
DNSSEC Security:	supported	(This server supports improved security standards.)
Alphabetic Case:	all lower	(An improvement could be created by mixing case.)
Extra Anti-Spoofing:	unknown	(Unable to obtain server fingerprint.)


Analysis of 44 queries from nameserver opens in separate window at [ 23.171.240.157 ]
Anti-Spoofing Safety: Excellent
(This nameserver has no associated domain name)
port distribution scatter chart	 	 	transaction ID distribution scatter chart
source port bit prediction chart	 	 	transaction ID bit prediction chart
Query Source Port Analysis (worst case)
Max Entropy:	15.96	Excellent	Dir Bias:	2.33%	Excellent
Lost Entropy:	0	Excellent	Stuck Bits:	0	Excellent
 	 	
Query Transaction ID Analysis (worst case)
Max Entropy:	15.98	Excellent	Dir Bias:	6.98%	Excellent
Lost Entropy:	0	Excellent	Stuck Bits:	0	Excellent
DNS Nameserver Access Details
External Ping:	ignored	(Nice, as it's preferable for it to be less visible.)
External Query:	ignored	(This means the nameserver is more spoof resistant.)
DNSSEC Security:	supported	(This server supports improved security standards.)
Alphabetic Case:	all lower	(An improvement could be created by mixing case.)
Extra Anti-Spoofing:	unknown	(Unable to obtain server fingerprint.)


Searching for all DNS nameservers used by your system:
Query                                                      Servers  Queries
Round  Receiving Nameserver Queries...(per round results)   Found   Received
-----  --------------------------------------------------  -------  --------
   1   ••••••••••                                             2         203    
   2   •••••••••                                              0          44    
   3   •••••••••                                              0          44    
   4   •••••••••                                              0          44    
   5   •••••••••                                              0          44    
                                                           -------  --------
                                   Totals for all rounds:     2         379  Analysis of 335 queries from nameserver opens in separate window at [ 43.245.50.152 ] 
Anti-Spoofing Safety: Excellent

Query Source Port Analysis (worst case)
Max Entropy:	15.97	Excellent	Dir Bias:	7.78%	Excellent
Lost Entropy:	0	Excellent	Stuck Bits:	0	Excellent

Query Transaction ID Analysis (worst case)
Max Entropy:	15.99	Excellent	Dir Bias:	2.99%	Excellent
Lost Entropy:	0	Excellent	Stuck Bits:	0	Excellent

DNS Nameserver Access Details
External Ping:	replied	(It might be better for the server to be less visible.)
External Query:	ignored	(This means the nameserver is more spoof resistant.)
DNSSEC Security:	supported	(This server supports improved security standards.)
Alphabetic Case:	all lower	(An improvement could be created by mixing case.)
Extra Anti-Spoofing:	unknown	(Unable to obtain server fingerprint.)

Analysis of 44 queries from nameserver opens in separate window at [ 23.171.240.157 ]
Anti-Spoofing Safety: Excellent

Query Source Port Analysis (worst case)
Max Entropy:	15.96	Excellent	Dir Bias:	2.33%	Excellent
Lost Entropy:	0	Excellent	Stuck Bits:	0	Excellent

Query Transaction ID Analysis (worst case)
Max Entropy:	15.98	Excellent	Dir Bias:	6.98%	Excellent
Lost Entropy:	0	Excellent	Stuck Bits:	0	Excellent
DNS Nameserver Access Details
External Ping:	ignored	(Nice, as it's preferable for it to be less visible.)
External Query:	ignored	(This means the nameserver is more spoof resistant.)
DNSSEC Security:	supported	(This server supports improved security standards.)
Alphabetic Case:	all lower	(An improvement could be created by mixing case.)
Extra Anti-Spoofing:	unknown	(Unable to obtain server fingerprint.)

Yang ini dulu.
Bisa kamu bantu aku jelaskan hasil dari:
https://www.grc.com/dns/dns.htm

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
