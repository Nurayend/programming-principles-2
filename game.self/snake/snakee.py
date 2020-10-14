import pygame
import random 
import time


pygame.init()

#-------MAIN---------
rows = 20
width = 600
height = 500

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Snake Game')
font = pygame.font.SysFont('Arial', 32) 
running = True

d = 5
FPS = 30
clock = pygame.time.Clock()

class Snake:

    def __init__(self):
        self.size = 1
        self.elements = [[100, 100]]
        self.radius = 10
        self.dx = 5  # right
        self.dy = 0
        self.score = 0
        self.is_add = False
        self.choose = 0

    def draw(self):
        for element in self.elements:
            pygame.draw.circle(screen, ((70 + element[0]) % 255, 10, (200 + element[0]) % 255), element, self.radius)

    def add_to_snake(self):
        self.choose = (self.choose + 1) % 5
        self.size += 1
        self.score += 1
        self.elements.append([0, 0])
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
        self.x = random.randint(30, width - 50)
        self.y = random.randint(30, height - 50)
        # self.radius = 10
        self.image = [pygame.image.load("fruit.png"), pygame.image.load("fruit-1.png"), pygame.image.load("fruit-2.png"), pygame.image.load("fruit-3.png"), pygame.image.load("fruit-4.png")]
        self.pos = [random.randint(0, 468), random.randint(0, 368)]
        self.food_append = True

    def draw(self):
        for i in self.pos:
            screen.blit(self.image[snake.choose], (self.x, self.y))


def in_walls():
    if snake.elements[0][0] > width - 24 or snake.elements[0][0] < 24:
        return True
        # snake.elements[0][0] = (snake.elements[0][0] + width) % width
    if snake.elements[0][1] > height - 24 or snake.elements[0][1] < 24:
        return True
    return False
        #snake.elements[0][1] = (snake.elements[0][1] + height) % height


def game_over():
    screen.fill((210, 160, 190))
    res = font.render('G A M E   O V E R!', True, (0, 90, 255))
    res1 = font.render('total score: ' + str(snake.score), True, (0, 90, 255))
    screen.blit(res, (150,150))
    screen.blit(res1, (200,250))
    pygame.display.update()
    time.sleep(3)
    pygame.quit()

def collision():
    if (food.x in range(snake.elements[0][0] - 28, snake.elements[0][0])) and  (food.y  in range(snake.elements[0][1] - 28, snake.elements[0][1])) :
        snake.is_add = True 
        if snake.is_add == True:
            food.x = random.randint(50, width - 50)
            food.y = random.randint(50, height - 50)

def scores (x,y, score):
    res = font.render('s c o r e:  ' + str(snake.score), True, (0, 90, 255)) #draw text on a new Surf
    screen.blit(res, (x, y))

wallImage = pygame.image.load('wall.png')

def make_walls():
    for i in range(0, width, 10):
        screen.blit(wallImage, (i, 0))
        screen.blit(wallImage, (i, height - 20))
        screen.blit(wallImage, (0, i))
        screen.blit(wallImage, (width - 24, i))


snake = Snake()
food = Food()

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
            game_over()
            running = False

    if in_walls() == 1:
        game_over()
        running = False
        
    collision()
    snake.move()
    screen.fill((251, 205, 182))
    snake.draw()
    food.draw()
    scores(25, 25, snake.score)
    make_walls()
    pygame.display.flip()