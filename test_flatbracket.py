import pytest
from flatbracket import _draw
from flatbracket import (
    iter_results,
    create_bracket,
    random_result,
    generate_matchups,
    initialize_matchups,
)
from unittest.mock import patch


def test_draw_two_teams():
    """Test bracket with 2 teams (single matchup)."""
    matchups = [(0, 1), (0, 0)]
    teams = ["Team A", "Team B"]

    result = list(_draw(matchups, teams))

    assert result[0] == "flowchart LR"
    assert result[1] == "    2-0[Team A vs. Team B] --> 1-0"
    assert result[2] == "    1-0[Team A]"


def test_draw_four_teams():
    """Test bracket with 4 teams (2 rounds)."""
    matchups = [(0, 1), (2, 3), (0, 2), (0, 0)]
    teams = ["Team A", "Team B", "Team C", "Team D"]

    result = list(_draw(matchups, teams))

    assert result[0] == "flowchart LR"
    assert result[1] == "    4-0[Team A vs. Team B] --> 2-0"
    assert result[2] == "    4-1[Team C vs. Team D] --> 2-0"
    assert result[3] == "    2-0[Team A vs. Team C] --> 1-0"
    assert result[4] == "    1-0[Team A]"


def test_draw_eight_teams():
    """Test bracket with 8 teams (3 rounds)."""
    matchups = [
        (0, 1),
        (2, 3),
        (4, 5),
        (6, 7),  # Round 1
        (0, 2),
        (4, 6),  # Round 2
        (0, 4),  # Round 3
        (0, 0),  # Winner
    ]
    teams = ["A", "B", "C", "D", "E", "F", "G", "H"]

    result = list(_draw(matchups, teams))

    assert result[0] == "flowchart LR"
    # Round 1 (8 teams -> 4 teams)
    assert result[1] == "    8-0[A vs. B] --> 4-0"
    assert result[2] == "    8-1[C vs. D] --> 4-0"
    assert result[3] == "    8-2[E vs. F] --> 4-1"
    assert result[4] == "    8-3[G vs. H] --> 4-1"
    # Round 2 (4 teams -> 2 teams)
    assert result[5] == "    4-0[A vs. C] --> 2-0"
    assert result[6] == "    4-1[E vs. G] --> 2-0"
    # Round 3 (2 teams -> 1 team)
    assert result[7] == "    2-0[A vs. E] --> 1-0"
    # Winner
    assert result[8] == "    1-0[A]"


def test_draw_empty_matchups():
    """Test with empty matchups list."""
    matchups = []
    teams = ["Team A", "Team B"]

    result = list(_draw(matchups, teams))

    assert result == ["flowchart LR"]


def test_draw_single_matchup():
    """Test with only the first round matchup."""
    matchups = [(0, 1)]
    teams = ["Team A", "Team B"]

    result = list(_draw(matchups, teams))

    assert result[0] == "flowchart LR"
    assert result[1] == "    2-0[Team A vs. Team B] --> 1-0"


def test_draw_team_names_with_special_chars():
    """Test that team names with special characters are handled."""
    matchups = [(0, 1), (0, 0)]
    teams = ["Team [A]", "Team (B)"]

    result = list(_draw(matchups, teams))

    assert result[0] == "flowchart LR"
    assert result[1] == "    2-0[Team [A] vs. Team (B)] --> 1-0"
    assert result[2] == "    1-0[Team [A]]"


def test_draw_round_transitions():
    """Test that round size transitions correctly."""
    matchups = [(0, 1), (2, 3), (0, 2), (0, 0)]
    teams = ["A", "B", "C", "D"]

    result = list(_draw(matchups, teams))

    # First two matchups should have round_size=4, next_round_size=2
    assert "4-0" in result[1] and "2-0" in result[1]
    assert "4-1" in result[2] and "2-0" in result[2]
    # Third matchup should have round_size=2, next_round_size=1
    assert "2-0" in result[3] and "1-0" in result[3]
    # Final matchup should have round_size=1, next_round_size=0
    assert result[4] == "    1-0[A]"


def test_create_bracket_empty():
    """Test creating bracket with no results."""
    results = []
    bracket = create_bracket(results)
    assert bracket == b""


def test_create_bracket_single_result():
    """Test creating bracket with a single result."""
    results = [0]
    bracket = create_bracket(results)
    assert bracket == b"\x00"

    results = [1]
    bracket = create_bracket(results)
    assert bracket == b"\x01"


