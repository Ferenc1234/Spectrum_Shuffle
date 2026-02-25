import random
from collections import defaultdict


# ---------------------------------------------------------------------------
# Game configuration
# ---------------------------------------------------------------------------

COLORS = ["Red", "Orange", "Yellow", "Green", "Blue", "Violet"]
BOARD_SIZE = len(COLORS)  # number of spaces on the board


# ---------------------------------------------------------------------------
# Core game logic
# ---------------------------------------------------------------------------

def create_deck():
    """Return a shuffled deck of colour cards (two cards per colour)."""
    deck = COLORS * 2
    random.shuffle(deck)
    return deck


def play_game(num_players=2):
    """
    Simulate one game of Spectrum Shuffle.

    Rules (simplified):
    - Each player starts at position 0.
    - On their turn a player draws a card and advances to the next space
      that matches the drawn colour (wrapping around the board if needed).
    - The first player to reach or pass the last space wins.

    Returns
    -------
    dict with keys:
        "winner"  – player index (0-based) of the winner
        "turns"   – total number of turns played
    """
    positions = [0] * num_players
    deck = create_deck()
    deck_index = 0
    turn = 0

    while True:
        current_player = turn % num_players

        # Replenish deck when exhausted
        if deck_index >= len(deck):
            deck = create_deck()
            deck_index = 0

        card = deck[deck_index]
        deck_index += 1

        # Advance to the next matching colour space
        color_index = COLORS.index(card)
        if color_index > positions[current_player]:
            positions[current_player] = color_index
        else:
            positions[current_player] = color_index + BOARD_SIZE  # wrap

        if positions[current_player] >= BOARD_SIZE - 1:
            return {"winner": current_player, "turns": turn + 1}

        turn += 1


# ---------------------------------------------------------------------------
# Simulation and statistics
# ---------------------------------------------------------------------------

def run_simulations(num_simulations=1000, num_players=2):
    """
    Run *num_simulations* games and return a statistics dictionary.

    Statistics collected
    --------------------
    - wins_per_player : dict mapping player index -> win count
    - avg_turns       : average number of turns per game
    - min_turns       : shortest game (in turns)
    - max_turns       : longest game (in turns)
    """
    wins_per_player = defaultdict(int)
    all_turns = []

    for _ in range(num_simulations):
        result = play_game(num_players=num_players)
        wins_per_player[result["winner"]] += 1
        all_turns.append(result["turns"])

    stats = {
        "wins_per_player": dict(wins_per_player),
        "avg_turns": sum(all_turns) / len(all_turns),
        "min_turns": min(all_turns),
        "max_turns": max(all_turns),
    }
    return stats


def print_statistics(stats, num_simulations, num_players):
    """Pretty-print the simulation statistics."""
    print(f"\n{'=' * 40}")
    print(f"  Spectrum Shuffle – Simulation Results")
    print(f"{'=' * 40}")
    print(f"  Simulations : {num_simulations}")
    print(f"  Players     : {num_players}")
    print(f"  Avg turns   : {stats['avg_turns']:.2f}")
    print(f"  Min turns   : {stats['min_turns']}")
    print(f"  Max turns   : {stats['max_turns']}")
    print(f"\n  Win rates:")
    for player in range(num_players):
        wins = stats["wins_per_player"].get(player, 0)
        rate = wins / num_simulations * 100
        print(f"    Player {player + 1}: {wins:>6} wins  ({rate:.1f} %)")
    print(f"{'=' * 40}\n")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    NUM_SIMULATIONS = 1000
    NUM_PLAYERS = 2

    stats = run_simulations(num_simulations=NUM_SIMULATIONS, num_players=NUM_PLAYERS)
    print_statistics(stats, num_simulations=NUM_SIMULATIONS, num_players=NUM_PLAYERS)
