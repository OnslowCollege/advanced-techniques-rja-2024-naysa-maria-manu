import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
CARD_WIDTH, CARD_HEIGHT = 100, 150
CARD_SPACING = 10
NUM_CARDS = 7
BUTTON_COLOR = (0, 0, 0)
TEXT_COLOR = (255, 255, 255)
FONT_SIZE = 20
REVEAL_BUTTON_SIZE = (150, 50)
SHOW_BUTTON_SIZE = (100, 50)

# Load card images
def load_card_images():
    card_images = {}
    colors = ["red", "green", "blue", "yellow"]
    for color in colors:
        for i in range(10):  # Numbers 0-9
            card_images[f"{color}_{i}"] = pygame.image.load(f"{color}_{i}.jpg")
        for special in ["+2", "rev", "skip"]:  # Special cards
            card_images[f"{color}_{special}"] = pygame.image.load(
                f"{color}_{special}.jpg"
            )
    card_images["UNO_+4"] = pygame.image.load("UNO_+4.jpg")
    return card_images

card_images = load_card_images()

# Define Button class
class Button:
    def __init__(self, text, pos, size, bg_color, text_color, font):
        self.text = text
        self.pos = pos
        self.size = size
        self.bg_color = bg_color
        self.text_color = text_color
        self.font = font

    def draw(self, screen):
        pygame.draw.rect(screen, self.bg_color, (*self.pos, *self.size))
        text_surface = self.font.render(self.text, True, self.text_color)
        screen.blit(
            text_surface,
            (
                self.pos[0] + (self.size[0] - text_surface.get_width()) // 2,
                self.pos[1] + (self.size[1] - text_surface.get_height()) // 2,
            ),
        )

    def is_clicked(self, event):
        x, y = event.pos
        rect = pygame.Rect(
            self.pos[0], self.pos[1], self.size[0], self.size[1]
        )
        return rect.collidepoint(x, y)

# Load fonts
font = pygame.font.Font(None, FONT_SIZE)

# Game state
state = "home"
current_turn = "player"
player_cards = [f"red_{i}" for i in range(NUM_CARDS)]  # Example player's cards
computer_cards = [
    f"blue_{i}" for i in range(NUM_CARDS)
]  # Example computer's cards
discard_pile = ["red_0"]  # Example discard pile
reveal_cards = False

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Uno Game")

