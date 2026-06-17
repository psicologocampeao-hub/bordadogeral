#!/usr/bin/env python3
"""Download all external assets and update index.html for local deployment."""

import urllib.request
import urllib.error
import os
import re
import json
from pathlib import Path
from urllib.parse import urlparse, urljoin

BASE_DIR = Path(r"c:\Users\igorz\Documents\Sites\bordadogeral")
ASSETS_CSS    = BASE_DIR / "assets/css"
ASSETS_JS     = BASE_DIR / "assets/js"
ASSETS_FONTS  = BASE_DIR / "assets/fonts"
ASSETS_IMAGES = BASE_DIR / "assets/images"

for d in [ASSETS_CSS, ASSETS_JS, ASSETS_FONTS, ASSETS_IMAGES]:
    d.mkdir(parents=True, exist_ok=True)

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Referer': 'https://maquinadeebook.online/bordado/'
}

def download(url, dest: Path) -> bool:
    clean_url = url.split('?')[0]
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            data = r.read()
        # If CSS/JS returned HTML, try ?nonitro=1
        if dest.suffix in ('.css', '.js') and data.lstrip()[:5].lower() in (b'<!doc', b'<html', b'<?xml'):
            print(f"  [HTML response] retrying with ?nonitro=1: {dest.name}")
            req2 = urllib.request.Request(clean_url + '?nonitro=1', headers=HEADERS)
            with urllib.request.urlopen(req2, timeout=30) as r2:
                data = r2.read()
        dest.write_bytes(data)
        size = len(data)
        print(f"  OK  {dest.name}  ({size:,} bytes)")
        return True
    except Exception as e:
        print(f"  FAIL {url}: {e}")
        return False

# ── URL → local relative path mapping ────────────────────────────────────────
# Key: URL (with or without query string), Value: local relative path from BASE_DIR
url_map: dict[str, str] = {}

# ── CSS files ────────────────────────────────────────────────────────────────
CSS_URLS = [
    ("https://maquinadeebook.online/wp-content/plugins/hostinger-reach/frontend/dist/blocks/subscription.css?ver=1781714147", "subscription.css"),
    ("https://maquinadeebook.online/wp-content/themes/twentytwentyfive/style.css?ver=1.3", "style.css"),
    ("https://maquinadeebook.online/wp-content/plugins/elementor/assets/css/frontend.min.css?ver=4.1.3", "frontend.min.css"),
    ("https://maquinadeebook.online/wp-content/uploads/elementor/css/post-5.css?ver=1781714189", "post-5.css"),
    ("https://maquinadeebook.online/wp-content/plugins/elementor/assets/css/widget-heading.min.css?ver=4.1.3", "widget-heading.min.css"),
    ("https://maquinadeebook.online/wp-content/plugins/elementor/assets/css/widget-image.min.css?ver=4.1.3", "widget-image.min.css"),
    ("https://maquinadeebook.online/wp-content/plugins/elementor/assets/css/widget-icon-list.min.css?ver=4.1.3", "widget-icon-list.min.css"),
    ("https://maquinadeebook.online/wp-content/plugins/elementor/assets/lib/animations/styles/e-animation-pulse.min.css?ver=4.1.3", "e-animation-pulse.min.css"),
    ("https://maquinadeebook.online/wp-content/plugins/elementor/assets/lib/swiper/v8/css/swiper.min.css?ver=8.4.5", "swiper.min.css"),
    ("https://maquinadeebook.online/wp-content/plugins/elementor/assets/css/conditionals/e-swiper.min.css?ver=4.1.3", "e-swiper.min.css"),
    ("https://maquinadeebook.online/wp-content/plugins/elementor/assets/css/widget-image-carousel.min.css?ver=4.1.3", "widget-image-carousel.min.css"),
    ("https://maquinadeebook.online/wp-content/plugins/elementor/assets/css/widget-image-box.min.css?ver=4.1.3", "widget-image-box.min.css"),
    ("https://maquinadeebook.online/wp-content/plugins/elementor-pro/assets/css/widget-countdown.min.css?ver=3.27.6", "widget-countdown.min.css"),
    ("https://maquinadeebook.online/wp-content/plugins/elementor/assets/css/widget-divider.min.css?ver=4.1.3", "widget-divider.min.css"),
    ("https://maquinadeebook.online/wp-content/plugins/elementor/assets/css/widget-rating.min.css?ver=4.1.3", "widget-rating.min.css"),
    ("https://maquinadeebook.online/wp-content/plugins/elementor-pro/assets/css/widget-nested-carousel.min.css?ver=3.27.6", "widget-nested-carousel.min.css"),
    ("https://maquinadeebook.online/wp-content/plugins/elementor/assets/css/widget-toggle.min.css?ver=4.1.3", "widget-toggle.min.css"),
    ("https://maquinadeebook.online/wp-content/uploads/elementor/css/post-2393.css?ver=1781714190", "post-2393.css"),
]

