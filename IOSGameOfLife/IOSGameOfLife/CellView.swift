import SwiftUI

struct CellView: View {
    var tribe: Int
    
    var body: some View {
        Rectangle()
            .fill(GameOfLifeModel.tribeColors[tribe])
            .border(Color.gray.opacity(0.2), width: 0.5)
    }
}