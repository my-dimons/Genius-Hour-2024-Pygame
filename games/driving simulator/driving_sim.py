import pygame
import random
import os
pygame.font.init()
#PROJECT STARTED OCT 2, 2024 @9:30am

#---VARS---

#ASSETS
CAR_IMAGE = pygame.image.load(os.path.join('games', 'driving simulator', 'Assets', 'car.png'))
ROAD_LINES_IMAGE = pygame.image.load(os.path.join('games', 'driving simulator','Assets', 'road.png'))
GAS_CAN_IMAGE = pygame.image.load(os.path.join('games', 'driving simulator','Assets', 'gas.png'))

#CLIENT
WIDTH, HEIGHT = 600, 1000
FPS = 60
SCORE = 1

#CAR
CAR_WIDTH, CAR_HEIGHT = 118, 220
CAR = pygame.transform.rotate(pygame.transform.scale(CAR_IMAGE, (CAR_WIDTH, CAR_HEIGHT)), 0)

CAR_STRAFE_SPEED = WIDTH / 75
BASE_GAME_SPEED = 12

#ROAD
ROAD_WIDTH = 15
ROAD_LEFT, ROAD_RIGHT = (WIDTH/3 - ROAD_WIDTH), (WIDTH - WIDTH/3)
# LINES
ROAD_LINES_HEIGHT = ROAD_LINES_IMAGE.get_height()
ROAD_LINES = pygame.transform.rotate(pygame.transform.scale(ROAD_LINES_IMAGE, (ROAD_WIDTH, ROAD_LINES_HEIGHT)), 0)
ROAD_START_POS = -400

#GAS
GAS_CAN_WIDTH, GAS_CAN_HEIGHT = 100, 100
GAS_CAN = pygame.transform.scale(GAS_CAN_IMAGE, (GAS_CAN_WIDTH, GAS_CAN_HEIGHT))
MAX_FUEL = 100

#COLORS
WHITE = 255, 255, 255
BLACK = 0, 0, 0
RED = 255, 0, 0

#---VARS---
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("work pls")

def draw_window(car, road_left, road_right, score_text, fuel_text, game_over_text, fuel, gas_cans): #UPDATE DISPLAY
    WIN.fill(BLACK) #ALWAYS UPDATE FIRST
    #ROAD LINES
    WIN.blit(ROAD_LINES, (road_left)) #RENDER LEFT ROAD LINES
    WIN.blit(ROAD_LINES, (road_right)) #RENDER RIGHT ROAD LINES
    for i in range(len(gas_cans)):
        WIN.blit(GAS_CAN, (gas_cans[i].x, gas_cans[i].y)) #RENDER GAS CAN
    WIN.blit(CAR, (car.x, car.y)) #RENDER CAR
    WIN.blit(score_text, (0,0)) #SCORE TEXT
    WIN.blit(fuel_text, (0,35)) #FUEL TEXT
    if (fuel <= 0):
        WIN.blit(game_over_text, game_over_text.get_rect(center=(WIDTH / 2, HEIGHT / 2)))
    pygame.display.update()


