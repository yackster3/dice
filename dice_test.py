import dice
import random


anglesList = [[135, 135, 135],
                [135, 135, 45],
                [135, 45, 135],
                [45, 135, 135]]

origin = [0,0,0]


def Test_NearestAngle():
    if [135,135,135] == dice.NearestAngle(origin, anglesList):
        print("Test 1: Success")
    else:
        print("Test 1: Failure")
    return "Complete"
