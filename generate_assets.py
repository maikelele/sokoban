import pygame
import os

def create_asset(size, color, filename):
    surface = pygame.Surface((size, size))
    surface.fill(color)
    pygame.image.save(surface, filename)

def main():
    # Initialize Pygame
    pygame.init()
    
    # Create themes directory if it doesn't exist
    os.makedirs("themes/default", exist_ok=True)
    
    # Generate basic assets
    size = 32
    assets = {
        "wall.png": (100, 100, 100),      # Gray
        "box.png": (139, 69, 19),         # Brown
        "box_on_target.png": (0, 255, 0), # Green
        "floor.png": (255, 255, 255),     # White
        "target.png": (255, 0, 0),        # Red
        "player.png": (0, 0, 255)         # Blue
    }
    
    for filename, color in assets.items():
        create_asset(size, color, f"themes/default/{filename}")
    
    pygame.quit()

if __name__ == "__main__":
    main() 