def main():
    car = pygame.Rect(WIDTH/2 - CAR_WIDTH/2, HEIGHT - 250, CAR_WIDTH, CAR_HEIGHT)
    road_left = pygame.Rect(ROAD_LEFT, ROAD_START_POS, ROAD_LINES_HEIGHT, HEIGHT) # left road line
    road_right = pygame.Rect(ROAD_RIGHT, ROAD_START_POS, ROAD_LINES_HEIGHT, HEIGHT) # right road line 

    # Stores the spawned gas cans
    gas_can_list = []

    # List of spawn locations for objects like the gas can
    spawn_locations = [(WIDTH/2 - WIDTH/3) - (GAS_CAN_WIDTH/2 + GAS_CAN_WIDTH/6),
                        WIDTH/2 - 50,
                        WIDTH - (WIDTH/2 - WIDTH/3) - (GAS_CAN_WIDTH/2 - GAS_CAN_WIDTH/6)]
    
    # Main stats
    current_fuel = MAX_FUEL
    speed = BASE_GAME_SPEED
    score = SCORE

    
    # TIMERS
    
    # Adds score
    SCOREEVENT = pygame.USEREVENT + 1
    pygame.time.set_timer(SCOREEVENT, 1000//5) #1 second = 1000 milliseconds

    # Spawns Fuel
    FUELEVENT = pygame.USEREVENT + 2
    pygame.time.set_timer(FUELEVENT, (1000 * 3 // (speed//BASE_GAME_SPEED))) #1 second = 1000 milliseconds

    # Collides with fuel (and adds fuel)
    GASCOLLECT = pygame.USEREVENT + 3

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            # Adds score
            elif event.type == SCOREEVENT:
                if (current_fuel > 0):
                    current_fuel = (current_fuel - speed/BASE_GAME_SPEED)
                    score = (score + speed/BASE_GAME_SPEED)
                    print(score)

            # Spawns Gas Can
            elif event.type == FUELEVENT:
                    gas_can = pygame.Rect(spawn_locations[random.randrange(0, 3)], -200, GAS_CAN_WIDTH, GAS_CAN_HEIGHT)
                    print("SPAWNING FUEL")
                    gas_can_list.append(gas_can)

            # Adds fuel when gas can is collected
            elif event.type == GASCOLLECT:
                current_fuel +=  50
                if current_fuel > MAX_FUEL:
                    current_fuel = 100
        
        # TEXT
        game_stats_font = pygame.font.SysFont('Arial', 30)
        game_over_font = pygame.font.SysFont('Arial', WIDTH//16)
        
        score_text_surface = game_stats_font.render(("SCORE = " + str(int(score))), False, (WHITE))
        fuel_text_surface = game_stats_font.render(("FUEL = " + str(int(current_fuel))) + "/100", False, (WHITE))
        game_over_text_surface = game_over_font.render("NO FUEL", False, (RED))

        # KEYS
        keys_pressed = pygame.key.get_pressed()

        # CALLING FUNCTIONS
        speed = control_car(keys_pressed, car, speed, current_fuel)
        move_road(road_left, road_right, speed, current_fuel)
        hande_gas_cans(gas_can_list, pygame.Rect(car.x, car.y, CAR_WIDTH, CAR_HEIGHT), current_fuel, speed, GASCOLLECT)
        draw_window(car,
                    road_left, 
                    road_right, 
                    score_text_surface, 
                    fuel_text_surface, 
                    game_over_text_surface, 
                    current_fuel,
                    gas_can_list)


# Moves the car left/right based on key presses
def control_car(key, car, speed, fuel):
    if key[pygame.K_a] and car.x > 0 - 30 and fuel > 0: #LEFT
        car.x -= CAR_STRAFE_SPEED
    if key[pygame.K_d] and car.x < WIDTH - 170 and fuel > 0: #RIGHT
        car.x += CAR_STRAFE_SPEED
    if key[pygame.K_w] and fuel > 0: #TURBO
        speed = BASE_GAME_SPEED * 3 #CONTROL SPEED
    else:
        speed = BASE_GAME_SPEED #CONTROL SPEED
    return speed

# Moves the road lines to simulate the car moving
def move_road(road_left, road_right, speed, fuel):
    if fuel > 0:
        road_left.y += speed
        road_right.y += speed

    # Repositions the road lines to make them "infinite"
    if (road_left.y >= (ROAD_START_POS + ROAD_LINES_HEIGHT/4 + 43)):
        print("REPOSITION")
        road_left.y = ROAD_START_POS
        road_right.y = ROAD_START_POS

# Handles gas can collision
def hande_gas_cans(gas_cans, car, fuel, speed, gascollect):
    if fuel > 0:
        for can in gas_cans:
            can.y += speed
            if car.colliderect(can):
                pygame.event.post(pygame.event.Event(gascollect))
                gas_cans.remove(can)



if __name__ == "__main__":
    main()

#--------CREDITS--------#


#GAS CAN:
    #https://pngtree.com/element/down?id=NTcxNTI2MQ==&type=1&time=1728244747&token=OWI1NDFiNTBiNzg3NTZhMzg4YTJiMTkxZGUxZjg0MTk=&t=0
#CAR:
    #https://www.clipartmax.com/middle/m2i8H7b1b1Z5Z5N4_car-clipart-birds-eye-view/


#--------CREDITS--------#


#TODO 
# (FIX) side border is broken, not properly colliding and is shifted to the left
# (ADD) Obstacles (cones, other cars, etc.)
# (CHANGE) change spawn_locations array (~ln 72, near the start of main()) to not use gas can width, make a new variable which is the new standard for objects
# (CHANGE) update comments to be more clear and be shorter