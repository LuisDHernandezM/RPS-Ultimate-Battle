# Canvas for the character making in the rps game
# Keeping user's character as drawing

import pygame # type: ignore
import sys

# Initialize Pygame
pygame.init()

# Canvas size
WIDTH, HEIGHT = 500, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Draw Your Character")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Fill background
screen.fill(WHITE)

drawing = False
last_pos = None
brush_size = 8   # thickness of line

def draw_line(surface, start, end):
    pygame.draw.line(surface, BLACK, start, end, brush_size)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Start drawing
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:   # left mouse button
                drawing = True
                last_pos = event.pos

        # Stop drawing
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                drawing = False
                last_pos = None

        # Detect keyboard shortcuts
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_c:
                screen.fill(WHITE)  # clear screen
            if event.key == pygame.K_s:
                pygame.image.save(screen, "drawing.png")
                print("Saved drawing as drawing.png")
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

    # Continue drawing while mouse moves
    if drawing:
        mouse_pos = pygame.mouse.get_pos()
        if last_pos is not None:
            draw_line(screen, last_pos, mouse_pos)
        last_pos = mouse_pos

    pygame.display.update()