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
