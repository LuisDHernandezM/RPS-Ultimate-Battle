# Canvas for the character making in the rps game
# Keeping user's character as drawing

import pygame # type: ignore
import sys
from preprocess import preprocess_image
import numpy as np
import torch # type: ignore
import numpy as np
from preprocess import preprocess_image


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

classes = ["rock", "paper", "scissors"]

# Load PyTorch model
from train_classifier_pytorch import RPScnn

model = RPScnn()
model.load_state_dict(torch.load("rps_model.pt", weights_only=True))
model.eval()

def classify_image(path="drawing.png"):
    img = preprocess_image(path)  # (64,64,1)
    img = np.transpose(img, (2,0,1))  # (1,64,64)
    img = torch.tensor(img, dtype=torch.float32).unsqueeze(0)  # (1,1,64,64)

    with torch.no_grad():
        output = model(img)
        prediction = torch.argmax(output, dim=1).item()

    return classes[prediction]

while True:
    number = 1
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
                result = classify_image("drawing.png")
                print("You drew:", result)
            if event.key == pygame.K_ESCAPE:
                player_choice = classify_image("drawing.png")
                pygame.quit()
                sys.exit()

    # Continue drawing while mouse moves
    if drawing:
        mouse_pos = pygame.mouse.get_pos()
        if last_pos is not None:
            draw_line(screen, last_pos, mouse_pos)
        last_pos = mouse_pos

    pygame.display.update()


# decition stored in player_choice variable
