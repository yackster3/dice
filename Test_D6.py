from ursina import *
import random as rand
from ursina.prefabs.first_person_controller import FirstPersonController
import dice



"""
    This sequence just creates a d6 Die that allows you to roll it.
"""

app = Ursina()

d = dice.d6()

#myGrid = Entity(model = Grid(3,5), color = color.rgb(255,0,0))


floor = Entity(model = "plane", position = (0,-4,0), scale = (100,.1,100), color = color.rgb(25,165,25), texture= 'grass', collider = 'mesh')
Sky()


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
