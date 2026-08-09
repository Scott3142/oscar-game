import pygame
import random
import math
import asyncio

# --- Configuration ---
WIDTH, HEIGHT = 800, 600
FPS = 60
INVENTORY_BG = (30, 30, 50)

# Exact colors from Numberblocks 1-5
NUMBERBLOCK_COLORS = {
    1: (220, 50, 50),   # Red
    2: (255, 140, 0),   # Orange
    3: (255, 215, 0),   # Yellow
    4: (50, 205, 50),   # Green
    5: (30, 144, 255)   # Blue
}

def draw_numberblock(surface, number, x, bottom_y, block_size=30):
    color = NUMBERBLOCK_COLORS[number]
    def draw_block(bx, by):
        rect = (bx, by, block_size, block_size)
        pygame.draw.rect(surface, color, rect)
        pygame.draw.rect(surface, (0, 0, 0), rect, 3) 
        
    if number == 1:
        draw_block(x, bottom_y - block_size)
    elif number == 2:
        draw_block(x, bottom_y - block_size)
        draw_block(x, bottom_y - block_size*2)
    elif number == 3:
        draw_block(x, bottom_y - block_size)
        draw_block(x, bottom_y - block_size*2)
        draw_block(x, bottom_y - block_size*3)
    elif number == 4:
        draw_block(x, bottom_y - block_size)
        draw_block(x + block_size, bottom_y - block_size)
        draw_block(x, bottom_y - block_size*2)
        draw_block(x + block_size, bottom_y - block_size*2)
    elif number == 5:
        for i in range(1, 6):
            draw_block(x, bottom_y - i*block_size)

class Obstacle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.type = random.choice(["planet", "rocket", "asteroid", "satellite"])
        self.radius = 60
        self.is_hidden = False
        
        if self.type == "planet":
            self.color = (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))
            self.has_ring = random.choice([True, False])
        elif self.type == "rocket":
            self.color = (200, 200, 200)
            self.tip_color = (220, 50, 50)
        elif self.type == "asteroid":
            gray = random.randint(70, 110)
            self.color = (gray, gray, gray)
        elif self.type == "satellite":
            self.color = (150, 150, 150)
            self.panel_color = (30, 144, 255)

    def draw(self, surface):
        if self.is_hidden:
            return
            
        if self.type == "planet":
            pygame.draw.circle(surface, self.color, (self.x, self.y), 50)
            pattern_color = (max(0, self.color[0]-40), max(0, self.color[1]-40), max(0, self.color[2]-40))
            pygame.draw.circle(surface, pattern_color, (self.x - 15, self.y - 10), 10)
            pygame.draw.circle(surface, pattern_color, (self.x + 10, self.y + 15), 6)
            if self.has_ring:
                ring_rect = pygame.Rect(self.x - 80, self.y - 20, 160, 40)
                ring_color = (min(255, self.color[0]+30), min(255, self.color[1]+30), min(255, self.color[2]+30))
                pygame.draw.ellipse(surface, ring_color, ring_rect, 6)
            pygame.draw.circle(surface, (0, 0, 0), (self.x, self.y), 50, 4)

        elif self.type == "rocket":
            body_rect = pygame.Rect(self.x - 15, self.y - 40, 30, 80)
            pygame.draw.rect(surface, self.color, body_rect)
            pygame.draw.rect(surface, (0, 0, 0), body_rect, 4)
            nose_points = [(self.x - 15, self.y - 40), (self.x + 15, self.y - 40), (self.x, self.y - 70)]
            pygame.draw.polygon(surface, self.tip_color, nose_points)
            pygame.draw.polygon(surface, (0, 0, 0), nose_points, 4)
            pygame.draw.circle(surface, (10, 10, 30), (self.x, self.y - 15), 8)
            pygame.draw.circle(surface, (0, 0, 0), (self.x, self.y - 15), 8, 2)
            pygame.draw.circle(surface, (255, 140, 0), (self.x, self.y + 45), 10)
            pygame.draw.circle(surface, (255, 215, 0), (self.x, self.y + 45), 5)

        elif self.type == "asteroid":
            random.seed(self.x + self.y) 
            points = []
            for angle in range(0, 360, 45):
                dist = random.randint(30, 55)
                rad = math.radians(angle)
                px = self.x + dist * math.cos(rad)
                py = self.y + dist * math.sin(rad)
                points.append((px, py))
            random.seed()
            pygame.draw.polygon(surface, self.color, points)
            pygame.draw.polygon(surface, (0, 0, 0), points, 4)
            pygame.draw.line(surface, (0,0,0), (points[0]), (self.x, self.y), 2)
            pygame.draw.line(surface, (0,0,0), (points[3]), (self.x, self.y), 2)

        elif self.type == "satellite":
            body_rect = pygame.Rect(self.x - 20, self.y - 20, 40, 40)
            pygame.draw.rect(surface, self.color, body_rect)
            pygame.draw.rect(surface, (0, 0, 0), body_rect, 4)
            panel_l = pygame.Rect(self.x - 70, self.y - 15, 50, 30)
            pygame.draw.rect(surface, self.panel_color, panel_l)
            pygame.draw.rect(surface, (0, 0, 0), panel_l, 3)
            panel_r = pygame.Rect(self.x + 20, self.y - 15, 50, 30)
            pygame.draw.rect(surface, self.panel_color, panel_r)
            pygame.draw.rect(surface, (0, 0, 0), panel_r, 3)

