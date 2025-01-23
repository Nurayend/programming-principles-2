import pygame

pygame.init()

screen = pygame.display.set_mode((800, 600))

done = False

color1 = (0, 128, 255)
color2 = (255, 0, 0)
is_color1 = True

x = 30
y = 30

# playerImage = pygame.image.load("pygame_idle.png")

# def player(x, y):
#     screen.blit(playerImage, (x, y))


while not done:
    for event in pygame.event.get():
        # event on quit
        if event.type == pygame.QUIT: # event.type == pygame.KEYDOWN
            done = True
        # Change color on press space key
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            is_color1 = not is_color1
        # Move
    # if event.type == pygame.KEYDOWN:
    #     if event.key == pygame.K_UP:
    #         y -= 3
    #     if event.key == pygame.K_DOWN:
    #         y += 3
    #     if event.key == pygame.K_LEFT:
    #         x -= 3
    #     if event.key == pygame.K_RIGHT:
    #         x += 3
    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_UP]: y -= 1
    if pressed[pygame.K_DOWN]: y += 1
    if pressed[pygame.K_LEFT]: x -= 1
    if pressed[pygame.K_RIGHT]: x += 1
        
    if is_color1:
        color = color1
    else:
        color = color2
    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, color, pygame.Rect(x, y, 60, 60))
    pygame.display.flip()

pygame.quit()