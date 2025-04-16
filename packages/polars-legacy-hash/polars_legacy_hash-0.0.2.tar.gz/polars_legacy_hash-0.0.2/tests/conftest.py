"""Conftest.py is kind overkill, but allows reuse between function behaviour and checking test assertions are good."""

import polars as pl
from pytest import fixture


@fixture
def raw_struct_df() -> pl.DataFrame:
    return pl.DataFrame({"a": [-42, 13], "b": [-42, 0]})


@fixture
def raw_struct_df_singular() -> pl.DataFrame:
    return pl.DataFrame({"a": [-42, 32]})


@fixture
def expected_int64_neg_42():
    return pl.Series("test", [15244781726809025498], dtype=pl.UInt64)


@fixture
def expected_int32_neg_42():
    return pl.Series("test", [17010062867703544896], dtype=pl.UInt64)


@fixture
def expected_uint64_42():
    return pl.Series("test", [3146795401079207122], dtype=pl.UInt64)


@fixture
def expected_uint32_42():
    return pl.Series("test", [3146795401079207122], dtype=pl.UInt64)


@fixture
def expected_int_struct():
    return pl.Series("test", [78953510757616805, 10151173556673123992], dtype=pl.UInt64)


@fixture
def expected_int_struct_singular():
    return pl.Series("test", [15244781726809025498, 4321950247308341530], dtype=pl.UInt64)
