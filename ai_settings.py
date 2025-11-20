# File for AI logic in the RPS Battle Arena game

import random


player_history = {"rock": 0, "paper": 0, "scissors": 0}

def ai_move_random():
    return random.choice(["rock", "paper", "scissors"])

def ai_move_counter(player_move):
    counters = {"rock": "paper", "paper": "scissors", "scissors": "rock"}
    return counters[player_move]

def ai_move_learning():
    predicted = max(player_history, key=player_history.get)
    counters = {"rock": "paper", "paper": "scissors", "scissors": "rock"}
    return counters[predicted]

def ai_move(player_move, difficulty="easy"):
    player_history[player_move] += 1

    if difficulty == "easy":
        return ai_move_random()
    elif difficulty == "medium":
        return ai_move_counter(player_move)
    else:
        return ai_move_learning()