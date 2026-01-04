import pygame
import math
import random

pygame.init()

# --- Variables ---
bullets = []
size = 10
target_x = 0
target_y = 0
running = True
round = 1
goal = 1
ammo = 20
ammo_used = 20
gravity = 0
radius = 5
bounce = 0
score = 0
target = False
difficulty = "N"
challenge = input("Do you want to be challenged: ")
bouncecheck = input("Do you want to have a bounce on the Left (L) side and Right (R) side: y/n ")
if bouncecheck == "y" or bouncecheck == "yes":
    bouncecheck = True
else:
    bouncecheck = False
if challenge == "yes" or challenge == "y":
    difficulty = input("What difficulty do you want? E ( Easy ) / M ( Medium ) / H ( Hard ): ")
if challenge != "yes" and challenge != "y":
    answer = input("Do you want to have a target: ")
    if answer == "yes" or answer == "y":
        target = True

gravity_speed = float(input("What speed should the gravity be? (Normal: 0.3): "))
font = pygame.font.SysFont(None, 36)  # None = default font, 36 = size
def circle_rect_collision(cx, cy, radius, rx, ry, rw, rh):
    # Find closest point on rectangle to circle center
    closest_x = max(rx, min(cx, rx + rw))
    closest_y = max(ry, min(cy, ry + rh))

    # Distance from circle center to closest point
    dx = cx - closest_x
    dy = cy - closest_y

    return (dx * dx + dy * dy) <= (radius * radius)

def targetx(a, b, c, SZ, DF):
    if difficulty == "N":
        a = random.randint(100,500)
        b = 575
    elif difficulty == "E":
        a = random.randint(100,500)
        b = 575
    elif difficulty == "M":
        a = random.randint(100, 500)
        b = random.randint(300, 575)
    elif difficulty == "H":
        a = random.randint(100, 500)
        b = random.randint(0, 575)
    else:
        print("Something has gone wrong")
        c = False
    if DF == "E" or difficulty == "N":
        SZ = 10
    if DF == "M":
        SZ = random.randint(8, 20)
    if DF == "H":
        SZ = random.randint(3, 20)
    return a, b, c, SZ, DF

target_x, target_y, running, size, difficulty = targetx(target_x, target_y, running, size, difficulty)




# Cannon position (fixed)
cannon_x = 40
cannon_y = 580  # near bottom
cannon_angle = 45  # initial angle in degrees
bullet_speed = 8   # how fast bullets are shot

screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()


