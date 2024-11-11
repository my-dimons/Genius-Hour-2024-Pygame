import pygame
import os
import math
pygame.font.init()

#------Vars

#CLIENT
WIDTH, HEIGHT = 1200, 1000
FPS = 60

#COLORS
BLACK = 0, 0, 0
WHITE = 255, 255, 255
BROWN = 245, 222, 179
BACKGROUND_COLOR = 43, 52, 87

#PIZZA
PIZZA_RADIUS = 200
PIZZA_POS = WIDTH/4, HEIGHT/2

#UPGRADES
MULTIPLIER_ADD = 1
UPGRADE_COST = 10
UPGRADE_COST_INCREASE = 2
UPGRADE_WIDTH = 450
UPGRADE_HEIGHT = 75
#CURRANCY
MONEY = 0 #PEPS IS MAIN CURRANCY

#DISPLAY
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("work pls")

def draw_window(peps_text, upgrade_text, upgrade_multiplier_button): #UPDATE DISPLAY
    WIN.fill(BACKGROUND_COLOR)
    pygame.draw.circle(WIN, BROWN, PIZZA_POS, PIZZA_RADIUS)
    

    pygame.draw.rect(WIN, WHITE, pygame.Rect(upgrade_multiplier_button.x, upgrade_multiplier_button.y, upgrade_multiplier_button.width, upgrade_multiplier_button.height))

    WIN.blit(peps_text, (10,5))
    upgrade_text_rect = upgrade_text.get_rect(center=(upgrade_multiplier_button.x + upgrade_text.get_rect().width/2 + 15, upgrade_multiplier_button.y + upgrade_text.get_rect().height))
    WIN.blit(upgrade_text, upgrade_text_rect)
    pygame.display.update()

def main():
    pizza = pygame.draw.circle(WIN, BROWN, PIZZA_POS, PIZZA_RADIUS)
    upgrade_multiplier = pygame.Rect(WIDTH/2, HEIGHT - HEIGHT/4, UPGRADE_WIDTH, UPGRADE_HEIGHT)
    money = 0
    money_muliplier = 1
    multiplier_cost = 10

    font = pygame.font.SysFont('Arial', 70)
    small_font = pygame.font.SysFont('Arial', 30)
    run = True
    clock = pygame.time.Clock()
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            mouse_pos = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if(clicked_circle(pizza, PIZZA_RADIUS)):
                    money += int(1 * money_muliplier)
                    print("---MONEY---")
                    print(money)
                    print("---MONEY---")
                if upgrade_multiplier.collidepoint(mouse_pos):
                    if(money >= multiplier_cost):
                        money_muliplier += 1
                        money -= int(multiplier_cost)
                        multiplier_cost *= UPGRADE_COST_INCREASE
                        int(multiplier_cost)
                        print("---MULTIPLIER---")
                        print(money_muliplier)
                        print("---MULTIPLIER---")
                    else:
                        print("ERROR, NOT ENOUGH MONEY")
            if event.type == pygame.QUIT:
                run = False
        peps_text = font.render('Money: ' + str(int(money)), False, WHITE)
        upgrade_text = small_font.render('NEXT UPGRADE | COST: ' + str(int(multiplier_cost)), False, BLACK)
        draw_window(peps_text, upgrade_text, upgrade_multiplier)

def clicked_circle(self, radius):
    mouse_x, mouse_y = pygame.mouse.get_pos()
    dx = mouse_x - self.centerx
    dy = mouse_y - self.centery
    distance = math.sqrt(dx*dx + dy*dy)  # or: distance = math.hypot(dx, dy)
    return distance <= radius

if __name__ == "__main__":
    main()