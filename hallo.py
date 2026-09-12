import pygame
import random

# Memulai Pygame
pygame.init()

# Ukuran layar
LEBAR = 800
TINGGI = 600
layar = pygame.display.set_mode((LEBAR, TINGGI))
pygame.display.set_caption("Tangkap Koin!")

# Warna
HITAM = (20, 20, 20)
PUTIH = (255, 255, 255)
BIRU = (50, 150, 255)
KUNING = (255, 220, 0)
MERAH = (255, 60, 60)

# Pemain
pemain = pygame.Rect(350, 520, 100, 40)
kecepatan = 7

# Koin
koin = pygame.Rect(
    random.randint(0, LEBAR - 30),
    0,
    30,
    30
)
kecepatan_koin = 5

# Skor
skor = 0
font = pygame.font.Font(None, 40)

# Game Over
game_over = False

# FPS
clock = pygame.time.Clock()

# Game loop
berjalan = True

while berjalan:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            berjalan = False

        # Tekan ENTER untuk mulai lagi
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN and game_over:
                skor = 0
                pemain.x = 350
                koin.x = random.randint(0, LEBAR - 30)
                koin.y = 0
                game_over = False

    # Jika game masih berjalan
    if not game_over:
        # Kontrol pemain
        tombol = pygame.key.get_pressed()

        if tombol[pygame.K_LEFT]:
            pemain.x -= kecepatan

        if tombol[pygame.K_RIGHT]:
            pemain.x += kecepatan

        # Batas layar
        if pemain.left < 0:
            pemain.left = 0

        if pemain.right > LEBAR:
            pemain.right = LEBAR

        # Koin jatuh
        koin.y += kecepatan_koin

        # Jika koin tertangkap
        if pemain.colliderect(koin):
            skor += 1

            koin.x = random.randint(0, LEBAR - 30)
            koin.y = 0

            # Koin semakin cepat
            kecepatan_koin += 0.3

        # Jika koin jatuh ke bawah
        if koin.top > TINGGI:
            game_over = True

    # Background
    layar.fill(HITAM)

    # Gambar pemain
    pygame.draw.rect(layar, BIRU, pemain)

    # Gambar koin
    if not game_over:
        pygame.draw.ellipse(layar, KUNING, koin)

    # Menampilkan skor
    teks_skor = font.render(f"Skor: {skor}", True, PUTIH)
    layar.blit(teks_skor, (20, 20))

    # Game Over
    if game_over:
        teks_game_over = font.render(
            "GAME OVER!",
            True,
            MERAH
        )

        teks_restart = font.render(
            "Tekan ENTER untuk bermain lagi",
            True,
            PUTIH
        )

        layar.blit(
            teks_game_over,
            (LEBAR // 2 - 100, 250)
        )

        layar.blit(
            teks_restart,
            (LEBAR // 2 - 200, 300)
        )

    # Update layar
    pygame.display.update()

    # FPS
    clock.tick(60)

pygame.quit()
