# File for AI logic in the RPS Battle Arena game

import random
import math
from arena_template import *
from attacks import RockAttack, PaperProjectile, ScissorsCone

# RPS relationship function
def rps_relation(ai_type, player_type):
    """
    Returns:
        1  -> AI has advantage
        0  -> tie
        -1 -> AI is weak
    """
    if ai_type == player_type:
        return 0

    if (ai_type == "rock"     and player_type == "scissors") or \
       (ai_type == "paper"    and player_type == "rock")     or \
       (ai_type == "scissors" and player_type == "paper"):
        return 1  # advantage

    return -1  # disadvantage

# AI movement behavior based on RPS matchup
def ai_move_behavior(enemy, player):
    """
    AI moves differently depending on whether it has RPS advantage.
    """
    relation = rps_relation(enemy.label, player.label)

    # distance between fighters
    dx = player.x - enemy.x
    dy = player.y - enemy.y
    dist = math.sqrt(dx*dx + dy*dy)

    # desired combat ranges
    IDEAL_CLOSE = 150     # ideal range for melee attackers
    IDEAL_FAR   = 350     # ideal range for ranged / defensive

    # base speed
    speed = enemy.speed * 0.9

    # ------------------------------
    # 1. AI HAS ADVANTAGE → GET CLOSER
    # ------------------------------
    if relation == 1:
        if dist > IDEAL_CLOSE:
            enemy.x += speed * (dx / dist)
            enemy.y += speed * (dy / dist)
        if dist == 0:
            enemy.x += speed
        else:
            # circle around the player so it doesn't flicker
            enemy.x += speed * (-dy / dist)
            enemy.y += speed * (dx / dist)

    # ------------------------------------------
    # 2. AI IS WEAK → KEEP DISTANCE & KITE AWAY
    # ------------------------------------------
    elif relation == -1:
        if dist < IDEAL_FAR:
            # move AWAY from player
            enemy.x -= speed * (dx / dist)
            enemy.y -= speed * (dy / dist)
        if dist == 0:
            enemy.x += speed
        else:
            # strafe to avoid projectiles
            enemy.x += speed * (dy / dist)
            enemy.y -= speed * (dx / dist)

    # ------------------------------
    # 3. SAME TYPE → neutral behavior
    # ------------------------------
    else:
        if dist > 250:
            enemy.x += speed * (dx / dist)
            enemy.y += speed * (dy / dist)
        if dist == 0:
            enemy.x += speed
        else:
            enemy.x += speed * (-dy / dist)
            enemy.y += speed * (dx / dist)

    # Keep inside screen
    from arena_template import WIDTH, HEIGHT, size_number
    enemy.x = max(0, min(enemy.x, WIDTH - size_number))
    enemy.y = max(20, min(enemy.y, HEIGHT - size_number))


# AI attack decision based on distance
def ai_should_attack(enemy, player):
    """Attack when in a good distance relative to matchup."""
    dx = enemy.x - player.x
    dy = enemy.y - player.y
    dist = math.sqrt(dx*dx + dy*dy)

    # Aggressive types attack more often
    relation = rps_relation(enemy.label, player.label)

    if relation == 1:   # advantage
        return dist < 350

    if relation == -1:  # disadvantage
        return dist < 500  # shoot from far

    # neutral
    return dist < 400

def ai_trigger_attack(enemy, player, attacks_list):
    """Makes the enemy perform the correct attack."""
    enemy.trigger_attack()  # update cooldown timer

    if enemy.label == "rock":
        attacks_list.append(RockAttack(enemy))

    elif enemy.label == "paper":
        mx = player.x + 40
        my = player.y + 40
        attacks_list.append(PaperProjectile(enemy.x + 75, enemy.y + 75, mx, my))

    elif enemy.label == "scissors":
        mx, my = player.x, player.y
        attacks_list.append(ScissorsCone(enemy, (mx, my)))