print("\n=== Downloading CSS ===")
for url, local_name in CSS_URLS:
    dest = ASSETS_CSS / local_name
    rel = f"assets/css/{local_name}"
    url_map[url] = rel
    url_map[url.split('?')[0]] = rel
    download(url, dest)

# ── JS files ─────────────────────────────────────────────────────────────────
JS_URLS = [
    ("https://maquinadeebook.online/wp-includes/js/jquery/jquery.min.js?ver=3.7.1", "jquery.min.js"),
    ("https://maquinadeebook.online/wp-includes/js/jquery/jquery-migrate.min.js?ver=3.4.1", "jquery-migrate.min.js"),
    ("https://maquinadeebook.online/wp-content/plugins/hostinger-reach/frontend/dist/blocks/subscription-view.js?ver=1781714147", "subscription-view.js"),
    ("https://maquinadeebook.online/wp-content/plugins/elementor/assets/js/webpack.runtime.min.js?ver=4.1.3", "webpack.runtime.min.js"),
    ("https://maquinadeebook.online/wp-content/plugins/elementor/assets/js/frontend-modules.min.js?ver=4.1.3", "frontend-modules.min.js"),
    ("https://maquinadeebook.online/wp-includes/js/jquery/ui/core.min.js?ver=1.13.3", "jquery-ui-core.min.js"),
    ("https://maquinadeebook.online/wp-content/plugins/elementor/assets/js/frontend.min.js?ver=4.1.3", "elementor-frontend.min.js"),
    ("https://maquinadeebook.online/wp-content/plugins/elementor/assets/lib/swiper/v8/swiper.min.js?ver=8.4.5", "swiper.min.js"),
    ("https://maquinadeebook.online/wp-content/plugins/elementor-pro/assets/js/webpack-pro.runtime.min.js?ver=3.27.6", "webpack-pro.runtime.min.js"),
    ("https://maquinadeebook.online/wp-includes/js/dist/hooks.min.js?ver=4d63a3d491d11ffd8ac6", "hooks.min.js"),
    ("https://maquinadeebook.online/wp-includes/js/dist/i18n.min.js?ver=5e580eb46a90c2b997e6", "i18n.min.js"),
    ("https://maquinadeebook.online/wp-content/plugins/elementor-pro/assets/js/frontend.min.js?ver=3.27.6", "elementor-pro-frontend.min.js"),
    ("https://maquinadeebook.online/wp-content/plugins/elementor-pro/assets/js/elements-handlers.min.js?ver=3.27.6", "elements-handlers.min.js"),
    ("https://maquinadeebook.online/wp-includes/js/wp-emoji-release.min.js?ver=6.8.5", "wp-emoji-release.min.js"),
]

print("\n=== Downloading JS ===")
for url, local_name in JS_URLS:
    dest = ASSETS_JS / local_name
    rel = f"assets/js/{local_name}"
    url_map[url] = rel
    url_map[url.split('?')[0]] = rel
    download(url, dest)

