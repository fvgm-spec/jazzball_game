import pygame
import sys
import random
import math
import os
from pygame.locals import *
from screenshot_helper import take_screenshot

# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
CYAN = (0, 255, 255)

# Game states
MENU = 0
DEMO = 1
PLAYING = 2

class Ball:
    def __init__(self, x, y, radius, color, speed_x=0, speed_y=0):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.original_color = color
        self.active = True
    
    def update(self):
        self.x += self.speed_x
        self.y += self.speed_y
        
        # Bounce off walls
        if self.x - self.radius <= 0 or self.x + self.radius >= SCREEN_WIDTH:
            self.speed_x *= -1
        if self.y - self.radius <= 0 or self.y + self.radius >= SCREEN_HEIGHT:
            self.speed_y *= -1
    
    def draw(self, screen):
        if self.active:
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
    
    def collides_with(self, other_ball):
        distance = math.sqrt((self.x - other_ball.x)**2 + (self.y - other_ball.y)**2)
        return distance < (self.radius + other_ball.radius)

class Player(Ball):
    def __init__(self, x, y, radius, color):
        super().__init__(x, y, radius, color)
        self.score = 0
    
    def move_to(self, pos_x, pos_y):
        self.x = pos_x
        self.y = pos_y
        
        # Keep player within screen bounds
        self.x = max(self.radius, min(self.x, SCREEN_WIDTH - self.radius))
        self.y = max(self.radius, min(self.y, SCREEN_HEIGHT - self.radius))

class JazzBallGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("JazzBall Game")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 36)
        self.small_font = pygame.font.SysFont(None, 24)
        
        self.game_state = MENU
        self.reset_game()
    
    def reset_game(self):
        self.player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, 20, GREEN)
        self.balls = []
        self.target_balls = []
        self.obstacle_balls = []
        self.level = 1
        self.score = 0
        self.demo_timer = 0
        self.game_over = False
        
        # Create initial balls
        self.create_level(self.level)
    
    def create_level(self, level):
        self.balls.clear()
        self.target_balls.clear()
        self.obstacle_balls.clear()
        
        # Create target balls (collect these)
        for _ in range(3 + level):
            x = random.randint(50, SCREEN_WIDTH - 50)
            y = random.randint(50, SCREEN_HEIGHT - 50)
            speed_x = random.uniform(-2, 2)
            speed_y = random.uniform(-2, 2)
            ball = Ball(x, y, 15, YELLOW, speed_x, speed_y)
            self.target_balls.append(ball)
            self.balls.append(ball)
        
        # Create obstacle balls (avoid these)
        for _ in range(level):
            x = random.randint(50, SCREEN_WIDTH - 50)
            y = random.randint(50, SCREEN_HEIGHT - 50)
            speed_x = random.uniform(-3, 3)
            speed_y = random.uniform(-3, 3)
            ball = Ball(x, y, 20, RED, speed_x, speed_y)
            self.obstacle_balls.append(ball)
            self.balls.append(ball)
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    if self.game_state == MENU:
                        pygame.quit()
                        sys.exit()
                    else:
                        self.game_state = MENU
                
                if self.game_state == MENU:
                    if event.key == K_1:
                        self.reset_game()
                        self.game_state = PLAYING
                    elif event.key == K_2:
                        self.reset_game()
                        self.game_state = DEMO
                
                if self.game_state == PLAYING or self.game_state == DEMO:
                    if event.key == K_r:
                        self.reset_game()
                
                # Screenshot functionality
                if event.key == K_F12:
                    screenshot_path = take_screenshot(self.screen)
                    print(f"Screenshot saved to {screenshot_path}")
            
            if event.type == MOUSEBUTTONDOWN and self.game_state == MENU:
                mouse_pos = pygame.mouse.get_pos()
                # Check if play button is clicked
                if 300 <= mouse_pos[0] <= 500 and 200 <= mouse_pos[1] <= 250:
                    self.reset_game()
                    self.game_state = PLAYING
                # Check if demo button is clicked
                elif 300 <= mouse_pos[0] <= 500 and 300 <= mouse_pos[1] <= 350:
                    self.reset_game()
                    self.game_state = DEMO
    
    def update(self):
        if self.game_state == PLAYING:
            # Move player with mouse
            mouse_pos = pygame.mouse.get_pos()
            self.player.move_to(mouse_pos[0], mouse_pos[1])
            
            # Update all balls
            for ball in self.balls:
                ball.update()
            
            # Check collisions with target balls
            for ball in self.target_balls[:]:
                if ball.active and self.player.collides_with(ball):
                    ball.active = False
                    self.score += 10
                    self.target_balls.remove(ball)
            
            # Check collisions with obstacle balls
            for ball in self.obstacle_balls:
                if ball.active and self.player.collides_with(ball):
                    self.game_over = True
            
            # Check if level is complete
            if len(self.target_balls) == 0:
                self.level += 1
                self.create_level(self.level)
        
        elif self.game_state == DEMO:
            # Update all balls
            for ball in self.balls:
                ball.update()
            
            # Simple AI for demo mode
            if self.target_balls:
                # Find closest target ball
                closest_ball = min(self.target_balls, key=lambda b: 
                                  math.sqrt((b.x - self.player.x)**2 + (b.y - self.player.y)**2))
                
                # Move towards it while avoiding obstacles
                target_x, target_y = closest_ball.x, closest_ball.y
                
                # Simple obstacle avoidance
                for obstacle in self.obstacle_balls:
                    dist = math.sqrt((obstacle.x - self.player.x)**2 + (obstacle.y - self.player.y)**2)
                    if dist < 100:  # Avoidance radius
                        avoid_x = self.player.x + (self.player.x - obstacle.x)
                        avoid_y = self.player.y + (self.player.y - obstacle.y)
                        target_x = (target_x + avoid_x) / 2
                        target_y = (target_y + avoid_y) / 2
                
                # Move player towards target
                dx = target_x - self.player.x
                dy = target_y - self.player.y
                dist = math.sqrt(dx*dx + dy*dy)
                
                if dist > 0:
                    dx /= dist
                    dy /= dist
                    self.player.move_to(self.player.x + dx * 5, self.player.y + dy * 5)
            
            # Check collisions with target balls
            for ball in self.target_balls[:]:
                if ball.active and self.player.collides_with(ball):
                    ball.active = False
                    self.score += 10
                    self.target_balls.remove(ball)
            
            # Check collisions with obstacle balls
            for ball in self.obstacle_balls:
                if ball.active and self.player.collides_with(ball):
                    self.game_over = True
            
            # Check if level is complete
            if len(self.target_balls) == 0:
                self.level += 1
                self.create_level(self.level)
            
            # Demo timer to return to menu
            self.demo_timer += 1
            if self.demo_timer > FPS * 30:  # 30 seconds demo
                self.game_state = MENU
    
    def draw(self):
        self.screen.fill(BLACK)
        
        if self.game_state == MENU:
            # Draw title
            title = self.font.render("JazzBall Game", True, WHITE)
            self.screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 100))
            
            # Draw play button
            pygame.draw.rect(self.screen, BLUE, (300, 200, 200, 50))
            play_text = self.font.render("Play Game", True, WHITE)
            self.screen.blit(play_text, (400 - play_text.get_width()//2, 215))
            
            # Draw demo button
            pygame.draw.rect(self.screen, PURPLE, (300, 300, 200, 50))
            demo_text = self.font.render("Watch Demo", True, WHITE)
            self.screen.blit(demo_text, (400 - demo_text.get_width()//2, 315))
            
            # Draw instructions
            instructions = [
                "Instructions:",
                "- Move the mouse to control your ball",
                "- Collect yellow balls to score points",
                "- Avoid red balls",
                "- Complete levels to increase difficulty",
                "- Press ESC to return to menu",
                "- Press R to restart the game",
                "- Press F12 to take a screenshot"
            ]
            
            for i, line in enumerate(instructions):
                text = self.small_font.render(line, True, WHITE)
                self.screen.blit(text, (50, 400 + i * 25))
        
        elif self.game_state == PLAYING or self.game_state == DEMO:
            # Draw all balls
            for ball in self.balls:
                ball.draw(self.screen)
            
            # Draw player
            self.player.draw(self.screen)
            
            # Draw score and level
            score_text = self.font.render(f"Score: {self.score}", True, WHITE)
            self.screen.blit(score_text, (20, 20))
            
            level_text = self.font.render(f"Level: {self.level}", True, WHITE)
            self.screen.blit(level_text, (20, 60))
            
            # Draw demo indicator
            if self.game_state == DEMO:
                demo_text = self.font.render("DEMO MODE", True, RED)
                self.screen.blit(demo_text, (SCREEN_WIDTH - demo_text.get_width() - 20, 20))
            
            # Draw game over
            if self.game_over:
                over_text = self.font.render("GAME OVER! Press R to restart", True, RED)
                self.screen.blit(over_text, (SCREEN_WIDTH//2 - over_text.get_width()//2, SCREEN_HEIGHT//2))
        
        pygame.display.flip()
    
    def run(self):
        while True:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)

if __name__ == "__main__":
    game = JazzBallGame()
    game.run()
