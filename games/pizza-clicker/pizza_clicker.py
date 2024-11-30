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

#BUTTONS
BUTTON_WIDTH = 450
BUTTON_HEIGHT = 75
# upgrades
UPGRADE_COST = 100
MULTIPLIER_ADD = 1
UPGRADE_COST_INCREASE = 10

#$/S BUILDINGS
BUILDING_PRICE_INCREASE = 1.2
# pizza stand
PIZZA_STAND_BASE_PRICE = 25
PIZZA_STAND_BUTTON = pygame.Rect(WIDTH/2, HEIGHT/8 * 0 + 40, BUTTON_WIDTH, BUTTON_HEIGHT)
# food truck
FOOD_TRUCK_BASE_PRICE = 250
FOOD_TRUCK_BUTTON = pygame.Rect(WIDTH/2, HEIGHT/8 * 1 + 40, BUTTON_WIDTH, BUTTON_HEIGHT)
# pizzeria
PIZZERIA_BASE_PRICE = 8000
PIZZERIA_BUTTON = pygame.Rect(WIDTH/2, HEIGHT/8 * 2 + 40, BUTTON_WIDTH, BUTTON_HEIGHT)
# theme park
THEME_PARK_BASE_PRICE = 100000
THEME_PARK_BUTTON = pygame.Rect(WIDTH/2, HEIGHT/8 * 3 + 40, BUTTON_WIDTH, BUTTON_HEIGHT)
# space station
SPACE_STATION_BASE_PRICE = 1000000
SPACE_STATION_BUTTON = pygame.Rect(WIDTH/2, HEIGHT/8 * 4 + 40, BUTTON_WIDTH, BUTTON_HEIGHT)
# pizza dimension
PIZZA_DIMENSION_BASE_PRICE = 1000000000
PIZZA_DIMENSION_BUTTON = pygame.Rect(WIDTH/2, HEIGHT/8 * 5 + 40, BUTTON_WIDTH, BUTTON_HEIGHT)

#TOPPINGS
TOPPING_SIZE = 2.5
TOPPING_DIMENSIONS = PIZZA_RADIUS/TOPPING_SIZE
TOPPING_VARIANCE = 25

# sauce
SAUCE_RADIUS = PIZZA_RADIUS - 15
# cheese
CHEESE_RADIUS = PIZZA_RADIUS - 25
# pepperoni
PEPPERONI_IMAGE = pygame.image.load(os.path.join('games', 'pizza-clicker', 'assets', 'pepperoni.png'))
PEPPERONI = pygame.transform.scale(PEPPERONI_IMAGE, (TOPPING_DIMENSIONS, TOPPING_DIMENSIONS))
# mushrooms
MUSHROOM_IMAGE = pygame.image.load(os.path.join('games', 'pizza-clicker', 'assets', 'mushroom.png'))
MUSHROOM = pygame.transform.scale(MUSHROOM_IMAGE, (TOPPING_DIMENSIONS, TOPPING_DIMENSIONS))
# olives
OLIVES_IMAGE = pygame.image.load(os.path.join('games', 'pizza-clicker', 'assets', 'olives.png'))
OLIVES = pygame.transform.scale(OLIVES_IMAGE, (TOPPING_DIMENSIONS/2, TOPPING_DIMENSIONS/2))
# tomato
TOMATO_IMAGE = pygame.image.load(os.path.join('games', 'pizza-clicker', 'assets', 'tomato.png'))
TOMATO = pygame.transform.scale(TOMATO_IMAGE, (TOPPING_DIMENSIONS/1.5, TOPPING_DIMENSIONS/1.5))
# basil
BASIL_IMAGE = pygame.image.load(os.path.join('games', 'pizza-clicker', 'assets', 'basil.png'))
BASIL = pygame.transform.scale(BASIL_IMAGE, (TOPPING_DIMENSIONS, TOPPING_DIMENSIONS))
# shrimp
SHRIMP_IMAGE = pygame.image.load(os.path.join('games', 'pizza-clicker', 'assets', 'shrimp.png'))
SHRIMP = pygame.transform.scale(SHRIMP_IMAGE, (TOPPING_DIMENSIONS, TOPPING_DIMENSIONS))

SAUCE_UNLOCKED = False
CHEESE_UNLOCKED = False
PEPPERONI_UNLOCKED = False
MUSHROOM_UNOCKED = False
OLIVES_UNLOCKED = False
TOMATO_UNLOCKED = False


#CURRANCY
MONEY = 0.0 #MAIN CURRANCY

