from threading import Thread
import threading as th
import pika, uuid, json
import pygame
import random
import time

IP = '34.254.177.17'
PORT = 5672
VIRTUAL_HOST = 'dar-tanks'
USERNAME = 'dar-tanks'
PASSWORD = '5orPLExUYnyVYZg48caMpX'
width = 800 + 180
height = 600

pygame.init()
screen = pygame.display.set_mode((width, height))
font = pygame.font.SysFont('Times New Roman', 20)

class TankRpcClient:
    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host = IP,
                port = PORT,
                virtual_host = VIRTUAL_HOST,
                credentials = pika.PlainCredentials(
                    username = USERNAME,
                    password = PASSWORD
                )
            )
        )
        self.channel = self.connection.channel()
        queue = self.channel.queue_declare(queue='',
                                           auto_delete=True,
                                           exclusive= True)
        self.callback_queue = queue.method.queue
        self.channel.queue_bind(
            exchange = 'X:routing.topic',
            queue = self.callback_queue
        )

        self.channel.basic_consume(
            queue = self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack = True
        )

        # self.response = None
        # self.corr_id = None
        self.token = None
        self.tank_id = None
        self.room_id = None

    def on_response(self, ch, method, props, body):#Принимает запрос
        if self.corr_id == props.correlation_id:
            self.response = json.loads(body)

    def call(self, key, message):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange = 'X:routing.topic',
            routing_key = key,
            properties=pika.BasicProperties(
                reply_to =self.callback_queue,
                correlation_id = self.corr_id
            ),
            body = json.dumps(message)
        )
        while self.response is None:
            self.connection.process_data_events()

    def check_server(self): #Healthcheck
        self.call('tank.request.healthcheck','')
        return self.response['status'] == '200'

    def obtain_token(self, room_id): #Register
        message = {
            'roomId':room_id
        }
        self.call('tank.request.register', message)
        if 'token' in self.response:
            self.token = self.response['token']
            self.tank_id = self.response['tankId']
            self.room_id = self.response['roomId']
            return True
        return False

    def turn_tank(self, token, direction):
        message = {
            'token': token,
            'direction': direction
        }
        self.call('tank.request.turn', message)

    def fire_bullet(self, token):
        message = {
            'token': token
        }
        self.call('tank.request.fire', message)


class TankConsumerClient(Thread):
    def __init__(self, roomId):
        super().__init__()
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host = IP,
                port = PORT,
                virtual_host = VIRTUAL_HOST,
                credentials = pika.PlainCredentials(
                    username = USERNAME,
                    password = PASSWORD
                )
            )
        )
        self.channel = self.connection.channel()
        queue = self.channel.queue_declare(queue='',
                                           auto_delete=True,
                                           exclusive= True
                                           )
        event_listener = queue.method.queue
        self.channel.queue_bind(exchange='X:routing.topic',
                                queue=event_listener,
                                routing_key='event.state.'+roomId
                                )
        self.channel.basic_consume(
            queue=event_listener,
            on_message_callback=self.on_response,
            auto_ack=True
        )
        self.response = None

    def on_response(self, ch, method, props, body):
        self.response = json.loads(body)
        print(self.response)

    def run(self):
        self.channel.start_consuming()

client = TankRpcClient()
event_client = TankConsumerClient('room-1')
event_client.daemon = True

UP = 'UP'
DOWN = 'DOWN'
LEFT = 'LEFT'
RIGHT = 'RIGHT'

def draw_tank(id, x, y, width, height, direction, health, score, img):
    if direction == RIGHT:
        right = pygame.transform.rotate(img, 90)
        screen.blit(right, (x, y))
    if direction == LEFT:
        left = pygame.transform.rotate(img, 270)
        screen.blit(left, (x, y))
    if direction == UP:
        up = pygame.transform.rotate(img, 180)
        screen.blit(up, (x, y))
    if direction == DOWN:
        down = pygame.transform.rotate(img, 0)
        screen.blit(down, (x, y))

def draw_bullets(owner, x, y, width, height, direction, fire):
    if direction == RIGHT:
        right = pygame.transform.rotate(fire, 270)
        screen.blit(right, (x, y))
    if direction == LEFT:
        left = pygame.transform.rotate(fire, 90)
        screen.blit(left, (x, y))
    if direction == UP:
        up = pygame.transform.rotate(fire, 0)
        screen.blit(up, (x, y))
    if direction == DOWN:
        down = pygame.transform.rotate(fire, 180)
        screen.blit(down, (x, y))

def information_panel(remaining_time):
    surface = pygame.Surface((200, 600))
    surface.fill((0, 51, 0))
    first_line = font.render('ID     | Health | Score ', True, (255, 255, 255))
    text = font.render('Remaining Time: {}'.format(remaining_time), True, (255, 255, 255))
    screen.blit(surface, (width-180, 0))
    screen.blit(text, (width-180, 0))
    screen.blit(first_line, (width-180, 30))

def game_over():
    screen.fill((128, 128, 128))
    text = font.render('If you want to replay press R', True, (0, 90, 255))
    over = font.render('GAME  OVER!', True, (0, 90, 255))
    screen.blit(over, (150,150))
    screen.blit(text, (150, 170))
    pygame.display.update()

