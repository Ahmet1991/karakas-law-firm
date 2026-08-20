# -*- coding: utf-8 -*-
"""Hero katmanlarini uretir.

  python tools/build-hero.py [scale] [boss_y]

Kaynaklar assets/_source icinde. Terazi ayri bir katman oldugu icin
sahne (terazisiz), terazi (seffaf) ve ikisinin birlesigi ayri ayri
yazilir; mobil icin ayni uclu, dikey ekrana uygun kadrajla tekrarlanir.
"""
import sys
from PIL import Image

SCALE = float(sys.argv[1]) if len(sys.argv) > 1 else 0.27
BOSS_Y = int(sys.argv[2]) if len(sys.argv) > 2 else 210

BOSS = (1009, 51)          # sarkac.png'de gobegin tepesi
BOSS_MID = 100             # gobegin dikey merkezi
LEAN = 0.077               # sopa asagi indikce saga kayiyor (~4.4 derece)
MOBILE_CROP = (780, 10, 1660, 900)

BOSS_X = 1292 + round((BOSS_Y - 172) * LEAN)

A = Image.open('assets/_source/hero-katman-a-terazisiz.png').convert('RGBA')
B = Image.open('assets/_source/hero-katman-b-terazi.png').convert('RGBA')
W, H = A.size

Bs = B.resize((round(B.width*SCALE), round(B.height*SCALE)), Image.LANCZOS)
layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
layer.alpha_composite(Bs, (BOSS_X - round(BOSS[0]*SCALE), BOSS_Y - round(BOSS[1]*SCALE)))
full = A.copy(); full.alpha_composite(layer)

layer.save('assets/hero-terazi.webp', quality=92, method=6)
A.convert('RGB').save('assets/hero-adalet-base.webp', quality=86, method=6)
full.convert('RGB').save('assets/hero-adalet-premium.webp', quality=86, method=6)

cx0, cy0, cx1, cy1 = MOBILE_CROP
cw, ch = cx1-cx0, cy1-cy0
layer.crop(MOBILE_CROP).save('assets/hero-terazi-mobil.webp', quality=92, method=6)
A.crop(MOBILE_CROP).convert('RGB').save('assets/hero-adalet-mobil.webp', quality=86, method=6)
full.crop(MOBILE_CROP).convert('RGB').save('assets/hero-adalet-mobil-full.webp', quality=86, method=6)

pvx, pvy = BOSS_X, BOSS_Y + (BOSS_MID - BOSS[1]) * SCALE
print('olcek %.2f  gobek (%d,%d)' % (SCALE, BOSS_X, BOSS_Y))
print('masaustu mesnet : %.2f%% %.2f%%' % (100*pvx/W, 100*pvy/H))
print('mobil mesnet    : %.2f%% %.2f%%' % (100*(pvx-cx0)/cw, 100*(pvy-cy0)/ch))
print('mobil en/boy    : %d/%d' % (cw, ch))
