"""Extract forecast data for ftd-exhibits.html (the FC const). Run inside the
container: docker exec -i <id> python3 - < this_file > forecast.json"""
import argparse
_ap = argparse.ArgumentParser()
_ap.add_argument("--ftd-csv", default="data/cns-fails-to-deliver/sec_fails_to_deliver_all.csv")
_ap.add_argument("--regsho-dir", default="data/regsho")
_args = _ap.parse_args()
FTD_CSV, REGSHO_DIR = _args.ftd_csv, _args.regsho_dir
import csv, bisect, json
from datetime import datetime

X = {}
with open(FTD_CSV, newline='', encoding='utf-8') as f:
    r = csv.reader(f); next(r)
    for row in r:
        if row[2] == 'XRT':
            d = f"{row[0][:4]}-{row[0][4:6]}-{row[0][6:8]}"
            X[d] = X.get(d, 0) + int(row[3])

def load(fn, col, fmt, symcol):
    per, alldates = {}, set()
    with open(fn) as fh:
        r = csv.reader(fh); next(r)
        for row in r:
            try: d = datetime.strptime(row[col], fmt).date()
            except (ValueError, IndexError): continue
            alldates.add(d); per.setdefault(row[symcol], set()).add(d)
    return per, alldates

nyse, nyse_all = load(REGSHO_DIR + '/nyse_regsho.csv', 1, '%Y-%m-%d', 3)
cal = sorted(nyse_all)

def streaks(dates):
    ds = sorted(dates); out, cur = [], [ds[0]]
    for p, t in zip(ds, ds[1:]):
        j = bisect.bisect_right(cal, p)
        if j < len(cal) and t == cal[j]: cur.append(t)
        else: out.append(cur); cur = [t]
    out.append(cur); return out

xs = streaks(nyse['XRT'])
live, done = xs[-1], xs[:-1]

lens = sorted(len(s) for s in done)
surv = [[n, sum(1 for L in lens if L >= n) / len(lens)] for n in range(1, max(lens) + 2)]

big = [s for s in done if len(s) >= 13]
fan = []
for k in range(1, 200):
    vals = sorted(X.get(str(s[k-1]), 0) for s in big if len(s) >= k)
    if len(vals) < 3: break
    q = lambda p: vals[min(int(p * len(vals)), len(vals) - 1)]
    fan.append([k, q(0.25), q(0.50), q(0.75), len(vals)])

live_path = [[i + 1, X.get(str(d), 0)] for i, d in enumerate(live) if str(d) <= max(X)]
age = len(live)
reached = [L for L in lens if L >= age]

print(json.dumps({'surv': surv, 'fan': fan, 'live': live_path,
                  'live_start': str(live[0]), 'live_days': age,
                  'cond': {'age': age, 'n_reached': len(reached), 'lengths': reached},
                  'lens': lens}, separators=(',', ':')))
