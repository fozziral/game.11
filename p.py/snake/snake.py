import pygame
import random
import sys

pygame.init()

# =========================
# PENGATURAN GAME
# =========================
GRID_SIZE = 17
CELL_SIZE = 40

WIDTH = GRID_SIZE * CELL_SIZE
HEIGHT = GRID_SIZE * CELL_SIZE

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake 17 x 17")

clock = pygame.time.Clock()

# Warna
BG_COLOR = (30, 30, 30)
GRID_COLOR = (55, 55, 55)
SNAKE_COLOR = (50, 200, 70)
HEAD_COLOR = (80, 240, 90)
GRAPE_COLOR = (160, 60, 220)
TEXT_COLOR = (255, 255, 255)
GAMEOVER_COLOR = (220, 60, 60)
WIN_COLOR = (60, 220, 100)

font = pygame.font.SysFont(None, 32)
big_font = pygame.font.SysFont(None, 55)


# =========================
# MEMBUAT ANGGUR
# =========================
def buat_anggur(jumlah, snake):
    grapes = []

    while len(grapes) < jumlah:
        posisi = (
            random.randint(0, GRID_SIZE - 1),
            random.randint(0, GRID_SIZE - 1)
        )

        if posisi not in snake and posisi not in grapes:
            grapes.append(posisi)

    return grapes


# =========================
# RESET GAME
# =========================
def reset_game():
    snake = [(7, 7), (6, 7), (5, 7)]

    direction = (1, 0)
    next_direction = direction

    grapes = buat_anggur(1, snake)

    return snake, direction, next_direction, grapes


# =========================
# MENENTUKAN JUMLAH ANGGUR
# =========================
def jumlah_anggur(panjang):
    # Awalnya 1 anggur
    # Setiap 5 panjang, jumlah anggur bertambah 1
    jumlah = 1 + (panjang // 5)

    # Maksimal 10 anggur
    return min(jumlah, 10)


# =========================
# GAME UTAMA
# =========================
snake, direction, next_direction, grapes = reset_game()

game_over = False
win = False

running = True

while running:

    # =========================
    # EVENT
    # =========================
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            # Restart
            if event.key == pygame.K_r:
                snake, direction, next_direction, grapes = reset_game()
                game_over = False
                win = False

            # Jika game sedang berjalan
            if not game_over and not win:

                if event.key in (pygame.K_UP, pygame.K_w):
                    if direction != (0, 1):
                        next_direction = (0, -1)

                elif event.key in (pygame.K_DOWN, pygame.K_s):
                    if direction != (0, -1):
                        next_direction = (0, 1)

                elif event.key in (pygame.K_LEFT, pygame.K_a):
                    if direction != (1, 0):
                        next_direction = (-1, 0)

                elif event.key in (pygame.K_RIGHT, pygame.K_d):
                    if direction != (-1, 0):
                        next_direction = (1, 0)


    # =========================
    # LOGIKA ULAR
    # =========================
    if not game_over and not win:

        direction = next_direction

        kepala_x, kepala_y = snake[0]

        new_head = (
            (kepala_x + direction[0]) % GRID_SIZE,
            (kepala_y + direction[1]) % GRID_SIZE
        )

        if new_head in snake:
            game_over = True

        else:

            snake.insert(0, new_head)

            # =========================
            # CEK MAKAN ANGGUR
            # =========================
            if new_head in grapes:

                grapes.remove(new_head)

                # Jumlah anggur mengikuti panjang ular
                target_grapes = jumlah_anggur(len(snake))

                # Tambahkan anggur jika jumlahnya kurang
                tambahan = target_grapes - len(grapes)

                if tambahan > 0:
                    grapes.extend(
                        buat_anggur(tambahan, snake + grapes)
                    )

            else:
                # Jika tidak makan, ekor dihapus
                snake.pop()

            # =========================
            # CEK MENANG
            # =========================
            if len(snake) >= GRID_SIZE * GRID_SIZE:
                win = True

    # =========================
    # GAMBAR BACKGROUND
    # =========================
    screen.fill(BG_COLOR)

    # =========================
    # GAMBAR GRID
    # =========================
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):

            rect = pygame.Rect(
                x * CELL_SIZE,
                y * CELL_SIZE,
                CELL_SIZE,
                CELL_SIZE
            )

            pygame.draw.rect(
                screen,
                GRID_COLOR,
                rect,
                1
            )

    # =========================
    # GAMBAR ANGGUR
    # =========================
    for grape in grapes:

        x, y = grape

        center_x = x * CELL_SIZE + CELL_SIZE // 2
        center_y = y * CELL_SIZE + CELL_SIZE // 2

        # Buah anggur
        pygame.draw.circle(
            screen,
            GRAPE_COLOR,
            (center_x - 6, center_y),
            6
        )

        pygame.draw.circle(
            screen,
            GRAPE_COLOR,
            (center_x + 6, center_y),
            6
        )

        pygame.draw.circle(
            screen,
            GRAPE_COLOR,
            (center_x, center_y + 8),
            6
        )

        # Daun
        pygame.draw.circle(
            screen,
            (50, 180, 70),
            (center_x + 6, center_y - 8),
            5
        )

    # =========================
    # GAMBAR ULAR
    # =========================
    for i, segment in enumerate(snake):

        x, y = segment

        rect = pygame.Rect(
            x * CELL_SIZE + 2,
            y * CELL_SIZE + 2,
            CELL_SIZE - 4,
            CELL_SIZE - 4
        )

        if i == 0:
            pygame.draw.rect(
                screen,
                HEAD_COLOR,
                rect,
                border_radius=8
            )
        else:
            pygame.draw.rect(
                screen,
                SNAKE_COLOR,
                rect,
                border_radius=5
            )

    # =========================
    # INFORMASI
    # =========================
    panjang_text = font.render(
        f"Panjang: {len(snake)}/225",
        True,
        TEXT_COLOR
    )

    screen.blit(
        panjang_text,
        (10, 10)
    )

    # =========================
    # GAME OVER
    # =========================
    if game_over:

        text = big_font.render(
            "GAME OVER",
            True,
            GAMEOVER_COLOR
        )

        text_rect = text.get_rect(
            center=(WIDTH // 2, HEIGHT // 2 - 20)
        )

        screen.blit(text, text_rect)

        restart = font.render(
            "Tekan R untuk bermain lagi",
            True,
            TEXT_COLOR
        )

        restart_rect = restart.get_rect(
            center=(WIDTH // 2, HEIGHT // 2 + 35)
        )

        screen.blit(restart, restart_rect)

    # =========================
    # MENANG
    # =========================
    if win:

        text = big_font.render(
            "KAMU MENANG!",
            True,
            WIN_COLOR
        )

        text_rect = text.get_rect(
            center=(WIDTH // 2, HEIGHT // 2 - 20)
        )

        screen.blit(text, text_rect)

        restart = font.render(
            "Layar 15 x 15 sudah dipenuhi ular!",
            True,
            TEXT_COLOR
        )

        restart_rect = restart.get_rect(
            center=(WIDTH // 2, HEIGHT // 2 + 35)
        )

        screen.blit(restart, restart_rect)

    # =========================
    # UPDATE LAYAR
    # =========================
    pygame.display.flip()

    clock.tick(8)


pygame.quit()
sys.exit()