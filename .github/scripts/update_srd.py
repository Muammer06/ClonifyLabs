#!/usr/bin/env python3

import os
import re

# SRD dosyasının yolu
srd_path = 'docs/SRD.md'

# Yeni değişiklik içeriğini oku
with open('changes.md', 'r', encoding='utf-8') as f:
    changes_content = f.read()

# SRD dosyasını oku
with open(srd_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Değişiklik bölümünü güncelle
pattern = r'<!-- LATEST_CODE_CHANGES -->.*?<!-- END_LATEST_CODE_CHANGES -->'
replacement = f'<!-- LATEST_CODE_CHANGES -->\n{changes_content}\n<!-- END_LATEST_CODE_CHANGES -->'
updated_content = re.sub(pattern, replacement, content, flags=re.DOTALL)

# Dosyayı güncelle
with open(srd_path, 'w', encoding='utf-8') as f:
    f.write(updated_content)

print(f"{srd_path} dosyası güncellendi.")
