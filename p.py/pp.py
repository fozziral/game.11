import pygame
import random
import math

# =========================
# INISIALISASI
# =========================
pygame.init()

WIDTH = 900
HEIGHT = 600
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("RPG Adventure")
clock = pygame.time.Clock()

# Font
font = pygame.font.Font(None, 28)
big_font = pygame.font.Font(None, 50)

# Warna
WHITE = (255, 255, 255)
BLACK = (20, 20, 20)
GREEN = (50, 200, 80)
RED = (220, 60, 60)
BLUE = (60, 120, 255)
YELLOW = (255, 220, 50)
BROWN = (120, 80, 40)
DARK_GREEN = (35, 120, 60)
PURPLE = (150, 70, 200)


# =========================
# PLAYER
# =========================
player = {
    "x": WIDTH // 2,
    "y": HEIGHT // 2,
    "speed": 4,
    "hp": 100,
    "max_hp": 100,
    "attack": 20,
    "level": 1,
    "exp": 0,
    "max_exp": 100,
    "potion": 3
}

player_size = 35


# =========================
# MUSUH
# =========================
enemies = []

for i in range(6):
    enemy = {
        "x": random.randint(50, WIDTH - 50),
        "y": random.randint(100, HEIGHT - 50),
        "hp": 40,
        "max_hp": 40,
        "speed": 1.2,
        "size": 30
    }

    enemies.append(enemy)


# =========================
# PROJECTILE
# =========================
projectiles = []


# =========================
# FUNGSI
# =========================
def draw_text(text, x, y, color=WHITE, font_type=font):
    image = font_type.render(text, True, color)
    screen.blit(image, (x, y))


def distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def add_enemy():
    enemy = {
        "x": random.choice([
            random.randint(30, WIDTH - 30),
            random.choice([30, WIDTH - 30])
        ]),
        "y": random.randint(100, HEIGHT - 30),
        "hp": 40 + player["level"] * 10,
        "max_hp": 40 + player["level"] * 10,
        "speed": 1.2 + player["level"] * 0.1,
        "size": 30
    }

    enemies.append(enemy)


def level_up():
    if player["exp"] >= player["max_exp"]:
        player["exp"] -= player["max_exp"]

        player["level"] += 1
        player["max_exp"] += 50

        player["max_hp"] += 20
        player["hp"] = player["max_hp"]
        player["attack"] += 5

        print("LEVEL UP!")


# =========================
# GAME LOOP
# =========================
running = True
game_over = False

