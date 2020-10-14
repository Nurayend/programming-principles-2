import pygame
import random

pygame.init()
screen = pygame.display.set_mode((500, 400))


def wildPainting():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    x = random.randint(0, screen.get_size()[0])
    y = random.randint(0, screen.get_size()[1])
    R = random.randint(50, 500)

    pygame.draw.circle(screen, (r, g, b), (x, y), R)

ballx = 350
bally = 200
dx = 700
dy = 700
def draw_ball(seconds):
    global ballx, bally, dx, dy
    pygame.draw.circle(screen, (255, 0, 0), (ballx, bally), 10)
    ballx += int(dx * seconds)
    bally += int(dy * seconds)
    if ballx + 2 * 10 > screen.get_size()[0] or ballx < 0:
        dx *= -1
    if bally + 2 * 10 > screen.get_size()[1] or bally < 0:
        dy *= -1


running = True
FPS = 30

clock = pygame.time.Clock()

while running:
    millis = clock.tick(FPS)
    seconds = millis / 1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_1:
                FPS = 5
            if event.key == pygame.K_2:
                FPS = 10
            if event.key == pygame.K_3:
                FPS = 20
            if event.key == pygame.K_4:
                FPS = 40

    # wildPainting()
    screen.fill((0, 0, 0))
    draw_ball(seconds)
    pygame.display.flip()