import pygame
import math 
import os 
import random
pygame.init()



GAMEINFO = "The bathtub is being invaded by Germs!  YOU MUST GET RID OF THEM BEFORE THEY GET RID OF YOU"
USER_CONTROLS = "W A S D = Move  Mouse = Aim  MouseClick = Shoot"
INFO = "You can collect speed,immunity, and bullet power ups by finding them around the bathroom."
print(INFO)
print(GAMEINFO)
print(USER_CONTROLS)
user_start = input("Press Enter To Continue")

  
W = 1000
H = 1000
screen = pygame.display.set_mode((W,H))


BASE_DIR = os.path.dirname(__file__)
IMAGE_DIR = os.path.join(BASE_DIR, "Images")

soapBase = pygame.image.load(os.path.join(IMAGE_DIR, "soap.jpg")).convert_alpha()
soapBase = pygame.transform.smoothscale(soapBase, (64, 64))
germImg = pygame.image.load(os.path.join(IMAGE_DIR,"Germ.png")).convert_alpha()
germImg = pygame.transform.smoothscale(germImg, (64, 64))
logoImg = pygame.image.load(os.path.join(IMAGE_DIR, "Logo.png" )).convert_alpha()
logoImg = pygame.transform.scale(logoImg, (W/2, H/2))
logorect = logoImg.get_rect(center=(500, 300))
healthImg = pygame.image.load(os.path.join(IMAGE_DIR, "health.png")).convert_alpha()
healthImg = pygame.transform.smoothscale(healthImg, (100,100))


