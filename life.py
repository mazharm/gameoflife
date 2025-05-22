"""
A simple implementation of Game of Life with fluid implementation of
board setup, optimized for iPhone 15 Pro in portrait mode, with tribal dynamics.
"""
import sys
import pygame
import numpy as np

# Detect if running in browser (via Pygbag/Pyodide)
try:
    import platform
    IN_BROWSER = platform.system() == 'Emscripten'
except:
    IN_BROWSER = False

WIDTH = 600  # Width of the screen in pixels
HEIGHT = 1296  # Height of the screen in pixels (iPhone 15 Pro portrait ratio ~2.16:1)
BUTTON_WIDTH = 150  # Width of the button in pixels
BUTTON_HEIGHT = 50  # Height of the button in pixels

# Colors
ALIVE_COLOR = (255, 255, 255)
DEAD_COLOR = (0, 0, 0)
TRANSPARENT_COLOR = (0, 0, 0)

# Tribe colors - each tribe has a unique color
TRIBE_COLORS = [
    DEAD_COLOR,            # 0: Dead cell
    ALIVE_COLOR,           # 1: Default tribe (white)
    (255, 0, 0),          # 2: Red tribe
    (0, 255, 0),          # 3: Green tribe
    (0, 0, 255),          # 4: Blue tribe
    (255, 255, 0),        # 5: Yellow tribe
    (255, 0, 255),        # 6: Magenta tribe
    (0, 255, 255),        # 7: Cyan tribe
    (255, 128, 0),        # 8: Orange tribe
    (128, 0, 255)         # 9: Purple tribe
]

# Maximum number of tribes
MAX_TRIBES = len(TRIBE_COLORS) - 1  # Subtract 1 because index 0 is for dead cells

# Cell size in pixels
CELL_SIZE = 7

# Board position offset for centering
BOARD_X_OFFSET = (WIDTH - 80 * CELL_SIZE) // 2
BOARD_Y_OFFSET = 50  # Provide some space at the top


def game_of_life(board, tribal_mode=True):
    """
    Apply the rules of the Game of Life to the board with tribal dynamics
    """
    # Copy the board to a new array to avoid modifying the original
    new_board = np.copy(board)
    
    if tribal_mode:
        # Tribal mode logic
        for i in range(1, board.shape[0]-1):
            for j in range(1, board.shape[1]-1):
                # Get the neighborhood window
                neighbors_window = board[i-1:i+2, j-1:j+2].copy()
                # Count living neighbors (cells with non-zero values)
                living_neighbors = np.sum(neighbors_window > 0) - (board[i, j] > 0)
                
                # Get counts of each tribe in the neighborhood
                unique_tribes = {}
                for x in range(3):
                    for y in range(3):
                        if not (x == 1 and y == 1):  # Skip the center cell
                            tribe = neighbors_window[x, y]
                            if tribe > 0:  # If it's a living cell
                                unique_tribes[tribe] = unique_tribes.get(tribe, 0) + 1
                
                # Apply Game of Life rules with tribal dynamics
                if board[i, j] > 0:  # If cell is alive
                    if living_neighbors < 2 or living_neighbors > 3:
                        new_board[i, j] = 0  # Cell dies
                else:  # If cell is dead
                    if living_neighbors == 3:
                        # Cell is born - determine which tribe based on neighbors
                        if unique_tribes:  # If there are living neighbors
                            # Find the dominant tribe (tribe with most neighbors)
                            dominant_tribe = max(unique_tribes.items(), key=lambda x: x[1])[0]
                            new_board[i, j] = dominant_tribe
    else:
        # Standard Game of Life logic
        for i in range(1, board.shape[0]-1):
            for j in range(1, board.shape[1]-1):
                # Count the number of live neighbors (any non-zero value is alive)
                neighbors = np.sum(board[i-1:i+2, j-1:j+2] > 0) - (board[i, j] > 0)
                # Apply the rules of the Game of Life
                if board[i, j] > 0:
                    if neighbors < 2 or neighbors > 3:
                        new_board[i, j] = 0
                else:
                    if neighbors == 3:
                        # In standard mode, all new cells will be tribe 1
                        new_board[i, j] = 1
    
    return new_board

