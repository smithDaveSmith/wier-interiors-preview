"""Check destinations, cross-page fragments and all referenced assets in the generated site."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import json,re
ROOT=Path(__file__).resolve().parent.parent
root=ROOT/'dist'
site_host=urlsplit(json.loads((ROOT/'source/site-settings.json').read_text())['origin']).netloc
files=list(root.rglob('*.html'));errors=[];count=0;destinations=set();external=set()
class Check(HTMLParser):
 def __init__(self):super().__init__();self.h1=0;self.ids=set();self.duplicates=[];self.refs=[];self.images=[];self.fields=[];self.labels=set();self.robot=False
 def handle_starttag(self,t,attrs):
  a=dict(attrs)
  if t=='h1':self.h1+=1
  if 'id' in a:
   if a['id'] in self.ids:self.duplicates.append(a['id'])
   self.ids.add(a['id'])
  if t=='meta' and a.get('name')=='robots':self.robot='noindex' in a.get('content','')
  if t=='label':self.labels.add(a.get('for'))
  if t in ['input','select','textarea']:self.fields.append(a.get('id'))
  if t=='img':self.images.append(a)
  for k in ['href','src','data-full','action']:
   if k in a:self.refs.append((k,a[k]))
  if 'srcset' in a:
   for candidate in a['srcset'].split(','):
    self.refs.append(('srcset',candidate.strip().split()[0]))
pages={}
for f in files:
 c=Check();c.feed(f.read_text());pages[f.resolve()]=c
for f,c in pages.items():
 name=str(f.relative_to(root.resolve()))
 if c.h1!=1:errors.append([name,'h1 count',c.h1])
 if not c.robot:errors.append([name,'missing noindex'])
 for ident in c.duplicates:errors.append([name,'duplicate id',ident])
 for x in c.fields:
  if x not in c.labels:errors.append([name,'unlabelled control',x])
 for image in c.images:
  if not all(k in image for k in ['width','height','alt']):errors.append([name,'missing image dimensions/alt'])
 for attr,ref in c.refs:
  u=urlsplit(ref)
  if u.scheme in ['data','mailto','tel']:continue
  if u.netloc and u.netloc!=site_host:external.add(ref);continue
  if u.scheme and u.scheme not in ['http','https']:errors.append([name,'unsupported URL',ref]);continue
  if not ref:errors.append([name,'empty destination',attr]);continue
  target=root/unquote(u.path).lstrip('/') if u.path.startswith('/') else f.parent/unquote(u.path) if u.path else f
  if target.is_dir():target=target/'index.html'
  target=target.resolve()
  if not target.is_relative_to(root.resolve()):errors.append([name,'destination outside site',ref]);continue
  if not target.is_file():errors.append([name,'missing destination',ref]);continue
  if u.fragment and (target not in pages or unquote(u.fragment) not in pages[target].ids):errors.append([name,'missing destination fragment',ref])
  count+=1;destinations.add('/'+str(target.relative_to(root.resolve())))
# CSS assets do not appear in HTML attributes (for example local font files).
css_refs=0
for f in root.rglob('*.css'):
 for match in re.finditer(r'url\(\s*[\'\"]?([^\s\'\"\)]+)[\'\"]?\s*\)',f.read_text()):
  ref=match[1];u=urlsplit(ref)
  if u.scheme or u.netloc:continue
  target=root/unquote(u.path).lstrip('/') if u.path.startswith('/') else f.parent/unquote(u.path)
  target=target.resolve()
  if not target.is_relative_to(root.resolve()) or not target.is_file():errors.append([str(f.relative_to(root)),'missing CSS asset',ref])
  else:css_refs+=1;destinations.add('/'+str(target.relative_to(root.resolve())))
try:
 from PIL import Image
 image_files=[f for f in (root/'assets').rglob('*') if f.is_file()]
 for f in image_files:
  try:
   with Image.open(f) as im:im.verify()
  except Exception as ex:errors.append([str(f),'image decode',str(ex)])
 image_check='passed'
except ImportError:image_check='skipped: Pillow unavailable'
result={'content_pages':len(list(root.rglob('index.html'))),'404_page':(root/'404.html').exists(),'internal_references_checked':count,'css_asset_references_checked':css_refs,'unique_local_destinations':len(destinations),'external_destinations':sorted(external),'gallery_images':len(json.loads((ROOT/'source/gallery-data.json').read_text())),'image_decode_check':image_check,'errors':errors}
print(json.dumps(result,indent=2));assert not errors
(ROOT/'docs').mkdir(exist_ok=True)
(ROOT/'docs/link-checks.json').write_text(json.dumps(result,indent=2)+'\n')
