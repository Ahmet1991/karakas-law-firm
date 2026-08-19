# Karakaş Hukuk Bürosu

Bağımsız, çok sayfalı, iki dilli (TR/EN) statik web sitesi.
Bağımlılık yok — GitHub Pages `main` dalının kökünden doğrudan yayınlanır.

## Yapı

```
index.html                        TR ana sayfa
en/index.html                     EN ana sayfa
faaliyet-alanlari/                TR faaliyet alanları (dizin + 12 detay sayfası)
en/practice-areas/                EN karşılıkları
styles.css                        Görsel sistem (tek dosya)
script.js                         Yalnızca davranış — hiçbir stil enjekte etmez
assets/                           Görseller, favicon seti, OG kartı
sitemap.xml, robots.txt           Üretilen dosyalar
tools/content.json                İçeriğin tek kaynağı
tools/build.py                    Sayfa üreticisi
```

## İçerik güncelleme

Faaliyet alanı metinleri `tools/content.json` içinde tutulur. Değişiklikten sonra:

```bash
python tools/build.py
```

26 faaliyet alanı sayfası ile `sitemap.xml` ve `robots.txt` yeniden üretilir.
**Üretilen HTML dosyaları repoya işlenir**; yayına alırken build adımı gerekmez,
GitHub Pages dosyaları olduğu gibi servis eder.

Ana sayfalar (`index.html`, `en/index.html`) elle düzenlenir — üretici onlara
dokunmaz.

## Görseller

Kaynak dosyalar (`KARAKAS_HUKUK_LOGO_SEFFAF_4K.png`, `pinar-karakas-seffaf-*.png`)
repoda durur ama tarayıcıya gönderilmez. Yayınlanan varyantlar bunlardan
üretilmiştir:

| Dosya | Kullanım |
| --- | --- |
| `mark-120/240.webp` | Header monogramı |
| `logo-lockup-420/840.webp` | Açık zemin için tam logo |
| `logo-lockup-ondark-420/840.webp` | Koyu zemin için (alt satır krem'e çekilmiştir) |
| `pinar-karakas-400/640/900.webp` | Portre, `srcset` ile |
| `favicon.ico`, `favicon-32.png`, `apple-touch-icon.png`, `icon-512.png` | Simge seti |
| `og-image.jpg` | Link önizleme kartı (1200×630) |

Orijinal logodaki "HUKUK BÜROSU" alt satırı siyahtır ve lacivert zeminde
okunmaz; `-ondark` varyantları bu satırı krem tona çeker.

Varyantları kaynak dosyalardan yeniden üretmek için (Pillow gerekir):

```bash
python tools/build_assets.py
```

## İletişim formu

Form, sunucu gerektirmeyen [web3forms.com](https://web3forms.com) üzerinden
çalışır. Bağlamak için:

1. `avpinarkarakas@gmail.com` ile ücretsiz kaydolun.
2. E-posta ile gelen Access Key'i `script.js` içindeki `FORM_ACCESS_KEY`
   sabitine yapıştırın.

Anahtar girilmediği sürece form gönderim yapmaz; bunun yerine ziyaretçiye,
girdiği bilgilerle **önceden doldurulmuş bir e-posta bağlantısı** sunulur —
yani hiçbir talep kaybolmaz. Formda ayrıca gizli bir spam tuzağı alanı ve
zorunlu KVKK onayı bulunur.

## Gizlilik

Site hiçbir çerez yerleştirmez; analitik veya reklam scripti yoktur. Harita
yalnızca ziyaretçi "Haritayı Yükle" düğmesine bastığında yüklenir — sayfa
açılışında Google'a hiçbir istek gitmez. `kvkk/` ve `en/privacy/` sayfalarındaki
aydınlatma metinleri `tools/legal-tr.html` ve `tools/legal-en.html` dosyalarından
üretilir.

## Hero fotoğrafı (opsiyonel)

`index.html` içinde yorum satırına alınmış `hero__photo` bloğu vardır. Uygun bir
İzmir/büro fotoğrafı `assets/hero-izmir.webp` olarak eklenip yorum kaldırılırsa
fotoğraf otomatik olarak bronz–lacivert duotone'a çevrilir; başka değişiklik
gerekmez.

## Yayına alma

Site şu an **hazırlık modundadır**: tüm sayfalarda `noindex` etiketi ve
`robots.txt` içinde `Disallow: /` bulunur. Böylece büronun canlı sitesiyle arama
sonuçlarında çakışmaz.

Alan adı bu siteye yönlendirildiğinde:

1. `tools/content.json` → `firm.preview` değerini `false` yapın, `python tools/build.py` çalıştırın.
2. `index.html` ve `en/index.html` içindeki `<meta name="robots" content="noindex, nofollow">` satırlarını silin.
3. Aynı dosyalara `<link rel="canonical" href="https://www.karakaslawfirm.com/">` (ve `/en/`) ekleyin.
4. `Settings → Pages` → Source: **Deploy from a branch**, Branch: **main**, Folder: **/(root)**.

## Doğrulanması gerekenler

Aşağıdaki maddeler yayına almadan önce Av. Pınar Karakaş tarafından teyit
edilmelidir:

- ~~**Adres.**~~ Netleşti: **Akdeniz Mah. 1353 Sk. No:2, Armesa İş Merkezi
  D:32, Konak / İzmir.** Canlı Wix sitesinin sayfa başlığında geçen
  *Adalet/Anadolu Caddesi, Bayraklı* adresi hatalıdır; yayına geçildiğinde
  Google İşletme Profili ve diğer dizinlerdeki eski kayıtların da
  güncellenmesi gerekir.
- Biyografi, unvan ve eğitim bilgileri.
- Faaliyet alanı metinleri ve ana sayfadaki alıntı cümlesi.
- Tüm içerik Türkiye Barolar Birliği Reklam Yasağı Yönetmeliği gözetilerek
  yazılmıştır: başarı oranı, müvekkil/dava sayısı, karşılaştırmalı veya üstünlük
  bildiren ifadeler bilinçli olarak kullanılmamıştır. Bu ilke korunmalıdır.
