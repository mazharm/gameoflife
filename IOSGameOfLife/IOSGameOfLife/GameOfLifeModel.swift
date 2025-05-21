import Foundation
import SwiftUI

class GameOfLifeModel: ObservableObject {
    // Constants
    static let numTribes = 5
    
    // Colors for different tribes
    static let tribeColors: [Color] = [
        .black,         // 0: Dead cells
        .white,         // 1: White tribe
        .red,           // 2: Red tribe
        .green,         // 3: Green tribe
        .blue,          // 4: Blue tribe
        .yellow,        // 5: Yellow tribe
    ]
    
    // Board dimensions
    let width: Int
    let height: Int
    
    // Game state
    @Published var board: [[Int]]
    @Published var isRunning = false
    @Published var selectedTribe = 1
    
    // Timer for automatic updates
    private var timer: Timer?
    private let updateInterval = 0.1
    
    init(width: Int = 60, height: Int = 120) {
        self.width = width
        self.height = height
        self.board = Array(repeating: Array(repeating: 0, count: height), count: width)
    }
    
    // Reset the board to empty
    func resetBoard() {
        board = Array(repeating: Array(repeating: 0, count: height), count: width)
        objectWillChange.send()
    }
    
    // Toggle cell at given coordinates
    func toggleCell(x: Int, y: Int) {
        guard x >= 0 && x < width && y >= 0 && y < height else { return }
        
        if board[x][y] == 0 {
            // Cell is dead, make it alive with the selected tribe
            board[x][y] = selectedTribe
        } else {
            // Cell is alive, make it dead
            board[x][y] = 0
        }
        
        objectWillChange.send()
    }
    
    // Set cell to specific tribe
    func setCell(x: Int, y: Int, tribe: Int) {
        guard x >= 0 && x < width && y >= 0 && y < height else { return }
        board[x][y] = tribe
        objectWillChange.send()
    }
    
    // Start the simulation
    func startSimulation() {
        guard timer == nil else { return }
        
        isRunning = true
        timer = Timer.scheduledTimer(withTimeInterval: updateInterval, repeats: true) { [weak self] _ in
            self?.updateBoard()
        }
    }
    
    // Stop the simulation
    func stopSimulation() {
        timer?.invalidate()
        timer = nil
        isRunning = false
    }
    
    // Toggle the simulation state
    func toggleSimulation() {
        if isRunning {
            stopSimulation()
        } else {
            startSimulation()
        }
    }
    
    // Update the board based on Game of Life rules with tribal dynamics
    func updateBoard() {
        var newBoard = Array(repeating: Array(repeating: 0, count: height), count: width)
        
        for x in 0..<width {
            for y in 0..<height {
                let currentCell = board[x][y]
                var tribeCounts = Array(repeating: 0, count: GameOfLifeModel.numTribes + 1)
                
                // Count neighbors of each tribe
                for nx in max(0, x-1)...min(width-1, x+1) {
                    for ny in max(0, y-1)...min(height-1, y+1) {
                        if nx == x && ny == y { continue } // Skip the cell itself
                        
                        let neighbor = board[nx][ny]
                        tribeCounts[neighbor] += 1
                    }
                }
                
                // Total neighbors of any tribe
                let totalNeighbors = tribeCounts.enumerated().reduce(0) { $0 + ($1.0 > 0 ? $1.1 : 0) }
                
                // Apply Game of Life rules with tribal dynamics
                if currentCell > 0 {  // Cell is alive
                    // Survive with 2 or 3 neighbors, die otherwise
                    if totalNeighbors == 2 || totalNeighbors == 3 {
                        newBoard[x][y] = currentCell
                    } else {
                        newBoard[x][y] = 0 // Cell dies
                    }
                } else {  // Cell is dead
                    // Become alive with exactly 3 neighbors
                    if totalNeighbors == 3 {
                        // Determine which tribe dominates
                        let dominantTribe = tribeCounts.enumerated()
                            .filter { $0.0 > 0 } // Only consider tribes (not dead cells)
                            .max { $0.1 < $1.1 } // Find the max count
                        
                        // If there's a tie, choose randomly between the dominant tribes
                        let maxCount = dominantTribe?.1 ?? 0
                        let dominantTribes = tribeCounts.enumerated()
                            .filter { $0.0 > 0 && $0.1 == maxCount }
                            .map { $0.0 }
                        
                        if !dominantTribes.isEmpty {
                            newBoard[x][y] = dominantTribes.randomElement() ?? 1
                        }
                    }
                }
            }
        }
        
        board = newBoard
        objectWillChange.send()
    }
}