# ---Vars---

#DISPLAY
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pizza Clicker")

def main():
    get_global_buildings()
    # Calculate all the topping variation
    variation = [calculate_topping_variation(),
                 calculate_topping_variation(),
                 calculate_topping_variation(),
                 calculate_topping_variation()]
    # Buildings
    building_buttons = [(PIZZA_STAND_BUTTON, "Pizza Stand"),
                 (FOOD_TRUCK_BUTTON, "Food Truck"),
                 (PIZZERIA_BUTTON, "Pizzeria"),
                 (THEME_PARK_BUTTON, "Theme Park"),
                 (SPACE_STATION_BUTTON, "Space Station"),
                 (PIZZA_DIMENSION_BUTTON, "Pizza Dimension")]
    #Building Variables
    pizza_stands_owned = 0
    pizza_stand_price = PIZZA_STAND_BASE_PRICE
    pizza_stand_money = 0.25
    food_trucks_owned = 0
    food_truck_price = FOOD_TRUCK_BASE_PRICE
    food_truck_money = 2
    pizzerias_owned = 0
    pizzeria_price = PIZZERIA_BASE_PRICE
    pizzeria_money = 6
    theme_parks_owned = 0
    theme_park_price = THEME_PARK_BASE_PRICE
    theme_park_money = 25
    space_stations_owned = 0
    space_station_price = SPACE_STATION_BASE_PRICE
    space_station_money = 50
    pizza_dimensions_owned = 0
    pizza_dimension_price = PIZZA_DIMENSION_BASE_PRICE
    pizza_dimension_money = 50000
    #Building Variables


    #Button
    buttonColors = {
            'normal': '#ffffff',
            'hover': '#666666',
            'pressed': '#333333',
        }

    # Money
    money = MONEY
    money_muliplier = 1
    upgrade = 1
    multiplier_cost = UPGRADE_COST
    money_per_second = 0.0
    money_per_second_count = 0

    # Pizza
    toppings_unlocked = 0
    pizza = pygame.draw.circle(WIN, BROWN, PIZZA_POS, PIZZA_RADIUS)
    upgrade_multiplier_button = pygame.Rect(WIDTH/2, HEIGHT - HEIGHT/8, BUTTON_WIDTH, BUTTON_HEIGHT)

    # Font
    font = pygame.font.SysFont('Arial', 70)
    small_font = pygame.font.SysFont('Arial', 30)
    super_small_font = pygame.font.SysFont('Arial', 15)
    # Timers
    money_per_second_interval = 1000 # 1 seconds
    money_per_second_timer = pygame.USEREVENT + 1
    pygame.time.set_timer(money_per_second_timer , money_per_second_interval)

    pizza_stand_money, food_truck_money, pizzeria_money, theme_park_money, space_station_money, pizza_dimension_money = update_building_money(pizza_stand_money, food_truck_money, pizzeria_money, theme_park_money, space_station_money, pizza_dimension_money, upgrade)
    
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
                if upgrade_multiplier_button.collidepoint(mouse_pos):
                    if money >= multiplier_cost:
                        money_muliplier *= 2.5
                        upgrade *= 2
                        money -= int(multiplier_cost)
                        pizza_stand_money, food_truck_money, pizzeria_money, theme_park_money, space_station_money, pizza_dimension_money = update_building_money(pizza_stand_money, food_truck_money, pizzeria_money, theme_park_money, space_station_money, pizza_dimension_money, upgrade)
        
                        multiplier_cost *= UPGRADE_COST_INCREASE
                        int(multiplier_cost)

                        toppings_unlocked += 1

                        print("---MULTIPLIER---")
                        print("")
                        print(money_muliplier)
                        print("")
                        print("---MULTIPLIER---")
                    else:
                        print("ERROR, NOT ENOUGH MONEY/MAX UPGRADES")
                # Buy $/s building
                if building_buttons[0][0].collidepoint(mouse_pos):
                    pizza_stands_owned, pizza_stand_price, money = buy_building(pizza_stands_owned, pizza_stand_price, money)
                if building_buttons[1][0].collidepoint(mouse_pos):
                    food_trucks_owned, food_truck_price, money = buy_building(food_trucks_owned, food_truck_price, money)             
                if building_buttons[2][0].collidepoint(mouse_pos):
                    pizzerias_owned, pizzeria_price, money = buy_building(pizzerias_owned, pizzeria_price, money)                 
                if building_buttons[3][0].collidepoint(mouse_pos):
                    theme_parks_owned, theme_park_price, money = buy_building(theme_parks_owned, theme_park_price, money)                 
                if building_buttons[4][0].collidepoint(mouse_pos):
                    space_stations_owned, space_station_price, money = buy_building(space_stations_owned, space_station_price, money)                 
                if building_buttons[5][0].collidepoint(mouse_pos):
                    pizza_dimensions_owned, pizza_dimension_price, money = buy_building(pizza_dimensions_owned, pizza_dimension_price, money)  
                money_per_second = calculate_money_per_second(pizza_stands_owned, 
                                                              pizza_stand_money, 
                                                              food_trucks_owned, 
                                                              food_truck_money, 
                                                              pizzerias_owned, 
                                                              pizzeria_money,
                                                              theme_parks_owned,
                                                              theme_park_money,
                                                              space_stations_owned,
                                                              space_station_money,
                                                              pizza_dimensions_owned,
                                                              pizza_dimension_money)
                
            # Calculates the money per second
            elif event.type == money_per_second_timer:
                money += money_per_second

            if event.type == pygame.QUIT:
                run = False
        # Text
        money_per_second_text = small_font.render('$/s: ' + str(round(money_per_second, 1)), False, WHITE)
        money_text = font.render('$' + str(round(money, 1)), False, WHITE)
        topping_upgrade_text = small_font.render(buy_next_topping_text(toppings_unlocked, multiplier_cost), False, BLACK)
        building_buy_text = [small_font.render(building_buttons[0][1] + ' | $' + str(round(pizza_stand_price, 1)), False, BLACK),
                             small_font.render(building_buttons[1][1] + ' | $' + str(round(food_truck_price, 1)), False, BLACK),
                             small_font.render(building_buttons[2][1] + ' | $' + str(round(pizzeria_price, 1)), False, BLACK),
                             small_font.render(building_buttons[3][1] + ' | $' + str(round(theme_park_price, 1)), False, BLACK),
                             small_font.render(building_buttons[4][1] + ' | $' + str(round(space_station_price, 1)), False, BLACK),
                             small_font.render(building_buttons[5][1] + ' | $' + str(round(pizza_dimension_price, 1)), False, BLACK)]
        buildings_owned_text = [super_small_font.render('Owned ' + str(pizza_stands_owned) , False, BLACK),
                                super_small_font.render('Owned ' + str(food_trucks_owned) , False, BLACK),
                                super_small_font.render('Owned ' + str(pizzerias_owned) , False, BLACK),
                                super_small_font.render('Owned ' + str(theme_parks_owned) , False, BLACK),
                                super_small_font.render('Owned ' + str(space_stations_owned) , False, BLACK),
                                super_small_font.render('Owned ' + str(pizza_dimensions_owned) , False, BLACK)]        
        building_money_per_second_text = [super_small_font.render('+' + str(round(pizza_stand_money, 1)) + '$/s', False, BLACK),
                                          super_small_font.render('+' + str(round(food_truck_money, 1)) + '$/s', False, BLACK),
                                          super_small_font.render('+' + str(round(pizzeria_money, 1)) + '$/s', False, BLACK),
                                          super_small_font.render('+' + str(round(theme_park_money, 1)) + '$/s', False, BLACK),
                                          super_small_font.render('+' + str(round(space_station_money, 1)) + '$/s', False, BLACK),
                                          super_small_font.render('+' + str(round(pizza_dimension_money, 1)) + '$/s', False, BLACK)]
        
        
        
        draw_window(money_text,
                    topping_upgrade_text, 
                    upgrade_multiplier_button, 
                    toppings_unlocked,
                    money_per_second_text, 
                    variation,
                    building_buy_text,
                    building_buttons,
                    buildings_owned_text,
                    building_money_per_second_text)