class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.vx = random.uniform(-8, 8)
        self.vy = random.uniform(-10, 2)
        self.life = random.randint(30, 60)
        self.size = random.randint(5, 12)

    def move(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.5 
        self.life -= 1

    def draw(self, surface):
        if self.life > 0:
            pygame.draw.rect(surface, self.color, (int(self.x), int(self.y), self.size, self.size))

# MUST be async for Pygbag
async def get_player_name(screen):
    font = pygame.font.SysFont(None, 100)
    prompt_font = pygame.font.SysFont(None, 70)
    name = ""
    clock = pygame.time.Clock()
    stars = [(random.randint(0, WIDTH), random.randint(0, HEIGHT), random.randint(1, 3)) for _ in range(100)]
    
    while True:
        screen.fill((10, 10, 30))
        for sx, sy, size in stars:
            pygame.draw.circle(screen, (200, 200, 255), (sx, sy), size)
            
        prompt = prompt_font.render("What is your name?", True, (255, 255, 255))
        prompt_rect = prompt.get_rect(center=(WIDTH//2, HEIGHT//2 - 60))
        screen.blit(prompt, prompt_rect)
        
        name_text = font.render(name.upper(), True, (255, 255, 255))
        name_shadow = font.render(name.upper(), True, (0, 0, 0))
        name_rect = name_text.get_rect(center=(WIDTH//2, HEIGHT//2 + 40))
        
        screen.blit(name_shadow, (name_rect.x + 3, name_rect.y + 3))
        screen.blit(name_text, name_rect)
        
        dad_font = pygame.font.SysFont(None, 30)
        dad_text = dad_font.render("(Type name and press ENTER)", True, (150, 150, 150))
        screen.blit(dad_text, dad_text.get_rect(center=(WIDTH//2, HEIGHT - 50)))

        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if name.strip() != "":
                        return name.upper()
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                else:
                    if len(name) < 12:
                        name += event.unicode
                        
        await asyncio.sleep(0) # CRITICAL: Yields to browser
        clock.tick(FPS)

# MUST be async for Pygbag
async def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Numberblocks Space Seek!")
    clock = pygame.time.Clock()
    win_font = pygame.font.SysFont(None, 80)
    
    player_name = await get_player_name(screen)
    
    grid_w = WIDTH // 4
    grid_h = (HEIGHT - 150) // 3
    positions = []
    for row in range(3):
        for col in range(4):
            px = (col * grid_w) + (grid_w // 2)
            py = (row * grid_h) + (grid_h // 2) + 50
            positions.append((px, py))
    
    random.shuffle(positions)
    
    hidden_blocks = {} 
    for i in range(1, 6):
        hidden_blocks[positions[i-1]] = i

    obstacles = []
    for i in range(9):
        pos = positions[i]
        obstacles.append(Obstacle(pos[0], pos[1]))

    inventory = [] 
    particles = []
    game_won = False
    stars = [(random.randint(0, WIDTH), random.randint(0, HEIGHT - 120), random.randint(1, 3)) for _ in range(100)]

    running = True
    while running:
        screen.fill((10, 10, 30))
        for sx, sy, size in stars:
            pygame.draw.circle(screen, (200, 200, 255), (sx, sy), size)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and not game_won:
                mx, my = event.pos
                
                clicked_obstacle = False
                for obs in obstacles:
                    if not obs.is_hidden and math.dist((mx, my), (obs.x, obs.y)) < obs.radius:
                        obs.is_hidden = True
                        clicked_obstacle = True
                        for _ in range(10):
                            particles.append(Particle(obs.x, obs.y, (200, 200, 200)))
                        break 
                
                if not clicked_obstacle:
                    for pos, val in list(hidden_blocks.items()):
                        covered = False
                        for obs in obstacles:
                            if not obs.is_hidden and obs.x == pos[0] and obs.y == pos[1]:
                                covered = True
                                break
                        
                        if not covered:
                            if math.dist((mx, my), (pos[0], pos[1] - 45)) < 60:
                                inventory.append(val)
                                del hidden_blocks[pos] 
                                for _ in range(20):
                                    particles.append(Particle(pos[0], pos[1], NUMBERBLOCK_COLORS[val]))
                                
                                if len(inventory) == 5:
                                    game_won = True
                                break

        for pos, val in hidden_blocks.items():
            for obs in obstacles:
                if obs.x == pos[0] and obs.y == pos[1] and obs.is_hidden:
                    draw_numberblock(screen, val, pos[0] - 15, pos[1] + 30)

        for obs in obstacles:
            obs.draw(screen)

        for p in particles[:]:
            p.move()
            p.draw(screen)
            if p.life <= 0:
                particles.remove(p)

        pygame.draw.rect(screen, INVENTORY_BG, (0, HEIGHT - 120, WIDTH, 120))
        
        slot_width = WIDTH // 5
        for i in range(5):
            center_x = (i * slot_width) + (slot_width // 2) - 15
            pygame.draw.circle(screen, (20, 20, 40), (center_x + 15, HEIGHT - 60), 40)
            
        for val in inventory:
            i = val - 1 
            center_x = (i * slot_width) + (slot_width // 2) - 15
            draw_numberblock(screen, val, center_x, HEIGHT - 10)

        if game_won:
            random_color = random.choice(list(NUMBERBLOCK_COLORS.values()))
            particles.append(Particle(random.randint(0, WIDTH), -20, random_color))
            particles.append(Particle(random.randint(0, WIDTH), -20, random_color))
            
            text = win_font.render(f"YOU FOUND THEM, {player_name}!", True, (255, 255, 255))
            shadow = win_font.render(f"YOU FOUND THEM, {player_name}!", True, (0, 0, 0))
            text_rect = text.get_rect(center=(WIDTH//2, HEIGHT//2 - 50))
            
            screen.blit(shadow, (text_rect.x + 4, text_rect.y + 4))
            screen.blit(text, text_rect)

        pygame.display.flip()
        await asyncio.sleep(0) # CRITICAL: Yields to browser
        clock.tick(FPS)

# Pygbag entry point
if __name__ == "__main__":
    asyncio.run(main())