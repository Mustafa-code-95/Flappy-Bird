from ursina import Ursina
from ursina import Entity
from ursina import color
from ursina import camera
from ursina import invoke
from ursina import time
from ursina import held_keys
from ursina import clamp
from ursina import Text
from ursina import destroy
import random

app = Ursina()

background = Entity(
    model='quad',
    texture='background.jpg',
    scale=(20, 10),
    z=1
    )

wiese = Entity(
    model='quad',
    texture='wiese.jpg',
    scale=(20, 2.5),
    position=(0, -5),
    z=-1
    )

re = None
play = None
game_start = False
points = 0
v_speed = 0
gravity = -4
jump = 0
jump_strength = 3
game_over = False
rohrr = None
rohre = []
liste = []
j = []

scoe = Text(text='', origin=(0, -0.5), scale=2, color=color.white)
mytext = Text(text='', position=(0, 2.5), scale=2)
a = Text(text='', origin=(0, -3), scale=5, color=color.black)
player = Entity(model='cube', color=color.white, texture='Flappy_Bird', position=(0, 3), scale=(0.5, 0.5), collider='box')


class rohr:
    def __init__(self):
        self.rohr_x = 9
        self.rohr_position = random.randint(-1, 2)

        self.rohr_oben = Entity(model='cube', color=color.white, texture='rohr1', position=(self.rohr_x, self.rohr_position - 4), scale=(1, 5), collider='box')
        self.rohr_unten = Entity(model='cube', color=color.white, texture='rohr', position=(self.rohr_x, self.rohr_position + 4), scale=(1, 5), collider='box')

    def weiter(self, speed):
        self.rohr_oben.x -= speed * time.dt
        self.rohr_unten.x -= speed * time.dt


def add_rohr():
    global rohrr, rohre
    rohrr = rohr()
    rohre.append(rohrr)


def restart_game():
    global points, v_speed, re, rohre, play, mytext, player, scoe, jump

    scoe.text = ''
    jump = 0
    points = 0
    mytext.text = 'Score: 0'
    v_speed = 0

    destroy(re)
    re = None

    player.y = 3

    for r in rohre:
        destroy(r.rohr_oben)
        destroy(r.rohr_unten)
    rohre.clear()


def add():
    global game_over, points, mytext
    if not game_over:
        add_rohr()
        points += 1
        mytext.text = f'Score: {points}'
        invoke(add, delay=random.randint(3, 5))


def adding():
    print('return restart')


def update():
    global rohre, game_over, player, v_speed, jump_strength, gravity, wiese, a, game_start, play, re, scoe, liste, jump, j

    if not game_over and game_start:
        if held_keys['space']:
            v_speed = jump_strength

        v_speed += gravity * time.dt
        player.y += v_speed * time.dt

        if player.intersects(wiese).hit:
            game_over = True
            re = Entity(model='cube', color=color.white, texture='re', scale=(4, 1.7), position=(0, -1), collider='box', z=-1)

        for r in rohre:
            if r.rohr_oben.position > 9:
                destroy(r)
            if player.intersects(r.rohr_oben).hit or player.intersects(r.rohr_unten).hit:
                re = Entity(model='cube', color=color.white, texture='re', scale=(4, 1.7), position=(0, -1), collider='box', z=-1)
                game_over = True
            r.weiter(1)
        player.y = clamp(player.y, -3.5, 4.5)
    elif not game_start:
        if play == None:
            play = Entity(model='cube', color=color.white, texture='play', scale=(4, 1.7), position=(0, -0.5), collider='box')
            background.texture = 'flapy'
        if play and play.hovered and held_keys['left mouse']:
            background.texture = 'background'
            destroy(play)
            game_start = True
            add()
    else:
        j = j + [jump]
        liste = liste + [points]
        nu = max(liste)
        no = max(j)
        scoe.text = f'Hightscore: {nu}\nScore: {points}\nMax Jumps: {no}\nJumps: {jump}\nMax Actions: {no + nu}\nActions: {jump + points}'
        a.text = 'Game Over'
        invoke(adding, delay=3)
        if re and re.hovered and held_keys['left mouse']:
            a.text = ''
            restart_game()
            invoke(adding, delay=2)
            game_over = False
            invoke(add, delay=3)


def input(key):
    global jump, game_over, re
    if not game_over and key == 'space':
        jump += 1


camera.orthographic = True
camera.fov = 10

app.run()
