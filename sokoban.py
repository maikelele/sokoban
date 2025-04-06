import pygame
import time
import sys
import os
from environment import Environment
from level import Level

# Global variables
myEnvironment = None
myLevel = None
theme = "default"  # Default theme
level_set = "original"
current_level = 1
target_found = False

def drawLevel(matrix_to_draw):
    global myEnvironment, myLevel
    
    # Load images for different level elements
    base_path = myEnvironment.getPath()
    wall = pygame.image.load(f"{base_path}/themes/{theme}/images/wall.png").convert()
    box = pygame.image.load(f"{base_path}/themes/{theme}/images/box.png").convert()
    box_on_target = pygame.image.load(f"{base_path}/themes/{theme}/images/box_on_target.png").convert()
    floor = pygame.image.load(f"{base_path}/themes/{theme}/images/floor.png").convert()
    target = pygame.image.load(f"{base_path}/themes/{theme}/images/target.png").convert()
    player = pygame.image.load(f"{base_path}/themes/{theme}/images/player.png").convert()
    
    # Get level size and screen size
    level_width = len(matrix_to_draw[0])
    level_height = len(matrix_to_draw)
    screen_width, screen_height = myEnvironment.size
    
    # Calculate scaling if needed
    box_size = wall.get_width()
    scale = min(screen_width / (level_width * box_size),
                screen_height / (level_height * box_size))
    
    if scale < 1:
        wall = pygame.transform.scale(wall, (int(box_size * scale), int(box_size * scale)))
        box = pygame.transform.scale(box, (int(box_size * scale), int(box_size * scale)))
        box_on_target = pygame.transform.scale(box_on_target, (int(box_size * scale), int(box_size * scale)))
        floor = pygame.transform.scale(floor, (int(box_size * scale), int(box_size * scale)))
        target = pygame.transform.scale(target, (int(box_size * scale), int(box_size * scale)))
        player = pygame.transform.scale(player, (int(box_size * scale), int(box_size * scale)))
        box_size = int(box_size * scale)
    
    # Create mapping of level elements to images
    images = {
        '#': wall,
        ' ': floor,
        '$': box,
        '.': target,
        '@': player,
        '*': box_on_target
    }
    
    # Draw the level
    for y, row in enumerate(matrix_to_draw):
        for x, cell in enumerate(row):
            pos_x = x * box_size
            pos_y = y * box_size
            myEnvironment.screen.blit(images[cell], (pos_x, pos_y))
    
    pygame.display.update()

def movePlayer(direction, myLevel):
    global target_found
    
    # Get current matrix and add to history
    matrix = myLevel.getMatrix()
    myLevel.addToHistory(matrix)
    
    # Get player position
    player_pos = myLevel.getPlayerPosition()
    if not player_pos:
        return
    
    x, y = player_pos
    new_x, new_y = x, y
    
    # Calculate new position based on direction
    if direction == "L":
        new_x -= 1
    elif direction == "R":
        new_x += 1
    elif direction == "U":
        new_y -= 1
    elif direction == "D":
        new_y += 1
    
    # Check if the new position is within bounds
    if new_y < 0 or new_y >= len(matrix) or new_x < 0 or new_x >= len(matrix[0]):
        return
    
    # Check what's in the new position
    target_cell = matrix[new_y][new_x]
    
    # Handle empty space
    if target_cell == " ":
        matrix[y][x] = "." if target_found else " "
        matrix[new_y][new_x] = "@"
        target_found = False
    
    # Handle box
    elif target_cell in ["$", "*"]:
        # Calculate the position behind the box
        box_x = new_x + (new_x - x)
        box_y = new_y + (new_y - y)
        
        # Check if the position behind the box is within bounds
        if box_y < 0 or box_y >= len(matrix) or box_x < 0 or box_x >= len(matrix[0]):
            return
            
        box_target = matrix[box_y][box_x]
        
        # Check if there's another box behind this one
        if box_target in ["$", "*"]:
            return
            
        # Check if there's a wall behind the box
        if box_target == "#":
            return
        
        # Move the box
        if box_target == " ":
            # Move box to empty space
            matrix[box_y][box_x] = "$"
            matrix[new_y][new_x] = "@"
            matrix[y][x] = "." if target_found else " "
            target_found = False
        elif box_target == ".":
            # Move box to target
            matrix[box_y][box_x] = "*"
            matrix[new_y][new_x] = "@"
            matrix[y][x] = "." if target_found else " "
            target_found = False
    
    # Handle target
    elif target_cell == ".":
        matrix[y][x] = "." if target_found else " "
        matrix[new_y][new_x] = "@"
        target_found = True
    
    # Handle wall
    elif target_cell == "#":
        return
    
    # Update display
    drawLevel(matrix)
    
    # Print remaining boxes
    print("Boxes remaining: " + str(len(myLevel.getBoxes())))
    
    # Check if level is complete
    if len(myLevel.getBoxes()) == 0:
        # Fill screen with black
        myEnvironment.screen.fill((0, 0, 0))
        pygame.display.update()
        
        # Print level completed message
        print("Level Completed")
        
        # Increment level counter
        global current_level
        current_level += 1
        
        # Initialize next level
        initLevel(level_set, current_level)

def initLevel(level_set, level_num):
    global myLevel, target_found
    
    # Create a new instance of Level
    myLevel = Level(level_set, level_num)
    
    # Draw the initial level state
    drawLevel(myLevel.getMatrix())
    
    # Reset target_found flag
    target_found = False

def getAvailableThemes():
    """Get a list of available themes from the themes directory."""
    base_path = myEnvironment.getPath()
    themes_dir = os.path.join(base_path, 'themes')
    
    if not os.path.exists(themes_dir):
        return ["default"]
    
    themes = []
    for theme_name in os.listdir(themes_dir):
        theme_path = os.path.join(themes_dir, theme_name)
        if os.path.isdir(theme_path) and os.path.exists(os.path.join(theme_path, 'images')):
            themes.append(theme_name)
    
    return themes if themes else ["default"]

def main():
    global myEnvironment
    
    # Initialize environment
    myEnvironment = Environment()
    
    # Initialize first level
    initLevel(level_set, current_level)
    
    # Main game loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    movePlayer("L", myLevel)
                elif event.key == pygame.K_RIGHT:
                    movePlayer("R", myLevel)
                elif event.key == pygame.K_UP:
                    movePlayer("U", myLevel)
                elif event.key == pygame.K_DOWN:
                    movePlayer("D", myLevel)
                elif event.key == pygame.K_u:
                    # Undo last move
                    last_matrix = myLevel.getLastMatrix()
                    drawLevel(last_matrix)
                elif event.key == pygame.K_r:
                    initLevel(level_set, current_level)
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
        
        time.sleep(0.1)  # Basic frame rate control

if __name__ == "__main__":
    main() 