import pygame
from pygame.locals import QUIT, MOUSEMOTION, MOUSEBUTTONDOWN, MOUSEBUTTONUP

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
DRAW_COLOR = (0, 255, 0)
DRAW_RADIUS = 5

# Set up the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simple Drawing App")

# Variables
drawing = False
points = []  # Current drawing points
lines = []   # List to store completed lines

# Main loop
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        elif event.type == MOUSEBUTTONDOWN:
            drawing = True
            points = []  # Clear points when starting a new line
        elif event.type == MOUSEBUTTONUP:
            drawing = False
            if points:  # Save the completed line when the mouse is released
                lines.append(points)
        elif event.type == MOUSEMOTION:
            if drawing:
                x, y = event.pos
                points.append((x, y))

    # Draw on the screen
    screen.fill(BLACK)

    # Draw completed lines
    for line in lines:
        if len(line) >= 2:
            pygame.draw.lines(screen, DRAW_COLOR, False, line, DRAW_RADIUS)

    # Draw the current line
    if len(points) >= 2:
        pygame.draw.lines(screen, DRAW_COLOR, False, points, DRAW_RADIUS)

    # Update the display
    pygame.display.flip()
