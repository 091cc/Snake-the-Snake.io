from js import document, setInterval, clearInterval
from pyodide.ffi import create_proxy
from random import randint

canvas = document.getElementById("game")
ctx = canvas.getContext("2d")
CELL = 20
WIDTH = canvas.width // CELL
HEIGHT = canvas.height // CELL

best_score = 0
key_proxy = create_proxy(None)
move_proxy = create_proxy(None)
game_loop = None

INITIAL_SPEED = 200
MIN_SPEED = 50
SPEED_DECREMENT = 5

def new_food(snake):
    while True:
        f = [randint(0, WIDTH-1), randint(0, HEIGHT-1)]
        if f not in snake:
            return f

def draw(snake, food, score):
    ctx.fillStyle = "black"
    ctx.fillRect(0, 0, canvas.width, canvas.height)
    ctx.fillStyle = "red"
    ctx.font = f"{CELL}px sans-serif"
    ctx.fillText("", food[0]*CELL, (food[1]+1)*CELL)
    ctx.fillStyle = "lime"
    for x, y in snake:
        ctx.fillRect(x*CELL, y*CELL, CELL, CELL)
    ctx.fillStyle = "white"
    ctx.font = "16px sans-serif"
    ctx.fillText(f"Score: {score}", 10, 20)
    ctx.fillText(f"Best: {best_score}", 100, 20)

def game_over(snake, food, score):
    global game_loop, best_score
    clearInterval(game_loop)
    if score > best_score:
        best_score = score
    ctx.fillStyle = "white"
    ctx.font = "30px sans-serif"
    ctx.fillText("Game Over!", 180, 180)
    ctx.fillText(f"Final Score: {score}", 180, 220)
    btn = document.createElement("button")
    btn.innerHTML = "PLAY AGAIN"
    btn.style.position = "absolute"
    btn.style.top = "65%"
    btn.style.left = "50%"
    btn.style.transform = "translate(-50%, -50%)"
    btn.style.fontSize = "20px"
    document.body.appendChild(btn)
    def restart(event):
        document.body.removeChild(btn)
        start_game()
    btn_proxy = create_proxy(restart)
    btn.addEventListener("click", btn_proxy)

def move(snake, direction, food, score):
    new_head = [snake[0][0]+direction[0], snake[0][1]+direction[1]]
    if new_head in snake or not (0 <= new_head[0] < WIDTH) or not (0 <= new_head[1] < HEIGHT):
        game_over(snake, food, score)
        return snake, direction, food, score, False
    snake.insert(0, new_head)
    if new_head == food:
        score += 1
        food = new_food(snake)
    else:
        snake.pop()
    draw(snake, food, score)
    return snake, direction, food, score, True

def on_key(event):
    global direction
    key = event.key
    if key == "ArrowUp" and direction != [0,1]: direction = [0,-1]
    if key == "ArrowDown" and direction != [0,-1]: direction = [0,1]
    if key == "ArrowLeft" and direction != [1,0]: direction = [-1,0]
    if key == "ArrowRight" and direction != [-1,0]: direction = [1,0]

def on_touch(btn_dir):
    global direction
    if btn_dir == "up" and direction != [0,1]: direction=[0,-1]
    if btn_dir == "down" and direction != [0,-1]: direction=[0,1]
    if btn_dir == "left" and direction != [1,0]: direction=[-1,0]
    if btn_dir == "right" and direction != [-1,0]: direction=[1,0]

def start_game():
    global snake, direction, food, score, move_proxy, game_loop
    snake = [[WIDTH//4, HEIGHT//2],[WIDTH//4-1, HEIGHT//2]]
    direction = [1,0]
    score = 0
    food = new_food(snake)
    draw(snake, food, score)
    speed = max(INITIAL_SPEED - score*SPEED_DECREMENT, MIN_SPEED)
    move_proxy = create_proxy(lambda event=None: run_game())
    game_loop = setInterval(move_proxy, speed)

def run_game():
    global snake, direction, food, score, game_loop
    snake, direction, food, score, alive = move(snake, direction, food, score)
    if alive:
        new_speed = max(INITIAL_SPEED - score*SPEED_DECREMENT, MIN_SPEED)
        clearInterval(game_loop)
        game_loop = setInterval(move_proxy, new_speed)
    else:
        clearInterval(game_loop)

document.addEventListener("keydown", create_proxy(on_key))

# 建立手機觸控按鍵
dirs = ["up","down","left","right"]
for d in dirs:
    btn = document.createElement("button")
    btn.innerHTML = d.upper()
    btn.style.position = "absolute"
    if d=="up": btn.style.bottom="100px"; btn.style.left="80px"
    if d=="down": btn.style.bottom="20px"; btn.style.left="80px"
    if d=="left": btn.style.bottom="60px"; btn.style.left="20px"
    if d=="right": btn.style.bottom="60px"; btn.style.left="140px"
    btn.style.fontSize="20px"
    document.body.appendChild(btn)
    btn_proxy = create_proxy(lambda e, dir=d: on_touch(dir))
    btn.addEventListener("click", btn_proxy)

start_game()