def draw_board(screen, board, previous_board):
    """
    Render the board to the screen
    """
    for board_x in range(board.shape[0]):
        for board_y in range(board.shape[1]):
            if board[board_x, board_y] != previous_board[board_x, board_y]:
                # Get color based on tribe ID
                tribe_id = int(board[board_x, board_y])
                color = TRIBE_COLORS[min(tribe_id, len(TRIBE_COLORS) - 1)]
                rect = (BOARD_X_OFFSET + board_x * CELL_SIZE, BOARD_Y_OFFSET + board_y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(screen, color, rect)
                pygame.display.update(rect)
    previous_board[:] = board

def draw_buttons(screen, running, draw, current_tribe=1, tribal_mode=True):
    """ Render the Draw/Erase, Reset and Start/Pause buttons on the screen
    """
    # Set up font for button text
    font = pygame.font.Font(None, 30)
    
    # Position buttons in the bottom area of the screen
    buttons_y_start = BOARD_Y_OFFSET + 80 * CELL_SIZE + 40  # Start button positioning below the board with some padding
    
    # Create the draw button -- this is only visible when the game is not running
    draw_button = pygame.Rect((WIDTH - BUTTON_WIDTH)//2, buttons_y_start,
                               BUTTON_WIDTH, BUTTON_HEIGHT)

    # Create the reset button -- this is only visible when the game is not running
    reset_button = pygame.Rect((WIDTH - BUTTON_WIDTH)//2, buttons_y_start + BUTTON_HEIGHT + 10,
                               BUTTON_WIDTH, BUTTON_HEIGHT)
                               
    # Create the tribe selection button
    tribe_button = pygame.Rect((WIDTH - BUTTON_WIDTH)//2, buttons_y_start + 2 * (BUTTON_HEIGHT + 10),
                               BUTTON_WIDTH, BUTTON_HEIGHT)
                                
    # Create the mode toggle button
    mode_button = pygame.Rect((WIDTH - BUTTON_WIDTH)//2, buttons_y_start + 3 * (BUTTON_HEIGHT + 10),
                              BUTTON_WIDTH, BUTTON_HEIGHT)

    blank_text = font.render("********", True, DEAD_COLOR, (0,0,0,0))

    if running:
        game_button_name = "Pause"
        draw_text = blank_text
        reset_text = blank_text
        tribe_text = blank_text
        mode_text = blank_text
        color = (0, 0, 0)
    else:
        if draw:
            draw_title = "Draw"
        else:
            draw_title = "Erase"
        game_button_name = " Start "
        # Draw the text on the reset button
        reset_text = font.render("Reset", True, (255,255,255), (0,0,0,0))
        draw_text = font.render(draw_title, True, (255,255,255), (0,0,0,0))
        tribe_text = font.render(f"Tribe: {current_tribe}", True, (255,255,255), (0,0,0,0))
        mode_text = font.render(f"Mode: {'Tribal' if tribal_mode else 'Standard'}", True, (255,255,255), (0,0,0,0))
        color = (255, 0, 0)

    screen.blit(reset_text, (reset_button.x + (reset_button.width - reset_text.get_width()) \
                 // 2, reset_button.y + (reset_button.height - reset_text.get_height()) // 2))
    pygame.draw.rect(screen, color, reset_button, 2)

    screen.blit(draw_text, (draw_button.x + (draw_button.width - draw_text.get_width()) \
                 // 2, draw_button.y + (draw_button.height - draw_text.get_height()) // 2))
    pygame.draw.rect(screen, color, draw_button, 2)
    
    # Draw the tribe button
    screen.blit(tribe_text, (tribe_button.x + (tribe_button.width - tribe_text.get_width()) \
                // 2, tribe_button.y + (tribe_button.height - tribe_text.get_height()) // 2))
    # Draw a colored border using the tribe's color
    pygame.draw.rect(screen, TRIBE_COLORS[current_tribe], tribe_button, 2)
    
    # Draw the mode toggle button
    screen.blit(mode_text, (mode_button.x + (mode_button.width - mode_text.get_width()) \
                // 2, mode_button.y + (mode_button.height - mode_text.get_height()) // 2))
    pygame.draw.rect(screen, color, mode_button, 2)

    # Create the start/pause game button -- this is button is always visible
    start_game_button = pygame.Rect((WIDTH - BUTTON_WIDTH)//2, buttons_y_start + 4 * (BUTTON_HEIGHT + 10), \
                            BUTTON_WIDTH, BUTTON_HEIGHT)

    start_game_text = font.render(game_button_name, True, (255,255,255), (0,0,0,0))
    # draw the blank surface over the previous text
    screen.blit(start_game_text, (start_game_button.x + \
                (start_game_button.width - start_game_text.get_width()) // 2, \
                start_game_button.y + (start_game_button.height - \
                start_game_text.get_height()) // 2))
    pygame.draw.rect(screen, (255, 0, 0), start_game_button, 2)

    return start_game_button, reset_button, draw_button, tribe_button, mode_button

def main():
    """ Main function"""

    # Initialize pygame
    pygame.init()

    # Create a blank board
    game_board = np.zeros((80, 80), dtype=int)
    clock = pygame.time.Clock()
    f_p_s = 60
    mouse_down = False
    draw = True
    running = False
    current_tribe = 1  # Default tribe for drawing
    tribal_mode = True  # Default to tribal mode

    # Set window size and title
    game_screen_size = (WIDTH, HEIGHT)
    game_screen = pygame.display.set_mode(game_screen_size)
    pygame.display.set_caption("Game of Life - Tribal Edition")

    # Handle touch events for mobile devices
    has_touchscreen = pygame.display.get_active() and hasattr(pygame, 'FINGERDOWN')

    while True:
        previous_board = np.copy(game_board)
        start_game_button, reset_button, draw_button, tribe_button, mode_button = draw_buttons(
            game_screen, running, draw, current_tribe, tribal_mode)

        # Check for mouse/touch events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            # Handle touch events for mobile
            elif has_touchscreen and event.type == pygame.FINGERDOWN:
                # Convert touch coordinates to screen coordinates
                x = event.x * WIDTH
                y = event.y * HEIGHT
                pos = (x, y)
                
                if running:
                    if start_game_button.collidepoint(pos):
                        running = not running
                else:
                    if start_game_button.collidepoint(pos):
                        running = not running
                    elif reset_button.collidepoint(pos):
                        # reset the board to blank
                        game_board = np.zeros((80, 80), dtype=int)
                    elif draw_button.collidepoint(pos):
                        draw = not draw
                    elif tribe_button.collidepoint(pos):
                        # Cycle through tribes
                        current_tribe = (current_tribe % MAX_TRIBES) + 1
                    elif mode_button.collidepoint(pos):
                        # Toggle between standard and tribal mode
                        tribal_mode = not tribal_mode
                    else:
                        # Place a cell at touch position
                        board_x = int((x - BOARD_X_OFFSET) // CELL_SIZE)
                        board_y = int((y - BOARD_Y_OFFSET) // CELL_SIZE)
                        if 0 <= board_x < game_board.shape[0] and 0 <= board_y < game_board.shape[1]:
                            game_board[board_x, board_y] = current_tribe if draw else 0
                
            # Regular mouse events
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if running:
                    if start_game_button.collidepoint(event.pos):
                        running = not running
                else:
                    if start_game_button.collidepoint(event.pos):
                        running = not running
                    elif reset_button.collidepoint(event.pos):
                        # reset the board to blank
                        game_board = np.zeros((80, 80), dtype=int)
                    elif draw_button.collidepoint(event.pos):
                        draw = not draw
                    elif tribe_button.collidepoint(event.pos):
                        # Cycle through tribes
                        current_tribe = (current_tribe % MAX_TRIBES) + 1
                    elif mode_button.collidepoint(event.pos):
                        # Toggle between standard and tribal mode
                        tribal_mode = not tribal_mode
                    else:
                        mouse_down = True
            elif event.type == pygame.MOUSEBUTTONUP:
                mouse_down = False
                
        if running:
            # Update the board with tribal dynamics
            game_board = game_of_life(game_board, tribal_mode)
            
        if mouse_down:
            # draw/erase a cell
            mouse_x, mouse_y = pygame.mouse.get_pos()
            board_x = (mouse_x - BOARD_X_OFFSET) // CELL_SIZE
            board_y = (mouse_y - BOARD_Y_OFFSET) // CELL_SIZE
            if 0 <= board_x < game_board.shape[0] and 0 <= board_y < game_board.shape[1]:
                game_board[board_x, board_y] = current_tribe if draw else 0

        # Draw the board
        draw_board(game_screen, game_board, previous_board)

        pygame.display.flip()
        clock.tick(f_p_s)

if __name__ == "__main__":
    main()
