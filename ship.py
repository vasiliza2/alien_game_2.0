import pygame

class Ship:
    def __init__(self, ai_game):
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        
        # Загрузка и масштабирование изображения корабля
        self.image = pygame.image.load('resources/images/ship.bmp')
        self.image = pygame.transform.scale(self.image, (50, 50))  # Масштабируем до 50x50
        
        # Устанавливаем белый цвет как прозрачный
        self.image.set_colorkey((255, 255, 255))
        
        self.rect = self.image.get_rect()
        self.screen_rect = ai_game.screen.get_rect()

        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)

        self.moving_right = False
        self.moving_left = False

    def update(self):
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed
        self.rect.x = self.x

    def blitme(self):
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """Сброс корабля в центр экрана."""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)  # Обновление позиции в координатах с плавающей точкой
