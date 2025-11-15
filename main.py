# Main file for rps game
from rps import play_game
import random

if __name__ == "__main__":
    user_choice = input("Enter rock, paper, or scissors: ").lower()
    result = play_game(user_choice)
    print(f"You chose: {result['user_choice']}")
    print(f"Computer chose: {result['computer_choice']}")
    if result['winner'] == 'tie':
        print("It's a tie!")
    elif result['winner'] == 'user':
        print("You win!")
    else:
        print("Computer wins!")
    print("Thank you for playing!")

#     print("Thank you for playing!")