import pygame #MAKE SURE PYGAME IS INSTALLED

#CLIENT VARS
HEIGHT, WIDTH = 600, 600 #display size (height x width)
FPS = 200 #change fps

#DISPLAY
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game in Pygame")


def main():

    #CODE HERE

    run = True
    clock = pygame.time.Clock()
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        #CODE HERE

        draw_window()

def draw_window():
    #CODE TO UPDATE DISPLAY
    pygame.display.update()

if __name__ == "__main__":
    main()