from ursina import *
import random as rand
from ursina.prefabs.first_person_controller import FirstPersonController

"""
 TODO:
    d6:
        need to color the individual faces, get numbers on each one and in the
        proper positions (only 6 possible starting positions required)

        the settling animation requires some work, only 2 angles should be used
        but determining which 2 will be interesting.

    d4:
        Die needs new focus points on where exactly it's supposed to fall.
        the faces aren't all showing at all times.

        it still falls like a d6

    a lot more debugging
"""

class d6(Entity):
    def __init__(self, **kwargs):
        super().__init__(self, **kwargs)
        self.model = "cube"
        self.texture = "white_cube"
        self.collider = 'box'
        self.rgb = (0,255,0)
        self.rolling = False
        self.rolling_speed = 20
        self.omega_x = 0
        self.omega_y = 0
        self.omega_z = 0
        self.speed_x = 0
        self.speed_y = 0
        self.speed_z = 0
        self.rebound = .75
        self.pause = False
        self.floor = False


    def roll(self):
        self.omega_x = rand.random()*1000
        self.omega_y = rand.random()*1000
        self.omega_z = rand.random()*1000
        self.speed_y = self.rolling_speed
        self.floor = False


    def motion(self):
        #rotation speed
        self.rotation_x += self.omega_x * time.dt
        self.rotation_y += self.omega_y * time.dt
        self.rotation_z += self.omega_z * time.dt

        #translation speed
        self.x += self.speed_x * time.dt
        self.y += self.speed_y * time.dt
        self.z += self.speed_z * time.dt

    def gravity(self):
        if not self.floor:
            #gravity
            self.speed_y -= 9.81 * time.dt


    def bounce(self):
        #floor
        if self.y < -3:
            self.y = -3
            #Impact on the floor

            impact = abs(self.speed_y - (self.speed_y * self.rebound))

            #reaction based on the impact of the floor
            #Here it is becoming static
            if impact < .35:
                self.omega_x = 0
                self.omega_y = 0
                self.omega_z = 0
                self.y = -3
                self.floor = True

            #Here it is nestling
            elif impact < .9:
                self.speed_y = -self.rebound * self.speed_y

                X = self.rotation_x + 45
                Y = self.rotation_y + 45
                Z = self.rotation_z + 45

                X = (X // 90) * 90
                Y = (Y // 90) * 90
                Z = (Z // 90) * 90

                self.omega_x = X - self.rotation_x
                self.omega_y = Y - self.rotation_y
                self.omega_z = Z - self.rotation_z

            #Here it is bouncing wildly
            else:
                self.speed_y = -self.rebound * self.speed_y

                #rotation bounce
                self.omega_x = 3.5 * self.omega_x * (.5 - rand.random())
                self.omega_y = 3.5 * self.omega_y * (.5 - rand.random())
                self.omega_z = 3.5 * self.omega_z * (.5 - rand.random())



    def update(self):
        #keep rotation angle convienient
        self.rotation_x = self.rotation_x % 360
        self.rotation_y = self.rotation_y % 360
        self.rotation_z = self.rotation_z % 360

        #Check if it's in play
        if not self.pause:
            self.motion()
            self.gravity()
            self.bounce()


    def input(self, key):
        #roll the die
        if key == "space":
            self.roll()

        #toggle pause function
        if key == "p":
            self.pause = not self.pause
class d4(Entity):
    def __init__(self, **kwargs):
        super().__init__(self, **kwargs)
        #Build the d4 shape
        self.verts = ((1,1,1), (1,-1,-1), (-1,1,-1), (-1,-1,1))
        self.tris = (0, 1, 2, 1, 2, 3, 0, 2, 3, 0, 1, 3,
                        3, 1, 0, 3, 2, 0, 3, 2, 1, 2, 1, 3,
                        1, 3, 2, 2, 3, 1, 1, 0, 2, 2, 0, 3)

        # TODO:  What are these?
        self.uvs = ((1,0), (0,1), (0,0), (1,1))
        self.norms = ((0, 0, -1),)*len(self.verts)

        #assigning colors to the corners?
        self.colors = (color.red, color.blue, color.lime, color.black)

        #constructing the model
        self.model = Mesh(vertices = self.verts, triangles = self.tris, uvs = self.uvs,
                            normals = self.norms, colors = self.colors)

        self.texture = "white_cube"
        self.collider = 'box'
        self.rolling = False
        self.rolling_speed = 20
        self.omega_x = 0
        self.omega_y = 0
        self.omega_z = 0
        self.speed_x = 0
        self.speed_y = 0
        self.speed_z = 0
        self.rebound = .75
        self.pause = False
        self.floor = False


    def roll(self):
        self.omega_x = rand.random()*1000
        self.omega_y = rand.random()*1000
        self.omega_z = rand.random()*1000
        self.speed_y = self.rolling_speed
        self.floor = False


    def motion(self):
        #rotation speed
        self.rotation_x += self.omega_x * time.dt
        self.rotation_y += self.omega_y * time.dt
        self.rotation_z += self.omega_z * time.dt

        #translation speed
        self.x += self.speed_x * time.dt
        self.y += self.speed_y * time.dt
        self.z += self.speed_z * time.dt

    def gravity(self):
        if not self.floor:
            #gravity
            self.speed_y -= 9.81 * time.dt


    def bounce(self):
        #floor
        if self.y < -3:
            self.y = -3

            #Impact on the floor
            impact = abs(self.speed_y - (self.speed_y * self.rebound))

            #reaction based on the impact of the floor
            #Here it is becoming static
            if impact < .35:
                self.omega_x = 0
                self.omega_y = 0
                self.omega_z = 0
                self.y = -3
                self.floor = True

            #Here it is nestling
            elif impact < .9:
                self.speed_y = -self.rebound * self.speed_y

                X = self.rotation_x + 45
                Y = self.rotation_y + 45
                Z = self.rotation_z + 45

                X = (X // 90) * 90
                Y = (Y // 90) * 90
                Z = (Z // 90) * 90

                self.omega_x = X - self.rotation_x
                self.omega_y = Y - self.rotation_y
                self.omega_z = Z - self.rotation_z

            #Here it is bouncing wildly
            else:
                self.speed_y = -self.rebound * self.speed_y

                #rotation bounce
                self.omega_x = 3.5 * self.omega_x * (.5 - rand.random())
                self.omega_y = 3.5 * self.omega_y * (.5 - rand.random())
                self.omega_z = 3.5 * self.omega_z * (.5 - rand.random())



    def update(self):
        #keep rotation angle convienient
        self.rotation_x = self.rotation_x % 360
        self.rotation_y = self.rotation_y % 360
        self.rotation_z = self.rotation_z % 360

        #Check if it's in play
        if not self.pause:
            self.motion()
            self.gravity()
            self.bounce()


    def input(self, key):
        #roll the die
        if key == "r":
            self.roll()
            print(self.colors)
        #toggle pause function
        if key == "p":
            self.pause = not self.pause

app = Ursina()

d = d4()
floor = Entity(model = "plane", position = (0,-4,0), scale = (100,.1,100), color = color.rgb(25,165,25), texture= 'grass', collider = 'mesh')
Sky()
print(color.random_color)

#Camera when rolling
"""
camera.position = (0,5,-55)

def update():
    camera.look_at(d)

"""


"""
    Extra testing code
"""
verts = ((0,0,0), (1,0,0), (.5, 1, 0), (-.5,1,0))
tris = (1, 2, 0, 2, 3, 0)
uvs = ((1.0, 0.0), (0.0, 1.0), (0.0, 0.0), (1.0, 1.0))
norms = ((0,0,-1),) * len(verts)
colors = (color.red, color.blue, color.lime, color.black)


e = Entity(model=Mesh(vertices=verts, triangles=tris, uvs=uvs, normals=norms, colors=colors), scale=2)
verts = (Vec3(0,0,0), Vec3(0,1,0), Vec3(1,1,0), Vec3(2,2,0), Vec3(0,3,0), Vec3(-2,3,0))
tris = ((0,1), (3,4,5))

lines = Entity(model=Mesh(vertices=verts, triangles=tris, mode='line', thickness=4), color=color.cyan, z=-1)
points = Entity(model=Mesh(vertices=verts, mode='point', thickness=.05), color=color.red, z=-1.01)


"""
    testing code end
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
