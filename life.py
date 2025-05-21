"""
A simple implementation of Game of Life with fluid implementation of
board setup
"""
import sys
import pygame
import numpy as np


WIDTH = 600  # Width of the screen in pixels
HEIGHT = 1296  # Height of the screen in pixels (iPhone 15 Pro portrait ratio ~2.16:1)
BUTTON_WIDTH = 150  # Width of the button in pixels
BUTTON_HEIGHT = 50  # Height of the button in pixels

# Colors
ALIVE_COLOR = (255, 255, 255)
DEAD_COLOR = (0, 0, 0)
TRANSPARENT_COLOR = (0, 0, 0)

# Cell size in pixels
CELL_SIZE = 7

# Board position offset for centering
BOARD_X_OFFSET = (WIDTH - 80 * CELL_SIZE) // 2
BOARD_Y_OFFSET = 50  # Provide some space at the top


def game_of_life(board):
    """
    Apply the rules of the Game of Life to the board
    """
    # Copy the board to a new array to avoid modifying the original
    new_board = np.copy(board)
    for i in range(1, board.shape[0]-1):
        for j in range(1, board.shape[1]-1):
            # Count the number of live neighbors
            neighbors = np.sum(board[i-1:i+2, j-1:j+2]) - board[i, j]
            # Apply the rules of the Game of Life
            if board[i, j]:
                if neighbors < 2 or neighbors > 3:
                    new_board[i, j] = False
            else:
                if neighbors == 3:
                    new_board[i, j] = True
    return new_board

def draw_board(screen, board, previous_board):
    """
    Render the board to the screen
    """
    for board_x in range(board.shape[0]):
        for board_y in range(board.shape[1]):
            if board[board_x, board_y] != previous_board[board_x, board_y]:
                if board[board_x, board_y]:
                    color = ALIVE_COLOR
                else:
                    color = DEAD_COLOR
                rect = (BOARD_X_OFFSET + board_x * CELL_SIZE, BOARD_Y_OFFSET + board_y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(screen, color, rect)
                pygame.display.update(rect)
    previous_board[:] = board

def draw_buttons(screen, running, draw) :
    """ Render the Draw/Erase, Reset and Start/Pause buttons on the screen
    """
    # Set up font for button text
    font = pygame.font.Font(None, 30)

    # Create the draw button -- this is only visible when the game is not running
    draw_button = pygame.Rect((WIDTH - BUTTON_WIDTH)//2, HEIGHT - 3*BUTTON_HEIGHT-20,\
                               BUTTON_WIDTH, BUTTON_HEIGHT)

    # Create the reset button -- this is only visible when the game is not running
    reset_button = pygame.Rect((WIDTH - BUTTON_WIDTH)//2, HEIGHT - 2*BUTTON_HEIGHT-10,\
                                BUTTON_WIDTH, BUTTON_HEIGHT)

    blank_text = font.render("********", True, DEAD_COLOR, (0,0,0,0))

    if running:
        game_button_name = "Pause"
        draw_text = blank_text
        reset_text = blank_text
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
        color = (255, 0, 0)

    screen.blit(reset_text, (reset_button.x + (reset_button.width - reset_text.get_width()) \
                 // 2, reset_button.y + (reset_button.height - reset_text.get_height()) // 2))
    pygame.draw.rect(screen, color, reset_button, 2)

    screen.blit(draw_text, (draw_button.x + (draw_button.width - draw_text.get_width()) \
                 // 2, draw_button.y + (draw_button.height - draw_text.get_height()) // 2))
    pygame.draw.rect(screen, color, draw_button, 2)

    # Create the start/pause game button -- this is button is always visible
    start_game_button = pygame.Rect((WIDTH - BUTTON_WIDTH)//2, HEIGHT - BUTTON_HEIGHT, \
                            BUTTON_WIDTH, BUTTON_HEIGHT)

    start_game_text = font.render(game_button_name, True, (255,255,255), (0,0,0,0))
    # draw the blank surface over the previous text
    screen.blit(start_game_text, (start_game_button.x + \
                (start_game_button.width - start_game_text.get_width()) // 2, \
                start_game_button.y + (start_game_button.height - \
                start_game_text.get_height()) // 2))
    pygame.draw.rect(screen, (255, 0, 0), start_game_button, 2)

    return start_game_button, reset_button, draw_button

def main():
    """ Main function"""

    # Initialize pygame
    pygame.init()

    # Create a blank board
    game_board = np.zeros((80, 80), dtype=bool)
    clock = pygame.time.Clock()
    f_p_s = 60
    mouse_down = False
    draw = True
    running = False

    # Set window size and title
    game_screen_size = (WIDTH, HEIGHT)
    game_screen = pygame.display.set_mode(game_screen_size)
    pygame.display.set_caption("Game of Life - iPhone 15 Pro")

    while True:
        previous_board = np.copy(game_board)
        start_game_button, reset_button, draw_button = draw_buttons(game_screen, running, draw)

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
                        game_board = np.zeros((80, 80), dtype=bool)
                    elif draw_button.collidepoint(event.pos):
                        draw = not draw
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
            board_x = (mouse_x - BOARD_X_OFFSET) // CELL_SIZE
            board_y = (mouse_y - BOARD_Y_OFFSET) // CELL_SIZE
            if 0 <= board_x < game_board.shape[0] and 0 <= board_y < game_board.shape[1]:
                game_board[board_x, board_y] = draw

        # Draw the board
        draw_board(game_screen, game_board, previous_board)

        pygame.display.flip()
        clock.tick(f_p_s)


if __name__ == "__main__":
    main()
