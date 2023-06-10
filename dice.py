from ursina import *
import random as rand

class d6(Entity):
    def __init__(self, **kwargs):
        super().__init__(self, **kwargs)
        self.model = "cube"
        self.texture = "white_cube"
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
            #Hit the floor
            impact = abs(self.speed_y - (self.speed_y * self.rebound))
            if impact < .1:
                self.speed_y = -self.rebound * self.speed_y

                #setting speeds to 0
                self.omega_x = 0
                self.omega_y = 0
                self.omega_z = 0

                #rotation bounce
                self.rotation_x = self.rotation_x * rand.random()
                self.rotation_y = self.rotation_y * rand.random()
                self.rotation_z = self.rotation_z * rand.random()
                """
                            #get workable rotation values
                            rot = []
                            for rotate in player.rotation:
                                rot.append(rotate//360)

                            #see which sides are closest.
                            for i in range(0,len(rot)):
                                rot[i] = (rot[i] % 4) * 90

                            player.rotation_x = rot[0]
                            player.rotation_y = rot[1]
                            player.rotation_z = rot[2]
                            print("rotation:" + str(rot))
                            speed_y = 0
                """


            else:
                self.speed_y = -self.rebound * self.speed_y

                #rotation bounce
                self.omega_x = 3 * self.omega_x * (.5 - rand.random())
                self.omega_y = 3 * self.omega_y * (.5 - rand.random())
                self.omega_z = 3 * self.omega_z * (.5 - rand.random())

        elif self.y + 3 < .00001:
            self.speed_y = 0
            self.floor = True

        if self.floor and self.y != -3:
            self.floor = False



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

camera.position = (0,5,-55)

app.run()
