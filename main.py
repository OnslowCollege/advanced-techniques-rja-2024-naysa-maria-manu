"""
Created by: Naysa Maria Manu.

UNO Card game.
"""

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
            # Load the image
            card_image = pygame.image.load(f"images/{card_name}")
            # Scale the image
            card_images[f"{color}_{number}"] = pygame.transform.scale(
                card_image,
                (
                    int(card_image.get_width() * CARD_SCALE),  # New width
                    int(card_image.get_height() * CARD_SCALE),  # New height
                ),
            )

    # Load special cards
    for color in card_colors:
        for special in special_cards:
            card_name = f"{color}_{special}.jpg"
            # Load the image
            card_image = pygame.image.load(f"images/{card_name}")
            # Scale the image
            card_images[f"{color}_{special}"] = pygame.transform.scale(
                card_image,
                (
                    int(card_image.get_width() * CARD_SCALE),  # New width
                    int(card_image.get_height() * CARD_SCALE),  # New height
                ),
            )

# Call the function
load_and_scale_card_images()


class Button:
    """A class to represent buttons in the game."""

    def __init__(self, text, pos, size, color, text_color, font):
        """Initialize characteristics of buttons."""
        # Button text
        self.text = text
        # Position of the button
        self.pos = pos
        # Size of the button
        self.size = size
        # Background color of the button
        self.color = color
        # Color of the text
        self.text_color = text_color
        # Font
        self.font = font
        # rectangle for the button
        self.rect = pygame.Rect(pos, size)
        self.rendered_text = self.font.render(text, True, self.text_color)
        self.text_rect = self.rendered_text.get_rect(center=self.rect.center)

    def draw(self, surface):
        """Draws and displays the button on the screen."""
        # Draw the button's rectangle
        pygame.draw.rect(surface, self.color, self.rect)
        # Draw the button
        surface.blit(self.rendered_text, self.text_rect)

    def is_clicked(self, event):
        """Check if the button is clicked based on the event."""
        # Check for mouse button down event
        return (
            event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
            and self.rect.collidepoint(event.pos)
        )


# Start button
start_button = Button(
    "Start", (400, 350), (200, 80), COLOR_RED, (255, 255, 255), font
)

# Instructions button
instructions_button = Button(
    "Instructions", (650, 350), (250, 80), COLOR_RED, (255, 255, 255), font
)

# Exit button
exit_button = Button(
    "Exit",
    (SCREEN_WIDTH - 400, SCREEN_HEIGHT - 90),
    (100, 50),
    COLOR_RED,
    (255, 255, 255),
    font,
)

# Reveal Cards button
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

# Draw Card button
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

# Play button
play_button = Button(
    "PLAY",
    (SCREEN_WIDTH - 200, SCREEN_HEIGHT - 60),
    (100, 50),
    COLOR_RED,
    TEXT_COLOR,
    font,
)

# Game state variables
state = "home"
# Indicates if cards are to be revealed
reveal_cards = False
# if the reveal button has been clicked
reveal_button_clicked = False
# player cards
player_cards = []
# computer cards
computer_cards = []
# discard pile
discard_pile = []
# List of cards in the deck
deck = []
# track of the card that has been clicked
selected_card = None
# Direction of play
direction = 1


def draw_home_screen():
    """Draw the home screen with all buttons."""
    # Draw background first
    screen.blit(home_background_image, (0, 0))
    start_button.draw(screen)
    instructions_button.draw(screen)
    exit_button.draw(screen)
    # Update the display
    pygame.display.flip()


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

        if discard_pile:
            top_card = discard_pile[0]
            if not card_matches_top_card(card, top_card):
                display_message("Card doesn't match! Computer's turn.", 1000)
                pygame.time.wait(1000)
                computer_turn()


