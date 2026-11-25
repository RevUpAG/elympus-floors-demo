#!/usr/bin/env python3
"""src.html + img/ -> index.html (one self-contained file). Fails if a link, phone or anchor is wrong."""
import base64, json, pathlib, re
here = pathlib.Path(__file__).parent
h = (here / 'src.html').read_text(encoding='utf8')
MIME = {'.webp': 'image/webp', '.png': 'image/png', '.jpg': 'image/jpeg'}
def inline(m):
    f = here / 'img' / m.group(2)
    return f'{m.group(1)}="data:{MIME[f.suffix]};base64,{base64.b64encode(f.read_bytes()).decode()}"'
out = re.sub(r'\b(src|href)="img/([^"]+)"', inline, h)
assert '"img/' not in out, 'image left outside the file'
tels, was = set(re.findall(r'(?:tel|sms):(\+\d+)', h)), set(re.findall(r'wa\.me/(\d+)', h))
assert tels == {'+19737529896'} and was == {'19737529896'}, (tels, was)
ids = set(re.findall(r'\bid="([^"]+)"', h))
missing = [a for a in re.findall(r'href="#([^"]+)"', h) if a not in ids]
assert not missing, missing
need = set(re.findall(r'name="need" value="([^"]+)"', h)); svc = set(re.findall(r'data-svc="([^"]+)"', h))
assert need == svc, need ^ svc
json.loads(re.search(r'ld\+json">(.*?)</script>', h, re.S).group(1))
(here / 'index.html').write_text(out, encoding='utf8')
print('index.html', round(len(out) / 1024), 'KB')
