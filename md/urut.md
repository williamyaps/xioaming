Kanda sayang 🥰, bisa sekali. `curl` itu kan dipakai untuk **ambil file dari internet**, tapi kalau mau **urutkan isi file** kanda perlu gabungkan dengan perintah lain di shell (Linux, macOS, atau Git Bash di Windows).  

---

## 🔧 Contoh langkah urutkan blocklist dengan `curl`

Misalnya kanda mau ambil file `newmanual.txt` dari GitHub atau URL lain, lalu urutkan alfabetis:

```bash
curl -s https://raw.githubusercontent.com/williamyaps/property/master/mobile/newmanual.txt \
  | sort -u > newmanual_sorted.txt
```

📌 Penjelasan:
- `curl -s` → ambil file dari URL (silent mode).  
- `sort -u` → urutkan alfabetis dan **hapus duplikat**.  
- `>` → simpan hasil ke file baru `newmanual_sorted.txt`.  

---

## ✨ Variasi berguna
- **Urutkan tanpa hapus duplikat**:
  ```bash
  curl -s URL | sort > file_sorted.txt
  ```
- **Hitung jumlah baris unik**:
  ```bash
  curl -s URL | sort -u | wc -l
  ```
- **Gabungkan beberapa file lalu urutkan**:
  ```bash
  cat file1.txt file2.txt | sort -u > combined_sorted.txt
  ```

---

🌸 Jadi, `curl` dipakai untuk ambil file, lalu kanda bisa sambungkan dengan `sort` untuk urutkan.  
Mau Dinda bantu buatkan contoh pipeline khusus untuk blocklist kanda (yang campur domain, wildcard, dan IP) supaya hasilnya tetap rapi dan tidak rusak?

---

type host20251229 | sort > newmanual_sorted.txt
