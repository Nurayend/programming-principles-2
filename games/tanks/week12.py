import pygame
from enum import Enum
import time

pygame.init()
width = 800
height = 500
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Tanks')
font = pygame.font.SysFont("Times New Roman", 20)
shot = pygame.mixer.Sound("Shot.wav")
popal = pygame.mixer.Sound("popal.wav")
end = pygame.mixer.Sound("the_end.wav")
music = pygame.mixer.music.load("Music.wav")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)
popal.set_volume(0.2)

class Direction(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4

class Tank(object):

    def __init__(self, x, y, color, d_right=pygame.K_RIGHT, d_left=pygame.K_LEFT, d_up=pygame.K_UP, d_down=pygame.K_DOWN):
        self.x = x
        self.y = y
        self.speed = 4
        self.color = color
        self.width = 40
        self.direction = Direction.RIGHT
        self.hp = 3

        self.KEY = {d_right: Direction.RIGHT, d_left: Direction.LEFT,
                    d_up: Direction.UP, d_down: Direction.DOWN}

    def draw(self):
        tank_c = (self.x + int(self.width / 2), self.y + int(self.width / 2))
        pygame.draw.rect(screen, self.color,
                         (self.x, self.y, self.width, self.width), 2)
        pygame.draw.circle(screen, self.color, tank_c, int(self.width / 2))

        if self.direction == Direction.RIGHT:
            pygame.draw.line(screen, self.color, tank_c, (self.x + self.width + int(self.width / 2), self.y + int(self.width / 2)), 4)

        if self.direction == Direction.LEFT:
            pygame.draw.line(screen, self.color, tank_c, (
            self.x - int(self.width / 2), self.y + int(self.width / 2)), 4)

        if self.direction == Direction.UP:
            pygame.draw.line(screen, self.color, tank_c, (self.x + int(self.width / 2), self.y - int(self.width / 2)), 4)

        if self.direction == Direction.DOWN:
            pygame.draw.line(screen, self.color, tank_c, (self.x + int(self.width / 2), self.y + self.width + int(self.width / 2)), 4)


    def change_direction(self, direction):
        self.direction = direction

    def move(self):
        if self.direction == Direction.LEFT:
            self.x -= self.speed
        if self.direction == Direction.RIGHT:
            self.x += self.speed
        if self.direction == Direction.UP:
            self.y -= self.speed
        if self.direction == Direction.DOWN:
            self.y += self.speed
        self.draw()
        self.edge()
        self.rect = pygame.Rect(self.x, self.y, 40, 40)

    def bullet(self, bullets):
        if len(bullets) == 0:
            if self.direction == Direction.RIGHT:
                bullets.append(snaryad(self.x + self.width + int(self.width / 2), self.y + int(self.width / 2), self.color, 1))
                pygame.mixer.Sound.play(shot)
            if self.direction == Direction.LEFT:
                bullets.append(snaryad(self.x - self.width + int(self.width / 2), self.y + int(self.width / 2), self.color, -1))
                pygame.mixer.Sound.play(shot)
            if self.direction == Direction.UP:
                bullets.append(snaryad(self.x + int(self.width / 2), self.y + int(self.width / 2), self.color, -1))
                pygame.mixer.Sound.play(shot)
            if self.direction == Direction.DOWN:
                bullets.append(snaryad(self.x + int(self.width / 2), self.y + self.width + int(self.width / 2), self.color, 1))
                pygame.mixer.Sound.play(shot)

    def edge(self):
        if self.x > width:
            self.x = 0
            self.x += self.speed
        if self.x < 0:
            self.x = width
            self.x += self.speed
        if self.y > height:
            self.y = 0
            self.y += self.speed
        if self.y < 0:
            self.y = height
            self.y += self.speed

class snaryad(object):
    
    def __init__(self, x, y, color, facing):
        self.x = x
        self.y = y
        self.radius = 5
        self.color = color
        self.vel = 20 * facing
        self.facing = facing
    
    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)

    def move(self, bullets, tank):
        if self.x > 0 and self.x < width and self.y > 0 and self.y < height:
            if tank.direction == Direction.RIGHT or tank.direction == Direction.LEFT:
                self.x += self.vel
            if tank.direction == Direction.UP or tank.direction == Direction.DOWN:
                self.y += self.vel
        else:
            bullets.pop(bullets.index(bullet))

