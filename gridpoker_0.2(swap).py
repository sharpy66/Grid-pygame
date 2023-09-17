import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 1300
SCREEN_HEIGHT = 1024
GRID_SIZE = 5
CARD_SIZE = 150
CARD_SPACING = 20
GRID_X = 50
GRID_Y = 50
DECK_X = GRID_X + (GRID_SIZE * (CARD_SIZE + CARD_SPACING)) + 50
DECK_Y = 50
BUTTON_X = DECK_X
BUTTON_Y = DECK_Y + CARD_SIZE + 20
CARD_X = DECK_X + CARD_SIZE + 20
CARD_Y = DECK_Y
LINE_COLOR = (255, 255, 255) 
EMPTY_COLOR = (0, 255, 0) 
FILLED_COLOR = (255, 0, 0) 
BACKGROUND_COLOR = (255, 255, 255)
BACKGROUND_SIZE = CARD_SIZE - 20
exit_button_rect = pygame.Rect(BUTTON_X, BUTTON_Y + (CARD_SIZE + 20) * 2, CARD_SIZE, CARD_SIZE)
# Colors
WHITE = (255, 255, 255)

            # Define a constant for the swap button position and size
SWAP_X = BUTTON_X
SWAP_Y = BUTTON_Y + (CARD_SIZE + 20) * 3
swap_button_rect = pygame.Rect(SWAP_X, SWAP_Y, CARD_SIZE, CARD_SIZE)

# Define a variable to store the first card selected for swapping
first_card = None

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Poker Grid Game")

# Create a deck of cards
suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King", "Ace"]
deck = [{"suit": suit, "rank": rank} for suit in suits for rank in ranks]

# Shuffle the deck
random.shuffle(deck)

