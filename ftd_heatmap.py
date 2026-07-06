#!/usr/bin/env python3
# ftd_heatmap.py
#
# Plot a fails‑to‑deliver heat‑map for selected tickers over a chosen period.
#
# EXAMPLE
#   python ftd_heatmap.py data/cns-fails-to-deliver/sec_fails_to_deliver_all.csv              \
#       -t GME XRT BABA CHWY KOSS                  \
#       --freq W --log                             \
#       --from 2021‑01‑01 --to 2023‑12‑31          \
#       --width 18
#
# REQUIREMENTS: pandas, matplotlib (pip install pandas matplotlib)

import argparse, numpy as np, pandas as pd, matplotlib.pyplot as plt


# ── CLI ────────────────────────────────────────────────────────────────────
def cli() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Visualise SEC FTD volumes for a basket of tickers.")
    p.add_argument("csv", help="raw SEC FTD file (huge *.csv)")
    p.add_argument("-t", "--tickers", nargs="+", required=True,
                   help="tickers to plot (e.g. GME XRT …)")
    p.add_argument("--freq", choices=["D", "W", "M"], default="D",
                   help="aggregate by D‑ay, W‑eek, or M‑onth (default D)")
    p.add_argument("--log", action="store_true",
                   help="use log₁₀(fails+1) colour scale")
    p.add_argument("--width", type=int, default=14,
                   help="figure width in inches (default 14)")
    p.add_argument("--from", dest="start", type=str,
                   help="first settlement date YYYY‑MM‑DD to include")
    p.add_argument("--to", dest="end", type=str,
                   help="last settlement date YYYY‑MM‑DD to include (inclusive)")
    return p.parse_args()


args = cli()

# ── LOAD ───────────────────────────────────────────────────────────────────
use_cols = ["settlement_date", "symbol", "quantity_fails"]
df = pd.read_csv(args.csv, usecols=use_cols, parse_dates=["settlement_date"],
                 low_memory=False)
df = df[df.symbol.isin(args.tickers)]

# optional date window
if args.start:
    df = df[df["settlement_date"] >= pd.Timestamp(args.start)]
if args.end:
    df = df[df["settlement_date"] <= pd.Timestamp(args.end)]

# ── AGGREGATE ──────────────────────────────────────────────────────────────
pivot = (df.groupby(["settlement_date", "symbol"])["quantity_fails"]
           .sum()
           .unstack(fill_value=0)
           .sort_index())             # daily

if args.freq != "D":
    pivot = pivot.resample(args.freq).sum()

# drop all‑zero periods (optional; comment out if you want to keep them)
pivot = pivot[pivot.sum(axis=1) > 0]

data = np.log10(pivot + 1) if args.log else pivot

# ── PLOT ───────────────────────────────────────────────────────────────────
fig_h = len(args.tickers) * 0.5 + 2
fig, ax = plt.subplots(figsize=(args.width, fig_h))
im = ax.imshow(data.T, aspect="auto", interpolation="nearest")

# y‑axis
ax.set_yticks(range(len(args.tickers)))
ax.set_yticklabels(args.tickers)

# x‑axis label thinning
n_cols = data.shape[0]
max_labels = args.width * 6             # ≈ characters that fit
step = max(1, n_cols // max_labels)
idx = np.arange(0, n_cols, step)
fmt = "%Y‑%m‑%d" if args.freq == "D" else "%Y‑%m"
ax.set_xticks(idx)
ax.set_xticklabels(pivot.index[idx].strftime(fmt), rotation=45,
                   ha="right", fontsize=8)

title_freq = {"D": "Daily", "W": "Weekly", "M": "Monthly"}[args.freq]
ax.set_title(f"FTD Volume Heatmap ({title_freq}) – {' vs '.join(args.tickers)}")

cbar = fig.colorbar(im, ax=ax, pad=0.02)
cbar.set_label("log₁₀(fails+1)" if args.log else "Fails to deliver")

fig.tight_layout()
plt.show()
