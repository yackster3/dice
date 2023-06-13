from ursina import *
import random as rand
from ursina.prefabs.first_person_controller import FirstPersonController
import dice



app = Ursina()

d = dice.d4()
floor = Entity(model = "plane", position = (0,-4,0), scale = (100,.1,100), color = color.rgb(25,165,25), texture= 'grass', collider = 'mesh')
Sky()
print(color.random_color)

#Camera when rolling
"""
camera.position = (0,5,-55)

def update():
    camera.look_at(d)

"""

player = FirstPersonController(y=1, enabled=True)

ec = EditorCamera()
ec.enabled = False
rotation_info = Text(position=window.top_left)

def update():
    rotation_info.text = str(int(ec.rotation_y)) + '\n' + str(int(ec.rotation_x))


def input(key):
    if key == 'tab':    # press tab to toggle edit/play mode
        ec.enabled = not ec.enabled
        player.enabled = not player.enabled

app.run()
