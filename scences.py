import pygame, sys, math
from config import WIDTH, HEIGH, YELLOW, RED, GRAY, GREEN_FIELD, BLACK, WHITE
from button import Button
from player import Player
from ball import Ball

player1 = [
    pygame.image.load("assets/images/sprites/red/red1.png"),
    pygame.image.load("assets/images/sprites/red/red2.png"),
    pygame.image.load("assets/images/sprites/red/red3.png"),
    pygame.image.load("assets/images/sprites/red/red4.png")
]
player1 = [pygame.transform.scale(img, (48, 48)) for img in player1]
player2 = [
    pygame.image.load("assets/images/sprites/blue/blue1.png"),
    pygame.image.load("assets/images/sprites/blue/blue2.png"),
    pygame.image.load("assets/images/sprites/blue/blue3.png"),
    pygame.image.load("assets/images/sprites/blue/blue4.png")
]
player2 = [pygame.transform.scale(img, (48, 48)) for img in player2]
ball = pygame.image.load("assets/images/ball.png")
ball = pygame.transform.scale(ball, (32, 32))
bg = pygame.image.load("assets/images/background.jpg").convert()
bg = pygame.transform.scale(bg, (800, 600))

#manager
class SceneManager:
    def __init__(self):
        self.scene = None

    def go_to(self, scene):
        self.scene = scene

#scenes
class Scene:
    def handle_events(self):
        pass
    def update(self):
        pass
    def draw(self):
        pass

#menu    
class MenuScene(Scene):
    def __init__(self, manager):
        self.manager = manager
        self.font = pygame.font.SysFont("arialblack", 45)
        self.button_play = Button(100, 400, 200, 80, "PLAY", self.start_game)
        self.button_quit = Button(500, 400, 200, 80, "QUIT", self.quit_game)

    def handle_events(self, events):
        for event in events:
            self.button_play.handle_event(event)
            self.button_quit.handle_event(event)

    def draw(self, screen):
        screen.blit(bg, (0, 0))
        
        title_text = "Welcome to TINY FOOTBALL"
        
        for dx in [-2, 2, 0, 0]:
            for dy in [0, 0, -2, 2]:
                outline = self.font.render(title_text, True, WHITE)
                screen.blit(outline, (50 + dx, 200 + dy))
        
        text = self.font.render(title_text, True, BLACK)
        screen.blit(text, (50, 200))
        self.button_play.draw(screen)
        self.button_quit.draw(screen)
        
    def start_game(self):
        self.manager.go_to(GameScene(self.manager))
        
    def quit_game(self):
        pygame.quit()
        sys.exit()
        
