import random
import pygame
import time



class Fly(pygame.sprite.Sprite):
    bullets = pygame.sprite.Group()
    def __init__(self,screen):
        pygame.sprite.Sprite.__init__(self)
        self.fly = pygame.image.load("./素材/fly.png")
        self.hp_ph = pygame.image.load("./素材/hearts.png")
        self.rect=self.fly.get_rect()
        self.rect.topleft =[80,150]

        self.hp = 3
        self.hp_height = 3
        self.speed = 5
        self.bullet_type="bullet"
        self.shot_delay=None
        self.last_shot_time = 0
        self.screen = screen
        self.bullets=pygame.sprite.Group()

    def take_damage(self,damage):
        self.hp-=damage
        if self.hp <= 0:
           self.kill()
    def heal(self):
        if self.hp>=self.hp_height:
            self.hp=self.hp_height
        else:
            self.hp+=1

    def change_bullet_type(self,type):
        self.bullet_type=type

    def key_control(self):

        key = pygame.key.get_pressed()
        current_time = pygame.time.get_ticks()

        if key[pygame.K_SPACE]:
            bullet = Bullet(self.screen, self.rect.center, self.bullet_type)
            self.shot_delay = bullet.shot_delay
            if current_time - self.last_shot_time > self.shot_delay:
                Fly.bullets.add(bullet)
                self.bullets.add(bullet)
                self.last_shot_time = current_time

        if key[pygame.K_w] and self.rect.y > -10:
            self.rect.y -= self.speed
        if key[pygame.K_s] and self.rect.y < 430:
            self.rect.y += self.speed
        if key[pygame.K_a] and self.rect.x > 0:
            self.rect.x -= self.speed
        if key[pygame.K_d] and self.rect.x < 925:
            self.rect.x += self.speed


    def display(self):
        self.screen.blit(self.fly,self.rect)
        self.bullets.update()
        self.bullets.draw(self.screen)


    def update(self):
        self.key_control()
        self.display()


class Food_hp(pygame.sprite.Sprite):
    def __init__(self,screen):
        pygame.sprite.Sprite.__init__(self)
        self.hp = pygame.image.load("./素材/hearts.png")
        self.screen = screen
        #位置和碰撞框
        self.rect=self.hp.get_rect()
        self.rect.topleft =[random.randint(500,950),0]
    def display(self):
        self.screen.blit(self.hp, self.rect)

    def update(self):
        self.rect.right-=1
        self.rect.top += 1
        if self.rect.top >= self.screen.get_height():
            self.kill()


class Food_bullet(pygame.sprite.Sprite):
    def __init__(self,screen):
        pygame.sprite.Sprite.__init__(self)
        self.hp = pygame.image.load("./素材/bullet_1.png")
        self.screen = screen
        #位置和碰撞框
        self.rect=self.hp.get_rect()
        self.rect.topleft =[random.randint(500,950),0]
    def display(self):
        self.screen.blit(self.hp, self.rect)

    def update(self):
        self.rect.right-=1
        self.rect.top += 1
        if self.rect.top >= self.screen.get_height():
            self.kill()


class Bullet(pygame.sprite.Sprite):
    def __init__(self,screen,position,type):
        x,y=position
        pygame.sprite.Sprite.__init__(self)
        if type=="bullet":
            self.screen = screen
            self.image=pygame.image.load('./素材/bullet.png')
            self.rect=self.image.get_rect()
            self.rect.topleft=[x+10,y-5]
            self.damage=1
            self.speed=8
            self.shot_delay = 500
        elif type=="bullet_1":
            self.image = pygame.image.load('./素材/bullet_1.png')
            self.rect=self.image.get_rect()
            self.rect=self.image.get_rect()
            self.rect.topleft=[x+20,y-20]
            self.damage = 10
            self.speed = 6
            self.shot_delay = 1500


    def update(self):
         self.rect.left+=self.speed
         if self.rect.left>1000:
            self.kill()


class Enemy(pygame.sprite.Sprite):
    def __init__(self,screen):
        pygame.sprite.Sprite.__init__(self)
        self.fly = pygame.image.load("./素材/enemy.png")
        self.rect = self.fly.get_rect()
        self.rect.topleft=[1000,random.randint(0,430)]
        self.hp = 3
        self.speed = 2
        self.screen = screen


    def display(self):
        self.screen.blit(self.fly, self.rect)
    def update(self):
        self.rect.right -= self.speed


class Boom(object):
    def __init__(self,screen,type):
        self.screen = screen
        if type=="enemy":
           self.mImage =[pygame.image.load("./素材/explosion"+str(v)+".png")for v in range(1,8)]
        elif type=="damage":
            self.mImage =[pygame.image.load("./素材/explosion_damage"+str(v)+".png")for v in range(1,8)]
        else:
            self.mImage=[pygame.image.load("./素材/explosion"+str(v)+".png")for v in range(1,8)]
        self.mIndex = 0
        self.mPos=[0,0]
        self.mVisible=False

    def action(self,rect):
        self.mPos[0]=rect.left-5
        self.mPos[1]=rect.top-5
        self.mVisible=True

    def  draw(self):
        if not self.mVisible:
            return
        self.screen.blit(self.mImage[self.mIndex],self.mPos)
        self.mIndex+=1
        if self.mIndex>=len(self.mImage):
            self.mIndex=0
            self.mVisible=False


