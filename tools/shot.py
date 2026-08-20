#!/usr/bin/env python3
"""Render a full-page PNG of a homepage.

    python -m http.server 8899          # ayrı bir terminalde, repo kökünde
    python tools/shot.py                # -> tools/_out/home-tr.png
    python tools/shot.py en

Chrome'un tek seferlik ekran görüntüsü pencere yüksekliği kadarını alır; hero
`min-height:100svh` kullandığı için pencere uzatılınca hero de uzuyor. Bu yüzden
sayfanın yakalama için ölçüleri sabitlenmiş geçici bir kopyası üretilir.
"""
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "tools", "_out")
PORT = os.environ.get("SHOT_PORT", "8899")

CHROME_CANDIDATES = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    "/usr/bin/google-chrome",
    "/usr/bin/chromium",
]

OVERRIDE = """<style id="shot-override">
.hero { min-height: 0 !important; padding: 190px 0 130px !important; }
.reveal, .reveal-words { opacity: 1 !important; transform: none !important; }
.word > span { transform: none !important; }
.portrait img { clip-path: none !important; transform: none !important; }
.draw { transform: none !important; }
.scroll-cue, .wa-float, .action-bar { display: none !important; }
.site-header { position: absolute !important; }
</style>
</head>"""


def chrome():
    for path in CHROME_CANDIDATES:
        if os.path.exists(path):
            return path
    raise SystemExit("Chrome bulunamadi.")


def main():
    lang = sys.argv[1] if len(sys.argv) > 1 else "tr"
    height = int(sys.argv[2]) if len(sys.argv) > 2 else 5700
    source = "index.html" if lang == "tr" else os.path.join("en", "index.html")

    with open(os.path.join(ROOT, source), encoding="utf-8") as fh:
        page = fh.read()

    # The copy lives beside its source so relative asset paths still resolve.
    tmp_name = "_shot-{}.html".format(lang)
    tmp_dir = ROOT if lang == "tr" else os.path.join(ROOT, "en")
    tmp_path = os.path.join(tmp_dir, tmp_name)
    with open(tmp_path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(page.replace("</head>", OVERRIDE, 1))

    os.makedirs(OUT, exist_ok=True)
    target = os.path.join(OUT, "home-{}.png".format(lang))
    url = "http://127.0.0.1:{}/{}{}".format(
        PORT, "" if lang == "tr" else "en/", tmp_name
    )

    try:
        subprocess.run(
            [
                chrome(),
                "--headless=new",
                "--disable-gpu",
                "--hide-scrollbars",
                "--window-size=1280,{}".format(height),
                "--screenshot=" + target,
                "--virtual-time-budget=10000",
                url,
            ],
            check=True,
            capture_output=True,
        )
    finally:
        os.remove(tmp_path)

    size = os.path.getsize(target) / 1024
    print("{}  ({:.0f} KB)".format(os.path.relpath(target, ROOT), size))


if __name__ == "__main__":
    main()
