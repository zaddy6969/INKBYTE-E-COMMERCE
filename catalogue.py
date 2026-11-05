"""Read the supplied workbook without editing it; create the preview catalogue."""
import json, re, sys, zipfile, xml.etree.ElementTree as E
from pathlib import Path

ROOT=Path(__file__).parent
NS={'m':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
SOURCE=Path(sys.argv[1]) if len(sys.argv)>1 else ROOT/'sources'/'Web-planning.xlsx'
if not SOURCE.is_file():
    raise SystemExit('Pass your source workbook: python catalogue.py /absolute/path/to/workbook.xlsx')
with zipfile.ZipFile(SOURCE) as z:
    strings=[''.join(t.text or '' for t in si.findall('.//m:t',NS)) for si in E.fromstring(z.read('xl/sharedStrings.xml')).findall('m:si',NS)]
    sheets=[]
    for sheet in (1,2):
        rows={}
        for row in E.fromstring(z.read(f'xl/worksheets/sheet{sheet}.xml')).findall('.//m:row',NS):
            cells={}
            for c in row.findall('m:c',NS):
                v=c.find('m:v',NS)
                value=v.text if v is not None else ''
                if c.get('t')=='s': value=strings[int(value)]
                cells[re.sub(r'\d','',c.get('r'))]=value
            rows[int(row.get('r'))]=cells
        sheets.append(rows)

categories=[]; products=[]
def group(key,name,division,art):
    categories.append(dict(id=key,name=name,division=division,art=art))
def add(sheet,row,category,name=None,price=None):
    c=next(c for c in categories if c['id']==category)
    raw=sheets[sheet-1][row].get('B','').strip()
    original_price=sheets[sheet-1][row].get('C','')
    name=name or raw
    pr=price if price is not None else original_price
    nums=[int(v) for v in re.findall(r'\d+',pr)]
    minimum=nums[0] if nums else None
    maximum=nums[1] if len(nums)>1 else None
    products.append(dict(id=f'{"g" if sheet==1 else "p"}{row:02}',name=name,category=category,division=c['division'],art=c['art'],min=minimum,max=maximum,unit='pack of 100' if category=='visiting-cards' else 'item',source=dict(sheet='Corporate gift' if sheet==1 else 'printing',row=row,description=raw,market_price=original_price,our_price=None)))

singles=[('pens','Premium pens','pen',2,'Premium metal pen'),('notebooks','Notebooks & diaries','notebook',3,'Classic notebook'),('tumblers','Tumblers','tumbler',4,'Insulated coffee tumbler'),('keychains','Keychains','keychain',5,'Premium keychain'),('phone-stands','Phone stands','stand',6,'Mobile stand / phone holder'),('cleaning-kits','Cleaning kits','cleaning',7,'Laptop & mobile cleaning kit'),('eco-bags','Eco-friendly bags','bag',8,'Eco-friendly jute / canvas bag'),('mugs','Coffee mugs','mug',9,'Branded coffee mug'),('plants','Desk plants','plant',10,'Mini plant / succulent'),('bottles','Water bottles','bottle',11,'Personalised water bottle')]
for key,title,art,row,name in singles:
    group(key,title,'corporate',art);add(1,row,key,name)
group('corporate-hampers','Corporate gift hampers','corporate','hamper')
for row,name,price in [(13,'Diary & pen gift set','250-450'),(14,'Diary, pen & bottle gift set','400-800'),(15,'Diary, pen & keychain gift set','350-550'),(16,'Diary, pen & coffee cup gift set','450-600'),(17,'Diary, pen & tumbler gift set','700-1200')]:add(1,row,'corporate-hampers',name,price)
group('festival-hampers','Festival gift hampers','corporate','festival')
for row,name in [(19,'Four dry fruits premium box'),(20,'Two dry fruits & coffee cup box'),(21,'Six dry fruits premium box'),(22,'Two dry fruits & tumbler box'),(23,'Three dry fruits gift box')]:add(1,row,'festival-hampers',name)
group('t-shirts','T-shirts','corporate','shirt')
for row,name in [(26,'Round neck T-shirt'),(27,'Polo T-shirt'),(28,'Oversized T-shirt'),(29,'V-neck T-shirt'),(30,'Sleeveless T-shirt / tank top'),(31,'Sports T-shirt')]:add(1,row,'t-shirts',name)
group('calendars','Calendars','corporate','calendar')
for row in range(34,41):add(1,row,'calendars')
group('bags','Tote & jute bags','corporate','bag')
for row in range(44,47):add(1,row,'bags')
group('hoodies','Sweatshirts & hoodies','corporate','hoodie');add(1,48,'hoodies')
group('wedding-cards','Wedding invitations','printing','wedding')
for row in range(3,15):add(2,row,'wedding-cards')
group('flyers','Flyers','printing','flyer')
flyers=[('Single-sided flyer','2-4'),('Double-sided flyer','3-12'),('DL flyer','3-10'),('A4 flyer','5-20'),('A3 flyer','10-35'),('Tri-fold flyer','8-30'),('Bi-fold flyer','7-25'),('Die-cut flyer','15-60'),('Event / promotional flyer','5-30'),('Menu flyer','8-40'),('Real estate flyer','8-40'),('Corporate flyer','8-50')]
for row,(name,price) in enumerate(flyers,16):add(2,row,'flyers',name,price)
group('catalogues','Catalogues','printing','catalogue');add(2,28,'catalogues','Custom product catalogue')
group('visiting-cards','Visiting cards','printing','cards')
for row in range(32,45):add(2,row,'visiting-cards')
for key,title,art,row in [('letterheads','Letterheads','letterhead',46),('stamps','Rubber stamps','stamp',48),('envelopes','Envelopes','envelope',50),('stickers','Stickers & labels','sticker',52)]:group(key,title,'printing',art);add(2,row,key,title)
data=dict(categories=categories,products=products,source='Web planning.xlsx',currency='INR',currency_note='INR assumed for the preview; confirm before publication.',pricing_note='Market reference ranges supplied in the workbook. Our price is blank for all products. No selling prices or discounts have been invented.')
(ROOT/'catalogue.json').write_text(json.dumps(data,ensure_ascii=False,indent=2))
print(f'{len(products)} products in {len(categories)} categories; {sum(p["min"] is None for p in products)} need pricing; workbook unchanged.')
