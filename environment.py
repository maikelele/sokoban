import os
import platform
import pygame
import time

class Environment:
    screen = None
    size = None

    def __init__(self):
        # Check if we're on Linux and using framebuffer
        if platform.system() == "Linux" and self.getUserInterface() == "framebuffer":
            # Try different framebuffer drivers
            drivers = ['fbcon', 'directfb', 'svgalib']
            initialized = False
            
            for driver in drivers:
                try:
                    # Set the SDL video driver environment variable
                    os.putenv('SDL_VIDEODRIVER', driver)
                    
                    # Initialize pygame display
                    pygame.display.init()
                    
                    # If we get here, initialization was successful
                    initialized = True
                    print(f"Successfully initialized with {driver} driver")
                    break
                except pygame.error as e:
                    print(f"Failed to initialize with {driver} driver: {e}")
            
            if not initialized:
                raise Exception('No suitable video driver found!')
            
            # Get the framebuffer size
            self.size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
            
            # Set fullscreen mode
            self.screen = pygame.display.set_mode(self.size, pygame.FULLSCREEN)
            
            # Clear screen, initialize fonts, and hide cursor
            self.screen.fill((0, 0, 0))
            pygame.font.init()
            pygame.mouse.set_visible(False)
            
            # Update the display
            pygame.display.update()
            
        # Standard initialization for Windows or X Window
        elif platform.system() == "Windows" or self.getUserInterface() == "graphics":
            pygame.display.init()
            pygame.display.set_caption("pySokoban")
            self.size = (800, 600)
            self.screen = pygame.display.set_mode(self.size)

    def getOS(self):
        return platform.system()

    def getUserInterface(self):
        if "DISPLAY" in os.environ:
            return "graphics"
        return "framebuffer"

    def getPath(self):
        return os.path.dirname(os.path.abspath(__file__)) 