# ── Fonts from maquinadeebook ─────────────────────────────────────────────────
FONT_URLS = [
    ("https://maquinadeebook.online/wp-content/themes/twentytwentyfive/assets/fonts/manrope/Manrope-VariableFont_wght.woff2", "Manrope-VariableFont_wght.woff2"),
    ("https://maquinadeebook.online/wp-content/themes/twentytwentyfive/assets/fonts/fira-code/FiraCode-VariableFont_wght.woff2", "FiraCode-VariableFont_wght.woff2"),
]

print("\n=== Downloading Fonts ===")
for url, local_name in FONT_URLS:
    dest = ASSETS_FONTS / local_name
    rel = f"assets/fonts/{local_name}"
    url_map[url] = rel
    url_map[url.split('?')[0]] = rel
    download(url, dest)

# ── Images from maquinadeebook ────────────────────────────────────────────────
IMAGE_URLS_MAQUINA = [
    "https://maquinadeebook.online/wp-content/uploads/2026/06/ChatGPT-Image-14-de-jun.-de-2026-15_58_58-1024x1024.png",
    "https://maquinadeebook.online/wp-content/uploads/2026/06/ChatGPT-Image-14-de-jun.-de-2026-15_58_58-150x150.png",
    "https://maquinadeebook.online/wp-content/uploads/2026/06/ChatGPT-Image-14-de-jun.-de-2026-15_58_58-300x300.png",
    "https://maquinadeebook.online/wp-content/uploads/2026/06/ChatGPT-Image-14-de-jun.-de-2026-15_58_58-768x768.png",
    "https://maquinadeebook.online/wp-content/uploads/2026/06/ChatGPT-Image-14-de-jun.-de-2026-15_58_58.png",
    "https://maquinadeebook.online/wp-content/uploads/2026/06/ChatGPT-Image-14-de-jun.-de-2026-16_07_32-1.png",
    "https://maquinadeebook.online/wp-content/uploads/2026/06/ChatGPT-Image-14-de-jun.-de-2026-16_07_33-2.png",
    "https://maquinadeebook.online/wp-content/uploads/2026/06/ChatGPT-Image-14-de-jun.-de-2026-16_07_33-3.png",
    "https://maquinadeebook.online/wp-content/uploads/2026/06/ChatGPT-Image-14-de-jun.-de-2026-16_07_33-4.png",
    "https://maquinadeebook.online/wp-content/uploads/2026/06/ChatGPT-Image-14-de-jun.-de-2026-16_07_35-5.png",
    "https://maquinadeebook.online/wp-content/uploads/2026/06/ChatGPT-Image-14-de-jun.-de-2026-16_07_35-7.png",
    "https://maquinadeebook.online/wp-content/uploads/2026/06/ChatGPT-Image-14-de-jun.-de-2026-16_07_35-8.png",
    "https://maquinadeebook.online/wp-content/uploads/2026/06/ChatGPT-Image-14-de-jun.-de-2026-16_07_36-10.png",
    "https://maquinadeebook.online/wp-content/uploads/2026/06/ChatGPT-Image-14-de-jun.-de-2026-16_07_36-9-1024x1024.png",
    "https://maquinadeebook.online/wp-content/uploads/2026/06/ChatGPT-Image-14-de-jun.-de-2026-16_07_36-9-150x150.png",
    "https://maquinadeebook.online/wp-content/uploads/2026/06/ChatGPT-Image-14-de-jun.-de-2026-16_07_36-9-300x300.png",
    "https://maquinadeebook.online/wp-content/uploads/2026/06/ChatGPT-Image-14-de-jun.-de-2026-16_07_36-9-768x768.png",
    "https://maquinadeebook.online/wp-content/uploads/2026/06/ChatGPT-Image-14-de-jun.-de-2026-16_07_36-9.png",
    "https://maquinadeebook.online/wp-content/uploads/2026/06/ChatGPT-Image-14-de-jun.-de-2026-16_14_44-1.png",
    "https://maquinadeebook.online/wp-content/uploads/2026/06/ChatGPT-Image-14-de-jun.-de-2026-16_14_44-2.png",
    "https://maquinadeebook.online/wp-content/uploads/2026/06/ChatGPT-Image-14-de-jun.-de-2026-16_14_45-3.png",
    "https://maquinadeebook.online/wp-content/uploads/2026/06/ChatGPT-Image-14-de-jun.-de-2026-16_14_45-4.png",
    "https://maquinadeebook.online/wp-content/uploads/2026/06/ChatGPT-Image-14-de-jun.-de-2026-16_14_45-5.png",
    "https://maquinadeebook.online/wp-content/uploads/2026/06/ChatGPT-Image-14-de-jun.-de-2026-16_14_45-6.png",
    "https://maquinadeebook.online/wp-content/uploads/2026/06/ChatGPT-Image-14-de-jun.-de-2026-16_14_46-10.png",
    "https://maquinadeebook.online/wp-content/uploads/2026/06/ChatGPT-Image-14-de-jun.-de-2026-16_14_46-7.png",
    "https://maquinadeebook.online/wp-content/uploads/2026/06/ChatGPT-Image-14-de-jun.-de-2026-16_14_46-8.png",
    "https://maquinadeebook.online/wp-content/uploads/2026/06/ChatGPT-Image-14-de-jun.-de-2026-16_14_46-9.png",
    "https://maquinadeebook.online/wp-content/uploads/2026/06/ChatGPT-Image-14-de-jun.-de-2026-16_25_16-1024x768.png",
    "https://maquinadeebook.online/wp-content/uploads/2026/06/ChatGPT-Image-14-de-jun.-de-2026-16_25_16-300x225.png",
    "https://maquinadeebook.online/wp-content/uploads/2026/06/ChatGPT-Image-14-de-jun.-de-2026-16_25_16-768x576.png",
    "https://maquinadeebook.online/wp-content/uploads/2026/06/ChatGPT-Image-14-de-jun.-de-2026-16_25_16.png",
    "https://maquinadeebook.online/wp-content/uploads/2026/06/ChatGPT-Image-14-de-jun.-de-2026-16_31_39-1024x1024.png",
    "https://maquinadeebook.online/wp-content/uploads/2026/06/ChatGPT-Image-14-de-jun.-de-2026-16_31_39-150x150.png",
    "https://maquinadeebook.online/wp-content/uploads/2026/06/ChatGPT-Image-14-de-jun.-de-2026-16_31_39-300x300.png",
    "https://maquinadeebook.online/wp-content/uploads/2026/06/ChatGPT-Image-14-de-jun.-de-2026-16_31_39-768x768.png",
    "https://maquinadeebook.online/wp-content/uploads/2026/06/ChatGPT-Image-14-de-jun.-de-2026-16_31_39.png",
    "https://maquinadeebook.online/wp-content/uploads/2026/06/ChatGPT-Image-14-de-jun.-de-2026-17_09_56-1-240x300.png",
    "https://maquinadeebook.online/wp-content/uploads/2026/06/ChatGPT-Image-14-de-jun.-de-2026-17_09_56-1-768x960.png",
    "https://maquinadeebook.online/wp-content/uploads/2026/06/ChatGPT-Image-14-de-jun.-de-2026-17_09_56-1-819x1024.png",
    "https://maquinadeebook.online/wp-content/uploads/2026/06/ChatGPT-Image-14-de-jun.-de-2026-17_09_56-1.png",
    "https://maquinadeebook.online/wp-content/uploads/2026/06/ChatGPT-Image-14-de-jun.-de-2026-17_09_56-2-240x300.png",
    "https://maquinadeebook.online/wp-content/uploads/2026/06/ChatGPT-Image-14-de-jun.-de-2026-17_09_56-2-768x960.png",
    "https://maquinadeebook.online/wp-content/uploads/2026/06/ChatGPT-Image-14-de-jun.-de-2026-17_09_56-2-819x1024.png",
    "https://maquinadeebook.online/wp-content/uploads/2026/06/ChatGPT-Image-14-de-jun.-de-2026-17_09_56-2.png",
    "https://maquinadeebook.online/wp-content/uploads/2026/06/ChatGPT-Image-14-de-jun.-de-2026-17_09_56-3-240x300.png",
    "https://maquinadeebook.online/wp-content/uploads/2026/06/ChatGPT-Image-14-de-jun.-de-2026-17_09_56-3-768x960.png",
    "https://maquinadeebook.online/wp-content/uploads/2026/06/ChatGPT-Image-14-de-jun.-de-2026-17_09_56-3-819x1024.png",
    "https://maquinadeebook.online/wp-content/uploads/2026/06/ChatGPT-Image-14-de-jun.-de-2026-17_09_56-3.png",
    "https://maquinadeebook.online/wp-content/uploads/2026/06/ChatGPT-Image-14-de-jun.-de-2026-17_41_33-1024x1024.png",
    "https://maquinadeebook.online/wp-content/uploads/2026/06/ChatGPT-Image-14-de-jun.-de-2026-17_41_33-150x150.png",
    "https://maquinadeebook.online/wp-content/uploads/2026/06/ChatGPT-Image-14-de-jun.-de-2026-17_41_33-300x300.png",
    "https://maquinadeebook.online/wp-content/uploads/2026/06/ChatGPT-Image-14-de-jun.-de-2026-17_41_33-768x768.png",
    "https://maquinadeebook.online/wp-content/uploads/2026/06/ChatGPT-Image-14-de-jun.-de-2026-17_41_33.png",
    "https://maquinadeebook.online/wp-content/uploads/2026/06/ChatGPT-Image-14-de-jun.-de-2026-17_41_48-1024x1024.png",
    "https://maquinadeebook.online/wp-content/uploads/2026/06/ChatGPT-Image-14-de-jun.-de-2026-17_41_48-150x150.png",
    "https://maquinadeebook.online/wp-content/uploads/2026/06/ChatGPT-Image-14-de-jun.-de-2026-17_41_48-300x300.png",
    "https://maquinadeebook.online/wp-content/uploads/2026/06/ChatGPT-Image-14-de-jun.-de-2026-17_41_48-768x768.png",
    "https://maquinadeebook.online/wp-content/uploads/2026/06/ChatGPT-Image-14-de-jun.-de-2026-17_41_48.png",
    # April uploads (icons)
    "https://maquinadeebook.online/wp-content/uploads/2026/04/4904543.png",
    "https://maquinadeebook.online/wp-content/uploads/2026/04/4904543-300x300.png",
    "https://maquinadeebook.online/wp-content/uploads/2026/04/4904543-150x150.png",
    "https://maquinadeebook.online/wp-content/uploads/2026/04/check-mark.png",
    "https://maquinadeebook.online/wp-content/uploads/2026/04/check-mark-300x300.png",
    "https://maquinadeebook.online/wp-content/uploads/2026/04/check-mark-150x150.png",
    "https://maquinadeebook.online/wp-content/uploads/2026/04/digital-drawing.png",
    "https://maquinadeebook.online/wp-content/uploads/2026/04/digital-drawing-300x300.png",
    "https://maquinadeebook.online/wp-content/uploads/2026/04/digital-drawing-150x150.png",
    "https://maquinadeebook.online/wp-content/uploads/2026/04/download.png",
    "https://maquinadeebook.online/wp-content/uploads/2026/04/download-300x300.png",
    "https://maquinadeebook.online/wp-content/uploads/2026/04/download-150x150.png",
    "https://maquinadeebook.online/wp-content/uploads/2026/04/folders-1.png",
    "https://maquinadeebook.online/wp-content/uploads/2026/04/folders-1-300x300.png",
    "https://maquinadeebook.online/wp-content/uploads/2026/04/folders-1-150x150.png",
    "https://maquinadeebook.online/wp-content/uploads/2026/04/garantia-15-dias-1.png",
    "https://maquinadeebook.online/wp-content/uploads/2026/04/garantia-15-dias-1-1024x683.png",
    "https://maquinadeebook.online/wp-content/uploads/2026/04/garantia-15-dias-1-768x512.png",
    "https://maquinadeebook.online/wp-content/uploads/2026/04/garantia-15-dias-1-300x200.png",
    "https://maquinadeebook.online/wp-content/uploads/2026/04/icons-meio-de-pagamento-e1738718378460-2-1.png",
    "https://maquinadeebook.online/wp-content/uploads/2026/04/manual-book.png",
    "https://maquinadeebook.online/wp-content/uploads/2026/04/manual-book-300x300.png",
    "https://maquinadeebook.online/wp-content/uploads/2026/04/manual-book-150x150.png",
    "https://maquinadeebook.online/wp-content/uploads/2026/04/member-card.png",
    "https://maquinadeebook.online/wp-content/uploads/2026/04/member-card-300x300.png",
    "https://maquinadeebook.online/wp-content/uploads/2026/04/member-card-150x150.png",
    "https://maquinadeebook.online/wp-content/uploads/2026/04/order.png",
    "https://maquinadeebook.online/wp-content/uploads/2026/04/order-300x300.png",
    "https://maquinadeebook.online/wp-content/uploads/2026/04/order-150x150.png",
    "https://maquinadeebook.online/wp-content/uploads/2026/04/scale.png",
    "https://maquinadeebook.online/wp-content/uploads/2026/04/scale-300x300.png",
    "https://maquinadeebook.online/wp-content/uploads/2026/04/scale-150x150.png",
]

