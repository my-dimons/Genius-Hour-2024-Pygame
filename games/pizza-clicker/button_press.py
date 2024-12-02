import pygame, humanize # MAKE SURE PYGAME IS INSTALLED
print(humanize.intword("1234000", "%0.3f"))
# INFO: THIS SCRIPT WAS MADE TO TEST HOW PRESSSING A BUTTON WORKS

# CLIENT
HEIGHT, WIDTH = 600, 600 # Display size (height x width)
FPS = 60 # Change fps

# DISPLAY
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game in Pygame")


def main():
    pressed = 255, 0, 255
    normal = 255, 255, 255
    color = normal
    # CODE HERE (RUNS ONCE AT START)

    run = True
    clock = pygame.time.Clock()
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                color = pressed
            if event.type == pygame.MOUSEBUTTONUP:
                color = normal
            if event.type == pygame.QUIT:
                run = False

        # CODE HERE (UPDATED EVERY FRAME)

        draw_window(color)

def draw_window(color):
    WIN.fill(color)
    # CODE TO UPDATE DISPLAY
    pygame.display.update()

if __name__ == "__main__":
    main()