def test_create_bracket_eight_results():
    """Test creating bracket with exactly 8 results (1 byte)."""
    results = [0, 0, 0, 0, 0, 0, 0, 0]
    bracket = create_bracket(results)
    assert bracket == b"\x00"

    results = [1, 1, 1, 1, 1, 1, 1, 1]
    bracket = create_bracket(results)
    assert bracket == b"\xff"


def test_create_bracket_bit_positions():
    """Test that bits are set in correct positions."""
    results = [1, 0, 0, 0, 0, 0, 0, 0]
    bracket = create_bracket(results)
    assert bracket == b"\x01"

    results = [0, 1, 0, 0, 0, 0, 0, 0]
    bracket = create_bracket(results)
    assert bracket == b"\x02"

    results = [0, 0, 0, 0, 0, 0, 0, 1]
    bracket = create_bracket(results)
    assert bracket == b"\x80"


def test_create_bracket_multiple_bytes():
    """Test creating bracket with multiple bytes."""
    results = [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0]
    bracket = create_bracket(results)
    assert bracket == b"\xff\x00"

    results = [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1]
    bracket = create_bracket(results)
    assert bracket == b"\x00\xff"


def test_create_bracket_partial_byte():
    """Test creating bracket with partial byte (less than 8 results)."""
    results = [1, 0, 1]
    bracket = create_bracket(results)
    assert bracket == b"\x05"  # bits 0 and 2 set: 0b00000101

    results = [1, 1, 0, 0, 1]
    bracket = create_bracket(results)
    assert bracket == b"\x13"  # bits 0, 1, 4 set: 0b00010011


def test_create_bracket_mixed_pattern():
    """Test creating bracket with mixed bit pattern."""
    results = [1, 0, 1, 0, 1, 0, 1, 0]
    bracket = create_bracket(results)
    assert bracket == b"\x55"  # 0b01010101

    results = [0, 1, 0, 1, 0, 1, 0, 1]
    bracket = create_bracket(results)
    assert bracket == b"\xaa"  # 0b10101010


def test_create_bracket_roundtrip():
    """Test that create_bracket and iter_results are inverse operations."""

    original_results = [1, 0, 1, 1, 0, 0, 1, 0, 1, 1]
    bracket = create_bracket(original_results)
    decoded_results = list(iter_results(bracket))

    # Should match original results (padded to byte boundary)
    assert decoded_results[: len(original_results)] == original_results


def test_random_result_deterministic_mock():
    """Test random_result with mocked random values."""
    seeds = [1, 2, 3, 4]

    # Mock random to return 0.5
    with patch("flatbracket.RNG.random", return_value=0.5):
        # above_index=0 (seed=1), below_index=1 (seed=2)
        # probability = 2/(1+2) = 0.667
        # 0.5 > 0.667 is False, so result should be 0
        result = random_result(0, 1, seeds)
        assert result == 0

    # Mock random to return 0.8
    with patch("flatbracket.RNG.random", return_value=0.8):
        # above_index=0 (seed=1), below_index=1 (seed=2)
        # probability = 2/(1+2) = 0.667
        # 0.8 > 0.667 is True, so result should be 1
        result = random_result(0, 1, seeds)
        assert result == 1


def test_random_result_equal_seeds():
    """Test random_result with equal seeds."""
    seeds = [2, 2, 2, 2]

    # With equal seeds, probability = 2/(2+2) = 0.5
    with patch("flatbracket.RNG.random", return_value=0.4):
        result = random_result(0, 1, seeds)
        assert result == 0

    with patch("flatbracket.RNG.random", return_value=0.6):
        result = random_result(0, 1, seeds)
        assert result == 1


def test_random_result_heavily_favored():
    """Test random_result with heavily favored matchup."""
    seeds = [1, 16]

    # above_index=0 (seed=1), below_index=1 (seed=16)
    # probability = 16/(1+16) = 0.941
    with patch("flatbracket.RNG.random", return_value=0.95):
        result = random_result(0, 3, seeds)
        assert result == 1

    with patch("flatbracket.RNG.random", return_value=0.90):
        result = random_result(0, 3, seeds)
        assert result == 0


