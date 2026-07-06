# Synthetic Short Basket Tracker

**Identify and monitor synthetic short exposure through FTD clustering, timing convergence, and systemic basket risk.**

## Overview

This project maps relationships between GME and its wrapper instruments (e.g., XRT, CHWY, BABA) by joining:

- SEC CNS failures-to-deliver (2019 to present, consolidated in the
  [cns-fails-to-deliver](https://github.com/Linereck/cns-fails-to-deliver) data repository)
- Reg SHO threshold-list membership from NYSE, NASDAQ, and CBOE (`data/regsho/`)

The goal is to uncover synthetic basket activity, predict unwind windows, and provide timing signals for potential short pressure events.

## Published analysis

Interactive results, hosted from this repository via GitHub Pages:

- **[Interactive exhibits](https://linereck.github.io/synthetic-short-basket-tracker/exhibits.html)** -
  the January 2021 GME-to-XRT fails handoff, six years of XRT threshold-list residencies,
  the inverted close-out cliff, and a conditional forecast of the live residency.
- **[Findings report](https://linereck.github.io/synthetic-short-basket-tracker/report.html)** -
  the written analysis: what the data proves and cannot prove, the 2024 echo, and the
  design of an event-conditioned predictive model.

Headline findings so far:

- XRT sat on the Reg SHO threshold list for 37% of all trading days since October 2019;
  its longest residency ran at least 187 days against a rule designed to force exit in 13.
- January 2021: GME fails peak on the 26th, the buy button dies on the 28th, XRT posts its
  own fails peak and enters the threshold list on the 29th; GME leaves the list on
  February 3rd and has not returned since.
- Fails are suppressed at residency tails (to satisfy the 5-clean-day exit test) and
  explode up to 85x within five days of exiting: deliveries track the rule's measurement
  windows, not economic settlement.

## Repository layout

```
docs/                      GitHub Pages site (exhibits, report)
analysis/                  extraction scripts that regenerate the exhibit data
data/cns-fails-to-deliver  FTD dataset (git submodule, CSV in Git LFS)
data/regsho                threshold-list CSVs (NYSE, NASDAQ, CBOE)
ftd_heatmap.py             FTD volume heatmap for a basket of tickers
```

## Reproducing

```
git clone --recurse-submodules https://github.com/Linereck/synthetic-short-basket-tracker
# or skip LFS and fetch the CSV from the data repo's releases:
#   download sec_fails_to_deliver_all.csv.gz, gunzip into data/cns-fails-to-deliver/
pip install -r requirements.txt
python analysis/extract_exhibit_data.py > exhibits.json
python ftd_heatmap.py data/cns-fails-to-deliver/sec_fails_to_deliver_all.csv -t GME XRT CHWY --freq W --log
```

## Roadmap

- FTD clustering engine: group tickers failing in sync with GME, ranked by frequency and notional
- T+35 convergence heatmap: calendar view of overlapping close-out deadlines
- Synthetic pressure score: daily 0-100 risk score per ticker or basket from FTD volume,
  cost-to-borrow, ETF flows, and gamma exposure
- Historical price overlay against FTD cycles; alerts for new FTD spikes and borrow-fee surges

## License

MIT
