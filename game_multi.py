# Game loop for multiplyer mode
from canvas import draw_character
from arena_template import *
from ai_settings import *
from attacks import *
import pygame  # type: ignore
import sys
import time
import math

def game_multi():
    print("Starting two player mode!")

    while True:
        print("Player 1's turn:")
        p1 = draw_character()

        print("Player 2's turn:")
        p2 = draw_character()

        print(f"P1: {p1} | P2: {p2}")
        # result = determine_winner(p1, p2)
        # print(result)