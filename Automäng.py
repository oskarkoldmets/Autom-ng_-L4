import pygame
import random

# Algseaded
pygame.init()
screen_width = 640
screen_height = 480
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Autode mäng")
clock = pygame.time.Clock()

# Värvid
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Laadime pildid
background_image = pygame.image.load("bg_rally.jpg")
red_car_image = pygame.image.load("f1_red.png")
blue_car_image = pygame.image.load("f1_blue.png")

# Mänguobjektide klassid
class Car(pygame.sprite.Sprite):
    def __init__(self, image, x, y, speed):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = speed

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > screen_height:
            self.rect.y = -self.rect.height
            self.rect.x = random.randint(20, screen_width - 20)

# Tekstiklass skoori kuvamiseks
class Text:
    def __init__(self, text, size, x, y, color):
        self.font = pygame.font.SysFont(None, size)
        self.text = text
        self.color = color
        self.rendered_text = self.font.render(text, True, color)
        self.rect = self.rendered_text.get_rect(center=(x, y))

    def update(self, new_text):
        self.text = new_text
        self.rendered_text = self.font.render(self.text, True, self.color)

# Mängu algseaded
all_sprites = pygame.sprite.Group()
red_car = Car(red_car_image, screen_width // 2, screen_height - 50, 0)
all_sprites.add(red_car)
blue_cars = pygame.sprite.Group()
score = 0
score_display = Text("Score: 0", 30, screen_width // 2, 20, WHITE)

# Peamise mänguloop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Kui kasutaja vajutab sulgemisnuppu
            running = False

    # Loome uue sinise auto, kui vähemalt 60 kaadrit on möödunud
    if random.randint(0, 60) == 0:
        blue_car = Car(blue_car_image, random.randint(20, screen_width - 20), -50, random.randint(1, 5))
        blue_cars.add(blue_car)
        all_sprites.add(blue_car)

    # Uuendame kõiki mänguobjekte
    all_sprites.update()

    # Kollisioonide tuvastamine punase ja sinise auto vahel
    for blue_car in blue_cars:
        if blue_car.rect.top > screen_height:
            blue_cars.remove(blue_car)
            all_sprites.remove(blue_car)

        elif red_car.rect.colliderect(blue_car.rect):
            blue_cars.remove(blue_car)
            all_sprites.remove(blue_car)
            # Kui sinine auto läheb punasest mööda, suurenda skoori
            score += 1
            score_display.update("Score: " + str(score))

    # Ekraanipuhastus
    screen.blit(background_image, (0, 0))
    all_sprites.draw(screen)
    screen.blit(score_display.rendered_text, score_display.rect)
    pygame.display.flip()

    clock.tick(60)

# Sulgemisnupp
pygame.quit()
