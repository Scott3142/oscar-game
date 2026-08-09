import pygame
import random
import math

# --- Configuration ---
WIDTH, HEIGHT = 1800, 1200
FPS = 60

# Colors
SKY_BLUE = (135, 206, 235)
GRASS_GREEN = (124, 252, 0)
INVENTORY_BG = (50, 50, 50)

# Exact colors from Numberblocks 1-5
NUMBERBLOCK_COLORS = {
    1: (220, 50, 50),   # Red
    2: (255, 140, 0),   # Orange
    3: (255, 215, 0),   # Yellow
    4: (50, 205, 50),   # Green
    5: (30, 144, 255)   # Blue
}

def draw_numberblock(surface, number, x, bottom_y, block_size=30):
    """Draws the iconic block shapes. bottom_y is the bottom edge of the shape."""
    color = NUMBERBLOCK_COLORS[number]
    
    def draw_block(bx, by):
        rect = (bx, by, block_size, block_size)
        pygame.draw.rect(surface, color, rect)
        pygame.draw.rect(surface, (0, 0, 0), rect, 3) # Bold outline for kids
        
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
        # Numberblock 4 is a 2x2 square!
        draw_block(x, bottom_y - block_size)
        draw_block(x + block_size, bottom_y - block_size)
        draw_block(x, bottom_y - block_size*2)
        draw_block(x + block_size, bottom_y - block_size*2)
    elif number == 5:
        # 5 is a tall stack
        for i in range(1, 6):
            draw_block(x, bottom_y - i*block_size)

class Obstacle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        # We change the types to space-themed items
        self.type = random.choice(["planet", "rocket", "asteroid", "satellite"])
        self.radius = 60 # Hitbox size for clicking remains the same
        self.is_hidden = False
        
        # We assign colors based on the type here to draw faster later
        if self.type == "planet":
            # Give planets a random, non-dark color
            self.color = (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))
            # Some planets have rings, determined by a coin flip
            self.has_ring = random.choice([True, False])
        elif self.type == "rocket":
            self.color = (200, 200, 200) # Red-ish rocket body
            self.tip_color = (220, 50, 50)
        elif self.type == "asteroid":
            # Dark grey irregularly shaped rocks
            gray = random.randint(70, 110)
            self.color = (gray, gray, gray)
        elif self.type == "satellite":
            self.color = (150, 150, 150) # Metallic grey body
            self.panel_color = (30, 144, 255) # Blue solar panels

    def draw(self, surface):
        if self.is_hidden:
            return
            
        if self.type == "planet":
            # Draw the main planet body
            pygame.draw.circle(surface, self.color, (self.x, self.y), 50)
            
            # Optional: Add a subtle crater/pattern to make it look less plain
            pattern_color = (max(0, self.color[0]-40), max(0, self.color[1]-40), max(0, self.color[2]-40))
            pygame.draw.circle(surface, pattern_color, (self.x - 15, self.y - 10), 10)
            pygame.draw.circle(surface, pattern_color, (self.x + 10, self.y + 15), 6)

            if self.has_ring:
                # To make rings look behind and in front, we draw a thick ellipse outline
                ring_rect = pygame.Rect(self.x - 80, self.y - 20, 160, 40)
                # Slighting darker/greyer version of the planet color for the ring
                ring_color = (min(255, self.color[0]+30), min(255, self.color[1]+30), min(255, self.color[2]+30))
                pygame.draw.ellipse(surface, ring_color, ring_rect, 6)

            # Standard bold black outline that he's used to seeing
            pygame.draw.circle(surface, (0, 0, 0), (self.x, self.y), 50, 4)

        elif self.type == "rocket":
            # Drawn slightly tilted for a dynamic space look
            # Rocket Body
            body_rect = pygame.Rect(self.x - 15, self.y - 40, 30, 80)
            pygame.draw.rect(surface, self.color, body_rect)
            pygame.draw.rect(surface, (0, 0, 0), body_rect, 4)
            
            # Nose Cone
            nose_points = [(self.x - 15, self.y - 40), (self.x + 15, self.y - 40), (self.x, self.y - 70)]
            pygame.draw.polygon(surface, self.tip_color, nose_points)
            pygame.draw.polygon(surface, (0, 0, 0), nose_points, 4)
            
            # Simple circular window
            pygame.draw.circle(surface, (10, 10, 30), (self.x, self.y - 15), 8)
            pygame.draw.circle(surface, (0, 0, 0), (self.x, self.y - 15), 8, 2)
            
            # Rocket Booster 'fire' (just orange/yellow circles)
            pygame.draw.circle(surface, (255, 140, 0), (self.x, self.y + 45), 10)
            pygame.draw.circle(surface, (255, 215, 0), (self.x, self.y + 45), 5)

        elif self.type == "asteroid":
            # We draw an irregular shape. Instead of complex math,
            # we just generate a few random points around the center.
            # (In a real game you'd pre-calculate this, but for a simple game this works fine)
            random.seed(self.x + self.y) # Ensure the shape stays the same between frames
            points = []
            for angle in range(0, 360, 45):
                dist = random.randint(30, 55)
                rad = math.radians(angle)
                px = self.x + dist * math.cos(rad)
                py = self.y + dist * math.sin(rad)
                points.append((px, py))
            random.seed() # Reset seed

            pygame.draw.polygon(surface, self.color, points)
            pygame.draw.polygon(surface, (0, 0, 0), points, 4)
            
            # Add a couple of lines inside to simulate surface texture
            pygame.draw.line(surface, (0,0,0), (points[0]), (self.x, self.y), 2)
            pygame.draw.line(surface, (0,0,0), (points[3]), (self.x, self.y), 2)

        elif self.type == "satellite":
            # Central Body box
            body_rect = pygame.Rect(self.x - 20, self.y - 20, 40, 40)
            pygame.draw.rect(surface, self.color, body_rect)
            pygame.draw.rect(surface, (0, 0, 0), body_rect, 4)
            
            # Left Solar Panel
            panel_l = pygame.Rect(self.x - 70, self.y - 15, 50, 30)
            pygame.draw.rect(surface, self.panel_color, panel_l)
            pygame.draw.rect(surface, (0, 0, 0), panel_l, 3)
            
            # Right Solar Panel
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
        self.vy += 0.5 # Gravity
        self.life -= 1

    def draw(self, surface):
        if self.life > 0:
            pygame.draw.rect(surface, self.color, (int(self.x), int(self.y), self.size, self.size))

