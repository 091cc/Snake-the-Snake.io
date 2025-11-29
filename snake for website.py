from js import document, setInterval, clearInterval
from pyodide.ffi import create_proxy
from random import randint

canvas = document.getElementById("game")
ctx = canvas.getContext("2d")
CELL = 20
WIDTH = canvas.width // CELL
HEIGHT = canvas.height // CELL

snake = [[WIDTH//4, HEIGHT//2]]
direction = [1, 0]
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

def move():
    global snake, food
    new_head = [snake[0][0]+direction[0], snake[0][1]+direction[1]]
    if new_head in snake or not (0<=new_head[0]<WIDTH) or not (0<=new_head[1]<HEIGHT):
        clearInterval(game_loop)
        ctx.fillStyle = "white"
        ctx.fillText("Game Over!", 180, 180)
        return
    snake.insert(0, new_head)
    if new_head == food:
        food = [randint(0, WIDTH-1), randint(0, HEIGHT-1)]
    else:
        snake.pop()
    draw()

def on_key(event):
    global direction
    key = event.key
    if key=="ArrowUp" and direction != [0,1]: direction=[0,-1]
    if key=="ArrowDown" and direction != [0,-1]: direction=[0,1]
    if key=="ArrowLeft" and direction != [1,0]: direction=[-1,0]
    if key=="ArrowRight" and direction != [-1,0]: direction=[1,0]

key_proxy = create_proxy(on_key)
document.addEventListener("keydown", key_proxy)
move_proxy = create_proxy(move)
game_loop = setInterval(move_proxy, 200)
draw()