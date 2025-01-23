import pygame
import random

pygame.init()

screen = pygame.display.set_mode((800, 600))

pygame.display.set_caption("Spaceship")
score_sur = pygame.Surface((100,20))
score_d = pygame.font.Font(None, 20)
score = 0
done = True

backgroundImage = pygame.image.load("space.jpg")

playerImage = pygame.image.load("player.png")
player_x = 200
player_y = 530

enemyImage = pygame.image.load("enemy.png")
enemy_x = random.randint(0, 736)
enemy_y = random.randint(20, 50)

enemy_dx = 3
enemy_dy = 26

bullets = []

def player(x, y):
    screen.blit(playerImage, (x, y))

def enemy(x, y):
    screen.blit(enemyImage, (x, y))
        
class snaryad():
    
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.vel = 8 

    def draw(self,screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)

while done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            done = False

    for bullet in bullets:
        if bullet.y > 0 and bullet.y < 800:
            bullet.y -= bullet.vel
        else:
            bullets.pop(bullets.index(bullet))

    pressed = pygame.key.get_pressed()

    if pressed[pygame.K_SPACE]:
        if len(bullets) == 0:
            bullets.append(snaryad(round(player_x + 64//2), round(player_y + 64//2), 5, (255, 0, 0)))
    if pressed[pygame.K_LEFT] and player_x > 0: 
        player_x -= 3
    if pressed[pygame.K_RIGHT] and player_x < 736: 
        player_x += 3

    enemy_x += enemy_dx
    if enemy_x < 0 or enemy_x > 736:
        enemy_dx = -enemy_dx
        enemy_y += enemy_dy
   
    if enemy_x <= player_x <= round(enemy_x + 64//2) and enemy_y <= player_y <= round(enemy_y + 64//2):
        done = False
    
    for bullet in bullets:
        while enemy_x <= bullet.x <= enemy_x + 64 and enemy_y <= bullet.y <= enemy_y + 64:
            enemy_x = random.randint(0, 736)
            enemy_y = random.randint(20, 50)
            enemy_dx += 2
            enemy_dy += 2
            score += 1

    screen.blit(backgroundImage, (0, 0))
    score_sur.fill((0,0,0))
    score_sur.blit(score_d.render("Score: "+ str(score), 1, (255,255,255)), (0,0))
    screen.blit(score_sur,(0,0))
    player(player_x, player_y)
    enemy(enemy_x, enemy_y)
    for bullet in bullets:
        bullet.draw(screen)
    pygame.display.flip()

pygame.quit()