import pygame #MAKE SURE PYGAME IS INSTALLED

#CLIENT VARS
HEIGHT, WIDTH = 900, 900 #display size (height x width)
FPS = 800 #change fps

#COLORS
GREEN = 0, 255, 0
RED = 255, 0, 0
#DISPLAY
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Test your reaction time")


def main():
    can_click = False
    current_color = RED
    TIMEREVENT = pygame.USEREVENT + 1
    
    pygame.time.set_timer(TIMEREVENT, 1000)

    run = True
    clock = pygame.time.Clock()
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == TIMEREVENT:
                current_color = GREEN
                can_click = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if can_click:
                    print("CLICKED")
                else:
                    print("CLICKED TOO EARLY")


        #CODE HERE
        draw_window(current_color)

def draw_window(color):
    
    WIN.fill(color)
    pygame.display.update()
    
if __name__ == "__main__":
    main()