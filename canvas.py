# Canvas for the character making in the rps game
# Keeping user's character as drawing

import pygame # type: ignore
import sys
from preprocess import preprocess_image
import numpy as np
import torch # type: ignore
import numpy as np
from preprocess import preprocess_image

classes = ['paper', 'rock', 'scissors']

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

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
brush_size = 8
last_pos = None

def draw_line(surface, start, end):
    pygame.draw.line(surface, BLACK, start, end, brush_size)

def erase_line(surface, start, end):
    pygame.draw.line(surface, WHITE, start, end, 20)

def draw_character():
    pygame.init()
    screen = pygame.display.set_mode((500, 500))
    pygame.display.set_caption("Draw your character")

    drawing = False
    erasing = False
    clock = pygame.time.Clock()

    # White canvas
    screen.fill((WHITE))

    running = True
    while running:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Start drawing
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:   # left mouse button
                    drawing = True
                    last_pos = event.pos
            
            # Start erasing
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 3:   # right mouse button
                    erasing = True
                    last_pos = event.pos

            # Stop drawing
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    drawing = False
                    last_pos = None
                elif event.button == 3:
                    erasing = False
                    last_pos = None

            # Detect keyboard shortcuts
            if event.type == pygame.KEYDOWN:

                # Clear screen (C)
                if event.key == pygame.K_c:
                    screen.fill(WHITE)  # clear screen

                # Save and classify drawing (S) fro checking correctness of users input
                if event.key == pygame.K_s:
                    pygame.image.save(screen, "player_drawing.png")
                    result = classify_image("player_drawing.png")
                    print("You drew:", result)

                # Finish drawing and exit (ENTER)
                if event.key == pygame.K_RETURN:
                    pygame.image.save(screen, "player_drawing.png")

                    # run classifier
                    label = classify_image("player_drawing.png")  
                    
                    pygame.quit()
                    return "player_drawing.png", label

            # Continue drawing while mouse moves
        if drawing:
            mouse_pos = pygame.mouse.get_pos()
            if last_pos is not None:
                draw_line(screen, last_pos, mouse_pos)
            last_pos = mouse_pos
        if erasing:
            mouse_pos = pygame.mouse.get_pos()
            if last_pos is not None:
                erase_line(screen, last_pos, mouse_pos)
            last_pos = mouse_pos

        pygame.display.update()

    pygame.quit()
    return None, None  # if window closed

# decition stored in player_choice variable
