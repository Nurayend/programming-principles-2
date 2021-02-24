import pygame
import random

WIDTH = 600
HEIGHT = 700
FPS = 40

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Lab1")
clock = pygame.time.Clock()

font_name = pygame.font.match_font('arial')

def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


def show_go_screen():
    screen.blit(background, background_rect)
    draw_text(screen, "LAB1", 64, WIDTH / 2, HEIGHT / 4)
    draw_text(screen, "Welcome!", 22, WIDTH / 2, HEIGHT / 2)
    draw_text(screen, "Press a key to begin", 18, WIDTH / 2, HEIGHT * 3 / 4)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (100, 40))
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0

    def update(self):
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -8
        if keystate[pygame.K_RIGHT]:
            self.speedx = 8
        self.rect.x += self.speedx
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = mob_img
        self.image = pygame.transform.scale(mob_img, (80, 80))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100,-40)
        self.speedy = random.randrange(1, 8)
        self.speedx = random.randrange(-3, 3)
        
    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)

player_img = pygame.image.load("rainbow.jpg")
mob_img = pygame.image.load( "0.png")
background = pygame.image.load("f.jpg")
background_rect = background.get_rect()

hit_sound = pygame.mixer.Sound("s.wav")
pygame.mixer.music.load("s.wav")
pygame.mixer.music.play()
pygame.mixer.music.set_volume(0.8)


waiting = True
running = True
while running:
    if waiting:
        show_go_screen()
        waiting = False
        all_sprites = pygame.sprite.Group()
        mobs = pygame.sprite.Group()
        player = Player()
        fallen = pygame.draw.rect(screen, (0, 0, 0), (0, HEIGHT, 2, 2))
        all_sprites.add(player)
        
        for i in range(8):
            m = Mob()
            all_sprites.add(m)
            mobs.add(m)
        score = 0
        score2=0

    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    all_sprites.update()
    
    hits = pygame.sprite.spritecollide(player, mobs, True)
    if hits:
        running =True
        score+=1
        hit_sound.play()
    fall = pygame.sprite.spritecollide(mobs, fallen, True)
    if fall:
        running = True
        score2 += 1
    if score2 == 10:
        running = False
    if score==8:
        running=False
    
    

    screen.fill(WHITE)
    screen.blit(background, background_rect)
    draw_text(screen, 'Score:'+str(score), 20, WIDTH /10, 10)
    draw_text(screen, 'Score2:'+str(score2), 20, WIDTH - 60, 10)
    
    all_sprites.draw(screen)
    pygame.display.flip()

pygame.quit()