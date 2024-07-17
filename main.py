import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
COLOR_RED = (176, 39, 47)
FONT_PATH = "Font_mont.ttf"
BACKGROUND_IMAGE = "UNO_Home.png"

# Load background image and font
background_image = pygame.image.load(BACKGROUND_IMAGE)
font = pygame.font.Font(FONT_PATH, 40)

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Uno Game")


class Button:
    """
    A class to represent a button in the game.

    Attributes:

    text (str): The text to display on the button.
    pos (tuple): The position of the top-left corner of the button.
    size (tuple): The size (width, height) of the button.
    color (tuple): The color of the button rectangle.
    font (pygame.font.Font): The font used for the button text.

    """

    def __init__(self, text, pos, size, color, font):
        """
        Constructs all the necessary attributes for the button object.

        Parameters:

        text (str): The text to display on the button.
        pos (tuple): The position of the top-left corner of the button.
        size (tuple): The size (width, height) of the button.
        color (tuple): The color of the button rectangle.
        font (pygame.font.Font): The font used for the button text.

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

        Parameters:
        surface (pygame.Surface): The surface to draw the button on.
        """
        pygame.draw.rect(surface, self.color, self.rect)
        surface.blit(self.rendered_text, self.text_rect)

    def is_clicked(self, event):
        """
        Checks if the button was clicked.

        Parameters:
        event (pygame.event.Event): The event to check for a click.

        Returns:
        bool: True if the button was clicked, False otherwise.
        """
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
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
    """
    Displays the home screen with the start button.
    """
    screen.blit(background_image, (0, 0))
    start_button.draw(screen)


def game_screen():
    """
    Displays the game screen with the shuffle and play button.
    """
    screen.blit(background_image, (0, 0))
    shuffle_play_button.draw(screen)


# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if state == "home":
            if start_button.is_clicked(event):
                state = "game"

        elif state == "game":
            if shuffle_play_button.is_clicked(event):
                print("Shuffle and Play button clicked")

    if state == "home":
        home_screen()
    elif state == "game":
        game_screen()

    pygame.display.flip()

pygame.quit()
sys.exit()
