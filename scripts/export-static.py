"""Export the current static build for a root domain or a subdirectory."""
from pathlib import Path
from html.parser import HTMLParser
import argparse, shutil, re
p=argparse.ArgumentParser()
p.add_argument('--output', required=True)
p.add_argument('--base-path', default='/')
args=p.parse_args()
root=Path(__file__).resolve().parent.parent
source=root/'dist'
target=Path(args.output).resolve()
base='/' + args.base_path.strip('/') + '/' if args.base_path.strip('/') else '/'
if not re.fullmatch(r'/[A-Za-z0-9_./-]*/?',base) or '..' in base:
    p.error('Use a plain URL directory path, such as /weir-interiors/.')
if target == source.resolve() or target.is_relative_to(source.resolve()) or source.resolve().is_relative_to(target):
    p.error('Output must be a separate directory, outside dist and its parents.')
if target.exists() and any(target.iterdir()):
    p.error('Output exists and is not empty; choose a new directory.')
shutil.copytree(source,target,dirs_exist_ok=True)
def path(value):
    return base+value.lstrip('/') if value.startswith('/') and not value.startswith('//') else value
for f in target.rglob('*.html'):
    text=f.read_text()
    text=re.sub(r'(href|src|data-full|action)="([^"<>]*)"',lambda m:m[1]+'="'+path(m[2])+'"',text)
    text=re.sub(r'srcset="([^"]+)"',lambda m:'srcset="'+', '.join(path(x.strip()) for x in m[1].split(','))+'"',text)
    f.write_text(text)

for f in target.rglob('*.css'):
    text=f.read_text()
    text=re.sub(r'''url\((['"]?)(/[^)'"\s]+)\1\)''',lambda m:'url('+m[1]+path(m[2])+m[1]+')',text)
    f.write_text(text)
htaccess=target/'.htaccess'
if htaccess.exists():htaccess.write_text(htaccess.read_text().replace('ErrorDocument 404 /404.html','ErrorDocument 404 '+base+'404.html'))
(target/'.nojekyll').write_text('')
print(f'Exported {len(list(target.rglob("index.html")))} pages to {target}; URL base: {base}')
