import os
import platform
import pygame
import time

class Environment:
    screen = None
    size = None

    
    def __init__(self):

        pygame.display.init()
        pygame.display.set_caption("Sokoban")
        self.size = (800,600)
        self.screen = pygame.display.set_mode(self.size)
        self.screen.fill((0, 0, 0))        
        pygame.font.init()
        pygame.mouse.set_visible(False)
        pygame.display.update()

    def getOS(self):
        return platform.system()

    def getUserInterface(self):
        if os.getenv("DISPLAY"):
            return "graphics"
        else:
            return "framebuffer"
        
    def getPath(self):
        return os.path.dirname(os.path.abspath(__file__))