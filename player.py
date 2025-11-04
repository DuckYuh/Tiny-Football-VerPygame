import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, frames, x, y, team, speed = 5):
        super().__init__()
        self.frames = frames
        self.current_frame = 0
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = speed
        self.team = team
        self.angle = 0 
        self.animation_time = 150 
        self.last_update = pygame.time.get_ticks()
    
    def update(self, keys, controls):
        dx, dy = 0, 0
        if keys[controls["left"]]:
            dx = -self.speed
            self.angle = 90
        if keys[controls["right"]]:
            dx = self.speed
            self.angle = 270
        if keys[controls["up"]]:
            dy = -self.speed
            self.angle = 180
        if keys[controls["down"]]:
            dy = self.speed
            self.angle = 0
            
        if keys[controls["left"]] and keys[controls["up"]]:
            self.angle = 135
        if keys[controls["right"]] and keys[controls["down"]]:
            self.angle = 135
        if keys[controls["up"]] and keys[controls["right"]]:
            self.angle = 45
        if keys[controls["down"]] and keys[controls["left"]]:
            self.angle = 45
            
        self.rect.x += dx
        self.rect.y += dy
        
        now = pygame.time.get_ticks()
        if now - self.last_update > self.animation_time:
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.last_update = now
        
        frame = self.frames[self.current_frame]
        self.image = pygame.transform.rotate(frame, -self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)