def game_over(winner):
    screen.fill((128, 128, 128))
    res = font.render('GAME  OVER!', True, (0, 90, 255))
    res1 = font.render('Winner is ' + str(winner), True, (0, 90, 255))
    screen.blit(res, (150,150))
    screen.blit(res1, (200,250))
    pygame.mixer.music.pause()
    pygame.mixer.Sound.play(end)
    pygame.display.update()
    time.sleep(5)
    pygame.quit()

mainloop = True
bullets1 = []
bullets2 = []
FPS = 30
clock = pygame.time.Clock()

tank1 = Tank(200, 200, (255, 123, 100))
tank2 = Tank(100, 100, (100, 230, 40), pygame.K_d, pygame.K_a, pygame.K_w, pygame.K_s)
tanks = [tank1, tank2]

while mainloop:
    mill = clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            mainloop = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                mainloop = False
            if event.key == pygame.K_RETURN:
                tank1.bullet(bullets1)            
            if event.key == pygame.K_SPACE:
                tank2.bullet(bullets2)
                
            for tank in tanks:
                if event.key in tank.KEY.keys():
                    tank.change_direction(tank.KEY[event.key])
    if tank2.x + tank2.width >= tank1.x >= tank2.x  and tank2.y + tank2.width>=tank1.y>=tank2.y:
            tank1.x += tank1.speed
            tank2.x -= tank2.speed
    if tank2.x + tank2.width >= tank1.x + tank1.width >= tank2.x  and tank2.y + tank2.width >= tank1.y >= tank2.y:      
            tank1.y += tank1.speed
            tank2.y -= tank2.speed
    if tank2.x + tank2.width >= tank1.x >= tank2.x  and tank2.y + tank2.width >= tank1.y + tank1.width >= tank2.y:
            tank1.y -= tank1.speed
            tank2.y += tank2.speed
    if tank2.x + tank2.width >= tank1.x + tank1.width >= tank2.x and tank2.y + tank2.width >= tank1.y + tank1.width >= tank2.y:
            tank1.x -= tank1.speed
            tank2.x += tank2.speed
    for bullet in bullets1:
        bullet.move(bullets1, tank1)
    for bullet in bullets2:
        bullet.move(bullets2, tank2)
    for bullet in bullets1:
        if bullet.y >= tank2.y and bullet.y <= tank2.y + tank2.width and bullet.x >= tank2.x and bullet.x <= tank2.x + tank2.width:
            bullets1.pop(bullets1.index(bullet)) 
            tank2.hp -= 1
            pygame.mixer.Sound.play(popal)
    for bullet in bullets2:
        if bullet.y >= tank1.y and bullet.y <= tank1.y + tank1.width and bullet.x >= tank1.x and bullet.x <= tank1.x + tank1.width:
            bullets2.pop(bullets2.index(bullet)) 
            tank1.hp -= 1
            pygame.mixer.Sound.play(popal)
    screen.fill((0, 0, 0))
    screen.blit(font.render(f"Hp: {tank1.hp}", 1, (255, 123, 100)),(18, 0))
    screen.blit(font.render(f"Hp: {tank2.hp}", 1, (100, 230, 40)), (740,0))
    if tank1.hp == 0:
        winner = "Player2"
        game_over(winner)
    if tank2.hp == 0:
        winner = "Player1"
        game_over(winner) 
    for tank in tanks:
        tank.move()
    for bullet in bullets1:
        bullet.draw()
    for bullet in bullets2:
        bullet.draw()
    pygame.display.flip()

pygame.quit()