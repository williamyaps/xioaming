skrip 1:
Bisa Bro. Paling gampang pakai *Cloudflare Workers* buat bikin proxy web. Gratis 100k request/hari, nggak perlu VPS.

Ini konsepnya: lu bikin worker di Cloudflare, semua request di-forward ke web tujuan, terus HTML/CSS/URL nya di-rewrite biar asset ke-load bener.

### 1. Setup 5 menit

1. Buka http://dash.cloudflare.com → Workers & Pages → Create application → Create Worker
2. Nama bebas, misal `web-proxy`
3. Paste kode di bawah, Deploy

### 2. Kode Worker - Universal Proxy
export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    
    // Ganti path jadi URL tujuan. Format: /https://example.com/path
    const targetUrl = url.pathname.slice(1) + url.search;
    
    if (!targetUrl.startsWith('http')) {
      return new Response('Format salah. Pakai: /https://situs.com', {status: 400});
    }

    // Forward request
    let response = await fetch(targetUrl, {
      method: request.method,
      headers: request.headers,
      body: request.body,
      redirect: 'follow'
    });

    // Rewrite HTML biar link CSS/JS/gambar nggak broken
    if (response.headers.get('content-type')?.includes('text/html')) {
      response = new HTMLRewriter()
        .on('a, link, script, img, iframe, form', {
          element(element) {
            const attrs = ['href', 'src', 'action', 'srcset'];
            for (let attr of attrs) {
              let val = element.getAttribute(attr);
              if (val && !val.startsWith('data:') && !val.startsWith('#')) {
                try {
                  let absUrl = new URL(val, targetUrl).href;
                  element.setAttribute(attr, '/' + absUrl);
                } catch {}
              }
            }
          }
        })
        .transform(response);
    }

    // Biar CSS/JS jalan
    let newHeaders = new Headers(response.headers);
    newHeaders.set('Access-Control-Allow-Origin', '*');
    newHeaders.delete('content-security-policy');
    newHeaders.delete('x-frame-options');

    return new Response(response.body, {
      status: response.status,
      headers: newHeaders
    });
  }
}
### 3. Cara pakai

Misal domain worker lu: `https://web-proxy.username.workers.dev`

Mau buka Google:
`https://web-proxy.username.workers.dev/https://google.com`

Mau buka GitHub:
`https://web-proxy.username.workers.dev/https://github.com`

### 4. Biar tampilan 99% bener

Masalah utama proxy gratis itu:
1. *Cookie/Login*: Nggak bisa login ke FB, Gmail, dll. Karena cookie domain beda.
2. *Websocket*: Chat live, notifikasi real-time biasanya mati.
3. *Anti-bot*: Cloudflare, Datadome bisa block.

Tapi buat baca artikel, buka GitHub, Docs, Wikipedia, Reddit old, tampilannya bakal bener. CSS/JS/image ke-rewrite otomatis.

### 5. Biar lebih mulus

Beli domain $1 di Cloudflare Registrar, pasang ke Worker. Jadi URL nya jadi `https://proxy.ludomain.com/https://situs.com`. Nggak keliatan aneh.

---

*Catatan penting Bro:*
1. Jangan pakai buat hal ilegal. Cloudflare bakal ban akun lu kalau disalahgunain.
2. Ini bukan VPN. IP tetep keliatan Cloudflare. Traffic nggak dienkripsi end-to-end ke situs tujuan.
3. Kalau mau buka situs yang berat JS, hasilnya tetep bisa ancur. Nggak ada proxy gratis yang 100% sempurna.

Mau gue bikinin versi yang auto redirect semua path biar lu tinggal ganti DNS CNAME aja?

---

Wkwk proxy nya nggak sakti kalau origin nya yang mati Bro 🤣

Error itu `Error 522: Connection timed out`. Artinya Cloudflare Workers lu berhasil nerima request, tapi dia nggak bisa nyambung ke server website tujuan dalam 15 detik.