# Flaticon icons
FLATICON_URLS = [
    ("https://cdn-icons-png.flaticon.com/512/733/733585.png", "flaticon-733585.png"),
    ("https://cdn-icons-png.flaticon.com/512/732/732200.png", "flaticon-732200.png"),
]

print("\n=== Downloading Images (maquinadeebook) ===")
for url in IMAGE_URLS_MAQUINA:
    local_name = Path(urlparse(url).path).name
    dest = ASSETS_IMAGES / local_name
    rel = f"assets/images/{local_name}"
    url_map[url] = rel
    download(url, dest)

print("\n=== Downloading Flaticon Icons ===")
for url, local_name in FLATICON_URLS:
    dest = ASSETS_IMAGES / local_name
    rel = f"assets/images/{local_name}"
    url_map[url] = rel
    url_map[url.split('?')[0]] = rel
    download(url, dest)

# ── Scan downloaded CSS for additional url() resources ────────────────────────
print("\n=== Scanning CSS for embedded url() resources ===")

def extract_css_urls(css_text: str, css_url: str) -> list[str]:
    """Extract all url(...) values from CSS, resolved against css_url."""
    found = []
    for m in re.finditer(r'url\(\s*["\']?([^)"\'\s]+)["\']?\s*\)', css_text):
        raw = m.group(1)
        if raw.startswith('data:'):
            continue
        resolved = urljoin(css_url, raw)
        if resolved.startswith('https://maquinadeebook.online'):
            found.append(resolved.split('?')[0])
    return found