while running:

    # =========================
    # FPS
    # =========================
    clock.tick(FPS)

    # =========================
    # EVENT
    # =========================
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        # Klik kiri = menyerang
        if event.type == pygame.MOUSEBUTTONDOWN:

            if event.button == 1 and not game_over:

                mouse_x, mouse_y = pygame.mouse.get_pos()

                dx = mouse_x - player["x"]
                dy = mouse_y - player["y"]

                length = math.sqrt(dx * dx + dy * dy)

                if length != 0:
                    dx /= length
                    dy /= length

                    projectiles.append({
                        "x": player["x"],
                        "y": player["y"],
                        "dx": dx * 8,
                        "dy": dy * 8,
                        "damage": player["attack"]
                    })

        # Tombol R = potion
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_r:
                if player["potion"] > 0 and player["hp"] < player["max_hp"]:
                    player["hp"] += 30

                    if player["hp"] > player["max_hp"]:
                        player["hp"] = player["max_hp"]

                    player["potion"] -= 1


    if not game_over:

        # =========================
        # MOVEMENT PLAYER
        # =========================
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w] or keys[pygame.K_UP]:
            player["y"] -= player["speed"]

        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            player["y"] += player["speed"]

        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            player["x"] -= player["speed"]

        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            player["x"] += player["speed"]


        # Batasi player di layar
        player["x"] = max(20, min(WIDTH - 20, player["x"]))
        player["y"] = max(80, min(HEIGHT - 20, player["y"]))


        # =========================
        # PROJECTILE
        # =========================
        for bullet in projectiles:

            bullet["x"] += bullet["dx"]
            bullet["y"] += bullet["dy"]

        # Hapus projectile di luar layar
        projectiles = [
            bullet for bullet in projectiles
            if 0 < bullet["x"] < WIDTH
            and 70 < bullet["y"] < HEIGHT
        ]


        # =========================
        # MUSUH MENGEJAR PLAYER
        # =========================
        for enemy in enemies:

            dx = player["x"] - enemy["x"]
            dy = player["y"] - enemy["y"]

            length = math.sqrt(dx * dx + dy * dy)

            if length != 0:
                dx /= length
                dy /= length

                enemy["x"] += dx * enemy["speed"]
                enemy["y"] += dy * enemy["speed"]


            # Musuh menyentuh player
            if distance(
                player["x"],
                player["y"],
                enemy["x"],
                enemy["y"]
            ) < player_size / 2 + enemy["size"] / 2:

                player["hp"] -= 0.5


        # =========================
        # COLLISION PROJECTILE
        # =========================
        for bullet in projectiles[:]:

            for enemy in enemies[:]:

                if distance(
                    bullet["x"],
                    bullet["y"],
                    enemy["x"],
                    enemy["y"]
                ) < enemy["size"] / 2:

                    enemy["hp"] -= bullet["damage"]

                    if bullet in projectiles:
                        projectiles.remove(bullet)

                    if enemy["hp"] <= 0:

                        enemies.remove(enemy)

                        player["exp"] += 25

                        level_up()

                        # Spawn musuh baru
                        add_enemy()

                    break


        # =========================
        # GAME OVER
        # =========================
        if player["hp"] <= 0:
            player["hp"] = 0
            game_over = True


    # =========================
    # DRAW BACKGROUND
    # =========================
    screen.fill(DARK_GREEN)

    # Tanah
    pygame.draw.rect(
        screen,
        (45, 150, 70),
        (0, 70, WIDTH, HEIGHT - 70)
    )

    # =========================
    # HUD
    # =========================
    pygame.draw.rect(
        screen,
        (30, 30, 30),
        (0, 0, WIDTH, 70)
    )

    draw_text(
        f"Level: {player['level']}",
        20,
        15
    )

    draw_text(
        f"Potion: {player['potion']} [R]",
        150,
        15
    )

    draw_text(
        f"FPS: {int(clock.get_fps())}",
        760,
        15,
        YELLOW
    )


    # HP BAR
    pygame.draw.rect(
        screen,
        (80, 80, 80),
        (20, 45, 200, 15)
    )

    hp_width = int(
        200 * player["hp"] / player["max_hp"]
    )

    pygame.draw.rect(
        screen,
        RED,
        (20, 45, hp_width, 15)
    )


    # EXP BAR
    pygame.draw.rect(
        screen,
        (80, 80, 80),
        (240, 45, 200, 15)
    )

    exp_width = int(
        200 * player["exp"] / player["max_exp"]
    )

    pygame.draw.rect(
        screen,
        BLUE,
        (240, 45, exp_width, 15)
    )


    # =========================
    # PLAYER
    # =========================
    pygame.draw.circle(
        screen,
        BLUE,
        (int(player["x"]), int(player["y"])),
        player_size // 2
    )


    # Pedang / arah serangan
    mouse_x, mouse_y = pygame.mouse.get_pos()

    dx = mouse_x - player["x"]
    dy = mouse_y - player["y"]

    length = math.sqrt(dx * dx + dy * dy)

    if length != 0:
        dx /= length
        dy /= length

    pygame.draw.line(
        screen,
        WHITE,
        (player["x"], player["y"]),
        (
            player["x"] + dx * 35,
            player["y"] + dy * 35
        ),
        5
    )


    # =========================
    # MUSUH
    # =========================
    for enemy in enemies:

        pygame.draw.circle(
            screen,
            RED,
            (int(enemy["x"]), int(enemy["y"])),
            enemy["size"] // 2
        )

        # HP musuh
        pygame.draw.rect(
            screen,
            BLACK,
            (
                enemy["x"] - 20,
                enemy["y"] - 30,
                40,
                5
            )
        )

        pygame.draw.rect(
            screen,
            GREEN,
            (
                enemy["x"] - 20,
                enemy["y"] - 30,
                40 * enemy["hp"] / enemy["max_hp"],
                5
            )
        )


    # =========================
    # PROJECTILE
    # =========================
    for bullet in projectiles:

        pygame.draw.circle(
            screen,
            YELLOW,
            (int(bullet["x"]), int(bullet["y"])),
            6
        )


    # =========================
    # GAME OVER
    # =========================
    if game_over:

        overlay = pygame.Surface(
            (WIDTH, HEIGHT),
            pygame.SRCALPHA
        )

        overlay.fill((0, 0, 0, 170))
        screen.blit(overlay, (0, 0))

        text = big_font.render(
            "GAME OVER",
            True,
            RED
        )

        screen.blit(
            text,
            (
                WIDTH // 2 - text.get_width() // 2,
                HEIGHT // 2 - 40
            )
        )

        draw_text(
            "Tutup game untuk keluar.",
            WIDTH // 2 - 100,
            HEIGHT // 2 + 20
        )


    pygame.display.flip()


pygame.quit()
