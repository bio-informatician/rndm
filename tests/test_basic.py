import rndm

def test_int_range_inclusive():
    rndm.reseed(12345, stream_id=1)
    for _ in range(1000):
        x = rndm.time_based_random(0, 10, inclusive=True)
        assert 0 <= x <= 10
        assert isinstance(x, int)

def test_int_range_exclusive():
    rndm.reseed(12345, stream_id=2)
    for _ in range(1000):
        x = rndm.time_based_random(0, 10, inclusive=False)
        assert 0 <= x < 10

def test_float_precision():
    rndm.reseed(12345, stream_id=3)
    x = rndm.time_based_random("0.000", "0.999", precision=3)
    assert 0.0 <= x <= 0.999
    # Should be rounded to 3 decimals
    s = f"{x:.3f}"
    assert len(s.split(".")[1]) == 3