def test_random_result_opposite_matchup():
    """Test random_result with reversed matchup positions."""
    seeds = [1, 16]

    # above_index=1 (seed=16), below_index=0 (seed=1)
    # probability = 1/(16+1) = 0.059
    with patch("flatbracket.RNG.random", return_value=0.05):
        result = random_result(1, 0, seeds)
        assert result == 0

    with patch("flatbracket.RNG.random", return_value=0.10):
        result = random_result(1, 0, seeds)
        assert result == 1


def test_random_result_single_seed():
    """Test random_result with single seed list."""
    seeds = [5]

    # Both teams get same seed, probability = 5/(5+5) = 0.5
    with patch("flatbracket.RNG.random", return_value=0.3):
        result = random_result(0, 0, seeds)
        assert result == 0

    with patch("flatbracket.RNG.random", return_value=0.7):
        result = random_result(0, 0, seeds)
        assert result == 1


def test_generate_matchups_two_teams():
    """Test generate_matchups with 2 teams (1 game)."""
    # Result: 0 means first team wins
    results = [0]
    matchups = list(generate_matchups(results, 2))

    assert len(matchups) == 2
    assert matchups[0] == (0, 1)  # Initial matchup
    assert matchups[1] == (0, 0)  # Winner matchup


def test_generate_matchups_two_teams_second_wins():
    """Test generate_matchups with 2 teams where second team wins."""
    # Result: 1 means second team wins
    results = [1]
    matchups = list(generate_matchups(results, 2))

    assert len(matchups) == 2
    assert matchups[0] == (0, 1)  # Initial matchup
    assert matchups[1] == (1, 1)  # Winner matchup


def test_generate_matchups_four_teams():
    """Test generate_matchups with 4 teams."""
    # Results: [0, 0, 0] means first team wins all games
    results = [0, 0, 0]
    matchups = list(generate_matchups(results, 4))

    assert len(matchups) == 4
    assert matchups[0] == (0, 1)  # Round 1, game 1
    assert matchups[1] == (2, 3)  # Round 1, game 2
    assert matchups[2] == (0, 2)  # Round 2 (finals)
    assert matchups[3] == (0, 0)  # Winner


def test_generate_matchups_four_teams_missing():
    """Test generate_matchups with 4 teams."""
    results = [0, 0]
    matchups = list(generate_matchups(results, 4))

    assert len(matchups) == 3
    assert matchups[0] == (0, 1)  # Round 1, game 1
    assert matchups[1] == (2, 3)  # Round 1, game 2
    assert matchups[2] == (0, 2)  # Round 2 (finals)


def test_generate_matchups_four_teams_mixed_results():
    """Test generate_matchups with 4 teams and mixed results."""
    # Results: [1, 0, 1] means team 1 wins game 1, team 2 wins game 2, team 1 wins finals
    results = [1, 0, 1]
    matchups = list(generate_matchups(results, 4))

    assert len(matchups) == 4
    assert matchups[0] == (0, 1)  # Round 1, game 1
    assert matchups[1] == (2, 3)  # Round 1, game 2
    assert matchups[2] == (
        1,
        2,
    )  # Round 2: winner of game 1 (team 1) vs winner of game 2 (team 2)
    assert matchups[3] == (2, 2)  # Winner is team 2


def test_generate_matchups_eight_teams():
    """Test generate_matchups with 8 teams."""
    # All first teams win: [0, 0, 0, 0, 0, 0, 0]
    results = [0, 0, 0, 0, 0, 0, 0]
    matchups = list(generate_matchups(results, 8))

    assert len(matchups) == 8
    # Round 1
    assert matchups[0] == (0, 1)
    assert matchups[1] == (2, 3)
    assert matchups[2] == (4, 5)
    assert matchups[3] == (6, 7)
    # Round 2
    assert matchups[4] == (0, 2)
    assert matchups[5] == (4, 6)
    # Round 3
    assert matchups[6] == (0, 4)
    # Winner
    assert matchups[7] == (0, 0)


def test_generate_matchups_eight_teams_all_upsets():
    """Test generate_matchups with 8 teams where all second teams win."""
    # All second teams win: [1, 1, 1, 1, 1, 1, 1]
    results = [1, 1, 1, 1, 1, 1, 1]
    matchups = list(generate_matchups(results, 8))

    assert len(matchups) == 8
    # Round 1
    assert matchups[0] == (0, 1)
    assert matchups[1] == (2, 3)
    assert matchups[2] == (4, 5)
    assert matchups[3] == (6, 7)
    # Round 2
    assert matchups[4] == (1, 3)
    assert matchups[5] == (5, 7)
    # Round 3
    assert matchups[6] == (3, 7)
    # Winner
    assert matchups[7] == (7, 7)


