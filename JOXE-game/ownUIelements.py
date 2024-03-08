import pygame

class Slider:
    def __init__(self, x, y, width, min_val, max_val):
        self.rect = pygame.Rect(x, y, width, 20)
        self.min = min_val
        self.max = max_val
        self.val = min_val
        self.grabbed = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.grabbed = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.grabbed = False
        elif event.type == pygame.MOUSEMOTION:
            if self.grabbed:
                self.val = self.min + (event.pos[0] - self.rect.x) / self.rect.width * (self.max - self.min)
                self.val = max(min(self.val, self.max), self.min)

    def draw(self, window):
        pygame.draw.rect(window, (255, 255, 255), self.rect, 2)
        pygame.draw.circle(window, (255, 0, 0), (int(self.rect.x + (self.val - self.min) / (self.max - self.min) * self.rect.width), self.rect.centery), 10)
