import pytest

from python_sei.sin import decode_sin, encode_sin


def test_decode_sin_valid():
    value = decode_sin("S")
    assert value

    value = decode_sin("N")
    assert not value


def test_decode_sin_invalid():
    with pytest.raises(ValueError):
        decode_sin("foo")


def test_encode_sin():
    value = encode_sin(True)
    assert value == "S"

    value = encode_sin(False)
    assert value == "N"
