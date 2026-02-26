# rndm/core.py
from __future__ import annotations
from datetime import datetime

_MASK64 = (1 << 64) - 1

# SplitMix64 constants
_GAMMA = 0x9E3779B97F4A7C15
_M1 = 0xBF58476D1CE4E5B9
_M2 = 0x94D049BB133111EB

# One global stream by default
_STATE = 0
_STREAM_ID = 0


def _mix64(x: int) -> int:
    """SplitMix64 mixing function (finalizer)."""
    x &= _MASK64
    x ^= (x >> 30) & _MASK64
    x = (x * _M1) & _MASK64
    x ^= (x >> 27) & _MASK64
    x = (x * _M2) & _MASK64
    x ^= (x >> 31) & _MASK64
    return x & _MASK64


def _time_seed64() -> int:
    now = datetime.now()
    # build a time seed (ms resolution) and mix it
    seed = (
        now.year * 10000000000000
        + now.month * 100000000000
        + now.day * 1000000000
        + now.hour * 10000000
        + now.minute * 100000
        + now.second * 1000
        + (now.microsecond // 1000)
    )
    return _mix64(seed)


def set_stream_id(stream_id: int) -> None:
    """
    Set the stream id (lets you have independent sequences).
    Changing the stream id reseeds the generator using current time + stream_id.
    """
    global _STREAM_ID
    _STREAM_ID = int(stream_id)
    reseed()  # reseed with new stream id


def reseed(seed: int | None = None, stream_id: int | None = None) -> int:
    """
    Reseed the generator.

    - If seed is None -> seed from current time.
    - If stream_id is provided -> also updates the stream id.
    Returns the 64-bit internal state used.

    Note: seed can be any int (positive/negative/large). It will be mixed to 64-bit.
    """
    global _STATE, _STREAM_ID

    if stream_id is not None:
        _STREAM_ID = int(stream_id)

    if seed is None:
        base = _time_seed64()
    else:
        base = _mix64(int(seed))

    # Combine base seed with stream id to make independent streams
    combined = _mix64(base ^ _mix64(_STREAM_ID))

    # SplitMix state must be nonzero
    _STATE = combined or 1
    return _STATE


def _ensure_seeded():
    global _STATE
    if _STATE == 0:
        reseed()


def _next_u64() -> int:
    """
    SplitMix64 step: updates state and returns a 64-bit value.
    """
    global _STATE
    _ensure_seeded()

    _STATE = (_STATE + _GAMMA) & _MASK64
    return _mix64(_STATE)


def randbits(k: int) -> int:
    """
    Return an integer with k random bits (k >= 0).
    Uses the internal 64-bit generator.
    """
    k = int(k)
    if k < 0:
        raise ValueError("k must be >= 0")
    if k == 0:
        return 0

    out = 0
    bits_filled = 0

    while bits_filled < k:
        r = _next_u64()
        take = min(64, k - bits_filled)
        # take top 'take' bits (no modulo)
        chunk = r >> (64 - take)
        out = (out << take) | chunk
        bits_filled += take

    return out


def _uniform_below(n: int) -> int:
    """
    Exact uniform integer in [0, n) using rejection sampling.
    No modulo.
    """
    n = int(n)
    if n <= 0:
        raise ValueError("n must be positive")

    k = n.bit_length()
    while True:
        r = _next_u64() >> (64 - k)  # [0, 2^k)
        if r < n:
            return r


def _decimal_places(x) -> int:
    # Strings preserve trailing zeros: "0.000" => 3
    if isinstance(x, str):
        return len(x.split(".", 1)[1]) if "." in x else 0
    s = str(x)
    return len(s.split(".", 1)[1]) if "." in s else 0


def _to_scaled_int(x, scale: int, p: int) -> int:
    """
    Convert int/float/str to scaled integer with exactly p decimals.
    Uses string parsing to avoid float artifacts and preserve user precision when passed as strings.
    """
    s = x if isinstance(x, str) else str(x)

    sign = -1 if s.startswith("-") else 1
    if sign == -1:
        s = s[1:]

    if "." not in s:
        return sign * (int(s) * scale)

    whole, frac = s.split(".", 1)
    frac = (frac + "0" * p)[:p]
    whole_i = int(whole) if whole else 0
    return sign * (whole_i * scale + int(frac))


def time_based_random(min_value=0, max_value=1, inclusive=True, precision=None):
    """
    - Int bounds -> returns int.
    - Otherwise returns float with decimals limited to:
        * `precision` if provided, else
        * max decimals detected from inputs (strings preserve trailing zeros).

    No modulo (%) used.
    """
    # INT MODE
    if isinstance(min_value, int) and isinstance(max_value, int):
        n = (max_value - min_value + 1) if inclusive else (max_value - min_value)
        if n <= 0:
            raise ValueError("Invalid integer range.")
        return min_value + _uniform_below(n)

    # FLOAT MODE
    p = precision if precision is not None else max(_decimal_places(min_value), _decimal_places(max_value))
    scale = 10 ** p

    min_i = _to_scaled_int(min_value, scale, p)
    max_i = _to_scaled_int(max_value, scale, p)

    n = (max_i - min_i + 1) if inclusive else (max_i - min_i)
    if n <= 0:
        raise ValueError("Invalid float range.")

    idx = _uniform_below(n)
    val_i = min_i + idx
    return round(val_i / scale, p)
