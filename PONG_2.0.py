from tkinter import *
import random


screen_width = 1920 #в пикселях
screen_height = 1000

actual_screen_width = screen_width / 1.25
actual_screen_height = screen_height / 1.25

pad_width = actual_screen_width / 125
pad_height = actual_screen_height / 8

bounce_count = 0

W = 0
S = 0
UP = 0
DOWN = 0

pause = False

#скорость вообще должна зависить от разрешения экрана, но мне лень пока что всё делать правильно,
#                        поэтому сделаю так, чтоб хорошо на FullHD работало и всё, ждите патча :)
#кстати тут получилось много переменных, значения которых ДОЛЖНЫ зависеть от разрешения экрана
#а я ведь хотел сделать чтоб разрешение окна можно было запросто изменять...
ball_size = actual_screen_height / 125
ball_speed = 30
speed_rng = 40
ball_x_speed = 20
ball_y_speed = 0

pad_speed = 14
lpad_y_speed = 0
rpad_y_speed = 0

l_score = 0
r_score = 0

right_side = True

root = Tk()

c = Canvas(root, width = actual_screen_width, height = actual_screen_height, bg = 'black')
c.pack()

root.title('PONG')

lpad = c.create_rectangle(pad_width * 2, actual_screen_height / 2 - pad_height / 2,
                          pad_width * 3, actual_screen_height / 2 + pad_height / 2,
                          fill = 'white', width = 0)

rpad = c.create_rectangle(actual_screen_width - pad_width * 3, actual_screen_height / 2 - pad_height / 2,
                          actual_screen_width - pad_width * 2, actual_screen_height / 2 + pad_height / 2,
                          fill = 'white', width = 0)

ball = c.create_rectangle(actual_screen_width / 2 - ball_size, actual_screen_height / 2 - ball_size,
                          actual_screen_width / 2 + ball_size, actual_screen_height / 2 + ball_size,
                          fill = 'white', width = 0)

l_text = c.create_text(int(actual_screen_width / 4), int(actual_screen_height / 20), font = ('Consolas', 20), fill = 'white')
r_text = c.create_text(int(actual_screen_width - (actual_screen_width / 4)), int(actual_screen_height / 20),
                       font = ('Consolas', 20), fill = 'white')

c.focus_set()

def key_status(event):
    global W, S, UP, DOWN, pause
    if event.keysym == 'w':
        W = 1
    elif event.keysym == 's':
        S = 1
    if event.keysym == 'Up':
        UP = 1
    elif event.keysym == 'Down':
        DOWN = 1
    if event.keysym == 'p':
        pause = not pause

c.bind('<KeyPress>', key_status)

def key_status_neg(event):
    global W, S, UP, DOWN 
    if event.keysym == 'w':
        W = 0
    elif event.keysym == 's':
        S = 0
    if event.keysym == 'Up':
        UP = 0
    elif event.keysym == 'Down':
        DOWN = 0

c.bind('<KeyRelease>', key_status_neg)



def ball_move():
    if right_side == True:
        c.move(ball, ball_x_speed / 5, ball_y_speed / 5)
    else:
        c.move(ball, -ball_x_speed / 5, ball_y_speed / 5)

def random_ball_speed():
    global ball_x_speed, ball_y_speed
    ball_y_speed = random.randint(-40 - bounce_count * 2, 40 + bounce_count * 2)
    if ball_x_speed > 0:
        ball_x_speed = random.randint(bounce_count * 2 + ball_speed, bounce_count * 2 + ball_speed + speed_rng)
    else:
        ball_x_speed = -(random.randint(bounce_count * 2 + ball_speed, bounce_count * 2 + ball_speed + speed_rng))

def ball_ricochet():
    global ball_x_speed, ball_y_speed, bounce_count, right_side
    if (c.coords(ball)[2] >= c.coords(rpad)[0]) and ((c.coords(ball)[3] >= c.coords(rpad)[1]) and (c.coords(ball)[1] <= c.coords(rpad)[3])):
        if (c.coords(ball)[2] >= c.coords(rpad)[0]) and (c.coords(ball)[0] < c.coords(rpad)[2]):
            right_side = False
            #ball_x_speed = -ball_x_speed
            bounce_count += 1
            random_ball_speed()
    elif (c.coords(ball)[0] <= c.coords(lpad)[2]) and ((c.coords(ball)[3] >= c.coords(lpad)[1]) and (c.coords(ball)[1] <= c.coords(lpad)[3])):
        if (c.coords(ball)[0] <= c.coords(lpad)[2]) and (c.coords(ball)[2] > c.coords(lpad)[0]):
            right_side = True
            #ball_x_speed = -ball_x_speed
            bounce_count += 1
            random_ball_speed()
    
    if c.coords(ball)[1] <= 0:
        ball_y_speed = -ball_y_speed
    elif c.coords(ball)[3] >= actual_screen_height:
        ball_y_speed = -ball_y_speed



def pads_move():
    c.move(lpad, 0, lpad_y_speed)
    if c.coords(lpad)[1] < 0:
        c.move(lpad, 0, - c.coords(lpad)[1])
    elif c.coords(lpad)[3] > actual_screen_height:
        c.move(lpad, 0, actual_screen_height - c.coords(lpad)[3])
    c.move(rpad, 0, rpad_y_speed)
    if c.coords(rpad)[1] < 0:
        c.move(rpad, 0, - c.coords(rpad)[1])
    elif c.coords(rpad)[3] > actual_screen_height:
        c.move(rpad, 0, actual_screen_height - c.coords(rpad)[3])

def lpad_controller():
    global lpad_y_speed
    if W == 1:
        lpad_y_speed = -pad_speed
    elif S == 1:
        lpad_y_speed = pad_speed
    else:
        lpad_y_speed = 0

def rpad_controller():
    global rpad_y_speed
    if UP == 1:
        rpad_y_speed = -pad_speed
    elif DOWN == 1:
        rpad_y_speed = pad_speed
    else:
        rpad_y_speed = 0

def reset():
    global ball_x_speed, ball_y_speed, bounce_count
    bounce_count = 0
    ball_x_speed = ball_speed - ball_speed / 3
    ball_y_speed = 0

def score():
    global l_score, r_score, right_side
    if c.coords(ball)[2] < 0:
        c.coords(ball, actual_screen_width / 2 - ball_size, actual_screen_height / 2 - ball_size,
                 actual_screen_width / 2 + ball_size, actual_screen_height / 2 + ball_size,)
        r_score += 1
        right_side = False
        reset()
        text_update()
    elif c.coords(ball)[0] > actual_screen_width:
        c.coords(ball, actual_screen_width / 2 - ball_size, actual_screen_height / 2 - ball_size,
                 actual_screen_width / 2 + ball_size, actual_screen_height / 2 + ball_size,)
        l_score += 1
        right_side = True
        reset()
        text_update()

def text_update():
    c.itemconfig(l_text, text = l_score)
    c.itemconfig(r_text, text = r_score)


def Update():
    if pause == False:
        ball_move()
        ball_ricochet()
        pads_move()
        lpad_controller()
        rpad_controller()
        score()
    root.after(16, Update)

root.state('zoomed')
Update()
text_update()
root.mainloop()