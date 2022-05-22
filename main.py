import tkinter
from tkinter import *
import time
import random

class Bug:
    def __init__(self, pos, speed, shape, canvas):
        self.pos = pos
        self.speed = speed
        self.shape = shape
        self.canvas = canvas
        self.score = 0

    def add_points(self, points):
        self.score += points

    def get_points(self):
        return self.score

    def hide(self):
        self.canvas.delete(self.shape)

    def move(self, food_list):
        # move it to food
        move_x = 0
        move_y = 0

        if len(food_list) > 0:
            nearest = food_list[0] # make sure that when they get landed on they get removed
            distance = float("inf")

            for food in food_list:
                next_distance = abs(self.pos[0] - food.get_pos()[0]) + abs(self.pos[1] - food.get_pos()[1])
                if next_distance < distance:
                    distance = next_distance
                    nearest = food

            # x_diff x^2 + y_diff x^2 = speed^2 gets turined into this mess with some algebra
            x = ((self.speed**2) / ((self.pos[0] - nearest.get_pos()[0])**2 + (self.pos[1] - nearest.get_pos()[1])**2)) ** (1/2)

            if (((self.pos[0] - nearest.get_pos()[0]))**2 + ((self.pos[1] - nearest.get_pos()[1]))**2)**(1/2) <= self.speed:
                self.canvas.move(self.shape, self.pos[0] - nearest.get_pos()[0], self.pos[1] - nearest.get_pos()[1])
                self.pos = nearest.get_pos()
                self.add_points(food.get_points())
                return nearest
            else:
                # move the bug on the canvas
                self.canvas.move(self.shape, -(x * (self.pos[0] - nearest.get_pos()[0])), -(x * (self.pos[1] - nearest.get_pos()[1])))
                # update the bug on its position
                self.pos = (self.pos[0]-(x * (self.pos[0] - nearest.get_pos()[0])), self.pos[1]-(x * (self.pos[1] - nearest.get_pos()[1])))

class Food:
    def __init__(self, healing_points, pos, oval, canvas):
        self.healing_points = healing_points
        self.pos = pos
        self.shape = oval
        self.canvas = canvas

    def get_pos(self):
        return self.pos

    def get_points(self):
        return self.healing_points

    def hide(self):
        self.canvas.delete(self.shape)



def main():
    win=tkinter.Tk()

    canvas = Canvas(win, width=800, height=800)

    ret_val = newGen(canvas)

    canvas.pack()

    generations = 5
    for i in range(generations):
        test(win, 0, ret_val[0], ret_val[1])

        hide_all(ret_val[0], ret_val[1], canvas, win)

        ret_val = newGen(canvas)


    hide_all(ret_val[0], ret_val[1], canvas, win)



def hide_all(bugs, foods, canvas, window):
    for bug in bugs:
        bug.hide()

    for food in foods:
        food.hide()

    window.update()

def newGen(canvas):
    radius = 5
    bugs = []
    food = []

    for i in range(200):
        pos = (random.random()*800, random.random()*800)
        oval=canvas.create_oval(pos[0]-radius, pos[1]-radius, pos[0]+radius, pos[1]+radius, fill='green')
        food += [Food(10, pos, oval, canvas)]

    for i in range(20):
        pos = (random.random()*800, random.random()*800)
        speed = random.random()*5
        oval=canvas.create_oval(pos[0]-radius, pos[1]-radius, pos[0]+radius, pos[1]+radius, fill='blue')
        bugs += [Bug(pos, speed, oval, canvas)]

    canvas.pack()

    return (bugs, food)


def test(win, count, bugs, food_list):
    for b in bugs:
        ret_val = b.move(food_list)
        if ret_val != None:
            food_list.remove(ret_val)
            ret_val.hide()

    win.update()

    if count < 400:
        time.sleep(.01)
        test(win, count+1, bugs, food_list)


if __name__ == '__main__':
    main()
