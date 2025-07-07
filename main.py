import pygame
from os.path import join
from random import randint, uniform

class Window:
    def __init__(self):
        self.width = 1280
        self.height = 720
class Player(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)

        # variables
        self.image = pygame.image.load(join('images', 'player.png')).convert_alpha()
        self.rect = self.image.get_frect(center = (window.width / 2, window.height / 2))
        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 500

        # cooldown
        self.canShoot = True
        self.laserShootTime = 0
        self.cooldownDuration = 400


        # get the laser timer
    def laserTimer(self):
        if not self.canShoot:
            currentTime = pygame.time.get_ticks()
            if currentTime - self.laserShootTime >= self.cooldownDuration:
                self.canShoot = True

    def update(self, dt):
        # check the direction and puts it into the vector
        self.direction.x = int(keys[pygame.K_d]) - int(keys[pygame.K_a])
        self.direction.y = int(keys[pygame.K_s]) - int(keys[pygame.K_w])

        # turns the diagonal vector into a magnitude of 1
        if self.direction:
            self.direction = self.direction.normalize()
        
        # move player
        self.rect.center += self.direction * self.speed * dt
        
        # keep player within screen bounds
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > window.width:
            self.rect.right = window.width
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > window.height:
            self.rect.bottom = window.height
            
        self.laserTimer()
        # shoots laser
        if justpressed_keys[pygame.K_SPACE] and self.canShoot:
            Laser(laser, self.rect.midtop, (allSprites, laserSprites))
            self.canShoot = False
            self.laserShootTime = pygame.time.get_ticks()
            laserSound.play()
class Star(pygame.sprite.Sprite):
    def __init__(self, *groups, surf):
        super().__init__(*groups)
        self.image = surf
        # puts star in random pos
        self.rect = self.image.get_frect(center = (randint(0, window.width),randint(0, window.height)))
class Laser(pygame.sprite.Sprite):
    def __init__(self, surf, pos, *groups):
        super().__init__(*groups)
        self.image = surf
        self.rect = self.image.get_frect(midbottom = pos)

    def update(self, dt):
        global explosionFrames
        self.rect.y -= 400 * dt
        for laser in laserSprites:
            if pygame.sprite.spritecollide(laser, meteorSprites, True):
                Explosions(explosionFrames, laser.rect.midtop, allSprites)
                laser.kill()
class Meteor(pygame.sprite.Sprite):

    def __init__(self, surf, pos, group):
        super().__init__(group)
        self.originalsurf = surf
        self.image = self.originalsurf
        self.rect = self.image.get_frect(center = (randint(0, window.width), randint(-200, -100)))
        self.direction = pygame.math.Vector2(uniform(-0.5, 0.5), 1)
        self.speed = 300
        self.rotationSpeed = randint(40, 100)
        self.rotation = 0
        self.image = pygame.transform.rotate(self.image, randint(0, 360))
    
    def update(self, dt):
        
        self.rect.center += self.direction * self.speed * dt
        if self.rect.top > window.height:
            self.kill()
        self.rotation += self.rotationSpeed * dt
        self.image = pygame.transform.rotozoom(self.originalsurf, self.rotation, 1)
        self.rect = self.image.get_frect(center = self.rect.center)

class Explosions(pygame.sprite.Sprite):
    def __init__(self, frames, pos, *groups):
        super().__init__(*groups)
        self.image = frames[0]
        self.rect = self.image.get_frect(center = pos)
        self.frames = frames
        self.frame = -1
        explosionSound.play()
    
    def update(self, dt):
        if self.frame <= 20:
            self.image = self.frames[int(self.frame)]
            self.frame += 50 * dt
        else:
            self.kill()


def update():
    allSprites.draw(screen)
    pygame.display.update()

def displayScore():
    currentTime = pygame.time.get_ticks() // 1000
    textSurf = font.render(str(currentTime), True, (240, 240, 240))
    textRect = textSurf.get_frect(midbottom = (window.width // 2, window.height - 50))
    margin = 10
    marginVector = pygame.math.Vector2(margin, -margin)
    pygame.draw.rect(screen, (240,240,240), textRect.inflate(30, 10).move(0, -10), 5, 10)
    screen.blit(textSurf, textRect)
    

# setup
pygame.init()
pygame.font.init()
pygame.mixer.init()
font = pygame.font.Font(join('images', 'Oxanium-Bold.ttf'), 50)
window = Window()
bgColor = (143, 133, 133)
screen = pygame.display.set_mode((window.width, window.height))
running = True
clock = pygame.time.Clock()

# sprites initialization
allSprites = pygame.sprite.Group()
meteorSprites = pygame.sprite.Group()
laserSprites = pygame.sprite.Group()
endScreenSprites = pygame.sprite.Group()
starSurface = pygame.image.load(join('images', 'star.png')).convert_alpha()
for i in range(20):
    Star(allSprites, surf=starSurface)
player = Player(allSprites)

# img imports
meteorSurf = pygame.image.load(join('images', "meteor.png")).convert_alpha()
laser = pygame.image.load(join('images', 'laser.png')).convert_alpha()
explosionFrames = []
for i in range (21):
    explosionFrames.append(pygame.image.load(join('images', 'explosion', f'{i}.png')).convert_alpha())
print(explosionFrames)

# sound imports
laserSound = pygame.mixer.Sound(join('audio', 'laser.wav'))
laserSound.set_volume(0.2)
explosionSound = pygame.mixer.Sound(join('audio', 'explosion.wav'))
explosionSound.set_volume(0.2)
gameMusic = pygame.mixer.Sound(join('audio', 'game_music.wav'))
gameMusic.set_volume(0.5)
# meteor event
meteorEvent = pygame.event.custom_type()
pygame.time.set_timer(meteorEvent, 200)

gameMusic.play(loops=-1)

while running:
    # variables that will be use throughout
    dt = clock.tick() / 1000
    keys = pygame.key.get_pressed()
    justpressed_keys = pygame.key.get_just_pressed()

    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            running = False
        if event.type == meteorEvent:
            Meteor(meteorSurf, (randint(0, window.width), randint(-200, -100)), (allSprites, meteorSprites))

    # makes the sprites change
    allSprites.update(dt)

    # check collisions
    if pygame.sprite.spritecollide(player, meteorSprites, True, pygame.sprite.collide_mask):
        
        running = False

    # update
    screen.fill(bgColor)
    displayScore()    
    update()

pygame.quit()