### Penyebab paling sering:

*1. Website tujuan nge-block Cloudflare*
Banyak situs gede kayak Facebook, Instagram, TikTok, Google Services nge-block IP Cloudflare. 
Jadi pas Workers lu nyoba `fetch` ke mereka, langsung ditolak/timed out.

*2. Website nya emang lagi down*
Coba buka langsung `https://situs-tujuan.com` di browser lu. Kalau di sana juga lemot/error, berarti bukan salah proxy.

*3. Website butuh browser beneran*
Situs modern pakai Cloudflare Turnstile, Datadome, Akamai Bot Manager. Mereka deteksi kalau request nya dari `fetch` doang tanpa browser, langsung di-drop. Proxy JS murni nggak bisa nembus itu.

### Cara fix:

*Yang bisa:*
- Pakai proxy buat situs yang ringan: Wikipedia, GitHub, Docs, blog WordPress, Reddit old. Itu biasanya jalan.
- Tambahin `User-Agent` palsu biar keliatan kayak browser beneran. Edit kode Worker lu:
headers: {
  ...request.headers,
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36'
}
*Yang nggak bisa:*
- Jangan paksa buat buka Google, Facebook, WA Web. Mereka emang nge-block proxy umum. Itu alasan WA Web lu kumat redirect tadi.
- Kalau mau yang sakti buat semua situs, butuh browser beneran di server = harus pakai Browserless, ScrapeOps, atau sewa VPS. Nggak gratis.

---

Coba tes proxy lu buka `https://example.com` atau `https://news.ycombinator.com`. Kalau jalan, berarti proxy nya aman. Tinggal website tujuan yang galak.

Mau kirim link situs yang error 522 itu? Gue cek dulu apa emang di-block Cloudflare atau nggak.

---
skrip - 2:

Bener Bro, itu konsepnya mirip CroxyProxy. Dia spoof User-Agent + rewrite semua link biar asset ke-load lewat proxy.

Ini script lengkap Cloudflare Worker yang udah gue rapihin. Tinggal copy-paste → Deploy:
export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    const path = url.pathname.slice(1);

    // Halaman home buat test
    if (!path) {
      return new Response(`
        <h2>Proxy Aktif Bro ✅</h2>
        <p>Pakai format: <code>/https://situs.com</code></p>
        <p>Contoh: <code>/https://example.com</code></p>
      `, { headers: { 'content-type': 'text/html' } });
    }

    // Validasi URL
    if (!path.startsWith('http')) {
      return new Response('Format salah. Pakai: /https://situs.com', { status: 400 });
    }

    let targetUrl;
    try {
      targetUrl = new URL(path);
    } catch {
      return new Response('URL invalid', { status: 400 });
    }

    // Ambil request baru
    let newRequest = new Request(targetUrl, {
      method: request.method,
      headers: request.headers,
      body: request.body,
      redirect: 'follow'
    });

    // Spoof header biar keliatan kayak Chrome di Windows 10
    newRequest.headers.set('User-Agent', 
      'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    );
    newRequest.headers.set('Accept-Language', 'en-US,en;q=0.9,id;q=0.8');
    newRequest.headers.set('Referer', targetUrl.origin);
    newRequest.headers.delete('cf-ipcountry');
    newRequest.headers.delete('cf-ray');

    let response;
    try {
      response = await fetch(newRequest);
    } catch (e) {
      return new Response(`Error 522: Gagal connect ke ${targetUrl.host}. Situs nya nge-block atau down.`, { status: 522 });
    }

    // Rewrite HTML biar link nggak broken
    let contentType = response.headers.get('content-type') || '';
    if (contentType.includes('text/html')) {
      response = new HTMLRewriter()
        .on('a, link, script, img, iframe, form, source, video, audio', {
          element(element) {
            const attrs = ['href', 'src', 'action', 'srcset', 'poster'];
            for (let attr of attrs) {
              let val = element.getAttribute(attr);
              if (val && !val.startsWith('data:') && !val.startsWith('#') && !val.startsWith('javascript:')) {
                try {
                  let absUrl = new URL(val, targetUrl).href;
                  element.setAttribute(attr, '/' + absUrl);
                } catch {}
              }
            }
          }
        })
        .transform(response);
    }

    // Hapus header yang bikin broken
    let newHeaders = new Headers(response.headers);
    newHeaders.delete('content-security-policy');
    newHeaders.delete('content-security-policy-report-only');
    newHeaders.delete('x-frame-options');
    newHeaders.delete('strict-transport-security');
    newHeaders.set('Access-Control-Allow-Origin', '*');
    newHeaders.set('Access-Control-Allow-Headers', '*');

    return new Response(response.body, {
      status: response.status,
      statusText: response.statusText,
      headers: newHeaders
    });
  }
}
### Cara pakai:
1. Buka `dash.cloudflare.com` → Workers & Pages → Create → Create Worker
2. Paste kode di atas → Deploy
3. Buka `https://nama-worker.username.workers.dev/https://example.com`

