import pygame

class hero(object):

    def __init__(self, sur):
        self.x = 10
        self.y = 10
        self.sur = sur
        self.vel = 5
        
    def draw(self):
        pygame.draw.rect(sur, (0,255,0), (x, y))

class cub(object):

    def __init__(self, sur):
        self.x = 500
        self.y = 500
        self.sur = sur

    def draw(self):
        pygame.draw.rect(sur, (0,255,0), (x, y))

sur = pygame.display.set_mode(500, 500)

run = True

while run:
    for event in pygame.event.get():
        if evnt.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()
    