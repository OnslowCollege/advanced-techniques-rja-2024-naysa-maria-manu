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

# Load images and font
home_background_image = pygame.image.load(HOME_BACKGROUND_IMAGE)
game_background_image = pygame.image.load(GAME_BACKGROUND_IMAGE)
original_card_image = pygame.image.load(
    "images/UNO_card.jpg"
)  # Default card image for unknown cards
font = pygame.font.Font(FONT_PATH, 40)


# Function to load card images based on filenames
def load_card_image(filename):
    image = pygame.image.load(filename)
    return pygame.transform.scale(
        image,
        (
            int(image.get_width() * CARD_SCALE),
            int(image.get_height() * CARD_SCALE),
        ),
    )


# Card filenames
colors = ["red", "blue", "green", "yellow"]
numbers = [str(i) for i in range(10)] + [str(i) for i in range(1, 10)]
specials = ["skip", "rev", "+2"]
wild_cards = ["UNO_+4.jpg"]

# Load all card images into a dictionary
card_images = {}
for color in colors:
    for number in numbers:
        filename = f"images/{color}_{number}.jpg"
        card_images[f"{color}_{number}"] = load_card_image(filename)
    for special in specials:
        filename = f"images/{color}_{special}.jpg"
        card_images[f"{color}_{special}"] = load_card_image(filename)
for wild in wild_cards:
    card_images[wild] = load_card_image(f"images/{wild}")

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Uno Game")


class Button:
    def __init__(self, text, pos, size, color, text_color, font):
        self.text = text
        self.pos = pos
        self.size = size
        self.color = color
        self.text_color = text_color
        self.font = font
        self.rect = pygame.Rect(pos, size)
        self.rendered_text = self.font.render(text, True, self.text_color)
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
user_hand = []
computer_hand = []


def home_screen():
    screen.blit(home_background_image, (0, 0))
    start_button.draw(screen)


def game_screen():
    screen.blit(game_background_image, (0, 0))
    shuffle_play_button.draw(screen)


def play_game():
    screen.blit(game_background_image, (0, 0))

    # Display computer's cards
    card_width, card_height = list(card_images.values())[0].get_size()
    for i in range(NUM_CARDS):
        x = (
            i * (card_width + CARD_SPACING)
            + (SCREEN_WIDTH - ((card_width + CARD_SPACING) * NUM_CARDS)) // 2
        )
        y = 20  # Top of the screen
        screen.blit(original_card_image, (x, y))  # Back of the card

    # Display player's cards
    for i, card in enumerate(user_hand):
        x = (
            i * (card_width + CARD_SPACING)
            + (SCREEN_WIDTH - ((card_width + CARD_SPACING) * NUM_CARDS)) // 2
        )
        y = SCREEN_HEIGHT - card_height - 20
        screen.blit(card_images[card], (x, y))

    # Draw the Reveal Cards button
    reveal_button.draw(screen)


def shuffle_and_deal():
    global user_hand, computer_hand

    deck = (
        [f"{color}_{num}" for color in colors for num in numbers * 2]
        + [
            f"{color}_{special}"
            for color in colors
            for special in specials * 2
        ]
        + wild_cards * 4
    )
    random.shuffle(deck)
    user_hand = deck[:NUM_CARDS]
    computer_hand = deck[NUM_CARDS : NUM_CARDS * 2]


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
                pass
        elif state == "game":
            if shuffle_play_button.is_clicked(event):
                shuffle_and_deal()
                state = "play"
            else:
                pass
        elif state == "play":
            if reveal_button.is_clicked(event):
                print("Reveal Cards button clicked!")
            else:
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
