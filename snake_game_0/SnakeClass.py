import pygame, random

pygame.init()
#game
size = (720,460)
window = pygame.display.set_mode(size)
pygame.display.set_caption("Snake")
score_sur = pygame.Surface((100,20))
score_d = pygame.font.Font(None, 20)
score = 0
run = 1
game = False
FPS = 30
#menu
menu_sur = pygame.Surface(size)
menu = True
diff = ["Easy","Norm","Hard"]
Easy = True
Norm = False
Hard = False
class Snake:
    def __init__ (self, sur):
        self.head = [200,200]
        self.body = [[200,200], [200,190], [200,180]]
        self.sur = sur
        self.up = False
        self.down = True
        self.right = False
        self.left = False
    def direction(self,direction):
        if direction == "D" and self.up == False:
            self.down = True
            self.up = self.right = self.left = False
        elif direction == "U" and self.down == False:
            self.up = True
            self.down = self.right= self.left = False
        elif direction == "R" and self.left == False:
            self.right = True
            self.down = self.up = self.left = False
        elif direction == "L" and self.right == False:
            self.left = True
            self.down = self.up=self.right = False
    def move(self):
        if self.up: 
            self.head[1] -=10
            if self.head[1]<=-10: self.head[1]=460
        elif self.down: 
            self.head[1] +=10
            if self.head[1]>=460: self.head[1]=0
        elif self.right: 
            self.head[0] +=10
            if self.head[0]>=720: self.head[0]=0
        elif self.left: 
            self.head[0] -=10
            if self.head[0]<=-10: self.head[0]=720
    def boday(self,foodx,foody,score):
        self.body.insert(0,list(self.head))
        if foodx == self.head[0] and foody == self.head[1]:
            foodx = random.randrange(1,72)*10
            foody = random.randrange(1,46)*10
            score+=1
            return foodx,foody,score
        else: 
            self.body.pop()
            return foodx,foody,score
    def draw(self):
        for f in self.body:
            pygame.draw.rect(self.sur, (0,255,0),(f[0],f[1],10,10))
class Food:
    def __init__(self,sur):
        self.x = random.randrange(1,72)*10
        self.y = random.randrange(1,46)*10
        self.sur = sur
    def draw(self):
        pygame.draw.rect(self.sur, (255,0,0),(self.x,self.y,10,10))
snake = Snake(window)
food = Food(window)
direction = "D"
j = 0
while run:
    if menu:
        for f in pygame.event.get():
            if f.type == pygame.QUIT:
                pygame.quit()
                quit()
            if f.type == pygame.KEYDOWN:
                if f.key == pygame.K_SPACE:
                    game, menu = True, False
                if f.key == pygame.K_UP and j!=0:
                    j-=1
                if f.key == pygame.K_DOWN and j!=len(diff)-1:
                    j+=1

        menu_sur.fill((0,0,0))
        window.blit(menu_sur,(0,0))
        i = 200
        
        for f in diff:
            if j == 0 and diff.index(f) == j:
                window.blit((pygame.font.Font(None, 40)).render(f, 1, (200,200,0)),(250,i))
                FPS = 20
            elif j == 1 and diff.index(f) == j:
                window.blit((pygame.font.Font(None, 40)).render(f, 1, (200,200,0)),(250,i))
                FPS = 30
            elif j == 2 and diff.index(f) == j:
                window.blit((pygame.font.Font(None, 40)).render(f, 1, (200,200,0)),(250,i))
                FPS = 40
            else:
                window.blit((pygame.font.Font(None, 40)).render(f, 1, (200,0,0)),(250,i))
            i+=45
        pygame.display.update()
    elif game:
        for f in pygame.event.get():
            if f.type == pygame.QUIT:
                pygame.quit()
                quit()
            if f.type == pygame.KEYDOWN:
                if f.key == pygame.K_DOWN:
                    direction = "D"
                if f.key == pygame.K_UP:
                    direction = "U"
                if f.key == pygame.K_RIGHT:
                    direction = "R"
                if f.key == pygame.K_LEFT:
                    direction = "L"
        window.fill((150,150,150))
        snake.direction(direction)
        score_sur.fill((0,0,0))
        score_sur.blit(score_d.render("Score: "+str(score), 1, (255,255,255)), (0,0))
        window.blit(score_sur,(0,0))
        snake.move()
        food.x,food.y,score = snake.boday(food.x,food.y,score)
        food.draw()
        snake.draw()
        pygame.display.update()
        pygame.time.Clock().tick(FPS)
        
    