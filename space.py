# Save this file as something meaningful!
# Unless you want your game to be callled skeleton...

import pygame
from pygame.math import Vector2
from random import randint
import random
# Setup
pygame.init()

WHITE = (255, 255, 255)
RED =   (255,   0,   0)
BLACK = (  0,   0,   0)

# Screen
size = [400, 700]
screen = pygame.display.set_mode(size)

# Objects and variables
done = False
game_over = False
clock = pygame.time.Clock()
x_speed = 0
y_speed = 0
small_font = pygame.font.SysFont("Arial", 12)
hit_count = 0
# timer
class End_Screen(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        #self.speed = vector2(0, 0)

        self.image = pygame.image.load('End.png')
        self.image = pygame.transform.scale(self.image,(200, 400))

        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = 100

class Down(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        #self.speed = vector2(0, 0)

        self.image = pygame.Surface((400, 20))
        self.image.fill(RED)
        self.image.set_colorkey(WHITE)

        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 680


class Laser(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.speed = Vector2(0, -20)

        self.image = pygame.Surface((3, 15))
        self.image.fill(WHITE)
        self.image.set_colorkey(WHITE)
        pygame.draw.line(self.image,RED, (1,0),(1,15), 3)

        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0

    def update(self):
        self.rect.y += self.speed.y
        self.rect.x += self.speed.x
        if self.rect.bottom <0:
            self.kill()

class Alien(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.speed = Vector2(0, 6)

        self.image = pygame.image.load('UFO.png')
        self.image = pygame.transform.scale(self.image,(50, 33))

        self.rect = self.image.get_rect()
        self.rect.x = 175
        self.rect.y = -50


    def update(self):
        self.rect.y += self.speed.y
        self.rect.x += self.speed.x

class Heart(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)

        self.speed = Vector2(0, 0)

        self.image = pygame.image.load('Heart.png')
        self.image = pygame.transform.scale(self.image,(39, 30))

        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x

    def update(self):
        self.rect.y += self.speed.y
        self.rect.x += self.speed.x



# Make Ship a subclass of Sprite.
# This means that all the operations that the Sprite class has will be
# something that the Ship class can do.
# We say "Ship inherits from Sprite"
class Ship(pygame.sprite.Sprite):
    # All classes must have an __init__ method.
    # All data that a class uses must be initialised in the __init__ method.
    # Each data element is called a field.
    def __init__(self):
        # First make sure the base class is initialised.
        pygame.sprite.Sprite.__init__(self)

        # This ship will have a speed as internal data as a Vector2, which
        # set to (0,0) initially.
        self.speed = Vector2(0, 0)

        # Spirtes should have an image field. In this caes we load the image
        # from a file on disk and scale it so it is suitable for our screen.
        self.image = pygame.image.load('Ship Ne.png')
        self.image = pygame.transform.scale(self.image, (60, 70))

        # pygame uses the rect field of a Spirte to draw the Sprite, but also
        # to calculate collisions so we have to initialise it.
        # We take the rect from the image field and then we change the x and y
        # fields of the rect in order to place the Ship on the right spot on the
        # screen.
        self.rect = self.image.get_rect()
        self.rect.x = 175
        self.rect.y = 600

    # The update method of the Sprite class doesn't do anything. The purpose of
    # it is to provide a hook for you to provide a way to update your class in
    # a way that fits with the basic features of pygame.
    # In this caes we just move the rect with the coordinates of the speed vector.
    def update(self):
        self.rect.x += self.speed.x
        self.rect.y += self.speed.y

        if self.rect.left <0:
            self.rect.left = 0

        if self.rect.right >400:
            self.rect.right = 400

# Create Objects
# All the objects to be on the screen when the game starts.
End = End_Screen()
Bottom = Down()
player_ship = Ship()
enemy = Alien()
life_1 = Heart(351, 10)
life_2 = Heart(302, 10)
life_3 = Heart(253, 10)
lifes = 3
# Handle sprites
# Create as many Sprite groups as you need to make things easy to manage.
# all_sprites contains all the objects we'll ever create. All objects must be
# added to the all_sprites Group for things to work.
all_sprites = pygame.sprite.Group()
all_sprites.add(Bottom)
all_sprites.add(player_ship)
all_sprites.add(enemy)
all_sprites.add(life_1)
all_sprites.add(life_2)
all_sprites.add(life_3)
all_bullets = pygame.sprite.Group()
all_comets = pygame.sprite.Group()
Game_over = pygame.sprite.GroupSingle(End)
player = pygame.sprite.GroupSingle(player_ship)
The_Botton = pygame.sprite.GroupSingle(Bottom)
all_comets.add(enemy)

def new_alien():
    enemy = Alien()
    enemy.rect.x = random.randint(30, 350)
    all_sprites.add(enemy)
    all_comets.add(enemy)


def add_alien(hits, kills):
    if kills >0:
        for i in range(kills):
            new_alien()
        if hits == 10:
            new_alien()
        if hits == 20:
            new_alien()
        if hits == 30:
            new_alien()

# -------- Main Program Loop -----------
# we use the global variable done to control when to end the game.
while not done:


    # --- Event Processing
    # Get all events from keyboard and/or mouse.
    for event in pygame.event.get():
        # if you click the x in the window top the game will end
        if event.type == pygame.QUIT:
            done = True

        # if you press a key and it is either A or D change the speed of
        # the x_speed variable.
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                x_speed = -6
            elif event.key == pygame.K_d:
                x_speed = +6
            elif event.key == pygame.K_SPACE:
                bullet = Laser()
                all_bullets.add(bullet)
                print(all_bullets)
                all_sprites.add(bullet)
                bullet.rect.x = player_ship.rect.centerx - 1
                bullet.rect.y = player_ship.rect.top


        # When the A or D  key is released change the x_speed to 0.
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                x_speed = 0
            elif event.key == pygame.K_d:
                x_speed = 0

    # --- Game Logic
    # Update variables
    player_ship.speed.x = x_speed
    all_sprites.update()



    # Collisions
    # Read the documentation of groupcollide very carefully and figure out
    # how the arguments work.
    hit_list = pygame.sprite.groupcollide(all_comets, all_bullets, True, True)
    hit_count += len(hit_list)
    add_alien(hit_count, len(hit_list))


    past_by = pygame.sprite.groupcollide(The_Botton, all_comets, False, True)
    if len(past_by)>0:
        if lifes == 3:
            all_sprites.remove(life_3)
            lifes -= 1
            new_alien()
        elif lifes == 2:
            all_sprites.remove(life_2)
            lifes -= 1
            new_alien()
        elif lifes == 1:
            all_sprites.remove(life_1)
            lifes -= 1
            game_over = True


    hit_by = pygame.sprite.groupcollide(player, all_comets, False, True)
    if len(hit_by)>0:
        if lifes == 3:
            all_sprites.remove(life_3)
            lifes -= 1
            new_alien()
        elif lifes == 2:
            all_sprites.remove(life_2)
            lifes -= 1
            new_alien()
        elif lifes == 1:
            all_sprites.remove(life_1)
            lifes -= 1
            game_over = True


    # --- Draw
    # When using Sprite groups it is super easy to update the screen:
    # 1. Clear the screen.
    # 2. Call the draw method of the all_sprites Group using the screen as the
    #    only argument.
    screen.fill(WHITE)
    all_sprites.draw(screen)

    hit_text = small_font.render("Hits: " + str(hit_count), 1, BLACK)
    screen.blit(hit_text, (10, 10))

    if game_over == True:
            Game_over.draw(screen)


    # Update screen
    # pygame will draw the screen in the background and only when it is time
    # to update it will it be shown on the screen.
    clock.tick(30)  # update the screen 30 times every second.
    pygame.display.flip()
    # print(player_ship.rect.left)


# When we break out of the gmae loop there is nothing to do but..
# Close the window and quit.
pygame.quit()
