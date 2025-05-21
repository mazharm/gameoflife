#!/usr/bin/env python3
"""
Visual test script for the Game of Life tribal dynamics implementation.
This script creates a video file showing the tribal dynamics in action.
"""
import numpy as np
import pygame
import cv2
from life import game_of_life, TRIBE_COLORS

# Configuration
WIDTH = 400
HEIGHT = 400
CELL_SIZE = 10
GRID_WIDTH = WIDTH // CELL_SIZE
GRID_HEIGHT = HEIGHT // CELL_SIZE
FPS = 10
FRAMES = 300
OUTPUT_FILE = "tribal_dynamics_demo.mp4"

def create_interesting_pattern(board):
    """Create an interesting initial pattern with multiple tribes."""
    # Clear the board
    board.fill(0)
    
    # Tribe 1 - Glider
    board[5, 5] = 1
    board[6, 6] = 1
    board[7, 4] = 1
    board[7, 5] = 1
    board[7, 6] = 1
    
    # Tribe 2 - Blinker
    board[15, 15] = 2
    board[15, 16] = 2
    board[15, 17] = 2
    
    # Tribe 3 - Block
    board[10, 25] = 3
    board[10, 26] = 3
    board[11, 25] = 3
    board[11, 26] = 3
    
    # Tribe 4 - Glider
    board[30, 5] = 4
    board[31, 6] = 4
    board[32, 4] = 4
    board[32, 5] = 4
    board[32, 6] = 4
    
    # Tribe 5 - Random pattern
    for _ in range(50):
        x = np.random.randint(0, GRID_WIDTH)
        y = np.random.randint(0, GRID_HEIGHT)
        tribe = np.random.randint(1, 6)
        board[x, y] = tribe
    
    return board

def render_board(board):
    """Render the board to a pygame surface and return it."""
    surface = pygame.Surface((WIDTH, HEIGHT))
    surface.fill((0, 0, 0))  # Fill with black
    
    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT):
            tribe_id = board[x, y]
            if tribe_id > 0:
                color = TRIBE_COLORS[min(tribe_id, len(TRIBE_COLORS) - 1)]
                rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(surface, color, rect)
    
    return surface

def surface_to_opencv(surface):
    """Convert a pygame surface to an OpenCV image."""
    # Get the array buffer
    img_str = pygame.image.tostring(surface, 'RGB')
    # Create OpenCV image from the string buffer
    img = np.frombuffer(img_str, np.uint8).reshape(surface.get_height(), surface.get_width(), 3)
    # Convert RGB to BGR for OpenCV
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    return img

def main():
    """Main function to create the demo video."""
    # Initialize pygame
    pygame.init()
    
    # Create board
    board = np.zeros((GRID_WIDTH, GRID_HEIGHT), dtype=int)
    board = create_interesting_pattern(board)
    
    # Set up video writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video = cv2.VideoWriter(OUTPUT_FILE, fourcc, FPS, (WIDTH, HEIGHT))
    
    print(f"Creating {FRAMES} frames of tribal dynamics simulation...")
    
    # Generate frames
    for i in range(FRAMES):
        # Render current state
        surface = render_board(board)
        
        # Add frame number
        font = pygame.font.Font(None, 24)
        text = font.render(f"Frame: {i}", True, (255, 255, 255))
        surface.blit(text, (10, 10))
        
        # Add to video
        frame = surface_to_opencv(surface)
        video.write(frame)
        
        # Update board for next frame
        board = game_of_life(board, tribal_mode=True)
        
        # Print progress
        if i % 10 == 0:
            print(f"Progress: {i}/{FRAMES} frames")
    
    # Release video
    video.release()
    pygame.quit()
    
    print(f"Video saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()