import pygame, os, math, random
pygame.font.init()

# ---Vars---

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
PIZZA_RADIUS = 200 #SCALABLE
PIZZA_POS = WIDTH/4, HEIGHT/2

#UPGRADES
MULTIPLIER_ADD = 1
UPGRADE_COST = 10
UPGRADE_COST_INCREASE = 1.75
UPGRADE_WIDTH = 450
UPGRADE_HEIGHT = 75

#TOPPINGS
SAUCE_RADIUS = PIZZA_RADIUS - 15
CHEESE_RADIUS = PIZZA_RADIUS - 25
PEPPERONI_RADIUS = PIZZA_RADIUS/7.5
TOPPING_VARIANCE = 22

SAUCE_UNLOCKED = False
CHEESE_UNLOCKED = False
PEPPERONI_UNLOCKED = False

#CURRANCY
MONEY = 0 #MAIN CURRANCY

# ---Vars---

#DISPLAY
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("work pls")

def main():
    # Calculate all the topping variation
    pepperoni_variation = calculate_topping_variation()
    
    # Money
    money = 3000
    money_muliplier = 1
    multiplier_cost = 10
    money_per_second = 0
    money_per_second_count = 0

    # Pizza
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
            # ON CLICK
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Add money
                if(clicked_circle(pizza, PIZZA_RADIUS)):
                    add_money = int(1 * money_muliplier)
                    money += add_money
                    money_per_second_count += add_money
                    
                    print("---MONEY---")
                    print("")
                    print(money)
                    print("")
                    print("---MONEY---")
                    
                # Upgrade clicking
                if upgrade_multiplier.collidepoint(mouse_pos):
                    if(money >= multiplier_cost):
                        money_muliplier *= 2.5
                        money -= int(multiplier_cost)

                        multiplier_cost *= UPGRADE_COST_INCREASE
                        int(multiplier_cost)

                        toppings_unlocked += 1

                        print("---MULTIPLIER---")
                        print("")
                        print(money_muliplier)
                        print("")
                        print("---MULTIPLIER---")
                    else:
                        print("ERROR, NOT ENOUGH MONEY")

            # Calculates the money per second
            elif event.type == money_per_second_timer:
                money_per_second = money_per_second_count # (var changes when money is added)
                money_per_second_count = 0
                print("MONEY PER SECOND: " + str(money_per_second))

            if event.type == pygame.QUIT:
                run = False
        # Text
        money_text = font.render('$' + str(int(money)), False, WHITE)
        money_per_second_text = small_font.render('$ per second: ' + str(int(money_per_second)), False, WHITE)
        upgrade_text = small_font.render('NEXT TOPPING | COST: ' + str(int(multiplier_cost)), False, BLACK)

        draw_window(money_text           ,
                    upgrade_text         , 
                    upgrade_multiplier   , 
                    toppings_unlocked    ,
                    money_per_second_text, 
                    pepperoni_variation  )


def draw_window(money_text, upgrade_text, upgrade_multiplier_button, toppings_unlocked, money_per_second, topping_variation): #UPDATE DISPLAY
    WIN.fill(BACKGROUND_COLOR)

    # PIZZA
    pygame.draw.circle(WIN, BROWN, PIZZA_POS, PIZZA_RADIUS)

    # SAUCE
    if toppings_unlocked >= 1:
        SAUCE_UNLOCKED = True
        pygame.draw.circle(WIN, SAUCE_COLOR, PIZZA_POS, SAUCE_RADIUS)

    # CHEESE
    if toppings_unlocked >= 2:
        CHEESE_UNLOCKED = True
        pygame.draw.circle(WIN, CHEESE_COLOR, PIZZA_POS, CHEESE_RADIUS)

    # PEPPERONI
    if toppings_unlocked >= 3:
        PEPPERONI_UNLOCKED = True
        render_variation_toppings(SAUCE_COLOR, PIZZA_POS[0], PIZZA_POS[1], topping_variation, PEPPERONI_RADIUS)

    # Render text
    WIN.blit(money_per_second, (10, 80)) 
    WIN.blit(money_text, (10, 5))

    # Render upgrade button
    pygame.draw.rect(WIN, WHITE, pygame.Rect(upgrade_multiplier_button.x, upgrade_multiplier_button.y, upgrade_multiplier_button.width, upgrade_multiplier_button.height)) # upgrade button
    upgrade_text_rect = upgrade_text.get_rect(center=(upgrade_multiplier_button.x + upgrade_text.get_rect().width/2 + 15, upgrade_multiplier_button.y + upgrade_text.get_rect().height)) # upgrade text
    WIN.blit(upgrade_text, upgrade_text_rect)

    pygame.display.update()

def clicked_circle(self, radius):
    mouse_x, mouse_y = pygame.mouse.get_pos()
    dx = mouse_x - self.centerx
    dy = mouse_y - self.centery
    distance = math.sqrt(dx*dx + dy*dy)
    return distance <= radius

# Uses an array of turples to calculate the individual amount of variance for a topping
def calculate_topping_variation():
    i = 0
    variance = []
    while i < 10:
        variance.append([random.randrange(-TOPPING_VARIANCE, TOPPING_VARIANCE), random.randrange(-TOPPING_VARIANCE, TOPPING_VARIANCE)])
        i += 1

    return variance

# CHANGE THIS FORMAT FROM CIRCLES -> IMAGES
def render_variation_toppings(color, x_pos, y_pos, variation, radius):
    corners = PIZZA_RADIUS/1.7
    edges = PIZZA_RADIUS/2.5

    pygame.draw.circle(WIN, color, (x_pos - edges   + variation[0][0], y_pos  + edges  + variation[0][1]), radius) 
    pygame.draw.circle(WIN, color, (x_pos + edges   + variation[1][0], y_pos  - edges  + variation[1][1]), radius)
    pygame.draw.circle(WIN, color, (x_pos + edges   + variation[2][0], y_pos  + edges  + variation[2][1]), radius)
    pygame.draw.circle(WIN, color, (x_pos - edges   + variation[3][0], y_pos  - edges  + variation[3][1]), radius)
    pygame.draw.circle(WIN, color, (x_pos           + variation[4][0], y_pos + corners + variation[4][1]), radius) 
    pygame.draw.circle(WIN, color, (x_pos           + variation[5][0], y_pos - corners + variation[5][1]), radius)
    pygame.draw.circle(WIN, color, (x_pos + corners + variation[6][0], y_pos           + variation[6][1]), radius) 
    pygame.draw.circle(WIN, color, (x_pos - corners + variation[7][0], y_pos           + variation[7][1]), radius)
    pygame.draw.circle(WIN, color, (x_pos           + variation[8][0], y_pos           + variation[8][1]), radius)

# For fun
def grow_pizza(increment):
    global PIZZA_RADIUS
    global SAUCE_RADIUS
    global CHEESE_RADIUS
    global PEPPERONI_RADIUS

    PIZZA_RADIUS += increment
    SAUCE_RADIUS += increment
    CHEESE_RADIUS += increment
    PEPPERONI_RADIUS = PIZZA_RADIUS/7.5

if __name__ == "__main__":
    main()

# TODO
# (CHANGE) Center money text
# (ADD)    MORE TOPPINGS
# (ADD)    Money per second buildings
# (CHANGE) Change rendering for pepperoni from circles to images, allowing easy addition of new toppings