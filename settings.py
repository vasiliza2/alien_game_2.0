class Settings:
    def __init__(self):
        # Параметры экрана
        self.screen_width = 800
        self.screen_height = 600
        self.bg_color = (0, 0, 0)

        # Параметры корабля
        self.ship_speed = 0.5

        # Параметры снарядов
        self.bullet_speed = 1.0
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (255, 0, 0)
        self.bullets_allowed = 3

        # Параметры инопланетян
        self.alien_speed = 0.2
        self.fleet_drop_speed = 5
        self.fleet_direction = 1

        # Параметры увеличения сложности
        self.speedup_scale = 1.1
        self.initialize_dynamic_settings()
               

    def initialize_dynamic_settings(self):
        """Настройки, которые изменяются в ходе игры"""
        self.alien_speed = 0.1
        self.fleet_drop_speed = 5

    def increase_speed(self):
        """Увеличение скорости для новой волны"""
        self.alien_speed *= self.speedup_scale
