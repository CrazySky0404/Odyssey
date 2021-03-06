from tkinter import *

from PIL import Image, ImageTk
from random import randint
from time import sleep, time
from math import sqrt

WIDTH = 1000
HEIGHT = 600

top = Tk()
top.title('Одиссея')

w = Canvas(top, bg="blue", width=WIDTH, height=HEIGHT)
w.pack()

image = ImageTk.PhotoImage(file="img/fon.jpg")
w.create_image(0, 0, image=image, anchor=NW)

hat_id = w.create_polygon(-30, 5, -30, -5, -40, -5, fill='black')
hat_id2 = w.create_polygon(30, -5, 30, 5, 40, -5, fill='black')
hat_id3 = w.create_rectangle(-30, 5, 30, -5, fill='black', width=0)
hat_id4 = w.create_rectangle(-30, 15, 30, 5, fill='red', width=0)
hat_id5 = w.create_rectangle(-30, 35, 30, 15, fill='black', width=0)

HAT_R = 15
MID_X = WIDTH / 2
MID_Y = HEIGHT / 2
w.move(hat_id, MID_X, MID_Y)
w.move(hat_id2, MID_X, MID_Y)
w.move(hat_id3, MID_X, MID_Y)
w.move(hat_id4, MID_X, MID_Y)
w.move(hat_id5, MID_X, MID_Y)
HAT_SPD = 10


def move_hat(event):
    if event.keysym == 'Up':
        w.move(hat_id, 0, -HAT_SPD)
        w.move(hat_id2, 0, -HAT_SPD)
        w.move(hat_id3, 0, -HAT_SPD)
        w.move(hat_id4, 0, -HAT_SPD)
        w.move(hat_id5, 0, -HAT_SPD)

    elif event.keysym == 'Down':
        w.move(hat_id, 0, HAT_SPD)
        w.move(hat_id2, 0, HAT_SPD)
        w.move(hat_id3, 0, HAT_SPD)
        w.move(hat_id4, 0, HAT_SPD)
        w.move(hat_id5, 0, HAT_SPD)

    elif event.keysym == 'Left':
        w.move(hat_id, -HAT_SPD, 0)
        w.move(hat_id2, -HAT_SPD, 0)
        w.move(hat_id3, -HAT_SPD, 0)
        w.move(hat_id4, -HAT_SPD, 0)
        w.move(hat_id5, -HAT_SPD, 0)

    elif event.keysym == 'Right':
        w.move(hat_id, HAT_SPD, 0)
        w.move(hat_id2, HAT_SPD, 0)
        w.move(hat_id3, HAT_SPD, 0)
        w.move(hat_id4, HAT_SPD, 0)
        w.move(hat_id5, HAT_SPD, 0)


w.bind_all('<Key>', move_hat)

coin_id = list()
coin_r = list()
coin_speed = list()
MIN_COIN_R = 10
MAX_COIN_R = 30
MAX_COIN_SPEED = 10
GAP = 200


def get_coords(id_num):
    pos = w.coords(id_num)
    x = (pos[0] + pos[2]) / 2
    y = (pos[1] + pos[3]) / 2
    return x, y


def create_coin():
    x = WIDTH + GAP
    y = randint(0, HEIGHT)
    r = randint(MIN_COIN_R, MAX_COIN_R)
    id1 = w.create_oval(x - r, y - r, x + r, y + r, outline='#FF9900', width=10)
    coin_id.append(id1)
    coin_r.append(r)
    coin_speed.append(MAX_COIN_SPEED)


def move_coin():
    for i in range(len(coin_id)):
        print(i)
        print(len(coin_id))
        print(coin_id, coin_speed)
        print(coin_id[i], -coin_speed[i])
        w.move(coin_id[i], -coin_speed[i], 0)


def del_coin(i):
    del coin_r[i]
    del coin_speed[i]
    w.delete(coin_id[i])
    del coin_id[i]


def clean_up_coins():
    for i in range(len(coin_id) - 1, -1, -1):
        x, y = get_coords(coin_id[i])
        if x < -GAP:
            del_coin(i)


def distance(id1, id2):
    x1, y1 = get_coords(id1)
    x2, y2 = get_coords(id2)
    return sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def collision():
    points = 0
    for coin in range(len(coin_id) - 1, -1, -1):
     if distance(hat_id2, coin_id[coin]) < (HAT_R + coin_r[coin]):
        points += (coin_r[coin] + coin_speed[coin])
        del_coin(coin)
    return points


w.create_text(50, 30, text='Время', fill="blue")
w.create_text(150, 30, text='ВАШ СЧЕТ', fill="blue")
time_text = w.create_text(50, 50, fill="black")
score_text = w.create_text(150, 50, fill="black")

COIN_CHANCE = 10
TIME_LIMIT = 10
BONUS_SCORE = 1000
score = 0
bonus = 0
end = time() + TIME_LIMIT


def show_score(score):
    w.itemconfig(score_text, text=str(score))


def show_time(time_left):
    w.itemconfig(time_text, text=str(time_left))


while time() < end:
    if randint(1, COIN_CHANCE) == 1:
        create_coin()
        move_coin()
        clean_up_coins()
        score += collision()
        if (int(score / BONUS_SCORE)) > bonus:
            bonus = + 1
            end += TIME_LIMIT
        show_score(score)
        show_time(int(end - time()))
        print(score)
        top.update()
        sleep(0.01)


w.create_text(MID_X, MID_Y, text="Игра окончена", fil="blue", font=('Helvetica', 30))
w.create_text(MID_X, MID_Y + 30, text="ВАШ СЧЕТ: " + str(score), fil="blue")
w.create_text(MID_X, MID_Y + 45, text="Бонусное время: " + str(bonus * TIME_LIMIT), fil="blue")

# top.mainloop()