def game_start():
    mainloop = True
    win = False
    kick = False
    lose = False
    client.turn_tank(client.token, UP)
    while mainloop:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                mainloop = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    mainloop = False
                
        try:
            remaining_time = event_client.response["remainingTime"]
        except:
            pass
        bullets = event_client.response['gameField']['bullets']
        tanks = event_client.response['gameField']['tanks']
        hits = event_client.response['hits']
        winners = event_client.response['winners']
        losers = event_client.response['losers']
        kicked = event_client.response['kicked']

        img1 = pygame.image.load("tank1m.png")
        img2 = pygame.image.load("tank2m.png")
        fire1 = pygame.image.load("fire1.png")
        fire2 = pygame.image.load("fire2.png")

        tankx = 0
        tanky = 0
        tankw = 0
        tankh = 0
        tankd = ''
        enemyx = 0
        enemyy = 0
        enemyw = 0
        enemyh = 0
        enemyd = ''
        bulletx = 0
        bullety = 0
        bulletw = 0
        bulleth = 0
        bulletd = ''
        ebulletx = 0
        ebullety = 0
        ebulletw = 0
        ebulleth = 0
        ebulletd = ''
        
        for tank in tanks:
            if tank['id'] == client.tank_id:
                tankx = tank['x']
                tanky = tank['y']
                tankw = tank['width']
                tankh = tank['height']
                tankd = tank['direction']
                draw_tank(tank['id'], tankx, tanky, tankw, tankh, tankd, tank['health'], tank['score'], img1)
            else:
                enemyx = tank['x']
                enemyy = tank['y']
                enemyw = tank['width']
                enemyh = tank['height']
                enemyd = tank['direction']
                draw_tank(tank['id'], enemyx, enemyy, enemyw, enemyh, enemyd, tank['health'], tank['score'], img2)    

        for bullet in bullets:
            if bullet['owner'] == client.tank_id:
                bulletx = bullet['x']
                bullety = bullet['y']
                bulletw = bullet['width']
                bulleth = bullet['height']
                bulletd = bullet['direction']
                draw_bullets(bullet['owner'], bulletx, bullety, bulletw, bulleth, bulletd, fire1)
            else:
                ebulletx = bullet['x']
                ebullety = bullet['y']
                ebulletw = bullet['width']
                ebulleth = bullet['height']
                ebulletd = bullet['direction']
                draw_bullets(bullet['owner'], ebulletx, ebullety, ebulletw, ebulleth, ebulletd, fire2)     
        
        #если стреляют с правой или с левой стороны
        if (0 <= ebulletx + ebulletw <= tankx or tankx <= ebulletx + ebulletw <= 800) and tanky <= ebullety <= tanky + tankh:
            client.turn_tank(client.token, UP)
        elif (0 <= ebullety + ebulleth <= tanky or tanky <= ebullety + ebulleth <= 600) and tankx <= ebulletx <= tankx + tankw:
            client.turn_tank(client.token, RIGHT)
        #если другие танки находятся справа или слева - стрелять в них
        if 35 < enemyx - tankx <= 100 and enemyy <= tanky + tankh//2 <= enemyy + enemyh:
            client.turn_tank(client.token, RIGHT)
            client.fire_bullet(client.token)
        elif 35 < tankx - enemyx <= 100 and enemyy <= tanky + tankh//2 <= enemyy + enemyh:
            client.turn_tank(client.token, LEFT)
            client.fire_bullet(client.token)
        #если другой танк сверху или снизу
        if 35 < enemyy - tanky <= 100 and enemyx <= tankx + tankw//2 <= enemyx + enemyw:
            client.turn_tank(client.token, DOWN)
            client.fire_bullet(client.token)
        elif 35 < tanky - enemyy <= 100 and enemyx <= tankx + tankw//2 <= enemyx + enemyw:
            client.turn_tank(client.token, UP)
            client.fire_bullet(client.token)    
        
        try:
            information_panel(remaining_time)
        except:
            pass
            
        j = 50
        t = {}
        for tank in tanks:      
            t[tank['id']] = [tank['health'],tank['score']]
        t_sorted = {a: b for a, b in sorted(t.items(), key=lambda item: item[1][1], reverse = True)}
        for i,s in t_sorted.items():
            lines = font.render('{}   | {} | {}'.format(i, s[0], s[1]), True, (255, 255, 255))
            screen.blit(lines, (width-180, j))
            j += 20

        if kicked:
            for e in kicked:
                if client.tank_id == e['tankId']:
                    kick = True
                
        elif losers:
            for e in losers:
                if client.tank_id == e['tankId']:
                    lose = True

        elif winners:
            for e in winners:
                if client.tank_id == e['tankId']:
                    win = True    
                    
        if kick == True:
            game_over()
            reason = font.render('You are kicked', True, (0, 90, 255))
            screen.blit(reason, (150, 190))
        if win == True:
            game_over()
            reason = font.render('You are winner', True, (0, 90, 255))
            screen.blit(reason, (150, 190))    
        if lose == True:
            game_over()
            reason = font.render('You are loser', True, (0, 90, 255))
            screen.blit(reason, (150, 190))
        
        pygame.display.flip()
    
    client.connection.close()

client.check_server()
print(client.obtain_token('room-1'))
event_client.start()
game_start()