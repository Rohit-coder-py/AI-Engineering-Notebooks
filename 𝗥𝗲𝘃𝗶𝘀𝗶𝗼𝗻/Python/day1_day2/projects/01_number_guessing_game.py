"""
PROJECT 1 (SOLVED) - Number Guessing Game
Concepts: while loop, if/elif/else, break, input validation, try/except,
type conversion, lists, f-strings.
"""
import random


def get_int(prompt, low, high):
    """Keep asking until user enters an int within [low, high]."""
    while True:
        raw = input(prompt).strip()
        try:
            value = int(raw)
        except ValueError:
            print("  Please enter a whole number.")
            continue
        if not low <= value <= high:
            print(f"  Number must be between {low} and {high}.")
            continue
        return value


def play_round(low=1, high=100, max_attempts=7):
    secret = random.randint(low, high)
    guesses = []
    print(f"\nI'm thinking of a number between {low} and {high}. You have {max_attempts} tries.")

    attempt = 0
    while attempt < max_attempts:
        guess = get_int(f"Attempt {attempt + 1}/{max_attempts}: ", low, high)
        if guess in guesses:
            print("  You already tried that! (no attempt used)")
            continue                      # repeated guess doesn't cost an attempt
        guesses.append(guess)
        attempt += 1

        if guess == secret:
            print(f"Correct! You got it in {attempt} attempt(s).")
            return attempt
        hint = "higher" if guess < secret else "lower"
        close = " (very close!)" if abs(guess - secret) <= 5 else ""
        print(f"  Go {hint}.{close}")
    print(f"Out of attempts. The number was {secret}.")
    return None


def main():
    scores = []          # attempts used in won rounds
    played = 0
    while True:
        played += 1
        result = play_round()
        if result is not None:
            scores.append(result)
        again = input("Play again? (y/n): ").strip().lower()
        if again != "y":
            break

    print("\n--- Summary ---")
    print(f"Rounds played: {played} | Won: {len(scores)}")
    if scores:
        print(f"Best: {min(scores)} attempts | Average: {sum(scores) / len(scores):.1f}")


if __name__ == "__main__":
    main()