for url, local_name in CSS_URLS:
    css_file = ASSETS_CSS / local_name
    if not css_file.exists():
        continue
    css_base_url = url.split('?')[0]
    try:
        css_text = css_file.read_text(encoding='utf-8', errors='replace')
    except:
        continue
    embedded_urls = extract_css_urls(css_text, css_base_url)
    if not embedded_urls:
        continue
    print(f"  {local_name} has {len(embedded_urls)} embedded URL(s)")
    for eurl in set(embedded_urls):
        if eurl in url_map:
            continue
        parsed = urlparse(eurl)
        ename = Path(parsed.path).name
        ext = Path(ename).suffix.lower()
        if ext in ('.woff', '.woff2', '.ttf', '.eot', '.otf'):
            dest = ASSETS_FONTS / ename
            rel = f"assets/fonts/{ename}"
        elif ext in ('.png', '.jpg', '.jpeg', '.gif', '.webp', '.svg'):
            dest = ASSETS_IMAGES / ename
            rel = f"assets/images/{ename}"
        else:
            dest = ASSETS_CSS / ename
            rel = f"assets/css/{ename}"
        if not dest.exists():
            print(f"    Downloading embedded: {ename}")
            download(eurl, dest)
        url_map[eurl] = rel

# ── Rewrite CSS files to use local paths ─────────────────────────────────────
print("\n=== Rewriting CSS files ===")

