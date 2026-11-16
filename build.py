"""Produce a buildless development preview and a fully self-contained HTML."""
from pathlib import Path
from decimal import Decimal
import json, base64
ROOT=Path(__file__).parent
DIST=ROOT/'dist'
data=json.loads((ROOT/'catalogue.json').read_text())
additions = json.loads((ROOT / 'catalogue-additions.json').read_text(encoding='utf-8'))
categories = {category['id']: category for category in data['categories']}
product_ids = {item['id'] for item in data['products']}

for item in additions:
    if item['id'] in product_ids:
        raise ValueError(f"Duplicate product ID: {item['id']}")
    product_ids.add(item['id'])
    category = categories[item['category']]
    data['products'].append({
        **item,
        'division': category['division'],
        'art': category['art'],
        'min': None,
        'max': None,
        'unit': 'pack of 100' if category['id'] == 'visiting-cards' else 'item',
        'isNew': True,
    })

products = {item['id']: item for item in data['products']}
for product_id, item in products.items():
    price = item.get('price')
    regular_price = item.get('regularPrice')
    for amount in (price, regular_price):
        if amount is None:
            continue
        if type(amount) not in (int, float) or not (0 < amount < float('inf')) or Decimal(str(amount)).as_tuple().exponent < -2:
            raise ValueError(f'Invalid price for {product_id}. Use a positive INR amount with up to two decimal places.')
    if regular_price is not None and (price is None or regular_price <= price):
        raise ValueError(f'Regular price for {product_id} must be above its selling price.')
    if 'gstExtra' in item and type(item['gstExtra']) is not bool:
        raise ValueError(f'gstExtra for {product_id} must be true or false.')
    if item.get('gstExtra') and price is None:
        raise ValueError(f'Selling price required to show GST for {product_id}.')

photo_manifest = json.loads((ROOT / 'product-photos.json').read_text(encoding='utf-8'))
photo_sheets = {}
photographed = set()

for sheet in photo_manifest['sheets']:
    key = sheet['id']
    if key in photo_sheets:
        raise ValueError(f'Duplicate photo sheet: {key}')
    if not (DIST / sheet['src']).is_file():
        raise FileNotFoundError(sheet['src'])
    if len(sheet['products']) != sheet['columns'] * sheet['rows']:
        raise ValueError(f'Photo sheet {key} must have one product per tile')
    photo_sheets[key] = {
        field: sheet[field] for field in ('src', 'width', 'height', 'columns', 'rows')
    }
    for index, product_id in enumerate(sheet['products']):
        if product_id in photographed:
            raise ValueError(f'Multiple photos assigned to {product_id}')
        products[product_id]['photo'] = {'sheet': key, 'index': index}
        photographed.add(product_id)

missing = products.keys() - photographed
if missing:
    raise ValueError(f'Missing product photos: {", ".join(sorted(missing))}')
data['photoSheets'] = photo_sheets

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
for sheet in photo_sheets.values():
    src = sheet['src']
    encoded = base64.b64encode((DIST / src).read_bytes()).decode()
    standalone = standalone.replace(json.dumps(src), json.dumps(f'data:image/webp;base64,{encoded}'), 1)
(ROOT/'INKBYTE-preview.html').write_text(standalone)
print(f'Built {len(data["products"])} products; standalone HTML: {(ROOT/"INKBYTE-preview.html").stat().st_size:,} bytes')