def card_matches_top_card(card, top_card):
    """Check if the drawn card matches the top card on the discard pile."""
    card_color, card_value = card.split("_")
    top_color, top_value = top_card.split("_")
    return card_color == top_color or card_value == top_value


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

    # Draw the Start and Play buttons on the instructions screen
    play_button.draw(screen)
    # Update the display
    pygame.display.flip()

    # Wait for player interaction
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                waiting = False
            if start_button.is_clicked(event) or play_button.is_clicked(event):
                shuffle_and_deal()
                state = "play"
                waiting = False


def draw_player_cards():
    """Draw the player's cards on the screen."""
    global screen, game_background_image
    # Clear the background
    screen.blit(game_background_image, (0, 0))

    card_width, card_height = scaled_card_back_image.get_size()
    for i, card in enumerate(player_cards):
        # Determine the card's position
        card_x = (
            i * (card_width + CARD_SPACING)
            + (
                SCREEN_WIDTH
                - ((card_width + CARD_SPACING) * len(player_cards))
            )
            // 2
        )
        card_y = SCREEN_HEIGHT - card_height - 20

        # If the card is selected, move it up
        if card == selected_card:
            # Move the card up by 20 pixels
            card_y -= 20

        # Draw the card
        card_image = card_images[card]
        screen.blit(card_image, (card_x, card_y))
    # Update the display to show the new positions
    pygame.display.flip()


def get_card_at_position(x, y):
    """Check if the mouse position is over a card and return the card key."""
    card_width, card_height = scaled_card_back_image.get_size()
    # Use length of player_cards
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

        # If the card is selected, move it up
        if player_cards[i] == selected_card:
            # Adjust the y position for the selected card
            card_y -= 20

        if (
            card_x <= x <= card_x + card_width
            and card_y <= y <= card_y + card_height
        ):
            return player_cards[i]
    return None


def play_card(card_key):
    """Handle the action of playing a card from the player's hand."""
    global \
        discard_pile, \
        player_cards, \
        selected_card, \
        computer_cards, \
        deck, \
        direction
    # Check if the selected card is in the player's hand
    if card_key in player_cards:
        print(f"Attempting to play card: {card_key}")

        # Split card into color and value
        card_color, card_value = card_key.split("_")
        # Get the top card from the discard pile
        top_card = discard_pile[0] if discard_pile else None

        # Check if the card can be played
        if top_card:
            top_color, top_value = top_card.split("_")
            if card_color != top_color and card_value != top_value:
                # If the card cannot be played
                display_message("Wrong selection! Lost your chance", 1000)
                pygame.time.wait(1000)
                computer_turn()
                return

        # Keep the card raised
        selected_card = card_key
        draw_player_cards()
        pygame.display.flip()

        # Remove the card from player's hand and add it to the discard pile
        player_cards.remove(card_key)
        discard_pile.insert(0, card_key)
        # Deselect the card after it's played
        selected_card = None
        print(f"Player played: {card_key}")

        # Handle special cards
        if card_value == "+2":
            # Draw 2 cards for the computer
            for _ in range(2):
                if deck:
                    drawn_card = random.choice(deck)
                    deck.remove(drawn_card)
                    computer_cards.append(drawn_card)
            display_message("Computer drew 2 cards!", 1000)

        elif card_value == "rev":
            # Reverse the direction of play
            direction *= -1
            display_message("Reverse card played!", 1000)
            return

        elif card_value == "skip":
            # Skip the next player's turn
            direction *= -1
            display_message("Skip card played!", 1000)
            return

        elif card_value == "+4":
            # Draw 4 cards for the computer
            for _ in range(4):
                if deck:
                    drawn_card = random.choice(deck)
                    deck.remove(drawn_card)
                    computer_cards.append(drawn_card)
            display_message("Computer drew 4 cards!", 1000)
            display_message("Your turn!", 1000)

        # Check if the player has won
        if not player_cards:
            print("Player has no more cards. Player won the game!")
            end_game("YOU WON!")

        # After the player serves, give control to the computer
        computer_turn()


def draw_card_for_computer():
    """Draw a card for the computer from the deck."""
    global deck, computer_cards

    if deck:
        drawn_card = random.choice(deck)
        while drawn_card == "+4":
            drawn_card = random.choice(deck)
        deck.remove(drawn_card)
        computer_cards.append(drawn_card)
        print(f"Computer drew a card: {drawn_card}")


