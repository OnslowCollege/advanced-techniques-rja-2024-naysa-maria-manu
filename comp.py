# Created by: Naysa Maria Manu.

# UNO Card game.

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
selected_card = None  # To track the card that has been clicked


def draw_card_from_deck():
    """Draw one random card from the deck and add it to the player's hand."""
    global deck, player_cards, discard_pile

    if deck:
        card = random.choice(deck)  # Draw a random card from the deck
        deck.remove(card)  # Remove the card from the deck
        player_cards.append(card)  # Add it to the player's hand
        print(f"Drawn card: {card}")

        # Check if the drawn card matches the top card on the discard pile
        if discard_pile:
            top_card = discard_pile[0]
            top_color, top_value = top_card.split("_")
            drawn_card_color, drawn_card_value = card.split("_")

            if drawn_card_color == top_color or drawn_card_value == top_value:
                # If the drawn card matches, let the player play it
                return

        # If no match, pass the turn to the computer
        computer_turn()


def shuffle_and_deal():
    """Shuffles and hands cards to user and computer."""
    global player_cards, computer_cards, deck
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

    # Print debug information
    print(f"Deck size: {len(deck)}")
    print(f"Player cards: {len(player_cards)}")
    print(f"Computer cards: {len(computer_cards)}")


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
    """Handle playing a card and update game state."""
    global discard_pile, player_cards

    if card_key in player_cards:
        card_color, card_value = card_key.split("_")
        top_card = discard_pile[0] if discard_pile else None

        if top_card:
            top_color, top_value = top_card.split("_")

            if (
                card_color != top_color
                and card_value != top_value
                and card_value != "+4"
            ):
                # Return the card to the player's hand and display an error message
                display_message(
                    "Wrong selection! Try again.", 2000
                )  # Display for 2 seconds
                return

        # Valid move
        player_cards.remove(card_key)
        discard_pile.insert(0, card_key)
        print(f"Player played card: {card_key}")

        # Check if the player has won
        if not player_cards:
            end_game("YOU WON!")

        # Pass the turn to the computer
        computer_turn()


def display_message(message, duration):
    """Display a message on the screen for a specific duration."""
    global screen, font, SCREEN_WIDTH, SCREEN_HEIGHT
    screen.fill((0, 0, 0))  # Clear the screen
    text = font.render(message, True, COLOR_RED)
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(text, text_rect)
    pygame.display.flip()
    pygame.time.wait(duration)  # Wait for the specified duration


def computer_turn():
    """Handle the computer's turn with a delay after the user plays a card."""
    global computer_cards, discard_pile, deck

    pygame.time.wait(
        2000
    )  # Wait for 2 seconds before the computer plays its card

    if computer_cards:
        # Top card on the discard pile
        top_card = discard_pile[0]
        top_color, top_value = top_card.split("_")

        # Try to find a matching card in the computer's hand
        playable_card = None
        for card in computer_cards:
            card_color, card_value = card.split("_")
            if card_color == top_color or card_value == top_value:
                playable_card = card
                break

        if playable_card:
            computer_cards.remove(playable_card)
            discard_pile.insert(0, playable_card)
            print(f"Computer played card: {playable_card}")
            # Check if the computer has won
            if not computer_cards:
                end_game("YOU LOST!")
        else:
            # Draw a card if no matching card is found
            if deck:
                drawn_card = random.choice(deck)
                deck.remove(drawn_card)
                computer_cards.append(drawn_card)
                print(f"Computer drew a card: {drawn_card}")

                # Check if the drawn card matches
                drawn_card_color, drawn_card_value = drawn_card.split("_")
                if (
                    drawn_card_color == top_color
                    or drawn_card_value == top_value
                ):
                    # If the drawn card matches, play it
                    computer_cards.remove(drawn_card)
                    discard_pile.insert(0, drawn_card)
                    print(f"Computer played card: {drawn_card}")
                    # Check if the computer has won
                    if not computer_cards:
                        end_game("YOU LOST!")
                else:
                    # If no match, display message
                    display_message("Your turn", 3000)  # Display for 3 seconds


