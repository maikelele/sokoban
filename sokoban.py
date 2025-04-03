import pygame
import time
import sys
from environment import Environment
from level import Level

# Global variables
myEnvironment = None
myLevel = None
theme = "default"
level_set = "set1"
current_level = 1
target_found = False

def drawLevel(matrix_to_draw):
    global myEnvironment, myLevel
    
    # Load images for different level elements
    base_path = myEnvironment.getPath()
    wall = pygame.image.load(f"{base_path}/themes/{theme}/wall.png")
    box = pygame.image.load(f"{base_path}/themes/{theme}/box.png")
    box_on_target = pygame.image.load(f"{base_path}/themes/{theme}/box_on_target.png")
    floor = pygame.image.load(f"{base_path}/themes/{theme}/floor.png")
    target = pygame.image.load(f"{base_path}/themes/{theme}/target.png")
    player = pygame.image.load(f"{base_path}/themes/{theme}/player.png")
    
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

def initLevel(level_set, level_num):
    global myLevel
    myLevel = Level(level_set, level_num)
    drawLevel(myLevel.matrix)

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
        
        time.sleep(0.1)  # Basic frame rate control

if __name__ == "__main__":
    main() 