def display_message(message, duration):
    """Display a message on the screen for a specified duration."""
    global screen, font, SCREEN_WIDTH, SCREEN_HEIGHT, game_background_image
    # Clear the screen with the background image
    screen.blit(game_background_image, (0, 0))
    # Render the text
    text = font.render(message, True, COLOR_RED)
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    # Display the text on the screen
    screen.blit(text, text_rect)
    pygame.display.flip()
    # Wait for the specified duration
    pygame.time.wait(duration)


def shuffle_and_deal():
    """Shuffle the deck and deal cards to the player and computer."""
    global deck, player_cards, computer_cards, discard_pile

    # Define all possible cards
    deck = []

    # Create number cards
    for color in card_colors:
        for number in range(10):
            deck.append(f"{color}_{number}")

    # Create special cards
    for color in card_colors:
        for special in special_cards:
            deck.append(f"{color}_{special}")

    # Shuffle the deck
    random.shuffle(deck)

    # Deal 7 cards to the player and computer
    player_cards = [deck.pop() for _ in range(NUM_CARDS)]
    computer_cards = [deck.pop() for _ in range(NUM_CARDS)]

    # Set the initial discard pile card
    while True:
        discard_pile = [deck.pop()]
        if discard_pile[0] not in wild_cards:
            break

    # Print the initial state for debugging
    print("Deck:", deck)
    print("Player Cards:", player_cards)
    print("Computer Cards:", computer_cards)
    print("Discard Pile:", discard_pile)


def computer_turn():
    """Perform the computer's turn."""
    global computer_cards, discard_pile, deck, direction, player_cards

    pygame.time.wait(2000)

    if computer_cards:
        # Get the top card from the discard pile
        top_card = discard_pile[0] if discard_pile else None

        if top_card:
            try:
                top_color, top_value = top_card.split("_")
            except ValueError:
                print(f"Error: Invalid top card format: {top_card}")
                return

            playable_card = None

            # Find a playable card from the computer's hand
            for card in computer_cards:
                card_color, card_value = card.split("_")
                if card_color == top_color or card_value == top_value:
                    playable_card = card
                    break

            if playable_card:
                # Play the selected card
                computer_cards.remove(playable_card)
                discard_pile.insert(0, playable_card)
                print(f"Computer played: {playable_card}")

                # Handle special cards
                if "+2" in playable_card:
                    # Draw 2 cards for the player
                    for _ in range(2):
                        if deck:
                            drawn_card = random.choice(deck)
                            deck.remove(drawn_card)
                            player_cards.append(drawn_card)
                    display_message(
                        "Computer played +2 card! You drew 2 cards.", 1000
                    )

                elif "rev" in playable_card:
                    # Reverse the direction of play
                    direction *= -1
                    display_message("Computer played Reverse card!", 1000)
                    computer_turn()
                    return

                elif "skip" in playable_card:
                    # Skip the player's turn
                    direction *= -1
                    display_message("Computer played Skip card!", 1000)
                    computer_turn()
                    return

                elif "+4" in playable_card:
                    # Draw 4 cards for the player
                    for _ in range(4):
                        if deck:
                            drawn_card = random.choice(deck)
                            deck.remove(drawn_card)
                            player_cards.append(drawn_card)
                    display_message("Computer played +4 card!", 2000)

                # Check if the computer has won
                if not computer_cards:
                    end_game("YOU LOST!")

            else:
                # If no playable card, draw from the deck
                if deck:
                    drawn_card = random.choice(deck)
                    deck.remove(drawn_card)
                    computer_cards.append(drawn_card)
                    print(f"Computer drew: {drawn_card}")

                    try:
                        drawn_card_color = drawn_card.split("_")
                        drawn_card_value = drawn_card.split("_")
                        matches_color = drawn_card_color == top_color
                        matches_value = drawn_card_value == top_value

                        if matches_color or matches_value:
                            # Play the drawn card if it matches
                            computer_cards.remove(drawn_card)
                            discard_pile.insert(0, drawn_card)
                            print(f"Computer played: {drawn_card}")

                            if drawn_card == "+4":
                                # Draw 4 cards for the computer
                                for _ in range(4):
                                    if deck:
                                        drawn_card = random.choice(deck)
                                        deck.remove(drawn_card)
                                        computer_cards.append(drawn_card)
                                display_message(
                                    "Computer played +4 card!", 2000
                                )

                            elif "rev" in drawn_card:
                                # Reverse the direction of play
                                direction *= -1
                                display_message(
                                    "Computer played Reverse card!", 2000
                                )
                                computer_turn()
                                return

                            elif "skip" in drawn_card:
                                # Skip the player's turn
                                direction *= -1
                                display_message(
                                    "Computer played Skip card!", 2000
                                )
                                computer_turn()
                                return

                            # Check if the computer has won
                            if not computer_cards:
                                end_game("YOU LOST!")

                        else:
                            print("Computer didn't find a matching card.")
                            display_message("Your turn!", 1000)

                    except ValueError:
                        print(
                            f"Error: Invalid drawn card format: {drawn_card}"
                        )

        else:
            print("Error: No top card on discard pile.")
    else:
        print("Error: No cards in computer's hand.")


