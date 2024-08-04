import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 960
SCREEN_HEIGHT = 545
COLOR_RED = (176, 39, 47)
FONT_PATH = "Text_features/Font_mont.ttf"
CARD_FONT_PATH = "Text_features/Comic.ttf"
HOME_BACKGROUND_IMAGE = "images/UNO_Home.jpg"
GAME_BACKGROUND_IMAGE = "images/UNO_bg.jpg"
# Number of cards per player
NUM_CARDS = 7
# Scale down the cards size down by 47%
CARD_SCALE = 0.47
# Space between cards
CARD_SPACING = 10
# Size of the Reveal Cards button
REVEAL_BUTTON_SIZE = (270, 60)

# Define the new colors
BUTTON_COLOR = COLOR_RED
TEXT_COLOR = (254, 245, 185)

# Define card colors and types
card_colors = ["blue", "red", "yellow", "green"]
special_cards = ["+2", "rev", "skip"]
wild_cards = ["+4"]

# Load images and fonts
home_background_image = pygame.image.load(HOME_BACKGROUND_IMAGE)
game_background_image = pygame.image.load(GAME_BACKGROUND_IMAGE)

font = pygame.font.Font(FONT_PATH, 40)
font_card = pygame.font.Font(CARD_FONT_PATH, 60)

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.setCaption("Uno Game")

# Define card images dictionary
card_images = {}


# Load and scale card images
def load_and_scale_card_images():
    global card_images
    card_images = {}

    # Load number cards
    for color in card_colors:
        for number in range(10):
            card_name = f"{color}_{number}.jpg"
            card_image = pygame.image.load(f"images/{card_name}")
            card_images[f"{color}_{number}"] = pygame.transform.scale(
                card_image,
                (
                    int(card_image.get_width() * CARD_SCALE),
                    int(card_image.get_height() * CARD_SCALE),
                ),
            )

    # Load special cards
    for color in card_colors:
        for special in special_cards:
            card_name = f"{color}_{special}.jpg"
            card_image = pygame.image.load(f"images/{card_name}")
            card_images[f"{color}_{special}"] = pygame.transform.scale(
                card_image,
                (
                    int(card_image.get_width() * CARD_SCALE),
                    int(card_image.get_height() * CARD_SCALE),
                ),
            )

    # Load wild cards
    for wild in wild_cards:
        card_name = f"UNO_{wild}.jpg"
        card_image = pygame.image.load(f"images/{card_name}")
        card_images[wild] = pygame.transform.scale(
            card_image,
            (
                int(card_image.get_width() * CARD_SCALE),
                int(card_image.get_height() * CARD_SCALE),
            ),
        )

load_and_scale_card_images()

class Button:
    """A class to represent buttons in the game."""

    def __init__(self, text, pos, size, color, text_color, font):
        self.text = text
        self.pos = pos
        self.size = size
        self.color = color
        self.text_color = text_color
        self.font = font
        self.rect = pygame.Rect(pos, size)
        self.rendered_text = self.font.render(
            text, True, self.text_color
        )  # Text color
        self.text_rect = self.rendered_text.get_rect(center=self.rect.center)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        surface.blit(self.rendered_text, self.text_rect)

    def is_clicked(self, event):
        if (
            event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
            and self.rect.collidepoint(event.pos)
        ):
            return True
        return False


# Create buttons
start_button = Button(
    "Start", (400, 350), (200, 80), COLOR_RED, (255, 255, 255), font
)
shuffle_play_button = Button(
    "Shuffle and Play", (300, 350), (400, 80), COLOR_RED, (255, 255, 255), font
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

# Game state
state = "home"
reveal_cards = False
player_cards = []
computer_cards = []


def shuffle_and_deal():
    global player_cards, computer_cards
    deck = [
        f"{color}_{number}" for color in card_colors for number in range(10)
    ]
    deck += [
        f"{color}_{special}"
        for color in card_colors
        for special in special_cards
    ]
    deck += [wild for wild in wild_cards] * 4  # 4 wild cards
    random.shuffle(deck)
    player_cards = deck[:NUM_CARDS]
    computer_cards = deck[NUM_CARDS : NUM_CARDS * 2]

def home_screen():
    """Display the home screen with the start button."""
    screen.blit(home_background_image, (0, 0))
    start_button.draw(screen)


def game_screen():
    """Display the game screen with the shuffle and play button."""
    screen.blit(game_background_image, (0, 0))
    shuffle_play_button.draw(screen)


def play_game():
    """Display the game screen with cards."""
    screen.blit(game_background_image, (0, 0))

    # Display computer's cards
    card_width, card_height = list(card_images.values())[0].get_size()
    for i in range(NUM_CARDS):
        x = (
            i * (card_width + CARD_SPACING)
            + (SCREEN_WIDTH - ((card_width + CARD_SPACING) * NUM_CARDS)) // 2
        )
        y = 20
        screen.blit(
            card_images["blue_0"], (x, y)
        )  # Assuming blue_0.jpg as the back of the card

    # Display player's cards in a U-shape
    mid_x = SCREEN_WIDTH // 2
    positions = [
        # left bottom
        (
            mid_x - 3 * card_width - 3 * CARD_SPACING,
            SCREEN_HEIGHT - card_height - 100,
        ),
        (
            mid_x - 2 * card_width - 2 * CARD_SPACING,
            SCREEN_HEIGHT - card_height - 60,
        ),
        (
            mid_x - card_width - CARD_SPACING,
            SCREEN_HEIGHT - card_height - 20,
        ),
        # middle bottom
        (
            mid_x - card_width // 2,
            SCREEN_HEIGHT - card_height - 20,
        ),
        # right bottom
        (
            mid_x + card_width + CARD_SPACING,
            SCREEN_HEIGHT - card_height - 20,
        ),
        (
            mid_x + 2 * card_width + 2 * CARD_SPACING,
            SCREEN_HEIGHT - card_height - 60,
        ),
        (
            mid_x + 3 * card_width + 3 * CARD_SPACING,
            SCREEN_HEIGHT - card_height - 100,
        ),
    ]

    for i in range(NUM_CARDS):
        card_key = player_cards[i]
        if reveal_cards:
            screen.blit(card_images[card_key], positions[i])
        else:
            screen.blit(
                card_images["blue_0"], positions[i]
            )  # Assuming blue_0.jpg as the back of the card

    # Draw the Reveal Cards button
    reveal_button.draw(screen)

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if state == "home":
            if start_button.is_clicked(event):
                state = "game"
            else:
                home_screen()
        elif state == "game":
            if shuffle_play_button.is_clicked(event):
                shuffle_and_deal()
                state = "play"
            else:
                game_screen()
        elif state == "play":
            if reveal_button.is_clicked(event):
                reveal_cards = True
            play_game()

        pygame.display.flip()

pygame.quit()
sys.exit()
