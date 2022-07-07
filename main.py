import tkinter 
from tkinter import *
from tkinter.font import BOLD, Font
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

    def get_speed(self):
        return self.speed

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
    generations = 200

    canvas = Canvas(win, width=1600, height=900)

    font = Font(win, size=35, weight=BOLD)

    ret_val = new_gen(canvas, win, True)

    canvas.pack()

    for i in range(generations):
        label = Label(win, text="Gen "+str(i+1)+"/" + str(generations), font=font)
        label.place(x=1, y=1)
        test(win, 0, ret_val[0], ret_val[1], canvas)
        best_bugs = get_best_bugs(ret_val[0])
        hide_all(ret_val[0], ret_val[1], canvas, win)
        ret_val = new_gen(canvas, win, False, best_bugs=best_bugs)

    hide_all(ret_val[0], ret_val[1], canvas, win)

def get_best_bugs(bugs):
    best = []
    scores = []
    for bug in bugs:
        scores += [bug.get_points()]

    scores.sort(reverse=True)
    scores = scores[:int(len(bugs)*.20)]
    print(scores)

    for bug in bugs:
        if bug.get_points() in scores:
            best += [bug]

    return best

def hide_all(bugs, foods, canvas, window):
    for bug in bugs:
        bug.hide()

    for food in foods:
        food.hide()

    window.update()

def new_gen(canvas, win, first_round, best_bugs=None):
    radius = 5
    mutation_rate = 1.5
    bugs = []
    food = []

    new_food(700, food, canvas)

    if first_round:
        for i in range(60):
            pos = (random.random()*1600, random.random()*900)
            speed = random.random()*1
            oval=canvas.create_oval(pos[0]-radius, pos[1]-radius, pos[0]+radius, pos[1]+radius, fill='blue')
            bugs += [Bug(pos, speed, oval, canvas)]
        canvas.pack()
    else:
        speeds = []
        for bug in best_bugs:
            pos = (random.random()*1600, random.random()*900)
            speed = bug.get_speed()
            speeds += [speed]
            oval=canvas.create_oval(pos[0]-radius, pos[1]-radius, pos[0]+radius, pos[1]+radius, fill='blue')
            bugs += [Bug(pos, speed, oval, canvas)]

        av_speed = sum(speeds)/len(speeds)
        font = Font(win, size=15)
        label = Label(win, text="Ave top 20% speed: {:.2f}".format(av_speed), font=font)
        label.place(x=1, y=50)

        for i in range(60-(len(bugs))):
            pos = (random.random()*1600, random.random()*900)
            speed =  av_speed + random.random()*mutation_rate - random.random()*mutation_rate
            oval=canvas.create_oval(pos[0]-radius, pos[1]-radius, pos[0]+radius, pos[1]+radius, fill='blue')
            bugs += [Bug(pos, speed, oval, canvas)]

        canvas.pack()
    return (bugs, food)

def new_food(food_num, food_list, canvas):
    for i in range(food_num):
        radius = 5
        pos = (random.random()*1600, random.random()*900)
        oval=canvas.create_oval(pos[0]-radius, pos[1]-radius, pos[0]+radius, pos[1]+radius, fill='green')
        food_list += [Food(10, pos, oval, canvas)]

    canvas.pack()


def test(win, count, bugs, food_list, canvas):
    for b in bugs:
        ret_val = b.move(food_list)
        if ret_val != None:
            food_list.remove(ret_val)
            ret_val.hide()

    win.update()


    if count < 400:
        new_food(1, food_list, canvas)
        # time.sleep(.01)
        test(win, count+1, bugs, food_list, canvas)


if __name__ == '__main__':
    main()
