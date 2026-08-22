import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
NORMAL_ENEMY_COLOR = (50, 200, 50)  # Green
PAIN_COLOR = (255, 50, 0)           # Searing Red
DARK_RED = (100, 0, 0)

class Enemy:
    def __init__(self, x, y):
        self.base_x = x
        self.base_y = y
        self.x = x
        self.y = y
        self.width = 100
        self.height = 100
        
        # 144,000 health losing 2 HP per frame at 60 FPS = exactly 20 minutes
        self.max_health = 144000 
        self.health = 144000
        self.in_pain = True
        self.pain_tick = 0

    def update(self):
        if self.in_pain and self.health > 0:
            # 1. Mechanical Pain: Continuous health drain
            self.health -= 2 
            
            # 2. Visual Pain: Erratic shaking 
            shake_intensity = 6
            self.x = self.base_x + random.randint(-shake_intensity, shake_intensity)
            self.y = self.base_y + random.randint(-shake_intensity, shake_intensity)
            
            self.pain_tick += 1
        else:
            # Death or relief
            self.x = self.base_x
            self.y = self.base_y

    def draw(self, surface):
        if self.health <= 0:
            return  # Enemy has succumbed

        # 3. Visual Pain: Flashing colors
        if self.in_pain:
            if self.pain_tick % 8 < 4:
                color = PAIN_COLOR
            else:
                color = WHITE
        else:
            color = NORMAL_ENEMY_COLOR

        # Draw the enemy
        pygame.draw.rect(surface, color, (self.x, self.y, self.width, self.height))

        # Draw massive boss Health Bar
        health_ratio = self.health / self.max_health
        bar_width = 400
        bar_x = (WIDTH // 2) - (bar_width // 2)
        pygame.draw.rect(surface, DARK_RED, (bar_x, HEIGHT - 50, bar_width, 20))
        pygame.draw.rect(surface, (255, 0, 0), (bar_x, HEIGHT - 50, bar_width * health_ratio, 20))

def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("20 Minutes of Searing Pain")
    clock = pygame.time.Clock()

    # Center the enemy
    victim = Enemy((WIDTH // 2) - 50, (HEIGHT // 2) - 50)

    running = True
    font = pygame.font.SysFont(None, 48)
    small_font = pygame.font.SysFont(None, 24)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update
        victim.update()

        # Render
        screen.fill(BLACK)
        victim.draw(screen)
        
        # Data and Timers
        if victim.health > 0:
            # Calculate time left based on health depletion rate 
            # (120 health = 1 second)
            seconds_left = int(victim.health / 120)
            mins, secs = divmod(seconds_left, 60)
            
            percent = (victim.health / victim.max_health) * 100
            
            status_text = font.render("STATUS: BURNING ALIVE", True, PAIN_COLOR)
            time_text = font.render(f"TIME UNTIL DEMISE: {mins:02d}:{secs:02d}", True, WHITE)
            dmg_text = small_font.render(f"INTEGRITY: {percent:.2f}% ({victim.health:,} HP)", True, (200, 200, 200))
            
            screen.blit(status_text, (WIDTH//2 - status_text.get_width()//2, 50))
            screen.blit(time_text, (WIDTH//2 - time_text.get_width()//2, 100))
            screen.blit(dmg_text, (WIDTH//2 - dmg_text.get_width()//2, HEIGHT - 80))
        else:
            text = font.render("SUFFERING CONCLUDED.", True, (100, 100, 100))
            screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
