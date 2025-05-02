# Synthetic Short Basket Tracker

**Identify & monitor synthetic short exposure through FTD clustering, timing convergence, and systemic basket risk.**

## Overview

This tool maps relationships between GME and other tickers (e.g., CHWY, XRT, BABA) by analyzing:

- Failures-to-Deliver (FTDs)
- Borrow data
- Options positioning

The goal is to uncover synthetic basket activity, predict unwind windows, and provide timing signals for potential short pressure events.

---

## Core Features

### 1. FTD Clustering Engine

Identify tickers that repeatedly fail-to-deliver in sync with GME.

- Parse SEC FTD data across 100+ tickers
- Align tickers by T+35 closing deadlines (not just trade dates)
- Group tickers that:
  - Fail to deliver in the same 5–7 day window as GME
  - Show high FTD volumes (>50K+)
- **Output:** Top tickers clustered with GME, ranked by frequency and total $ notional

---

### 2. T+35 Convergence Heatmap

Visualize when multiple tickers have overlapping FTD closing deadlines.

- Calendar view showing how many securities have T+35s falling on each day
- Color-coded days with major deadline clusters
- Optional countdown clock for next big compression window

Initial ftd_heatmap.py implementation plots a FTD Volume heatmap

![image](https://github.com/user-attachments/assets/3eca765e-56e7-4e5f-a8bc-deecc06eac81)

```
python ftd_heatmap.py \
data/cns-fails-to-deliver/sec_fails_to_deliver_all.csv \
-t GME XRT CHWY KOSS \
--freq W
```

![image](https://github.com/user-attachments/assets/b0bfde8e-ac3b-409c-8762-f6f5504696fd)

```
python ftd_heatmap.py \
data/cns-fails-to-deliver/sec_fails_to_deliver_all.csv \
-t GME XRT CHWY KOSS \
--freq D \
--log \
--from 2023-01-01 --to 2025-05-01
```
---

### 3. Synthetic Pressure Score

Daily score estimating risk of systemic unwind.

Factors considered:

- FTD volume & recency
- CTB (Cost to Borrow) changes (scraped)
- ETF inflows/outflows (e.g., XRT, IWM)
- Options gamma exposure near current price

**Output:**  
0–100 risk score, calculated per ticker or basket

---

## Suggested File Structure
```

├── data/
│   ├── ftd_raw
│   ├── etf_holdings
│   ├── borrow_rates
├── scripts/
│   ├── parse_ftd.py
│   ├── calc_t35_windows.py
│   ├── cluster_engine.py
│   ├── gamma_analysis.py
│   ├── scrape_ctb.py
├── outputs/
│   ├── cluster_heatmap.csv
│   ├── ticker_risk_scores.json
├── root_files/
│   ├── dashboard.py
│   ├── README.md
```
---

## Stretch Goals

- Pull historical price action and overlay vs FTD cycles
- Add chart annotations for T+35 windows
- Live alerts for new FTD spikes or borrow fee surges

---

## License

MIT
