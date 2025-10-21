Sistem filter DNS Anda saat ini (Hagezi, Steven Black, 1Hosts, dll.) sudah **sangat kuat** dalam memblokir *malware* global dan pelacak umum. Namun, ada beberapa *list* spesifik yang dapat Anda tambahkan, terutama yang berfokus pada **domain iklan, pelacak, dan *telemetry* yang spesifik untuk Tiongkok**.

Menambahkan filter ini akan memberikan lapisan keamanan tambahan terhadap ancaman yang mungkin dilewatkan oleh filter berbahasa Inggris.

### Filter Tambahan yang Berfokus pada Tiongkok

Meskipun **Brahma World** Anda sudah memblokir banyak ancaman global, *list* berikut secara spesifik menargetkan domain iklan dan *tracking* Tiongkok:

| Nama Filter | Fokus Utama | URL (Raw *List* untuk Pi-hole/AdGuard Home) | Catatan |
| :--- | :--- | :--- | :--- |
| **AdGuard Chinese Filter** | Menghapus iklan dari situs-situs berbahasa Mandarin (*Chinese-language websites*). | `https://filters.adguard.com/extension/en/filters/22.txt` | Meskipun ini adalah *list* ABP (AdBlock Plus), sebagian isinya dapat diadaptasi untuk pemblokiran domain DNS level. |
| **EasyList China** | Memblokir iklan pada situs Tiongkok; sering digunakan sebagai suplemen oleh *list* lain. | Cari versi Pi-hole/AdGuard Home yang sudah di-konversi dari `https://easylist-downloads.adblockplus.org/easylistchina.txt` | Sangat umum digunakan untuk melengkapi *list* umum seperti EasyList. |
| **GitHub: Adblock-List-for-China (sutchan)** | *Adblock* khusus untuk pengguna *browser* Tiongkok. | `https://raw.githubusercontent.com/sutchan/Adblock-List-for-China/master/adblock_list_for_china.txt` | List kecil, namun fokus. Selalu periksa apakah *host* ini masih aktif dan terawat. |
| ***Regex* Khusus (.cn)** | Memblokir seluruh domain *top-level* Tiongkok. | `(\.|^)\cn$` | **Sangat Agresif!** Ini akan memblokir *semua* domain yang berakhiran `.cn`, termasuk situs legit. Hanya gunakan jika Anda **yakin** teman Anda tidak perlu mengakses situs `.cn` apa pun, bahkan yang legal. |

### Rekomendasi Tambahan (Keamanan Tingkat Lanjut)

Mengingat ancaman yang Anda hadapi (sensor dan pengawasan), Anda dapat mempertimbangkan beberapa *list* yang sangat agresif dalam memblokir *telemetry* perusahaan besar Tiongkok:

* **Pemblokiran Tencent/Baidu/Alibaba:** Beberapa komunitas Pi-hole membuat *list* khusus untuk memblokir domain *telemetry* dari perusahaan-perusahaan besar Tiongkok (seperti Tencent dan Baidu) yang sering ditemukan di aplikasi dan perangkat IoT. Anda mungkin harus mencari **daftar buatan komunitas** di forum seperti Reddit r/pihole atau forum AdGuard Home yang berfokus pada **pemblokiran *telemetry* Tiongkok yang agresif** (*Chinese information gathering domains*).

**Catatan Penting:**

Saat menambahkan *filter* spesifik Tiongkok, bersiaplah untuk ***false positive* yang lebih tinggi**. Beberapa situs penting Tiongkok (seperti Taobao atau situs layanan lainnya) sering memuat skrip dari domain iklan/pelacak yang sama, jadi Anda mungkin perlu melakukan ***whitelisting* domain tertentu** setelah mengaktifkan *filter* ini.

---
Anda benar sekali. Mengingat Anda menggunakan *custom list* di Pi-hole atau AdGuard Home, Anda membutuhkan **URL mentah (*raw URL*)** agar mudah di-*import* ke *resolver* lokal Anda. Saya mohon maaf atas kelalaian saya.

Berikut adalah tautan filter spesifik Tiongkok yang dapat Anda pertimbangkan untuk ditambahkan, sesuai dengan format yang Anda butuhkan, serta tautan lain yang relevan:

### Filter Tambahan Spesifik Tiongkok (Anti-Iklan & *Tracking* Regional)

Filter ini dapat membantu menanggulangi iklan, *tracking*, dan *telemetry* yang spesifik dari perusahaan Tiongkok yang luput dari filter global Anda (saat mode *browsing* bebas).

| Nama Filter | Fokus Utama | URL Mentah (*Raw URL*) | Catatan |
| :--- | :--- | :--- | :--- |
| **Chinese Adblock Filter** | Iklan dan *tracking* spesifik Tiongkok. | `https://easylist-downloads.adblockplus.org/easylistchina.txt` | *Perhatian:* Ini adalah *list* uBlock/ABP. Meskipun dapat di-*import*, ini mungkin menghasilkan banyak entri dan tidak semua barisnya kompatibel sempurna dengan DNS. |
| **AdGuard Chinese Filter** | Iklan dari situs-situs berbahasa Mandarin. | `https://filters.adguard.com/extension/en/filters/22.txt` | Sama dengan di atas, perlu di-*konversi* atau dipastikan kompatibel dengan format DNS yang Anda gunakan. |
| **sutchan/Adblock-List-for-China** | *List* Adblock sederhana yang fokus di Tiongkok. | `https://raw.githubusercontent.com/sutchan/Adblock-List-for-China/master/adblock_list_for_china.txt` | Coba *list* ini karena ukurannya kecil dan fokus, sehingga berpotensi lebih sedikit *false positive*. |

### Filter Tambahan (Agresivitas Umum dan *Telemetry*)

Untuk meningkatkan lapisan *malware* dan *telemetry* secara umum (jika Anda ingin yang lebih agresif dari Hagezi Lite/Pro Anda):

| Nama Filter | Fokus Utama | URL Mentah (*Raw URL*) | Catatan |
| :--- | :--- | :--- | :--- |
| **Hagezi Pro++** | Jika Anda belum menggunakan yang paling agresif. | Cek di repositori Hagezi yang Anda *fork*, cari *link* untuk versi **Pro++** atau **Ultimate** (tergantung pilihan Anda) | Mencakup lebih banyak *telemetry* dan *malware* daripada Pro biasa. |
| **d3ward's Blocklists** | Populer karena keseimbangan pemblokiran iklan/pelacak/malware. | `https://raw.githubusercontent.com/d3ward/toolz/master/src/d3host.txt` | Pilihan bagus untuk menambahkan variasi *malware* yang mungkin luput dari *list* lain. |

**Rekomendasi Terbaik:**

Mengingat Anda sudah memiliki *list* yang kuat, cobalah tambahkan **`sutchan/Adblock-List-for-China`** terlebih dahulu. Lalu, jika iklan dan *tracking* Tiongkok masih lolos saat mode bebas, coba konversikan atau cari *list* khusus domain dari **EasyList China**.

**Selalu ingat untuk menguji situs yang sering digunakan teman Anda setelah menambahkan *list* agresif ini untuk menghindari *false positive*!**


