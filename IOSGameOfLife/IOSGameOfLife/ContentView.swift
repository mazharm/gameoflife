import SwiftUI

struct ContentView: View {
    @StateObject private var model = GameOfLifeModel()
    
    var body: some View {
        VStack {
            Text("Game of Life - Tribal Edition")
                .font(.headline)
                .padding()
            
            // Game grid
            GridView(model: model)
                .aspectRatio(CGFloat(model.width) / CGFloat(model.height), contentMode: .fit)
                .border(Color.gray, width: 1)
                .padding(.horizontal)
            
            // Tribe selection
            ScrollView(.horizontal, showsIndicators: false) {
                HStack(spacing: 10) {
                    ForEach(1...GameOfLifeModel.numTribes, id: \.self) { tribe in
                        Button(action: {
                            model.selectedTribe = tribe
                        }) {
                            Text("Tribe \(tribe)")
                                .padding(8)
                                .background(GameOfLifeModel.tribeColors[tribe])
                                .foregroundColor(tribe == 1 ? .black : .white)
                                .cornerRadius(8)
                                .overlay(
                                    RoundedRectangle(cornerRadius: 8)
                                        .stroke(model.selectedTribe == tribe ? Color.yellow : Color.clear, lineWidth: 2)
                                )
                        }
                    }
                }
                .padding()
            }
            
            // Control buttons
            HStack(spacing: 20) {
                Button(action: {
                    model.toggleSimulation()
                }) {
                    Text(model.isRunning ? "Pause" : "Start")
                        .frame(width: 80)
                        .padding()
                        .background(Color.blue)
                        .foregroundColor(.white)
                        .cornerRadius(8)
                }
                
                Button(action: {
                    model.resetBoard()
                }) {
                    Text("Reset")
                        .frame(width: 80)
                        .padding()
                        .background(Color.red)
                        .foregroundColor(.white)
                        .cornerRadius(8)
                }
            }
            .padding()
            
            Text("Tap or drag on the grid to create cells when paused")
                .font(.caption)
                .padding(.bottom)
        }
        .frame(maxWidth: .infinity, maxHeight: .infinity)
        .background(Color.black.opacity(0.1))
        .edgesIgnoringSafeArea(.all)
    }
}