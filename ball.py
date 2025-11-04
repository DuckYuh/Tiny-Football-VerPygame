import pygame

class Ball(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.image = image.convert_alpha()
        self.rect = self.image.get_rect(center=(x, y))
        self.initx = x
        self.inity = y
        self.vel = pygame.Vector2(0, 0)
        self.friction = 0.95
    
    def update(self):
        self.rect.x += self.vel.x
        self.rect.y += self.vel.y
        
        self.vel.x *= self.friction
        self.vel.y *= self.friction
        
        if self.rect.left < 50:
            self.rect.left = 50
            self.vel.x = -self.vel.x
        if self.rect.right > 750:
            self.rect.right = 750
            self.vel.x = -self.vel.x
        if self.rect.top < 100:
            self.rect.top = 100
            self.vel.y = -self.vel.y
        if self.rect.bottom > 550:
            self.rect.bottom = 550
            self.vel.y = -self.vel.y
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)
    
    def reset(self):
        self.rect.center = (self.initx, self.inity) 
        self.vel = pygame.Vector2(0, 0)