def buy_building(owned, price, money):
    global BUILDING_PRICE_INCREASE
    if money >= price:
        money -= price
        price *= BUILDING_PRICE_INCREASE
        owned += 1
        print("BOUGHT BUILDING")
        return owned, price, money
    else:
        print("NOT ENOUGH MONEY")
        return owned, price, money

def draw_window(money_text, upgrade_text, button, toppings_unlocked, money_per_second, variation, building_text, buildings, buildings_owned_text, building_money_per_second_text): #UPDATE DISPLAY
    WIN.fill(BACKGROUND_COLOR)

    # Render pizza with toppings
    render_pizza(toppings_unlocked, variation)

    # Render text
    WIN.blit(money_per_second, (10, 80)) 
    WIN.blit(money_text, (10, 5))

    render_building_buttons(building_text, buildings_owned_text, building_money_per_second_text, buildings)

    # Render upgrade button
    pygame.draw.rect(WIN, WHITE, pygame.Rect(button.x, button.y, button.width, button.height)) # upgrade button
    upgrade_text_rect = upgrade_text.get_rect(center=(button.x + upgrade_text.get_rect().width/2 + 15, button.y + upgrade_text.get_rect().height)) # upgrade text
    WIN.blit(upgrade_text, upgrade_text_rect)

    pygame.display.update()

