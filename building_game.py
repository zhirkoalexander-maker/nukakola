import pygame
import sys
import random
import math

pygame.init()

# Экран и конфиг
WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Base Defense - Tower Builder")
clock = pygame.time.Clock()
font_big = pygame.font.Font(None, 48)
font_medium = pygame.font.Font(None, 36)
font_small = pygame.font.Font(None, 24)
font_tiny = pygame.font.Font(None, 18)

# Цвета с градиентами
SKY_BLUE = (135, 206, 250)
GROUND_GREEN = (34, 139, 34)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 223, 0)
ORANGE = (255, 140, 0)
RED = (220, 20, 60)
LIGHT_BROWN = (210, 180, 140)
DARK_BROWN = (101, 67, 33)

# Класс текстурированного блока
class Block:
    BLOCK_SIZE = 40
    BLOCK_TYPES = {
        'wood': {'color': DARK_BROWN, 'pattern': '█', 'health': 40, 'cost': 40},
        'stone': {'color': (169, 169, 169), 'pattern': '■', 'health': 80, 'cost': 80},
        'brick': {'color': (210, 105, 30), 'pattern': '▬', 'health': 60, 'cost': 70},
        'grass': {'color': GROUND_GREEN, 'pattern': '▲', 'health': 30, 'cost': 30},
        'sand': {'color': (238, 214, 175), 'pattern': '░', 'health': 25, 'cost': 25},
        'iron': {'color': (100, 100, 100), 'pattern': '◆', 'health': 150, 'cost': 150},
        'crystal': {'color': (100, 200, 255), 'pattern': '◇', 'health': 120, 'cost': 120},
        'obsidian': {'color': (50, 20, 60), 'pattern': '■', 'health': 200, 'cost': 250},
        'diamond': {'color': (150, 220, 255), 'pattern': '✦', 'health': 300, 'cost': 400},
        'titanium': {'color': (180, 180, 200), 'pattern': '█', 'health': 180, 'cost': 200},
    }
    
    def __init__(self, x, y, block_type='wood'):
        self.x = x
        self.y = y
        self.block_type = block_type
        self.color = self.BLOCK_TYPES[block_type]['color']
        self.max_health = self.BLOCK_TYPES[block_type]['health']
        self.health = self.max_health
        self.width = self.BLOCK_SIZE
        self.height = self.BLOCK_SIZE
        self.damage_flash = 0
    
    def draw(self, surface):
        # Мигание при урыне
        draw_color = self.color
        if self.damage_flash > 0:
            draw_color = (255, 100, 100)
            self.damage_flash -= 1
        
        # Основной блок
        pygame.draw.rect(surface, draw_color, (self.x, self.y, self.width, self.height))
        
        # 3D эффект - боковая грань (с затемнением)
        darker_color = tuple(max(0, c - 40) for c in draw_color)
        side_points = [
            (self.x + self.width, self.y),
            (self.x + self.width + 4, self.y - 4),
            (self.x + self.width + 4, self.y + self.height - 4),
            (self.x + self.width, self.y + self.height)
        ]
        pygame.draw.polygon(surface, darker_color, side_points)
        
        # 3D эффект - верхняя грань (со светлением)
        lighter_color = tuple(min(255, c + 50) for c in draw_color)
        top_points = [
            (self.x, self.y),
            (self.x + 4, self.y - 4),
            (self.x + self.width + 4, self.y - 4),
            (self.x + self.width, self.y)
        ]
        pygame.draw.polygon(surface, lighter_color, top_points)
        
        # Основная передняя грань
        pygame.draw.rect(surface, draw_color, (self.x, self.y, self.width, self.height))
        
        # Паттерн текстуры в зависимости от типа блока
        if self.block_type == 'wood':
            # Диагональные линии для дерева
            for i in range(0, self.width, 6):
                pygame.draw.line(surface, darker_color, (self.x + i, self.y), (self.x + i, self.y + self.height), 1)
        elif self.block_type == 'stone':
            # Крапчатый рисунок для камня
            for i in range(5):
                px = self.x + random.randint(2, self.width - 2)
                py = self.y + random.randint(2, self.height - 2)
                pygame.draw.circle(surface, darker_color, (px, py), 2)
        elif self.block_type == 'brick':
            # Разделения для кирпича
            pygame.draw.line(surface, darker_color, (self.x + self.width // 2, self.y), (self.x + self.width // 2, self.y + self.height), 1)
            pygame.draw.line(surface, darker_color, (self.x, self.y + self.height // 2), (self.x + self.width, self.y + self.height // 2), 1)
        elif self.block_type == 'iron':
            # Решетка для железа
            for i in range(8, self.width, 8):
                pygame.draw.line(surface, lighter_color, (self.x + i, self.y + 2), (self.x + i, self.y + self.height - 2), 1)
            for i in range(8, self.height, 8):
                pygame.draw.line(surface, lighter_color, (self.x + 2, self.y + i), (self.x + self.width - 2, self.y + i), 1)
        
        # Тень/граница для глубины
        pygame.draw.rect(surface, (0, 0, 0), (self.x, self.y, self.width, self.height), 2)
        
        # Светлая полоса сверху (свет)
        pygame.draw.line(surface, lighter_color, (self.x + 2, self.y + 2), (self.x + self.width - 2, self.y + 2), 3)
        
        # Темная полоса снизу (тень)
        pygame.draw.line(surface, darker_color, (self.x + 2, self.y + self.height - 2), (self.x + self.width - 2, self.y + self.height - 2), 3)
        
        # Полоса здоровья блока (если он повреждён)
        if self.health < self.max_health:
            bar_width = self.width - 4
            bar_height = 2
            bar_x = self.x + 2
            bar_y = self.y + self.height - 6
            
            pygame.draw.rect(surface, RED, (bar_x, bar_y, bar_width, bar_height))
            health_width = (self.health / self.max_health) * bar_width
            pygame.draw.rect(surface, (0, 200, 0), (bar_x, bar_y, health_width, bar_height))
    
    def take_damage(self, damage):
        self.health -= damage
        self.damage_flash = 5
        return self.health <= 0
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
    
    def is_clicked(self, pos):
        return self.get_rect().collidepoint(pos)
    
    def take_damage(self, damage):
        self.health -= damage
        return self.health <= 0

# Класс игрока
class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 30
        self.height = 40
        self.speed = 2.5
        self.selected_block = 'wood'
        self.money = 500
        self.health = 100
        self.max_health = 100
        self.mode = 'build'  # 'build', 'break', 'weapon'
        
        # Система оружия
        self.weapons = {
            'sword': {'damage': 25, 'range': 60, 'cooldown': 30, 'color': (200, 200, 200)},
            'axe': {'damage': 40, 'range': 70, 'cooldown': 50, 'color': (200, 100, 50)},
            'spear': {'damage': 20, 'range': 100, 'cooldown': 20, 'color': (150, 150, 150)},
            'sniper': {'damage': 80, 'range': 300, 'cooldown': 60, 'color': (50, 50, 50)},
            'hammer': {'damage': 60, 'range': 90, 'cooldown': 80, 'color': (139, 69, 19)},
            'laser': {'damage': 35, 'range': 150, 'cooldown': 25, 'color': (255, 0, 0)},
        }
        self.weapon_type = 'sword'
        self.weapon_damage = self.weapons[self.weapon_type]['damage']
        self.weapon_range = self.weapons[self.weapon_type]['range']
        self.weapon_cooldown_max = self.weapons[self.weapon_type]['cooldown']
        self.attack_cooldown = 0
        self.attack_animation = 0
        
        # Баффы
        self.speed_boost = 0
        self.shield_active = 0
        self.mega_strike = 0  # Усиленный удар
    
    def draw(self, surface):
        # Цвет с эффектом щита
        body_color = (100, 255, 100) if self.shield_active > 0 else (255, 100, 100)
        
        # Тело
        pygame.draw.rect(surface, body_color, (self.x, self.y, self.width, self.height))
        
        # Боковая грань (3D эффект)
        pygame.draw.polygon(surface, tuple(max(0, c - 50) for c in body_color), [
            (self.x + self.width, self.y),
            (self.x + self.width + 3, self.y - 2),
            (self.x + self.width + 3, self.y + self.height - 2),
            (self.x + self.width, self.y + self.height)
        ])
        
        # Голова
        pygame.draw.circle(surface, (255, 200, 150), (int(self.x + self.width // 2), int(self.y - 15)), 9)
        
        # Волосы/шапка
        pygame.draw.arc(surface, (100, 50, 30), (self.x - 2, self.y - 20, self.width + 4, 10), 0, 3.14, 3)
        
        # Глаза
        pygame.draw.circle(surface, BLACK, (int(self.x + 10), int(self.y - 18)), 2)
        pygame.draw.circle(surface, BLACK, (int(self.x + 20), int(self.y - 18)), 2)
        
        # Белки глаз
        pygame.draw.circle(surface, WHITE, (int(self.x + 10), int(self.y - 18)), 1)
        pygame.draw.circle(surface, WHITE, (int(self.x + 20), int(self.y - 18)), 1)
        
        # Рот
        pygame.draw.line(surface, RED, (int(self.x + 11), int(self.y - 10)), (int(self.x + 19), int(self.y - 10)), 1)
        
        # Щит если активен
        if self.shield_active > 0:
            pygame.draw.circle(surface, (100, 200, 255), (int(self.x + self.width // 2), int(self.y + self.height // 2)), 25, 3)
        
        # Рука с оружием/инструментом
        if self.mode == 'weapon':
            # Разные оружия
            angle = (self.attack_animation / 10.0) * 45 if self.attack_animation > 0 else 0
            angle_rad = math.radians(angle)
            
            weapon_color = self.weapons[self.weapon_type]['color']
            
            if self.weapon_type == 'sword':
                # Меч
                sword_start_x = self.x + self.width
                sword_start_y = self.y + 10
                sword_end_x = sword_start_x + math.cos(angle_rad) * 20
                sword_end_y = sword_start_y + math.sin(angle_rad) * 20
                pygame.draw.line(surface, weapon_color, (int(sword_start_x), int(sword_start_y)), 
                                (int(sword_end_x), int(sword_end_y)), 4)
                pygame.draw.circle(surface, (150, 100, 50), (int(sword_start_x), int(sword_start_y)), 3)
                
            elif self.weapon_type == 'axe':
                # Топор
                axe_start_x = self.x + self.width
                axe_start_y = self.y + 10
                axe_end_x = axe_start_x + math.cos(angle_rad) * 18
                axe_end_y = axe_start_y + math.sin(angle_rad) * 18
                pygame.draw.line(surface, (150, 100, 50), (int(axe_start_x), int(axe_start_y)), 
                                (int(axe_end_x), int(axe_end_y)), 3)
                pygame.draw.rect(surface, weapon_color, (int(axe_end_x - 4), int(axe_end_y - 6), 8, 12), 2)
                
            elif self.weapon_type == 'spear':
                # Копьё
                spear_start_x = self.x + self.width
                spear_start_y = self.y + 10
                spear_end_x = spear_start_x + math.cos(angle_rad) * 25
                spear_end_y = spear_start_y + math.sin(angle_rad) * 25
                pygame.draw.line(surface, (150, 100, 50), (int(spear_start_x), int(spear_start_y)), 
                                (int(spear_end_x), int(spear_end_y)), 2)
                pygame.draw.polygon(surface, weapon_color, [
                    (int(spear_end_x), int(spear_end_y)),
                    (int(spear_end_x - 3), int(spear_end_y - 4)),
                    (int(spear_end_x + 3), int(spear_end_y - 4))
                ])
            
            elif self.weapon_type == 'sniper':
                # Снайперская винтовка
                gun_start_x = self.x + self.width
                gun_start_y = self.y + 10
                gun_end_x = gun_start_x + math.cos(angle_rad) * 30
                gun_end_y = gun_start_y + math.sin(angle_rad) * 30
                # Ствол
                pygame.draw.line(surface, weapon_color, (int(gun_start_x), int(gun_start_y)), 
                                (int(gun_end_x), int(gun_end_y)), 3)
                # Приклад
                pygame.draw.rect(surface, (100, 100, 100), (int(gun_start_x - 8), int(gun_start_y - 2), 8, 4))
                # Прицел (в режиме атаки)
                if self.attack_animation > 0:
                    pygame.draw.circle(surface, (255, 0, 0), (int(gun_end_x), int(gun_end_y)), 3, 1)
            
            elif self.weapon_type == 'hammer':
                # Молот
                hammer_start_x = self.x + self.width
                hammer_start_y = self.y + 10
                hammer_end_x = hammer_start_x + math.cos(angle_rad) * 20
                hammer_end_y = hammer_start_y + math.sin(angle_rad) * 20
                # Ручка
                pygame.draw.line(surface, (150, 100, 50), (int(hammer_start_x), int(hammer_start_y)), 
                                (int(hammer_end_x), int(hammer_end_y)), 4)
                # Голова молота (квадрат)
                pygame.draw.rect(surface, weapon_color, (int(hammer_end_x - 6), int(hammer_end_y - 6), 12, 12))
            
            elif self.weapon_type == 'laser':
                # Лазер
                laser_start_x = self.x + self.width
                laser_start_y = self.y + 10
                laser_end_x = laser_start_x + math.cos(angle_rad) * 80
                laser_end_y = laser_start_y + math.sin(angle_rad) * 80
                # Лазерный луч
                if self.attack_animation > 0:
                    pygame.draw.line(surface, (255, 0, 0), (int(laser_start_x), int(laser_start_y)), 
                                    (int(laser_end_x), int(laser_end_y)), 2)
                    # Свечение
                    pygame.draw.line(surface, (255, 100, 100), (int(laser_start_x), int(laser_start_y)), 
                                    (int(laser_end_x), int(laser_end_y)), 4)
                # Генератор лазера
                pygame.draw.circle(surface, weapon_color, (int(laser_start_x), int(laser_start_y)), 4)
        else:
            # Молот/кирка для строительства
            arm_end_x = self.x + self.width + 15
            arm_end_y = self.y
            pygame.draw.line(surface, (255, 150, 100), (self.x + self.width, self.y + 10), (arm_end_x, arm_end_y), 3)
            pygame.draw.circle(surface, (150, 100, 50), (int(arm_end_x), int(arm_end_y)), 4)
        
        # Полоса здоровья над игроком
        bar_width = 40
        bar_height = 4
        bar_x = self.x + (self.width - bar_width) // 2
        bar_y = self.y - 25
        
        pygame.draw.rect(surface, RED, (bar_x, bar_y, bar_width, bar_height))
        health_width = (self.health / self.max_health) * bar_width
        pygame.draw.rect(surface, (0, 200, 0), (bar_x, bar_y, health_width, bar_height))
        pygame.draw.rect(surface, BLACK, (bar_x, bar_y, bar_width, bar_height), 1)
    
    def update_cooldown(self):
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
        if self.attack_animation > 0:
            self.attack_animation -= 1
        if self.speed_boost > 0:
            self.speed_boost -= 1
        if self.shield_active > 0:
            self.shield_active -= 1
    
    def attack(self, enemies):
        """Атаковать врагов в радиусе оружия"""
        if self.attack_cooldown <= 0:
            self.attack_animation = 10
            self.attack_cooldown = self.weapon_cooldown_max
            
            # Урон с учётом мега-удара
            damage = self.weapon_damage
            if self.mega_strike > 0:
                damage *= 2
                self.mega_strike = 0
            
            # Наносим урон врагам в радиусе
            for enemy in enemies:
                dist = math.sqrt((enemy.x + enemy.width // 2 - (self.x + self.width // 2))**2 + 
                               (enemy.y + enemy.height // 2 - (self.y + self.height // 2))**2)
                if dist < self.weapon_range:
                    enemy.health -= damage
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
    
    def move(self, dx, dy, blocks):
        # Проверка столкновения с блоками
        current_speed = 2.5
        if self.speed_boost > 0:
            current_speed = 4.5  # Ускорение
        
        dx = (dx / 5) * current_speed  # Масштабирование по скорости
        dy = (dy / 5) * current_speed
        
        new_rect = self.get_rect().move(dx, dy)
        collision = False
        for block in blocks:
            if new_rect.colliderect(block.get_rect()):
                collision = True
                break
        
        if not collision:
            self.x = max(0, min(WIDTH - self.width, self.x + dx))
            self.y = max(0, min(HEIGHT - self.height, self.y + dy))

# Класс кнопки интерфейса
class Button:
    def __init__(self, x, y, width, height, text, color, font=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover = False
        self.font = font if font else font_small
    
    def draw(self, surface):
        color = tuple(min(255, c + 30) for c in self.color) if self.hover else self.color
        pygame.draw.rect(surface, color, self.rect, border_radius=8)
        pygame.draw.rect(surface, WHITE if self.hover else BLACK, self.rect, 3, border_radius=8)
        
        text_surface = self.font.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)
    
    def update(self, pos):
        self.hover = self.rect.collidepoint(pos)
    
    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

# Класс снаряда/стрелы
class Projectile:
    def __init__(self, x, y, target_x, target_y, damage, color, speed=8):
        self.x = x
        self.y = y
        self.target_x = target_x
        self.target_y = target_y
        self.damage = damage
        self.color = color
        self.speed = speed
        self.size = 4
        
        # Вычисляем направление
        dx = target_x - x
        dy = target_y - y
        dist = math.sqrt(dx**2 + dy**2)
        if dist > 0:
            self.vx = (dx / dist) * speed
            self.vy = (dy / dist) * speed
        else:
            self.vx = 0
            self.vy = 0
        
        self.lifetime = 300  # Снаряд живет 5 секунд
    
    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.lifetime -= 1
    
    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.size)
        # Хвост снаряда
        pygame.draw.line(surface, self.color, (int(self.x), int(self.y)), 
                        (int(self.x - self.vx * 5), int(self.y - self.vy * 5)), 2)
    
    def get_rect(self):
        return pygame.Rect(self.x - self.size, self.y - self.size, self.size * 2, self.size * 2)
    
    def is_alive(self):
        return self.lifetime > 0

# Инициализация
player = Player(WIDTH // 2 - 15, HEIGHT - 100)
blocks = []
enemies = []
loots = []  # Выпавший лут
powerups = []  # Power-ups
particles = []
npcs = []  # NPC помощники
projectiles = []  # Снаряды
wave = 1
wave_timer = 0
wave_delay = 180  # Задержка между волнами
enemies_spawned = 0
enemies_per_wave = 3
score = 0
game_over = False
game_won = False
paused = False
game_state = 'menu'  # 'menu' или 'playing'
game_difficulty = 'normal'  # 'normal', 'hard', 'survival'
base_rect = pygame.Rect(WIDTH // 2 - 50, 50, 100, 50)  # База (должна быть защищена)

# Стоимость NPC
npc_costs = {
    'archer': 120,
    'warrior': 150,
    'mage': 140
}

# Создаём землю
for x in range(0, WIDTH, Block.BLOCK_SIZE):
    blocks.append(Block(x, HEIGHT - Block.BLOCK_SIZE, 'grass'))

# Функция инициализации игры
def init_game():
    global player, blocks, enemies, loots, powerups, particles, npcs, projectiles
    global wave, wave_timer, enemies_spawned, enemies_per_wave, score
    global game_over, game_won, paused
    
    player = Player(WIDTH // 2 - 15, HEIGHT - 100)
    blocks = []
    enemies = []
    loots = []
    powerups = []
    particles = []
    npcs = []
    projectiles = []
    wave = 1
    wave_timer = 0
    enemies_spawned = 0
    score = 0
    game_over = False
    game_won = False
    paused = False
    
    # Создаём землю
    for x in range(0, WIDTH, Block.BLOCK_SIZE):
        blocks.append(Block(x, HEIGHT - Block.BLOCK_SIZE, 'grass'))
    
    if game_difficulty == 'normal':
        enemies_per_wave = 3
    elif game_difficulty == 'hard':
        enemies_per_wave = 5
    else:  # survival
        enemies_per_wave = 4

# Кнопки типов блоков (размещены внизу слева)
block_labels = {
    'wood': 'WOOD', 'stone': 'STONE', 'brick': 'BRICK', 'grass': 'GRASS',
    'sand': 'SAND', 'iron': 'IRON', 'crystal': 'CRYSTAL', 'obsidian': 'OBSID.',
    'diamond': 'DIAM.', 'titanium': 'TITAN.'
}
button_width = 55
button_height = 30
buttons = {}
block_types = ['wood', 'stone', 'brick', 'grass', 'sand', 'iron', 'crystal', 'obsidian', 'diamond', 'titanium']
for i, block_type in enumerate(block_types):
    x = 10 + (i % 5) * (button_width + 3)
    y = HEIGHT - 95 + (i // 5) * (button_height + 3)
    buttons[block_type] = Button(x, y, button_width, button_height, block_labels[block_type], Block.BLOCK_TYPES[block_type]['color'], font_tiny)

# Кнопки NPC (размещены внизу справа)
npc_button_width = 70
npc_button_height = 30
npc_buttons = {
    'archer': Button(WIDTH - 225, HEIGHT - 95, npc_button_width, npc_button_height, 'ARCHER', (150, 100, 50), font_tiny),
    'warrior': Button(WIDTH - 150, HEIGHT - 95, npc_button_width, npc_button_height, 'WARRIOR', (200, 50, 50), font_tiny),
    'mage': Button(WIDTH - 75, HEIGHT - 95, npc_button_width, npc_button_height, 'MAGE', (100, 100, 255), font_tiny),
}

# Кнопки меню
menu_buttons = [
    Button(WIDTH // 2 - 200, 280, 400, 60, "CLASSIC MODE", (100, 200, 100), font_medium),
    Button(WIDTH // 2 - 200, 360, 400, 60, "HARD MODE", (200, 50, 50), font_medium),
    Button(WIDTH // 2 - 200, 440, 400, 60, "SURVIVAL MODE", (200, 150, 50), font_medium),
]

# Кнопки для меню настроек и помощи
settings_back_btn = Button(WIDTH // 2 - 100, HEIGHT - 80, 200, 50, "BACK TO MENU", (150, 100, 100), font_medium)
howtoplay_back_btn = Button(WIDTH // 2 - 100, HEIGHT - 80, 200, 50, "BACK TO MENU", (150, 100, 100), font_medium)

# Дополнительные кнопки главного меню
howtoplay_btn = Button(WIDTH // 2 - 200, 540, 190, 50, "HOW TO PLAY", (100, 150, 255), font_medium)
settings_btn = Button(WIDTH // 2 + 10, 540, 190, 50, "SETTINGS", (200, 200, 100), font_medium)

# Основной цикл
running = True
tool_mode = 'build'  # 'build' или 'break'
particles = []

def spawn_enemy():
    # Враги появляются с правой или левой стороны
    side = random.choice(['left', 'right'])
    if side == 'left':
        x = 10
    else:
        x = WIDTH - 35
    
    y = random.randint(100, HEIGHT - 100)
    
    # Разные типы врагов с увеличивающимся шансом при волнах
    if wave <= 2:
        enemy_type = random.choices(['zombie', 'fast'], weights=[70, 30], k=1)[0]
    elif wave <= 4:
        enemy_type = random.choices(['zombie', 'fast', 'heavy', 'ranged'], weights=[40, 30, 20, 10], k=1)[0]
    else:
        enemy_type = random.choices(['zombie', 'fast', 'heavy', 'ranged', 'healer'], weights=[30, 25, 20, 15, 10], k=1)[0]
    
    enemy = Enemy(x, y, enemy_type)
    enemies.append(enemy)

powerups = []  # Добавляем список power-ups
menu_state = 'main'  # 'main', 'settings', 'howtoplay'
volume = 50  # Громкость (от 0 до 100)
difficulty_display = 'NORMAL'  # Отображение сложности

def spawn_loot(x, y):
    # Враги выпадают случайный лут при смерти
    loot_chance = random.random()
    
    if loot_chance < 0.1:  # 10% chance for power-up
        powerup_type = random.choices(['speed', 'shield', 'mega_strike'], weights=[40, 40, 20], k=1)[0]
        powerups.append(PowerUp(x, y, powerup_type))
    else:
        loot_types = ['wood', 'stone', 'coins', 'health']
        weights = [40, 30, 20, 10]
        loot_type = random.choices(loot_types, weights=weights, k=1)[0]
        loots.append(Loot(x, y, loot_type))

class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.life = 30
        self.vx = random.uniform(-3, 3)
        self.vy = random.uniform(-5, -1)
    
    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.2  # Гравитация
        self.life -= 1
    
    def draw(self, surface):
        if self.life > 0:
            size = max(1, int(5 * self.life / 30))
            pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), size)

# Класс врага
class Enemy:
    def __init__(self, x, y, enemy_type='zombie'):
        self.x = x
        self.y = y
        self.width = 25
        self.height = 35
        self.enemy_type = enemy_type
        self.attack_cooldown = 0
        self.animation_frame = 0
        
        # Разные типы врагов
        if enemy_type == 'zombie':
            self.health = 30
            self.max_health = 30
            self.speed = 1.5
            self.color = (100, 200, 100)
            self.damage = 10
            self.attack_range = 50
            self.attack_damage = 15
        elif enemy_type == 'fast':
            self.health = 15
            self.max_health = 15
            self.speed = 2.8  # Быстрый враг
            self.color = (200, 150, 50)  # Жёлтый
            self.damage = 5
            self.attack_range = 40
            self.attack_damage = 8
        elif enemy_type == 'heavy':
            self.health = 60
            self.max_health = 60
            self.speed = 0.8  # Медленный враг
            self.color = (100, 50, 50)  # Тёмный красный
            self.damage = 20
            self.attack_range = 60
            self.attack_damage = 30
        elif enemy_type == 'ranged':
            self.health = 25
            self.max_health = 25
            self.speed = 1.2  # Средний враг
            self.color = (150, 100, 200)  # Фиолетовый
            self.damage = 8
            self.attack_range = 200  # Длинная атака!
            self.attack_damage = 12
        elif enemy_type == 'healer':
            self.health = 20
            self.max_health = 20
            self.speed = 0.9  # Медленный враг
            self.color = (100, 255, 100)  # Светло-зелёный
            self.damage = 5
            self.attack_range = 100
            self.attack_damage = 5
            self.heal_power = 10  # Лечит других врагов
    
    def draw(self, surface):
        # Тело врага - 3D эффект
        darker_color = tuple(max(0, c - 40) for c in self.color)
        lighter_color = tuple(min(255, c + 40) for c in self.color)
        
        # Боковая грань (темная)
        pygame.draw.polygon(surface, darker_color, [
            (self.x + self.width, self.y),
            (self.x + self.width + 3, self.y - 2),
            (self.x + self.width + 3, self.y + self.height - 2),
            (self.x + self.width, self.y + self.height)
        ])
        
        # Основной прямоугольник
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height))
        
        # Голова
        pygame.draw.circle(surface, self.color, (int(self.x + self.width // 2), int(self.y - 10)), 6)
        
        # Глаза - враждебный взгляд (горящие)
        pygame.draw.circle(surface, RED, (int(self.x + 8), int(self.y - 12)), 3)
        pygame.draw.circle(surface, YELLOW, (int(self.x + 8), int(self.y - 12)), 1)
        pygame.draw.circle(surface, RED, (int(self.x + 17), int(self.y - 12)), 3)
        pygame.draw.circle(surface, YELLOW, (int(self.x + 17), int(self.y - 12)), 1)
        
        # Пасть
        pygame.draw.arc(surface, RED, (self.x + 5, self.y - 8, 15, 5), 0, 3.14, 2)
        
        # Специальные визуальные эффекты
        if self.enemy_type == 'fast':
            # Линии скорости
            pygame.draw.line(surface, lighter_color, (self.x - 5, self.y + 5), (self.x - 10, self.y + 5), 2)
            pygame.draw.line(surface, lighter_color, (self.x - 5, self.y + 15), (self.x - 10, self.y + 15), 2)
        elif self.enemy_type == 'heavy':
            # Броня
            pygame.draw.line(surface, (50, 50, 50), (self.x + 5, self.y + 10), (self.x + self.width - 5, self.y + 10), 3)
        elif self.enemy_type == 'ranged':
            # Лук/пушка
            pygame.draw.circle(surface, lighter_color, (int(self.x + self.width - 5), int(self.y + 5)), 3)
        elif self.enemy_type == 'healer':
            # Святой символ
            pygame.draw.line(surface, (255, 255, 0), (self.x + self.width // 2, self.y + 5), 
                            (self.x + self.width // 2, self.y + 15), 2)
            pygame.draw.line(surface, (255, 255, 0), (self.x + 5, self.y + 10), 
                            (self.x + self.width - 5, self.y + 10), 2)
        
        # Полоса здоровья
        bar_width = 25
        bar_height = 3
        bar_x = self.x + (self.width - bar_width) // 2
        bar_y = self.y - 18
        
        pygame.draw.rect(surface, RED, (bar_x, bar_y, bar_width, bar_height))
        health_width = (self.health / self.max_health) * bar_width
        pygame.draw.rect(surface, (0, 200, 0), (bar_x, bar_y, health_width, bar_height))
        pygame.draw.rect(surface, BLACK, (bar_x, bar_y, bar_width, bar_height), 1)
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
    
    def update_cooldown(self):
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
    
    def find_nearest_block(self, blocks):
        """Найти ближайший блок в радиусе атаки"""
        nearest_block = None
        nearest_dist = self.attack_range
        
        for block in blocks:
            block_center_x = block.x + block.width // 2
            block_center_y = block.y + block.height // 2
            enemy_center_x = self.x + self.width // 2
            enemy_center_y = self.y + self.height // 2
            
            dist = math.sqrt((block_center_x - enemy_center_x)**2 + (block_center_y - enemy_center_y)**2)
            if dist < nearest_dist:
                nearest_dist = dist
                nearest_block = block
        
        return nearest_block
    
    def attack_block(self, block):
        """Атаковать блок"""
        if self.attack_cooldown <= 0 and block:
            if block.take_damage(self.attack_damage):
                return True  # Блок разрушен
            self.attack_cooldown = 30  # Задержка перед следующей атакой
            return False
        return False
    
    def move_towards(self, target_x, target_y, blocks):
        # Сначала проверяем, есть ли блоки рядом
        nearest_block = self.find_nearest_block(blocks)
        if nearest_block:
            # Движемся к блоку вместо движения к игроку
            target_x = nearest_block.x + nearest_block.width // 2
            target_y = nearest_block.y + nearest_block.height // 2
        
        # Движение к цели (игроку или блоку)
        dx = target_x - self.x
        dy = target_y - self.y
        dist = math.sqrt(dx**2 + dy**2)
        
        if dist > 0:
            dx /= dist
            dy /= dist
            new_x = self.x + dx * self.speed
            new_y = self.y + dy * self.speed
            
            # Проверка столкновения с блоками
            new_rect = pygame.Rect(new_x, new_y, self.width, self.height)
            collision = False
            for block in blocks:
                if new_rect.colliderect(block.get_rect()):
                    collision = True
                    break
            
            if not collision:
                self.x = new_x
                self.y = new_y

# Класс лута (выпадает из врагов)
class Loot:
    LOOT_TYPES = {
        'wood': {'color': DARK_BROWN, 'symbol': '█', 'value': 50},
        'stone': {'color': (169, 169, 169), 'symbol': '■', 'value': 75},
        'coins': {'color': YELLOW, 'symbol': '●', 'value': 100},
        'health': {'color': (0, 200, 0), 'symbol': '+', 'value': 25},
    }
    
    def __init__(self, x, y, loot_type='wood'):
        self.x = x
        self.y = y
        self.loot_type = loot_type
        self.color = self.LOOT_TYPES[loot_type]['color']
        self.value = self.LOOT_TYPES[loot_type]['value']
        self.size = 10
        self.vy = 0  # Для падения
        self.rotation = 0  # Для вращения эффекта
        self.bounce = random.uniform(3, 5)  # Начальная скорость отскока
    
    def draw(self, surface):
        # Основной шар лута с эффектом 3D
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.size)
        
        # Белый блик (верхний левый)
        highlight_color = tuple(min(255, c + 100) for c in self.color)
        pygame.draw.circle(surface, highlight_color, (int(self.x - 3), int(self.y - 3)), 3)
        
        # Темный блик (нижний правый)
        shadow_color = tuple(max(0, c - 80) for c in self.color)
        pygame.draw.circle(surface, shadow_color, (int(self.x + 4), int(self.y + 4)), 3)
        
        # Граница
        pygame.draw.circle(surface, BLACK, (int(self.x), int(self.y)), self.size, 2)
        
        # Маленький вращающийся орнамент
        angle = math.radians(self.rotation)
        orbit_x = int(self.x + math.cos(angle) * 6)
        orbit_y = int(self.y + math.sin(angle) * 6)
        pygame.draw.circle(surface, highlight_color, (orbit_x, orbit_y), 2)
    
    def update(self):
        # Падение с отскоком
        self.vy += 0.3
        self.y += self.vy
        self.rotation = (self.rotation + 5) % 360
        
        # Отскок от земли
        if self.y > HEIGHT - 50:
            self.vy = -abs(self.vy) * 0.7
            self.y = HEIGHT - 50
    
    def get_rect(self):
        return pygame.Rect(self.x - self.size, self.y - self.size, self.size * 2, self.size * 2)
    
    def is_colliding(self, rect):
        return self.get_rect().colliderect(rect)

# Класс power-up (баффы и усиления)
class PowerUp:
    POWERUP_TYPES = {
        'speed': {'color': (100, 255, 200), 'symbol': '⚡', 'duration': 300},
        'shield': {'color': (100, 200, 255), 'symbol': '◆', 'duration': 400},
        'mega_strike': {'color': (255, 100, 100), 'symbol': '★', 'duration': 1},
    }
    
    def __init__(self, x, y, powerup_type='speed'):
        self.x = x
        self.y = y
        self.powerup_type = powerup_type
        self.color = self.POWERUP_TYPES[powerup_type]['color']
        self.duration = self.POWERUP_TYPES[powerup_type]['duration']
        self.size = 12
        self.vy = 0
        self.rotation = 0
        self.pulse = 0
    
    def draw(self, surface):
        # Свечение вокруг power-up
        glow_size = self.size + int(3 * abs(math.sin(self.rotation / 30)))
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), glow_size, 2)
        
        # Основной шар
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.size)
        
        # Блик
        highlight_color = tuple(min(255, c + 100) for c in self.color)
        pygame.draw.circle(surface, highlight_color, (int(self.x - 4), int(self.y - 4)), 4)
        
        # Звезда/символ в центре
        pygame.draw.circle(surface, WHITE, (int(self.x), int(self.y)), 4, 1)
    
    def update(self):
        self.vy += 0.3
        self.y += self.vy
        self.rotation = (self.rotation + 8) % 360
        
        if self.y > HEIGHT - 50:
            self.vy = -abs(self.vy) * 0.7
            self.y = HEIGHT - 50
    
    def get_rect(self):
        return pygame.Rect(self.x - self.size, self.y - self.size, self.size * 2, self.size * 2)
    
    def is_colliding(self, rect):
        return self.get_rect().colliderect(rect)

# Класс NPC помощника
class NPC:
    def __init__(self, x, y, npc_type='archer'):
        self.x = x
        self.y = y
        self.width = 20
        self.height = 30
        self.npc_type = npc_type
        self.attack_cooldown = 0
        self.lifetime = 600  # 10 секунд жизни (при 60 FPS)
        
        if npc_type == 'archer':
            self.health = 25
            self.max_health = 25
            self.speed = 1.8
            self.color = (150, 100, 50)
            self.damage = 4  # Очень низкий урон
            self.attack_range = 250
        elif npc_type == 'warrior':
            self.health = 35
            self.max_health = 35
            self.speed = 2.0
            self.color = (200, 50, 50)
            self.damage = 3  # Низкий урон
            self.attack_range = 80
        elif npc_type == 'mage':
            self.health = 20
            self.max_health = 20
            self.speed = 1.5
            self.color = (100, 100, 255)
            self.damage = 5  # Низкий урон
            self.attack_range = 200
    
    def draw(self, surface):
        # Тело NPC
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height))
        
        # Голова
        pygame.draw.circle(surface, self.color, (int(self.x + self.width // 2), int(self.y - 8)), 5)
        
        # Корона/символ типа
        if self.npc_type == 'archer':
            # Лук
            pygame.draw.polygon(surface, (150, 100, 50), [
                (int(self.x + self.width), int(self.y - 5)),
                (int(self.x + self.width + 5), int(self.y)),
                (int(self.x + self.width), int(self.y + 5))
            ])
        elif self.npc_type == 'warrior':
            # Щит
            pygame.draw.circle(surface, (200, 200, 50), (int(self.x - 5), int(self.y + 10)), 6)
        elif self.npc_type == 'mage':
            # Посох
            pygame.draw.line(surface, (200, 150, 50), (int(self.x + self.width), int(self.y)), 
                           (int(self.x + self.width + 8), int(self.y - 10)), 2)
        
        # Индикатор времени жизни (полоса над NPC)
        lifetime_bar_width = 20
        lifetime_bar_height = 2
        lifetime_bar_x = self.x + (self.width - lifetime_bar_width) // 2
        lifetime_bar_y = self.y - 20
        
        # Фон полосы
        pygame.draw.rect(surface, (50, 50, 50), (lifetime_bar_x, lifetime_bar_y, lifetime_bar_width, lifetime_bar_height))
        # Полоса жизни
        lifetime_width = (self.lifetime / 600) * lifetime_bar_width
        lifetime_color = (200, 200, 50) if self.lifetime > 300 else (255, 100, 0)
        pygame.draw.rect(surface, lifetime_color, (lifetime_bar_x, lifetime_bar_y, lifetime_width, lifetime_bar_height))
        
        # Полоса здоровья
        bar_width = 20
        bar_height = 2
        bar_x = self.x + (self.width - bar_width) // 2
        bar_y = self.y - 15
        
        pygame.draw.rect(surface, RED, (bar_x, bar_y, bar_width, bar_height))
        health_width = (self.health / self.max_health) * bar_width
        pygame.draw.rect(surface, (0, 200, 0), (bar_x, bar_y, health_width, bar_height))
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
    
    def update_cooldown(self):
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
        self.lifetime -= 1
    
    def find_nearest_enemy(self, enemies):
        """Найти ближайшего врага"""
        nearest_enemy = None
        nearest_dist = self.attack_range * 1.5
        
        for enemy in enemies:
            dist = math.sqrt((enemy.x + enemy.width // 2 - (self.x + self.width // 2))**2 + 
                           (enemy.y + enemy.height // 2 - (self.y + self.height // 2))**2)
            if dist < nearest_dist:
                nearest_dist = dist
                nearest_enemy = enemy
        
        return nearest_enemy
    
    def attack(self, enemies):
        if self.attack_cooldown <= 0:
            for enemy in enemies:
                dist = math.sqrt((enemy.x + enemy.width // 2 - (self.x + self.width // 2))**2 + 
                               (enemy.y + enemy.height // 2 - (self.y + self.height // 2))**2)
                if dist < self.attack_range:
                    enemy.health -= self.damage
                    self.attack_cooldown = 40  # Более медленная атака
                    break
    
    def move_towards(self, target_x, target_y, blocks):
        dx = target_x - self.x
        dy = target_y - self.y
        dist = math.sqrt(dx**2 + dy**2)
        
        if dist > 0:
            dx /= dist
            dy /= dist
            new_x = self.x + dx * self.speed
            new_y = self.y + dy * self.speed
            
            new_rect = pygame.Rect(new_x, new_y, self.width, self.height)
            collision = False
            for block in blocks:
                if new_rect.colliderect(block.get_rect()):
                    collision = True
                    break
            
            if not collision:
                self.x = new_x
                self.y = new_y

while running:
    clock.tick(60)
    mouse_pos = pygame.mouse.get_pos()
    
    # ===== ГЛАВНОЕ МЕНЮ =====
    if game_state == 'menu':
        # ===== ГЛАВНОЕ МЕНЮ =====
        if menu_state == 'main':
            # Отрисовка меню
            # Фон с градиентом
            for y in range(HEIGHT):
                shade = int(20 + y / HEIGHT * 50)
                pygame.draw.line(screen, (shade, shade // 2, shade + 50), (0, y), (WIDTH, y))
            
            # Заголовок с красивым форматированием
            title = font_big.render("BASE DEFENSE", True, (100, 255, 100))
            subtitle = font_medium.render("Tower Builder Strategy Game", True, (150, 150, 255))
            
            title_rect = title.get_rect(center=(WIDTH // 2, 80))
            subtitle_rect = subtitle.get_rect(center=(WIDTH // 2, 150))
            
            # Рисуем декоративные линии вокруг заголовка
            pygame.draw.line(screen, (100, 255, 100), (title_rect.left - 20, title_rect.top - 10), 
                            (title_rect.left - 5, title_rect.top - 10), 3)
            pygame.draw.line(screen, (100, 255, 100), (title_rect.right + 5, title_rect.top - 10), 
                            (title_rect.right + 20, title_rect.top - 10), 3)
            
            screen.blit(title, title_rect)
            screen.blit(subtitle, subtitle_rect)
            
            # Описание режимов
            mode_descriptions = [
                ("CLASSIC", "3 enemies, balanced difficulty"),
                ("HARD", "5 enemies, intense combat"),
                ("SURVIVAL", "4 enemies, endless waves")
            ]
            
            # Обновление и отрисовка кнопок меню
            for i, button in enumerate(menu_buttons):
                button.update(mouse_pos)
                button.draw(screen)
                
                # Добавляем описание под каждой кнопкой
                desc_text = font_tiny.render(mode_descriptions[i][1], True, (200, 200, 200))
                screen.blit(desc_text, (button.rect.centerx - desc_text.get_width() // 2, button.rect.bottom + 5))
            
            # Кнопки информации и настроек
            howtoplay_btn.update(mouse_pos)
            settings_btn.update(mouse_pos)
            howtoplay_btn.draw(screen)
            settings_btn.draw(screen)
            
        # ===== ЭКРАН КАК ИГРАТЬ =====
        elif menu_state == 'howtoplay':
            # Фон
            for y in range(HEIGHT):
                shade = int(30 + y / HEIGHT * 40)
                pygame.draw.line(screen, (shade, shade, shade + 30), (0, y), (WIDTH, y))
            
            # Заголовок
            title = font_big.render("HOW TO PLAY", True, (100, 255, 100))
            screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 20))
            
            # Инструкции
            instructions = [
                "OBJECTIVE: Protect your Base Core from enemy waves",
                "",
                "BUILD MODE [Press 1]:",
                "  • Click to place blocks around your base",
                "  • Select block type from bottom-left panel",
                "  • Cost: 30-400$ depending on block type",
                "",
                "BREAK MODE [Press 2]:",
                "  • Click blocks to destroy and recover some money",
                "  • Useful for repositioning defenses",
                "",
                "WEAPON MODE [Press 3]:",
                "  • Click to attack enemies in range",
                "  • Press X/C/V/Z/F/L to switch weapons",
                "  • Different weapons have different damage & range",
                "",
                "HIRE UNITS [Bottom-Right Shop]:",
                "  • Archer: $120 - Long range, fast attacks",
                "  • Warrior: $150 - Melee, moderate damage",
                "  • Mage: $140 - Medium range, balanced",
                "  • Units auto-attack and last 10 seconds",
                "",
                "COMBAT: Defeat enemies to earn money and score",
                "PROGRESSION: Each wave gets harder with more enemies",
                "",
                "CONTROLS: WASD-Move | ESC-Menu | P-Pause"
            ]
            
            y_pos = 70
            for line in instructions:
                if line == "":
                    y_pos += 10
                else:
                    color = (100, 200, 255) if line.startswith("  ") else (200, 255, 200) if ":" in line and not line.startswith("  ") else (220, 220, 220)
                    text = font_tiny.render(line, True, color)
                    screen.blit(text, (30, y_pos))
                    y_pos += 22
            
            # Кнопка назад
            howtoplay_back_btn.update(mouse_pos)
            howtoplay_back_btn.draw(screen)
        
        # ===== ЭКРАН НАСТРОЕК =====
        elif menu_state == 'settings':
            # Фон
            for y in range(HEIGHT):
                shade = int(30 + y / HEIGHT * 40)
                pygame.draw.line(screen, (shade + 20, shade, shade), (0, y), (WIDTH, y))
            
            # Заголовок
            title = font_big.render("SETTINGS", True, (255, 200, 50))
            screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 20))
            
            # Панель настроек
            settings_panel = pygame.Rect(WIDTH // 2 - 300, 120, 600, 450)
            pygame.draw.rect(screen, (50, 40, 40), settings_panel)
            pygame.draw.rect(screen, (200, 150, 100), settings_panel, 3)
            
            # Громкость
            volume_label = font_medium.render("VOLUME", True, (255, 200, 50))
            screen.blit(volume_label, (WIDTH // 2 - 200, 150))
            
            # Ползунок громкости
            slider_rect = pygame.Rect(WIDTH // 2 - 180, 210, 360, 20)
            pygame.draw.rect(screen, (60, 60, 60), slider_rect)
            pygame.draw.rect(screen, (200, 150, 100), slider_rect, 2)
            
            # Позиция ползунка
            slider_pos = WIDTH // 2 - 180 + (volume / 100) * 360
            pygame.draw.circle(screen, (100, 255, 100), (int(slider_pos), 220), 8)
            
            volume_text = font_small.render(f"{volume}%", True, (200, 255, 200))
            screen.blit(volume_text, (slider_pos - 15, 235))
            
            # Сложность
            difficulty_label = font_medium.render("DEFAULT DIFFICULTY", True, (255, 200, 50))
            screen.blit(difficulty_label, (WIDTH // 2 - 200, 300))
            
            diff_buttons = [
                Button(WIDTH // 2 - 180, 360, 110, 40, "CLASSIC", (100, 200, 100), font_small),
                Button(WIDTH // 2 - 35, 360, 110, 40, "HARD", (200, 50, 50), font_small),
                Button(WIDTH // 2 + 110, 360, 110, 40, "SURVIVAL", (200, 150, 50), font_small),
            ]
            
            for btn in diff_buttons:
                btn.update(mouse_pos)
                btn.draw(screen)
            
            current_diff = font_small.render(f"Currently: {difficulty_display}", True, (200, 255, 200))
            screen.blit(current_diff, (WIDTH // 2 - 100, 420))
            
            # Кнопка назад
            settings_back_btn.update(mouse_pos)
            settings_back_btn.draw(screen)
        
        # Обработка событий меню
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if menu_state == 'main':
                    # Кнопки режимов
                    if menu_buttons[0].is_clicked(mouse_pos):  # Classic Mode
                        game_state = 'playing'
                        game_difficulty = 'normal'
                        difficulty_display = 'CLASSIC'
                        init_game()
                    elif menu_buttons[1].is_clicked(mouse_pos):  # Hard Mode
                        game_state = 'playing'
                        game_difficulty = 'hard'
                        difficulty_display = 'HARD'
                        init_game()
                    elif menu_buttons[2].is_clicked(mouse_pos):  # Survival Mode
                        game_state = 'playing'
                        game_difficulty = 'survival'
                        difficulty_display = 'SURVIVAL'
                        init_game()
                    # Кнопки навигации
                    elif howtoplay_btn.is_clicked(mouse_pos):
                        menu_state = 'howtoplay'
                    elif settings_btn.is_clicked(mouse_pos):
                        menu_state = 'settings'
                
                elif menu_state == 'howtoplay':
                    if howtoplay_back_btn.is_clicked(mouse_pos):
                        menu_state = 'main'
                
                elif menu_state == 'settings':
                    if settings_back_btn.is_clicked(mouse_pos):
                        menu_state = 'main'
                    
                    # Обработка изменения сложности
                    diff_buttons = [
                        Button(WIDTH // 2 - 180, 360, 110, 40, "CLASSIC", (100, 200, 100), font_small),
                        Button(WIDTH // 2 - 35, 360, 110, 40, "HARD", (200, 50, 50), font_small),
                        Button(WIDTH // 2 + 110, 360, 110, 40, "SURVIVAL", (200, 150, 50), font_small),
                    ]
                    if diff_buttons[0].is_clicked(mouse_pos):
                        difficulty_display = 'CLASSIC'
                    elif diff_buttons[1].is_clicked(mouse_pos):
                        difficulty_display = 'HARD'
                    elif diff_buttons[2].is_clicked(mouse_pos):
                        difficulty_display = 'SURVIVAL'
            
            # Обработка ползунка громкости при движении мыши
            elif event.type == pygame.MOUSEMOTION and menu_state == 'settings':
                slider_rect = pygame.Rect(WIDTH // 2 - 180, 210, 360, 20)
                if slider_rect.collidepoint(event.pos):
                    if pygame.mouse.get_pressed()[0]:  # Левая кнопка мыши нажата
                        # Обновляем громкость на основе позиции мыши
                        relative_x = event.pos[0] - slider_rect.left
                        volume = max(0, min(100, int((relative_x / slider_rect.width) * 100)))
    
    # ===== ОСНОВНАЯ ИГРА =====
    elif game_state == 'playing':
        if not game_over and not game_won:
            # Логика волн врагов
            wave_timer += 1
            if wave_timer >= wave_delay and enemies_spawned < enemies_per_wave:
                spawn_enemy()
                enemies_spawned += 1
                wave_timer = 0
            
            # Проверка завершения волны
            if len(enemies) == 0 and enemies_spawned >= enemies_per_wave:
                wave += 1
                enemies_spawned = 0
                wave_timer = 0
                
                # Увеличение сложности по волнам и изменение скорости спавна
                if game_difficulty == 'normal':
                    enemies_per_wave = 3 + (wave // 2) * 2
                    wave_delay = max(90, 180 - wave * 5)  # Спавн становится быстрее
                elif game_difficulty == 'hard':
                    enemies_per_wave = 5 + (wave // 2) * 3
                    wave_delay = max(60, 150 - wave * 8)  # Еще быстрее
                else:  # survival
                    enemies_per_wave = 4 + (wave // 2) * 4
                    wave_delay = max(50, 120 - wave * 6)  # И еще быстрее
                
                # Бонус за волну
                player.money += 200 * wave
            
            # Движение врагов
            for enemy in enemies:
                enemy.update_cooldown()
                enemy.move_towards(player.x + player.width // 2, player.y + player.height // 2, blocks)
                
                nearest_block = enemy.find_nearest_block(blocks)
                if enemy.attack_block(nearest_block):
                    blocks.remove(nearest_block)
                    for _ in range(8):
                        particles.append(Particle(nearest_block.x + nearest_block.width // 2, 
                                                nearest_block.y + nearest_block.height // 2, 
                                                nearest_block.color))
                
                if enemy.get_rect().colliderect(player.get_rect()):
                    damage = enemy.damage
                    if player.shield_active <= 0:
                        player.health -= damage / 60
                
                if enemy.get_rect().colliderect(base_rect):
                    player.health -= enemy.damage / 60
            
            # Удаление мёртвых врагов
            for enemy in enemies[:]:
                if enemy.health <= 0:
                    enemies.remove(enemy)
                    score += 100
                    spawn_loot(enemy.x + enemy.width // 2, enemy.y + enemy.height // 2)
                    for _ in range(5):
                        particles.append(Particle(enemy.x + enemy.width // 2, enemy.y + enemy.height // 2, RED))
            
            # NPC атаки и движение (преследование врагов)
            for npc in npcs:
                npc.update_cooldown()
                
                # Ищем ближайшего врага
                nearest_enemy = npc.find_nearest_enemy(enemies)
                if nearest_enemy:
                    # Преследуем врага
                    npc.move_towards(nearest_enemy.x + nearest_enemy.width // 2, 
                                   nearest_enemy.y + nearest_enemy.height // 2, blocks)
                    npc.attack(enemies)
                else:
                    # Если врагов нет, двигаемся к центру
                    npc.move_towards(WIDTH // 2, HEIGHT // 2, blocks)
            
            # Удаление мёртвых NPC или истекшего времени жизни
            for npc in npcs[:]:
                if npc.health <= 0 or npc.lifetime <= 0:
                    npcs.remove(npc)
                    score += 50
            
            # Обновление снарядов
            for projectile in projectiles[:]:
                projectile.update()
                
                # Проверка столкновения с врагами
                for enemy in enemies[:]:
                    if projectile.get_rect().colliderect(enemy.get_rect()):
                        enemy.health -= projectile.damage
                        projectiles.remove(projectile)
                        particles.append(Particle(projectile.x, projectile.y, projectile.color))
                        break
                
                # Удаление снарядов, вышедших из области видимости
                if not projectile.is_alive() or projectile.x < -50 or projectile.x > WIDTH + 50 or projectile.y < -50 or projectile.y > HEIGHT + 50:
                    if projectile in projectiles:
                        projectiles.remove(projectile)
            
            # Проверка конца игры
            if player.health <= 0:
                game_over = True
            
            # Обновление лута
            for loot in loots[:]:
                loot.update()
                if loot.is_colliding(player.get_rect()):
                    if loot.loot_type == 'coins':
                        player.money += loot.value
                    elif loot.loot_type == 'health':
                        player.health = min(player.max_health, player.health + loot.value)
                    elif loot.loot_type in ['wood', 'stone']:
                        player.money += loot.value
                    
                    loots.remove(loot)
                    particles.append(Particle(loot.x, loot.y, loot.color))
                elif loot.y > HEIGHT + 50:
                    loots.remove(loot)
            
            # Обновление power-ups
            for powerup in powerups[:]:
                powerup.update()
                if powerup.is_colliding(player.get_rect()):
                    if powerup.powerup_type == 'speed':
                        player.speed_boost = 300
                    elif powerup.powerup_type == 'shield':
                        player.shield_active = 400
                    elif powerup.powerup_type == 'mega_strike':
                        player.mega_strike = 1
                    
                    powerups.remove(powerup)
                    for _ in range(10):
                        particles.append(Particle(powerup.x, powerup.y, powerup.color))
                elif powerup.y > HEIGHT + 50:
                    powerups.remove(powerup)
        
        # События игры
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_state = 'menu'
                    paused = False
                elif event.key == pygame.K_p:
                    paused = not paused
                elif event.key == pygame.K_1 and not paused:
                    player.mode = 'build'
                elif event.key == pygame.K_2 and not paused:
                    player.mode = 'break'
                elif event.key == pygame.K_3 and not paused:
                    player.mode = 'weapon'
                elif event.key in [pygame.K_x, pygame.K_c, pygame.K_v, pygame.K_z, pygame.K_f, pygame.K_l] and not paused:
                    if event.key == pygame.K_x:
                        player.weapon_type = 'sword'
                    elif event.key == pygame.K_c:
                        player.weapon_type = 'axe'
                    elif event.key == pygame.K_v:
                        player.weapon_type = 'spear'
                    elif event.key == pygame.K_z:
                        player.weapon_type = 'sniper'
                    elif event.key == pygame.K_f:
                        player.weapon_type = 'hammer'
                    elif event.key == pygame.K_l:
                        player.weapon_type = 'laser'
                    player.weapon_damage = player.weapons[player.weapon_type]['damage']
                    player.weapon_range = player.weapons[player.weapon_type]['range']
                    player.weapon_cooldown_max = player.weapons[player.weapon_type]['cooldown']
                elif event.key == pygame.K_SPACE and (game_over or game_won):
                    game_state = 'menu'
                    game_over = False
                    game_won = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not paused:
                if player.mode == 'weapon':
                    player.attack(enemies)
                else:
                    clicked_button = False
                    for block_type, button in buttons.items():
                        if button.is_clicked(mouse_pos):
                            player.selected_block = block_type
                            clicked_button = True
                            break
                    
                    for npc_type, button in npc_buttons.items():
                        if button.is_clicked(mouse_pos):
                            if player.money >= npc_costs[npc_type]:
                                player.money -= npc_costs[npc_type]
                                npcs.append(NPC(player.x - 40, player.y, npc_type))
                            clicked_button = True
                            break
                    
                    if not clicked_button:
                        if player.mode == 'build':
                            grid_x = (mouse_pos[0] // Block.BLOCK_SIZE) * Block.BLOCK_SIZE
                            grid_y = (mouse_pos[1] // Block.BLOCK_SIZE) * Block.BLOCK_SIZE
                            
                            occupied = False
                            for block in blocks:
                                if block.x == grid_x and block.y == grid_y:
                                    occupied = True
                                    break
                            
                            cost = Block.BLOCK_TYPES[player.selected_block]['cost']
                            if not occupied and player.money >= cost:
                                new_block = Block(grid_x, grid_y, player.selected_block)
                                blocks.append(new_block)
                                player.money -= cost
                                for _ in range(3):
                                    particles.append(Particle(grid_x + Block.BLOCK_SIZE // 2, grid_y + Block.BLOCK_SIZE // 2, new_block.color))
                        
                        elif player.mode == 'break':
                            for block in blocks[:]:
                                if block.is_clicked(mouse_pos):
                                    blocks.remove(block)
                                    player.money += 30
                                    for _ in range(5):
                                        particles.append(Particle(block.x + Block.BLOCK_SIZE // 2, block.y + Block.BLOCK_SIZE // 2, block.color))
                                    break
        
        # Обновление игрока
        keys = pygame.key.get_pressed()
        if not paused:
            if keys[pygame.K_w]:
                player.move(0, -player.speed, blocks)
            if keys[pygame.K_s]:
                player.move(0, player.speed, blocks)
            if keys[pygame.K_a]:
                player.move(-player.speed, 0, blocks)
            if keys[pygame.K_d]:
                player.move(player.speed, 0, blocks)
        
        player.update_cooldown()
        
        # Обновление частиц
        for particle in particles[:]:
            particle.update()
            if particle.life <= 0:
                particles.remove(particle)
        
        # Обновление кнопок
        for button in buttons.values():
            button.update(mouse_pos)
        for button in npc_buttons.values():
            button.update(mouse_pos)
        
        # === ОТРИСОВКА ИГРЫ ===
        # Небо с градиентом
        for y in range(HEIGHT // 2):
            color = (135, 206 - y // 5, 250)
            pygame.draw.line(screen, color, (0, y), (WIDTH, y))
        
        # Земля
        for y in range(HEIGHT // 2, HEIGHT):
            shade = int(34 + (y - HEIGHT // 2) / (HEIGHT // 2) * 50)
            pygame.draw.line(screen, (0, shade, 0), (0, y), (WIDTH, y))
        
        # Блоки
        sorted_blocks = sorted(blocks, key=lambda b: b.y)
        for block in sorted_blocks:
            block.draw(screen)
        
        # Игрок
        player.draw(screen)
        
        # NPC
        for npc in npcs:
            npc.draw(screen)
        
        # Частицы
        for particle in particles:
            particle.draw(screen)
        
        # Враги
        for enemy in enemies:
            enemy.draw(screen)
        
        # Лут
        for loot in loots:
            loot.draw(screen)
        
        # Power-ups
        for powerup in powerups:
            powerup.draw(screen)
        
        # Снаряды
        for projectile in projectiles:
            projectile.draw(screen)
        
        # === ИНТЕРФЕЙС В ИГРЕ ===
        
        # Блоки меню (внизу слева)
        # Рисуем блок с содержимым
        block_panel_rect = pygame.Rect(5, HEIGHT - 105, 340, 100)
        pygame.draw.rect(screen, (30, 30, 30), block_panel_rect)
        pygame.draw.rect(screen, (100, 150, 100), block_panel_rect, 2)
        block_label = font_tiny.render('BUILDING BLOCKS', True, (100, 200, 100))
        screen.blit(block_label, (15, HEIGHT - 102))
        for button in buttons.values():
            button.draw(screen)
        
        # NPC кнопки (внизу справа) - панель магазина
        shop_panel_rect = pygame.Rect(WIDTH - 230, HEIGHT - 105, 225, 100)
        pygame.draw.rect(screen, (30, 30, 30), shop_panel_rect)
        pygame.draw.rect(screen, (150, 100, 50), shop_panel_rect, 2)
        
        # Заголовок магазина
        shop_title = font_tiny.render("SHOP - HIRE UNITS", True, (255, 200, 50))
        screen.blit(shop_title, (WIDTH - 220, HEIGHT - 102))
        
        for button in npc_buttons.values():
            button.draw(screen)
        
        # Информационная панель сверху
        # Левая часть - волны и очки
        wave_text = f"WAVE {wave}"
        enemies_text = f"Enemies: {len(enemies)}"
        score_text = f"SCORE: {score}"
        
        screen.blit(font_medium.render(wave_text, True, (255, 100, 100)), (15, 10))
        screen.blit(font_small.render(enemies_text, True, (255, 150, 100)), (15, 48))
        screen.blit(font_medium.render(score_text, True, (100, 255, 100)), (15, 75))
                # Центр - база
        pygame.draw.rect(screen, YELLOW, base_rect)
        pygame.draw.rect(screen, BLACK, base_rect, 3)
        base_text = font_tiny.render("BASE CORE", True, BLACK)
        screen.blit(base_text, (base_rect.centerx - 28, base_rect.centery - 10))
        
        # Правая часть - здоровье и деньги
        money_text = f"MONEY: ${int(player.money)}"
        health_text = f"HEALTH: {int(player.health)}/{int(player.max_health)}"
        npcs_count = f"Active Units: {len(npcs)}"
        
        screen.blit(font_medium.render(money_text, True, YELLOW), (WIDTH - 320, 10))
        screen.blit(font_medium.render(health_text, True, RED), (WIDTH - 320, 50))
        screen.blit(font_small.render(npcs_count, True, (150, 200, 255)), (WIDTH - 320, 80))
        
        # Информационная панель справа посередине
        mode_names = {'build': 'BUILD [1]', 'break': 'BREAK [2]', 'weapon': 'WEAPON [3]'}
        mode_display = f"MODE: {mode_names[player.mode]}"
        screen.blit(font_small.render(mode_display, True, (100, 200, 255)), (WIDTH - 320, HEIGHT // 2 - 60))
        
        # Оружие (если активно)
        if player.mode == 'weapon':
            weapon_display = f"WEAPON: {player.weapon_type.upper()}"
            dmg_display = f"DAMAGE: {player.weapon_damage} | RANGE: {player.weapon_range}"
            screen.blit(font_small.render(weapon_display, True, (255, 150, 50)), (WIDTH - 320, HEIGHT // 2 - 20))
            screen.blit(font_small.render(dmg_display, True, (255, 100, 50)), (WIDTH - 320, HEIGHT // 2 + 10))
        
        # Баффы (справа посередине)
        if player.speed_boost > 0 or player.shield_active > 0:
            buff_display = ""
            if player.speed_boost > 0:
                buff_display += f"SPEED BOOST: {player.speed_boost//60}s\n"
            if player.shield_active > 0:
                buff_display += f"SHIELD: {player.shield_active//60}s"
            
            y_offset = HEIGHT // 2 + 60
            for line in buff_display.split('\n'):
                if line.strip():
                    screen.blit(font_small.render(line, True, (100, 200, 255)), (WIDTH - 320, y_offset))
                    y_offset += 30
        
        # Контролы внизу в центре
        controls_text = "WASD-Move | ESC-Menu | P-Pause | LMB-Action | 1/2/3-Modes | X/C/V/Z/F/L-Weapons"
        screen.blit(font_tiny.render(controls_text, True, (150, 150, 150)), (WIDTH // 2 - 330, HEIGHT - 24))
        
        # === ЭКРАН ПАУЗЫ ===
        if paused:
            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.set_alpha(200)
            overlay.fill(BLACK)
            screen.blit(overlay, (0, 0))
            
            # Фон для текста паузы
            pause_box = pygame.Rect(WIDTH // 2 - 250, HEIGHT // 2 - 100, 500, 200)
            pygame.draw.rect(screen, (50, 50, 50), pause_box)
            pygame.draw.rect(screen, (255, 200, 50), pause_box, 4)
            
            pause_text = font_big.render("PAUSED", True, (255, 200, 50))
            resume_text = font_medium.render("Press P to Resume", True, WHITE)
            menu_text = font_medium.render("Press ESC for Menu", True, WHITE)
            
            screen.blit(pause_text, (WIDTH // 2 - pause_text.get_width() // 2, HEIGHT // 2 - 75))
            screen.blit(resume_text, (WIDTH // 2 - resume_text.get_width() // 2, HEIGHT // 2 - 10))
            screen.blit(menu_text, (WIDTH // 2 - menu_text.get_width() // 2, HEIGHT // 2 + 40))
        
        # === ЭКРАН ПОРАЖЕНИЯ ===
        if game_over:
            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.set_alpha(220)
            overlay.fill(BLACK)
            screen.blit(overlay, (0, 0))
            
            # Фон для текста поражения
            game_box = pygame.Rect(WIDTH // 2 - 350, HEIGHT // 2 - 120, 700, 240)
            pygame.draw.rect(screen, (80, 20, 20), game_box)
            pygame.draw.rect(screen, RED, game_box, 4)
            
            game_over_text = font_big.render("BASE DESTROYED!", True, RED)
            wave_result = font_medium.render(f"Waves Survived: {wave - 1}", True, WHITE)
            final_score = font_medium.render(f"Final Score: {score}", True, (100, 255, 100))
            restart_text = font_small.render("Press SPACE to Return to Menu", True, WHITE)
            
            screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 100))
            screen.blit(wave_result, (WIDTH // 2 - wave_result.get_width() // 2, HEIGHT // 2 - 20))
            screen.blit(final_score, (WIDTH // 2 - final_score.get_width() // 2, HEIGHT // 2 + 25))
            screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 85))
        
        # === ЭКРАН ПОБЕДЫ ===
        if game_won:
            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.set_alpha(220)
            overlay.fill(BLACK)
            screen.blit(overlay, (0, 0))
            
            # Фон для текста победы
            win_box = pygame.Rect(WIDTH // 2 - 350, HEIGHT // 2 - 120, 700, 240)
            pygame.draw.rect(screen, (20, 80, 20), win_box)
            pygame.draw.rect(screen, (100, 255, 100), win_box, 4)
            
            won_text = font_big.render("NEW RECORD!", True, YELLOW)
            wave_result = font_medium.render(f"Waves Survived: {wave - 1}", True, WHITE)
            final_score = font_medium.render(f"Final Score: {score}", True, (100, 255, 100))
            restart_text = font_small.render("Press SPACE to Return to Menu", True, WHITE)
            
            screen.blit(won_text, (WIDTH // 2 - won_text.get_width() // 2, HEIGHT // 2 - 100))
            screen.blit(wave_result, (WIDTH // 2 - wave_result.get_width() // 2, HEIGHT // 2 - 20))
            screen.blit(final_score, (WIDTH // 2 - final_score.get_width() // 2, HEIGHT // 2 + 25))
            screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 85))
    
    pygame.display.flip()

pygame.quit()
sys.exit()
