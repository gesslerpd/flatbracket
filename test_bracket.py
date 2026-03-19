from itertools import batched
import os
import pytest
from flatbracket import create_bracket, encode, iter_results, _generate_seeds, decode


class TestCreateBracket:
    """Test suite for the create_bracket function."""

    def test_empty_results(self):
        """Test with empty results list."""
        results = []
        bracket_data = create_bracket(results)
        assert bracket_data == b""

    def test_single_result_zero(self):
        """Test with a single result of 0."""
        results = [0]
        bracket_data = create_bracket(results)
        assert bracket_data == b"\x00"
        assert list(iter_results(bracket_data))[0] == 0

    def test_single_result_one(self):
        """Test with a single result of 1."""
        results = [1]
        bracket_data = create_bracket(results)
        assert bracket_data == b"\x01"
        assert list(iter_results(bracket_data))[0] == 1

    def test_multiple_results_within_one_byte(self):
        """Test with multiple results that fit in one byte."""
        results = [1, 0, 1, 1, 0, 0, 1, 0]
        bracket_data = create_bracket(results)
        # Binary: 01001101 (reversed due to bit packing)
        # Decimal: 77
        assert bracket_data == b"\x4d"
        assert list(iter_results(bracket_data))[:8] == results

    def test_exactly_eight_results(self):
        """Test with exactly 8 results (one full byte)."""
        results = [1, 1, 1, 1, 1, 1, 1, 1]
        bracket_data = create_bracket(results)
        assert bracket_data == b"\xff"
        assert list(iter_results(bracket_data))[:8] == results

    def test_all_zeros_one_byte(self):
        """Test with all zeros in one byte."""
        results = [0, 0, 0, 0, 0, 0, 0, 0]
        bracket_data = create_bracket(results)
        assert bracket_data == b"\x00"
        assert list(iter_results(bracket_data))[:8] == results

    def test_multiple_bytes(self):
        """Test with results spanning multiple bytes."""
        results = [
            1,
            0,
            1,
            0,
            1,
            0,
            1,
            0,  # First byte: 0x55
            0,
            1,
            0,
            1,
            0,
            1,
            0,
            1,
        ]  # Second byte: 0xaa
        bracket_data = create_bracket(results)
        assert bracket_data == b"\x55\xaa"
        assert list(iter_results(bracket_data))[:16] == results

    def test_partial_last_byte(self):
        """Test with results that don't fill the last byte completely."""
        results = [1, 1, 1]
        bracket_data = create_bracket(results)
        # First 3 bits set: 0b00000111 = 0x07
        assert bracket_data == b"\x07"
        assert list(iter_results(bracket_data))[:3] == results

    def test_nine_results(self):
        """Test with 9 results (1 full byte + 1 bit in second byte)."""
        results = [
            1,
            1,
            1,
            1,
            1,
            1,
            1,
            1,  # First byte: 0xff
            1,
        ]  # Second byte: 0x01
        bracket_data = create_bracket(results)
        assert bracket_data == b"\xff\x01"
        assert list(iter_results(bracket_data))[:9] == results

    def test_fifteen_results(self):
        """Test with 15 results (1 full byte + 7 bits in second byte)."""
        results = [
            0,
            1,
            0,
            1,
            0,
            1,
            0,
            1,  # First byte
            1,
            0,
            1,
            0,
            1,
            0,
            1,
        ]  # Second byte (7 bits)
        bracket_data = create_bracket(results)
        assert len(bracket_data) == 2
        assert list(iter_results(bracket_data))[:15] == results

    def test_64_team_bracket(self):
        """Test with 63 results (typical 64-team bracket)."""
        # 63 games in a 64-team single elimination bracket
        results = [1] * 63
        bracket_data = create_bracket(results)
        # 63 bits = 7 full bytes + 7 bits in 8th byte
        assert len(bracket_data) == 8
        assert list(iter_results(bracket_data))[:63] == results

    def test_bit_packing_order(self):
        """Test that bits are packed in the correct order (LSB first)."""
        # Bit 0 should be LSB, bit 7 should be MSB
        results = [1, 0, 0, 0, 0, 0, 0, 0]  # Only first bit set
        bracket_data = create_bracket(results)
        assert bracket_data == b"\x01"

        results = [0, 1, 0, 0, 0, 0, 0, 0]  # Only second bit set
        bracket_data = create_bracket(results)
        assert bracket_data == b"\x02"

        results = [0, 0, 0, 0, 0, 0, 0, 1]  # Only eighth bit set (MSB)
        bracket_data = create_bracket(results)
        assert bracket_data == b"\x80"

    def test_roundtrip_consistency(self):
        """Test that create_bracket and iter_results are inverses."""
        test_cases = [
            [0, 1, 1, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
            [0] * 20,
            [1, 0] * 10,
        ]
        for results in test_cases:
            bracket_data = create_bracket(results)
            decoded = list(iter_results(bracket_data))[: len(results)]
            assert decoded == results

    def test_generator_input(self):
        """Test that the function works with generator input."""

        def result_generator():
            for i in range(5):
                yield i % 2

        bracket_data = create_bracket(result_generator())
        expected = [0, 1, 0, 1, 0]
        assert list(iter_results(bracket_data))[:5] == expected

    def test_large_bracket(self):
        """Test with a large number of results."""
        results = [i % 2 for i in range(100)]
        bracket_data = create_bracket(results)
        # 100 bits = 12 full bytes + 4 bits
        assert len(bracket_data) == 13
        assert list(iter_results(bracket_data))[:100] == results


@pytest.mark.parametrize(
    "number_of_teams,expected",
    [
        (16, [1, 16, 8, 9, 5, 12, 4, 13, 6, 11, 3, 14, 7, 10, 2, 15]),
        (8, [1, 8, 4, 5, 3, 6, 2, 7]),
        (4, [1, 4, 2, 3]),
        (2, [1, 2]),
        (1, [1]),
        (0, []),
        (
            32,
            [
                1,
                32,
                16,
                17,
                9,
                24,
                8,
                25,
                12,
                21,
                5,
                28,
                13,
                20,
                4,
                29,
                11,
                22,
                6,
                27,
                14,
                19,
                3,
                30,
                10,
                23,
                7,
                26,
                15,
                18,
                2,
                31,
            ],
        ),
    ],
)
def test_seed_gen(number_of_teams, expected):
    assert _generate_seeds(number_of_teams) == expected


@pytest.mark.parametrize("n", range(2, 1024))
def test_seed_gen_all(n):
    seeds = _generate_seeds(n)
    assert len(seeds) >= n / 2
    assert len(seeds) == len(set(seeds))
    for above, below in batched(seeds, 2):
        assert above + below == n + 1


def test_decode():
    for i in range(10000):
        val = os.urandom(i)
        assert decode(encode(val)) == val
