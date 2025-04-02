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