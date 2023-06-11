from ursina import *
import random as rand
from ursina.prefabs.first_person_controller import FirstPersonController


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
        if key == "space":
            self.roll()

        #toggle pause function
        if key == "p":
            self.pause = not self.pause

app = Ursina()

d = d6()
floor = Entity(model = "plane", position = (0,-4,0), scale = (100,.1,100), color = color.rgb(25,165,25), texture= 'grass', collider = 'mesh')
Sky()

camera.position = (0,5,-55)

def update():
    camera.look_at(d)

app.run()
