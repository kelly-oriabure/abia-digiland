import re
from pathlib import Path

ROOT = Path('.')
BASE = ROOT / 'partials' / 'base.html'
base_template = BASE.read_text(encoding='utf-8')

for page in sorted(ROOT.glob('*.html')):
    text = page.read_text(encoding='utf-8')

    title_match = re.search(r'<title>(.*?)</title>', text, re.DOTALL | re.IGNORECASE)
    title = title_match.group(1).strip() if title_match else 'DIGILAND ABIA'

    body_match = re.search(r'<body[^>]*class="([^"]*)"', text, re.DOTALL | re.IGNORECASE)
    body_class = body_match.group(1) if body_match else 'bg-surface font-body text-on-surface'

    base = base_template.replace('{{PAGE_TITLE}}', title).replace('{{BODY_CLASS}}', body_class)

    text = re.sub(
        r'\s*(?:<!--\s*(?:Top|AppBar|TopAppBar|Top Navigation)[^>]*-->\s*)?<div hx-get="partials/(?:header|topbar)\.html"[^>]*>\s*</div>',
        '',
        text,
        flags=re.DOTALL | re.IGNORECASE,
    )
    text = re.sub(
        r'\s*(?:<!--\s*(?:Top|AppBar|TopAppBar|Top Navigation)[^>]*-->\s*)?<nav[^>]*fixed top-0[^>]*>.*?</nav>',
        '',
        text,
        count=1,
        flags=re.DOTALL | re.IGNORECASE,
    )

    pattern = re.compile(
        r'<!DOCTYPE html>\s*<html[^>]*>\s*<head>.*?</head>\s*<body[^>]*>',
        re.DOTALL | re.IGNORECASE,
    )
    new_text, count = pattern.subn(base, text, count=1)
    if count == 0:
        print(f'{page.name}: body pattern not found')
        continue

    page.write_text(new_text, encoding='utf-8')
    print(f'{page.name}: rebuilt')
