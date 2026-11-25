import turtle
import time
import random

# Game Settings
delay = 0.09
score = 0
high_score = 0
level = 1
apples_eaten = 0
paused = False
bonus_active = False
bonus_timer = 0

# Screen Setup
wn = turtle.Screen()
wn.title("NEON SNAKE // Arcade Edition")
wn.bgcolor("#0f172a")
wn.setup(width=640, height=680)
wn.tracer(0)

# Draw Arena Grid & Glowing Border
bg_pen = turtle.Turtle()
bg_pen.speed(0)
bg_pen.hideturtle()

# Subtle Grid Lines
bg_pen.color("#1e293b")
for x in range(-280, 281, 20):
    bg_pen.penup()
    bg_pen.goto(x, -280)
    bg_pen.pendown()
    bg_pen.goto(x, 280)

for y in range(-280, 281, 20):
    bg_pen.penup()
    bg_pen.goto(-280, y)
    bg_pen.pendown()
    bg_pen.goto(280, y)

# Neon Outer Border
bg_pen.pensize(4)
bg_pen.color("#38bdf8")
bg_pen.penup()
bg_pen.goto(-290, 290)
bg_pen.pendown()
for _ in range(4):
    bg_pen.forward(580)
    bg_pen.right(90)

# Snake Head
head = turtle.Turtle()
head.speed(0)
head.shape("square")
head.color("#22c55e")
head.shapesize(0.95, 0.95)
head.penup()
head.goto(0, 0)
head.direction = "stop"

# Snake Eyes
eye1 = turtle.Turtle()
eye1.speed(0)
eye1.shape("circle")
eye1.color("#0f172a")
eye1.shapesize(0.2, 0.2)
eye1.penup()

eye2 = turtle.Turtle()
eye2.speed(0)
eye2.shape("circle")
eye2.color("#0f172a")
eye2.shapesize(0.2, 0.2)
eye2.penup()

# Normal Food (Neon Pink)
food = turtle.Turtle()
food.speed(0)
food.shape("circle")
food.color("#f43f5e")
food.shapesize(0.85, 0.85)
food.penup()
food.goto(0, 100)

# Golden Bonus Food
bonus = turtle.Turtle()
bonus.speed(0)
bonus.shape("circle")
bonus.color("#facc15")
bonus.shapesize(1.1, 1.1)
bonus.penup()
bonus.goto(1000, 1000)

segments = []
obstacles = []

# HUD Scoreboard
pen = turtle.Turtle()
pen.speed(0)
pen.color("#f8fafc")
pen.penup()
pen.hideturtle()
pen.goto(0, 302)

# Status / Message Banner
msg_pen = turtle.Turtle()
msg_pen.speed(0)
msg_pen.color("#38bdf8")
msg_pen.penup()
msg_pen.hideturtle()
msg_pen.goto(0, -40)
msg_pen.write("Press Arrow Keys or WASD to Start!", align="center", font=("Consolas", 14, "bold"))

def update_hud():
    pen.clear()
    bonus_txt = f"  |  BONUS: {bonus_timer}" if bonus_active else ""
    pen.write(
        f"SCORE: {score}   HIGH: {high_score}   LVL: {level}{bonus_txt}",
        align="center",
        font=("Consolas", 14, "bold")
    )

def update_eyes():
    hx, hy = head.xcor(), head.ycor()
    if head.direction == "up" or head.direction == "stop":
        eye1.goto(hx - 4, hy + 4)
        eye2.goto(hx + 4, hy + 4)
    elif head.direction == "down":
        eye1.goto(hx - 4, hy - 4)
        eye2.goto(hx + 4, hy - 4)
    elif head.direction == "left":
        eye1.goto(hx - 4, hy + 4)
        eye2.goto(hx - 4, hy - 4)
    elif head.direction == "right":
        eye1.goto(hx + 4, hy + 4)
        eye2.goto(hx + 4, hy - 4)

def random_grid_pos():
    while True:
        x = random.randint(-13, 13) * 20
        y = random.randint(-13, 13) * 20
        if abs(x) < 60 and abs(y) < 60:
            continue
        if any(obs.xcor() == x and obs.ycor() == y for obs in obstacles):
            continue
        return x, y

def spawn_obstacle():
    obs = turtle.Turtle()
    obs.speed(0)
    obs.shape("square")
    obs.color("#ef4444")
    obs.shapesize(0.9, 0.9)
    obs.penup()
    obs.goto(random_grid_pos())
    obstacles.append(obs)

