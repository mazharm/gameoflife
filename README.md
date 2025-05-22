# Game of Life - Tribal Edition

A Python implementation of Conway's Game of Life with tribal dynamics.

## Features

### Standard Game of Life
- Classic Conway's Game of Life rules
- Interactive board editing (draw/erase cells)
- Support for iPhone 15 Pro portrait mode (2.16:1 aspect ratio)
- Pause and resume simulation
- Reset board functionality

### Tribal Dynamics
- Multiple tribes competing for dominance
- Each tribe has a unique color
- Tribal competition based on neighborhood dominance
- Toggle between standard and tribal modes

## Controls
- Click or tap on cells to draw or erase
- Use the buttons to control game functions:
  - Draw/Erase: Toggle between drawing and erasing cells
  - Reset: Clear the board
  - Start/Pause: Start or pause the simulation
  - Tribe: Cycle through available tribes (1-9)
  - Mode: Switch between Standard and Tribal modes

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

## Running on iPhone (including carrier-locked devices)

### Method 1: Web Browser (Recommended for carrier-locked iPhones)
This method works on all iPhones regardless of carrier lock status:

1. Visit the Game of Life web version at: `https://yourusername.github.io/gameoflife/`
2. For the best experience:
   - Use Safari browser in portrait orientation
   - Add to home screen: tap the share button (box with arrow) → "Add to Home Screen"
   - Launch from the home screen icon for a fullscreen experience

### Method 2: Using Pythonista (for non-carrier restricted iPhones)
If your iPhone allows installation of Pythonista:

1. Purchase and install [Pythonista](https://apps.apple.com/us/app/pythonista-3/id1085978097) from the App Store
2. Import the `life.py` file via:
   - iCloud Drive
   - Email attachment
   - GitHub download
3. Install the pygame module in Pythonista using StaSh
4. Run the script from within Pythonista

### Note for Carrier-Locked iPhones
Carrier-locked iPhones have restrictions that may prevent installing certain apps outside the App Store. The web browser method (Method 1) works regardless of these restrictions since it runs in Safari, which comes pre-installed on all iPhones.