def end_game(message):
    """Display the end game screen."""
    global state
    # Set game state to "end"
    state = "end"
    screen.blit(game_background_image, (0, 0))
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
                player_cards = []
                computer_cards = []
                deck = []
                discard_pile = []
                reveal_cards = False
                reveal_button_clicked = False
                waiting = False
            if instructions_button.is_clicked(event):
                display_instructions()


def play_game():
    """Display the game screen with cards and other UI elements."""
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
    for i in range(len(player_cards)):
        x = (
            i * (card_width + CARD_SPACING)
            + (
                SCREEN_WIDTH
                - ((card_width + CARD_SPACING) * len(player_cards))
            )
            // 2
        )
        y = SCREEN_HEIGHT - card_height - 20
        if i < len(player_cards):
            card_key = player_cards[i]
            if reveal_cards:
                if card_key == selected_card:
                    # Move selected card up by 30 pixels
                    y -= 30
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


def main():
    """Main game loop."""
    global state, reveal_cards, reveal_button_clicked
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if state == "home":
                if start_button.is_clicked(event) or play_button.is_clicked(
                    event
                ):
                    state = "play"
                    shuffle_and_deal()
                elif instructions_button.is_clicked(event):
                    display_instructions()
                elif exit_button.is_clicked(event):
                    pygame.quit()
                    sys.exit()

            elif state == "play":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if draw_card_button.rect.collidepoint(x, y):
                        draw_card_from_deck()
                    else:
                        card_key = get_card_at_position(x, y)
                        if card_key and reveal_cards:
                            selected_card = card_key
                            play_game()
                            pygame.display.flip()
                            pygame.time.wait(100)
                            play_card(card_key)
                            selected_card = None

                if reveal_button.is_clicked(event):
                    reveal_cards = True
                    reveal_button_clicked = True

            elif state == "end":
                # Or your specific end game condition
                end_game("Game Over")

        if state == "home":
            draw_home_screen()
        elif state == "play":
            play_game()
        elif state == "end":
            end_game("Game Over")

        pygame.display.flip()


if __name__ == "__main__":
    main()

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
                        pygame.time.wait(100)
                        play_card(card_key)
                        selected_card = None

            if reveal_button.is_clicked(event):
                reveal_cards = True
                reveal_button_clicked = True

        if state == "home":
            if start_button.is_clicked(event):
                shuffle_and_deal()
                state = "play"
            else:
                screen.blit(home_background_image, (0, 0))
                start_button.draw(screen)
        elif state == "home":
            if play_button.is_clicked(event):
                shuffle_and_deal()
                state = "play"
        elif state == "play":
            play_game()

        pygame.display.flip()

pygame.quit()
sys.exit()
