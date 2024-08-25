import pygame
import random
import time

# Initialize pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 600, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Memory Puzzle Game")

# Colors (lightened)
WHITE = (255, 255, 255)
LIGHT_GRAY = (200, 200, 200)
LIGHT_BLUE = (173, 216, 230)
LIGHT_PINK = (255, 182, 193)
BLACK = (0, 0, 0)

# Grid settings
GRID_SIZE = 4  # 4x4 grid
CARD_WIDTH = SCREEN_WIDTH // GRID_SIZE
CARD_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Load symbols or numbers for cards
symbols = list(range(1, (GRID_SIZE * GRID_SIZE // 2) + 1)) * 2
random.shuffle(symbols)

# Game variables
revealed = [[False] * GRID_SIZE for _ in range(GRID_SIZE)]
cards = [[symbols.pop() for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
first_selection = None
start_time = time.time()
TIME_LIMIT = 60  # 60 seconds
waiting = False
wrong_guesses = []

def draw_grid():
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            x = col * CARD_WIDTH
            y = row * CARD_HEIGHT
            if revealed[row][col] or (row, col) in wrong_guesses:
                pygame.draw.rect(screen, WHITE, (x, y, CARD_WIDTH, CARD_HEIGHT))
                font = pygame.font.Font(None, 80)
                text = font.render(str(cards[row][col]), True, BLACK)
                screen.blit(text, (x + CARD_WIDTH // 2 - text.get_width() // 2, y + CARD_HEIGHT // 2 - text.get_height() // 2))
            else:
                pygame.draw.rect(screen, LIGHT_PINK, (x, y, CARD_WIDTH, CARD_HEIGHT))
            pygame.draw.rect(screen, LIGHT_GRAY, (x, y, CARD_WIDTH, CARD_HEIGHT), 2)

def check_win():
    for row in revealed:
        if not all(row):
            return False
    return True

# Main game loop
running = True
while running:
    screen.fill(LIGHT_BLUE)

    # Draw grid
    draw_grid()

    # Check timer
    elapsed_time = time.time() - start_time
    if elapsed_time >= TIME_LIMIT:
        running = False
        print("Time's up! You lost.")

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and not waiting:
            x, y = pygame.mouse.get_pos()
            row, col = y // CARD_HEIGHT, x // CARD_WIDTH

            if not revealed[row][col] and (row, col) not in wrong_guesses:
                if first_selection is None:
                    first_selection = (row, col)
                    revealed[row][col] = True
                else:
                    first_row, first_col = first_selection
                    revealed[row][col] = True

                    if cards[first_row][first_col] == cards[row][col]:
                        revealed[row][col] = True
                        first_selection = None
                        if check_win():
                            running = False
                            print("You won!")
                    else:
                        wrong_guesses = [(first_row, first_col), (row, col)]
                        first_selection = None
                        waiting = True
                        pygame.time.set_timer(pygame.USEREVENT, 1000)  # Delay for 1 second

    if event.type == pygame.USEREVENT and waiting:
        revealed[wrong_guesses[0][0]][wrong_guesses[0][1]] = False
        revealed[wrong_guesses[1][0]][wrong_guesses[1][1]] = False
        wrong_guesses = []
        waiting = False

    # Update display
    pygame.display.flip()

pygame.quit()
