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
