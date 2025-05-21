# Game of Life with Tribal Dynamics

This repository contains two implementations of Conway's Game of Life with tribal dynamics:

1. A Python/Pygame implementation
2. A native iOS SwiftUI app designed for iPhone 15 Pro

Both versions feature tribal dynamics where different colored "tribes" of cells compete for territory using Conway's Game of Life rules.

## Tribal Dynamics Rules

In this implementation of Conway's Game of Life, cells belong to different "tribes" (represented by different colors):

- Cells follow the standard Game of Life rules for survival and death:
  - A live cell with fewer than 2 or more than 3 live neighboring cells dies
  - A live cell with 2 or 3 live neighboring cells survives
  - A dead cell with exactly 3 live neighboring cells becomes alive

- For tribal dynamics:
  - When a new cell is born, it takes on the tribe of the majority of its 3 live neighbors
  - If there's a tie between tribes, a random tribe is chosen
  - Cells maintain their tribal identity until they die

## Python Version

### Requirements
- Python 3.x
- Pygame library

### Running the Game
Run the game using:
```
python life.py
```

### Controls
- Click on cells to place/remove them when the game is paused
- Use the "Start" button to begin/pause the simulation
- Use the "Reset" button to clear the board
- Use the "Draw/Erase" button to toggle between drawing and erasing cells
- Select a tribe button to choose which tribe to draw

### Features
- Adapted for iPhone 15 Pro portrait aspect ratio (2.16:1)
- Supports multiple tribes with different colors
- Interactive UI for creating and controlling the simulation

## iOS Version

The iOS app is a native SwiftUI implementation designed specifically for iPhone 15 Pro.

### Requirements
- Xcode 12 or later
- iOS 14.0 or later
- iPhone (optimized for iPhone 15 Pro)

### Building and Running
1. Open the IOSGameOfLife.xcodeproj file in Xcode
2. Select your target device (iPhone 15 Pro recommended)
3. Build and run the app

### Features
- Designed for iPhone 15 Pro's portrait mode and screen dimensions
- Touch interface for creating and editing cells
- Smooth animations and performance optimization
- Support for tribal dynamics with multiple colored tribes
- Interface optimized for one-handed use on mobile
