"""Produce a buildless development preview and a fully self-contained HTML."""
from pathlib import Path
import json, base64
ROOT=Path(__file__).parent
DIST=ROOT/'dist'
data=json.loads((ROOT/'catalogue.json').read_text())
template=(DIST/'template.html').read_text()
html=template.replace('__CATALOGUE__',json.dumps(data,ensure_ascii=False).replace('<','\\u003c'))
(DIST/'index.html').write_text(html)
standalone=html.replace('<link rel="stylesheet" href="styles.css">','<style>\n'+(DIST/'styles.css').read_text()+'\n</style>')
for script in ('artwork.js','app.js'):
    standalone=standalone.replace(f'<script src="{script}"></script>','<script>\n'+(DIST/script).read_text()+'\n</script>')
for filename,mime in [('hero.webp','image/webp'),('inkbyte-logo.png','image/png')]:
    asset=DIST/'assets'/filename
    if asset.exists():
        standalone=standalone.replace('src="assets/'+filename+'"','src="data:'+mime+';base64,'+base64.b64encode(asset.read_bytes()).decode()+'"')
(ROOT/'INKBYTE-preview.html').write_text(standalone)
print(f'Built {len(data["products"])} products; standalone HTML: {(ROOT/"INKBYTE-preview.html").stat().st_size:,} bytes')
