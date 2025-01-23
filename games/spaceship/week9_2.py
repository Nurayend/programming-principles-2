import pygame
import random

pygame.init()

screen = pygame.display.set_mode((800, 600))

pygame.display.set_caption("Spaceship")
score_sur = pygame.Surface((100, 20))
score_d = pygame.font.Font(None, 20)
score = 0
done = True

backgroundImage = pygame.image.load("space.jpg")

playerImage = pygame.image.load("player.png")
player_x = 200
player_y = 530

bullets = []

def player(x, y):
    screen.blit(playerImage, (x, y))
#Враг
class Enemy(object):
    
    def __init__(self,sur):
        self.x = random.randint(0, 736)
        self.y = random.randint(20, 50)
        self.img = pygame.image.load("enemy.png")
        self.dx = 7
        self.dy = 30
        self.sur = sur
        self.hitbox = pygame.Rect(self.x, self.y, 64, 64)
        self.hp = 2
    
    def move(self):
        self.x += self.dx
        if self.x < 0 or self.x > 736:
            self.dx = -self.dx
            self.y += self.dy
        #self.hitbox = pygame.Rect(self.x, self.y, 64, 64)
    
    def win(self):
        if self.hp == 0:
           quit()
           pygame.quit()
    
    def draw(self):
        screen.blit(self.img, (self.x, self.y))
    
#Пуля
class snaryad(object):
    
    def __init__(self, color,hitboxenemy):
        self.x = -100
        self.y = -100
        self.radius = 5
        self.color = color
        self.vel = 8 
        self.hitbox = pygame.Rect(self.x, self.y, 10, 10)
        self.shot = False
        self.hitboxenemy = hitboxenemy
        self.popal = False
    
    def shoot(self,x,y):
        self.x = round(x + 64//2)
        self.y = round(y + 64//2)
        self.shot = True
    
    def move(self,hitboxenemy):
        if self.shot:
            self.hitboxenemy = hitboxenemy
            self.hitbox = pygame.Rect(self.x, self.y - self.vel, 10, 10)
            if self.hitbox.colliderect(self.hitboxenemy):
                self.x = -100
                self.y = -100
                self.popal = True
                self.shot = False
                return
            self.y-=self.vel
            if self.y <= 0:
                self.x = -100
                self.y = -100
                self.shot = False
                return
    
    def minushp(self,hp):
        if self.popal: 
            self.popal = False
            hp -=1
        return hp
    
    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)

#Враг и пуля
enemy = Enemy(screen)
bullet = snaryad((0,255,0), enemy.hitbox)

while done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            done = False

    for bullet in bullets:
        if bullet.y > 0 and bullet.y < 800:
            bullet.y -= bullet.vel
        else:
            bullets.pop(bullets.index(bullet))

    # if enemy.x <= player.x <= round(enemy.x + 64//2) and enemy.y <= player.y <= round(enemy.y + 64//2):
    #     done = False

    pressed = pygame.key.get_pressed()

    if pressed[pygame.K_SPACE] and not(bullet.shot):
        bullet.shoot(player_x,player_y)
    if pressed[pygame.K_LEFT] and player_x > 0: 
        player_x -= 3
    if pressed[pygame.K_RIGHT] and player_x < 736: 
        player_x += 3
    
    enemy.move()
    bullet.move(enemy.hitbox)
    #enemy.win()
    screen.blit(backgroundImage, (0, 0))
    score_sur.fill((0,0,0))
    enemy.draw()
    bullet.draw()
    enemy.hp = bullet.minushp(enemy.hp)
    score_sur.blit(score_d.render("Health P: "+ str(enemy.hp), 1, (255,255,255)), (0,0))
    screen.blit(score_sur, (0,0))
    player(player_x, player_y)
    pygame.display.update()

pygame.quit()