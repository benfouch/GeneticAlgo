import tkinter
from tkinter import *
import time

def main():
    win=tkinter.Tk()

    canvas = Canvas(win, width=500, height=500)

    pos = (100, 100)
    radius = 5

    oval=canvas.create_oval(pos[0]-radius, pos[1]-radius, pos[0]+radius, pos[1]+radius, fill='blue')
    canvas.pack()

    # sleep(5)

    # print("test")

    # win.after(10000, test(win, 0, canvas, pos, radius, oval))

    win.after(5000, test(win, 0, canvas, oval))

    win.mainloop()


def test(win, count, canvas, oval):
    i = count
    #print("test")
    canvas.move(oval, 10, 10)
    win.update()

    if i < 20:
        time.sleep(.5)
        test(win, count+1, canvas, oval)


if __name__ == '__main__':
    main()
