# Karakaş Hukuk Bürosu — SEO Yayına Alma Kontrolü

Bu dosya **karakaslawfirm.com bu repodaki siteye yönlendirildiği gün** uygulanacak son SEO adımlarını listeler.

## Yayından önce — şu anki durum

- `robots.txt` bilerek `Disallow: /` durumda.
- Yeni TR sayfalarda `noindex, nofollow` bilerek açık.
- Canonical, Open Graph / Twitter ve yapılandırılmış veri çekirdek sayfalara eklenmiştir.
- 3 makalede `Article` + `BreadcrumbList` JSON-LD ve ilgili çalışma alanlarına iç linkler vardır.
- Sitemap güncel makaleleri ve çalışma alanı detaylarını içerir.
- Eski `/faaliyet-alanlari/` genel dizin sayfası yeni `/uzmanlik-alanlari/` sayfasına yönlendirilir; detay URL'leri korunur.

## Alan adı bu siteye geçtiğinde

1. `robots.txt` içindeki:
   - `Disallow: /` kaldırılır.
   - `Allow: /` kullanılır.
   - `Sitemap: https://www.karakaslawfirm.com/sitemap.xml` korunur.
2. Yeni TR sayfalardaki `<meta name="robots" content="noindex, nofollow">` etiketleri kaldırılır.
3. `tools/content.json` içindeki `firm.preview` değeri `false` yapılmadan önce jeneratörün yeni `/uzmanlik-alanlari/` mimarisiyle uyumlu olduğu kontrol edilir.
4. İngilizce ana sayfa ve İngilizce practice-area sayfalarında canonical/hreflang karşılıklılığı son kez doğrulanır.
5. Google Search Console'da alan adı doğrulanır ve `https://www.karakaslawfirm.com/sitemap.xml` gönderilir.
6. URL Denetleme ile en az şu sayfalar indekslemeye gönderilir:
   - `/`
   - `/hakkimizda/`
   - `/uzmanlik-alanlari/`
   - `/makaleler/`
   - `/iletisim/`
   - üç makale URL'si
7. Google Rich Results Test ile ana sayfadaki `LegalService`, Hakkımızda'daki `ProfilePage/Person` ve makalelerdeki `Article/BreadcrumbList` işaretlemeleri kontrol edilir.
8. Google Business Profile'daki ad, telefon ve adres site ile birebir aynı tutulur:
   - Karakaş Hukuk Bürosu
   - +90 530 549 30 90
   - Akdeniz Mah. 1353 Sk. No:2, Armesa İş Merkezi D:32, Konak / İzmir
9. Gerçek Instagram/Facebook hesapları oluşursa `sameAs` ve footer bağlantılarına eklenir; sahte/boş profil eklenmez.
10. İlk 2–4 hafta Search Console'da indeksleme, Core Web Vitals, 404 ve canonical raporları takip edilir.

## İçerik kuralı

Makalelerde yazar bilgisi **Av. Pınar Karakaş** olarak tutarlı kalmalı. Yeni her makalede benzersiz title/description, yayın tarihi, canonical, Article schema, breadcrumb ve en az bir ilgili çalışma alanı iç bağlantısı bulunmalı.

Türkiye Barolar Birliği reklam yasağı dikkate alınarak başarı oranı, müvekkil/dava sayısı, karşılaştırmalı üstünlük, garanti veya yanıltıcı değerlendirme schema'ları eklenmemelidir.