### Yang ditingkatin dari versi sebelumnya:
1. *Spoof User-Agent Chrome 120* - biar nggak langsung ke-detect bot
2. *Rewrite lebih banyak tag* - `video`, `audio`, `source` biar video/gambar jalan
3. *Hapus CSP & X-Frame-Options* - biar nggak di-block iframe
4. *Error handling* - kalau timeout kasih pesan jelas Error 522

### Batasan tetep ada Bro:
1. *Login/Facebook/YouTube/Google* - 99% gagal. Mereka pakai bot protection yang deteksi JS execution. Proxy JS nggak bisa nembus itu.
2. *WebSocket/Chat live* - nggak jalan
3. *Situs berat JS* - kadang layout ancur

Tapi buat baca artikel, GitHub, Wikipedia, Docs, Reddit old, blog, 95% bener.

Kalau mau yang bisa buka YouTube/Facebook beneran, itu namanya "browser proxy" dan butuh VPS + Browserless. Nggak gratis.

Coba dulu pakai situs ringan. Kalau ada situs spesifik yang mau lu tes, kirim linknya, gue cek kenapa gagal.

---
skrip 3:
Oke paham Bro 😅  
Itu namanya "link relatif" nggak ke-rewrite bener. Jadinya pas lu klik ke halaman ke-3, URL nya jadi `https://proxy.lu.workers.dev/medan` bukan `https://proxy.lu.workers.dev/https://situs.com/medan`.

Makanya cuma mentok 2 level.

### Penyebabnya
Di halaman berita, link nya sering gini:
<a href="/medan">Medan</a>
<a href="berita/medan">Medan</a>
Script lama gue nggak nangkep kalau halaman udah nested 2x. Dia nganggap base URL nya salah.

### Fix: Update script nya pakai base URL yang bener

