"""
A simple implementation of Game of Life with tribal dynamics,
supporting iPhone 15 Pro portrait aspect ratio
"""
import sys
import pygame
import numpy as np
import random

# iPhone 15 Pro has aspect ratio of 2.16:1 in portrait mode
WIDTH = 600  # Width of the screen in pixels
HEIGHT = 1296  # Height of the screen in pixels (600 * 2.16)
BUTTON_WIDTH = 150  # Width of the button in pixels
BUTTON_HEIGHT = 50  # Height of the button in pixels

# Colors for different tribes
DEAD_COLOR = (0, 0, 0)
TRANSPARENT_COLOR = (0, 0, 0)
TRIBE_COLORS = [
    (0, 0, 0),          # 0: Dead cells
    (255, 255, 255),    # 1: White tribe
    (255, 50, 50),      # 2: Red tribe
    (50, 255, 50),      # 3: Green tribe
    (50, 50, 255),      # 4: Blue tribe
    (255, 255, 50),     # 5: Yellow tribe
]

# Number of tribes (excluding dead cells)
NUM_TRIBES = len(TRIBE_COLORS) - 1

# Cell size in pixels
CELL_SIZE = 10

# Current selected tribe (default to tribe 1)
CURRENT_TRIBE = 1


def game_of_life(board):
    """
    Apply the rules of the Game of Life to the board with tribal dynamics
    """
    # Copy the board to a new array to avoid modifying the original
    new_board = np.copy(board)
    
    for i in range(1, board.shape[0]-1):
        for j in range(1, board.shape[1]-1):
            # Get the 3x3 neighborhood
            neighborhood = board[i-1:i+2, j-1:j+2]
            current_cell = board[i, j]
            
            # Count cells of each tribe in the neighborhood
            tribe_counts = [0] * (NUM_TRIBES + 1)
            for tribe in range(NUM_TRIBES + 1):
                # Count cells of this tribe (excluding the center cell)
                if tribe == current_cell:
                    tribe_counts[tribe] = np.sum(neighborhood == tribe) - 1
                else:
                    tribe_counts[tribe] = np.sum(neighborhood == tribe)
            
            # Total neighbors (excluding self)
            total_neighbors = np.sum(tribe_counts) - tribe_counts[0]
            
            # Apply Game of Life rules with tribal dynamics
            if current_cell > 0:  # Cell is alive (part of a tribe)
                # Fewer than 2 or more than 3 neighbors of any tribe: die
                if total_neighbors < 2 or total_neighbors > 3:
                    new_board[i, j] = 0
            else:  # Cell is dead
                # Exactly 3 neighbors: become part of the majority tribe
                if total_neighbors == 3:
                    # Find the tribe with the most representatives
                    max_count = 0
                    dominant_tribes = []
                    
                    for tribe in range(1, NUM_TRIBES + 1):
                        if tribe_counts[tribe] > max_count:
                            max_count = tribe_counts[tribe]
                            dominant_tribes = [tribe]
                        elif tribe_counts[tribe] == max_count:
                            dominant_tribes.append(tribe)
                    
                    # Randomly choose among dominant tribes if there's a tie
                    if dominant_tribes:
                        new_board[i, j] = random.choice(dominant_tribes)
    
    return new_board

