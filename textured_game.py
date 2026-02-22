import pygame
import sys

pygame.init()
WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Texture Adventure")
clock = pygame.time.Clock()

BG_COLOR = (40, 40, 80)
TILE_COLOR = (120, 180, 120)
PLAYER_COLOR = (220, 60, 60)
BLOCK_COLOR = (180, 120, 60)

player_pos = [WIDTH//2, HEIGHT//2]
player_speed = 5
font = pygame.font.SysFont(None, 36)
blocks = []  # список построенных блоков

def draw():
    screen.fill(BG_COLOR)
    for x in range(0, WIDTH, 64):
        for y in range(0, HEIGHT, 64):
            pygame.draw.rect(screen, TILE_COLOR, (x, y, 64, 64))
    for b in blocks:
        pygame.draw.rect(screen, BLOCK_COLOR, b)
    pygame.draw.circle(screen, PLAYER_COLOR, player_pos, 32)
    info = font.render("ЛКМ — строить, ПКМ — ломать", True, (255,255,255))
    screen.blit(info, (10, 10))
    pygame.display.flip()

def handle_input():
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_pos[0] -= player_speed
    if keys[pygame.K_RIGHT]:
        player_pos[0] += player_speed
    if keys[pygame.K_UP]:
        player_pos[1] -= player_speed
    if keys[pygame.K_DOWN]:
        player_pos[1] += player_speed

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos
            grid_x = mx // 64 * 64
            grid_y = my // 64 * 64
            block_rect = pygame.Rect(grid_x, grid_y, 64, 64)
            if event.button == 1:
                # ЛКМ — строить
                if block_rect not in blocks:
                    blocks.append(block_rect)
            elif event.button == 3:
                # ПКМ — ломать
                for b in blocks:
                    if b.collidepoint(mx, my):
                        blocks.remove(b)
                        break
    handle_input()
    draw()
    clock.tick(60)

pygame.quit()
