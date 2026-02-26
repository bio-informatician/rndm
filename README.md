# rndm

A tiny, dependency-free random number utility built on **SplitMix64**.

It provides:
- Uniform integers without modulo bias (rejection sampling)
- Fixed-precision uniform floats within a range
- Optional independent streams via `stream_id`
- Fast `randbits(k)` for bit generation

> **Not for cryptography.** SplitMix64 is great for simulations, sampling, games, and testing—but not for security.

## Install

### From PyPI

```bash
pip install rndm
```

### From source (GitHub)

```bash
pip install .
```

For development:

```bash
pip install -e ".[dev]"
```

## Quick start

```python
import rndm

# (optional) reseed; if you don't, it seeds automatically on first use
rndm.reseed()

# Uniform int in [0, 10] (inclusive by default)
x = rndm.time_based_random(0, 10)
print(x)

# Uniform int in [50, 1000), exclusive upper bound
y = rndm.time_based_random(50, 1000, inclusive=False)
print(y)

# Uniform float in [-1.0, 1.0] with precision inferred from inputs (1 decimal here)
z = rndm.time_based_random(-1.0, 1.0)
print(z)

# Force precision (e.g., 3 decimals)
w = rndm.time_based_random("0.000", "0.999", precision=3)
print(w)

# Independent streams
rndm.set_stream_id(123)
a1 = rndm.time_based_random(0, 10)
rndm.set_stream_id(456)
a2 = rndm.time_based_random(0, 10)
```

## API

- `reseed(seed: int | None = None, stream_id: int | None = None) -> int`  
  Reseeds the generator. If `seed` is `None`, uses a mixed time-based seed. Returns the internal 64-bit state.

- `set_stream_id(stream_id: int) -> None`  
  Switches to a different independent stream (reseeds automatically).

- `randbits(k: int) -> int`  
  Returns an integer with `k` random bits.

- `time_based_random(min_value=0, max_value=1, inclusive=True, precision=None)`  
  - If both bounds are `int`, returns an `int`
  - Otherwise returns a `float` rounded to `precision` decimals (or inferred from inputs).
  - Uses rejection sampling (no `%` modulo reduction), so integer ranges are unbiased.

## Benchmarks

The repository includes example benchmark outputs under `https://github.com/bio-informatician/rndm/tree/main/benchmarks/`:

- Distribution plots: `https://github.com/bio-informatician/rndm/tree/main/benchmarks/plots/`
- Bin counts (CSV): `https://github.com/bio-informatician/rndm/tree/main/benchmarks/counts/`
- Summary table: ![summary](https://raw.githubusercontent.com/bio-informatician/rndm/main/benchmarks/summary.csv)

Example figures:

![Chi-square summary](https://raw.githubusercontent.com/bio-informatician/rndm/main/benchmarks/plots/summary_chi2.png)

![Speed summary](https://raw.githubusercontent.com/bio-informatician/rndm/main/benchmarks/plots/summary_speed.png)

## Development

Run tests:

```bash
pytest
```

Build a wheel + sdist:

```bash
python -m pip install --upgrade build
python -m build
```

## License

MIT — see [LICENSE](http://raw.githubusercontent.com/bio-informatician/rndm/refs/heads/main/LICENSE).
