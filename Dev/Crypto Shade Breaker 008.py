
# Import the Tkinter classes and functions
from Tkinter import *#Tk, Label, Button
from time import sleep
# Importing math
#from math import *

#Building the main window
'''The namespace 'Calculator' is being assigned to an object of type
TK from the tkinter library, that object is essentially a form or
window and we will create many more objects to populate it'''
Main = Tk()
'''Here we change a property of the object 'Calculator' of type TK,
that property is the title which if looked up in the documentation
contains what is written at the top of the window'''
Main.title('Puzzle Solver')
'''Here we change the initial size of the calculator window'''
Main.minsize(width = 200,height=200)

#Setting the setup variables
'''
x elements would be; number of rows,
number of discriptive elements for each row,
the arrays of those descriptives,
ideally this would be an initializer that
could be dynamically changed
'''
x_elements = [7,3,[[1],[2,1],[2,1],[1],[2,1],[2,1],[1]]]
y_elements = [6,3,[[2,2],[2,2],[-1],[1,1],[1,1],[3]]]    
'''
The tile grid is merely a 2d array, Y
encases X, it contains the tile objects
'''
tile_grid = []
solutions = [0,[[[0,1,0,1,0],[0,1,0,1,0],[0,0,0,0,0],[1,0,0,0,1],[0,1,1,1,0]]]]
'''
The x_solve holds proposed solutions,
first we lay out the most basic pattern of x,
then we iterate, cycling the right most line first
all the way through, if no solve then we iterate the next one
once and reiterate the right most etc until we find a solve.
Ideally we iterate past the solve to see if there are multiple
solves and store them, but for now we go till solve.
'''
solve = [[],[]]
grid_solve = []
labels = [[],[],0,0]
updated = False
finished = -1
Step = -1; i = 0; state = False

#Settings stuff
x_elem_label = Label(Main, font='bold', text = 'No. X Elements')
y_elem_label = Label(Main, font='bold', text = 'No. Y Elements')
elem_updt_label = Label(Main, font='bold', text = 'X/Y, index 0->n')
spacer_label = Label(Main, font='bold', text = '', bd = 5, padx=9, pady=3)

#Creating the Labels
def Create_Labels():
    global x_elements, y_elements, tile_grid, labels, updated, solutions
    labels = [[],[],0,0]; tile_grid = []
    if isinstance(x_elements[2], list):
        for i in xrange(len(x_elements[2])):
            if isinstance(x_elements[2][i], list):
                for j in xrange(len(x_elements[2][i])):
                    if j > labels[2]:
                        labels[2] = j
        if isinstance(y_elements[2], list):
            for i in xrange(len(y_elements[2])):
                if isinstance(y_elements[2][i], list):
                    for j in xrange(len(y_elements[2][i])):
                        if j > labels[3]:
                            labels[3] = j
            k = 0
            for i in xrange(len(x_elements[2])):
                if isinstance(x_elements[2][i], list):
                    for j in xrange(len(x_elements[2][i])):
                        labels[0].append(0)
                        labels[0][k] = StringVar()
                        labels[0][k].set(x_elements[2][i][len(x_elements[2][i])-j-1])
                        labels[0].append(Label(Main, font='bold', textvariable=labels[0][k]))
                        labels[0][k+1].grid(row = labels[2]-j, column = labels[3]+1+i)
                        k += 2
            for i in xrange(len(y_elements[2])):
                if isinstance(y_elements[2][i], list):
                    for j in xrange(len(y_elements[2][i])):
                        labels[0].append(0)
                        labels[0][k] = StringVar()
                        labels[0][k].set(y_elements[2][i][len(y_elements[2][i])-j-1])
                        labels[0].append(Label(Main, font='bold', textvariable=labels[0][k]))
                        labels[0][k+1].grid(column = labels[3]-j, row = labels[2]+1+i)
                        k += 2
        #Creating the tiles
        for i in xrange(y_elements[0]):
            tile_grid.append([0])
            if i >= len(solutions[1][0]):
                solutions[1][0].append([0])
            for j in xrange(x_elements[0]):
                if j != 0: tile_grid[i].append(0)
                tile_grid[i][j] = Label(Main, bg = 'white', bd = 5, padx=9, pady=3)
                tile_grid[i][j].grid(row = i+labels[2]+1, column = j+labels[3]+1)
                tile_grid[i][j].bind("<Button-1>",lambda e,y=i,x=j:Flip(x,y))
                if j >= len(solutions[1][0][i]):
                    solutions[1][0][i].append(0)
    x_elem_label.grid(row = 0, column = labels[3] + x_elements[0]+1)
    y_elem_label.grid(row = 2, column = labels[3] + x_elements[0]+1)
    spacer_label.grid(row = 0, column = labels[3] + x_elements[0]+2)
    elem_updt_label.grid(row = 0, column = labels[3] + x_elements[0]+3)
    updated = True

def Flip(x,y):
    global tile_grid, solutions
    if tile_grid[y][x].cget("bg") == 'white':
        tile_grid[y][x].configure(bg = 'black')
        solutions[1][solutions[0]][y][x] = 1
    else:
        tile_grid[y][x].configure(bg = 'white')
        solutions[1][solutions[0]][y][x] = 0
    if solutions[0]+1 < len(solutions[1]):
        solutions[0] += 1
    else:
        solutions[0] = 0