# Controls
def go_up():
    if head.direction != "down" and not paused:
        head.direction = "up"
        msg_pen.clear()

def go_down():
    if head.direction != "up" and not paused:
        head.direction = "down"
        msg_pen.clear()

def go_left():
    if head.direction != "right" and not paused:
        head.direction = "left"
        msg_pen.clear()

def go_right():
    if head.direction != "left" and not paused:
        head.direction = "right"
        msg_pen.clear()

def toggle_pause():
    global paused
    if head.direction == "stop":
        return
    paused = not paused
    msg_pen.clear()
    if paused:
        msg_pen.color("#facc15")
        msg_pen.write("PAUSED (Press P to Resume)", align="center", font=("Consolas", 16, "bold"))

def move():
    if head.direction == "up":
        head.sety(head.ycor() + 20)
    elif head.direction == "down":
        head.sety(head.ycor() - 20)
    elif head.direction == "left":
        head.setx(head.xcor() - 20)
    elif head.direction == "right":
        head.setx(head.xcor() + 20)
    update_eyes()

def game_over():
    global score, delay, level, apples_eaten, bonus_active
    msg_pen.clear()
    msg_pen.color("#f43f5e")
    msg_pen.write(f"GAME OVER! Score: {score}", align="center", font=("Consolas", 18, "bold"))
    wn.update()
    time.sleep(1.2)

    head.goto(0, 0)
    head.direction = "stop"
    update_eyes()

    for seg in segments:
        seg.goto(1000, 1000)
    segments.clear()

    for obs in obstacles:
        obs.goto(1000, 1000)
    obstacles.clear()

    bonus.goto(1000, 1000)
    bonus_active = False
    score = 0
    level = 1
    apples_eaten = 0
    delay = 0.09
    update_hud()

    msg_pen.clear()
    msg_pen.color("#38bdf8")
    msg_pen.write("Press Arrow Keys or WASD to Play Again!", align="center", font=("Consolas", 13, "bold"))

# Key Bindings
wn.listen()
wn.onkeypress(go_up, "Up")
wn.onkeypress(go_down, "Down")
wn.onkeypress(go_left, "Left")
wn.onkeypress(go_right, "Right")
wn.onkeypress(go_up, "w")
wn.onkeypress(go_down, "s")
wn.onkeypress(go_left, "a")
wn.onkeypress(go_right, "d")
wn.onkeypress(toggle_pause, "p")

update_hud()
update_eyes()

# Main Game Loop
while True:
    wn.update()

    if paused:
        time.sleep(0.1)
        continue

    # Wall Collision
    if head.xcor() > 270 or head.xcor() < -270 or head.ycor() > 270 or head.ycor() < -270:
        game_over()

    # Obstacle Collision
    for obs in obstacles:
        if head.distance(obs) < 18:
            game_over()

    # Normal Food Collision
    if head.distance(food) < 18:
        food.goto(random_grid_pos())
        apples_eaten += 1

        new_seg = turtle.Turtle()
        new_seg.speed(0)
        new_seg.shape("square")
        # Alternating green shades for body pattern
        new_seg.color("#4ade80" if len(segments) % 2 == 0 else "#16a34a")
        new_seg.shapesize(0.9, 0.9)
        new_seg.penup()
        segments.append(new_seg)

        score += 10
        if score > high_score:
            high_score = score

        # Level Up every 50 points
        new_level = (score // 50) + 1
        if new_level > level:
            level = new_level
            delay = max(0.045, delay - 0.007)
            spawn_obstacle()

        # Spawn Golden Bonus every 4 apples
        if apples_eaten % 4 == 0 and not bonus_active:
            bonus.goto(random_grid_pos())
            bonus_active = True
            bonus_timer = 45

        update_hud()

    # Golden Bonus Collision & Countdown
    if bonus_active:
        bonus_timer -= 1
        update_hud()
        if head.distance(bonus) < 20:
            score += 30
            if score > high_score:
                high_score = score
            bonus.goto(1000, 1000)
            bonus_active = False
            update_hud()
        elif bonus_timer <= 0:
            bonus.goto(1000, 1000)
            bonus_active = False
            update_hud()

    # Move Body
    for i in range(len(segments) - 1, 0, -1):
        segments[i].goto(segments[i - 1].xcor(), segments[i - 1].ycor())

    if len(segments) > 0:
        segments[0].goto(head.xcor(), head.ycor())

    move()

    # Self Collision
    for seg in segments:
        if seg.distance(head) < 18:
            game_over()

    time.sleep(delay)
