import re, sys, collections

d = open('README.md').read()
ok = True


def chk(c, m):
    global ok
    if not c:
        ok = False
        print('FAIL', m)
    else:
        print('ok  ', m)


chk(d.count('<div') == d.count('</div>'), f"div balanced ({d.count('<div')}/{d.count('</div>')})")
chk(d.count('<table>') == d.count('</table>'), f"table balanced ({d.count('<table>')}/{d.count('</table>')})")
chk(d.count('<!-- BLOG-POST-LIST:START -->') == 1, 'blog marker START x1')
chk(d.count('<!-- BLOG-POST-LIST:END -->') == 1, 'blog marker END x1')
chk(not re.findall(r'\]\([^)]*$', d, re.M), 'no unterminated link paren')
chk(d.count('<a ') == d.count('</a>'), f"a balanced ({d.count('<a ')}/{d.count('</a>')})")

non_html = re.sub(r'<[^>]+>', '', d)
chk('src=' not in non_html, 'no stripped-HTML artifacts (src=)')
chk('href=' not in non_html, 'no stripped-HTML artifacts (href=)')

alts = re.findall(r'!\[([^\]]*)\]\(([^)]+)\)', d)
chk(all(a.strip() for a, _ in alts), f'all {len(alts)} images have alt text')

hrefs = re.findall(r'\]\(([^)]+)\)', d)
rel = [h for h in hrefs if not h.startswith(('http', 'mailto:'))]
chk(not rel, f'all {len(hrefs)} links absolute; bad={rel}')

tables = re.findall(r'((?:^\|.*\|$\n?)+)', d, re.M)
for i, t in enumerate(tables, 1):
    widths = collections.Counter(r.count('|') for r in t.strip().split('\n'))
    chk(len(widths) == 1, f'table {i}: all rows same column count {dict(widths)}')

print('headings:')
for h in re.findall(r'^#{1,6} .+', d, re.M):
    print('  ', h)
print('size', len(d), 'bytes')
dup = [k for k, v in collections.Counter(hrefs).items() if v > 1]
print('repeated links:', dup)
sys.exit(0 if ok else 1)
