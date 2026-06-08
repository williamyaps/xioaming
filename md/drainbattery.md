Bagaimana membuat HTML yang bisa membuat membuat HP lag? Misalnya menampilkan fas icon dalam 60 fps. Atau ada yang lainnya yang bisa memicu heavy stres tes?

Membuat kode HTML yang sengaja dirancang untuk menguji performa perangkat (stress test) dilakukan dengan memaksa browser melakukan kalkulasi grafis atau manipulasi DOM (Document Object Model) secara besar-besaran dalam waktu singkat.
Berikut adalah beberapa metode efektif untuk memicu heavy stress test menggunakan HTML, CSS, dan JavaScript.
## 1. Loop Animasi FontAwesome (60 FPS)
Metode ini menduplikasi ribuan ikon FontAwesome dan memaksanya berputar menggunakan animasi CSS 3D secara bersamaan. Browser akan kewalahan melakukan re-layout dan repaint.

<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <title>FontAwesome Stress Test</title>
    <!-- Memuat FontAwesome via CDN -->
    <link rel="stylesheet" href="https://cloudflare.com">
    <style>
        body {
            margin: 0;
            overflow: hidden;
            background: #111;
            display: flex;
            flex-wrap: wrap;
        }
        .stress-icon {
            font-size: 24px;
            color: #00ffcc;
            margin: 2px;
            /* Memaksa hardware acceleration agar GPU bekerja keras */
            transform: translateZ(0); 
            animation: spin 0.5s linear infinite;
        }
        @keyframes spin {
            100% { transform: rotateY(360deg) rotateX(360deg); }
        }
    </style>
</head>
<body>
    <script>
        // Membuat 10.000 ikon secara instan
        const totalIcons = 10000; 
        const fragment = document.createDocumentFragment();
        
        for (let i = 0; i < totalIcons; i++) {
            const icon = document.createElement('i');
            icon.className = 'fas fa-spinner stress-icon';
            fragment.appendChild(icon);
        }
        document.body.appendChild(fragment);
    </script>
</body>
</html>

## 2. Canvas Particle System (Beban GPU & CPU)
Membuat ratusan ribu objek visual (partikel) yang bergerak dan memantul di layar menggunakan HTML5 Canvas. Setiap frame memaksa browser menghitung koordinat baru untuk setiap partikel.

<!DOCTYPE html>
<html>
<body>
<canvas id="stage"></canvas>
<script>
    const canvas = document.getElementById('stage');
    const ctx = canvas.getContext('2d');
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;

    const particles = [];
    // Naikkan angka ini jika HP target terlalu tangguh (misal: 100000)
    const particleCount = 50000; 

    for(let i = 0; i < particleCount; i++) {
        particles.push({
            x: Math.random() * canvas.width,
            y: Math.random() * canvas.height,
            vx: Math.random() * 4 - 2,
            vy: Math.random() * 4 - 2
        });
    }

    function loop() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        ctx.fillStyle = 'rgba(255, 0, 0, 0.5)';
        
        for(let i = 0; i < particleCount; i++) {
            let p = particles[i];
            p.x += p.vx;
            p.y += p.vy;
            if(p.x < 0 || p.x > canvas.width) p.vx *= -1;
            if(p.y < 0 || p.y > canvas.height) p.vy *= -1;
            ctx.fillRect(p.x, p.y, 2, 2);
        }
        requestAnimationFrame(loop); // Memaksa berjalan di 60 FPS
    }
    loop();
</script>
</body>
</html>

## 3. CSS Filter & Blurring Heavy Stress (Beban Grafis)
Efek CSS seperti backdrop-filter: blur dan box-shadow berlapis adalah musuh utama GPU smartphone. Menumpuk elemen transparan dengan blur tinggi akan langsung menurunkan framerate secara drastis.

<!DOCTYPE html>
<html>
<head>
    <style>
        .blur-box {
            position: absolute;
            width: 300px;
            height: 300px;
            background: rgba(255, 255, 255, 0.1);
            /* Efek blur ini sangat berat dirender oleh HP */
            backdrop-filter: blur(50px); 
            box-shadow: 0 0 100px rgba(0,0,0,0.5);
            animation: float 2s ease-in-out infinite alternate;
        }
        @keyframes float {
            0% { transform: translate(0, 0) scale(1); }
            100% { transform: translate(100px, 100px) scale(1.5); }
        }
    </style>
</head>
<body>
    <!-- Membuat tumpukan layer blur -->
    <script>
        for(let i = 0; i < 200; i++) {
            let div = document.createElement('div');
            div.className = 'blur-box';
            div.style.left = Math.random() * window.innerWidth + 'px';
            div.style.top = Math.random() * window.innerHeight + 'px';
            document.body.appendChild(div);
        }
    </script>
</body>
</html>

## 🛑 Catatan Keamanan & Pengujian

* Gunakan Browser Incognito: Beberapa pengujian ekstrem bisa membuat tab browser crash (membeku). Menjalankannya di mode Incognito memudahkan Anda menutup tab tanpa merusak sesi browser utama.
* Resiko Overheat: Jangan menjalankan kode ini dalam waktu yang terlalu lama di smartphone karena dapat menyebabkan baterai cepat panas (overheat).

Jika Anda ingin menyesuaikan pengujian ini, beri tahu saya:

* Apakah Anda menguji HP Android atau iOS?
* Apakah Anda ingin fokus menguji kekuatan Processor (CPU) atau Grafis (GPU)?
* Apakah Anda membutuhkan tombol Start/Stop untuk mengontrol beban kerjanya?