class Manager(object):
    def __init__(self):
        pygame.init()
        self.screen =pygame.display.set_mode((1000,500))
        self.background = pygame.image.load("素材/background.jpg")
        #窗口
        self.player = pygame.sprite.GroupSingle()
        self.enemies = pygame.sprite.Group()
        self.food_hp = pygame.sprite.Group()
        self.bullet_1 = pygame.sprite.Group()
        # 实体组
        self.damage_ph = Boom(self.screen, "damage")
        self.player_boom = Boom(self.screen,"player")
        self.enemies_boom = Boom(self.screen,"enemys")
        #爆炸

    #信息附属函数
    def text(self,text,x,y,textHeight=60,fontColor=(0,255,0),backgroundColor=None):
        font=pygame.font.Font(None,textHeight)
        text = font.render(text,True,fontColor,backgroundColor)
        text_rect = text.get_rect()
        text_rect.topleft=(x,y)
        self.screen.blit(text,text_rect)
    def draw_player(self):
        player = self.player.sprite
        i=0
        for i in range(player.hp):
            self.screen.blit(player.hp_ph, (i*50+80, 7))
    #信息函数
    def information(self):
        self.text("HP:",0,10)
        self.draw_player()

    def exit(self):
        pygame.quit()
        exit()

    def new_player(self):
        player=Fly(self.screen)
        self.player.add(player)
        #玩家对象

    def new_enemies(self):
        new_enemies=random.randint(0,100)
        if new_enemies==0:
            enemies = Enemy(self.screen)
            self.enemies.add(enemies)
        #敌机
        #掉落物
    def new_foods(self):
        new_foods=random.randint(0,1000)
        if new_foods==0:
            food_hp=Food_hp(self.screen)
            self.food_hp.add(food_hp)
    def new_buttle_1(self):
        player=self.player.sprite
        if player.bullet_type=="bullet":
            new_foods = random.randint(0, 1000)
            if new_foods == 0:
                bullet_1= Food_bullet(self.screen)
                self.bullet_1.add(bullet_1)

    def main(self):
        self.new_player()
        #调用方法创建实例
        pygame.display.update()
        time.sleep(0.01)
        i = 0
        while True:
                player = self.player.sprite
                self.new_enemies()
                self.new_foods()
                self.new_buttle_1()
                #背景
                i -= 1
                self.screen.blit(self.background, (i, 0))
                self.screen.blit(self.background, (1000 + i, 0))
                if i == -1000:
                    i=0
                #鼠标信号
                for event in pygame.event.get():  # 常用：清晰的 event
                 if event.type == pygame.QUIT:
                     self.exit()
                 if event.type == pygame.KEYDOWN:
                     print(event.key)
                # #碰撞效果
                self.player_boom.draw()
                self.enemies_boom.draw()
                #机机
                if len(self.player) > 0 and len(self.enemies) > 0:
                   ex = pygame.sprite.groupcollide(self.player, self.enemies,False, True)
                   if ex:
                       items=list(ex.items())[0]
                       print(items)
                       x=items[0]
                       y=items[1][0]
                       player.take_damage(1)
                       #self.player_boom.action(x.rect)
                       self.enemies_boom.action(y.rect)
                #弹机
                if len(self.enemies) > 0:
                    is_enemies=pygame.sprite.groupcollide(Fly.bullets, self.enemies,True, False)
                    if is_enemies:
                       bullet,enemies=list(is_enemies.items())[0]
                       items = list(is_enemies.items())[0]
                       y = items[1][0]
                       enemy=enemies[0]
                       damage=bullet.damage
                       enemy.hp-=damage
                       self.damage_ph.action(y.rect)
                       if enemy.hp<=0:
                          self.enemies_boom.action(y.rect)
                          enemy.kill()

                #机血（）
                if len(self.player) > 0 and len(self.food_hp) > 0 :
                    gt_hp=pygame.sprite.groupcollide(self.player, self.food_hp, False, True)
                    if gt_hp:
                        player = self.player.sprite
                        player.heal()
                #机蛋（）
                if len(self.player) > 0 and len(self.bullet_1 ) > 0:
                   bullet = pygame.sprite.groupcollide(self.player, self.bullet_1, False, True)
                   if bullet:
                       player.change_bullet_type("bullet_1")
                self.player.update()
                self.enemies.update()
                self.food_hp.update()
                self.bullet_1.update()

                for enemy in self.enemies:
                 enemy.display()
                for food in self.food_hp:
                    food.display()
                for bullet_1 in self.bullet_1:
                    bullet_1.display()
                self.damage_ph.draw()
                # 信息
                self.information()
                pygame.display.update()
                time.sleep(0.01)#帧率
        #实体显示
if __name__ == '__main__':
    m=Manager()
    m.main()