def end_game(message):
    """Displays the end game screen with a message."""
    global state
    state = "end"
    screen.fill((0, 0, 0))  # Clear the screen
    text = font.render(message, True, COLOR_RED)
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(text, text_rect)

    # Create the Exit and Return to Main Menu buttons
    exit_button = Button(
        "Exit",
        (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 60),
        (100, 50),
        COLOR_RED,
        (255, 255, 255),
        font,
    )
    menu_button = Button(
        "Main Menu",
        (SCREEN_WIDTH // 2 + 50, SCREEN_HEIGHT // 2 + 60),
        (200, 50),
        COLOR_RED,
        (255, 255, 255),
        font,
    )

    # Draw the buttons
    exit_button.draw(screen)
    menu_button.draw(screen)

    pygame.display.flip()

    # Wait for the player's action
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if exit_button.is_clicked(event):
                pygame.quit()
                sys.exit()
            if menu_button.is_clicked(event):
                # Reset to the home screen
                global \
                    player_cards, \
                    computer_cards, \
                    deck, \
                    discard_pile, \
                    reveal_cards, \
                    reveal_button_clicked
                state = "home"
                player_cards, computer_cards, deck, discard_pile = (
                    [],
                    [],
                    [],
                    [],
                )
                reveal_cards = False
                reveal_button_clicked = False
                waiting = False


def play_game():
    """Display the game screen with cards."""
    screen.blit(game_background_image, (0, 0))

    # Display computer's cards in a linear layout
    card_width, card_height = scaled_card_back_image.get_size()
    for i in range(len(computer_cards)):
        x = (
            i * (card_width + CARD_SPACING)
            + (
                SCREEN_WIDTH
                - ((card_width + CARD_SPACING) * len(computer_cards))
            )
            // 2
        )
        y = 20
        screen.blit(scaled_card_back_image, (x, y))

    # Display player's cards in a linear layout
    for i in range(len(player_cards)):  # Use length of player_cards
        x = (
            i * (card_width + CARD_SPACING)
            + (
                SCREEN_WIDTH
                - ((card_width + CARD_SPACING) * len(player_cards))
            )
            // 2
        )
        y = SCREEN_HEIGHT - card_height - 20
        if i < len(player_cards):  # Ensure index is within range
            card_key = player_cards[i]
            if reveal_cards:
                if card_key == selected_card:
                    y -= 30  # Move selected card up by 30 pixels
                screen.blit(card_images[card_key], (x, y))
            else:
                screen.blit(scaled_card_back_image, (x, y))

    # Draw the Reveal Cards button if not clicked
    if not reveal_button_clicked:
        reveal_button.draw(screen)
    else:
        # Draw discard pile
        if discard_pile:
            # Top card on discard pile
            top_card_key = discard_pile[0]
            screen.blit(
                card_images[top_card_key],
                (
                    SCREEN_WIDTH // 2 - card_width // 2,
                    SCREEN_HEIGHT // 2 - card_height // 2,
                ),
            )
        draw_card_button.draw(screen)

    pygame.display.flip()


# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if state == "play":
                if draw_card_button.rect.collidepoint(x, y):
                    draw_card_from_deck()
                else:
                    card_key = get_card_at_position(x, y)
                    if card_key and reveal_cards:
                        selected_card = card_key
                        play_game()
                        pygame.display.flip()
                        pygame.time.wait(2000)
                        play_card(card_key)
                        selected_card = None
                        computer_turn()

            if reveal_button.is_clicked(event):
                reveal_cards = True
                reveal_button_clicked = True

        if state == "home":
            if start_button.is_clicked(event):
                state = "game"
            else:
                screen.blit(home_background_image, (0, 0))
                start_button.draw(screen)
        elif state == "game":
            if shuffle_play_button.is_clicked(event):
                shuffle_and_deal()
                state = "play"
            else:
                screen.blit(game_background_image, (0, 0))
                shuffle_play_button.draw(screen)
        elif state == "play":
            play_game()

        pygame.display.flip()

pygame.quit()
sys.exit()
