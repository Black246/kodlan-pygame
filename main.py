import pygame
import random
import sys

# Inicializar Pygame
pygame.init()

# Dimensiones de la pantalla
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Invaders")

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Cargar imágenes
try:
    player_img = pygame.image.load("assets/player.png")
    enemy_img = pygame.image.load("assets/enemy.png")
    bullet_img = pygame.image.load("assets/bullet.png")
    print(f"Tamaño de enemy_img: {enemy_img.get_width()}x{enemy_img.get_height()}")
except pygame.error as e:
    print(f"Error al cargar una imagen: {e}")
    pygame.quit()
    sys.exit()

# Variables del juego
player_x = SCREEN_WIDTH // 2
player_y = SCREEN_HEIGHT - 100
player_speed = 5

bullets = []
bullet_speed = 7

enemies = []
enemy_speed = 1
enemy_spawn_time = 1000  # milisegundos
last_enemy_spawn = pygame.time.get_ticks()

score = 0

# Funciones personalizadas

def draw_text(text, size, x, y):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, WHITE)
    screen.blit(text_surface, (x, y))

def player(x, y):
    screen.blit(player_img, (x, y))

def shoot_bullet(x, y):
    bullets.append([x, y])

def spawn_enemy():
    if enemy_img.get_width() >= SCREEN_WIDTH:
        print("Error: El ancho de la imagen de enemigo es mayor o igual al ancho de la pantalla.")
        x = 0  # Posición predeterminada para evitar error
    else:
        x = random.randint(0, SCREEN_WIDTH - enemy_img.get_width())
    y = random.randint(-100, -40)
    enemies.append([x, y])

def move_enemies():
    global score
    for enemy in enemies[:]:
        enemy[1] += enemy_speed
        if enemy[1] > SCREEN_HEIGHT:
            enemies.remove(enemy)
            score -= 1  # Penalización por dejar pasar un enemigo

def check_collisions():
    global score
    for bullet in bullets[:]:
        bullet_rect = pygame.Rect(bullet[0], bullet[1], bullet_img.get_width(), bullet_img.get_height())
        for enemy in enemies[:]:
            enemy_rect = pygame.Rect(enemy[0], enemy[1], enemy_img.get_width(), enemy_img.get_height())
            if bullet_rect.colliderect(enemy_rect):
                bullets.remove(bullet)
                enemies.remove(enemy)
                score += 1
                break

# Menú de inicio
def show_start_menu():
    screen.fill(BLACK)
    draw_text("SPACE INVADERS", 64, SCREEN_WIDTH // 4, SCREEN_HEIGHT // 4)
    draw_text("Press ENTER to start", 32, SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2)
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    waiting = False

# Bucle principal del juego
def game_loop():
    global player_x, player_y, last_enemy_spawn

    running = True
    while running:
        screen.fill(BLACK)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    shoot_bullet(player_x + player_img.get_width() // 2, player_y)
        
        # Movimiento del jugador
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < SCREEN_WIDTH - player_img.get_width():
            player_x += player_speed

        # Disparos
        for bullet in bullets[:]:
            bullet[1] -= bullet_speed
            if bullet[1] < 0:
                bullets.remove(bullet)

        # Aparición de enemigos
        current_time = pygame.time.get_ticks()
        if current_time - last_enemy_spawn > enemy_spawn_time:
            spawn_enemy()
            last_enemy_spawn = current_time
        
        move_enemies()
        check_collisions()

        # Dibujar elementos
        player(player_x, player_y)
        for bullet in bullets:
            screen.blit(bullet_img, bullet)
        for enemy in enemies:
            screen.blit(enemy_img, enemy)

        # Mostrar puntuación
        draw_text(f"Score: {score}", 32, 10, 10)

        pygame.display.flip()
        pygame.time.Clock().tick(60)
    
    pygame.quit()
    sys.exit()

# Ejecutar el menú y el juego
show_start_menu()
game_loop()