def rewrite_css(css_text: str, css_url: str) -> str:
    def replace_url(m):
        raw = m.group(1).strip('\'"')
        if raw.startswith('data:'):
            return m.group(0)
        resolved = urljoin(css_url, raw).split('?')[0]
        if resolved in url_map:
            local_rel = url_map[resolved]
            # Make path relative from assets/css/
            if local_rel.startswith('assets/'):
                local_path = '../../' + local_rel
            else:
                local_path = local_rel
            return f"url('{local_path}')"
        return m.group(0)
    return re.sub(r'url\(\s*([^)]+)\s*\)', replace_url, css_text)

for url, local_name in CSS_URLS:
    css_file = ASSETS_CSS / local_name
    if not css_file.exists():
        continue
    css_text = css_file.read_text(encoding='utf-8', errors='replace')
    rewritten = rewrite_css(css_text, url.split('?')[0])
    css_file.write_text(rewritten, encoding='utf-8')
    print(f"  Rewritten: {local_name}")

# ── Read and update index.html ────────────────────────────────────────────────
print("\n=== Updating index.html ===")

html_file = BASE_DIR / "index.html"
html = html_file.read_text(encoding='utf-8')
original_html = html

# 1. Replace <link href="URL"> with local paths
def replace_link_href(m):
    full = m.group(0)
    url_raw = m.group(1)
    url_clean = url_raw.split('?')[0]
    if url_raw in url_map:
        return full.replace(url_raw, url_map[url_raw])
    if url_clean in url_map:
        return full.replace(url_raw, url_map[url_clean])
    return full

