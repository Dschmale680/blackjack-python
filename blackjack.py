# AI DEVELOPMENT LOG
#
# Copilot Prompt 1:Help me create a simple terminal-based Blackjack game in Python.
#
# Copilot Prompt 2:Make the code simple
#
# Copilot Prompt 3:Fix any issues with the code
#
# One problem or bug I encountered:I had to allow some iems to be done multiple times
#
# How I fixed it:Allow always
#
# One change I made myself without Copilot:I added hope to see you again after the thanks for playing promt
#
# One thing I learned about the Python code:It is a whole new language that I have a lot of respect for anyone that does this day in and day out 
#1. Calculate_score(hand) is what would determine the total value of a hand. It takes a list of cards as an input,loops through each card to check its rank against the card_values dictonary, and sums up the points to get the total hand score.
#2. The value of the ace is 11 right after summing the inital score it checks if the total equals 21
#3. During the testing a bug occurred where the script crashed after an instant natural blackjack tie. This was corrected by tracking the return paths for opening hands and ensuring the default chips variable was explicity returned during a push.
import random

CARD_VALUES = {
    '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10,
    'J': 10, 'Q': 10, 'K': 10, 'A': 11
}

def create_shoe():
    """Generates a shuffled 4-deck shoe of cards."""
    suits = ['♠', '♥', '♦', '♣']
    ranks = list(CARD_VALUES.keys())
    deck = [f"{rank}{suit}" for rank in ranks for suit in suits] * 4
    random.shuffle(deck)
    return deck

def calculate_score(hand):
    """Calculates total score, converting Aces from 11 to 1 if busting."""
    score = sum(CARD_VALUES[card[:-1]] for card in hand)
    aces = sum(1 for card in hand if card.startswith('A'))
    while score > 21 and aces:
        score -= 10
        aces -= 1
    return score

def display_table(player, dealer, chips, bet, hide_dealer=True):
    """Prints the hands and current bankroll status."""
    print(f"\n CHIPS: ${chips} | BET: ${bet}")
    print("-" * 30)
    if hide_dealer:
        print(f"Dealer's Hand: [{dealer[0]}, ??]")
    else:
        print(f"Dealer's Hand: {', '.join(dealer)} (Score: {calculate_score(dealer)})")
    print(f"Your Hand:     {', '.join(player)} (Score: {calculate_score(player)})")
    print("-" * 30)

def play_round(chips, deck):
    """Runs a single round of Blackjack."""
    while True: # Get valid bet
        try:
            bet = int(input(f"\nEnter your bet (1-{chips}): "))
            if 1 <= bet <= chips: break
            print("Invalid amount.")
        except ValueError:
            print("Please enter a number.")

    player = [deck.pop(), deck.pop()]
    dealer = [deck.pop(), deck.pop()]

    # Player Turn
    while calculate_score(player) < 21:
        display_table(player, dealer, chips, bet, hide_dealer=True)
        choice = input("Do you want to [H]it or [S]tand? ").strip().lower()
        if choice == 'h':
            player.append(deck.pop())
        elif choice == 's':
            break

    p_score = calculate_score(player)
    if p_score > 21:
        display_table(player, dealer, chips, bet, hide_dealer=False)
        print("💥 Bust! You went over 21. Dealer wins.")
        return chips - bet

    # Dealer Turn
    while calculate_score(dealer) < 17:
        dealer.append(deck.pop())

    display_table(player, dealer, chips, bet, hide_dealer=False)
    d_score = calculate_score(dealer)

    # Resolution
    if d_score > 21:
        print(f"Dealer busts! You win ${bet}.")
        return chips + bet
    elif p_score > d_score:
        print(f"You win ${bet}!")
        return chips + bet
    elif p_score < d_score:
        print(f"Dealer wins. Lost ${bet}.")
        return chips - bet
    else:
        print("It's a push (tie). Bet returned.")
        return chips

def main():
    print("Welcome to Simple Terminal Blackjack!")
    chips = 100
    deck = create_shoe()

    while chips > 0:
        if len(deck) < 15: # Reload deck if running low
            deck = create_shoe()
        chips = play_round(chips, deck)
        
        if chips <= 0:
            print("\n❌ Out of chips! Game Over.")
            break
        if input("\nPlay another hand? (y/n): ").strip().lower() != 'y':
            break

    print(f"\nFinal Bankroll: ${chips}. Thanks for playing!")

if __name__ == "__main__":
    main()
print("Hope to see you again!")
