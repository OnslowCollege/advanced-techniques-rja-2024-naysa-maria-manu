"""
UNO.

Created by: Naysa Maria Manu
Date: DATE
"""

import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 960
SCREEN_HEIGHT = 545
COLOR_RED = (176, 39, 47)
FONT_PATH = "Text_features/Font_mont.ttf"
HOME_BACKGROUND_IMAGE = "images/UNO_Home.jpg"
GAME_BACKGROUND_IMAGE = "images/UNO_bg.jpg"
CARD_IMAGE = "images/UNO_card.jpg"
NUM_CARDS = 7  # Number of cards per player
CARD_SCALE = 0.5  # Scale down the cards to 50% of their original size
CARD_SPACING = 10  # Space between cards

# Load images and font
home_background_image = pygame.image.load(HOME_BACKGROUND_IMAGE)
game_background_image = pygame.image.load(GAME_BACKGROUND_IMAGE)
original_card_image = pygame.image.load(CARD_IMAGE)
scaled_card_image = pygame.transform.scale(
    original_card_image,
    (
        int(original_card_image.get_width() * CARD_SCALE),
        int(original_card_image.get_height() * CARD_SCALE),
    ),
)
font = pygame.font.Font(FONT_PATH, 40)

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Uno Game")


class Button:
    """
    A class to represent a button in the game.

    Attributes
    ----------
    text : str
        The text to display on the button.
    pos : tuple
        The position of the top-left corner of the button.
    size : tuple
        The size (width, height) of the button.
    color : tuple
        The color of the button rectangle.
    font : pygame.font.Font
        The font used for the button text.

    """

    def __init__(self, text, pos, size, color, font):
        """
        Construct all the necessary attributes for the button object.

        Parameters
        ----------
        text : str
            The text to display on the button.
        pos : tuple
            The position of the top-left corner of the button.
        size : tuple
            The size (width, height) of the button.
        color : tuple
            The color of the button rectangle.
        font : pygame.font.Font
            The font used for the button text.

        """
        self.text = text
        self.pos = pos
        self.size = size
        self.color = color
        self.font = font
        self.rect = pygame.Rect(pos, size)
        self.rendered_text = self.font.render(
            text, True, (255, 255, 255)
        )  # White text
        self.text_rect = self.rendered_text.get_rect(center=self.rect.center)

    def draw(self, surface):
        """
        Draws the button on the given surface.

        Parameters
        ----------
        surface : pygame.Surface
            The surface to draw the button on.

        """
        pygame.draw.rect(surface, self.color, self.rect)
        surface.blit(self.rendered_text, self.text_rect)

    def is_clicked(self, event):
        """
        Check if the button was clicked.

        Parameters
        ----------
        event : pygame.event.Event
            The event to check for a click.

        Returns
        -------
        bool
            True if the button was clicked, False otherwise.

        """
        if (
            event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
            and self.rect.collidepoint(event.pos)
        ):
            return True
        return False


# Create buttons
start_button = Button("Start", (400, 350), (200, 80), COLOR_RED, font)
shuffle_play_button = Button(
    "Shuffle and Play", (300, 350), (400, 80), COLOR_RED, font
)

# Game state
state = "home"


def home_screen():
    """Display the home screen with the start button."""
    screen.blit(home_background_image, (0, 0))
    start_button.draw(screen)


def game_screen():
    """Display the game screen with the shuffle and play button."""
    screen.blit(game_background_image, (0, 0))
    shuffle_play_button.draw(screen)


def play_game():
    """Display the game screen with cards laid out for player and computer."""
    screen.blit(game_background_image, (0, 0))

    # Display computer's cards
    card_width, card_height = scaled_card_image.get_size()
    for i in range(NUM_CARDS):
        x = (
            i * (card_width + CARD_SPACING)
            + (SCREEN_WIDTH - ((card_width + CARD_SPACING) * NUM_CARDS)) // 2
        )
        y = 15  # Top of the screen
        screen.blit(scaled_card_image, (x, y))

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
        (mid_x - card_width - CARD_SPACING, SCREEN_HEIGHT - card_height - 20),
        # middle bottom
        (mid_x - card_width // 2, SCREEN_HEIGHT - card_height - 20),
        # right bottom
        (mid_x + card_width + CARD_SPACING, SCREEN_HEIGHT - card_height - 20),
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
        screen.blit(scaled_card_image, positions[i])

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
                # Handle other events on the home screen if needed
                pass
        elif state == "game":
            if shuffle_play_button.is_clicked(event):
                state = "play"
            else:
                # Handle other events on the game screen if needed
                pass
        elif state == "play":
            # Handle events in the play state if needed
            pass

    if state == "home":
        home_screen()
    elif state == "game":
        game_screen()
    elif state == "play":
        play_game()

    pygame.display.flip()

pygame.quit()
sys.exit()
