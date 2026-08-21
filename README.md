# Karakaş Hukuk Bürosu

Bağımsız, çok sayfalı, iki dilli (TR/EN) statik web sitesi. GitHub Pages `main` dalının kökünden doğrudan yayınlanır.

## Güncel yapı

```text
index.html                         TR ana sayfa
hakkimizda/                        TR hakkımızda / Pınar Karakaş
uzmanlik-alanlari/                 TR çalışma alanları ana dizini
faaliyet-alanlari/<slug>/          12 TR çalışma alanı detay sayfası
makaleler/                         TR makale dizini + 3 makale
iletisim/                          TR iletişim / ofis
kvkk/                              TR aydınlatma metni

en/index.html                      EN ana sayfa
en/about/                           EN about
en/practice-areas/                  EN practice areas + 12 detay
en/articles/                        EN article overview
en/contact/                         EN contact
en/privacy/                         EN privacy

404.html                            markalı özel 404
sitemap.xml                         iki dilli final sitemap
robots.txt                          hazırlık/canlı indeksleme kontrolü

tools/content.json                 çalışma alanı içerik kaynağı
tools/build.py                     eski temel sayfa üreticisi
tools/seo_postprocess.py           üretilen detay sayfalarının kalıcı SEO katmanı
tools/core_pages_seo.py            TR/EN çekirdek sayfa hreflang + EN metadata
tools/sitemap_finalize.py          final iki dilli sitemap üreticisi
tools/build_site.py                TEK KULLANILMASI GEREKEN build komutu
```

## İçerik ve SEO güncelleme

Faaliyet alanı metinleri `tools/content.json` içinde tutulur. İçerik veya jeneratör değişikliğinden sonra **`build.py` tek başına çalıştırılmamalıdır.** Doğru komut:

```bash
python tools/build_site.py
```

Bu komut sırasıyla:

1. temel TR/EN faaliyet sayfalarını üretir,
2. canonical, hreflang, Open Graph/Twitter ve yerel SEO metadata katmanını uygular,
3. elle yazılmış çekirdek TR/EN sayfaların dil eşleşmelerini normalize eder,
4. `/faaliyet-alanlari/` eski genel dizinini `/uzmanlik-alanlari/` sayfasına yönlendirir,
5. tüm gerçek TR/EN URL'lerini içeren `sitemap.xml` dosyasını son kez üretir,
6. `firm.preview` değerine göre `robots.txt` durumunu korur.

`.github/workflows/seo-build.yml` aynı komutu GitHub Actions üzerinden manuel **Run workflow** ile çalıştırabilecek şekilde tutulur.

## SEO hazırlık modu

Site şu an **hazırlık modundadır**. Üretim alan adı bu repoya taşınana kadar:

- önemli sayfalarda `noindex, nofollow` bulunur,
- `robots.txt` içinde `Disallow: /` bulunur,
- canonical ve hreflang değerleri nihai `https://www.karakaslawfirm.com/` adreslerini gösterir,
- sitemap hazırdır ancak staging kopyasının indekslenmesi bilinçli olarak engellenir.

Bu kilitler erken kaldırılmamalıdır; mevcut canlı site ile arama sonuçlarında çakışma oluşturabilir.

## Yayına alma

`karakaslawfirm.com` bu repodaki siteye yönlendirildiği gün:

1. `tools/content.json` içindeki `firm.preview` değerini `false` yapın.
2. `python tools/build_site.py` çalıştırın **veya** GitHub → Actions → **Regenerate practice SEO pages** → **Run workflow** kullanın.
3. Yeni TR çekirdek sayfalarda elle bırakılmış `noindex, nofollow` etiketleri varsa kaldırıldığını doğrulayın.
4. `robots.txt` çıktısının `Allow: /` ve `Sitemap: https://www.karakaslawfirm.com/sitemap.xml` içerdiğini doğrulayın.
5. Google Search Console'da alan adını doğrulayın ve sitemap'i gönderin.
6. Rich Results Test ile `LegalService`, `ProfilePage/Person`, `Article` ve `BreadcrumbList` işaretlemelerini kontrol edin.
7. Google Business Profile'da ad, telefon ve adresi site ile birebir eşitleyin.

Detaylı yayın kontrolü için `SEO_LAUNCH_CHECKLIST.md` dosyasını kullanın.

## Görseller

Yayınlanan temel görsel varlıklar:

| Dosya | Kullanım |
| --- | --- |
| `assets/logo-horizontal-ondark.webp` | Yeni header / marka |
| `assets/logo-lockup-ondark-420.webp` | Footer |
| `assets/hero-adalet-base.webp` | Masaüstü hero |
| `assets/hero-adalet-mobil.webp` | Mobil hero |
| `assets/hero-adalet-premium.webp` | Sosyal paylaşım / premium sahne |
| `assets/pinar-karakas-portre.webp` | Pınar Karakaş profil görseli |
| `assets/makale-*.webp` | Makale kapakları |
| `assets/og-image.jpg` | Üretilen faaliyet sayfalarının 1200×630 OG kartı |
| `favicon.ico`, `favicon-32.png`, `apple-touch-icon.png`, `icon-512.png` | Simge seti |

Kaynak görseller `assets/_source/` altında tutulur. Sayfalarda doğrudan kullanılmazlar.

Görsel varyantları yeniden üretmek için (Pillow gerekir):

```bash
python tools/build_assets.py
```

## İletişim ve ofis

- Telefon: **+90 530 549 30 90**
- E-posta: **avpinarkarakas@gmail.com**
- Adres: **Akdeniz Mah. 1353 Sk. No:2, Armesa İş Merkezi D:32, Konak / İzmir**
- LinkedIn: **Karakaş Law Firm**

İletişim sayfasındaki harita Armesa İş Merkezi konumuna sabitlenmiştir. Adres, telefon ve firma adı Google Business Profile ve diğer güvenilir dizinlerde aynı yazımla kullanılmalıdır.

## Gizlilik

`kvkk/` ve `en/privacy/` içeriklerinin kaynak parçaları `tools/legal-tr.html` ve `tools/legal-en.html` dosyalarındadır. Siteye analitik veya reklam servisi eklenirse KVKK/çerez tarafı yeniden değerlendirilmelidir.

## İçerik ilkesi

Yayına almadan önce Av. Pınar Karakaş tarafından biyografi, eğitim bilgileri, faaliyet alanı metinleri ve hukuki içerikler son kez teyit edilmelidir.

Türkiye Barolar Birliği reklam yasağı gözetilmelidir. Başarı oranı, müvekkil/dava sayısı, karşılaştırmalı üstünlük, garanti, yanıltıcı ödül veya değerlendirme ifadeleri eklenmemelidir.
