import os

class Level:
    def __init__(self, set, level_num):
        # Clear any existing data
        del self.matrix[:]
        del self.matrix_history[:]
        
        # Initialize empty lists for matrix and history
        self.matrix = []
        self.matrix_history = []
        
        # Construct the path to the level file
        base_path = os.path.dirname(os.path.abspath(__file__))
        level_path = os.path.join(base_path, 'levels', set, f'level{level_num}')
        
        # Read and parse the level file
        with open(level_path, 'r') as f:
            for row in f.read().splitlines():
                self.matrix.append(list(row))
    
    def __del__(self):
        pass  # Basic destructor, no specific cleanup needed yet
    
    def getMatrix(self):
        return self.matrix
    
    def addToHistory(self, matrix):
        # Create a deep copy of the matrix to store in history
        self.matrix_history.append([row[:] for row in matrix])
    
    def getLastMatrix(self):
        # Check if there are any states in history
        if len(self.matrix_history) > 0:
            # Get and remove the last state from history
            lastMatrix = self.matrix_history.pop()
            # Update the current matrix with the last state
            self.matrix = lastMatrix
            return lastMatrix
        # If no history, return current matrix
        return self.matrix
    
    def getPlayerPosition(self):
        for y, row in enumerate(self.matrix):
            for x, cell in enumerate(row):
                if cell == '@':
                    return [x, y]
        return None
    
    def getBoxes(self):
        boxes = []
        for y, row in enumerate(self.matrix):
            for x, cell in enumerate(row):
                if cell == '$':
                    boxes.append([x, y])
        return boxes 