# Create buttons
start_button = Button(
    "Start",
    (SCREEN_WIDTH // 2 - 75, SCREEN_HEIGHT // 2 - 25),
    (150, 50),
    BUTTON_COLOR,
    TEXT_COLOR,
    font,
)
reveal_button = Button(
    "Reveal Cards",
    (
        SCREEN_WIDTH // 2 - REVEAL_BUTTON_SIZE[0] // 2,
        SCREEN_HEIGHT // 2 - REVEAL_BUTTON_SIZE[1] // 2,
    ),
    REVEAL_BUTTON_SIZE,
    BUTTON_COLOR,
    TEXT_COLOR,
    font,
)
show_button = Button(
    "Show",
    (
        SCREEN_WIDTH // 2 + REVEAL_BUTTON_SIZE[0] // 2 + 10,
        SCREEN_HEIGHT // 2 - SHOW_BUTTON_SIZE[1] // 2,
    ),
    SHOW_BUTTON_SIZE,
    BUTTON_COLOR,
    TEXT_COLOR,
    font,
)

def home_screen():
    """Display the home screen."""
    screen.fill((255, 255, 255))
    start_button.draw(screen)
    pygame.display.flip()

def game_screen():
    """Display the game screen with cards."""
    screen.fill((255, 255, 255))
    # Display computer's cards
    for i in range(NUM_CARDS):
        x = (
            i * (CARD_WIDTH + CARD_SPACING)
            + (SCREEN_WIDTH - ((CARD_WIDTH + CARD_SPACING) * NUM_CARDS)) // 2
        )
        y = 20
        pygame.draw.rect(
            screen, (0, 0, 0), (x, y, CARD_WIDTH, CARD_HEIGHT)
        )  # Placeholder for card back

    # Display player's cards
    mid_x = SCREEN_WIDTH // 2.2
    positions = [
        (
            mid_x - 3 * CARD_WIDTH - 3 * CARD_SPACING,
            SCREEN_HEIGHT - CARD_HEIGHT - 100,
        ),
        (
            mid_x - 2 * CARD_WIDTH - 2 * CARD_SPACING,
            SCREEN_HEIGHT - CARD_HEIGHT - 60,
        ),
        (mid_x - CARD_WIDTH - CARD_SPACING, SCREEN_HEIGHT - CARD_HEIGHT - 20),
        (mid_x - CARD_WIDTH // 25, SCREEN_HEIGHT - CARD_HEIGHT - 20),
        (mid_x + CARD_WIDTH + CARD_SPACING, SCREEN_HEIGHT - CARD_HEIGHT - 20),
        (
            mid_x + 2 * CARD_WIDTH + 2 * CARD_SPACING,
            SCREEN_HEIGHT - CARD_HEIGHT - 60,
        ),
        (
            mid_x + 3 * CARD_WIDTH + 3 * CARD_SPACING,
            SCREEN_HEIGHT - CARD_HEIGHT - 100,
        ),
    ]

    for i in range(NUM_CARDS):
        card_key = player_cards[i]
        if reveal_cards:
            screen.blit(card_images[card_key], positions[i])
        else:
            pygame.draw.rect(
                screen, (0, 0, 0), (*positions[i], CARD_WIDTH, CARD_HEIGHT)
            )  # Placeholder for card back

    # Draw the Reveal Cards button
    if reveal_button:
        reveal_button.draw(screen)

    # Draw the Show Card button
    if reveal_cards and show_button:
        show_button.draw(screen)

    # Display discard pile
    if discard_pile:
        top_card = discard_pile[-1]
        top_card_image = card_images[top_card]
        screen.blit(
            top_card_image,
            (
                SCREEN_WIDTH // 2 - CARD_WIDTH // 2,
                SCREEN_HEIGHT // 2 - CARD_HEIGHT // 2,
            ),
        )

    pygame.display.flip()

def player_turn(card_index):
    """Handle player's turn logic."""
    # Logic for player's turn (play a card, draw a card, etc.)
    pass

def computer_turn():
    """Handle computer's turn logic."""
    # Simple computer AI to play a card or draw a card
    pass

def play_game():
    """Main game loop."""
    global state, reveal_cards, show_button
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if state == "home" and start_button.is_clicked(event):
                    state = "game"
                elif (
                    state == "game"
                    and reveal_button.is_clicked(event)
                    and not reveal_cards
                ):
                    reveal_cards = True
                    reveal_button = None  # Remove reveal button after clicking
                elif (
                    state == "game"
                    and reveal_cards
                    and show_button.is_clicked(event)
                ):
                    if player_cards:  # Ensure there is a card to show
                        selected_card = player_cards[0]
                        print(f"Showing card {selected_card} to the computer")
                        player_cards.remove(selected_card)
                        show_button = None  # Remove show button after clicking
                elif state == "game" and current_turn == "player":
                    for i, card in enumerate(player_cards):
                        x = (
                            i * (CARD_WIDTH + CARD_SPACING)
                            + (
                                SCREEN_WIDTH
                                - ((CARD_WIDTH + CARD_SPACING) * NUM_CARDS)
                            )
                            // 2
                        )
                        y = SCREEN_HEIGHT - CARD_HEIGHT - 30
                        card_rect = pygame.Rect(x, y, CARD_WIDTH, CARD_HEIGHT)
                        if card_rect.collidepoint(event.pos):
                            player_turn(i)
                            break
                elif state == "game" and current_turn == "computer":
                    computer_turn()
                    if not computer_cards:
                        print("Computer wins!")
                        state = "home"
                    elif not player_cards:
                        print("Player wins!")
                        state = "home"

        if state == "home":
            home_screen()
        elif state == "game":
            game_screen()
            if current_turn == "computer":
                computer_turn()
                if not computer_cards:
                    print("Computer wins!")
                    state = "home"
            if not player_cards:
                print("Player wins!")
                state = "home"

        pygame.display.flip()

    pygame.quit()
    sys.exit()

# Start the game
play_game()
