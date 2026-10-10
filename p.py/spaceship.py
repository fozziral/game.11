import pygame
import random
import math

# ============================================================
# SPACESHIP SHOOTER - PYGAME
# Controls:
#   WASD / Arrow Keys = Move
#   Mouse = Aim
#   Left Mouse / SPACE = Shoot
#   R = Restart after Game Over / Victory
#   ESC = Quit
# ============================================================

pygame.init()

WIDTH, HEIGHT = 1000, 700
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Spaceship Shooter")
clock = pygame.time.Clock()

# Colors
BLACK = (8, 10, 20)
WHITE = (240, 245, 255)
CYAN = (50, 220, 255)
GREEN = (60, 230, 100)
RED = (240, 65, 75)
YELLOW = (255, 220, 70)
PURPLE = (170, 90, 255)
GRAY = (80, 90, 110)

font = pygame.font.Font(None, 32)
big_font = pygame.font.Font(None, 72)
small_font = pygame.font.Font(None, 24)


def clamp(value, minimum, maximum):
    return max(minimum, min(value, maximum))


def distance(a, b):
    return math.hypot(a.x - b.x, a.y - b.y)


class Bullet:
    def __init__(self, x, y, vx, vy, owner):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.owner = owner
        self.radius = 5
        self.speed_life = 0

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.speed_life += 1

    def draw(self):
        color = CYAN if self.owner == "player" else RED
        pygame.draw.circle(screen, color, (int(self.x), int(self.y)), self.radius)

    def off_screen(self):
        return (
            self.x < -30 or self.x > WIDTH + 30 or
            self.y < -30 or self.y > HEIGHT + 30 or
            self.speed_life > 180
        )


