# Analysis scripts

Both scripts join the consolidated SEC fails-to-deliver CSV with the Reg SHO
threshold-list CSVs and print JSON to stdout. Run them from the repository root;
defaults point at `data/cns-fails-to-deliver/` (submodule, Git LFS) and `data/regsho/`.

- `extract_exhibit_data.py` - data for exhibits 1-3 (the January 2021 handoff window,
  the full XRT fails history with residency bands, and the pre/post-exit cliff).
- `extract_forecast.py` - data for exhibit 4 (residency survival curve, day-in-residency
  fail quantiles, live residency path).

The interactive pages in `docs/` inline this JSON: `docs/exhibits.html` contains
`const DATA = {...};` (exhibit data) and `const FC = {...};` (forecast data). To refresh
the site after a data update, regenerate both JSON payloads and swap those two consts.

Getting the inputs without Git LFS: download `sec_fails_to_deliver_all.csv.gz` from the
data repository's releases and gunzip it to the submodule path.

Method note: threshold-list streak continuity is judged against each exchange's own
publication calendar (a day the whole file is absent is unknown, not off-list; NYSE
publishes no list on Columbus Day or Veterans Day). Replications using naive weekday
calendars will understate every streak.
