# Karakaş Hukuk Bürosu — SEO Yayına Alma Kontrolü

Bu dosya **karakaslawfirm.com bu repodaki siteye yönlendirildiği gün** uygulanacak son SEO adımlarını listeler.

## Yayından önce — şu anki durum

- `tools/content.json` içindeki `firm.preview` değeri **true**.
- `robots.txt` staging kopyasını bilerek `Disallow: /` ile kapatıyor ve preview modunda production sitemap'i ilan etmiyor.
- İndekslenebilir olması planlanan TR/EN sayfalarda `noindex, nofollow` bilerek açık.
- Canonical, Open Graph / Twitter ve yapılandırılmış veri çekirdek sayfalara eklenmiştir.
- 12 Türkçe + 12 İngilizce çalışma alanı detayında yerel title/description, canonical ve karşılıklı hreflang bulunur.
- 3 makalede `Article` + `BreadcrumbList` JSON-LD, Av. Pınar Karakaş yazar bilgisi ve ilgili çalışma alanlarına iç linkler vardır.
- Final sitemap Türkçe/İngilizce çekirdek sayfaları, 3 makaleyi ve 24 çalışma alanı detayını içerir.
- Eski `/faaliyet-alanlari/` genel dizin sayfası `noindex` + canonical ile yeni `/uzmanlik-alanlari/` sayfasına yönlendirilir; detay URL'leri korunur.
- `404.html` markalıdır ve daima `noindex, follow` kalır.

## Tek doğru build komutu

İçerik veya SEO üretimi için `tools/build.py` **tek başına kullanılmaz**.

```bash
python tools/build_site.py
python tools/seo_audit.py
```

Alternatif olarak GitHub → **Actions** → **Regenerate practice SEO pages** → **Run workflow** kullanılabilir. Workflow build sonrasında `seo_audit.py` testini çalıştırır; audit başarısızsa üretilen SEO çıktısı commit edilmez.

## Alan adı bu siteye geçtiğinde

1. Önce DNS/hosting tarafında `karakaslawfirm.com` ve `www.karakaslawfirm.com` alan adlarının bu siteyi açtığını doğrulayın.
2. `tools/content.json` içindeki `firm.preview` değerini **false** yapın.
3. `python tools/build_site.py` çalıştırın veya GitHub Actions'tan **Run workflow** kullanın.
4. Ardından `python tools/seo_audit.py` sonucunun **SEO AUDIT OK** olduğunu doğrulayın.
5. Üretilen `robots.txt` şu yapıda olmalıdır:

```text
User-agent: *
Allow: /

Sitemap: https://www.karakaslawfirm.com/sitemap.xml
```

6. Ana sayfa, Hakkımızda, Uzmanlık Alanları, Makaleler, İletişim, üç Türkçe makale, TR/EN çalışma alanları ve EN çekirdek sayfalarda `noindex` kalmadığını doğrulayın. Bu işlem normalde `build_site.py` tarafından otomatik yapılır.
7. `404.html` ve eski `/faaliyet-alanlari/` genel yönlendirme sayfası **noindex kalmalıdır**.
8. Google Search Console'da alan adı mülkünü doğrulayın ve `https://www.karakaslawfirm.com/sitemap.xml` gönderin.
9. URL Denetleme ile öncelikle şu sayfaları indekslemeye gönderin:
   - `/`
   - `/hakkimizda/`
   - `/uzmanlik-alanlari/`
   - `/makaleler/`
   - `/iletisim/`
   - üç makale URL'si
   - `/en/`
10. Google Rich Results Test ile ana sayfadaki `LegalService`, Hakkımızda'daki `ProfilePage/Person` ve makalelerdeki `Article/BreadcrumbList` işaretlemelerini kontrol edin.
11. Google Business Profile'daki firma adı, telefon ve adresi site ile birebir aynı tutun:
   - Karakaş Hukuk Bürosu
   - +90 530 549 30 90
   - Akdeniz Mah. 1353 Sk. No:2, Armesa İş Merkezi D:32, Konak / İzmir
12. Eski canlı sitedeki URL'ler biliniyorsa yeni karşılıklarına mümkün olan yerde sunucu/CDN seviyesinde **301 redirect** tanımlayın. GitHub Pages'in istemci tarafı yönlendirmesi yalnızca fallback olarak düşünülmelidir.
13. Gerçek Instagram/Facebook hesapları oluşursa `sameAs` ve footer bağlantılarına ekleyin; sahte/boş profil eklemeyin.
14. İlk 2–4 hafta Search Console'da indeksleme, Core Web Vitals, 404, yönlendirme ve canonical raporlarını takip edin.

## SEO audit neyi kontrol eder?

`tools/seo_audit.py` build sonrasında otomatik olarak şunları denetler:

- beklenen dosyaların varlığı,
- canonical URL'ler,
- title ve meta description,
- absolute Open Graph görselleri,
- preview/production `noindex` durumu,
- TR ↔ EN hreflang karşılıklılığı,
- 3 makaledeki `Article` schema ve yazar bilgisi,
- sitemap URL seti,
- eski `/faaliyet-alanlari/` genel sayfasının sitemap dışında kalması,
- preview/production `robots.txt` davranışı,
- 404 ve legacy redirect sayfalarının noindex kalması,
- İngilizce ana sayfa/makale dizininde eski 2024 tarih kalıntısı bulunmaması.

## İçerik kuralı

Makalelerde yazar bilgisi **Av. Pınar Karakaş** olarak tutarlı kalmalı. Yeni her makalede benzersiz title/description, yayın tarihi, canonical, `Article` schema, breadcrumb ve en az bir ilgili çalışma alanı iç bağlantısı bulunmalı.

Türkiye Barolar Birliği reklam yasağı gözetilerek başarı oranı, müvekkil/dava sayısı, karşılaştırmalı üstünlük, garanti, yanıltıcı ödül veya değerlendirme schema'ları eklenmemelidir.
