import os
import platform
import pygame
import time

class Environment:
    screen = None
    size = None

    def __init__(self):
        if platform.system() == "Windows" or self.getUserInterface() == "graphics":
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