BULLET_R_NORMAL = 10
BULLET_R_BIG = 25
UPGRADERADIOUS = 50
maxGerm = 5
germs = []
bullets = []
BULLET_SPEED = 15
upgrades = []
start_button = pygame.Rect(W//2 - 100, H//2 + 200, 200, 80)
game = False
quacks = []
sadquacks = []
score = 0
font = pygame.font.Font(None, 28)
clock = pygame.time.Clock()
screen.fill((179, 179, 179))
germLevel = 1
MIN_SPAWN_DISTANCE = 500



"""Grid Background"""
def draw_grid(surf, cam_x, cam_y, spacing=80):
    start_x = - (cam_x % spacing)
    start_y = - (cam_y % spacing)

    x = start_x
    while x < W:
        pygame.draw.line(surf, (230,230,230), (x,0), (x,H))
        x += spacing

    y = start_y
    while y < H:
        pygame.draw.line(surf, (230,230,230), (0,y), (W,y))
        y += spacing



"""Enemy Class"""
class Germ:
    def __init__(self,x,y, speed):
        self.x = x
        self.y = y
        self.speed = speed
        self.r = 64
        pass
    def movePlayer(self,player):
        dx = player.x - self.x
        dy = player.y - self.y
        dist = (dx*dx + dy*dy) ** 0.5
        if dist != 0:
            dx /= dist
            dy /= dist
        self.x += dx * self.speed
        self.y += dy * self.speed
    def draw(self,screen,cam_x,cam_y):
        sx = self.x - cam_x
        sy = self.y - cam_y
        screen.blit(germImg, (sx - 32, sy - 32))


def spawn_germ(min_dist, speed_mult):
    while True:
        x = random.randint(-600, 600)
        y = random.randint(-600, 600)

        dx = x - player.x
        dy = y - player.y

        if dx*dx + dy*dy >= min_dist * min_dist:
            return Germ(x, y, germSpeed + speed_mult)

class Player:
    def __init__(self,facing,speed):
        self.upgrade = []
        self.x = 0
        self.y = 0
        self.r = 25
        self.speed = speed
        self.health = 3
    
    def move(self, keys):
        dx = 0
        dy = 0
        if keys[pygame.K_a]: dx -= 1
        if keys[pygame.K_d]: dx += 1
        if keys[pygame.K_w]: dy -= 1
        if keys[pygame.K_s]: dy += 1
    
        if dx != 0 or dy != 0:
            length = (dx*dx + dy*dy) ** 0.5
            dx /= length
            dy /= length

        self.x += dx * self.speed
        self.y += dy * self.speed
        

        
        pass


player = Player(0, 10)
cam_x = player.x - W/2
cam_y = player.y - H/2

"""Initial Germ Spawn"""
for _ in range(5):
    germChance = random.randint(1,10)
    if 0<= germChance <=5:
        germSpeed = 2
    elif 5<germChance<=7:
        germSpeed = 3
    else:
        germSpeed = 5

    germs.append(
        Germ(
            random.randint(-600, 600),
            random.randint(-600, 600),
            germSpeed
        )
    )




upgrades.append({
    "Used": True,
    "Timer": 360,
    "Type": "Immunity",
    "x": random.randint(50,1000),
    "y": random.randint(50,1000)
})




"""Main Menu"""
while not game:
    pygame.draw.rect(screen, (0, 200, 0), start_button, border_radius=10)

    text = font.render("START", True, (0, 0, 0))
    text_rect = text.get_rect(center=start_button.center)
    

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if start_button.collidepoint(event.pos):
                game = True 
    
    screen.fill((255,255,255))
    screen.blit(text, text_rect)
    screen.blit(logoImg,(logorect))

    pygame.draw.rect(screen, (255, 220, 0), start_button, border_radius=12)

   
    pygame.draw.rect(screen, (180, 140, 0), start_button, 4, border_radius=12)

    text = font.render("START", True, (0, 0, 0))
    text_rect = text.get_rect(center=start_button.center)
    screen.blit(text, text_rect)

    pygame.display.flip()
    clock.tick(60)

    
"""Main Game Loop"""
while game:
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():

        keys = pygame.key.get_pressed()
        
        mousex,mousey = pygame.mouse.get_pos()
        if event.type == pygame.QUIT:
            game = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            quacks.append({
                "x": player.x,
                "y": player.y - 40,   
                "alpha": 255
            })


            mouse_world_x = mx + cam_x
            mouse_world_y = my + cam_y

            
            dx = mouse_world_x - player.x
            dy = mouse_world_y - player.y

        
            distance = (dx*dx + dy*dy) ** 0.5
            if distance != 0:
                dx /= distance
                dy /= distance

            bullets.append({
                "x": player.x,
                "y": player.y,
                "vx": dx * BULLET_SPEED,
                "vy": dy * BULLET_SPEED,
                "distance": 0
            })


    
    player.move(keys)
    cam_x = player.x - W/2
    cam_y = player.y - H/2
    
    screen.fill((255,255,255))
    draw_grid(screen, cam_x, cam_y)

    

    for germ in germs:
        germ.movePlayer(player)

    i = -1
    germCount = 0
    for germ in germs:
        germCount +=1
        germ.draw(screen, cam_x, cam_y)


    if germCount < maxGerm:

        germs.append(spawn_germ(MIN_SPAWN_DISTANCE, germLevel))


    """Bullet Detection and collision"""
    for bullet in bullets:
        bullet["x"] += bullet["vx"]
        bullet["y"] += bullet["vy"]

    for bullet in bullets:
        i +=1
        sx = bullet["x"] - cam_x
        sy = bullet["y"] - cam_y
        bullet["distance"] = bullet["distance"] + 1
        screen.blit(soapImg, (sx - soap_half, sy - soap_half))

        if bullet["distance"] >= 100:
            bullets.pop(i)

        for germ in germs[:]:
            dx = bullet["x"] - germ.x
            dy = bullet["y"] - germ.y
            bullet_r = BULLET_R_BIG if "BiggerBullets" in player.upgrade else BULLET_R_NORMAL

            if dx*dx + dy*dy <= (germ.r + bullet_r) * (germ.r + bullet_r):
                if "BiggerBullets" not in player.upgrade:
                    bullets.remove(bullet)
                germs.remove(germ)
                score += 1
                break
    if "Immunity" not in player.upgrade:
        for germ in germs[:]:
            dx = player.x - germ.x
            dy = player.y - germ.y
            if dx*dx + dy*dy <= germ.r * germ.r:
                    player.health-=1
                    player.upgrade = []
                    player.upgrade.append("Immunity")
                    upgrades.append({
                        "Used": True,
                        "Timer": 120,
                        "Type": "Immunity",
                        "x": random.randint(50,1000),
                        "y": random.randint(50,1000)
                    })
                    
            
                    sadquacks.append({
                        "x": player.x,
                        "y": player.y - 40,   
                        "alpha": 255
                    })
    
    pygame.draw.circle(screen, (252,232,3), (W//2, H//2), player.r)


    """Upgrade Drawing and collision"""

    for upgrade in upgrades[:]:
        if upgrade["Type"] == "Immunity":
                upgradeColor = (46, 189, 255)
        elif upgrade["Type"] == 'Speed':
            upgradeColor = (255, 0, 0)
        elif upgrade["Type"] == "BiggerBullets":
            upgradeColor = (245, 66, 212)
    
        if upgrade["Used"]:
            upgrade["Timer"] -= 1
            if upgrade["Type"] not in player.upgrade:
                player.upgrade.append(upgrade["Type"])
            pygame.draw.circle(screen,(upgradeColor), (W//2, H//2), player.r, 5)
            



        else:
            sx = upgrade["x"] - cam_x
            sy = upgrade["y"] - cam_y
           
            pygame.draw.circle(screen, (upgradeColor), (sx, sy), 50)
            text_surf = font.render(str(upgrade["Type"]), True, (0, 0, 0))

            text_rect = text_surf.get_rect(center=(sx, sy))
            screen.blit(text_surf, text_rect)
            dx = player.x - upgrade['x']
            dy = player.y - upgrade['y']
            if dx*dx + dy*dy <= UPGRADERADIOUS * UPGRADERADIOUS:
                upgrade["Used"] = True
                upgrade["x"] = 100000000
                upgrade["y"] = 100000000
        if upgrade["Timer"] <= 0:
            if upgrade["Type"] in player.upgrade:
                player.upgrade.remove(upgrade["Type"])
            upgrade["Used"] = False
            upgrade["Timer"] = 120
            upgrades.remove(upgrade)
    

    if len(player.upgrade) == 0 and len(upgrades) == 0:
        upgradeTime = 120
        typeOfUpgrade = random.randint(1,3)
        if typeOfUpgrade == 1:
            typeOfUpgrade = "Immunity"
        elif typeOfUpgrade == 2:
            typeOfUpgrade = "Speed"
        elif typeOfUpgrade == 3:
            typeOfUpgrade = "BiggerBullets"
            upgradeTime = 360
        upgrades.append({
            "Used": False,
            "Timer": upgradeTime,
            "Type": typeOfUpgrade,
            "x": random.randint(-600, 600),
            "y": random.randint(-600, 600)
        })

    if "Speed" in player.upgrade:
        player.speed  = 20
    else:
        player.speed = 10
    
    if "BiggerBullets" in player.upgrade:
        soapImg = pygame.transform.smoothscale(soapBase, (96, 96))
        soap_half = 48
    else:
        soapImg = soapBase
        soap_half = 32

    germcalc = score/5
    if germcalc < 1:
        germcalc = 1
    
        germcalc = 2
        
    germLevel = germcalc
    maxGerm = 5 + germcalc
   



    """Quack On Click Effect"""
    for q in quacks[:]:
    
        sx = q["x"] - cam_x
        sy = q["y"] - cam_y

        text = font.render("QUACK", True, (0, 0, 0))
        text.set_alpha(q["alpha"])
        screen.blit(text, text.get_rect(center=(sx, sy)))

        q["alpha"] -= 5
        if q["alpha"] <= 0:
            quacks.remove(q)

    for q in sadquacks[:]:
    
        sx = q["x"] - cam_x
        sy = q["y"] - cam_y

        text = font.render("quack... :(", True, (0, 0, 0))
        text.set_alpha(q["alpha"])
        screen.blit(text, text.get_rect(center=(sx, sy)))

        q["alpha"] -= 5
        if q["alpha"] <= 0:
            sadquacks.remove(q)

    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))
    heart_w = healthImg.get_width()
    padding = 10

    for i in range(player.health):
        x = W - padding - (i + 1) * (heart_w + 6)
        y = 10
        screen.blit(healthImg, (x, y))
    if player.health <= 0:
        game = False
    pygame.display.flip()
    clock.tick(60)
    

screen.fill((0, 0, 0))  

final_text = font.render(f"FINAL SCORE: {score}", True, (255, 0, 0))
final_rect = final_text.get_rect(center=(W//2, H//2 - 30))
screen.blit(final_text, final_rect)

exit_text = font.render("Press ENTER to exit", True, (255, 0, 0))
exit_rect = exit_text.get_rect(center=(W//2, H//2 + 30))
screen.blit(exit_text, exit_rect)

pygame.display.flip()

waiting = True
while waiting:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                pygame.quit()
                exit()

    