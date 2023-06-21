from ursina import *
import random as rand
from ursina.prefabs.first_person_controller import FirstPersonController
import numpy as np

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
                self.omega_x = 3 * self.omega_x * (.5 - rand.random())
                self.omega_y = 3 * self.omega_y * (.5 - rand.random())
                self.omega_z = 3 * self.omega_z * (.5 - rand.random())



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

        #toggle pause function
        if key == "p":
            self.pause = not self.pause
class d4(Entity):
    def __init__(self, **kwargs):
        super().__init__(self, **kwargs)
        #Build the d4 shape
        self.verts = ((1,1,1), (-1,1,-1), (-1,-1,1), (1,-1,-1))
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
        self.diff = 1

    def roll(self):
        self.omega_x = rand.random()*1000
        self.omega_y = rand.random()*1000
        self.omega_z = rand.random()*1000
        self.speed_y = self.rolling_speed
        self.floor = False
        print(self.norms)

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
            if self.diff < .001 and not self.floor:
                self.omega_x = 0
                self.omega_y = 0
                self.omega_z = 0
                self.y = -3
                self.floor = True

            #Here it is nestling
            elif impact < 1:
                self.speed_y = -self.rebound * self.speed_y

                cur = np.array([self.rotation_x, self.rotation_y, self.rotation_z])

                #possible landing positions
                #decent
                f1 = np.array([35.26, 7, 42.26])
                f2 = np.array([155, 0, 45])
                f3 = np.array([215.26, 187, 222.26])
                f4 = np.array([330, 0, 135])

                angles = [f1,f2,f3,f4]

                settle = NearestAngle(cur, angles)

                self.omega_x = settle[0] - self.rotation_x
                self.omega_y = settle[1] - self.rotation_y
                self.omega_z = settle[2] - self.rotation_z

                print("target: " + str(settle))
                print("currrent: " + str(cur))

            #Here it is bouncing wildly
            else:
                self.speed_y = -self.rebound * self.speed_y

                #rotation bounce
                self.omega_x = impact * self.omega_x * (.5 - rand.random())
                self.omega_y = impact * self.omega_y * (.5 - rand.random())
                self.omega_z = impact * self.omega_z * (.5 - rand.random())



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

        elif self.pause:
            """
                This stuff was put in to help pause the game and move
                stuff around to see what is what...
            """
            #player input
            self.rotation_x += held_keys['j'] * time.dt
            self.rotation_x -= held_keys['l'] * time.dt
            self.rotation_y += held_keys['i'] * time.dt
            self.rotation_y -= held_keys['k'] * time.dt
            self.rotation_z += held_keys['o'] * time.dt
            self.rotation_z -= held_keys['u'] * time.dt

    def input(self, key):
        #roll the die
        if key == "r":
            self.roll()
            print(self.colors)
        #toggle pause function
        if key == "p":
            self.pause = not self.pause
        if key == "0":
            self.rotation_x = 0
            self.rotation_y = 0
            self.rotation_z = 0

        if key == "1":
            self.rotation_x = 28.5869
            self.rotation_z = 28.5869

        if key == "2":
            self.rotation_x = 61.4131
            self.rotation_y = 61.4131

#       f3 = np.array([215.26, 187, 222.26])
        if key == "3":
            self.rotation_x = 139.240
            self.rotation_z = 139.240

        if key == "4":
            self.rotation_x = 40.7598
            self.rotation_y = 40.7598

        if key == "x":
            self.rotation_x += 15

        if key == "g":
            self.rotation_x += 1
            self.rotation_z += 1
        if key == "h":
            self.rotation_y += 1
            self.rotation_z += 1
        if key == "j":
            self.rotation_y += 1
            self.rotation_x += 1

        if key == "y":
            self.rotation_y += 15

        if key == "z":
            self.rotation_z += 15
        if key == "m":
            print(str((self.rotation_x,self.rotation_y,self.rotation_z)))
"""
    inputs: single vector of angles as cur, list of vectors of angles as angles


    This finds the nearest angle in cyclic algebras of modulus 360

"""
def NearestAngle(cur, angles, modulus = [360,360,360]):

    #Max value possible in function
    #val = 3*180**2
    #Min value possible in function
    val = 0
    #near array is empty
    near = []
    for ang in angles:

        #resets next array
        next = []
        print("Angle: " + str(ang))

        for i in range(0, len(cur)):

            #Appends the smallest value to each component
            alpha = ((cur[i] - ang[i]) % modulus[i])
            beta = ((cur[i] - ang[i]) % modulus[i] - modulus[i])

            print("Alpha: " + str(alpha**2))
            print("Beta: " + str(beta**2))

            next.append(max(alpha**2, beta**2))

        #Check if the currrently examined angle is nearer or further.
        print("next: " + str(next))
        if sum(next) > val:
            near = ang
            val = sum(next)
        print("Val: " + str(val))

    return near