def View_Solution(k = 0):
    global solutions, tile_grid, updated
    if not updated: Create_Labels()
    if k == 0:
        if solutions[0] >= (len(solutions[1])-1):
            solutions[0] = 0
        else:
            solutions[0] += 1
            k = solutions[0]
    for i in xrange(len(solutions[1][k])):
        for j in xrange(len(solutions[1][k][i])):
            if solutions[1][k][i][j] == 1:
                tile_grid[i][j].configure(bg = 'black')
            else:
                tile_grid[i][j].configure(bg = 'white')
    Main.update()

def Populate_Solves():
    global x_elements, y_elements, grid_solve, solve
    solve = [[],[]]
    for x in xrange(x_elements[0]):
        solve[0].append([])
        for i in xrange(len(x_elements[2][x])):
            if x_elements[2][x][i] != -1:
                for j in xrange(x_elements[2][x][i]):
                    solve[0][x].append(1)
            solve[0][x].append(0)
        if len(solve[0][x]) < y_elements[0]:
            for k in xrange(y_elements[0]-len(solve[0][x])):
                solve[0][x].append(0)
    for y in xrange(y_elements[0]):
        solve[1].append([])
        for i in xrange(len(y_elements[2][y])):
            if y_elements[2][y][i] != -1:
                for j in xrange(y_elements[2][y][i]):
                    solve[1][y].append(1)
            solve[1][y].append(0)
        if len(solve[1][y]) < x_elements[0]:
            for k in xrange(x_elements[0]-len(solve[1][y])):
                solve[1][y].append(0)
    
def Check_Solution():
    global solve
    state = False; column = -1; column2 = -1
    for x in xrange(len(solve[0])):
        for y in xrange(len(solve[0][x])):
            if solutions[1][0][y][x] == 1 and solve[0][x][y] != 1:
                column = x
                break
            state = False
            while not state:
                for x1 in xrange(x+1):
                    if solve[0][x1][y] != solve[1][y][x1]:
                        state = Line_Shift(1,y)
                        break
                else:
                    column = -1
                    break
                column = x
            goog = False
            while not goog:
                goog = Line_Shift(1,y)
            if column != -1:
                break
        if column != -1:
            break
    return column
                
def Line_Shift(index, RowCol):
    global solve
    Line = solve[index][RowCol]; Line1 = []; Line2 = []
    if Line[len(Line)-1] == 0:
        Line1 = Line
        Line2 = []
    else:
        for i in xrange(len(Line)-2,-1,-1):
            if i != 0:
                if Line[i] == 0 and Line[i-1] == 0:
                    Line1 = Line[0:i+1]
                    Line2 = Line[i+1:len(Line)]
                    break
    if Line1.count(1) != 0:
        Line1 = Line1[0:len(Line1)-1]
        for i in xrange(len(Line1)-1,-1,-1):
            if (i == 0 or (i != 0 and Line1[i] == 1 and Line1[i-1] == 0)):
                Line1.insert(i, 0)
                break
        if Line[len(Line)-1] != 0:
            for j in xrange(len(Line1)-1,-1,-1):
                if (j == 0 or (j != 0 and Line1[j] == 0 and Line1[j-1] == 1)):
                    break
            for i in xrange(len(Line2)):
                Line1.insert(j+1, Line2[i])
        solve[index][RowCol] = Line1
        return False
    else:
        solve[index][RowCol] = Line2 + Line1
        return True

def Step_Solve():
    global Step
    if Step == -1:
        Step = 0
    else:
        Step = -1

Populate_Solves()
solutions = [solutions[0],[solutions[1][0]]]

def Brute_Solve_1():
    global solutions, solve, Step, i, state
    solutions[0] = len(solutions[1])-1
    if Step == -1 or Step == 0 or i == -1:        
        i = len(solve[0][0]); state = False
        solutions[1].append([])
        solutions[0] += 1
        for m in xrange(len(solve[0][0])):
            solutions[1][solutions[0]].append([])
            for n in xrange(len(solve[0])):
                solutions[1][solutions[0]][m].append(0)
        if Step == 0:
            Step = 1
    monk = True
    while (Step == -1 and i != -1) or monk:
        if state:
            state = False
            for j in xrange(len(solve[0])-1,i,-1):
                goog = False
                while not goog:
                    goog = Line_Shift(0,j)
            if i != 0:
                state = Line_Shift(0, i-1)
                if state:
                    i -= 1
        else:
            state = Line_Shift(0, i)
        if not state:
            i = Check_Solution()
        for m in xrange(len(solve[0][0])):
            for n in xrange(len(solve[0])):
                solutions[1][solutions[0]][m][n] = solve[0][n][m]
        View_Solution(solutions[0])
        monk = False

Create_Labels()
View_Solution(0)

go_solve = Button(Main, text="solve", command=Brute_Solve_1)
go_solve.grid(row = 0, column = 0)
view_solve = Button(Main, text="view", command=View_Solution)
view_solve.grid(row = 1, column = 0)
Stepper = Button(Main, text="stp", command=Step_Solve)
Stepper.grid(row = 0, column = 1)
Main.mainloop() #The final Thread
