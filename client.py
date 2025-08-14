import pygame
from socket import*
from random import randint
from threading import Thread
from customtkinter import *

server_ip = ""
server_port = 0
player_nick = ""

def gett():
    global server_ip, server_port, player_nick
    server_ip = entry_ip.get()
    server_port = int(entry_port.get())
    player_nick = entry_nick.get()
    okno.destroy()

okno = CTk()
okno.title("Підключення до сервера")
okno.geometry("600x450")

CTkLabel(okno, text="IP сервера:").pack(pady=5)
entry_ip = CTkEntry(okno)
entry_ip.pack(pady=5)

CTkLabel(okno, text="Порт:").pack(pady=5)
entry_port = CTkEntry(okno)
entry_port.pack(pady=5)

CTkLabel(okno, text="Нікнейм:").pack(pady=5)
entry_nick = CTkEntry(okno)
entry_nick.pack(pady=5)

CTkButton(okno, text="Підключитися", command=gett,width=100,height=28).pack(pady=10)

okno.mainloop()
pygame.init()
client = socket(AF_INET,SOCK_STREAM)
client.connect(("localhost",2010))
win_width = 1200
win_height = 700
window = pygame.display.set_mode((win_width, win_height))
clock = pygame.time.Clock()

class Ball():
    def __init__(self,x,y,color,radius):
        self.x = x
        self.y = y
        self.color = color
        self.radius = radius
        self.speed_x = 10
        self.speed_y = 10
        self.rect = pygame.Rect(self.x,self.y,self.radius*2,self.radius*2)
    def risovka(self):
        pygame.draw.circle(window,self.color,(self.rect.x,self.rect.y),self.radius)
    def reset2(self,text):
        self.rect = pygame.Rect(self.x,self.y,self.radius*2,self.radius*2)
        pygame.draw.circle(window,self.color,(self.rect.x+self.radius,self.rect.y+self.radius),self.radius)
        font = pygame.font.Font(None,self.radius*2)
        kartinka_texta = font.render(text,1,(0,0,255))
        window.blit(kartinka_texta,(self.rect.x,self.rect.y))
pygame.time.delay(1)
prinyat_sms = client.recv(1024).decode()
prinyat_sms=prinyat_sms.split(",")
# print(int(prinyat_sms[0]),int(prinyat_sms[1]),int(prinyat_sms[2]),int(prinyat_sms[3]))
my_id = int(prinyat_sms[0])
my_x = int(prinyat_sms[1])
my_y = int(prinyat_sms[2])
my_rad = int(prinyat_sms[3])
global vragi
vragi = []
def obmen():
    
    while 1:
        global vragi
        try:
            
            danni = client.recv(1024).decode()
            danni = danni.strip("|").split("|")
            vragi = []
            for eneme in danni:
                danni2 = eneme.split(",")
                nik = danni2[4]
                danni2 = list(map(int,danni2[:4]))# берем все кроме имени
                danni2.append(nik)
                vragi.append(danni2)
                
        except:
            pass
Thread(target=obmen).start()
spisok = []
for _ in range(5000):
    eda = Ball(randint(-2000,2000),randint(-2000,2000),(randint(0,255),randint(0,255),randint(0,255)),randint(10,40))
    spisok.append(eda)


input_pole = pygame.Rect(0,0,300,100)




ball = Ball(600,350,(255,0,0),my_rad)
image_name_user = " "
enter_name = "ввід"
font = pygame.font.SysFont(None,ball.radius*2)
dla_nika = True
nik = " "
finish =True
game = 1
# while 1:
#     window.fill((255,255,255))
    # for e in pygame.event.get():
    #     if e.type == pygame.QUIT:
    #         game = 0
    #         pygame.quit()
    #     elif e.type == pygame.KEYDOWN:
    #         if e.key == pygame.K_BACKSPACE:
    #             nik = nik[0:-1]
    #         else:
    #             nik += e.unicode
    #         if e.key == pygame.K_RETURN:
    #             finish = False
    #             enter_name = "не ввід"
                
                
    # pygame.draw.rect(window,(0,0,0),input_pole,4)
    # image_name_user = font.render(nik,True,(0,0,0))
    # window.blit(image_name_user,input_pole )
    # input_pole.w = image_name_user.get_width()+10
    # if image_name_user != " " :
    #     print(1)
    #     break





while game:
    window.fill((255,255,255))
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            game = 0
            pygame.quit()
        elif e.type == pygame.KEYDOWN:
            
            if enter_name == "ввід":
                if e.key == pygame.K_BACKSPACE:
                    nik = nik[0:-1]
                else:
                    nik += e.unicode
                if e.key == pygame.K_RETURN:
                    finish = False
                    enter_name = "не ввід"
                
    # ввод імені
    # pygame.draw.rect(window,(0,0,0),input_pole,4)
    # image_name_user = font.render(nik,True,(0,0,0))
    # window.blit(image_name_user,input_pole )
    # input_pole.w = image_name_user.get_width()+10
    
    if enter_name == "ввід":
            pygame.draw.rect(window,(0,0,0),input_pole,4)
            image_name_user = font.render(nik,True,(0,0,0))
            window.blit(image_name_user,input_pole )
            input_pole.w = image_name_user.get_width()+10
    
    if finish == False:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            for eda in spisok:
                eda.rect.x +=5
            my_x -=5
        if keys[pygame.K_RIGHT]:
            for eda in spisok:
                eda.rect.x +=-5
            my_x +=5
        if keys[pygame.K_DOWN]:
            for eda in spisok:
                eda.rect.y +=-5
            my_y +=5
        if keys[pygame.K_UP]:
            for eda in spisok:
                eda.rect.y +=5
            my_y -=5
        ball.reset2(nik)
        for i in spisok:
            if ball.rect.colliderect(i):
                if ball.radius > i.radius:
                    spisok.remove(i)
                    if ball.radius < 170:
                        ball.radius += 1
                        ball.rect.x -=1
                        ball.rect.y -=1
                    
                if ball.radius < i.radius:
                    i.risovka()
            else:
                i.risovka()
        

        # if image_name_user != "": ТУТ БУЛО КРІПЛЕННЯ ІМЕНІ
        #     ball.reset2(image_name_user)
            #window.blit(image_name_user,(win_width/2,win_height/2))
        
        try:

            client.send(f"{my_id},{my_x},{my_y},{ball.radius},Ярик".encode())
        except:
            # pygame.quit()
            pass

        for eneme in vragi:
            sdvigx = int((eneme[1] - my_x) + win_width//2)
            sdvigy = int((eneme[2] - my_y) + win_height//2)
            enemy = Ball(sdvigx,sdvigy,(0,0,0),eneme[3])
            if ball.rect.colliderect(enemy):
                if ball.radius < enemy.radius:
                    
                    client.send(f"loose".encode())
                
                    
                    game = 0
                    pygame.quit()
                elif ball.radius > enemy.radius:
                    #ball.radius += 1
                    vragi.remove(eneme)
            else:
                enemy.reset2(eneme[4])

    pygame.display.update()
    clock.tick(60)