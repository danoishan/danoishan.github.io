"""Focused static-site checks. Standard library only; no external requests."""
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
import json
import re
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
ORIGIN = 'https://danoishan.github.io'

class Page(HTMLParser):
    def __init__(self, text):
        super().__init__(convert_charrefs=True)
        self.ids = []; self.refs = []; self.canonical = []; self.h1 = 0
        self.title = False; self.description = False; self.styles = []; self.noindex = False
        self.tables = 0; self.captions = 0; self.header_scopes = []
        self.feed(text)
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if a.get('id'): self.ids.append(a['id'])
        if tag == 'h1': self.h1 += 1
        if tag == 'title': self.title = True
        if tag == 'table': self.tables += 1
        if tag == 'caption': self.captions += 1
        if tag == 'th': self.header_scopes.append(a.get('scope'))
        if tag == 'meta' and a.get('name') == 'description' and a.get('content'): self.description = True
        if tag == 'meta' and a.get('name') == 'robots' and 'noindex' in a.get('content', ''): self.noindex = True
        if tag == 'link' and a.get('rel') == 'canonical': self.canonical.append(a.get('href'))
        if tag == 'link' and a.get('rel') == 'stylesheet': self.styles.append(a.get('href'))
        for attr in ['href', 'src']:
            if a.get(attr): self.refs.append(a[attr])

pages = {p.relative_to(ROOT).as_posix(): Page(p.read_text()) for p in ROOT.rglob('*.html') if '.git' not in p.parts}
errors = []; references = 0; fragments = 0
canonical_urls = set()
for name, page in pages.items():
    path = ROOT / name
    if len(page.ids) != len(set(page.ids)):
        errors.append(f'{name}: duplicate IDs {dict((k,v) for k,v in Counter(page.ids).items() if v>1)}')
    if page.tables != page.captions: errors.append(f'{name}: each data table needs a caption')
    if any(s not in ['col','row','colgroup','rowgroup'] for s in page.header_scopes): errors.append(f'{name}: table header scope is missing')
    verification = name.startswith('google')
    redirect = name == 'work/form-disappearing.html'
    if not verification and not redirect:
        canonical_path = '' if name == 'index.html' else name.removesuffix('index.html') if name.endswith('/index.html') else name
        expected = ORIGIN + '/' + canonical_path
        if page.h1 != 1: errors.append(f'{name}: expected one H1, found {page.h1}')
        if not page.title or not page.description: errors.append(f'{name}: missing title or description')
        if page.canonical != [expected]: errors.append(f'{name}: canonical differs: {page.canonical}')
        bases = [i for i,s in enumerate(page.styles) if s and s.endswith('styles-base.css')]
        overrides = [i for i,s in enumerate(page.styles) if s and s.endswith('styles.css')]
        if not bases or not overrides or bases[0] >= overrides[0]: errors.append(f'{name}: base CSS must load before overrides')
        if not page.noindex: canonical_urls.add(expected)
    for reference in page.refs:
        u = urlsplit(reference)
        if u.scheme and u.scheme not in ['http', 'https']: continue
        if u.netloc and u.netloc != 'danoishan.github.io': continue
        target = (ROOT / unquote(u.path.lstrip('/'))) if u.path.startswith('/') else path.parent / unquote(u.path)
        if not u.path: target = path
        target = target.resolve()
        if target.is_dir(): target = target / 'index.html'
        references += 1
        if not target.is_relative_to(ROOT) or not target.exists():
            errors.append(f'{name}: missing local target {reference}'); continue
        if u.fragment:
            fragments += 1
            target_name = target.relative_to(ROOT).as_posix()
            if target_name in pages and unquote(u.fragment) not in pages[target_name].ids:
                errors.append(f'{name}: missing fragment {reference}')

ns = {'s': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
urls = [el.text for el in ET.parse(ROOT/'sitemap.xml').findall('s:url/s:loc', ns)]
text_urls = (ROOT/'sitemap.txt').read_text().splitlines()
if set(urls) != canonical_urls or len(urls) != len(canonical_urls): errors.append('XML sitemap differs from indexable canonical pages')
if set(text_urls) != canonical_urls or len(text_urls) != len(canonical_urls): errors.append('Text sitemap differs from indexable canonical pages')
pdf=(ROOT/'Danoishan_Sinnathamby_Resume_2026.pdf').read_bytes()
if not pdf.startswith(b'%PDF-') or b'%%EOF' not in pdf[-1024:]: errors.append('Resume PDF is incomplete')
if '@import' in (ROOT/'styles.css').read_text(): errors.append('CSS override still blocks on an import')

def luminance(hex_color):
    rgb = [int(hex_color[i:i+2],16)/255 for i in [1,3,5]]
    linear = [c/12.92 if c <= .04045 else ((c+.055)/1.055)**2.4 for c in rgb]
    return sum(a*b for a,b in zip(linear,[.2126,.7152,.0722]))
contrast={}
for label,fg,bg in [('case_navigation_light','#565c65','#f3f0e8'),('fault_label_dark','#f1d6d0','#3a201c')]:
    light,dark=sorted([luminance(fg),luminance(bg)],reverse=True)
    ratio=(light+.05)/(dark+.05);contrast[label]=round(ratio,2)
    if ratio < 4.5: errors.append(f'{label}: contrast below 4.5:1')

if errors:
    print('\n'.join(errors)); raise SystemExit(1)
print(json.dumps({'html_files':len(pages),'canonical_pages':len(canonical_urls),'local_references':references,'fragment_references':fragments,'focused_contrast_ratios':contrast,'result':'pass'},indent=2))