def get_player_name(screen):
    """Displays a prompt and captures keyboard input for the player's name."""
    font = pygame.font.SysFont(None, 100)
    prompt_font = pygame.font.SysFont(None, 70)
    name = ""
    clock = pygame.time.Clock()
    
    # Generate 100 random stars for the background (x, y, size)
    stars = [(random.randint(0, WIDTH), random.randint(0, HEIGHT), random.randint(1, 3)) for _ in range(100)]
    
    while True:
        screen.fill((10, 10, 30)) # Deep space blue
        
        # Draw the stars
        for sx, sy, size in stars:
            pygame.draw.circle(screen, (200, 200, 255), (sx, sy), size)
            
        # Draw the question
        prompt = prompt_font.render("What is your name?", True, (255, 255, 255)) # Changed text to white!
        prompt_rect = prompt.get_rect(center=(WIDTH//2, HEIGHT//2 - 60))
        screen.blit(prompt, prompt_rect)
        
        # Draw the name as it is being typed
        name_text = font.render(name.upper(), True, (255, 255, 255))
        name_shadow = font.render(name.upper(), True, (0, 0, 0))
        name_rect = name_text.get_rect(center=(WIDTH//2, HEIGHT//2 + 40))
        
        # Draw shadow then text
        screen.blit(name_shadow, (name_rect.x + 3, name_rect.y + 3))
        screen.blit(name_text, name_rect)
        
        # Instructions for Dad
        dad_font = pygame.font.SysFont(None, 30)
        dad_text = dad_font.render("(Type name and press ENTER)", True, (100, 100, 100))
        screen.blit(dad_text, dad_text.get_rect(center=(WIDTH//2, HEIGHT - 50)))

        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if name.strip() != "": # Don't let it be blank
                        return name.upper()
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                else:
                    # Limit to 12 characters so it fits on the win screen
                    if len(name) < 12:
                        name += event.unicode
                        
        clock.tick(FPS)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Numberblocks Hide and Seek!")
    clock = pygame.time.Clock()
    
    win_font = pygame.font.SysFont(None, 100)

    player_name = get_player_name(screen)

    # Setup a grid to place things so they don't overlap too much
    # 4 columns, 3 rows (leaving bottom for inventory)
    grid_w = WIDTH // 4
    grid_h = (HEIGHT - 150) // 3
    positions = []
    for row in range(3):
        for col in range(4):
            # Center of each grid cell
            px = (col * grid_w) + (grid_w // 2)
            py = (row * grid_h) + (grid_h // 2) + 50
            positions.append((px, py))
    
    random.shuffle(positions)
    
    # Assign 5 grid positions to our Numberblocks
    hidden_blocks = {} # key: (x,y), value: number
    for i in range(1, 6):
        hidden_blocks[positions[i-1]] = i

    # Create obstacles. Put one over every Numberblock, plus some empty decoys.
    obstacles = []
    for i in range(9): # 5 covers, 4 decoys
        pos = positions[i]
        obstacles.append(Obstacle(pos[0], pos[1]))

    inventory = [] # Will hold the numbers 1-5 as they are collected
    particles = []
    game_won = False

    # --- ADD THIS LINE ---
    # Generate 100 stars, keeping them above the inventory area at the bottom
    stars = [(random.randint(0, WIDTH), random.randint(0, HEIGHT - 120), random.randint(1, 3)) for _ in range(100)]

    running = True
    while running:

        screen.fill((10, 10, 30)) # Deep space blue
        
        # Draw the stars
        for sx, sy, size in stars:
            pygame.draw.circle(screen, (200, 200, 255), (sx, sy), size)

        # --- Event Handling ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and not game_won:
                mx, my = event.pos
                
                # 1. Did we click an obstacle?
                clicked_obstacle = False
                for obs in obstacles:
                    if not obs.is_hidden and math.dist((mx, my), (obs.x, obs.y)) < obs.radius:
                        obs.is_hidden = True
                        clicked_obstacle = True
                        # Dust particles for the obstacle poofing
                        for _ in range(10):
                            particles.append(Particle(obs.x, obs.y, (200, 200, 200)))
                        break # Only click one thing at a time
                
                # 2. If we didn't click an obstacle, did we click a revealed Numberblock?
                if not clicked_obstacle:
                    for pos, val in list(hidden_blocks.items()):
                        # Check if the block is revealed (no obstacle on top of it)
                        covered = False
                        for obs in obstacles:
                            if not obs.is_hidden and obs.x == pos[0] and obs.y == pos[1]:
                                covered = True
                                break
                        
                        if not covered:
                            # Distance check for the Numberblock
                            if math.dist((mx, my), (pos[0], pos[1] - 45)) < 60:
                                inventory.append(val)
                                del hidden_blocks[pos] # Remove from map
                                
                                # Happy particles!
                                for _ in range(20):
                                    particles.append(Particle(pos[0], pos[1], NUMBERBLOCK_COLORS[val]))
                                
                                # Check Win Condition
                                if len(inventory) == 5:
                                    game_won = True
                                break

        # --- Update & Draw ---
        
        # Draw revealed Numberblocks
        for pos, val in hidden_blocks.items():
            # Only draw if the obstacle covering it is hidden
            for obs in obstacles:
                if obs.x == pos[0] and obs.y == pos[1] and obs.is_hidden:
                    draw_numberblock(screen, val, pos[0] - 15, pos[1] + 30)

        # Draw Obstacles
        for obs in obstacles:
            obs.draw(screen)

        # Draw Particles
        for p in particles[:]:
            p.move()
            p.draw(screen)
            if p.life <= 0:
                particles.remove(p)

        # Draw Inventory (The bottom UI panel)
        pygame.draw.rect(screen, INVENTORY_BG, (0, HEIGHT - 120, WIDTH, 120))
        
        # Draw placeholder slots for the 5 blocks
        slot_width = WIDTH // 5
        for i in range(5):
            center_x = (i * slot_width) + (slot_width // 2) - 15
            pygame.draw.circle(screen, (70, 70, 70), (center_x + 15, HEIGHT - 60), 40)
            
        # Draw the collected blocks in their slots (sorted so 1 is first, 2 is second, etc.)
        # inventory.sort()
        # for i, val in enumerate(inventory):
        #     center_x = (i * slot_width) + (slot_width // 2) - 15
        #     draw_numberblock(screen, val, center_x, HEIGHT - 10)

        # Draw the collected blocks in their specific fixed slots
        for val in inventory:
            # Since Numberblocks are 1 to 5, we subtract 1 to get their slot position (0 to 4)
            i = val - 1 
            center_x = (i * slot_width) + (slot_width // 2) - 15
            draw_numberblock(screen, val, center_x, HEIGHT - 10)

        # --- Win State ---
        if game_won:
            # Constant rainbow confetti!
            random_color = random.choice(list(NUMBERBLOCK_COLORS.values()))
            particles.append(Particle(random.randint(0, WIDTH), -20, random_color))
            particles.append(Particle(random.randint(0, WIDTH), -20, random_color))
            
            # Big Win Text
            text = win_font.render(f"YOU FOUND THEM, {player_name.upper()}!", True, (255, 255, 255))
            shadow = win_font.render(f"YOU FOUND THEM, {player_name.upper()}!", True, (0, 0, 0))
            text_rect = text.get_rect(center=(WIDTH//2, HEIGHT//2 - 50))
            
            screen.blit(shadow, (text_rect.x + 4, text_rect.y + 4))
            screen.blit(text, text_rect)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()