# visualizer.py
# An ant visualizer
import ants
import tkinter

class Visualizer:
    """
    Visualizer for the ant simulation
    """

    def __init__(self, sim):
        self.sim = sim

        # create the window and the canvas
        width = sim.width * 4
        height = sim.height * 4
        self.win = tkinter.Tk()
        self.win.geometry(str(width) + "x" + str(height))
        can = tkinter.Canvas(self.win, width=width, height=height, bg="black")
        can.pack()
        self.can = can

        #create the pixels
        self.pixels = []
        for i in range(sim.height):
            self.pixels.append([])
            for j in range(sim.width):
                x = j * 4
                y = i * 4
                r = can.create_rectangle(x, y, x+4, y+4)
                self.pixels[i].append(r)

    def colorCell(self, x, y, color):
        self.can.itemconfig(self.pixels[y][x], fill=color, outline=color)
    
    def update(self):
        # draw the grid
        for i in range(self.sim.height):
            for j in range(self.sim.width):
                p = self.sim.patches.get(j, i)
                if p.nestScent[0] >= 1:
                    self.colorCell(j, i, "saddle brown")
                elif p.nestScent[1] >= 1:
                    self.colorCell(j, i, "sandy brown")
                elif p.danger:
                    self.colorCell(j, i, "purple")
                elif p.food > 0:
                    self.colorCell(j, i, "green")
                else:
                    if p.chemical[1] >= 1:
                        self.colorCell(j, i, "light pink")
                    elif p.chemical[0] >= 1:
                        self.colorCell(j, i, "light green")
                    else:
                        self.colorCell(j, i, "black")
        
        #draw the ants
        for a in self.sim.ants:
            x = int(round(a.x))
            y = int(round(a.y))
            if y<0 or x < 0 or y >= self.sim.height or x >= self.sim.width: continue
            if a.alive:
                if a.nestid == 0:
                    self.colorCell(x, y, "yellow")
                else:
                    self.colorCell(x, y, "red")
            else:
                self.colorCell(x, y, "dark gray")
        
        self.win.update()