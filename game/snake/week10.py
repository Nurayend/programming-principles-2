import pygame
import random

pygame.init()

screen = pygame.display.set_mode((600, 600))
pygame.display.set_caption("Snake")

score_d = pygame.font.Font(None, 30)
score = 0

backgroundImage = pygame.image.load("2.jpg")

class Snake:

    def __init__(self):
        self.size = 1
        self.elements = [[100, 100]]
        self.radius = 10
        self.dx = 5  # right
        self.dy = 0
        self.is_add = False

    def draw(self):
        for element in self.elements:
            pygame.draw.circle(screen, (0, 255, 0), element, self.radius)

    def add_to_snake(self):
        self.size += 1
        self.elements.append([0, 0])
        food.x = random.randint(80, 520)
        food.y = random.randint(80, 520)
        self.is_add = False
        
    def move(self):
        if self.is_add:
            self.add_to_snake()

        for i in range(self.size - 1, 0, -1):
            self.elements[i][0] = self.elements[i - 1][0]
            self.elements[i][1] = self.elements[i - 1][1]

        self.elements[0][0] += self.dx
        self.elements[0][1] += self.dy

class Food:

    def __init__(self):
        self.x = random.randint(80, 520)
        self.y = random.randint(80, 520)
        self.image = pygame.image.load("1.png")

    def draw(self):
        screen.blit(self.image, (self.x, self.y))
    
    def eat(self):
        if (self.x in range(snake.elements[0][0] - self.image.get_size()[0], snake.elements[0][0])) and (self.y  in range(snake.elements[0][1] - self.image.get_size()[1], snake.elements[0][1])):
            snake.is_add = True

poisonImage = pygame.image.load("poison.png")

def poison():
    for i in range(0, 600, 60):
        screen.blit(poisonImage, (i, 0))
        screen.blit(poisonImage, (i, 600 - 60))
        screen.blit(poisonImage, (0, i))
        screen.blit(poisonImage, (600 - 60, i))

def scores (x,y, score):
    sc = score_d.render('Score: ' + str(score), True, (0, 0, 0))
    screen.blit(sc, (x, y))

def end():
    if (snake.elements[0][0] > 600 - 65 or snake.elements[0][0] < 65) or (snake.elements[0][1] > 600 - 65 or snake.elements[0][1] < 65):
        return False

snake = Snake()
food = Food()

running = True

d = 5

FPS = 30

clock = pygame.time.Clock()

while running:
    mill = clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_RIGHT:
                snake.dx = d
                snake.dy = 0
            if event.key == pygame.K_LEFT:
                snake.dx = -d
                snake.dy = 0
            if event.key == pygame.K_UP:
                snake.dx = 0
                snake.dy = -d
            if event.key == pygame.K_DOWN:
                snake.dx = 0
                snake.dy = d
    
    for i in range(1, len(snake.elements)):
        if (snake.elements[0][0] == snake.elements[i][0] and snake.elements[0][1] == snake.elements[i][1]):
            running = False
    
    if end() == False:
        running = False

    if snake.is_add == True:
        score += 1
    
    screen.blit(backgroundImage, (0, 0))
    end()
    snake.move()
    food.eat()
    snake.draw()
    food.draw()
    poison()
    scores(0, 0, score)
    pygame.display.flip()

pygame.quit()