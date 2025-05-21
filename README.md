# Game of Life - Tribal Edition

A Python implementation of Conway's Game of Life with tribal dynamics.

## Features

### Standard Game of Life
- Classic Conway's Game of Life rules
- Draw/erase cells with mouse
- Start/pause simulation
- Reset board

### Tribal Dynamics
- Multiple tribes competing for dominance
- Each tribe has a unique color
- Tribal competition based on neighborhood dominance
- Toggle between standard and tribal modes

## How to Play

1. **Drawing Cells**: Click and drag to draw cells on the grid.
2. **Selecting Tribes**: Click the "Tribe" button to cycle through available tribes.
3. **Changing Modes**: Click the "Mode" button to toggle between Standard and Tribal modes.
4. **Starting Simulation**: Click "Start" to run the simulation.
5. **Pausing Simulation**: Click "Pause" to pause the simulation.
6. **Resetting Board**: Click "Reset" to clear the board.

## Rules

### Standard Mode
- Any live cell with fewer than 2 live neighbors dies (underpopulation)
- Any live cell with 2 or 3 live neighbors lives on
- Any live cell with more than 3 live neighbors dies (overpopulation)
- Any dead cell with exactly 3 live neighbors becomes a live cell (reproduction)

### Tribal Mode
- Each tribe follows the standard Game of Life rules
- When a new cell is born, it adopts the tribe of the dominant neighboring tribe
- Tribes compete for dominance based on numbers and positioning

## Requirements
- Python 3.x
- Pygame library

## How to Run
```
python life.py
```