def test_generate_matchups_insufficient_results():
    """Test generate_matchups when bracket_data runs out of results."""
    # Only provide 2 results for 4 teams (need 3)
    results = [0, 1]
    matchups = list(generate_matchups(results, 4))

    # Should yield initial matchups and partial progression
    assert len(matchups) == 3
    assert matchups[0] == (0, 1)  # Round 1, game 1
    assert matchups[1] == (2, 3)  # Round 1, game 2
    assert matchups[2] == (0, 3)  # Round 2 starts but incomplete


def test_generate_matchups_one_team():
    """Test generate_matchups with empty bracket data."""
    results = []
    matchups = list(generate_matchups(results, 1))

    # Should only yield initial matchups
    assert len(matchups) == 1
    assert matchups[0] == (0, 0)


def test_generate_matchups_empty_bracket_data():
    """Test generate_matchups with empty bracket data."""
    results = []
    matchups = list(generate_matchups(results, 2))

    # Should only yield initial matchups
    assert len(matchups) == 1
    assert matchups[0] == (0, 1)


def test_generate_matchups_single_result_for_two_teams():
    """Test that exactly one result creates complete 2-team bracket."""
    results = [1]
    matchups = list(generate_matchups(results, 2))

    assert len(matchups) == 2
    assert matchups[0] == (0, 1)
    assert matchups[1] == (1, 1)


def test_generate_matchups_progression():
    """Test that matchups progress correctly through rounds."""
    # 4 teams: game1 winner=1, game2 winner=3, finals winner=3
    results = [1, 1, 1]
    matchups = list(generate_matchups(results, 4))

    assert matchups[0] == (0, 1)  # Initial
    assert matchups[1] == (2, 3)  # Initial
    assert matchups[2] == (1, 3)  # Winners of games 0 and 1
    assert matchups[3] == (3, 3)  # Final winner


def test_generate_matchups_sixteen_teams():
    """Test generate_matchups with 16 teams (larger bracket)."""
    # Create results for 15 games (16 teams)
    results = [0] * 15  # All first teams win
    matchups = list(generate_matchups(results, 16))

    assert len(matchups) == 16
    # Verify first round (8 games)
    for i in range(8):
        assert matchups[i] == (i * 2, i * 2 + 1)
    # Verify final winner
    assert matchups[-1] == (0, 0)


def test_initialize_matchups_two_teams():
    """Test initialize_matchups with 2 teams."""
    matchups = initialize_matchups(2)
    assert matchups == [(0, 1)]


def test_initialize_matchups_four_teams():
    """Test initialize_matchups with 4 teams."""
    matchups = initialize_matchups(4)
    assert matchups == [(0, 1), (2, 3)]


def test_initialize_matchups_eight_teams():
    """Test initialize_matchups with 8 teams."""
    matchups = initialize_matchups(8)
    assert matchups == [(0, 1), (2, 3), (4, 5), (6, 7)]


def test_initialize_matchups_sixteen_teams():
    """Test initialize_matchups with 16 teams."""
    matchups = initialize_matchups(16)
    assert matchups == [
        (0, 1),
        (2, 3),
        (4, 5),
        (6, 7),
        (8, 9),
        (10, 11),
        (12, 13),
        (14, 15),
    ]


def test_initialize_matchups_odd_teams():
    """Test initialize_matchups with odd number of teams."""
    matchups = initialize_matchups(5)
    # Should create pairs and drop the incomplete pair
    assert matchups == [(0, 1), (2, 3)]


def test_initialize_matchups_three_teams():
    """Test initialize_matchups with 3 teams."""
    matchups = initialize_matchups(3)
    assert matchups == [(0, 1)]


def test_initialize_matchups_one_team():
    """Test initialize_matchups with single team."""
    matchups = initialize_matchups(1)
    assert matchups == []


def test_initialize_matchups_zero_teams():
    """Test initialize_matchups with zero teams."""
    matchups = initialize_matchups(0)
    assert matchups == []


def test_initialize_matchups_large_bracket():
    """Test initialize_matchups with larger bracket (32 teams)."""
    matchups = initialize_matchups(32)
    assert len(matchups) == 16
    assert matchups[0] == (0, 1)
    assert matchups[15] == (30, 31)
