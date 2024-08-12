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
HOME_BACKGROUND_IMAGE = "images/home_screen.jpg"
GAME_BACKGROUND_IMAGE = "images/UNO_bg.jpg"
CARD_BACK_IMAGE = "images/UNO_card.jpg"
NUM_CARDS = 7
CARD_SCALE = 0.37
CARD_SPACING = 10
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
card_back_image = pygame.image.load(CARD_BACK_IMAGE)
scaled_card_back_image = pygame.transform.scale(
    card_back_image,
    (
        int(card_back_image.get_width() * CARD_SCALE),
        int(card_back_image.get_height() * CARD_SCALE),
    ),
)
font = pygame.font.Font(FONT_PATH, 40)
font_card = pygame.font.Font(CARD_FONT_PATH, 60)

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Uno Game")

# Define card images dictionary
card_images = {}


# Load and scale card images
def load_and_scale_card_images():
    """Scales and loads card images."""
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
        """Initialize characteristics of buttons."""
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
        """Draws and displays buttons and screen."""
        pygame.draw.rect(surface, self.color, self.rect)
        surface.blit(self.rendered_text, self.text_rect)

    def is_clicked(self, event):
        """Handle event on click."""
        return (
            event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
            and self.rect.collidepoint(event.pos)
        )


# Create buttons
start_button = Button(
    "Start", (400, 350), (200, 80), COLOR_RED, (255, 255, 255), font
)
instructions_button = Button(
    "Instructions", (650, 350), (250, 80), COLOR_RED, (255, 255, 255), font
)
exit_button = Button(
    "Exit",
    (SCREEN_WIDTH - 120, SCREEN_HEIGHT - 60),
    (100, 50),
    COLOR_RED,
    (255, 255, 255),
    font,
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

draw_card_button = Button(
    "DRAW CARD",
    (
        SCREEN_WIDTH - REVEAL_BUTTON_SIZE[0] - 20,
        (SCREEN_HEIGHT - REVEAL_BUTTON_SIZE[1]) // 2,
    ),
    REVEAL_BUTTON_SIZE,
    BUTTON_COLOR,
    TEXT_COLOR,
    font,
)

# Game state
state = "home"
reveal_cards = False
reveal_button_clicked = False
player_cards = []
computer_cards = []
discard_pile = []
deck = []
# To track the card that has been clicked
selected_card = None
direction = 1


def draw_home_screen():
    """Draw the home screen with all buttons."""
    screen.blit(home_background_image, (0, 0))  # Draw background first
    start_button.draw(screen)
    instructions_button.draw(screen)
    exit_button.draw(screen)
    pygame.display.flip()  # Update the display


def draw_card_from_deck():
    """Draw one random card from the deck and add it to the player's hand."""
    global deck, player_cards

    if deck:
        # Draw a random card from the deck
        card = random.choice(deck)
        # Remove the card from the deck
        deck.remove(card)
        # Add it to the player's hand
        player_cards.append(card)
        print(f"Drawn card: {card}")


def display_instructions():
    """Display the instructions image with the 'Shuffle and Play' button."""
    # Load the instructions image
    instructions_image = pygame.image.load("images/instructions.jpg")

    # Resize the image to fit the screen, if necessary
    instructions_image = pygame.transform.scale(
        instructions_image, (SCREEN_WIDTH, SCREEN_HEIGHT)
    )

    # Display the image on the screen
    screen.blit(instructions_image, (0, 0))

    # Draw the Shuffle and Play button on the instructions screen
    shuffle_play_button.draw(screen)

    pygame.display.flip()  # Update the display

    # Wait for player interaction
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                waiting = False
            if shuffle_play_button.is_clicked(event):
                shuffle_and_deal()
                state = "play"
                waiting = False


def get_card_at_position(x, y):
    """Check if the mouse position is over a card and return the card key."""
    card_width, card_height = scaled_card_back_image.get_size()
    for i in range(len(player_cards)):  # Use length of player_cards
        card_x = (
            i * (card_width + CARD_SPACING)
            + (
                SCREEN_WIDTH
                - ((card_width + CARD_SPACING) * len(player_cards))
            )
            // 2
        )
        card_y = SCREEN_HEIGHT - card_height - 20
        if (
            card_x <= x <= card_x + card_width
            and card_y <= y <= card_y + card_height
        ):
            return player_cards[i]
    return None


def play_card(card_key):
    global discard_pile, player_cards, computer_cards, direction, deck

    if card_key in player_cards:
        try:
            print(
                f"Attempting to play card: {card_key}"
            )  # Debugging statement
            card_color, card_value = card_key.split("_")
            print(
                f"Card color: {card_color}, Card value: {card_value}"
            )  # Debugging statement

            top_card = discard_pile[0] if discard_pile else None

            if top_card:
                top_color, top_value = top_card.split("_")
                print(
                    f"Top card on discard pile: {top_card}"
                )  # Debugging statement
                print(
                    f"Top card color: {top_color}, Top card value: {top_value}"
                )  # Debugging statement

                if (
                    card_color == top_color
                    or card_value == top_value
                    or card_value in wild_cards
                ):
                    discard_pile.insert(0, card_key)
                    player_cards.remove(card_key)
                    print(f"Card played: {card_key}")

                    if card_value == "rev":
                        direction *= -1
                        print(
                            f"Direction reversed: {'clockwise' if direction == 1 else 'counter-clockwise'}"
                        )

                    elif card_value == "skip":
                        print("Next player skipped")

                    elif card_value == "+2":
                        print("Next player draws two cards")

                    elif card_value == "+4":
                        print("Next player draws four cards")

                    # After playing the card, the computer will play its turn
                    computer_turn()
                    return
                else:
                    print("Invalid card play. Try again.")
            else:
                print("No cards on discard pile. Invalid play.")
        except Exception as e:
            print(f"Error playing card: {e}")
    else:
        print("Card not found in player's hand.")


def computer_turn():
    global player_cards, computer_cards, discard_pile, deck
    # Basic AI to play a valid card or draw if none are valid
    top_card = discard_pile[0] if discard_pile else None
    if top_card:
        top_color, top_value = top_card.split("_")
        valid_cards = [
            card
            for card in computer_cards
            if card.split("_")[0] == top_color
            or card.split("_")[1] == top_value
            or card.split("_")[1] in wild_cards
        ]
        if valid_cards:
            card_to_play = random.choice(valid_cards)
            discard_pile.insert(0, card_to_play)
            computer_cards.remove(card_to_play)
            print(f"Computer played: {card_to_play}")

            if card_to_play.split("_")[1] == "rev":
                direction *= -1
                print(
                    f"Direction reversed: {'clockwise' if direction == 1 else 'counter-clockwise'}"
                )

            elif card_to_play.split("_")[1] == "skip":
                print("Player skipped")

            elif card_to_play.split("_")[1] == "+2":
                print("Player draws two cards")

            elif card_to_play.split("_")[1] == "+4":
                print("Player draws four cards")

        else:
            if deck:
                drawn_card = random.choice(deck)
                deck.remove(drawn_card)
                computer_cards.append(drawn_card)
                print(f"Computer drew a card: {drawn_card}")

def shuffle_and_deal():
    """Shuffles the deck and deals cards to the player and computer."""
    global deck, player_cards, computer_cards, discard_pile
    deck = (
        [f"{color}_{number}" for color in card_colors for number in range(10)]
        + [
            f"{color}_{special}"
            for color in card_colors
            for special in special_cards
        ]
        + [wild for wild in wild_cards for _ in range(4)]
    )
    random.shuffle(deck)

    player_cards = [deck.pop() for _ in range(NUM_CARDS)]
    computer_cards = [deck.pop() for _ in range(NUM_CARDS)]

    # Set the initial discard pile card
    discard_pile = [deck.pop()]

def draw_cards():
    """Draw cards on the screen."""
    global player_cards

    # Draw the background
    screen.blit(game_background_image, (0, 0))

    # Draw the player's cards
    for i, card in enumerate(player_cards):
        screen.blit(
            scaled_card_back_image,
            (
                i * (scaled_card_back_image.get_width() + CARD_SPACING)
                + (
                    SCREEN_WIDTH
                    - (scaled_card_back_image.get_width() + CARD_SPACING)
                    * len(player_cards)
                )
                // 2,
                SCREEN_HEIGHT - scaled_card_back_image.get_height() - 20,
            ),
        )

    pygame.display.flip()

def main():
    global state, reveal_cards, reveal_button_clicked

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if state == "home":
                if start_button.is_clicked(event):
                    state = "instructions"
                elif instructions_button.is_clicked(event):
                    display_instructions()
                elif exit_button.is_clicked(event):
                    pygame.quit()
                    sys.exit()

            elif state == "instructions":
                if shuffle_play_button.is_clicked(event):
                    shuffle_and_deal()
                    state = "play"

            elif state == "play":
                draw_cards()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    clicked_card = get_card_at_position(x, y)
                    if clicked_card:
                        play_card(clicked_card)

                    if reveal_button.is_clicked(event):
                        reveal_cards = True
                        reveal_button_clicked = True
                        pygame.time.wait(
                            2000
                        )  # Display the reveal button for 2 seconds
                        reveal_cards = False

        pygame.display.flip()

# Start the game
main()
