import re
import json

with open(r'C:\Users\61981\.gemini\antigravity\scratch\bruno_app\web\static\js\index.33a912fb.js', 'r', encoding='utf-8') as f:
    s = f.read()

# Patterns that match UI strings:
# children: "..."
# label: "..."
# title: "..."
# placeholder: "..."
# tooltip: "..."
# heading: "..."

patterns = [
    r'children:\s*["\']([^"\'\n\r{}]{2,100})["\']',
    r'label:\s*["\']([^"\'\n\r{}]{2,100})["\']',
    r'title:\s*["\']([^"\'\n\r{}]{2,100})["\']',
    r'placeholder:\s*["\']([^"\'\n\r{}]{2,100})["\']',
    r'heading:\s*["\']([^"\'\n\r{}]{2,100})["\']',
    r'tooltip:\s*["\']([^"\'\n\r{}]{2,100})["\']',
    r'"aria-label":\s*["\']([^"\'\n\r{}]{2,100})["\']',
]

extracted = set()
for pat in patterns:
    for m in re.finditer(pat, s):
        val = m.group(1).strip()
        # filter out css, classes, ids, hex colors, code snippets, urls, etc.
        if not val:
            continue
        if re.match(r'^(#|http|rgba?|data:|var\(|d:|M\d|\.|\/|calc|rgb|\d+$)', val):
            continue
        if any(c in val for c in ['{', '}', ';', '=>', '<', '>', '$', '\\']):
            continue
        if len(val.split()) > 15:
            continue
        # Check if contains letters
        if not re.search(r'[a-zA-Z]', val):
            continue
        extracted.add(val)

print(f"Total candidate UI strings extracted: {len(extracted)}")

with open(r'C:\Users\61981\.gemini\antigravity\scratch\all_ui_strings.json', 'w', encoding='utf-8') as f:
    json.dump(sorted(list(extracted)), f, indent=2, ensure_ascii=False)
