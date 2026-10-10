import pygame
import random
import sys
import os

# Inisialisasi Pygame
pygame.init()

# Konfigurasi Layar
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Game Menangkap Buah Jatuh")

# Pengaturan Warna (RGB)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 120, 255)

# Kecepatan Frame (FPS)
clock = pygame.time.Clock()
FPS = 60

# --- LOAD ASSET GAMBAR ---
ASSET_DIR = os.path.dirname(os.path.abspath(__file__))

def load_image(name, size=None, convert_alpha=True):
    path = os.path.join(ASSET_DIR, name)
    img = pygame.image.load(path)
    img = img.convert_alpha() if convert_alpha else img.convert()
    if size:
        img = pygame.transform.smoothscale(img, size)
    return img

# Background
background_img = load_image("background.jpg", (SCREEN_WIDTH, SCREEN_HEIGHT), convert_alpha=False)

# Pengaturan Keranjang (Player)
basket_width = 100
basket_height = 30
basket_x = SCREEN_WIDTH // 2 - basket_width // 2
basket_y = SCREEN_HEIGHT - 50
basket_speed = 8
basket_img = load_image("keranjang.png", (basket_width, basket_height))

# Pengaturan Buah (5 gambar berbeda)
fruit_radius = 15
fruit_size = fruit_radius * 2
fruit_images = [load_image(f"buah{i}.png", (fruit_size, fruit_size)) for i in range(1, 6)]

fruit_x = random.randint(fruit_radius, SCREEN_WIDTH - fruit_radius)
fruit_y = -50
fruit_speed = 5
current_fruit_img = random.choice(fruit_images)

# Skor, Nyawa, Missed, dan Goal
score = 0
lives = 3
missed = 0
GOAL = 50  # jumlah buah yang harus ditangkap untuk menang
font = pygame.font.SysFont(None, 36)
big_font = pygame.font.SysFont(None, 80)


def reset_fruit():
    """Reset posisi buah ke atas dan pilih gambar buah baru secara acak."""
    global fruit_x, fruit_y, current_fruit_img
    fruit_y = -50
    fruit_x = random.randint(fruit_radius, SCREEN_WIDTH - fruit_radius)
    current_fruit_img = random.choice(fruit_images)


def show_end_screen(message, color):
    """Tampilkan layar akhir (menang/kalah) lalu keluar dari game."""
    screen.blit(background_img, (0, 0))
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    overlay.set_alpha(160)
    overlay.fill(BLACK)
    screen.blit(overlay, (0, 0))

    text_surface = big_font.render(message, True, color)
    text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30))
    screen.blit(text_surface, text_rect)

    score_surface = font.render(f"Skor Akhir: {score}   Missed: {missed}", True, WHITE)
    score_rect = score_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40))
    screen.blit(score_surface, score_rect)

    pygame.display.flip()
    pygame.time.delay(3000)
    pygame.quit()
    sys.exit()


# --- LOOP UTAMA GAME ---
running = True
while running:
    # 1. Penanganan Input (Event Handling)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Kontrol Gerakan Keranjang (Tombol Panah Kiri & Kanan)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and basket_x > 0:
        basket_x -= basket_speed
    if keys[pygame.K_RIGHT] and basket_x < SCREEN_WIDTH - basket_width:
        basket_x += basket_speed

    # 2. Pembaruan Posisi Objek (Update Logic)
    # Buah jatuh ke bawah
    fruit_y += fruit_speed

    # Cek jika buah jatuh menyentuh tanah (Missed)
    if fruit_y > SCREEN_HEIGHT:
        lives -= 1
        missed += 1
        reset_fruit()

        # Cek Game Over (Kalah)
        if lives <= 0:
            show_end_screen("YOU LOSE", RED)

    # Cek Tabrakan (Collision) antara Buah dan Keranjang
    if (basket_x < fruit_x < basket_x + basket_width) and \
       (basket_y <= fruit_y + fruit_radius <= basket_y + basket_height):
        score += 1
        fruit_speed += 0.2  # Tingkatkan kesulitan sedikit demi sedikit
        reset_fruit()

        # Cek Kondisi Menang
        if score >= GOAL:
            show_end_screen("YOU WIN", GREEN)

    # 3. Proses Rendering (Menggambar ke Layar)
    screen.blit(background_img, (0, 0))

    # Gambar Keranjang
    screen.blit(basket_img, (basket_x, basket_y))

    # Gambar Buah
    screen.blit(current_fruit_img, (fruit_x - fruit_radius, int(fruit_y) - fruit_radius))

    # Tampilkan Skor & Missed di pojok kiri atas
    score_text = font.render(f"Skor: {score} / {GOAL}", True, BLACK)
    missed_text = font.render(f"Missed: {missed}", True, BLACK)
    screen.blit(score_text, (20, 20))
    screen.blit(missed_text, (20, 55))

    # Tampilkan Nyawa di pojok kanan atas
    lives_text = font.render(f"Nyawa: {lives}", True, BLACK)
    screen.blit(lives_text, (SCREEN_WIDTH - 140, 20))

    # Perbarui Tampilan Layar
    pygame.display.flip()

    # Batasi kecepatan frame per detik
    clock.tick(FPS)
