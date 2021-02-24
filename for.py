from threading import Thread
import pika
import uuid
import pygame
import json

pygame.init()
pygame.mixer.init() 

IP = '34.254.177.17'
PORT = 5672
VIRTUAL_HOST = 'dar-tanks'
USERNAME = 'dar-tanks'
PASSWORD = '5orPLExUYnyVYZg48caMpX'
width = 1000
height = 600
music = pygame.mixer.music.load("alive.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

window = pygame.display.set_mode((width, height))

shot = pygame.mixer.Sound("shoot1.wav")
shot.set_volume(0.2)
die = pygame.image.load("die.jpg") 
tank1_up = pygame.image.load("tank1_up.png")
tank1_right = pygame.image.load("tank1_right.png")
tank1_down = pygame.image.load("tank1_down.png")
tank1_left = pygame.image.load("tank1_left.png")

tank2_up = pygame.image.load("tank2_up.png")
tank2_right = pygame.image.load("tank2_right.png")
tank2_down = pygame.image.load("tank2_down.png")
tank2_left = pygame.image.load("tank2_left.png")

bullet1_up = pygame.image.load("bullet1_up.jpg")
bullet1_right = pygame.image.load("bullet1_right.jpg")
bullet2_up = pygame.image.load("bullet2_up.jpg")
bullet2_right = pygame.image.load("bullet2_right.jpg") 


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
            if self.tank_id == client.tank_id:
                return 1
            else : return 0 
            self.room_id = self.response['roomId'] 
            return True
        return False

    def turn_tank(self, token, direction):
        message = {
            'token': token,
            'direction': direction
        }
        self.call('tank.request.turn', message)

    def bullet(self, token):
        message = {
            'token' : token,
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

UP = 'UP'
DOWN = 'DOWN'
LEFT = 'LEFT'
RIGHT = 'RIGHT'

client = TankRpcClient()
event_client = TankConsumerClient('room-5')
event_client.daemon = True

def gameover():
    window.blit(die,(0,0)) 
    pygame.mixer.music.stop()
    music = pygame.mixer.music.load("over.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play() 

def game_start():
    font = pygame.font.SysFont('Comic Sans MS', 13)
    win = False
    kick = False
    lose = False  
    mainloop = True
    while mainloop:
        window.fill((0, 0, 0))
        info = pygame.Rect(800,0,200,600) 
        pygame.draw.rect(window, (75,0,130), info)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                mainloop = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    mainloop = False
                if event.key == pygame.K_w:
                    client.turn_tank(client.token, 'UP')
                if event.key == pygame.K_s:
                    client.turn_tank(client.token, 'DOWN')
                if event.key == pygame.K_d:
                    client.turn_tank(client.token, 'RIGHT')
                if event.key == pygame.K_a:
                    client.turn_tank(client.token, 'LEFT')
                if event.key == pygame.K_SPACE:
                    client.bullet(client.token)
                    pygame.mixer.stop()
                    pygame.mixer.Sound.play(shot) 
        try:
            remaining_time = event_client.response['remainingTime']
            text = font.render('Remaining Time: {}'.format(remaining_time),True, (154,50,205))
            textRect = text.get_rect()
            textRect.center = (880,20)
            window.blit(text, textRect)
            text_5 = font.render('Id :',True, (255,105,180))
            text_5_Rect = text.get_rect()
            text_5_Rect.center = (873,40) 
            window.blit(text_5, text_5_Rect)
            text_6 = font.render('Health :',True, (60,179,113))
            text_6_Rect = text.get_rect()
            text_6_Rect.center = (999,40)
            window.blit(text_6, text_6_Rect)
            text_7 = font.render('Score :',True, (205,92,92)) 
            text_7_Rect = text.get_rect()
            text_7_Rect.center = (940,40)
            window.blit(text_7, text_7_Rect)
        except:
            pass
        tanks = event_client.response['gameField']['tanks']
        bullets = event_client.response['gameField']['bullets']
        hits = event_client.response['hits']
        winners = event_client.response['winners']
        losers = event_client.response['losers']
        kicked = event_client.response['kicked']

        for tank in tanks:
            if tank['id'] == client.tank_id:
                if tank['direction'] == "UP":
                    tank_img = tank1_up
                elif tank['direction'] == "DOWN":
                    tank_img = tank1_down
                elif tank['direction'] == "LEFT":
                    tank_img = tank1_left
                elif tank['direction'] == "RIGHT":
                    tank_img = tank1_right
                window.blit(font.render(f"{tank['id']}", True, (255,0,0)), (tank['x'],tank['y']-int(tank['width']/2)))
            else:
                if tank['direction'] == "UP":
                    tank_img = tank2_up
                elif tank['direction'] == "DOWN":
                    tank_img = tank2_down
                elif tank['direction'] == "LEFT":
                    tank_img = tank2_left
                elif tank['direction'] == "RIGHT":
                    tank_img = tank2_right
                window.blit(font.render(f"{tank['id']}", True, (255,0,0)), (tank['x'],tank['y']-int(tank['width']/2)))
            window.blit(tank_img, (tank['x'],tank['y']))
        for bullet in bullets:
            if bullet['owner'] == client.tank_id:
                if bullet['direction'] == "UP":
                    bullet_img = bullet1_up
                elif bullet['direction'] == "DOWN":
                    bullet_img = bullet1_up
                elif bullet['direction'] == "LEFT":
                    bullet_img = bullet1_right
                elif bullet['direction'] == "RIGHT":
                    bullet_img = bullet1_right 
            else:
                if bullet['direction'] == "UP":
                    bullet_img = bullet2_up
                elif bullet['direction'] == "DOWN":
                    bullet_img = bullet2_up
                elif bullet['direction'] == "LEFT":
                    bullet_img = bullet2_right
                elif bullet['direction'] == "RIGHT":
                    bullet_img = bullet2_right 
            window.blit(bullet_img, (bullet['x'],bullet['y']))
        h = []
        s = [] 
        l = []
        k = [] 
        tanks.sort(key=lambda i: i['score'], reverse=1) 
        level = 60 
        caunt = 60 
        forik = 60 
        for tank in tanks: 
            c = int(tank["health"])
            h.append(c)
            c = int(tank["score"]) 
            s.append(c) 
            c = tank["id"]
            l.append(c) 
            for c in l: 
                text_3 = font.render('{}'.format(c),True, (255,105,180))
                text_3_Rect = text.get_rect()
                text_3_Rect.center = (873,forik)
            window.blit(text_3, text_3_Rect)
            forik += 20
            for c in h:
                text_1 = font.render('{}'.format(c),True,(60,179,113) )
                text_1_Rect = text.get_rect()
                text_1_Rect.center = (999,level)
            window.blit(text_1, text_1_Rect)
            level += 20
            for c in s:
                text_2 = font.render('{}'.format(c),True, (205,92,92))
                text_2_Rect = text.get_rect()
                text_2_Rect.center = (960,caunt)
            window.blit(text_2, text_2_Rect)
            caunt += 20
        
        if kicked:
            for z in kicked:
                if client.tank_id == z['tankId']:
                    kick = True
                
        elif losers:
            for z in losers:
                if client.tank_id == z['tankId']:
                    lose = True

        elif winners:
            for z in winners:
                if client.tank_id == z['tankId']:
                    win = True    
                    
        if kick == True:
            gameover()
            r = font.render('You are kicked', True, (0, 90, 255))
            screen.blit(r, (150, 190))
        elif win == True:
            gameover()
            r = font.render('You are winner', True, (0, 90, 255))
            screen.blit(r, (150, 190))    
        elif lose == True:
            gameover()
            r = font.render('You are loser', True, (0, 90, 255))
            screen.blit(r, (150, 190))

        pygame.display.flip()
    pygame.quit()
    client.connection.close()

client.check_server()
print(client.obtain_token('room-5'))
event_client.start()
game_start()