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
COMPUTER_BUTTON_SIZE = (330, 60)
BUTTON_COLOR = COLOR_RED
TEXT_COLOR = (254, 245, 185)

# Define card colors and types
card_colors = ["blue", "red", "yellow", "green"]
special_cards = ["+2", "rev", "skip"]
wild_cards = ["+4"]

# Load images and fonts with error handling
def load_image(path):
    try:
        return pygame.image.load(path)
    except pygame.error as e:
        print(f"Unable to load image at {path}: {e}")
        return None


def load_font(path, size):
    try:
        return pygame.font.Font(path, size)
    except pygame.error as e:
        print(f"Unable to load font at {path}: {e}")
        return pygame.font.Font(None, size)


home_background_image = load_image(HOME_BACKGROUND_IMAGE)
game_background_image = load_image(GAME_BACKGROUND_IMAGE)
card_back_image = load_image(CARD_BACK_IMAGE)
scaled_card_back_image = (
    pygame.transform.scale(
        card_back_image,
        (
            int(card_back_image.get_width() * CARD_SCALE),
            int(card_back_image.get_height() * CARD_SCALE),
        ),
    )
    if card_back_image
    else None
)
font = load_font(FONT_PATH, 40)
font_card = load_font(CARD_FONT_PATH, 60)

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
            card_image = load_image(f"images/{card_name}")
            if card_image:
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
            card_image = load_image(f"images/{card_name}")
            if card_image:
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
        card_image = load_image(f"images/{card_name}")
        if card_image:
            card_images[wild] = pygame.transform.scale(
                card_image,
                (
                    int(card_image.get_width() * CARD_SCALE),
                    int(card_image.get_height() * CARD_SCALE),
                ),
            )

    # Load the new wild color card
    wild_color_image = load_image("images/wild_color.jpg")
    if wild_color_image:
        card_images["wild_color"] = pygame.transform.scale(
            wild_color_image,
            (
                int(wild_color_image.get_width() * CARD_SCALE),
                int(wild_color_image.get_height() * CARD_SCALE),
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
        """Draws button."""
        pygame.draw.rect(surface, self.color, self.rect)
        surface.blit(self.rendered_text, self.text_rect)

    def is_clicked(self, event):
        """Follows button click."""
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
player_first_button = Button(
    "Player First",
    (
        SCREEN_WIDTH // 2 - REVEAL_BUTTON_SIZE[0] // 2,
        SCREEN_HEIGHT // 2 - REVEAL_BUTTON_SIZE[1] // 2 - 80,
    ),
    REVEAL_BUTTON_SIZE,
    BUTTON_COLOR,
    TEXT_COLOR,
    font,
)
computer_first_button = Button(
    "Computer First",
    (
        SCREEN_WIDTH // 2 - COMPUTER_BUTTON_SIZE[0] // 2,
        SCREEN_HEIGHT // 2 - COMPUTER_BUTTON_SIZE[1] // 2 + 80,
    ),
    COMPUTER_BUTTON_SIZE,
    BUTTON_COLOR,
    TEXT_COLOR,
    font,
)

# Game state
state = "home"
reveal_cards = False
player_cards = []
computer_cards = []
discard_pile = []
current_turn = "player"
deck = []


def shuffle_and_deal():
    global player_cards, computer_cards, discard_pile, current_turn, deck
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
    discard_pile = [
        deck[NUM_CARDS * 2]
    ]  # Start with one card in the discard pile
    deck = deck[NUM_CARDS * 2 + 1 :]  # Remaining cards in the deck
    current_turn = "player"  # Player starts first


def is_playable(card, top_card):
    card_color, card_value = card.split("_")
    top_color, top_value = top_card.split("_")
    return (
        card_color == top_color
        or card_value == top_value
        or card in wild_cards
    )


def switch_turn():
    global current_turn
    current_turn = "computer" if current_turn == "player" else "player"


def player_turn(card_index):
    global player_cards, discard_pile, deck
    selected_card = player_cards[card_index]
    top_card = discard_pile[-1]
    if is_playable(selected_card, top_card):
        discard_pile.append(selected_card)
        player_cards.pop(card_index)
        switch_turn()
    else:
        print("Cannot play this card!")


def computer_turn():
    """served by computer."""
    global computer_cards, discard_pile, deck
    top_card = discard_pile[-1]
    for i, card in enumerate(computer_cards):
        if is_playable(card, top_card):
            discard_pile.append(card)
            computer_cards.pop(i)
            switch_turn()
            return
    # If no card can be played, draw a card
    if deck:
        new_card = deck.pop(0)
        computer_cards.append(new_card)
        if is_playable(new_card, top_card):
            discard_pile.append(new_card)
            computer_cards.pop(-1)
            switch_turn()
            return
    switch_turn()


def draw_card(player):
    """Draws cards."""
    global deck
    if deck:
        new_card = deck.pop(0)
        if player == "player":
            player_cards.append(new_card)
        else:
            computer_cards.append(new_card)


def home_screen():
    """Display the home screen with the start button."""
    if home_background_image:
        screen.blit(home_background_image, (0, 0))
    start_button.draw(screen)
    pygame.display.flip()


def game_screen():
    """Display the screen for shuffling and dealing cards."""
    if game_background_image:
        screen.blit(game_background_image, (0, 0))
    shuffle_play_button.draw(screen)
    pygame.display.flip()


def choose_turn_order():
    """Chooses the turn order."""
    if game_background_image:
        screen.blit(game_background_image, (0, 0))
    player_first_button.draw(screen)
    computer_first_button.draw(screen)
    pygame.display.flip()


def play_game():
    """Display the game screen with cards."""
    screen.blit(game_background_image, (0, 0))

    # Display computer's cards
    card_width, card_height = scaled_card_back_image.get_size()
    for i in range(NUM_CARDS):
        x = (
            i * (card_width + CARD_SPACING)
            + (SCREEN_WIDTH - ((card_width + CARD_SPACING) * NUM_CARDS)) // 2
        )
        # Top of the screen
        y = 20
        screen.blit(scaled_card_back_image, (x, y))

    # Display player's cards in a U-shape
    mid_x = SCREEN_WIDTH // 2
    positions = [
        # left bottom
        (
            mid_x - 3 * card_width - 3 * CARD_SPACING - 50,
            SCREEN_HEIGHT - card_height - 100,
        ),
        (
            mid_x - 2 * card_width - 2 * CARD_SPACING - 50,
            SCREEN_HEIGHT - card_height - 60,
        ),
        (
            mid_x - card_width - CARD_SPACING - 50,
            SCREEN_HEIGHT - card_height - 20,
        ),
        # middle bottom
        (
            mid_x - card_width // 33 - 50,
            SCREEN_HEIGHT - card_height - 20,
        ),
        # right bottom
        (
            mid_x + card_width + CARD_SPACING - 50,
            SCREEN_HEIGHT - card_height - 20,
        ),
        (
            mid_x + 2 * card_width + 2 * CARD_SPACING - 50,
            SCREEN_HEIGHT - card_height - 60,
        ),
        (
            mid_x + 3 * card_width + 3 * CARD_SPACING - 50,
            SCREEN_HEIGHT - card_height - 100,
        ),
    ]

    for i in range(NUM_CARDS):
        screen.blit(scaled_card_back_image, positions[i])

    # Draw the Reveal Cards button
    reveal_button.draw(screen)

    # Add logic to display the current player's turn
    turn_text = font.render(
        f"Current Turn: {current_turn.capitalize()}", True, TEXT_COLOR
    )
    screen.blit(
        turn_text,
        (SCREEN_WIDTH // 2 - turn_text.get_width() // 2, SCREEN_HEIGHT - 50),
    )

card_width, card_height = scaled_card_back_image.get_size()


def handle_turns():
    """Handle the game turns and actions."""
    if state == "play":
        if current_turn == "computer":
            pygame.time.wait(1000)  # Simulate thinking time
            computer_turn()
        # Check if reveal button is clicked for the current turn
        if reveal_button.is_clicked(event):
            reveal_cards = True

        if current_turn == "player":
            # Player's card selection
            for i, card in enumerate(player_cards):
                x = (
                    i * (card_width + CARD_SPACING)
                    + (
                        SCREEN_WIDTH
                        - ((card_width + CARD_SPACING) * NUM_CARDS)
                    )
                    // 2
                )
                y = SCREEN_HEIGHT - card_height - 50
                card_rect = pygame.Rect(x, y, card_width, card_height)
                if card_rect.collidepoint(event.pos):
                    player_turn(i)
                    break
        else:
            # Computer's turn
            pygame.time.wait(1000)
            computer_turn()

# Main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if state == "home":
            if start_button.is_clicked(event):
                state = "game"
        elif state == "game":
            if shuffle_play_button.is_clicked(event):
                shuffle_and_deal()
                state = "choose_turn_order"
        elif state == "choose_turn_order":
            if player_first_button.is_clicked(event):
                current_turn = "player"
                state = "play"
            elif computer_first_button.is_clicked(event):
                current_turn = "computer"
                state = "play"
        elif state == "play":
            handle_turns()

    if state == "home":
        home_screen()
    elif state == "game":
        game_screen()
    elif state == "choose_turn_order":
        choose_turn_order()
    elif state == "play":
        play_game()
