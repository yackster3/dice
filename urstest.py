from ursina import *
import random as rand
# create a function called 'update'.
# this will automatically get called by the engine every frame.

def update():
    #translation speeds
    global speed_x
    global speed_y
    global speed_z

    #rotation speeds
    global rotation_x
    global rotation_y
    global rotation_z

    #dampening collisions
    damp = .7

    #player input
    player.x += held_keys['d'] * time.dt
    player.x -= held_keys['a'] * time.dt
    player.y += held_keys['w'] * time.dt
    player.y -= held_keys['s'] * time.dt

    #translation adjustments
    player.y += speed_y * time.dt
    player.x += speed_x * time.dt
    player.z += speed_z * time.dt

    #gravity
#    speed_y += -9.81 * time.dt

    #floor
    if player.y < -3:
        speed_y = -damp * speed_y

        r = rand.random()

        """
        This is to adjust the rotation each time the player hits the floor.
        """
        if abs(speed_y) < 2:

            """
            todo:
            Vec3 doesn't work well with int data types. I need these operations
            to act as though they are vectors in the mathematical sense...
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

        elif r > 1-1/8:
            rotation_x = rotation_x * rand.random() * 1/damp
            rotation_y = rotation_y * rand.random() * 1/damp
            rotation_z = rotation_z * rand.random() * 1/damp
        elif r > 1-1/4:
            rotation_x = rotation_x * -rand.random() * 1/damp
            rotation_y = rotation_y * rand.random() * 1/damp
            rotation_z = rotation_z * rand.random() * 1/damp
        elif r > 1-3/8:
            rotation_x = rotation_x * rand.random() * 1/damp
            rotation_y = rotation_y * -rand.random() * 1/damp
            rotation_z = rotation_z * rand.random() * 1/damp
        elif r > 1-1/2:
            rotation_x = rotation_x * -rand.random() * 1/damp
            rotation_y = rotation_y * -rand.random() * 1/damp
            rotation_z = rotation_z * rand.random() * 1/damp
        elif r > 1-5/8:
            rotation_x = rotation_x * rand.random() * 1/damp
            rotation_y = rotation_y * rand.random() * 1/damp
            rotation_z = rotation_z * -rand.random() * 1/damp
        elif r > 1-3/4:
            rotation_x = rotation_x * -rand.random() * 1/damp
            rotation_y = rotation_y * rand.random() * 1/damp
            rotation_z = rotation_z * -rand.random() * 1/damp
        elif r > 1-7/8:
            rotation_x = rotation_x * rand.random() * 1/damp
            rotation_y = rotation_y * -rand.random() * 1/damp
            rotation_z = rotation_z * -rand.random() * 1/damp
        else:
            rotation_x = rotation_x * -rand.random() * 1/damp
            rotation_y = rotation_y * -rand.random() * 1/damp
            rotation_z = rotation_z * -rand.random() * 1/damp

    #walls
    if abs(player.x) > 4:
        speed_x = -damp * speed_x

        rotation_x = rotation_x * rand.random()
        rotation_y = rotation_y * rand.random()
        rotation_z = rotation_z * rand.random()

    if abs(player.z) > 4:
        speed_z = -damp * speed_z

        rotation_x = rotation_x * rand.random()
        rotation_y = rotation_y * rand.random()
        rotation_z = rotation_z * rand.random()

    #change rotations
    player.rotation_x = player.rotation_x + time.dt * rotation_x
    player.rotation_y = player.rotation_y + time.dt * rotation_y
    player.rotation_z = player.rotation_z + time.dt * rotation_z

# this part will make the player move left or right based on our input.
# to check which keys are held down, we can check the held_keys dictionary.
# 0 means not pressed and 1 means pressed.
# time.dt is simply the time since the last frame. by multiplying with this, the
# player will move at the same speed regardless of how fast the game runs.

def input(key):
    #translation speeds
    global speed_x
    global speed_y
    global speed_z

    #rotation speeds
    global rotation_x
    global rotation_y
    global rotation_z

    #changing rotation speeds
    if key == 't':
        rotation_x += 25
    if key == 'g':
        rotation_y += 25
    if key == 'b':
        rotation_z += 25
    if key == 'y':
        rotation_x -= 27
    if key == 'h':
        rotation_y -= 27
    if key == 'n':
        rotation_z -= 27
    if key == '1':
        speed_x = 0
        speed_y = 0
        speed_z = 0
        rotation_x = 0
        rotation_y = 0
        rotation_z = 0

    #move the camera
    if key == 'down_arrow':
        camera.y -= 5
    if key == 'up_arrow':
        camera.y += 5
    if key == 'left_arrow':
        camera.z -= 5
    if key == 'right_arrow':
        camera.z += 5


    #tosses the object randomly
    if key == 'space':
        rotation_x = rand.random()*1000
        rotation_y = rand.random()*1000
        rotation_z = rand.random()*1000
#        speed_y = 20

    #stop everything
    if key == 'p':
        rotation_x = 0
        rotation_y = 0
        rotation_z = 0

    #ToDo ursina keeps closing poorly
    if key == 'escape':
        print("rotation: " + str(player.rotation))
        print("position: " + str(player.position))
        app.destroy()
        return


# create a window
app = Ursina()

#translation speeds
speed_x = 0
speed_y = 0
speed_z = 0

#rotation speeds
rotation_x = 0
rotation_y = 0
rotation_z = 0

# most things in ursina are Entities. An Entity is a thing you place in the world.
# you can think of them as GameObjects in Unity or Actors in Unreal.
# the first parameter tells us the Entity's model will be a 3d-model called 'cube'.
# ursina includes some basic models like 'cube', 'sphere' and 'quad'.

# the next parameter tells us the model's color should be orange.

# 'scale_y=2' tells us how big the entity should be in the vertical axis, how tall it should be.
# in ursina, positive x is right, positive y is up, and positive z is forward.

player = Entity(model='cube', rotation = (0,0,0), color=color.rgb(255,255,255), texture = "white_cube")
camera.position = (0,5,-55)

# start running the game
app.run()