html = re.sub(r'href=[\'"](https://maquinadeebook\.online[^\'"]+)[\'"]', replace_link_href, html)

# 2. Replace <script src="URL"> with local paths
def replace_script_src(m):
    full = m.group(0)
    url_raw = m.group(1)
    url_clean = url_raw.split('?')[0]
    if url_raw in url_map:
        return full.replace(url_raw, url_map[url_raw])
    if url_clean in url_map:
        return full.replace(url_raw, url_map[url_clean])
    return full

html = re.sub(r'src=[\'"](https://maquinadeebook\.online[^\'"]+\.js[^\'"]*)[\'"]', replace_script_src, html)

# 3. Replace image src attributes (img src=)
def replace_img_src(m):
    full = m.group(0)
    url_raw = m.group(1)
    url_clean = url_raw.split('?')[0]
    local = url_map.get(url_raw) or url_map.get(url_clean)
    if local:
        return full.replace(url_raw, local)
    return full

html = re.sub(r'(?<=[= \t])src=[\'\"](https://maquinadeebook\.online[^\'\"]+\.(?:png|jpg|jpeg|gif|webp|svg))[\'\"]\s*', replace_img_src, html)

# 4. Replace data-src attributes (lazy loaded carousel images)
def replace_data_src(m):
    full = m.group(0)
    url_raw = m.group(1)
    url_clean = url_raw.split('?')[0]
    local = url_map.get(url_raw) or url_map.get(url_clean)
    if local:
        return full.replace(url_raw, local)
    return full

html = re.sub(r'data-src=[\'\"](https://maquinadeebook\.online[^\'\"]+\.(?:png|jpg|jpeg|gif|webp|svg))[\'\"]\s*', replace_data_src, html)

# 5. Replace srcset entries (space-separated URL w entries)
def replace_srcset_entry(m):
    url_raw = m.group(1)
    suffix = m.group(2)
    url_clean = url_raw.split('?')[0]
    local = url_map.get(url_raw) or url_map.get(url_clean)
    if local:
        return local + suffix
    return m.group(0)

html = re.sub(
    r'(https://maquinadeebook\.online/wp-content/uploads/[^\s,\'"]+\.(?:png|jpg|jpeg|gif|webp))((?:\s+\d+[wx])?)',
    replace_srcset_entry,
    html
)

# 6. Replace flaticon icons in img src
for ft_url, ft_name in FLATICON_URLS:
    html = html.replace(ft_url, f"assets/images/{ft_name}")