while running:
    clock.tick(60)  # 60 FPS
    screen.fill((0, 0, 0))  # clear screen
    if target or challenge == "yes" or challenge == "y":
        pygame.draw.rect(screen, (62, 210, 28), (target_x, target_y, size, size))

    # --- Event handling ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            # Toggle gravity
            if event.key == pygame.K_g:
                gravity = 1 - gravity
                print("Gravity toggled:", gravity)
            # Shoot bullet at current angle
            elif event.key == pygame.K_SPACE:
                vx = bullet_speed * math.cos(math.radians(cannon_angle))
                vy = -bullet_speed * math.sin(math.radians(cannon_angle))  # negative = up
                bullets.append({"x": cannon_x + 5, "y": cannon_y, "vx": vx, "vy": vy, "radius": radius})
                ammo_used -= 1
            # Adjust cannon angle
            elif event.key == pygame.K_UP:
                cannon_angle = min(cannon_angle + 5, 90)  # max 90 degrees
            elif event.key == pygame.K_DOWN:
                cannon_angle = max(cannon_angle - 5, 0)   # min 0 degrees
            elif event.key == pygame.K_LEFT:
                bullet_speed -= 1
            elif event.key == pygame.K_RIGHT:
                bullet_speed += 1
            elif event.key == pygame.K_b:
                if challenge != "yes" and challenge != "y":
                    bounce = 1 - bounce
                    print(f"Bounce Toggled, {bounce}")
                else:
                    bounce = 0

    # --- Update bullets ---
    for bullet in bullets[:]:
        if gravity == 1:
            bullet["vy"] += gravity_speed

        bullet["x"] += bullet["vx"]
        bullet["y"] += bullet["vy"]

        if bullet["y"] + bullet["radius"] < 0:
            bullets.remove(bullet)
            continue

        # Stop bullet at floor
        if bullet["y"] < 10:
            bullets.remove(bullet)
            continue
        if bounce == 0:
            if bullet["y"] > 590:
                bullet["y"] = 590
                bullet["vy"] = 0
                bullets.remove(bullet)
                continue
            if bullet["x"] > 790:
                bullets.remove(bullet)
                continue
            if bullet["x"] < 10:
                bullets.remove(bullet)
                continue
        elif bounce == 1:
            if bullet["y"] > 580:  # bottom
                bullet["y"] = 580
                bullet["vy"] = -bullet["vy"] * 0.7
                #bullets.append({"x": cannon_x + 5, "y": cannon_y, "vx": vx, "vy": vy, "radius": radius})
                if abs(bullet["vy"]) < 1:
                    bullets.remove(bullet)
                    continue
            if bouncecheck == True:
                if bullet["x"] > 780:  # right
                    bullet["x"] = 780
                    bullet["vx"] = -bullet["vx"] * 0.7

                    if abs(bullet["vx"]) < 1:
                        bullets.remove(bullet)
                        continue

            if bouncecheck == True:
                if bullet["x"] < 20:
                    bullet["x"] = 20
                    bullet["vx"] = -bullet["vx"] * 0.7

                    if abs(bullet["vx"]) < 1:
                        bullets.remove(bullet)
                        continue
        bx = int(bullet["x"])
        by = int(bullet["y"])

        if 0 <= bx < 800 and 0 <= by < 600:
            if circle_rect_collision(
                    bullet["x"], bullet["y"], bullet["radius"],
                    target_x, target_y, size, size
            ):
                # hit logic here
                if size <= 8:
                    score += 3
                elif size <= 14:
                    score += 2
                else:
                    score += 1
                bullets.remove(bullet)
                target_x, target_y, running, size, difficulty = targetx(target_x, target_y, running, size, difficulty)
                continue

    if gravity == 0:
        GRAVITY = font.render("Gravity OFF", True, (255, 255, 255))
    elif gravity == 1:
        GRAVITY = font.render("Gravity ON", True, (255, 255, 255))
    if bounce == 0:
        BOUNCE = font.render("Bounce OFF", True, (255, 255, 255))
    elif bounce == 1:
        BOUNCE = font.render("Bounce ON", True, (255, 255, 255))
    BULLETSPEED = font.render(f"Bullet Speed: {bullet_speed}", True, (255, 255, 255))
    SCORE = font.render(f"Score: {score}", True, (255, 255, 255))
    ROUND = font.render(f"Round: {round}", True, (255, 255, 255))
    AMMO = font.render(f"Ammo: {ammo_used}", True, (255, 255, 255))
    GOAL = font.render(f"Goal: {goal}", True, (255, 255, 255))
    LOST = font.render(f"You lost!", True, (255, 255, 255))
    # --- Draw everything ---
    # Draw cannon base
    pygame.draw.rect(screen, (78, 37, 200), (cannon_x, cannon_y, 10, 15))
    screen.blit(GRAVITY, (10, 10))  # (x, y) position on screen
    screen.blit(BULLETSPEED, (10, 50))
    screen.blit(BOUNCE, (10, 90))
    if challenge == "yes" or challenge == "y":
        screen.blit(SCORE, (10, 130))
        screen.blit(ROUND, (10, 170))
        screen.blit(AMMO, (10, 210))
        screen.blit(GOAL, (10, 250))

    # Draw aiming direction
    length = 20
    end_x = cannon_x + 5 + length * math.cos(math.radians(cannon_angle))
    end_y = cannon_y - length * math.sin(math.radians(cannon_angle))
    pygame.draw.line(screen, (255, 0, 0), (cannon_x + 5, cannon_y), (end_x, end_y), 3)
    for bullet in bullets:
        pygame.draw.circle(screen, (255, 255, 255), (int(bullet["x"]), int(bullet["y"])), 5)

    pygame.display.flip()
    if challenge == "yes" or challenge == "y":
        if ammo_used < 0:
            print("You lost!")
            running = False
        if score >= goal:
            score = score - goal
            goal += 2
            round += 1
            ammo -= 2
            ammo_used = ammo
        if round == 6:
            print("You win!")
            running = False
pygame.quit()
