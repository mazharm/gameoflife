import pygame
import numpy as np
import sys

WIDTH = 800  # Width of the screen in pixels
HEIGHT = 600  # Height of the screen in pixels
BUTTON_WIDTH = 150  # Width of the button in pixels
BUTTON_HEIGHT = 50  # Height of the button in pixels

# Colors
ALIVE_COLOR = (255, 255, 255)
DEAD_COLOR = (0, 0, 0)
TRANSPARENT_COLOR = (0, 0, 0)

# Cell size in pixels
CELL_SIZE = 8

# Initialize pygame
pygame.init()

# Set window size and title
size = (800, 800)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Game of Life")

# Create a blank board
board = np.zeros((80, 80), dtype=bool)

# Set up font for button text
font = pygame.font.Font(None, 30)


"""
Apply the rules of the Game of Life to the board
"""
def game_of_life(board):
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

"""
Draw the board to the screen
"""
def draw_board(screen, board, previous_board):
    for x in range(board.shape[0]):
        for y in range(board.shape[1]):
            if board[x, y] != previous_board[x, y]:
                if board[x, y]:
                    color = ALIVE_COLOR
                else:
                    color = DEAD_COLOR
                rect = (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(screen, color, rect)
                pygame.display.update(rect)
    previous_board[:] = board

"""
Draw the buttons to the screen
"""
def draw_buttons(running, draw) :

    # Create the draw button -- this is only visible when the game is not running
    draw_button = pygame.Rect((WIDTH - BUTTON_WIDTH)//2, HEIGHT - 3*BUTTON_HEIGHT-20, BUTTON_WIDTH, BUTTON_HEIGHT)

    # Create the reset button -- this is only visible when the game is not running
    reset_button = pygame.Rect((WIDTH - BUTTON_WIDTH)//2, HEIGHT - 2*BUTTON_HEIGHT-10, BUTTON_WIDTH, BUTTON_HEIGHT)
 
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

    screen.blit(reset_text, (reset_button.x + (reset_button.width - reset_text.get_width()) // 2, reset_button.y + (reset_button.height - reset_text.get_height()) // 2))
    pygame.draw.rect(screen, color, reset_button, 2)

    screen.blit(draw_text, (draw_button.x + (draw_button.width - draw_text.get_width()) // 2, draw_button.y + (draw_button.height - draw_text.get_height()) // 2))
    pygame.draw.rect(screen, color, draw_button, 2)

    # Create the start/pause game button -- this is button is always visible
    start_game_button = pygame.Rect((WIDTH - BUTTON_WIDTH)//2, HEIGHT - BUTTON_HEIGHT, BUTTON_WIDTH, BUTTON_HEIGHT)

    start_game_text = font.render(game_button_name, True, (255,255,255), (0,0,0,0))
    # draw the blank surface over the previous text
    screen.blit(start_game_text, (start_game_button.x + (start_game_button.width - start_game_text.get_width()) // 2, start_game_button.y + (start_game_button.height - start_game_text.get_height()) // 2))
    pygame.draw.rect(screen, (255, 0, 0), start_game_button, 2)

    return start_game_button, reset_button, draw_button

"""
Main function
"""
def main():
    global board
    clock = pygame.time.Clock()
    FPS = 60
    mouse_down = False
    draw = True
    running = False

    while True:
        previous_board = np.copy(board)
        start_game_button, reset_button, draw_button = draw_buttons(running, draw)

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
                        board = np.zeros((80, 80), dtype=bool)
                    elif draw_button.collidepoint(event.pos):
                        draw = not draw
                    else:
                        mouse_down = True
            elif event.type == pygame.MOUSEBUTTONUP:
                mouse_down = False
            
        if running:
            # Update the board
            board = game_of_life(board)

        if mouse_down:
            # draw/erase a cell
            x, y = pygame.mouse.get_pos()
            x, y = x // CELL_SIZE, y // CELL_SIZE
            if x < board.shape[0] and y < board.shape[1]:
                board[x, y] = draw

        # Draw the board
        draw_board(screen, board, previous_board)
        
        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    main()