# Calculates the $/s using all the bought buildings and multipliers
def calculate_money_per_second(pizza_stands_owned, 
                                pizza_stand_money, 
                                food_trucks_owned, 
                                food_truck_money, 
                                pizzerias_owned, 
                                pizzeria_money,
                                theme_parks_owned,
                                theme_park_money,
                                space_stations_owned,
                                space_station_money,
                                pizza_dimensions_owned,
                                pizza_dimension_money):
    money_per_second = ((pizza_stands_owned * pizza_stand_money) + 
                        (food_trucks_owned * food_truck_money) + 
                        (pizzerias_owned * pizzeria_money) + 
                        (theme_parks_owned * theme_park_money) +
                        (space_stations_owned * space_station_money) + 
                        (pizza_dimensions_owned * pizza_dimension_money))
    print("MONEY PER SECOND: " + str(money_per_second))
    return money_per_second

# Renders all the buttons for $/s buildings
def render_building_buttons(text, owned, money, building_buttons):
    get_global_buildings()
    i = 0
    for button in building_buttons:
        pygame.draw.rect(WIN, WHITE, button[0])
        text_rect = text[i].get_rect(center=(button[0].x + text[i].get_rect().width/2 + 15, button[0].y + text[i].get_rect().height))
        owned_rect = owned[i].get_rect(center=(button[0].x + owned[i].get_rect().width/2 + 15, button[0].y + owned[i].get_rect().height + button[0].height/2 + 4))
        money_rect = owned[i].get_rect(center=(button[0].x + owned[i].get_rect().width/2 + 110, button[0].y + owned[i].get_rect().height + button[0].height/2 + 4))
        WIN.blit(owned[i], owned_rect)
        WIN.blit(text[i], text_rect)
        WIN.blit(money[i], money_rect)
        i += 1
    i = 0

def get_global_buildings():
    global PIZZA_STAND_BASE_PRICE
    global PIZZA_STAND_BUTTON
    global FOOD_TRUCK_BASE_PRICE
    global FOOD_TRUCK_BUTTON
    global PIZZERIA_BASE_PRICE
    global PIZZERIA_BUTTON
    global THEME_PARK_BASE_PRICE
    global THEME_PARK_BUTTON
    global SPACE_STATION_BASE_PRICE
    global SPACE_STATION_BUTTON 
    global PIZZA_DIMENSION_BASE_PRICE
    global PIZZA_DIMENSION_BUTTON

def render_pizza(toppings_unlocked, variation):
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
        render_variation_toppings(PIZZA_POS[0], PIZZA_POS[1], variation[0], TOPPING_DIMENSIONS, PEPPERONI)

    # MUSHROOM
    if toppings_unlocked >= 4:
        MUSHROOM_UNOCKED = True
        render_variation_toppings(PIZZA_POS[0], PIZZA_POS[1], variation[1], TOPPING_DIMENSIONS, MUSHROOM)
    
    # OLIVES
    if toppings_unlocked >= 5:
        OLIVES_UNLOCKED = True
        render_variation_toppings(PIZZA_POS[0], PIZZA_POS[1], variation[2], TOPPING_DIMENSIONS, OLIVES)

    # TOMATO
    if toppings_unlocked >= 6:
        OLIVES_UNLOCKED = True
        render_variation_toppings(PIZZA_POS[0], PIZZA_POS[1], variation[3], TOPPING_DIMENSIONS, TOMATO)

# Uses an array of turples to calculate the individual amount of variance for a topping
def calculate_topping_variation():
    i = 0
    variance = []
    while i < 10:
        variance.append([random.randrange(-TOPPING_VARIANCE, TOPPING_VARIANCE), random.randrange(-TOPPING_VARIANCE, TOPPING_VARIANCE), random.randrange(0, 360)])
        i += 1

    return variance