# 7. Update inline font-face declarations pointing to maquinadeebook
for url, local_name in FONT_URLS:
    html = html.replace(url, f"assets/fonts/{local_name}")

# 8. Update wp-emoji concatemoji URL
html = html.replace(
    r'https:\/\/maquinadeebook.online\/wp-includes\/js\/wp-emoji-release.min.js?ver=6.8.5',
    r'assets\/js\/wp-emoji-release.min.js'
)
# Also handle double-escaped version
html = html.replace(
    'https:\\/\\/maquinadeebook.online\\/wp-includes\\/js\\/wp-emoji-release.min.js?ver=6.8.5',
    'assets\\/js\\/wp-emoji-release.min.js'
)

# 9. Update elementorFrontendConfig assets URL
html = html.replace(
    r'"assets":"https:\/\/maquinadeebook.online\/wp-content\/plugins\/elementor\/assets\/"',
    r'"assets":"assets\/js\/"'
)
html = html.replace(
    r'"assets":"https:\/\/maquinadeebook.online\/wp-content\/plugins\/elementor-pro\/assets\/"',
    r'"assets":"assets\/js\/"'
)

# 10. Remove WordPress-specific link tags that are not needed
wp_noise_patterns = [
    r'<link rel="alternate"[^>]+maquinadeebook\.online[^>]*/>\n?',
    r'<link rel="https://api\.w\.org/"[^>]*/>\n?',
    r'<link rel="EditURI"[^>]*/>\n?',
    r'<link rel="shortlink"[^>]*/>\n?',
    r'<link rel="canonical"[^>]*/>\n?',
]
for pat in wp_noise_patterns:
    html = re.sub(pat, '', html)

# Write updated html
html_file.write_text(html, encoding='utf-8')
print(f"  index.html updated")

# Count replacements
remaining = len(re.findall(r'https://maquinadeebook\.online', html))
remaining_flat = len(re.findall(r'cdn-icons-png\.flaticon\.com', html))
print(f"\n  Remaining maquinadeebook.online refs: {remaining}")
print(f"  Remaining flaticon refs: {remaining_flat}")
if remaining > 0:
    # Show them
    for m in re.finditer(r'https://maquinadeebook\.online[^\s\'"<>]+', html):
        print(f"    {m.group(0)[:120]}")

# ── Create / update vercel.json ───────────────────────────────────────────────
print("\n=== Creating vercel.json ===")

vercel_config = {
    "cleanUrls": True,
    "trailingSlash": False,
    "routes": [
        {
            "src": "/assets/(.*)",
            "dest": "/assets/$1"
        },
        {
            "src": "/(.*)",
            "dest": "/index.html"
        }
    ]
}

vercel_file = BASE_DIR / "vercel.json"
vercel_file.write_text(json.dumps(vercel_config, indent=2), encoding='utf-8')
print(f"  vercel.json written")

# ── Final verification ────────────────────────────────────────────────────────
print("\n=== Verification ===")

# Count files downloaded
css_count = len(list(ASSETS_CSS.glob("*.css")))
js_count = len(list(ASSETS_JS.glob("*.js")))
font_count = len(list(ASSETS_FONTS.glob("*")))
img_count = len(list(ASSETS_IMAGES.glob("*")))

print(f"  CSS files:   {css_count}")
print(f"  JS files:    {js_count}")
print(f"  Font files:  {font_count}")
print(f"  Image files: {img_count}")

# Check for any missing images referenced in final HTML
with open(html_file, encoding='utf-8') as f:
    final_html = f.read()

local_imgs_in_html = re.findall(r'(?:src|data-src)=[\'"]assets/images/([^\'"]+)[\'"]', final_html)
missing = []
for img_name in local_imgs_in_html:
    if not (ASSETS_IMAGES / img_name).exists():
        missing.append(img_name)

if missing:
    print(f"\n  MISSING images ({len(missing)}):")
    for m in missing:
        print(f"    {m}")
else:
    print(f"  All {len(local_imgs_in_html)} img/data-src references have local files")

print("\n=== Done ===")