Ganti bagian `on('a, link, script...')` jadi gini:
export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    const path = url.pathname.slice(1);

    if (!path) {
      return new Response(`
        <h2>Proxy Aktif Bro ✅</h2>
        <p>Pakai format: <code>/https://situs.com</code></p>
      `, { headers: { 'content-type': 'text/html' } });
    }

    if (!path.startsWith('http')) {
      return new Response('Format salah. Pakai: /https://situs.com', { status: 400 });
    }

    let targetUrl;
    try {
      targetUrl = new URL(path);
    } catch {
      return new Response('URL invalid', { status: 400 });
    }

    let newRequest = new Request(targetUrl, {
      method: request.method,
      headers: request.headers,
      body: request.body,
      redirect: 'follow'
    });

    newRequest.headers.set('User-Agent', 
      'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    );
    newRequest.headers.set('Accept-Language', 'en-US,en;q=0.9,id;q=0.8');

    let response;
    try {
      response = await fetch(newRequest);
    } catch (e) {
      return new Response(`Error 522: Gagal connect ke ${targetUrl.host}`, { status: 522 });
    }

    let contentType = response.headers.get('content-type') || '';
    if (contentType.includes('text/html')) {
      
      // Ambil base URL buat resolve relative link
      let baseUrl = targetUrl.href;
      
      response = new HTMLRewriter()
        .on('base', {
          element(element) {
            let href = element.getAttribute('href');
            if (href) {
              try {
                baseUrl = new URL(href, baseUrl).href;
              } catch {}
            }
          }
        })
        .on('a, link, script, img, iframe, form, source, video, audio', {
          element(element) {
            const attrs = ['href', 'src', 'action', 'srcset', 'poster'];
            for (let attr of attrs) {
              let val = element.getAttribute(attr);
              if (val && !val.startsWith('data:') && !val.startsWith('#') && !val.startsWith('javascript:') && !val.startsWith('mailto:')) {
                try {
                  // Resolve pakai baseUrl yang udah diupdate
                  let absUrl = new URL(val, baseUrl).href;
                  element.setAttribute(attr, '/' + absUrl);
                } catch {}
              }
            }
          }
        })
        .transform(response);
    }

    let newHeaders = new Headers(response.headers);
    newHeaders.delete('content-security-policy');
    newHeaders.delete('content-security-policy-report-only');
    newHeaders.delete('x-frame-options');
    newHeaders.delete('strict-transport-security');
    newHeaders.set('Access-Control-Allow-Origin', '*');

    return new Response(response.body, {
      status: response.status,
      statusText: response.statusText,
      headers: newHeaders
    });
  }
}
### Yang gue ubah:
1. *Tambah handler `<base>`* - biar link relatif resolve nya bener kalau situs pakai tag `<base href="/...">`
2. *Pakai `baseUrl` dinamis* - jadi setiap halaman, base nya ikut URL halaman itu. Makanya klik ke level 3, 4, 5 tetep jalan.
3. *Block `mailto:` dan `javascript:`* - biar nggak error

### Cara test
Deploy ulang script ini. Terus coba buka berita utama → Sumatera Utara → Medan. 
Sekarang harusnya URL nya jadi:
`https://proxy.lu.workers.dev/https://situs.com/medan`

Kalau masih mentok, kirim link situs berita nya ke gue. Gue cek HTML nya langsung, biasanya ada JS yang ganti link pakai `window.location` dan itu nggak bisa di-rewrite pakai Worker doang.

---
skrip 4:

Wah, ini bukan ujian sekolah biasa, ini ujian kodingan Cloudflare Workers! 💻
Script proxy yang kamu buat ini sebenarnya sudah sangat bagus untuk skenario dasar (seperti me-rewrite link HTML dan playlist M3U8 HLS). Namun, kodingan ini masih punya 4 kelemahan fatal yang bisa bikin websitenya broken (rusak), kena blokir, atau boros resource saat digunakan di dunia nyata.
Berikut adalah hasil koreksi dan analisis mendalam untuk "ujian" kamu:
## 1. Masalah Fatal pada request.body (Sering Bikin Error)
Pada baris ini:

let newRequest = new Request(targetUrl, { body: request.body, ... });

Kamu langsung meneruskan request.body ke request yang baru. Di Cloudflare Workers, jika method-nya adalah GET atau HEAD, menyertakan properti body (walaupun isinya null atau undefined) akan memicu Runtime Error. Kamu harus memisahkan atau mengecek method-nya terlebih dahulu.
## 2. Isu CSS Background Image & AJAX (fetch/XHR)

* CSS: Banyak website menyimpan aset gambar di dalam file CSS eksternal menggunakan url(...). HTMLRewriter kamu tidak bisa membaca isi file CSS, sehingga gambar latar belakang website target akan broken.
* JavaScript Fetch: Jika website target menggunakan AJAX untuk mengambil data (misal fetch('/api/v1/data')), skrip JS asli di halaman tersebut akan menembak ke domain Workers kamu langsung (/api/v1/data) dan menghasilkan error 404, karena link di dalam file JS tidak ikut ter-rewrite oleh HTMLRewriter.

