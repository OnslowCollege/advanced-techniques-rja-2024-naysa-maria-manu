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
selected_cards = []

deck = []
discard_pile = []
current_playable_card = None

def draw_card_from_deck(player=True):
    """Draw one random card from the deck and add it to the player's or computer's hand."""
    global deck, player_cards, computer_cards
    if deck:
        card = random.choice(deck)
        deck.remove(card)
        if player:
            player_cards.append(card)
            print(f"Player drew card: {card}")
            if can_play_card(card):
                return card
        else:
            computer_cards.append(card)
            print(f"Computer drew card: {card}")
            if can_play_card(card):
                return card
    return None

def shuffle_and_deal():
    global \
        player_cards, \
        computer_cards, \
        deck, \
        discard_pile, \
        current_playable_card
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
    discard_pile = [deck.pop()]  # Start with one card on the discard pile
    current_playable_card = discard_pile[-1]  # Set the initial playable card

    print(f"Deck size: {len(deck)}")
    print(f"Player cards: {len(player_cards)}")
    print(f"Computer cards: {len(computer_cards)}")

def can_play_card(card):
    card_color, card_number = card.split("_")
    discard_color, discard_number = current_playable_card.split("_")
    return (
        card_color == discard_color
        or card_number == discard_number
        or "UNO" in card
    )


def player_turn():
    global selected_cards, discard_pile, current_playable_card
    if selected_cards:
        selected_card = selected_cards[0]
        if can_play_card(selected_card):
            discard_pile.append(selected_card)
            current_playable_card = selected_card
            selected_cards = []  # Clear selected cards after play
        else:
            draw_card_from_deck()
    else:
        draw_card_from_deck()


def computer_turn():
    global computer_cards, discard_pile, current_playable_card
    playable_cards = [card for card in computer_cards if can_play_card(card)]
    if playable_cards:
        chosen_card = random.choice(playable_cards)
        discard_pile.append(chosen_card)
        current_playable_card = chosen_card
        computer_cards.remove(chosen_card)
    else:
        draw_card_from_deck(player=False)

def get_card_at_position(x, y):
    """Check if the mouse position is over a card and return the card key."""
    card_width, card_height = scaled_card_back_image.get_size()
    for i in range(len(player_cards)):
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

def play_game():
    """Display the game screen with cards."""
    screen.blit(game_background_image, (0, 0))

    # Determine the scale for the player's cards
    if len(player_cards) >= 11:
        player_card_scale = 0.27  # Reduced scale for 11 or more cards
    else:
        player_card_scale = 1.0  # Full scale for fewer than 11 cards

    # Set the scale for the computer's cards
    computer_card_scale = 0.37

    # Scale the back image for computer's cards
    scaled_card_back_image = pygame.transform.scale(
        card_back_image,
        (
            int(card_back_image.get_width() * computer_card_scale),
            int(card_back_image.get_height() * computer_card_scale),
        ),
    )

    # Display computer's cards in a linear layout
    card_width, card_height = scaled_card_back_image.get_size()
    for i in range(NUM_CARDS):
        x = i * (card_width + CARD_SPACING) + 20
        y = 20
        screen.blit(scaled_card_back_image, (x, y))

    # Display player's cards
    scaled_card_images = {
        card: pygame.transform.scale(
            card_images[card],
            (
                int(card_width * player_card_scale),
                int(card_height * player_card_scale),
            ),
        )
        for card in player_cards
    }
    for i, card in enumerate(player_cards):
        x = (
            i * (card_width * player_card_scale + CARD_SPACING)
            + (
                SCREEN_WIDTH
                - (
                    (card_width * player_card_scale + CARD_SPACING)
                    * len(player_cards)
                )
            )
            // 2
        )
        y = SCREEN_HEIGHT - card_height * player_card_scale - 20
        screen.blit(scaled_card_images[card], (x, y))

    # Display the discard pile card
    if discard_pile:
        top_card_image = card_images[discard_pile[-1]]
        scaled_top_card_image = pygame.transform.scale(
            top_card_image, (int(card_width), int(card_height))
        )
        screen.blit(
            scaled_top_card_image,
            (
                SCREEN_WIDTH // 2 - card_width // 2,
                SCREEN_HEIGHT // 2 - card_height // 2,
            ),
        )

    if state == "play":
        if not reveal_button_clicked:
            reveal_button.draw(screen)
        else:
            draw_card_button.draw(screen)
            if draw_card_button.is_clicked(event):
                draw_card_from_deck()

            if selected_cards:
                player_turn()
                if not player_cards:
                    print("Player wins!")
                    return
                computer_turn()
                if not computer_cards:
                    print("Computer wins!")
                    return

    pygame.display.flip()

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if state == "play":
                if draw_card_button.is_clicked(event):
                    draw_card_from_deck()
                else:
                    card_key = get_card_at_position(x, y)
                    if card_key and reveal_cards:
                        if len(selected_cards) >= 1:
                            previous_card = selected_cards.pop(0)
                            if previous_card in player_cards:
                                player_cards.remove(previous_card)
                        selected_cards.insert(0, card_key)

                if reveal_button.is_clicked(event):
                    reveal_cards = True
                    reveal_button_clicked = True

        if state == "home":
            if start_button.is_clicked(event):
                state = "game"
        elif state == "game":
            if shuffle_play_button.is_clicked(event):
                shuffle_and_deal()
                state = "play"
        elif state == "play":
            play_game()

    pygame.display.flip()

pygame.quit()
sys.exit()
