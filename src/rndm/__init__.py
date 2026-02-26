from __future__ import annotations

"""rndm: lightweight non-cryptographic RNG utilities (SplitMix64)."""

from .core import (
    reseed,
    set_stream_id,
    randbits,
    time_based_random,
)

__all__ = [
    "reseed",
    "set_stream_id",
    "randbits",
    "time_based_random",
]

__version__ = "0.1.0"
