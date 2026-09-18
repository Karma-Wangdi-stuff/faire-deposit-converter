"""Build a single-file offline copy of index.html (CDN scripts inlined, web fonts dropped)."""
import re
import sys
import urllib.request
from pathlib import Path

HERE = Path(__file__).parent
out = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.home() / "Desktop" / "Faire_Deposit_Converter_Offline.html"
html = (HERE / "index.html").read_text()


def inline(m):
    src = urllib.request.urlopen(m.group(1), timeout=30).read().decode()
    return "<script>" + src.replace("</script", "<\\/script") + "</script>"


html, n = re.subn(r'<script src="(https://[^"]+)"></script>', inline, html)
assert n == 3, f"expected 3 CDN scripts, inlined {n}"
# ponytail: fonts fall back to sans-serif/monospace/serif offline, embed woff2 if looks matter
html = re.sub(r'<link[^>]+fonts\.(googleapis|gstatic)\.com[^>]*>\n?', "", html)
assert "https://" not in re.sub(r'xmlns="http://www.w3.org/2000/svg"', "", html).split("<script>")[0]
out.write_text(html)
print(out, f"{out.stat().st_size // 1024} KB")
