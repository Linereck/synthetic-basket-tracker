"""Extract chart data for ftd-exhibits.html (the DATA const). Run inside the
container: docker exec -i <id> python3 - < this_file > exhibits.json"""
import argparse
_ap = argparse.ArgumentParser()
_ap.add_argument("--ftd-csv", default="data/cns-fails-to-deliver/sec_fails_to_deliver_all.csv")
_ap.add_argument("--regsho-dir", default="data/regsho")
_args = _ap.parse_args()
FTD_CSV, REGSHO_DIR = _args.ftd_csv, _args.regsho_dir
import csv, bisect, json
from datetime import datetime, date

ftd = {'GME': {}, 'XRT': {}}
with open(FTD_CSV, newline='', encoding='utf-8') as f:
    r = csv.reader(f); next(r)
    for row in r:
        if len(row) >= 4 and row[2] in ftd:
            d = f"{row[0][:4]}-{row[0][4:6]}-{row[0][6:8]}"
            ftd[row[2]][d] = ftd[row[2]].get(d, 0) + int(row[3])

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
cal = sorted(nyse_all)  # per-exchange publication calendar (NYSE)

def streaks(dates):
    ds = sorted(dates); out, cur = [], [ds[0]]
    for p, t in zip(ds, ds[1:]):
        j = bisect.bisect_right(cal, p)
        if j < len(cal) and t == cal[j]: cur.append(t)
        else: out.append(cur); cur = [t]
    out.append(cur); return out

xs = streaks(nyse['XRT'])
gs = streaks(nyse['GME'])
X = ftd['XRT']

w0, w1 = '2020-11-16', '2021-03-31'
mig = {
  'gme':  sorted([d, q] for d, q in ftd['GME'].items() if w0 <= d <= w1),
  'xrt':  sorted([d, q] for d, q in ftd['XRT'].items() if w0 <= d <= w1),
  'gme_list': sorted(str(d) for s in gs for d in s if w0 <= str(d) <= w1),
  'xrt_list': sorted(str(d) for s in xs for d in s if w0 <= str(d) <= w1),
}
hist = sorted([d, q] for d, q in X.items() if d >= '2019-10-01')
bands = [{'s': str(s[0]), 'e': str(s[-1]), 'n': len(s)} for s in xs]

cliff = []
for s in xs:
    if len(s) < 13 or str(s[-1]) > max(X): continue
    endi = bisect.bisect_right(cal, s[-1])
    pre  = sum(X.get(str(d), 0) for d in s[-3:]) // 3
    post_days = cal[endi:endi+5]
    post = sum(X.get(str(d), 0) for d in post_days) // max(len(post_days), 1)
    cliff.append({'s': str(s[0]), 'e': str(s[-1]), 'n': len(s), 'pre': pre, 'post': post})

print(json.dumps({'mig': mig, 'hist': hist, 'bands': bands, 'cliff': cliff}, separators=(',', ':')))