# Initialize variables
grid = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
score = 0
score_button_rect = pygame.Rect(BUTTON_X, BUTTON_Y, CARD_SIZE, CARD_SIZE)
reset_button_rect = pygame.Rect(BUTTON_X, BUTTON_Y + CARD_SIZE + 20, CARD_SIZE, CARD_SIZE)
card_rect = pygame.Rect(CARD_X, CARD_Y, CARD_SIZE, CARD_SIZE) # This is the added line
card_drawn = None # This is the added line
total_score = 0
high_score = 0
# Function to draw the grid # This is the modified function
def draw_grid():
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            card = grid[row][col]
            if card:
                x = GRID_X + col * (CARD_SIZE + CARD_SPACING)
                y = GRID_Y + row * (CARD_SIZE + CARD_SPACING)
                # Draw a white rectangle with a smaller size than the grid space 
                pygame.draw.rect(screen, BACKGROUND_COLOR, (x + 10, y + 10, BACKGROUND_SIZE, BACKGROUND_SIZE))
                font = pygame.font.Font(None, 24)
                lines = [f"{card['rank']} of {card['suit']}"]
                max_text_width = CARD_SIZE - 20
                y_offset = y + 10
                for line in lines:
                    text = font.render(line, True, (0, 0, 0))
                    text_rect = text.get_rect()
                    # Center the text with the card 
                    text_rect.center = (x + CARD_SIZE // 2, y + CARD_SIZE // 2) 
                    screen.blit(text, text_rect)
                    y_offset += text_rect.height + 5


# Function to display the deck
def draw_deck():
    pygame.draw.rect(screen, WHITE, (DECK_X, DECK_Y, CARD_SIZE, CARD_SIZE))

# Function to draw the deck count
def draw_deck_count():
    font = pygame.font.Font(None, 24)
    text = font.render(f"Deck: {len(deck)} cards", True, (0, 0, 0))
    
    text_x = DECK_X + 10 # Adjust as needed
    text_y = DECK_Y + 10
    
    screen.blit(text, (text_x, text_y))

# Function to display the drawn card # This is the added function
def draw_card():
    if card_drawn:
        pygame.draw.rect(screen, WHITE, (CARD_X, CARD_Y, CARD_SIZE, CARD_SIZE))
        font = pygame.font.Font(None, 24)
        lines = [f"{card_drawn['rank']} of {card_drawn['suit']}"]
        max_text_width = CARD_SIZE - 20
        y_offset = CARD_Y + 10
        for line in lines:
            text = font.render(line, True, (0, 0, 0))
            text_rect = text.get_rect()
            text_rect.center = (CARD_X + CARD_SIZE // 2, y_offset)
            screen.blit(text, text_rect)
            y_offset += text_rect.height + 5

# Function to evaluate a poker hand # This is the updated function from before
def evaluate_hand(cards):
    # Sort the cards by rank in descending order
    ranks = ['Ace', 'King', 'Queen', 'Jack', '10', '9', '8', '7', '6', '5', '4', '3', '2']
    cards.sort(key=lambda card: ranks.index(card['rank']), reverse=True)

    # Get the rank and suit of each card
    rank_list = [card['rank'] for card in cards]
    suit_list = [card['suit'] for card in cards]

    # Check for a straight flush (five cards of the same suit in sequential order)
    # Aces can be either high or low in a straight
    if len(set(suit_list)) == 1 and (rank_list in [ranks[i:i + 5] for i in range(9)] or rank_list == ['Ace', '5', '4', '3', '2']):
        # If the highest card is an ace, it is a royal flush (the best possible hand)
        if rank_list[0] == 'Ace':
            return 10, "Royal Flush"
        else:
            return 9, f"Straight Flush ({rank_list[0]} high)"

    # Check for four of a kind (four cards of the same rank)
    for rank in set(rank_list):
        if rank_list.count(rank) == 4:
            return 8, f"Four of a Kind ({rank}s)"

    # Check for a full house (three cards of the same rank and two cards of another rank)
    for rank1 in set(rank_list):
        if rank_list.count(rank1) == 3:
            for rank2 in set(rank_list):
                if rank_list.count(rank2) == 2:
                    return 7, f"Full House ({rank1}s over {rank2}s)"

    # Check for a flush (five cards of the same suit)
    if len(set(suit_list)) == 1:
        return 6, f"Flush ({suit_list[0]}s)"

    # Check for a straight (five cards in sequential order)
    # Aces can be either high or low in a straight
    if rank_list in [ranks[i:i + 5] for i in range(9)] or rank_list == ['Ace', '5', '4', '3', '2']:
        return 5, f"Straight ({rank_list[0]} high)"

    # Check for three of a kind (three cards of the same rank)
    for rank in set(rank_list):
        if rank_list.count(rank) == 3:
            return 4, f"Three of a Kind ({rank}s)"

    # Check for two pair (two cards of the same rank and two cards of another rank)
    pairs = set()
    for rank in set(rank_list):
        if rank_list.count(rank) == 2:
            pairs.add(rank)
    if len(pairs) == 2:
        return 3, f"Two Pair ({pairs.pop()}s and {pairs.pop()}s)"

    # Check for one pair (two cards of the same rank)
    if len(pairs) == 1:
        return 2, f"One Pair ({pairs.pop()}s)"

    # Otherwise, it is a high card (the highest card in the hand)
    return 1, f"High Card ({rank_list[-1]})"

# Function to calculate scores for diagonals, rows, and columns 
def calculate_scores():
    scores = []
    descriptions = []

    # Check if the grid is empty 
    if all(grid[row][col] is None for row in range(GRID_SIZE) for col in range(GRID_SIZE)): # This is the added line
        return scores, descriptions 

    # Check diagonals from top-left to bottom-right
    for i in range(GRID_SIZE - 4):
        for j in range(GRID_SIZE - 4):
            diagonal = [grid[i + k][j + k] for k in range(5)]
            
            # Skip evaluation if any card in the diagonal is None
            if None in diagonal:
                continue

            score, description = evaluate_hand(diagonal)
            location = f"Diagonal {i + j + 1}"
            scores.append(score)
            descriptions.append(f"{location} - {description}")

    # Check diagonals from top-right to bottom-left
    for i in range(GRID_SIZE - 4):
        for j in range(GRID_SIZE - 4):
            diagonal = [grid[i + k][j + 4 - k] for k in range(5)]
            
            # Skip evaluation if any card in the diagonal is None
            if None in diagonal:
                continue

            score, description = evaluate_hand(diagonal)
            location = f"Diagonal {GRID_SIZE - i - j}"
            scores.append(score)
            descriptions.append(f"{location} - {description}")

    # Check rows
    for i, row in enumerate(grid):
        for j in range(GRID_SIZE - 4):
            row_slice = row[j:j + 5]

            # Skip evaluation if any card in the row is None
            if None in row_slice:
                continue

            score, description = evaluate_hand(row_slice)
            location = f"Row {i + 1}"
            scores.append(score)
            descriptions.append(f"{location} - {description}")

    # Check columns
    for j in range(GRID_SIZE):
        for i in range(GRID_SIZE - 4):
            col_slice = [grid[i + k][j] for k in range(5)]

            # Skip evaluation if any card in the column is None
            if None in col_slice:
                continue

            score, description = evaluate_hand(col_slice)
            location = f"Column {j + 1}"
            scores.append(score)
            descriptions.append(f"{location} - {description}")

    return scores, descriptions

# Function to draw lines for the grid 
def draw_lines():
    for i in range(1, GRID_SIZE):
        # Draw vertical lines
        x = GRID_X + i * (CARD_SIZE + CARD_SPACING) - (CARD_SPACING // 2) 
        y1 = GRID_Y + (CARD_SPACING // 2) 
        y2 = GRID_Y + (GRID_SIZE * (CARD_SIZE + CARD_SPACING)) - (CARD_SPACING // 2) 
        pygame.draw.line(screen, LINE_COLOR, (x, y1), (x, y2))

        # Draw horizontal lines
        x1 = GRID_X + (CARD_SPACING // 2) # This is the changed line
        x2 = GRID_X + (GRID_SIZE * (CARD_SIZE + CARD_SPACING)) - (CARD_SPACING // 2) 
        y = GRID_Y + i * (CARD_SIZE + CARD_SPACING) - (CARD_SPACING // 2) 
        pygame.draw.line(screen, LINE_COLOR, (x1, y), (x2, y))

def highlight_spaces():
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            x = GRID_X + col * (CARD_SIZE + CARD_SPACING)
            y = GRID_Y + row * (CARD_SIZE + CARD_SPACING)
            rect = pygame.Rect(x, y, CARD_SIZE, CARD_SIZE)
            if grid[row][col] is None:
                # Draw a green rectangle with a thick border for empty spaces 
                pygame.draw.rect(screen, EMPTY_COLOR, rect, 10) # This is the changed line
            else:
                # Draw a red rectangle with a thick border for filled spaces 
                pygame.draw.rect(screen, FILLED_COLOR, rect, 10) 



# Main game loop
running = True
scoring_requested = False
scores_displayed = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if score_button_rect.collidepoint(mouse_x, mouse_y):
                # Button clicked, trigger scoring
                scoring_requested = True
                scores_displayed = False
                card_drawn = None
            elif DECK_X <= mouse_x <= DECK_X + CARD_SIZE and DECK_Y <= mouse_y <= DECK_Y + CARD_SIZE:
                # Draw a card from the deck and place it off to the side
                if len(deck) > 0 and card_drawn is None:
                    card_drawn = deck.pop()
                    # Update the screen after drawing a card
                    scoring_requested = False

                    pygame.display.flip()
            elif CARD_X <= mouse_x <= CARD_X + CARD_SIZE and CARD_Y <= mouse_y <= CARD_Y + CARD_SIZE:
                # Place the drawn card in the first grid space they click
                if card_drawn:
                    for row in range(GRID_SIZE):
                        for col in range(GRID_SIZE):
                            if grid[row][col] is None:
                                grid[row][col] = card_drawn
                                card_drawn = None
                                break
                    # Update the screen after placing a card
                    pygame.display.flip()
            elif GRID_X <= mouse_x <= GRID_X + (GRID_SIZE * (CARD_SIZE + CARD_SPACING)) and GRID_Y <= mouse_y <= GRID_Y + (GRID_SIZE * (CARD_SIZE + CARD_SPACING)):
                # Place the drawn card in the grid space they click 
                if card_drawn: 
                    row = (mouse_y - GRID_Y) // (CARD_SIZE + CARD_SPACING) 
                    col = (mouse_x - GRID_X) // (CARD_SIZE + CARD_SPACING) 
                    if grid[row][col] is None: 
                        grid[row][col] = card_drawn 
                        card_drawn = None 
                        # Update the screen after placing a card
                        pygame.display.flip() 
                # Swap the selected card with the first card selected for swapping 
                elif first_card: 
                    row = (mouse_y - GRID_Y) // (CARD_SIZE + CARD_SPACING) 
                    col = (mouse_x - GRID_X) // (CARD_SIZE + CARD_SPACING) 
                    if grid[row][col]: 
                        second_card = grid[row][col] 
                        grid[row][col] = first_card 
                        first_card_row, first_card_col = first_card['position'] 
                        grid[first_card_row][first_card_col] = second_card 
                        first_card = None 
                        # Update the screen after swapping cards
                        pygame.display.flip() 
                # Select the first card for swapping # This is the added code block
                else: 
                    row = (mouse_y - GRID_Y) // (CARD_SIZE + CARD_SPACING) 
                    col = (mouse_x - GRID_X) // (CARD_SIZE + CARD_SPACING) 
                    if grid[row][col]: 
                        first_card = grid[row][col] 
                        first_card['position'] = (row, col) # Store the position of the first card on the grid
            elif swap_button_rect.collidepoint(mouse_x, mouse_y):
                pygame.display.flip()
                score_displayed = False
                scoring_requested = False
                # Check if there is a card drawn from the deck
                if card_drawn:
                    # Display a message saying that the card must be placed on the grid before swapping
                    font = pygame.font.Font(None, 24)
                    text = font.render("Please place the drawn card on the grid before swapping", True, (255, 0, 0))
                    text_rect = text.get_rect()
                    text_rect.x = SWAP_X + CARD_SIZE + 20
                    text_rect.y = SWAP_Y
                    screen.blit(text, text_rect)
                    pygame.display.flip()
                # Check if there is a first card selected for swapping
                
                elif first_card:
                    # Display the first card selected for swapping next to the swap button
                    pygame.draw.rect(screen, WHITE, (SWAP_X + CARD_SIZE + 20, SWAP_Y, CARD_SIZE, CARD_SIZE))
                    font = pygame.font.Font(None, 24)
                    lines = [f"{first_card['rank']} of {first_card['suit']}"]
                    max_text_width = CARD_SIZE - 20
                    y_offset = SWAP_Y + 10
                    for line in lines:
                        text = font.render(line, True, (0, 0, 0))
                        text_rect = text.get_rect()
                        text_rect.center = (SWAP_X + CARD_SIZE + 20 + CARD_SIZE // 2, y_offset)
                        screen.blit(text, text_rect)
                        y_offset += text_rect.height + 5
                    # Prompt the player to select a second card from the grid
                    pygame.display.flip()
                    font = pygame.font.Font(None, 24)
                    text = font.render("Please select a second card from the grid to swap", True, (255, 255, 0))
                    text_rect = text.get_rect()
                    text_rect.x = SWAP_X + CARD_SIZE + 20
                    text_rect.y = SWAP_Y + CARD_SIZE + 10
                    screen.blit(text, text_rect)
                    pygame.display.flip()
                else:
                    # Prompt the player to select a first card from the grid
                    pygame.display.flip()
                    font = pygame.font.Font(None, 24)
                    text = font.render("Please select a first card from the grid to swap", True, (255, 255, 0))
                    text_rect = text.get_rect()
                    text_rect.x = SWAP_X + CARD_SIZE + 20
                    text_rect.y = SWAP_Y
                    screen.blit(text, text_rect)
                    pygame.display.flip()
            elif reset_button_rect.collidepoint(mouse_x, mouse_y):
                # Button clicked, reset the grid and shuffle the deck
                grid = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
                deck = [{"suit": suit, "rank": rank} for suit in suits for rank in ranks]
                random.shuffle(deck)
                scoring_requested = False
                scores_displayed = False
                card_drawn = None
                first_card = None # This is the added line
            elif exit_button_rect.collidepoint(mouse_x, mouse_y):
                # Button clicked, end the game
                running = False

    # Fill the background only if scoring is not displayed
    if not (scoring_requested and scores_displayed):
        screen.fill((0, 0, 0))

        # Draw the grid and deck
        draw_grid()
        draw_deck()

        # Draw the drawn card 
        draw_card()

        # Draw the lines for the grid 
        draw_lines()

        # Highlight the spaces where cards can be placed 
        highlight_spaces()

        # Draw the swap button on the screen
        pygame.draw.rect(screen, (255, 255, 0), swap_button_rect)
        font = pygame.font.Font(None, 36)
        button_text = font.render("Swap", True, (0, 0, 0))
        button_text_rect = button_text.get_rect(center=swap_button_rect.center)
        screen.blit(button_text, button_text_rect)

        # Draw the scoring button
        pygame.draw.rect(screen, (0, 255, 0), score_button_rect)
        font = pygame.font.Font(None, 36)
        button_text = font.render("Score", True, (0, 0, 0))
        button_text_rect = button_text.get_rect(center=score_button_rect.center)
        screen.blit(button_text, button_text_rect)

        # Draw the reset button
        pygame.draw.rect(screen, (255, 0, 0), reset_button_rect)
        font = pygame.font.Font(None, 36)
        button_text = font.render("Reset", True, (0, 0, 0))
        button_text_rect = button_text.get_rect(center=reset_button_rect.center)
        screen.blit(button_text, button_text_rect)

        # Draw the exit button on the screen
        pygame.draw.rect(screen, (0, 0, 255), exit_button_rect)
        font = pygame.font.Font(None, 36)
        button_text = font.render("Exit", True, (0, 0, 0))
        button_text_rect = button_text.get_rect(center=exit_button_rect.center)
        screen.blit(button_text, button_text_rect)




    # Calculate and display scores if scoring is requested
    if scoring_requested and not scores_displayed:
        scores, descriptions = calculate_scores()
        font = pygame.font.Font(None, 24)
        y_offset = GRID_Y
                # Check if the scores and descriptions are empty 
        if len(scores) == 0 and len(descriptions) == 0: 
            # Display a message instead of looping through them 
            text = font.render("Not enough cards to calculate scores; need 5 in a row", True, (255, 0, 0)) 
            text_rect = text.get_rect() 
            text_rect.x = DECK_X + CARD_SIZE + 20 
            text_rect.y = y_offset 
            screen.blit(text, text_rect) 
            y_offset += text_rect.height + 5 
        else: 
            for score, description in zip(scores, descriptions):
                total_score = total_score + score
                text = font.render(f"{description} - Score: {score}", True, (255, 0, 0))
                text_rect = text.get_rect()
                text_rect.x = DECK_X + CARD_SIZE + 20
                text_rect.y = y_offset
                screen.blit(text, text_rect)
                y_offset += text_rect.height + 5
                # Display the total score at the end of the text
            text = font.render(f"Total score: {total_score}", True, (255, 0, 0))
            text_rect = text.get_rect()
            text_rect.x = DECK_X + CARD_SIZE + 20
            text_rect.y = y_offset
            screen.blit(text, text_rect)

            scores_displayed = True

    draw_deck_count()
    
    pygame.display.flip()
    total_score = 0
# Quit Pygame
pygame.quit()