class Player:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.radius = 22
        self.speed = 5.0
        self.health = 100
        self.max_health = 100
        self.shoot_cooldown = 0
        self.invulnerable = 0

    def update(self, keys):
        dx = 0
        dy = 0

        if keys[pygame.K_w] or keys[pygame.K_UP]:
            dy -= 1
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            dy += 1
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            dx -= 1
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            dx += 1

        # Normalize diagonal movement
        if dx != 0 or dy != 0:
            length = math.hypot(dx, dy)
            dx /= length
            dy /= length

        self.x += dx * self.speed
        self.y += dy * self.speed

        self.x = clamp(self.x, self.radius, WIDTH - self.radius)
        self.y = clamp(self.y, self.radius + 55, HEIGHT - self.radius)

        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

        if self.invulnerable > 0:
            self.invulnerable -= 1

    def shoot(self, target_x, target_y):
        if self.shoot_cooldown > 0:
            return None

        dx = target_x - self.x
        dy = target_y - self.y
        length = math.hypot(dx, dy)

        if length == 0:
            return None

        speed = 11
        vx = dx / length * speed
        vy = dy / length * speed

        self.shoot_cooldown = 8

        return Bullet(self.x, self.y, vx, vy, "player")

    def damage(self, amount):
        if self.invulnerable > 0:
            return

        self.health -= amount
        self.health = max(0, self.health)
        self.invulnerable = 35

    def draw(self):
        # Blink while temporarily invulnerable
        if self.invulnerable > 0 and (self.invulnerable // 4) % 2 == 0:
            return

        mx, my = pygame.mouse.get_pos()

        angle = math.atan2(my - self.y, mx - self.x)

        # Ship triangle points
        front = (
            self.x + math.cos(angle) * 30,
            self.y + math.sin(angle) * 30
        )
        left = (
            self.x + math.cos(angle + 2.45) * 20,
            self.y + math.sin(angle + 2.45) * 20
        )
        right = (
            self.x + math.cos(angle - 2.45) * 20,
            self.y + math.sin(angle - 2.45) * 20
        )

        pygame.draw.polygon(
            screen,
            CYAN,
            [front, left, right]
        )
        pygame.draw.polygon(
            screen,
            WHITE,
            [front, left, right],
            2
        )

        # Engine glow
        back_x = self.x - math.cos(angle) * 18
        back_y = self.y - math.sin(angle) * 18
        pygame.draw.circle(
            screen,
            YELLOW,
            (int(back_x), int(back_y)),
            6
        )


class Enemy:
    def __init__(self, x, y, enemy_type=0):
        self.x = x
        self.y = y
        self.radius = 20

        self.enemy_type = enemy_type

        if enemy_type == 0:
            self.speed = random.uniform(1.0, 1.6)
            self.health = 2
            self.max_health = 2
            self.shoot_delay = random.randint(70, 130)
            self.color = RED
        elif enemy_type == 1:
            self.speed = random.uniform(1.5, 2.2)
            self.health = 1
            self.max_health = 1
            self.shoot_delay = random.randint(90, 150)
            self.color = PURPLE
        else:
            self.speed = random.uniform(0.7, 1.1)
            self.health = 4
            self.max_health = 4
            self.shoot_delay = random.randint(50, 100)
            self.color = YELLOW

        self.shoot_timer = self.shoot_delay

    def update(self, player):
        dx = player.x - self.x
        dy = player.y - self.y
        length = math.hypot(dx, dy)

        if length > 0:
            dx /= length
            dy /= length

        # Keep some distance from the player.
        if length > 260:
            self.x += dx * self.speed
            self.y += dy * self.speed
        elif length < 160:
            self.x -= dx * self.speed
            self.y -= dy * self.speed

        # Small sideways movement makes enemies less predictable.
        side_x = -dy
        side_y = dx
        wobble = math.sin(pygame.time.get_ticks() / 500 + self.x) * 0.25
        self.x += side_x * wobble
        self.y += side_y * wobble

        self.x = clamp(self.x, self.radius, WIDTH - self.radius)
        self.y = clamp(self.y, self.radius + 55, HEIGHT - self.radius)

        self.shoot_timer -= 1

        if self.shoot_timer <= 0:
            self.shoot_timer = self.shoot_delay + random.randint(-15, 25)
            return self.shoot(player)

        return None

    def shoot(self, player):
        dx = player.x - self.x
        dy = player.y - self.y
        length = math.hypot(dx, dy)

        if length == 0:
            return None

        # Slight aiming error keeps the game playable.
        angle = math.atan2(dy, dx)
        angle += random.uniform(-0.10, 0.10)

        speed = 5.0 if self.enemy_type != 1 else 6.5

        vx = math.cos(angle) * speed
        vy = math.sin(angle) * speed

        return Bullet(self.x, self.y, vx, vy, "enemy")

    def damage(self, amount=1):
        self.health -= amount

    def draw(self):
        # Draw enemy body
        pygame.draw.circle(
            screen,
            self.color,
            (int(self.x), int(self.y)),
            self.radius
        )

        pygame.draw.circle(
            screen,
            WHITE,
            (int(self.x), int(self.y)),
            self.radius,
            2
        )

        # Enemy "eye"
        pygame.draw.circle(
            screen,
            BLACK,
            (int(self.x), int(self.y)),
            7
        )

        # Health bar
        bar_width = 42
        bar_height = 5
        hp_ratio = max(0, self.health / self.max_health)

        pygame.draw.rect(
            screen,
            (50, 50, 55),
            (
                int(self.x - bar_width / 2),
                int(self.y - self.radius - 12),
                bar_width,
                bar_height
            )
        )

        pygame.draw.rect(
            screen,
            GREEN,
            (
                int(self.x - bar_width / 2),
                int(self.y - self.radius - 12),
                int(bar_width * hp_ratio),
                bar_height
            )
        )


def create_enemies():
    enemies = []

    # Different enemy types are mixed into the wave.
    for i in range(12):
        while True:
            x = random.randint(50, WIDTH - 50)
            y = random.randint(90, HEIGHT - 50)

            # Avoid spawning directly on the player.
            if math.hypot(x - WIDTH / 2, y - HEIGHT / 2) > 220:
                break

        if i >= 9:
            enemy_type = 2
        elif i >= 6:
            enemy_type = 1
        else:
            enemy_type = 0

        enemies.append(Enemy(x, y, enemy_type))

    return enemies


def reset_game():
    return Player(), create_enemies(), [], 0, "playing"


def draw_background():
    screen.fill(BLACK)

    # Grid
    grid_size = 50
    offset = (pygame.time.get_ticks() // 20) % grid_size

    for x in range(-grid_size, WIDTH + grid_size, grid_size):
        pygame.draw.line(
            screen,
            (18, 23, 40),
            (x + offset, 55),
            (x + offset, HEIGHT)
        )

    for y in range(55, HEIGHT + grid_size, grid_size):
        pygame.draw.line(
            screen,
            (18, 23, 40),
            (0, y + offset),
            (WIDTH, y + offset)
        )

    # Stars
    random.seed(42)
    for _ in range(80):
        x = random.randrange(WIDTH)
        y = random.randrange(55, HEIGHT)
        pygame.draw.circle(screen, (45, 50, 70), (x, y), 1)
    random.seed()


def draw_ui(player, enemies, score):
    # Top bar
    pygame.draw.rect(screen, (14, 18, 30), (0, 0, WIDTH, 55))
    pygame.draw.line(screen, (45, 55, 80), (0, 54), (WIDTH, 54), 2)

    score_text = font.render(f"Score: {score}", True, WHITE)
    enemy_text = font.render(f"Enemies: {len(enemies)}", True, WHITE)

    screen.blit(score_text, (20, 14))
    screen.blit(enemy_text, (WIDTH - enemy_text.get_width() - 20, 14))

    # Health bar
    bar_x = WIDTH // 2 - 130
    bar_y = 15
    bar_w = 260
    bar_h = 24

    pygame.draw.rect(screen, (45, 45, 55), (bar_x, bar_y, bar_w, bar_h))
    health_width = int(bar_w * player.health / player.max_health)

    health_color = GREEN
    if player.health <= 50:
        health_color = YELLOW
    if player.health <= 25:
        health_color = RED

    pygame.draw.rect(
        screen,
        health_color,
        (bar_x, bar_y, health_width, bar_h)
    )
    pygame.draw.rect(
        screen,
        WHITE,
        (bar_x, bar_y, bar_w, bar_h),
        2
    )

    hp_text = small_font.render(
        f"HP {player.health}/{player.max_health}",
        True,
        BLACK if player.health > 20 else WHITE
    )
    screen.blit(
        hp_text,
        (
            bar_x + bar_w // 2 - hp_text.get_width() // 2,
            bar_y + 3
        )
    )

    controls = small_font.render(
        "WASD / Arrows: Move   |   Mouse / SPACE: Shoot",
        True,
        (150, 160, 180)
    )
    screen.blit(controls, (20, HEIGHT - 28))


def draw_end_screen(state, score):
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 175))
    screen.blit(overlay, (0, 0))

    if state == "victory":
        title = big_font.render("VICTORY!", True, GREEN)
        message = font.render(
            "All enemy ships have been destroyed!",
            True,
            WHITE
        )
    else:
        title = big_font.render("GAME OVER", True, RED)
        message = font.render(
            "Your spaceship was destroyed.",
            True,
            WHITE
        )

    score_message = font.render(
        f"Final Score: {score}",
        True,
        YELLOW
    )

    restart_message = font.render(
        "Press R to play again or ESC to quit",
        True,
        WHITE
    )

    screen.blit(
        title,
        (
            WIDTH // 2 - title.get_width() // 2,
            HEIGHT // 2 - 100
        )
    )

    screen.blit(
        message,
        (
            WIDTH // 2 - message.get_width() // 2,
            HEIGHT // 2 - 25
        )
    )

    screen.blit(
        score_message,
        (
            WIDTH // 2 - score_message.get_width() // 2,
            HEIGHT // 2 + 25
        )
    )

    screen.blit(
        restart_message,
        (
            WIDTH // 2 - restart_message.get_width() // 2,
            HEIGHT // 2 + 80
        )
    )


