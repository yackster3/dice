from ursina import *
import random as rand

class d6(Entity):
    def __init__(self, **kwargs):
        super().__init__(self, **kwargs)
        self.model = "cube"
        self.texture = "white_cube"
        self.rgb = (0,255,0)
        self.rolling = False
        self.omega_x = 0
        self.omega_y = 0
        self.omega_z = 0
        self.speed_x = 0
        self.speed_y = 0
        self.speed_z = 0
        self.pause = False
        self.rebound = .75
        self.floor = False

    def roll(self):
        rotation_x = rand.random()*1000
        rotation_y = rand.random()*1000
        rotation_z = rand.random()*1000
        self.speed_y = 10


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
            self = -3
            #Hit the floor
            if abs(self.speed_y - self.speed_y * self.rebound) < .01:
                self.speed_y = 0

            else:
                self.speed_y = -self.rebound * self.speed_y

                #rotation bounce
                self.rotation_x = -2 * self.rotation_x * (.5 - rand.random())
                self.rotation_y = -2 * self.rotation_y * (.5 - rand.random())
                self.rotation_z = -2 * self.rotation_z * (.5 - rand.random())

        elif self.y == -3:
            self.floor = True

        if self.floor and self.y != -3:
            self.floor = False



    def update(self):
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

app = Ursina()

d = d6()

app.run()
