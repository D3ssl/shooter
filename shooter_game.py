from pygame import *
from random import randint
from time import time as timer

#класс Player

class GameSprite(sprite.Sprite):
    def __init__(self, img, player_x, player_y, player_speed, w, h):
        super().__init__()
        self.image = transform.scale(image.load(img),(w,h))
        self.speed = player_speed 
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        

    def reset(self):
        window.blit(self.image,(self.rect.x,self.rect.y))

class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()       
        if keys_pressed[K_a] and self.rect.x > 5:
            self.rect.x -= 10
        if keys_pressed[K_d] and self.rect.x < 625:
            self.rect.x += 10
    def fire(self):
        bullet = Bullet("bullet.png", self.rect.centerx,self.rect.top,10,15,25)
        bullets.add(bullet)
lost = 0 #счетчик пропущенных нло
score = 0 #счетчик уничтоженных нло
class Enemy(GameSprite):
    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y > h:
            self.rect.x = randint(5,630)
            self.rect.y = 0
            lost += 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

font.init()       
font1 = font.SysFont('Arial',30)
font2 = font.SysFont('Arial',70)
font3 = font.SysFont('Arial',50)
#создаем окно и называем
w = 700
h = 500
run = True
finish = False
clock = time.Clock()
FPS = 60
window = display.set_mode((w,h))
display.set_caption("Шутер")
#создание заднего фона
bg = transform.scale(image.load('galaxy.jpg'),(w,h))
#подключение музыки
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
kick = mixer.Sound('fire.ogg')

#создание спрайтов
rocket = Player('rocket.png',315,395,10,65,100)
num_fire = 0
rel_time = False
monsters = sprite.Group()
bullets = sprite.Group()
asteroids = sprite.Group()
for i in range(1,6):
    monster = Enemy('ufo.png', randint(5,630), 0, randint(2,4), 80 ,45)
    monsters.add(monster)

for i in range(1,4):
    asteroid = Enemy('asteroid.png',randint(5,630),0, randint(2,3),45,50)
    asteroids.add(asteroid)
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                    rocket.fire()
                    kick.play()
                    num_fire += 1
                if num_fire >= 5 and rel_time == False:
                    rel_time = True
                    last_time = timer()
                    
                
                    
    
    
    if finish != True:
        window.blit(bg,(0,0))
        score_text = font1.render("Счет: " + str(score),1,(255,255,255))
        window.blit(score_text,(10,10))
        lose_text = font1.render('Пропущено: ' + str(lost),1,(255,255,255))
        window.blit(lose_text,(10,45))
        rocket.reset()
        rocket.update()


        monsters.draw(window)
        monsters.update()

        bullets.draw(window)
        bullets.update()

        asteroids.draw(window)
        asteroids.update()

        #перезарядка
        if rel_time == True:
            now_time = timer()
            if last_time - now_time < 3:
                kd_text = font3.render('wait, reload...',1,(255,0,0))
                window.blit(kd_text,(350,450))
            else:
                num_fire = 0
                rel_time = False

            

        
        #проверка столкновения пули и монстра
        list1 = sprite.groupcollide(bullets,monsters,True,True)
        for l in list1:
            score += 1
            monster = Enemy('ufo.png', randint(5,630), 0, randint(2,4), 80 ,45)
            monsters.add(monster)


        #проверка столкновения игрока и монстров 
        if sprite.spritecollide(rocket,monsters,False) or sprite.spritecollide(rocket,asteroids,False) or lost >= 3:
            finish = True
            lose = font2.render("YOU LOSE!",True,(255,0,0))
            window.blit(lose,(220,250))
            kick.play()



       
        

        #проверка выйгрыша
        if score >= 10:
            finish = True
            win = font2.render("YOU WIN!",True,(0,255,0))
            window.blit(win,(220,250))


        

        

        
        
        

        
    display.update()
    clock.tick(FPS)
