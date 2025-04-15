from functools import partial
from pathlib import Path

import numpy as np
from numpy.typing import NDArray
from pytest_cases import fixture, parametrize_with_cases

from genoray import VCF

tdir = Path(__file__).parent
ddir = tdir / "data"


@fixture  # type: ignore
def vcf():
    return VCF(ddir / "test.vcf.gz", dosage_field="DS")


def read_all():
    cse = "chr1", 81261, 81263
    # (s p v)
    genos = np.array([[[0, -1], [1, -1]], [[1, 0], [1, 1]]], np.int8)
    # (s v)
    dosages = np.full((2, 2), 0.5, np.float32)
    dosages[0, 1] = np.nan
    return cse, genos, dosages


def read_spanning_del():
    cse = "chr1", 81262, 81263
    # (s p v)
    genos = np.array([[[0], [1]], [[1], [1]]], np.int8)
    # (s v)
    dosages = np.full((2, 1), 0.5, np.float32)
    return cse, genos, dosages


@parametrize_with_cases("cse, genos, dosages", cases=".", prefix="read_")
def test_read(
    vcf: VCF,
    cse: tuple[str, int, int],
    genos: NDArray[np.int8],
    dosages: NDArray[np.float32],
):
    # (s p v)
    actual = vcf.read(*cse, VCF.Genos16Dosages)
    assert actual is not None
    np.testing.assert_equal(actual[0], genos)
    np.testing.assert_equal(actual[1], dosages)


@parametrize_with_cases("cse, genos, dosages", cases=".", prefix="read_")
def test_chunk(
    vcf: VCF,
    cse: tuple[str, int, int],
    genos: NDArray[np.int8],
    dosages: NDArray[np.float32],
):
    max_mem = vcf._mem_per_variant(VCF.Genos16Dosages)
    cat = partial(np.concatenate, axis=-1)
    itr = vcf.chunk(*cse, max_mem, VCF.Genos16Dosages)
    chunks = list(zip(*itr))
    assert len(chunks[0]) == genos.shape[-1]
    assert len(chunks[1]) == dosages.shape[-1]
    actual = cat(chunks[0]), cat(chunks[1])
    np.testing.assert_equal(actual[0], genos)
    np.testing.assert_equal(actual[1], dosages)
