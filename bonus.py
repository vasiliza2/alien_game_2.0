import pygame

class Bonus(pygame.sprite.Sprite):
    """Класс для управления бонусами."""
    def __init__(self, ai_game, position):
        """Инициализация бонуса в указанной позиции."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # Загрузка изображения бонуса, масштабирование и создание rect
        self.original_image = pygame.image.load('resources/images/bonus.png')
        self.image = pygame.transform.scale(self.original_image, (30, 30))
        self.rect = self.image.get_rect()

        # Установка позиции бонуса
        self.rect.center = position
        self.y = float(self.rect.y)  # Хранение "дробной" координаты

        # Скорость бонуса
        self.speed = 0.1  # Скорость падения

    def update(self):
        """Перемещение бонуса вниз."""
        self.y += self.speed  # Обновляем дробное значение
        self.rect.y = int(self.y)  # Применяем округление к целому числу
