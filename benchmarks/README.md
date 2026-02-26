# Benchmarks

This folder contains example outputs produced by a simple distribution + speed benchmark.

- `counts/`: bin counts used to compute statistics
- `plots/`: rendered plots
- `summary.csv`: summary metrics per distribution

**Metrics included**
- Chi-square vs. uniform (lower is better)
- Max relative deviation from expected bin count (lower is better)
- Runs test z-score (closer to 0 is better)
- Serial correlation at lag-1 (closer to 0 is better)
- Speed (calls/sec; higher is better)

If you add new benchmark runs, keep filenames stable and update `summary.csv`.
