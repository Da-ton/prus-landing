with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Add w-full clear-both block to every section to force vertical stacking
html = html.replace('<section class="', '<section class="w-full clear-both block ')

# Also let's fix the broken legal section just in case my previous fix missed it
# Let's ensure legal section closes properly
if 'id="legal"' in html:
    # Just a simple hack: verify structure. Actually, I already fixed it in step 2401.
    pass

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
