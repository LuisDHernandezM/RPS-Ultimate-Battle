# General code for a Rock-Paper-Scissors game

import random

def get_computer_choice():
    choices = ['rock', 'paper', 'scissors']
    return random.choice(choices)

def determine_winner(user_choice, computer_choice):
    if user_choice == computer_choice:
        return 'tie'
    elif (user_choice == 'rock' and computer_choice == 'scissors') or \
         (user_choice == 'paper' and computer_choice == 'rock') or \
         (user_choice == 'scissors' and computer_choice == 'paper'):
        return 'user'
    else:
        return 'computer'
    
def play_game(user_choice):
    computer_choice = get_computer_choice()
    winner = determine_winner(user_choice, computer_choice)
    return {
        'user_choice': user_choice,
        'computer_choice': computer_choice,
        'winner': winner
    }

# Example usage:
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

#     print("Thank you for playing!")
#     if __name__ == "__main__":
#         main()
