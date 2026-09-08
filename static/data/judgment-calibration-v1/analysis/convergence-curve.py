#!/usr/bin/env python3
"""
Convergence curve: operator tuning-event frequency over time, with the
`adopted` label breakdown so label coverage is always visible.

Reads ../structured/tuning-events.jsonl. Prints:
  - events per day (🔧 tuning vs 💬 directive)
  - labeled subset per day: adopted=1 / adopted=0 / null
  - first-half vs second-half frequency (is the system converging?)

`adopted` is a lexicon heuristic (see README). Rows with adopted=null are
reported, never dropped silently.
"""
import json
from collections import Counter, defaultdict

events = []
with open('../structured/tuning-events.jsonl', encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        if line:
            events.append(json.loads(line))

daily = defaultdict(lambda: Counter())
for e in events:
    day = e['timestamp'][:10]
    daily[day]['total'] += 1
    daily[day][e['type']] += 1
    a = e.get('adopted')
    daily[day]['adopted=1' if a == 1 else 'adopted=0' if a == 0 else 'null'] += 1

dates = sorted(daily)
# ASCII-only output so it runs on Windows consoles that are not UTF-8
print(f"{'Date':<12}{'total':>6}{'tune':>5}{'dir':>5}   {'a=1':>4}{'a=0':>5}{'null':>6}   cumulative")
print("-" * 70)
cum = 0
for d in dates:
    c = daily[d]
    cum += c['total']
    bar = "#" * c['total']
    print(f"{d:<12}{c['total']:>6}{c['tuning']:>5}{c['directive']:>5}   "
          f"{c['adopted=1']:>4}{c['adopted=0']:>5}{c['null']:>6}   {cum:>4}  {bar}")

total = sum(daily[d]['total'] for d in dates)
lab1 = sum(daily[d]['adopted=1'] for d in dates)
lab0 = sum(daily[d]['adopted=0'] for d in dates)
null = sum(daily[d]['null'] for d in dates)
print(f"\nTotal: {total} operator messages over {len(dates)} active days")
print(f"Labeled: {lab1 + lab0} ({100.0 * (lab1 + lab0) / total:.0f}%)  "
      f"adopted=1: {lab1}  adopted=0: {lab0}  null: {null}")
peak = max(dates, key=lambda d: daily[d]['total'])
print(f"Peak day: {peak} ({daily[peak]['total']} messages)")

if len(dates) >= 4:
    half = len(dates) // 2
    first = sum(daily[d]['total'] for d in dates[:half])
    second = sum(daily[d]['total'] for d in dates[half:])
    print(f"\nFirst half:  {first} messages")
    print(f"Second half: {second} messages")
    if second > first:
        print("WARNING: frequency INCREASING - still learning, or new features under calibration")
    else:
        print("OK: frequency decreasing - converging")
    # adoption rate on the labeled subset only, so the trend is not an artifact of coverage
    def rate(ds):
        one = sum(daily[d]['adopted=1'] for d in ds)
        zero = sum(daily[d]['adopted=0'] for d in ds)
        return (one, zero, (100.0 * one / (one + zero)) if (one + zero) else float('nan'))
    o1, z1, r1 = rate(dates[:half])
    o2, z2, r2 = rate(dates[half:])
    print(f"Adoption rate (labeled rows only): first half {r1:.0f}% ({o1}/{o1 + z1}), "
          f"second half {r2:.0f}% ({o2}/{o2 + z2})")
