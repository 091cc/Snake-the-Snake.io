import random
import curses
import time 

s = curses.initscr()
curses.curs_set(0)
sh, sw = s.getmaxyx()

INITIAL_SPEED = 150
MIN_SPEED = 30 
SPEED_DECREMENT = 5

w = curses.newwin(sh, sw, 0, 0)
w.keypad(1)
w.timeout(INITIAL_SPEED) 

snk_x = sw//4 
snk_y = sh//2
snake = [
  [snk_y, snk_x],
  [snk_y, snk_x-1],
  [snk_y, snk_x-2],
  [snk_y, snk_x-3]
]

score = 0

food = None
while food is None:
  nf = [
    random.randint(1, sh-2),
    random.randint(1, sw-2)
  ]
  food = nf if nf not in snake else None
w.addch(int(food[0]), int(food[1]), "") 

key = curses.KEY_RIGHT

def game_over_flash(window, message_line1, message_line2, sh, sw, current_snake, current_food):
    window.timeout(-1) 
    
    for y, x in current_snake:
        try:
            window.addch(int(y), int(x), ' ')
        except:
            pass
    
    window.addch(int(current_food[0]), int(current_food[1]), ' ')
    window.refresh() 

    center_y = sh // 2
    center_x1 = sw // 2 - len(message_line1) // 2
    center_x2 = sw // 2 - len(message_line2) // 2

    for i in range(5):
        window.addstr(center_y - 1, center_x1, message_line1, curses.A_REVERSE | curses.A_BOLD)
        window.addstr(center_y + 1, center_x2, message_line2, curses.A_REVERSE | curses.A_BOLD)
        window.refresh()
        time.sleep(0.3) 
        window.addstr(center_y - 1, center_x1, " " * len(message_line1))
        window.addstr(center_y + 1, center_x2, " " * len(message_line2))
        window.refresh()
        time.sleep(0.3)

    window.addstr(center_y - 1, center_x1, message_line1, curses.A_REVERSE | curses.A_BOLD)
    window.addstr(center_y + 1, center_x2, message_line2, curses.A_REVERSE | curses.A_BOLD)
    window.refresh()
    time.sleep(1)

while True:
  score_text = "Score: {}".format(score)
  w.addstr(0, sw - len(score_text) - 1, score_text)
  
  next_key = w.getch()
  wrong_operation = True if (next_key==-1 or next_key==curses.KEY_DOWN and key == curses.KEY_UP\
                            or key==curses.KEY_DOWN and next_key == curses.KEY_UP \
                            or next_key==curses.KEY_LEFT and key == curses.KEY_RIGHT\
                            or key==curses.KEY_LEFT and next_key == curses.KEY_RIGHT) else False  
  key = key if wrong_operation else next_key

  if snake[0][0] in [0, sh-1] or snake[0][1] in [0, sw-1] or snake[0] in snake[1:]:
    msg_line1 = "Oops, you lost!"
    msg_line2 = "Final Score: {}".format(score)
    game_over_flash(w, msg_line1, msg_line2, sh, sw, snake, food)

    curses.nocbreak()
    s.keypad(False)
    curses.echo()
    curses.endwin()
    print("Oops, you lost!\nFinal Score:", score)
    break

  new_head = [snake[0][0], snake[0][1]]

  if key == curses.KEY_DOWN:
    new_head[0] += 1
  if key == curses.KEY_UP:
    new_head[0] -= 1
  if key == curses.KEY_LEFT:
    new_head[1] -= 1
  if key == curses.KEY_RIGHT:
    new_head[1] += 1

  snake.insert(0, new_head)

  if snake[0] == food:
    score += 1
    
    new_timeout = INITIAL_SPEED - (score * SPEED_DECREMENT)
    if new_timeout < MIN_SPEED:
        new_timeout = MIN_SPEED
        
    w.timeout(new_timeout) 
    
    food = None
    while food is None:
      nf = [
        random.randint(1, sh-2),
        random.randint(1, sw-2)
      ]
      food = nf if nf not in snake else None
    w.addch(int(food[0]), int(food[1]), "")
  else:
    tail = snake.pop()
    w.addch(int(tail[0]), int(tail[1]), ' ')

  try:
    w.addch(int(snake[0][0]), int(snake[0][1]), curses.ACS_CKBOARD)
  except:
    msg_line1 = "Oops, you lost!"
    msg_line2 = "Final Score: {}".format(score)
    game_over_flash(w, msg_line1, msg_line2, sh, sw, snake, food)

    curses.nocbreak()
    s.keypad(False)
    curses.echo()
    curses.endwin()
    print("Oops, you lost!\nFinal Score:", score)
    break