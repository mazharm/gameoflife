import SwiftUI

struct GridView: View {
    @ObservedObject var model: GameOfLifeModel
    
    var body: some View {
        GeometryReader { geometry in
            let cellSize = min(
                geometry.size.width / CGFloat(model.width),
                geometry.size.height / CGFloat(model.height)
            )
            
            VStack(spacing: 0) {
                ForEach(0..<model.height, id: \.self) { y in
                    HStack(spacing: 0) {
                        ForEach(0..<model.width, id: \.self) { x in
                            CellView(tribe: model.board[x][y])
                                .frame(width: cellSize, height: cellSize)
                                .onTapGesture {
                                    if !model.isRunning {
                                        model.setCell(x: x, y: y, tribe: model.selectedTribe)
                                    }
                                }
                        }
                    }
                }
            }
            .gesture(
                DragGesture(minimumDistance: 0, coordinateSpace: .local)
                    .onChanged { value in
                        if model.isRunning { return }
                        
                        let x = Int(value.location.x / cellSize)
                        let y = Int(value.location.y / cellSize)
                        
                        if x >= 0 && x < model.width && y >= 0 && y < model.height {
                            model.setCell(x: x, y: y, tribe: model.selectedTribe)
                        }
                    }
            )
        }
    }
}