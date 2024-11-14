from distutils.core import setup
import py2exe, pygame, math
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
SAUCE_COLOR = 214, 56, 61
CHEESE_COLOR = 242, 217, 51

#PIZZA
PIZZA_RADIUS = 200
PIZZA_POS = WIDTH/4, HEIGHT/2

#UPGRADES
MULTIPLIER_ADD = 1
UPGRADE_COST = 10
UPGRADE_COST_INCREASE = 2.5
UPGRADE_WIDTH = 450
UPGRADE_HEIGHT = 75

#TOPPINGS
SAUCE_RADIUS = PIZZA_RADIUS - 15
CHEESE_RADIUS = PIZZA_RADIUS - 21

#CURRANCY
MONEY = 0 #PEPS IS MAIN CURRANCY

#DISPLAY
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("work pls")

def draw_window(money_text, upgrade_text, upgrade_multiplier_button, toppings_unlocked, money_per_second): #UPDATE DISPLAY
    WIN.fill(BACKGROUND_COLOR)
    #PIZZA
    pygame.draw.circle(WIN, BROWN, PIZZA_POS, PIZZA_RADIUS)
    
    #SAUCE
    if toppings_unlocked >= 1:
        pygame.draw.circle(WIN, SAUCE_COLOR, PIZZA_POS, SAUCE_RADIUS)

    #CHEESE
    if toppings_unlocked >= 2:
        pygame.draw.circle(WIN, CHEESE_COLOR, PIZZA_POS, CHEESE_RADIUS)

    pygame.draw.rect(WIN, WHITE, pygame.Rect(upgrade_multiplier_button.x, upgrade_multiplier_button.y, upgrade_multiplier_button.width, upgrade_multiplier_button.height))

    WIN.blit(money_per_second, (10, 80)) 
    WIN.blit(money_text, (10, 5))
    upgrade_text_rect = upgrade_text.get_rect(center=(upgrade_multiplier_button.x + upgrade_text.get_rect().width/2 + 15, upgrade_multiplier_button.y + upgrade_text.get_rect().height))
    WIN.blit(upgrade_text, upgrade_text_rect)
    pygame.display.update()

def main():
    # Money
    money = 0
    money_muliplier = 1
    multiplier_cost = 10
    money_per_second = 0
    money_per_second_count = 0

    toppings_unlocked = 0
    pizza = pygame.draw.circle(WIN, BROWN, PIZZA_POS, PIZZA_RADIUS)
    upgrade_multiplier = pygame.Rect(WIDTH/2, HEIGHT - HEIGHT/4, UPGRADE_WIDTH, UPGRADE_HEIGHT)

    # Font
    font = pygame.font.SysFont('Arial', 70)
    small_font = pygame.font.SysFont('Arial', 30)

    # Timers
    money_per_second_interval = 1000 # 1 seconds
    money_per_second_timer = pygame.USEREVENT + 1
    pygame.time.set_timer(money_per_second_timer , money_per_second_interval)

    run = True
    clock = pygame.time.Clock()
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            mouse_pos = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Add money
                if(clicked_circle(pizza, PIZZA_RADIUS)):
                    add_money = int(1 * money_muliplier)
                    money += add_money
                    money_per_second_count += add_money
                    
                    print("---MONEY---")
                    print(money)
                    print("---MONEY---")
                    
                # Increase money and add new topping on upgrade click
                if upgrade_multiplier.collidepoint(mouse_pos):
                    if(money >= multiplier_cost):
                        money_muliplier += 1
                        money -= int(multiplier_cost)
                        multiplier_cost *= UPGRADE_COST_INCREASE
                        int(multiplier_cost)
                        toppings_unlocked += 1
                        print("---MULTIPLIER---")
                        print(money_muliplier)
                        print("---MULTIPLIER---")
                    else:
                        print("ERROR, NOT ENOUGH MONEY")
            elif event.type == money_per_second_timer:
                money_per_second = money_per_second_count
                money_per_second_count = 0
                print("MONEY PER SECOND: " + str(money_per_second))
            if event.type == pygame.QUIT:
                run = False
        money_text = font.render('$' + str(int(money)), False, WHITE)
        money_per_second_text = small_font.render('$ per second: ' + str(int(money_per_second)), False, WHITE)
        upgrade_text = small_font.render('NEXT TOPPING | COST: ' + str(int(multiplier_cost)), False, BLACK)

        draw_window(money_text, upgrade_text, upgrade_multiplier, toppings_unlocked, money_per_second_text)

def clicked_circle(self, radius):
    mouse_x, mouse_y = pygame.mouse.get_pos()
    dx = mouse_x - self.centerx
    dy = mouse_y - self.centery
    distance = math.sqrt(dx*dx + dy*dy)  # or: distance = math.hypot(dx, dy)
    return distance <= radius

if __name__ == "__main__":
    main()

#TODO
# (CHANGE) Center money text
# (ADD)    MORE TOPPINGS
# (ADD)    Money per second buildings