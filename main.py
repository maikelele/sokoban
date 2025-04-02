import pygame
from environment import Environment
from level import Level

def main():
    env = Environment()
    
    # Load the first level
    level = Level('set1', 1)
    
    # Main game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Clear the screen
        env.screen.fill((255, 255, 255))
        
        # TODO: Draw the level (will be implemented in future commits)
        
        pygame.display.flip()
    
    pygame.quit()

if __name__ == "__main__":
    main() 