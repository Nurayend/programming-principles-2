import pygame
import random



pygame.init()
pygame.font.init()

screen = pygame.display.set_mode((800, 600))



def bg():
    backgroundImage = pygame.image.load("bg1.jpg")
    screen.blit(backgroundImage, (0, 0))

class Snake:

    def __init__(self):
        self.size = 1
        self.elements = [[100, 100]]
        self.radius = 10
        self.x = self.elements[0][0]
        self.y = self.elements[0][1]
        self.dx = 5
        self.dy = 0
        self.score = 0
        self.is_add = False

    def draw(self):
        for element in self.elements:
            pygame.draw.circle(screen, (255, 0, 0), element, self.radius)

    def add_to_snake(self):
        self.size += 1
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

def edge():
    if snake.elements[0][0] > 800:
        snake.elements[0][0] = 0
        snake.elements[0][0] += snake.dx
    if snake.elements[0][0] < 0:
        snake.elements[0][0] = 800
        snake.elements[0][0] += snake.dx
    if snake.elements[0][1] > 600:
        snake.elements[0][1] = 0
        snake.elements[0][1] += snake.dy
    if snake.elements[0][1] < 0:
        snake.elements[0][1] = 600
        snake.elements[0][1] += snake.dy



class Apple:
    def __init__(self, image_path):
        self.image = pygame.image.load(image_path)
        self.x = random.randint(10, 780)
        self.y = random.randint(10, 570)
        self.elements = [[100, 100]]
        self.rect = 10

    def draw(self):
        for element in self.elements:
            screen.blit(self.image, (self.x, self.y))


   
def collision():
    if (apple.x >= snake.elements[0][0] - apple.image.get_size()[0]  and apple.x < snake.elements[0][0] + apple.image.get_size()[0]) and  (apple.y >= snake.elements[0][1] - apple.image.get_size()[1] and apple.y < snake.elements[0][1] + apple.image.get_size()[1]):
        snake.is_add = True  
        if snake.is_add == True:
            snake.score += 5
            apple.x = random.randint(10, 780)
            apple.y = random.randint(10, 570)
    if (bonbon.x >= snake.elements[0][0] - bonbon.image.get_size()[0]  and bonbon.x < snake.elements[0][0] + bonbon.image.get_size()[0]) and  (bonbon.y >= snake.elements[0][1] - bonbon.image.get_size()[1] and bonbon.y < snake.elements[0][1] + bonbon.image.get_size()[1]):
        snake.is_add = True  
        if snake.is_add == True:
            snake.score += 5
            bonbon.x = random.randint(10, 780)
            bonbon.y = random.randint(10, 570)
    if (burger.x >= snake.elements[0][0] - burger.image.get_size()[0]  and burger.x < snake.elements[0][0] + burger.image.get_size()[0]) and  (burger.y >= snake.elements[0][1] - burger.image.get_size()[1] and burger.y < snake.elements[0][1] + burger.image.get_size()[1]):
        snake.is_add = True  
        if snake.is_add == True:
            snake.score += 5
            burger.x = random.randint(10, 780)
            burger.y = random.randint(10, 570)



def Score():
    font = pygame.font.SysFont("arial", 25)
    pnt = font.render("YOUR SCORE: " + str(snake.score), True, (238, 246, 11))
    screen.blit(pnt, (580, 10))

def GameOver():
    
        f = pygame.font.SysFont("arial", 75)
        end = f.render("G A M E   O V E R", True, (255, 255, 0))
        snake.dx = 0
        snake.dy = 0
        screen.blit(end, (200, 250))
        pygame.display.update()
        
        

snake = Snake()
apple = Apple("fruit-1.png")
bonbon = Apple("fruit-2.png")
burger = Apple("fruit-3.png")



running = True

d = 5

FPS = 30

clock = pygame.time.Clock()

k1_pressed = False

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
            if event.key == pygame.K_DOWN:
                snake.dx = 0
                snake.dy = d
            if event.key == pygame.K_LEFT:
                snake.dx = -d
                snake.dy = 0
            if event.key == pygame.K_UP:
                snake.dx = 0
                snake.dy = -d
    if snake.elements[0] in snake.elements[1:]:
        GameOver()
    
        

    screen.fill((0, 0, 0))
    bg()
    snake.move()
    edge()
    collision()
    Score()
    apple.draw()
    bonbon.draw()
    burger.draw()
    snake.draw()
    pygame.display.flip()
 