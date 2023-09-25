import pygame
import math
import random

BLUE = (20, 30, 255)
WHITE = (255, 255, 255)

class Mouse(pygame.sprite.Sprite):
    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load('cursor.png'), (50, 35))
        self.rect = pygame.Rect(0, 0, 0, 0)

class Weapon(pygame.sprite.Sprite):
    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load('weapon.png'), (100, 100))
        self.rect = self.image.get_rect()
        self.rect.topleft = position

    def draw(self):
        screen.blit(self.image, self.rect)
    
    def shoot(self,angle,a,b):
        bullet = Bullet(500, self.rect.top,angle,a, b)
        all_sprites.add(bullet)
        bullets.add(bullet)

class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load('aim.jpeg'), (60, 40))
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(-150, 0)
        self.rect.y = random.randrange(50, 300)
        self.speedy = random.randrange(-2,2)
        self.speedx = random.randrange(3,9)
    
    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > 800 + 10  < -25 or self.rect.right > 1200 + 20:
            self.rect.x = random.randrange(-100, 0)
            self.rect.y = random.randrange(50, 300)
            self.speedy = random.randrange(-1,1)
            self.speedx = random.randrange(3,5)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, angle, a,b):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 50))
        self.image = pygame.transform.scale(pygame.image.load('bullet.png'), (20, 10))
        self.rect = self.image.get_rect()
        self.rect.y= y
        self.rect.x = x
        self.speed = 40
        self.speedx = 0
        self.speedy = 0
        self.speedx = (self.speed * math.cos(angle/57.2))
        self.speedy = (self.speed * math.sin(angle/57.2))
      
    def update(self):
        self.rect.x += self.speedx
        self.rect.y -= self.speedy
        if self.rect.y < 0 or self.rect.x > 1000:
            self.kill()       

pygame.init()
win_pic = pygame.transform.scale(pygame.image.load('victory.jpg'), (1000, 500))
screen = pygame.display.set_mode((1000, 500))
clock = pygame.time.Clock()
mouse = Mouse((0, 0))
weapon = Weapon((500, 450))
all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()
all_sprites.add(bullets)

for i in range(5):
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)
   
otstup = pygame.math.Vector2(10, 10)
k = 0
running = [True]
while running:
        if k < 15:
            screen.fill(WHITE)
            mouse_pos = pygame.mouse.get_pos()
            mouse.rect.x = mouse_pos[0]
            mouse.rect.y = mouse_pos[1]
            pygame.mouse.set_visible(0)
            b = mouse.rect.x + 68
            a = mouse.rect.y + 68
            delx = b - 500
            dely = 500 - a
            cos = delx / ((math.sqrt(math.pow(dely , 2) + math.pow(delx , 2))) + 0.01)
            sin = dely / ((math.sqrt(math.pow(dely , 2) + math.pow(delx , 2))) + 0.01)
            angle = (((math.acos(cos))*57.2)) 

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        weapon.shoot(angle, a, b)
            
            all_sprites.update()
            weapon_image = pygame.transform.rotozoom(weapon.image, angle-90, 1)
            weapon_otstup = otstup.rotate(-angle)
            weapon_rect = weapon_image.get_rect(center=(500, 450) + weapon_otstup)
            hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
            for hit in hits:
                m = Mob()
                all_sprites.add(m)
                mobs.add(m)
                k += 1
            screen.blit(mouse.image, mouse.rect)
            all_sprites.draw(screen)
            screen.blit(weapon_image, weapon_rect)  
        else:
            screen.blit(win_pic, (0, 0))
        pygame.display.flip()              
        clock.tick(24)
            
        


pygame.quit ()