# Initial game state
player, enemies, bullets, score, game_state = reset_game()

running = True

while running:
    clock.tick(FPS)

    # ---------------- EVENTS ----------------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

            if event.key == pygame.K_r and game_state != "playing":
                player, enemies, bullets, score, game_state = reset_game()

    keys = pygame.key.get_pressed()

    # ---------------- GAME UPDATE ----------------
    if game_state == "playing":
        player.update(keys)

        # Shooting with mouse or SPACE.
        mouse_pressed = pygame.mouse.get_pressed()[0]

        if mouse_pressed or keys[pygame.K_SPACE]:
            mx, my = pygame.mouse.get_pos()
            new_bullet = player.shoot(mx, my)

            if new_bullet:
                bullets.append(new_bullet)

        # Update enemies and enemy bullets.
        for enemy in enemies:
            enemy_bullet = enemy.update(player)
            if enemy_bullet:
                bullets.append(enemy_bullet)

        # Update bullets.
        for bullet in bullets:
            bullet.update()

        bullets = [b for b in bullets if not b.off_screen()]

        # ---------------- BULLET COLLISIONS ----------------
        bullets_to_remove = set()
        enemies_to_remove = []

        for bullet in bullets:
            if bullet.owner == "player":
                for enemy in enemies:
                    if enemy in enemies_to_remove:
                        continue

                    d = math.hypot(
                        bullet.x - enemy.x,
                        bullet.y - enemy.y
                    )

                    if d < bullet.radius + enemy.radius:
                        bullets_to_remove.add(id(bullet))
                        enemy.damage(1)

                        # Score increases every time a player bullet hits.
                        score += 10

                        if enemy.health <= 0:
                            enemies_to_remove.append(enemy)
                            score += 40

                        break

            else:
                # Enemy bullet hits player.
                d = math.hypot(
                    bullet.x - player.x,
                    bullet.y - player.y
                )

                if d < bullet.radius + player.radius:
                    bullets_to_remove.add(id(bullet))
                    player.damage(10)

        bullets = [
            b for b in bullets
            if id(b) not in bullets_to_remove
        ]

        # Remove defeated enemies.
        for enemy in enemies_to_remove:
            if enemy in enemies:
                enemies.remove(enemy)

        # ---------------- ENEMY / PLAYER COLLISION ----------------
        for enemy in enemies:
            d = distance(
                pygame.Vector2(player.x, player.y),
                pygame.Vector2(enemy.x, enemy.y)
            )

            if d < player.radius + enemy.radius:
                player.damage(20)

                # Push enemy away after collision.
                dx = enemy.x - player.x
                dy = enemy.y - player.y
                length = math.hypot(dx, dy)

                if length > 0:
                    enemy.x += dx / length * 25
                    enemy.y += dy / length * 25

        # ---------------- GAME STATE ----------------
        if player.health <= 0:
            game_state = "game_over"

        elif len(enemies) == 0:
            game_state = "victory"

    # ---------------- DRAW ----------------
    draw_background()

    for bullet in bullets:
        bullet.draw()

    for enemy in enemies:
        enemy.draw()

    player.draw()

    draw_ui(player, enemies, score)

    if game_state != "playing":
        draw_end_screen(game_state, score)

    pygame.display.flip()

pygame.quit()
