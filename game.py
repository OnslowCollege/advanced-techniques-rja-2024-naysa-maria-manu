import pygame
import random
import sys

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
# Number of cards per player
NUM_CARDS = 7
# Scale down the cards size down by 47%
CARD_SCALE = 0.37
ENLARGED_SCALE = 0.6
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
        card_name = (
            f"UNO_{wild}.jpg"  # Wild card images are named with "UNO_" prefix
        )
        card_image = pygame.image.load(f"images/{card_name}")
        card_images[f"UNO_{wild}"] = pygame.transform.scale(
            card_image,
            (
                int(card_image.get_width() * CARD_SCALE),
                int(card_image.get_height() * CARD_SCALE),
            ),
        )

    # Debugging output to check if all images are loaded
    print("Loaded card images:")
    for key in card_images:
        print(key)


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


# Card Class
class Card:
    def __init__(self, color, value):
        self.color = color
        self.value = value

    def __repr__(self):
        return f"{self.color}_{self.value}"


# Deck Class
class Deck:
    def __init__(self):
        self.cards = []
        self.initialize_deck()

    def initialize_deck(self):
        for color in card_colors:
            for number in range(10):
                self.cards.append(Card(color, str(number)))
            for special in special_cards:
                self.cards.append(Card(color, special))
        for wild in wild_cards:
            self.cards.extend([Card("wild", wild)] * 4)
        random.shuffle(self.cards)

    def draw_card(self):
        return self.cards.pop()

    def is_empty(self):
        return len(self.cards) == 0

    def shuffle(self):
        random.shuffle(self.cards)

# Player Class
class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []

    def draw_card(self, deck):
        if not deck.is_empty():
            self.hand.append(deck.draw_card())

    def play_card(self, card):
        self.hand.remove(card)
        return card

    def get_playable_cards(self, current_card):
        playable = [
            card
            for card in self.hand
            if card.color == current_card.color
            or card.value == current_card.value
            or card.color == "wild"
        ]
        return playable

# Game Class
class Game:
    def __init__(self):
        self.deck = Deck()
        self.player = Player("Player")
        self.computer = Player("Computer")
        self.current_card = None
        self.turn = "Player"
        self.played_cards = []

    def start_game(self):
        self.deck.shuffle()
        self.deal_initial_cards()
        self.current_card = self.deck.draw_card()
        self.played_cards.append(self.current_card)
        self.turn = "Player"

    def deal_initial_cards(self):
        for _ in range(7):
            self.player.draw_card(self.deck)
            self.computer.draw_card(self.deck)

    def play_turn(self):
        if self.turn == "Player":
            self.handle_player_turn()
        else:
            self.handle_computer_turn()

    def handle_player_turn(self):
        playable_cards = self.player.get_playable_cards(self.current_card)
        if playable_cards:
            selected_card = self.get_player_selected_card(playable_cards)
            if selected_card:
                self.current_card = self.player.play_card(selected_card)
                self.played_cards.append(self.current_card)
                self.turn = "Computer"
        else:
            self.player.draw_card(self.deck)
            self.turn = "Computer"

    def handle_computer_turn(self):
        playable_cards = self.computer.get_playable_cards(self.current_card)
        if playable_cards:
            selected_card = playable_cards[0]
            self.current_card = self.computer.play_card(selected_card)
            self.played_cards.append(self.current_card)
        else:
            self.computer.draw_card(self.deck)
        self.turn = "Player"

    def get_player_selected_card(self, playable_cards):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for i, card in enumerate(playable_cards):
                    card_rect = get_card_image(card).get_rect(
                        topleft=positions[i]
                    )
                    if card_rect.collidepoint(event.pos):
                        return card
        return None

    def check_playable(self, card):
        return (
            card.color == self.current_card.color
            or card.value == self.current_card.value
            or card.color == "wild"
        )

# Game state
state = "home"
selected_card_index = None
reveal_cards = False
show_card = False

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
show_card_button = Button(
    "Show Card",
    (
        SCREEN_WIDTH // 2 - REVEAL_BUTTON_SIZE[0] // 2,
        SCREEN_HEIGHT // 2 - REVEAL_BUTTON_SIZE[1] // 2 + 70,
    ),
    REVEAL_BUTTON_SIZE,
    BUTTON_COLOR,
    TEXT_COLOR,
    font,
)

def get_card_image(card):
    card_name = (
        f"UNO_{card.value}"
        if card.color == "wild"
        else f"{card.color}_{card.value}"
    )
    return card_images.get(card_name)

# Render Home screen
def home_screen():
    screen.blit(home_background_image, (0, 0))
    start_button.draw(screen)

# Render Game screen
def game_screen():
    screen.blit(game_background_image, (0, 0))

    if game.current_card:
        current_card_image = get_card_image(game.current_card)
        if current_card_image:
            screen.blit(
                current_card_image,
                (
                    SCREEN_WIDTH // 2 - current_card_image.get_width() // 2,
                    SCREEN_HEIGHT // 2 - current_card_image.get_height() // 2,
                ),
            )

    # Draw player's cards
    num_cards = len(game.player.hand)
    positions = [
        (
            SCREEN_WIDTH // 2
            - (num_cards // 2)
            * (scaled_card_back_image.get_width() + CARD_SPACING)
            + i * (scaled_card_back_image.get_width() + CARD_SPACING),
            SCREEN_HEIGHT - scaled_card_back_image.get_height() - 10,
        )
        for i in range(num_cards)
    ]

    for i, card in enumerate(game.player.hand):
        card_image = get_card_image(card)
        if card_image:
            if i == selected_card_index:
                scaled_image = pygame.transform.scale(
                    card_image,
                    (
                        int(card_image.get_width() * ENLARGED_SCALE),
                        int(card_image.get_height() * ENLARGED_SCALE),
                    ),
                )
                screen.blit(
                    scaled_image, (positions[i][0], positions[i][1] - 10)
                )
            else:
                screen.blit(card_image, positions[i])

    # Draw computer's cards
    for i, card in enumerate(game.computer.hand):
        card_image = (
            get_card_image(card) if reveal_cards else scaled_card_back_image
        )
        if card_image:
            screen.blit(
                card_image,
                (
                    SCREEN_WIDTH // 2.2
                    + (i - 3)
                    * (scaled_card_back_image.get_width() + CARD_SPACING),
                    10,
                ),
            )

    # Draw buttons
    if not reveal_cards:
        reveal_button.draw(screen)
    if reveal_cards and not show_card:
        show_card_button.draw(screen)

def main():
    global state, game, selected_card_index, reveal_cards, show_card

    game = Game()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if state == "home":
                    if start_button.is_clicked(event):
                        state = "game"
                        game.start_game()
                elif state == "game":
                    if reveal_button.is_clicked(event):
                        reveal_cards = True
                    if show_card_button.is_clicked(event):
                        show_card = True
                    if not reveal_cards and not show_card:
                        num_cards = len(game.player.hand)
                        for i in range(num_cards):
                            card_rect = get_card_image(
                                game.player.hand[i]
                            ).get_rect(topleft=positions[i])
                            if card_rect.collidepoint(event.pos):
                                selected_card_index = i
                                break
                else:
                    if shuffle_play_button.is_clicked(event):
                        game.deck.shuffle()
                        game.start_game()

        if state == "home":
            home_screen()
        elif state == "game":
            game_screen()
            game.play_turn()

        pygame.display.flip()

if __name__ == "__main__":
    main()
