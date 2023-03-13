import base64
import os
import argparse
from random import SystemRandom


# 64 team bracket encodes to 12 characters
# can be made 11 by removing the ending padding `=` byte
def encode(bracket_data: bytes) -> str:
    return base64.urlsafe_b64encode(bracket_data).rstrip(b"=").decode("ascii")


def decode(bracket: str) -> bytes:
    return base64.urlsafe_b64decode(bracket + "===")


def random():
    bracket_data = os.urandom(8)
    last_byte = bracket_data[-1] & 0b1111111
    return bracket_data[:7] + bytes([last_byte])


rand = SystemRandom()

SEEDS = [1, 16, 8, 9, 5, 12, 4, 13, 6, 11, 3, 14, 7, 10, 2, 15]


def random_result(first_index: int, second_index: int):
    first_seed = SEEDS[first_index % 16]
    second_seed = SEEDS[second_index % 16]
    seed_quotient = second_seed / (first_seed + second_seed)
    return int(rand.random() > seed_quotient)


def iter_results(bracket_data: bytes):
    for byte in bracket_data:
        for i in range(8):
            yield (byte >> i) & 1


def generate_matchups(bracket_data: bytes, number_of_teams: int) -> list:
    last = None
    matchups = list((i, i + 1) for i in range(0, number_of_teams, 2))
    for i, (result, matchup) in enumerate(zip(iter_results(bracket_data), matchups)):
        winner = matchup[result]
        if i % 2:
            matchups.append((last, winner))
        last = winner

    matchups.append((winner, winner))
    return matchups


def create_bracket(number_of_teams: int) -> list:
    last = None
    matchups = list((i, i + 1) for i in range(0, number_of_teams, 2))
    results = []
    result_byte = 0
    for i, matchup in enumerate(matchups):
        result = yield matchup
        result_index = i % 8
        result_byte |= result << result_index
        winner = matchup[result]
        if i % 2:
            matchups.append((last, winner))
        if result_index == 7:
            results.append(result_byte)
            result_byte = 0

        last = winner
    if i % 8:
        results.append(result_byte)
    return bytes(results)


def _draw(matchups: list, teams: list):
    i = 0
    round = len(teams)
    next_round = round // 2
    yield "flowchart LR"
    for above, below in matchups:
        prefix = f"    {round}-{i}"
        matchup = f"{teams[above]} vs. {teams[below]}" if next_round else teams[above]
        suffix = f" --> {next_round}-{i // 2}" if next_round else ""
        yield f"{prefix}[{matchup}]{suffix}"
        i += 1
        if i >= next_round:
            i = 0
            round = next_round
            next_round //= 2


def draw(matchups: list, teams: list):
    return "\n".join(_draw(matchups, teams))


def main():
    parser = argparse.ArgumentParser("flatbracket", description="")
    parser.add_argument("teams", type=str, help="file containing teams list")
    parser.add_argument(
        "bracket",
        type=str,
        nargs="?",
        help="encoded bracket",
    )
    parser.add_argument(
        "-r",
        "--random",
        action="store_true",
        help="create random bracket",
    )
    args = parser.parse_args()

    with open(args.teams) as file:
        teams = [line.rstrip() for line in file]

    bracket = args.bracket

    if bracket:
        print(f"Bracket: {bracket}")
        bracket_data = decode(bracket)
        print()

        diagram = draw(generate_matchups(bracket_data, len(teams)), teams)
        print(diagram)
    else:
        coro = create_bracket(len(teams))
        high, low = next(coro)
        bracket_data = None
        while bracket_data is None:
            print(f"{teams[high]} vs. {teams[low]}")
            if args.random:
                result = random_result(high, low)
                print(result)
            else:
                result = None
                while result is None:
                    result_str = input("[0/1]: ").strip()
                    if result_str not in ("0", "1"):
                        continue
                    result = int(result_str)
            try:
                high, low = coro.send(result)
            except StopIteration as exc:
                bracket_data = exc.value
        print()
        print("Bracket:", encode(bracket_data))
    print()


if __name__ == "__main__":
    main()
