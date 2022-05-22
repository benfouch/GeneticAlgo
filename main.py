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
        print(oval)

    def get_pos(self):
        return self.pos

    def get_healing(self):
        return self.healing_points

    def hide(self):
        self.canvas.delete(self.shape)



def main():
    win=tkinter.Tk()

    canvas = Canvas(win, width=700, height=700)

    radius = 5
    bugs = []
    food = []


    for i in range(100):
        pos = (random.random()*650, random.random()*650)
        oval=canvas.create_oval(pos[0]-radius, pos[1]-radius, pos[0]+radius, pos[1]+radius, fill='green')
        food += [Food(10, pos, oval, canvas)]

    for i in range(20):
        pos = (random.random()*650, random.random()*650)
        speed = random.random()*15
        oval=canvas.create_oval(pos[0]-radius, pos[1]-radius, pos[0]+radius, pos[1]+radius, fill='blue')
        bugs += [Bug(pos, speed, oval, canvas)]



    canvas.pack()

    test(win, 0, bugs, food)
    win.mainloop()


def test(win, count, bugs, food_list):
    for b in bugs:
        ret_val = b.move(food_list)
        if ret_val != None:
            food_list.remove(ret_val)
            ret_val.hide()

    win.update()

    if count < 400:
        time.sleep(.05)
        test(win, count+1, bugs, food_list)


if __name__ == '__main__':
    main()
