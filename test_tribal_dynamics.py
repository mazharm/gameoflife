#!/usr/bin/env python3
"""
Test script for the Game of Life tribal dynamics implementation.
This script tests the core game logic without the GUI.
"""
import numpy as np
from life import game_of_life

def print_board(board):
    """Print a visual representation of the board."""
    for row in range(board.shape[1]):
        for col in range(board.shape[0]):
            if board[col, row] == 0:
                print(' ', end='')
            else:
                print(board[col, row], end='')
        print()
    print()

def test_standard_mode():
    """Test the standard Game of Life rules."""
    print("Testing standard mode...")
    
    # Create a board with a simple pattern (glider)
    board = np.zeros((10, 10), dtype=int)
    board[1, 2] = 1
    board[2, 3] = 1
    board[3, 1] = 1
    board[3, 2] = 1
    board[3, 3] = 1
    
    print("Initial board:")
    print_board(board)
    
    # Run 4 generations
    for i in range(4):
        board = game_of_life(board, tribal_mode=False)
        print(f"Generation {i+1}:")
        print_board(board)
    
    print("Standard mode test completed.")
    print("-" * 40)

def test_tribal_dynamics():
    """Test the tribal dynamics feature."""
    print("Testing tribal dynamics...")
    
    # Create a board with competing tribes (tribe 1 vs tribe 2)
    board = np.zeros((10, 10), dtype=int)
    
    # Tribe 1 pattern (left side)
    board[2, 4] = 1
    board[3, 4] = 1
    board[4, 4] = 1
    
    # Tribe 2 pattern (right side)
    board[5, 5] = 2
    board[6, 5] = 2
    board[7, 5] = 2
    
    print("Initial board with two tribes:")
    print_board(board)
    
    # Run 6 generations
    for i in range(6):
        board = game_of_life(board, tribal_mode=True)
        print(f"Generation {i+1}:")
        print_board(board)
    
    print("Tribal dynamics test completed.")
    print("-" * 40)

def test_tribe_competition():
    """Test the competition between multiple tribes."""
    print("Testing multi-tribe competition...")
    
    # Create a board with three competing tribes in close proximity
    board = np.zeros((15, 15), dtype=int)
    
    # Tribe 1 - Glider
    board[3, 3] = 1
    board[4, 4] = 1
    board[5, 2] = 1
    board[5, 3] = 1
    board[5, 4] = 1
    
    # Tribe 2 - Blinker
    board[8, 7] = 2
    board[8, 8] = 2
    board[8, 9] = 2
    
    # Tribe 3 - Block
    board[12, 12] = 3
    board[12, 13] = 3
    board[13, 12] = 3
    board[13, 13] = 3
    
    print("Initial board with three tribes:")
    print_board(board)
    
    # Run 10 generations
    for i in range(10):
        board = game_of_life(board, tribal_mode=True)
        print(f"Generation {i+1}:")
        print_board(board)
        
        # Count cells per tribe
        unique, counts = np.unique(board, return_counts=True)
        tribe_counts = dict(zip(unique, counts))
        print("Tribe population:", end=" ")
        for tribe, count in tribe_counts.items():
            if tribe > 0:  # Only show living tribes
                print(f"Tribe {tribe}: {count}", end=", ")
        print("\n")
    
    print("Multi-tribe competition test completed.")
    print("-" * 40)

def test_edge_case_ties():
    """Test edge case where there are ties between tribes."""
    print("Testing tie-breaking in tribal dynamics...")
    
    # Create a board with an edge case where a cell has equal neighbors from different tribes
    board = np.zeros((7, 7), dtype=int)
    
    # Setup where a dead cell has exactly 3 neighbors of different tribes
    # Tribe 1
    board[2, 3] = 1
    # Tribe 2
    board[3, 2] = 2
    # Tribe 3
    board[4, 3] = 3
    
    print("Initial board with potential tie:")
    print_board(board)
    
    # Run a few generations
    for i in range(3):
        board = game_of_life(board, tribal_mode=True)
        print(f"Generation {i+1}:")
        print_board(board)
    
    print("Tie-breaking test completed.")
    print("-" * 40)

if __name__ == "__main__":
    test_standard_mode()
    test_tribal_dynamics()
    test_tribe_competition()
    test_edge_case_ties()
    print("All tests completed successfully.")