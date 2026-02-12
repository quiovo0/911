import pygame
import random

pygame.init()
print("Pygame init OK - version:", pygame.version.ver)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Simple Rounds-Style Platformer")

# Colors
WHITE  = (255, 255, 255)
BLACK  = (0, 0, 0)
GREEN  = (0, 255, 0)
BLUE   = (0, 0, 255)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.center = (100, SCREEN_HEIGHT - 100)
        self.velocity_y = 0
        self.on_ground = False

    def update(self, platforms):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:  self.rect.x -= 5
        if keys[pygame.K_RIGHT]: self.rect.x += 5
        if keys[pygame.K_SPACE] and self.on_ground:
            self.velocity_y = -15
            self.on_ground = False

        self.velocity_y += 1
        self.rect.y += self.velocity_y

        self.on_ground = False
        for p in platforms:
            if self.rect.colliderect(p.rect) and self.velocity_y >= 0:
                self.rect.bottom = p.rect.top
                self.velocity_y = 0
                self.on_ground = True

        # Keep on screen
        self.rect.clamp_ip(screen.get_rect())

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        super().__init__()
        self.image = pygame.Surface((w, h))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect(topleft=(x, y))

class Collectible(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill((255, 220, 0))
        self.rect = self.image.get_rect(center=(x, y))

def main():
    clock = pygame.time.Clock()
    all_sprites = pygame.sprite.Group()
    platforms   = pygame.sprite.Group()
    coins       = pygame.sprite.Group()

    player = Player()
    all_sprites.add(player)

    # Platforms
    platforms.add(Platform(0, SCREEN_HEIGHT-20, SCREEN_WIDTH, 20))
    platforms.add(Platform(180, 420, 180, 20))
    platforms.add(Platform(480, 320, 160, 20))
    platforms.add(Platform(80, 220, 140, 20))
    all_sprites.add(platforms)

    # Coins
    for _ in range(6):
        c = Collectible(random.randint(40, SCREEN_WIDTH-40),
                        random.randint(40, SCREEN_HEIGHT-120))
        coins.add(c)
        all_sprites.add(c)

    score = 0
    font = pygame.font.Font(None, 42)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        player.update(platforms)

        collected = pygame.sprite.spritecollide(player, coins, True)
        score += len(collected)

        screen.fill((12, 14, 18))
        all_sprites.draw(screen)

        screen.blit(font.render(f"Score: {score}", True, WHITE), (12, 12))

        if score >= 6:
            txt = font.render("ROUND COMPLETE!", True, (80, 255, 120))
            screen.blit(txt, (SCREEN_WIDTH//2 - txt.get_width()//2, 240))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