def draw_board(screen, board, previous_board):
    """
    Render the board to the screen with different colors for different tribes
    """
    for board_x in range(board.shape[0]):
        for board_y in range(board.shape[1]):
            if board[board_x, board_y] != previous_board[board_x, board_y]:
                # Get the color based on the tribe
                tribe = board[board_x, board_y]
                color = TRIBE_COLORS[tribe]
                
                rect = (board_x * CELL_SIZE, board_y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(screen, color, rect)
                pygame.display.update(rect)
    
    previous_board[:] = board

def draw_buttons(screen, running, draw, current_tribe):
    """ Render the Draw/Erase, Reset, Start/Pause, and Tribe Selection buttons on the screen
    """
    # Set up font for button text
    font = pygame.font.Font(None, 30)

    # Create the draw button -- this is only visible when the game is not running
    draw_button = pygame.Rect((WIDTH - BUTTON_WIDTH)//2, HEIGHT - 5*BUTTON_HEIGHT-40,\
                              BUTTON_WIDTH, BUTTON_HEIGHT)

    # Create the reset button -- this is only visible when the game is not running
    reset_button = pygame.Rect((WIDTH - BUTTON_WIDTH)//2, HEIGHT - 4*BUTTON_HEIGHT-30,\
                               BUTTON_WIDTH, BUTTON_HEIGHT)
    
    # Create tribe selection buttons (one for each tribe)
    tribe_buttons = []
    for i in range(1, NUM_TRIBES + 1):
        tribe_button = pygame.Rect((WIDTH - BUTTON_WIDTH)//2, HEIGHT - (4-i)*BUTTON_HEIGHT-20,\
                                  BUTTON_WIDTH, BUTTON_HEIGHT)
        tribe_buttons.append(tribe_button)

    blank_text = font.render("********", True, DEAD_COLOR, (0,0,0,0))

    if running:
        game_button_name = "Pause"
        draw_text = blank_text
        reset_text = blank_text
        tribe_texts = [blank_text] * NUM_TRIBES
        button_color = (0, 0, 0)
    else:
        if draw:
            draw_title = "Draw"
        else:
            draw_title = "Erase"
        game_button_name = " Start "
        # Draw the text on the reset button
        reset_text = font.render("Reset", True, (255,255,255), (0,0,0,0))
        draw_text = font.render(draw_title, True, (255,255,255), (0,0,0,0))
        
        # Tribe selection texts
        tribe_texts = []
        for i in range(1, NUM_TRIBES + 1):
            tribe_name = f"Tribe {i}"
            text_color = (255, 255, 255)
            tribe_texts.append(font.render(tribe_name, True, text_color, (0,0,0,0)))
        
        button_color = (255, 0, 0)

    # Draw/Erase button
    screen.blit(draw_text, (draw_button.x + (draw_button.width - draw_text.get_width()) \
                // 2, draw_button.y + (draw_button.height - draw_text.get_height()) // 2))
    pygame.draw.rect(screen, button_color, draw_button, 2)
    
    # Reset button
    screen.blit(reset_text, (reset_button.x + (reset_button.width - reset_text.get_width()) \
                // 2, reset_button.y + (reset_button.height - reset_text.get_height()) // 2))
    pygame.draw.rect(screen, button_color, reset_button, 2)
    
    # Tribe selection buttons
    for i, (tribe_button, tribe_text) in enumerate(zip(tribe_buttons, tribe_texts)):
        screen.blit(tribe_text, (tribe_button.x + (tribe_button.width - tribe_text.get_width()) \
                    // 2, tribe_button.y + (tribe_button.height - tribe_text.get_height()) // 2))
        # Highlight the currently selected tribe
        if i + 1 == current_tribe:
            button_outline_color = TRIBE_COLORS[i + 1]
            thickness = 4
        else:
            button_outline_color = button_color
            thickness = 2
        pygame.draw.rect(screen, button_outline_color, tribe_button, thickness)

    # Create the start/pause game button -- this button is always visible
    start_game_button = pygame.Rect((WIDTH - BUTTON_WIDTH)//2, HEIGHT - BUTTON_HEIGHT - 10, \
                            BUTTON_WIDTH, BUTTON_HEIGHT)

    start_game_text = font.render(game_button_name, True, (255,255,255), (0,0,0,0))
    # draw the blank surface over the previous text
    screen.blit(start_game_text, (start_game_button.x + \
                (start_game_button.width - start_game_text.get_width()) // 2, \
                start_game_button.y + (start_game_button.height - \
                start_game_text.get_height()) // 2))
    pygame.draw.rect(screen, (255, 0, 0), start_game_button, 2)

    return start_game_button, reset_button, draw_button, tribe_buttons

def main():
    """ Main function"""

    # Initialize pygame
    pygame.init()

    # Create a blank board
    # Use integers instead of booleans to represent different tribes (0 = dead, 1-5 = tribes)
    board_width = 60  # Adjusted for aspect ratio
    board_height = 120  # Adjusted for aspect ratio
    game_board = np.zeros((board_width, board_height), dtype=int)
    clock = pygame.time.Clock()
    f_p_s = 60
    mouse_down = False
    draw = True
    running = False
    current_tribe = 1  # Start with tribe 1 selected

    # Set window size and title
    game_screen_size = (WIDTH, HEIGHT)
    game_screen = pygame.display.set_mode(game_screen_size)
    pygame.display.set_caption("Game of Life - Tribal Edition")

    while True:
        previous_board = np.copy(game_board)
        start_game_button, reset_button, draw_button, tribe_buttons = draw_buttons(
            game_screen, running, draw, current_tribe)

        # Check for mouse events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if running:
                    if start_game_button.collidepoint(event.pos):
                        running = not running
                else:
                    if start_game_button.collidepoint(event.pos):
                        running = not running
                    elif reset_button.collidepoint(event.pos):
                        # reset the board to blank
                        game_board = np.zeros((board_width, board_height), dtype=int)
                    elif draw_button.collidepoint(event.pos):
                        draw = not draw
                    else:
                        # Check if a tribe button was clicked
                        for i, tribe_button in enumerate(tribe_buttons):
                            if tribe_button.collidepoint(event.pos):
                                current_tribe = i + 1
                                break
                        else:
                            mouse_down = True
            elif event.type == pygame.MOUSEBUTTONUP:
                mouse_down = False

        if running:
            # Update the board
            game_board = game_of_life(game_board)

        if mouse_down:
            # draw/erase a cell
            mouse_x, mouse_y = pygame.mouse.get_pos()
            board_x, board_y = mouse_x // CELL_SIZE, mouse_y // CELL_SIZE
            if 0 <= board_x < game_board.shape[0] and 0 <= board_y < game_board.shape[1]:
                if draw:
                    # Draw with the current tribe
                    game_board[board_x, board_y] = current_tribe
                else:
                    # Erase (set to dead)
                    game_board[board_x, board_y] = 0

        # Draw the board
        draw_board(game_screen, game_board, previous_board)

        pygame.display.flip()
        clock.tick(f_p_s)


if __name__ == "__main__":
    main()