## 3. Masalah Duplikasi Prefix /https://... pada Tag <a>
Pada HTMLRewriter, kamu mengubah href menjadi '/' + absUrl.
Jika user mengklik link yang sudah di-rewrite, halaman baru akan dimuat. Saat halaman baru tersebut diproses lagi oleh Workers, baseUrl akan berubah menjadi https://workersmu.com.
Jika ada link relatif lain di sana, fungsi new URL(val, baseUrl) bisa menghasilkan URL double prefix yang rusak seperti https://workersmu.com....
## 4. response.body Terkunci setelah HTMLRewriter
Pada bagian pengecekan HLS (.m3u8), kamu menggunakan kondisi if (contentType.includes(...)). Namun, jika kondisi itu salah, di akhir kode kamu memanggil:

return new Response(response.body, { ... });

Jika contentType ternyata adalah HTML, response tersebut sudah diubah oleh HTMLRewriter sebelumnya. Di Cloudflare Workers, body dari response yang sudah dimasukkan ke HTMLRewriter.transform() tidak bisa dibaca ulang atau diteruskan begitu saja secara mentah karena stream-nya sudah terganggu.
------------------------------
## 🛠️ Solusi Kodingan yang Lebih Sempurna
Berikut adalah versi perbaikan yang mengatasi masalah error GET body, penyempurnaan routing, dan efisiensi stream:

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    // Menggunakan regex agar ekstraksi URL target lebih aman dan bersih
    const path = url.pathname.slice(1) + url.search; 

    if (!path) {
      return new Response(`
        <h2>Proxy Aktif Bro ✅</h2>
        <p>Pakai format: <code>/https://situs.com</code></p>
      `, { headers: { 'content-type': 'text/html' } });
    }

    if (!path.startsWith('http://') && !path.startsWith('https://')) {
      return new Response('Format salah. Pakai: /https://situs.com', { status: 400 });
    }

    let targetUrl;
    try {
      targetUrl = new URL(path);
    } catch {
      return new Response('URL invalid', { status: 400 });
    }

    // Solusi Masalah 1: Ambil body hanya jika method BUKAN GET/HEAD
    let requestInit = {
      method: request.method,
      headers: new Headers(request.headers),
      redirect: 'follow'
    };
    if (request.method !== 'GET' && request.method !== 'HEAD') {
      requestInit.body = request.body;
    }

    let newRequest = new Request(targetUrl, requestInit);

    // Setup Headers Keamanan & Penyamaran
    newRequest.headers.set('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36');
    newRequest.headers.set('Referer', targetUrl.origin);
    newRequest.headers.set('Origin', targetUrl.origin);
    newRequest.headers.delete('cf-ipcountry');
    newRequest.headers.delete('cf-ray');
    newRequest.headers.delete('x-forwarded-for');

    let response;
    try {
      response = await fetch(newRequest);
    } catch (e) {
      return new Response(`Error 522: Gagal connect ke ${targetUrl.host}`, { status: 522 });
    }

    let contentType = response.headers.get('content-type') || '';
    let newHeaders = new Headers(response.headers);

    // Bypass CORS & Security Policy
    newHeaders.delete('content-security-policy');
    newHeaders.delete('content-security-policy-report-only');
    newHeaders.delete('x-frame-options');
    newHeaders.delete('strict-transport-security');
    newHeaders.set('Access-Control-Allow-Origin', '*');

    // Solusi Masalah 4: Saring penanganan HTML dan M3U8 secara terpisah dan bersih
    if (contentType.includes('text/html')) {
      // Netralkan base URL agar rewrite asset relatif tidak double prefix
      let baseUrl = targetUrl.href; 
      
      let transformedResponse = new HTMLRewriter()
        .on('a, link, script, img, iframe, form, source, video, audio', {
          element(element) {
            const attrs = ['href', 'src', 'action', 'srcset', 'poster'];
            for (let attr of attrs) {
              let val = element.getAttribute(attr);
              if (val && !val.startsWith('data:') && !val.startsWith('#') && !val.startsWith('javascript:')) {
                try {
                  // Pastikan link tidak sengaja di-rewrite double jika sudah absolute ke proxy
                  if (!val.startsWith('/http')) {
                    let absUrl = new URL(val, baseUrl).href;
                    element.setAttribute(attr, '/' + absUrl);
                  }
                } catch {}
              }
            }
          }
        })
        .transform(response);

      return new Response(transformedResponse.body, { status: response.status, headers: newHeaders });
    }

    if (contentType.includes('application/vnd.apple.mpegurl') || targetUrl.pathname.endsWith('.m3u8')) {
      let body = await response.text();
      body = body.split('\n').map(line => {
        line = line.trim();
        if (line && !line.startsWith('#')) {
          try {
            let absUrl = new URL(line, targetUrl).href;
            return '/' + absUrl;
          } catch { return line; }
        }
        return line;
      }).join('\n');
      
      return new Response(body, { status: response.status, headers: newHeaders });
    }

    // Untuk file statis lainnya (Gambar, JS, CSS mentah)
    return new Response(response.body, { status: response.status, headers: newHeaders });
  }
}

