from environment import Environment

def main():
    env = Environment()
    
    # Main game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        pygame.display.flip()
    
    pygame.quit()

if __name__ == "__main__":
    main() 