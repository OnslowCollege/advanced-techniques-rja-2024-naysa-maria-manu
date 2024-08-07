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


def load_and_scale_card_images():
    global card_images
    card_images = {}

    # Load number cards
    for color in card_colors:
        for number in range(10):
            card_name = f"{color}_{number}.jpg"
            card_image = load_image(f"images/{card_name}")
            if card_image:
                scaled_image = pygame.transform.scale(
                    card_image,
                    (
                        int(card_image.get_width() * CARD_SCALE),
                        int(card_image.get_height() * CARD_SCALE),
                    ),
                )
                card_images[f"{color}_{number}"] = scaled_image

    # Load special cards
    for color in card_colors:
        for special in special_cards:
            card_name = f"{color}_{special}.jpg"
            card_image = load_image(f"images/{card_name}")
            if card_image:
                scaled_image = pygame.transform.scale(
                    card_image,
                    (
                        int(card_image.get_width() * CARD_SCALE),
                        int(card_image.get_height() * CARD_SCALE),
                    ),
                )
                card_images[f"{color}_{special}"] = scaled_image

    # Load wild cards
    for wild in wild_cards:
        card_name = f"UNO_{wild}.jpg"
        card_image = load_image(f"images/{card_name}")
        if card_image:
            scaled_image = pygame.transform.scale(
                card_image,
                (
                    int(card_image.get_width() * CARD_SCALE),
                    int(card_image.get_height() * CARD_SCALE),
                ),
            )
            card_images[wild] = scaled_image

    # Load the new wild color card
    wild_color_image = load_image("images/wild_color.jpg")
    if wild_color_image:
        scaled_image = pygame.transform.scale(
            wild_color_image,
            (
                int(wild_color_image.get_width() * CARD_SCALE),
                int(wild_color_image.get_height() * CARD_SCALE),
            ),
        )
        card_images["wild_color"] = scaled_image


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
        self.rendered_text = self.font.render(text, True, self.text_color)
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

def draw(screen, reveal=False):
    screen.fill((0, 128, 0))
    if state == "home":
        screen.blit(home_background_image, (0, 0))
        start_button.draw(screen)
        shuffle_play_button.draw(screen)
    elif state == "game":
        screen.blit(game_background_image, (0, 0))
        if reveal:
            # Draw cards face-up
            for index, card in enumerate(player_cards):
                card_image = card_images.get(card, scaled_card_back_image)
                if card_image:
                    screen.blit(
                        card_image,
                        (
                            100
                            + index * (card_image.get_width() + CARD_SPACING),
                            SCREEN_HEIGHT - card_image.get_height() - 50,
                        ),
                    )
        else:
            # Draw cards face-down
            for index, _ in enumerate(player_cards):
                screen.blit(
                    scaled_card_back_image,
                    (
                        100
                        + index
                        * (scaled_card_back_image.get_width() + CARD_SPACING),
                        SCREEN_HEIGHT
                        - scaled_card_back_image.get_height()
                        - 50,
                    ),
                )
        reveal_button.draw(screen)
        if current_turn == "player":
            # Show player options
            for index, card in enumerate(player_cards):
                card_image = card_images.get(card, scaled_card_back_image)
                if card_image:
                    screen.blit(
                        card_image,
                        (
                            100
                            + index * (card_image.get_width() + CARD_SPACING),
                            SCREEN_HEIGHT - card_image.get_height() - 50,
                        ),
                    )
        elif current_turn == "computer":
            # Show computer options
            for index, card in enumerate(computer_cards):
                card_image = card_images.get(card, scaled_card_back_image)
                if card_image:
                    screen.blit(
                        card_image,
                        (
                            SCREEN_WIDTH - card_image.get_width() - 100,
                            50
                            + index * (card_image.get_height() + CARD_SPACING),
                        ),
                    )
        # Draw discard pile
        if discard_pile:
            top_discard_card = discard_pile[-1]
            discard_card_image = card_images.get(top_discard_card)
            if discard_card_image:
                screen.blit(
                    discard_card_image,
                    (
                        SCREEN_WIDTH // 2
                        - discard_card_image.get_width() // 2,
                        SCREEN_HEIGHT // 2
                        - discard_card_image.get_height() // 2,
                    ),
                )

def main():
    global state, reveal_cards
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if state == "home":
                    if start_button.is_clicked(event):
                        state = "game"
                        shuffle_and_deal()
                    elif shuffle_play_button.is_clicked(event):
                        shuffle_and_deal()
                elif state == "game":
                    if reveal_button.is_clicked(event):
                        reveal_cards = not reveal_cards
                    if current_turn == "player":
                        for index, card in enumerate(player_cards):
                            card_rect = pygame.Rect(
                                100
                                + index
                                * (
                                    scaled_card_back_image.get_width()
                                    + CARD_SPACING
                                ),
                                SCREEN_HEIGHT
                                - scaled_card_back_image.get_height()
                                - 50,
                                scaled_card_back_image.get_width(),
                                scaled_card_back_image.get_height(),
                            )
                            if card_rect.collidepoint(event.pos):
                                player_turn(index)
                                break
                    else:
                        computer_turn()
        draw(screen, reveal_cards)
        pygame.display.flip()


if __name__ == "__main__":
    main()