Bagaimana hasil koreksinya? Jika kamu ingin mengembangkan script ini lebih jauh, beri tahu saya bagian apa yang ingin kamu tambahkan, seperti fitur cookie, handling CORS untuk AJAX, atau optimasi streaming video!

---

Script yang dioptimalkan untuk Cloudflare Workers ini mengatasi error 522 dengan teknik anti-bot dan header yang lebih ketat. Kode yang diberikan sudah mencakup penyamaran user-agent dan penghapusan header cf-. Berikut adalah full script yang bisa digunakan.

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    // Mengambil pathname dan search query agar parameter URL target tidak hilang
    const path = url.pathname.slice(1) + url.search; 

    // 1. Tampilan Halaman Utama Proxy
    if (!path) {
      return new Response(`
        <!DOCTYPE html>
        <html>
        <head>
          <title>Proxy Aktif Bro ✅</title>
          <style>
            body { font-family: sans-serif; text-align: center; padding: 50px; background: #121212; color: #fff; }
            code { background: #333; padding: 4px 8px; border-radius: 4px; color: #ff79c6; }
          </style>
        </head>
        <body>
          <h2>Proxy Aktif Bro ✅</h2>
          <p>Pakai format: <code>/${url.origin}/https://situs-target.com</code></p>
        </body>
        </html>
      `, { headers: { 'content-type': 'text/html; charset=utf-8' } });
    }

    // 2. Validasi Format URL Target
    if (!path.startsWith('http://') && !path.startsWith('https://')) {
      return new Response('Format salah. Pastikan menggunakan /http:// atau /https://', { status: 400 });
    }

    let targetUrl;
    try {
      targetUrl = new URL(path);
    } catch {
      return new Response('URL tidak valid', { status: 400 });
    }

    // 3. Konfigurasi Request Baru (Mencegah Error Body pada GET/HEAD)
    let requestInit = {
      method: request.method,
      headers: new Headers(request.headers),
      redirect: 'follow'
    };
    
    if (request.method !== 'GET' && request.method !== 'HEAD') {
      requestInit.body = request.body;
    }

    let newRequest = new Request(targetUrl, requestInit);

    // 4. Solusi Error 522: Penyamaran Header Browser Manusia (Anti-Bot Bypass)
    newRequest.headers.set('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36');
    newRequest.headers.set('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8');
    newRequest.headers.set('Accept-Language', 'en-US,en;q=0.9,id;q=0.8');
    newRequest.headers.set('Referer', targetUrl.origin);
    newRequest.headers.set('Origin', targetUrl.origin);
    
    // Memaksa server mengirim data tanpa enkripsi aneh yang bisa bikin hang/timeout
    newRequest.headers.set('Accept-Encoding', 'identity'); 

    // Kebijakan navigasi standar browser
    newRequest.headers.set('Sec-Fetch-Dest', 'document');
    newRequest.headers.set('Sec-Fetch-Mode', 'navigate');
    newRequest.headers.set('Sec-Fetch-Site', 'none');
    newRequest.headers.set('Sec-Fetch-User', '?1');
    newRequest.headers.set('Upgrade-Insecure-Requests', '1');

    // Hapus total jejak Cloudflare Workers agar tidak diblokir oleh sesama Cloudflare/Firewall
    newRequest.headers.delete('cf-connecting-ip');
    newRequest.headers.delete('cf-ipcountry');
    newRequest.headers.delete('cf-ray');
    newRequest.headers.delete('cf-visitor');
    newRequest.headers.delete('x-forwarded-for');
    newRequest.headers.delete('x-forwarded-proto');
    newRequest.headers.delete('x-real-ip');

    // 5. Eksekusi Fetch ke Website Target
    let response;
    try {
      response = await fetch(newRequest);
    } catch (e) {
      return new Response(`Error 522: Gagal terhubung ke ${targetUrl.host}. Server target down atau memblokir IP proxy ini.`, { status: 522 });
    }

    // 6. Pengaturan Header Response (Bypass CORS & Security Policy)
    let contentType = response.headers.get('content-type') || '';
    let newHeaders = new Headers(response.headers);

    newHeaders.delete('content-security-policy');
    newHeaders.delete('content-security-policy-report-only');
    newHeaders.delete('x-frame-options');
    newHeaders.delete('strict-transport-security');
    
    // Inject CORS agar asset bisa di-load dari domain mana saja
    newHeaders.set('Access-Control-Allow-Origin', '*');
    newHeaders.set('Access-Control-Allow-Headers', '*');
    newHeaders.set('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, PUT, DELETE');

    // 7. Handler HTML: Rewrite URL Internal/Relatif
    if (contentType.includes('text/html')) {
      let baseUrl = targetUrl.href;
      
      let transformedResponse = new HTMLRewriter()
        .on('a, link, script, img, iframe, form, source, video, audio', {
          element(element) {
            const attrs = ['href', 'src', 'action', 'srcset', 'poster'];
            for (let attr of attrs) {
              let val = element.getAttribute(attr);
              if (val && !val.startsWith('data:') && !val.startsWith('#') && !val.startsWith('javascript:')) {
                try {
                  // Mencegah double prefix jika URL sudah di-rewrite sebelumnya
                  if (!val.startsWith('/http://') && !val.startsWith('/https://')) {
                    let absUrl = new URL(val, baseUrl).href;
                    element.setAttribute(attr, '/' + absUrl);
                  }
                } catch {}
              }
            }
          }
        })
        .transform(response);

      return new Response(transformedResponse.body, { status: response.status, headers: newHeaders });
    }

    // 8. Handler Streaming Video (HLS .m3u8 Playlist)
    if (contentType.includes('application/vnd.apple.mpegurl') || targetUrl.pathname.endsWith('.m3u8')) {
      let body = await response.text();
      body = body.split('\n').map(line => {
        line = line.trim();
        if (line && !line.startsWith('#')) {
          try {
            let absUrl = new URL(line, targetUrl).href;
            return '/' + absUrl;
          } catch { return line; }
        }
        return line;
      }).join('\n');
      
      return new Response(body, { status: response.status, headers: newHeaders });
    }

    // 9. Handler Asset Statis Lainnya (Gambar, JS, CSS, Font, dll)
    return new Response(response.body, {
      status: response.status,
      statusText: response.statusText,
      headers: newHeaders
    });
  }
};


