import pygame, sys
from config import screen , clock
from scences import MenuScene, SceneManager

#main        
def main():
    manager = SceneManager()
    manager.go_to(MenuScene(manager))

    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        manager.scene.handle_events(events)
        manager.scene.update()
        manager.scene.draw(screen)

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()