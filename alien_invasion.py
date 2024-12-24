import sys
import pygame
import random  # Для генерации бонусов
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from save_load import save_game, load_game
from bonus import Bonus
import pickle
import os

class AlienInvasion:
    def __init__(self): 
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Инопланетное вторжение")

        # Загрузка фонового изображения
        self.bg_image = pygame.image.load('resources/images/background.jpg')

        # Инициализация звуков
        pygame.mixer.init()
        self.laser_sound = pygame.mixer.Sound("resources/sounds/laser.mp3")
        self.alien_explosion_sound = pygame.mixer.Sound("resources/sounds/alien_explosion.mp3")
        self.life_lost_sound = pygame.mixer.Sound("resources/sounds/life_lost.mp3")
        self.game_over_sound = pygame.mixer.Sound("resources/sounds/game_over.mp3")

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.bonuses = pygame.sprite.Group()  # Группа для бонусов
        self._create_fleet()

        # Добавляем атрибут для счёта и жизней
        self.score = 0
        self.lives = 3  # Начальные жизни
        self.font = pygame.font.SysFont(None, 48)  # Шрифт для отображения счёта и "Game Over"

        # Уровень игры
        self.level = 1

        # Флаг для заморозки пришельцев
        self.aliens_frozen = False
        self.freeze_timer = 0  # Таймер заморозки

    def run_game(self):
        while True:
            self._check_events()
            if not self.aliens_frozen:  # Обновляем пришельцев только если они не заморожены
                self._update_aliens()
            self.ship.update()
            self._update_bullets()
            self._update_bonuses()
            self._update_freeze_timer()
            self._update_screen()

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_s:  # Сохранение игры
            self._save_game()
        elif event.key == pygame.K_l:  # Загрузка игры
            self._load_game()

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
            self.laser_sound.play()  # Воспроизведение звука выстрела

    def _update_bullets(self):
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if collisions:
            self.score += 10 * len(collisions)
            self.alien_explosion_sound.play()
            # Генерация бонусов при уничтожении пришельцев
            for aliens in collisions.values():
                for alien in aliens:
                    if random.random() < 0.2:  # 20% вероятность появления бонуса
                        self._create_bonus(alien.rect.center)

        if not self.aliens:
            self.bullets.empty()
            self.settings.increase_speed()
            self.level += 1
            self._create_fleet()

    def _update_aliens(self):
        self.aliens.update()
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._take_life()
        self._check_aliens_bottom()

    def _update_bonuses(self):
        self.bonuses.update()
        for bonus in self.bonuses.copy():
            if bonus.rect.top >= self.settings.screen_height:
                self.bonuses.remove(bonus)

        # Проверяем, если корабль подобрал бонус
        collisions = pygame.sprite.spritecollide(self.ship, self.bonuses, True)
        if collisions:
            self._freeze_aliens()

    def _create_bonus(self, position):
        """Создание бонуса с вероятностью 7%."""
        if random.randint(1, 100) <= 7:  # 7% шанс выпадения
            bonus = Bonus(self, position)
            self.bonuses.add(bonus)


    def _freeze_aliens(self):
        """Замораживает всех пришельцев на определённое время."""
        self.aliens_frozen = True
        self.freeze_timer = pygame.time.get_ticks()  # Запускаем таймер заморозки

    def _update_freeze_timer(self):
        """Обновление состояния заморозки."""
        if self.aliens_frozen:
            if pygame.time.get_ticks() - self.freeze_timer > 5000:  # Заморозка на 5 секунд
                self.aliens_frozen = False

    def _check_aliens_bottom(self):
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                self._take_life()

    def _take_life(self):
        self.lives -= 1
        self.life_lost_sound.play()
        if self.lives <= 0:
            self._game_over()
        else:
            self.ship.center_ship()
            self.aliens.empty()
            self._create_fleet()
            self.bullets.empty()

    def _create_fleet(self):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        ship_height = self.ship.rect.height
        available_space_y = self.settings.screen_height - (3 * alien_height) - ship_height
        number_rows = available_space_y // (2 * alien_height)

        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _change_fleet_direction(self):
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _update_screen(self):
        self.screen.blit(self.bg_image, (0, 0))
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)
        self.bonuses.draw(self.screen)
        self._display_score()
        self._display_lives()
        self._display_level()
        pygame.display.flip()

    def _display_score(self):
        score_str = f"Score: {self.score}"
        score_image = self.font.render(score_str, True, (255, 255, 255))
        self.screen.blit(score_image, (20, 20))

    def _display_lives(self):
        lives_str = f"Lives: {self.lives}"
        lives_image = self.font.render(lives_str, True, (255, 255, 255))
        self.screen.blit(lives_image, (self.settings.screen_width - 150, 20))

    def _display_level(self):
        level_str = f"Level: {self.level}"
        level_image = self.font.render(level_str, True, (255, 255, 255))
        self.screen.blit(level_image, (self.settings.screen_width // 2 - 50, 20))

    def _game_over(self):
        self.screen.blit(self.bg_image, (0, 0))
        game_over_str = f"Game Over! Final Score: {self.score}"
        game_over_image = self.font.render(game_over_str, True, (255, 0, 0))
        self.screen.blit(game_over_image, (self.settings.screen_width // 2 - 150, self.settings.screen_height // 2))
        pygame.display.flip()
        self.game_over_sound.play()
        pygame.time.wait(2000)
        sys.exit()

    def _save_game(self):
        game_data = {"level": self.level, "score": self.score, "lives": self.lives}
        save_game(game_data)

    def _load_game(self):
        game_data = load_game()
        if game_data:
            self.level = game_data["level"]
            self.score = game_data["score"]
            self.lives = game_data["lives"]
            self.bullets.empty()
            self.aliens.empty()
            self.ship.center_ship()
            self._create_fleet()

if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()
