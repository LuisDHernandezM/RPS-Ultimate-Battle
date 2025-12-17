# Wrote by Luis D. Hernandez with assistance from ChatGPT and GenAI
# Date: December 2025
# Main file for rps game

from game_single import game_single
from game_multi import game_multi

def main():
    print("=== Welcome to RPS Ultimate Battle ===")
    print("1) Single Player (vs AI)")
    print("2) Multiplayer")
    
    choice = input("Choose a mode (1 or 2): ").strip()

    if choice == "1":
        game_single()
    elif choice == "2":
        game_multi()
    else:
        print("Invalid option!")

if __name__ == "__main__":
    main()