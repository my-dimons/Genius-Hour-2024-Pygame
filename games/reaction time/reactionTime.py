import pygame
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

    # Timer
    randomRange = random.randint(3, 6)
    TIMEREVENT = pygame.USEREVENT + 1
    pygame.time.set_timer(TIMEREVENT, randomRange * 1000)
    
    
    font = pygame.font.SysFont('Arial', 60)
    time_text = font.render('', False, (0, 0, 0))

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
                    time_text = font.render(str(seconds - randomRange) + " Second(s), " + str(milliseconds) + " Milliseconds", False, (0, 0, 0))
                else:
                    print("CLICKED TOO EARLY")
        
        # Timer text
        
        #Stopwatch 
        ticks = pygame.time.get_ticks()
        draw_window(current_color, time_text)

def draw_window(color, time_text):
    
    WIN.fill(color)
    WIN.blit(time_text, (WIDTH/2 - 50, HEIGHT/2))
    pygame.display.update()
    
if __name__ == "__main__":
    main()