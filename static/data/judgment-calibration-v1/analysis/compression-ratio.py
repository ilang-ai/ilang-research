#!/usr/bin/env python3
"""
Measure token counts across three versions (zh / en / ilang) of the same content.
Run after all three versions are generated.
"""
import os

def count_chars(path):
    with open(path) as f:
        return len(f.read())

def estimate_tokens(text_len, lang):
    """Rough token estimate: zh ~1.5 chars/token, en ~4 chars/token, ilang ~3 chars/token"""
    ratios = {'zh': 1.5, 'en': 4.0, 'ilang': 3.0}
    return int(text_len / ratios.get(lang, 3.0))

for fname in ['feishu-tuning-log.md', 'wecom-calibration-log.md', 'wecom-dialogue-full.md']:
    print(f"\n=== {fname} ===")
    for lang in ['zh', 'en', 'ilang']:
        ext = '.ilang' if lang == 'ilang' else '.md'
        path = f'../{lang}/{fname.replace(".md", ext)}'
        if os.path.exists(path):
            chars = count_chars(path)
            tokens = estimate_tokens(chars, lang)
            print(f"  {lang:6s}: {chars:>10,} chars  ~{tokens:>8,} tokens")
        else:
            print(f"  {lang:6s}: (not yet generated)")
