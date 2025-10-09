import base64
import argparse
from random import SystemRandom
from itertools import batched
from collections.abc import Iterable


# 64 team bracket encodes to 11 characters (padding removed)
def encode(bracket_data: bytes) -> str:
    return base64.urlsafe_b64encode(bracket_data).rstrip(b"=").decode("ascii")


def decode(bracket: str) -> bytes:
    return base64.urlsafe_b64decode(bracket + "==")


rand = SystemRandom()


def _generate_seeds(number_of_teams: int) -> list[int]:
    if number_of_teams <= 2:
        return list(range(1, number_of_teams + 1))

    previous = _generate_seeds(number_of_teams // 2)
    n_teams_and_one = number_of_teams + 1
    result = [
        previous[0],
        n_teams_and_one - previous[0],
    ]
    if len(previous) > 1:  # allow for non-power of two teams
        result.extend([
            previous[1],
            n_teams_and_one - previous[1],
        ])
    for i in range(2, len(previous), 2):
        first, second = previous[i + 1], previous[i]
        result.extend(
            [first, n_teams_and_one - first, second, n_teams_and_one - second]
        )

    return result


def random_result(above_index: int, below_index: int, seeds: list[int]) -> int:
    """Generate random result weighted by seed."""
    n_seeds = len(seeds)
    first_seed = seeds[above_index % n_seeds]
    second_seed = seeds[below_index % n_seeds]
    probability = second_seed / (first_seed + second_seed)
    return int(rand.random() > probability)


def iter_results(bracket_data: bytes):
    """Yield individual bit results from bracket data."""
    for byte in bracket_data:
        for i in range(8):
            yield (byte >> i) & 1


def _batched(iterable, n):
    for item in batched(iterable, n):
        # stop early on incomplete batches
        if len(item) != n:
            break
        yield item

def initialize_matchups(number_of_teams: int) -> list:
    """Initialize matchups for the first round."""
    return list(_batched(range(number_of_teams), 2))


def generate_matchups(
    bracket_data: bytes, number_of_teams: int
) -> Iterable[tuple[int, int]]:
    """Generate all matchups based on bracket results."""
    matchups = initialize_matchups(number_of_teams)
    prev_winner = winner = 0

    yield from matchups

    for i, (result, matchup) in enumerate(zip(iter_results(bracket_data), matchups)):
        winner = matchup[result]
        if i % 2:  # After every second game, create next round matchup
            next_matchup = (prev_winner, winner)
            matchups.append(next_matchup)
            yield next_matchup
        prev_winner = winner

    yield (winner, winner)  # chicken dinner


def create_bracket(results: Iterable[int]) -> bytes:
    return bytes(
        sum(bit << i for i, bit in enumerate(byte_results) if bit)
        for byte_results in batched(results, 8)
    )


def _draw(matchups: list, teams: list):
    """Generate mermaid flowchart lines for bracket visualization."""
    round_size = len(teams)
    game_num = 0

    yield "flowchart LR"

    for above, below in matchups:
        next_round_size = round_size // 2
        round_id = f"{round_size}-{game_num}"
        if next_round_size:
            next_round_id = f"{next_round_size}-{game_num // 2}"
            yield f"    {round_id}[{teams[above]} vs. {teams[below]}] --> {next_round_id}"
        else:
            yield f"    {round_id}[{teams[above]}]"

        game_num += 1
        if game_num >= next_round_size:
            game_num = 0
            round_size = next_round_size


def draw(matchups, teams: list) -> str:
    """Generate mermaid flowchart diagram for bracket."""
    return "\n".join(_draw(matchups, teams))


def _is_power_of_two(n: int) -> bool:
    return n > 0 and (n & (n - 1)) == 0


def main():
    parser = argparse.ArgumentParser(
        "flatbracket", description="Flat bracket encoding tool", allow_abbrev=False
    )
    parser.add_argument("teams", help="file containing teams list")
    parser.add_argument("bracket", nargs="?", help="encoded bracket to view")
    parser.add_argument(
        "-r", "--random", action="store_true", help="create random bracket"
    )
    parser.add_argument("--regions", type=int, default=4, help="number of regions")
    args = parser.parse_args()

    with open(args.teams) as file:
        teams = [line.rstrip() for line in file]

    if args.bracket:
        # View mode: decode and display bracket
        print(f"Bracket: {args.bracket}\n")
        bracket_data = decode(args.bracket)
        diagram = draw(generate_matchups(bracket_data, len(teams)), teams)
        print(diagram)
    else:
        # Create mode: build bracket interactively or randomly
        number_of_teams = len(teams)
        # assert _is_power_of_two(number_of_teams), "Number of teams must be a power of 2"
        # assert _is_power_of_two(args.regions), "Number of regions must be a power of 2"
        seeds = _generate_seeds(max(number_of_teams // args.regions, 1))
        matchups = initialize_matchups(number_of_teams)
        results = []
        prev_winner = 0

        for i, (above, below) in enumerate(matchups):
            print(
                f"{teams[above]} ({seeds[above % len(seeds)]}) vs. {teams[below]} ({seeds[below % len(seeds)]})"
            )

            if args.random:
                result = random_result(above, below, seeds)
                print("[1/2]: ", result + 1)
            else:
                while True:
                    result_str = input("[1/2]: ").strip()
                    if result_str in ("1", "2"):
                        result = int(result_str) - 1
                        break

            results.append(result)
            winner = below if result else above

            # Create next round matchup after every second game
            if i % 2:
                matchups.append((prev_winner, winner))

            prev_winner = winner

        bracket_data = create_bracket(results)
        print(f"\nWinner: {teams[prev_winner]}")
        print(f"Bracket: {encode(bracket_data)}")

    print()


if __name__ == "__main__":
    main()
