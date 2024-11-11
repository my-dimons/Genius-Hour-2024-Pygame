import pygame
import math
import random
pygame.font.init()
#PROJECT STARTED ~OCT 9, 2024

#---VARS---

#CLIENT
WIDTH, HEIGHT = 900, 900
FPS = 60

#COLORS
WHITE = 255, 255, 255
BLACK = 0, 0, 0
RED = 255, 0, 0
BACKGROUND_COLOR = 232, 220, 202

#ASSETS
BUTTON_RADIUS = 250
BUTTON_POS = (WIDTH/2, HEIGHT/2)

#---VARS---
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("GAMBLE!!!!")

def draw_window(times_clicked_text, failiure_chance_text): #UPDATE DISPLAY
    WIN.fill(BACKGROUND_COLOR)
    WIN.blit(times_clicked_text, times_clicked_text.get_rect(center=(WIDTH/2, 100)))
    WIN.blit(failiure_chance_text, failiure_chance_text.get_rect(center=(WIDTH/2, 800)))
    pygame.draw.circle(WIN, BLACK, BUTTON_POS, BUTTON_RADIUS + 20) #BLACK BACKGROUND
    pygame.draw.circle(WIN, RED, BUTTON_POS, BUTTON_RADIUS) #RED BUTTON
    pygame.display.update()


def main():
    circle_button = pygame.draw.circle(WIN, RED, BUTTON_POS, BUTTON_RADIUS)
    times_clicked = 0
    faliure_chance = 50
    current_failure_chance = 100
    highscore = 0
    highscore_failure_chance = 0

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if (clicked(circle_button, BUTTON_RADIUS)):
                    if (random.randint(0, 100) <= (100 / (100 / faliure_chance))):
                        if (times_clicked > highscore):
                            highscore = times_clicked
                            highscore_failure_chance = current_failure_chance
                        print("YOU LOST")
                        times_clicked = 0
                        current_failure_chance = 100
                    else:
                        times_clicked = times_clicked+ 1
                        current_failure_chance = current_failure_chance/ 2
                        print("|-------Button clicked!-------|")
                        print("")
                        print("Times Clicked = " + str(times_clicked))
                        print("Current Faliure Change = " + str(current_failure_chance))
                        print("")
                        print("-----Highscore-----")
                        print("Highscore = " + str(highscore))
                        print("Highscore Failure Chance = " + str(highscore_failure_chance))
                        print("-----Highscore-----")
                        print("")
                        print("|-------Button clicked!-------|")
        stats_text = pygame.font.SysFont("Arial", 60)
        times_clicked_text = stats_text.render('Currently Clicked ' + str(times_clicked) + " Times", False, (0, 0, 0))
        current_failure_chance_text = stats_text.render('To get this far is a ' + str(current_failure_chance) + '% Chance', False, (0, 0, 0))
        draw_window(times_clicked_text, current_failure_chance_text)


def clicked(self, radius):
    mouse_x, mouse_y = pygame.mouse.get_pos()
    dx = mouse_x - self.centerx
    dy = mouse_y - self.centery
    distance = math.sqrt(dx*dx + dy*dy)  # or: distance = math.hypot(dx, dy)
    return distance <= radius

if __name__ == "__main__":
    main()