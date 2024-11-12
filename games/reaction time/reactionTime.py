import pygame #MAKE SURE PYGAME IS INSTALLED
import random
pygame.font.init()
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


    # Stopwatch
    milliseconds = 0
    current_ticks = 0
    ticks = 0

    # Timner
    randomRange = random.randint(3, 6)
    TIMEREVENT = pygame.USEREVENT + 1
    pygame.time.set_timer(TIMEREVENT, randomRange * 1000)
    

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
                current_ticks = pygame.time.get_ticks()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if can_click:
                    milliseconds = (ticks - current_ticks) % 1000
                    seconds = int(ticks/1000 % 60)
                    print("CLICKED")
                    print(str(seconds - randomRange) + " Second(s), " + str(milliseconds) + " Milliseconds")
                else:
                    print("CLICKED TOO EARLY")
        
        # Timer text
        font = pygame.font.SysFont('Arial', 34)
        time_text = font.render('Reaction Time:' + str(milliseconds), False, (0, 0, 0))
        
        #Stopwatch 
        ticks = pygame.time.get_ticks()
        draw_window(current_color)

def draw_window(color):
    
    WIN.fill(color)
    pygame.display.update()
    
if __name__ == "__main__":
    main()