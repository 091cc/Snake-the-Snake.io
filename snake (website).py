from js import document, setInterval, clearInterval
from random import randint

canvas = document.getElementById("game")
ctx = canvas.getContext("2d")

CELL = 20
WIDTH = canvas.width // CELL
HEIGHT = canvas.height // CELL

snake = [[WIDTH//4, HEIGHT//2], [WIDTH//4-1, HEIGHT//2], [WIDTH//4-2, HEIGHT//2], [WIDTH//4-3, HEIGHT//2]]
direction = [1, 0]
score = 0
INITIAL_SPEED = 150
MIN_SPEED = 30
SPEED_DECREMENT = 5

food = [randint(0, WIDTH-1), randint(0, HEIGHT-1)]
while food in snake:
    food = [randint(0, WIDTH-1), randint(0, HEIGHT-1)]
def draw():
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

def game_over():
    clearInterval(game_loop)
    ctx.fillStyle = "white"
    ctx.font = "20px sans-serif"
    ctx.fillText(f"Game Over! Score: {score}", 50, canvas.height//2)

def move():
    global snake, food, score, game_loop, INITIAL_SPEED
    new_head = [snake[0][0] + direction[0], snake[0][1] + direction[1]]

    if new_head in snake or not (0 <= new_head[0] < WIDTH) or not (0 <= new_head[1] < HEIGHT):
        game_over()
        return

    snake.insert(0, new_head)

    if new_head == food:
        score += 1
        new_speed = INITIAL_SPEED - score*SPEED_DECREMENT
        if new_speed < MIN_SPEED:
            new_speed = MIN_SPEED
        game_loop = setInterval(move, new_speed)

        while True:
            nf = [randint(0, WIDTH-1), randint(0, HEIGHT-1)]
            if nf not in snake:
                food[:] = nf
                break
    else:
        snake.pop()

    draw()

def key(event):
    global direction
    key_map = {
        "ArrowUp": [0, -1],
        "ArrowDown": [0, 1],
        "ArrowLeft": [-1, 0],
        "ArrowRight": [1, 0]
    }
    if event.key in key_map:
        new_dir = key_map[event.key]
        if [new_dir[0], new_dir[1]] != [-direction[0], -direction[1]]:
            direction[:] = new_dir

document.addEventListener("keydown", key)

draw()
game_loop = setInterval(move, INITIAL_SPEED)