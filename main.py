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

    def move(self):
        # move it to food
        self.canvas.move(self.shape, self.speed, self.speed)

class Food:
    def __init__(self, healing_points, ):



def main():
    win=tkinter.Tk()

    canvas = Canvas(win, width=700, height=700)

    radius = 5
    bugs = []
    food = []

    for i in range(5):
        pos = (random.random()*650, random.random()*650)
        speed = random.random()*15
        oval=canvas.create_oval(pos[0]-radius, pos[1]-radius, pos[0]+radius, pos[1]+radius, fill='blue')
        bugs += [Bug(pos, speed, oval, canvas)]


    for i in range(10):
        pos = (random.random()*650, random.random()*650)
        food += []


    canvas.pack()

    test(win, 0, bugs)
    win.mainloop()


def test(win, count, bugs):
    for b in bugs:
        b.move()

    win.update()

    if count < 20:
        time.sleep(.3)
        test(win, count+1, bugs)


if __name__ == '__main__':
    main()