# CHANGE THIS FORMAT FROM CIRCLES -> IMAGES
def render_variation_toppings(x_pos, y_pos, variation, dimensions, image):
    x = 0 # doesn't do anything, just a filler for the pepperoni dimensions
    i = 0
    corners = PIZZA_RADIUS/1.7
    edges = PIZZA_RADIUS/2.5

    # CREATE RECTS
    topping  = [pygame.Rect(x_pos - edges   + variation[0][0], y_pos  + edges  + variation[0][1], x, x),
                pygame.Rect(x_pos + edges   + variation[1][0], y_pos  - edges  + variation[1][1], x, x),
                pygame.Rect(x_pos + edges   + variation[2][0], y_pos  + edges  + variation[2][1], x, x),
                pygame.Rect(x_pos - edges   + variation[3][0], y_pos  - edges  + variation[3][1], x, x),
                pygame.Rect(x_pos           + variation[4][0], y_pos + corners + variation[4][1], x, x),
                pygame.Rect(x_pos           + variation[5][0], y_pos - corners + variation[5][1], x, x),
                pygame.Rect(x_pos + corners + variation[6][0], y_pos           + variation[6][1], x, x),
                pygame.Rect(x_pos - corners + variation[7][0], y_pos           + variation[7][1], x, x),
                pygame.Rect(x_pos           + variation[8][0], y_pos           + variation[8][1], x, x)]

    # RENDER
    for rect in topping:
        # set the centers
        rect.x -= dimensions/2
        rect.y -= dimensions/2
        WIN.blit(pygame.transform.rotate(image, variation[i][2]), (rect.x, rect.y))
        i += 1
# Get the next topping in the form of a string
def buy_next_topping_text(toppings_unlocked, multiplier_cost):
    next_topping = toppings_unlocked + 1
    topping, add, cost = "", "", ""
    # CONSTANTS
    COST = " | $" + str(int(multiplier_cost))
    ADD = "Add "

    match next_topping:
        case 1:
            topping = "Sauce"
            add, cost = ADD, COST
        case 2:
            topping = "Cheese"
            add, cost = ADD, COST
        case 3:
            topping = "Pepperoni"
            add, cost = ADD, COST
        case 4:
            topping = "Mushroom"
            add, cost = ADD, COST
        case 5:
            topping = "Olive"
            add, cost = ADD, COST
        case 6:
            topping = "Tomato"
            add, cost = ADD, COST
        case _:
            topping = "Upgrade"
            add, cost = "", COST

    return str(add + topping + cost)
# For fun
def grow_pizza(increment):
    global PIZZA_RADIUS, SAUCE_RADIUS, CHEESE_RADIUS
    global TOPPING_DIMENSIONS

    PIZZA_RADIUS += increment
    SAUCE_RADIUS += increment
    CHEESE_RADIUS += increment
  
    TOPPING_DIMENSIONS = PIZZA_RADIUS/7.5

def update_building_money(pizza_stand, food_truck, pizzeria, theme_park, space_station, dimension, upgrade):
    if upgrade < 50:
        pizza_stand *= upgrade
        food_truck *= upgrade
        pizzeria *= upgrade
        theme_park *= upgrade
        space_station *= upgrade
        dimension *= upgrade
    return pizza_stand, food_truck, pizzeria, theme_park, space_station, dimension

def clicked_circle(self, radius):
    mouse_x, mouse_y = pygame.mouse.get_pos()
    dx = mouse_x - self.centerx
    dy = mouse_y - self.centery
    distance = math.sqrt(dx*dx + dy*dy)
    return distance <= radius

if __name__ == "__main__":
    main()

# TODO
# (CHANGE) Center money text
# (ADD)    Rebirths/Prestige (very simple)
# (ADD)    Goal text (goal is to crash the game)
# (CHANGE) Buttons to fade out to gray when they cannot be clicked
# (CHANGE) Balance midgame
# (CHANGE) make the topping button stand out (make it a little bit of a different color)
# (ADD)    hover & click animation on buttons
# (ADD)    Animations/interactions when clicking a button/pizza

# BUILDINGS LIST
# Pizza Stand
# Food Truck
# Pizzeria
# Theme Park
# Space Station
# Pizza Dimension


# CREDITS

# Pepperoni: https://www.svgrepo.com/svg/417228/pepperoni
# Olives: https://www.svgrepo.com/svg/417247/black-olives
# Mushroom: https://www.svgrepo.com/svg/417230/mushrooms
# Tomatos: https://nohat.cc/f/related-cut-tomato-clipart-tomato-slice-free-vector/m2i8d3N4N4m2K9Z5-202208020011.html