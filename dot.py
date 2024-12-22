import pygame
import sys
import math

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dot Connect Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Clock and FPS
clock = pygame.time.Clock()
FPS = 60

# Grid settings
GRID_SIZE = 5
DOT_RADIUS = 10
DOT_SPACING = 100

# Font for score
font = pygame.font.Font(None, 36)

# Dot class
class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = DOT_RADIUS
        self.color = BLUE

    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)

# Line class
class Line:
    def __init__(self, start_dot, end_dot):
        self.start_dot = start_dot
        self.end_dot = end_dot
        self.color = RED

    def draw(self):
        pygame.draw.line(screen, self.color, (self.start_dot.x, self.start_dot.y), (self.end_dot.x, self.end_dot.y), 5)

    def intersects(self, other_line):
        def ccw(A, B, C):
            return (C.y - A.y) * (B.x - A.x) > (B.y - A.y) * (C.x - A.x)

        A = self.start_dot
        B = self.end_dot
        C = other_line.start_dot
        D = other_line.end_dot

        return ccw(A, C, D) != ccw(B, C, D) and ccw(A, B, C) != ccw(A, B, D)

# Main game function
def game():
    running = True
    dots = []
    lines = []
    selected_dot = None
    score = 0

    # Create grid of dots
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            x = DOT_SPACING * (i + 1)
            y = DOT_SPACING * (j + 1)
            dots.append(Dot(x, y))

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                for dot in dots:
                    if math.hypot(dot.x - mouse_x, dot.y - mouse_y) < DOT_RADIUS:
                        selected_dot = dot
                        break
            if event.type == pygame.MOUSEBUTTONUP:
                if selected_dot:
                    mouse_x, mouse_y = event.pos
                    for dot in dots:
                        if dot != selected_dot and math.hypot(dot.x - mouse_x, dot.y - mouse_y) < DOT_RADIUS:
                            new_line = Line(selected_dot, dot)
                            if not any(line.intersects(new_line) for line in lines):
                                lines.append(new_line)
                                score += 1
                            break
                    selected_dot = None

        # Clear screen
        screen.fill(WHITE)

        # Draw dots
        for dot in dots:
            dot.draw()

        # Draw lines
        for line in lines:
            line.draw()

        # Draw temporary line
        if selected_dot:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            pygame.draw.line(screen, RED, (selected_dot.x, selected_dot.y), (mouse_x, mouse_y), 5)

        # Draw score
        score_text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))

        # Update display
        pygame.display.update()

        # Set the frame rate
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

# Start the game
if __name__ == "__main__":
    game()