#game
class GameScene(Scene):
    def __init__(self, manager):
        self.manager = manager
        self.font = pygame.font.SysFont(None, 20)
        self.sfont = pygame.font.SysFont(None, 40)
        self.aScore = 0
        self.bScore = 0
        self.start_time = pygame.time.get_ticks()
        self.ball = Ball(400, 325, ball)
        self.teamA = [
            Player(player1, 150, 250, 1, 4),
            Player(player1, 150, 400, 1, 4)
        ]
        self.teamB = [
            Player(player2, 650, 250, 2, 4),
            Player(player2, 650, 400, 2, 4)
        ]
        self.activeA = 0
        self.activeB = 0

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_f:
                self.activeA = (self.activeA + 1) % len(self.teamA)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_KP0:
                self.activeB = (self.activeB + 1) % len(self.teamB)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

    def update(self):
        now = pygame.time.get_ticks()
        self.elapsed_time = (now - self.start_time) // 1000
        
        if self.elapsed_time >= 90:
            self.elapsed_time = 90
        
        keys = pygame.key.get_pressed()
        self.teamA[self.activeA].update(keys, {
            "up": pygame.K_w,
            "down": pygame.K_s,
            "left": pygame.K_a,
            "right": pygame.K_d
        })
        self.teamB[self.activeB].update(keys, {
            "up": pygame.K_UP,
            "down": pygame.K_DOWN,
            "left": pygame.K_LEFT,
            "right": pygame.K_RIGHT
        })
        
        self.ball.update()
        
        for player in self.teamA + self.teamB:
            collirect = player.rect.inflate(-16, -16)
            if collirect.colliderect(self.ball.rect):
                dx = self.ball.rect.centerx - player.rect.centerx
                dy = self.ball.rect.centery - player.rect.centery
                length = math.hypot(dx, dy) or 1
                self.ball.vel.x = (dx / length) * 10
                self.ball.vel.y = (dy / length) * 10
        
        if self.ball.rect.top > 275 and self.ball.rect.top < 375:
            if self.ball.rect.left <= 50:
                self.ball.reset()
                self.bScore += 1
            if self.ball.rect.right >= 750:
                self.ball.reset()
                self.aScore += 1

    def draw(self, screen):
        screen.fill(GREEN_FIELD)
        text = self.font.render(f"Playing Tiny Football", True, BLACK)
        screen.blit(text, (10, 20))
        self.draw_field(screen)
        self.draw_scoreboard(screen)
        self.draw_timer(screen)
        self.ball.draw(screen)
        
        self.teamA[0].draw(screen)
        self.teamA[1].draw(screen)
        self.teamB[0].draw(screen)
        self.teamB[1].draw(screen)
        
        pygame.draw.circle(screen, YELLOW, (self.teamA[self.activeA].rect.centerx,self.teamA[self.activeA].rect.centery), 16, 2)
        pygame.draw.circle(screen, YELLOW, (self.teamB[self.activeB].rect.centerx,self.teamB[self.activeB].rect.centery), 16, 2)
        
        if self.elapsed_time >= 90:
            pygame.draw.rect(screen, WHITE, (100,200,600,200), border_radius = 5)
            pygame.draw.rect(screen, BLACK, (100,200,600,200), 3, border_radius = 5)
            game_over_text = self.sfont.render("Game Over!!!", True, RED)
            screen.blit(game_over_text, (WIDTH // 2 - 80, HEIGH // 2 - 50))
            TEAM = self.sfont.render("Team RED   Team BLUE", True, RED)
            RESULT = self.sfont.render(f"{self.aScore}                   {self.bScore}", True, BLACK)
            screen.blit(TEAM, (WIDTH // 2 - 150, HEIGH // 2))
            screen.blit(RESULT, (WIDTH // 2 - 80, HEIGH // 2 + 50))
            pygame.display.flip()
        
    def draw_field(self,screen):
        pygame.draw.rect(screen, WHITE, (50,100,700,450), 2)
        pygame.draw.line(screen, WHITE, (400,100), (400,550), 2)
        pygame.draw.circle(screen, WHITE, (400,325), 50, 2)
        pygame.draw.circle(screen, WHITE, (400,325), 5)
        pygame.draw.rect(screen, GRAY, (0,275,50,100), 2)
        pygame.draw.rect(screen, GRAY, (750,275,50,100), 2)
        pygame.draw.rect(screen, WHITE, (50,200,100,250), 2)
        pygame.draw.rect(screen, WHITE, (650,200,100,250), 2)
        
    def draw_scoreboard(self,screen):
        pygame.draw.rect(screen, WHITE, (10,40,200,20), border_radius=2)
        pygame.draw.line(screen, BLACK, (105, 40), (105,60), 2)
        
        scoreboard = self.font.render(f"Team A: {self.aScore}      Team B: {self.bScore} ", True, BLACK)
        text_rect = scoreboard.get_rect(center=(105, 50))
        screen.blit(scoreboard, text_rect)
        
    def draw_timer(self, screen):
        pygame.draw.rect(screen, WHITE, (250,40,55,20), border_radius=5)
        
        timer = self.font.render(f"{self.elapsed_time}:00", True, BLACK)
        text_timer = timer.get_rect(center=(277, 50))
        screen.blit(timer, text_timer)
