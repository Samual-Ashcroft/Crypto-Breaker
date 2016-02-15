
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
solve = [[],[],[]]
grid_solve = []
labels = [[],[],0,0]
updated = False
finished = -1

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
    updated = True

def Flip(x,y):
    global tile_grid, solutions
    print x,y, tile_grid[y][x]#.cget("bg")
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
    print solutions
        

Create_Labels()

def View_Solution(k = 0):
    global solutions, tile_grid, updated
    if not updated: Create_Labels()
    for i in xrange(len(solutions[1][k])):
        for j in xrange(len(solutions[1][k][i])):
            if solutions[1][k][i][j] == 1:
                tile_grid[i][j].configure(bg = 'black')
            else:
                tile_grid[i][j].configure(bg = 'white')
    Main.update()

def Populate_Solves():
    global x_elements, y_elements, grid_solve, solve
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
        solve[2].append([])
        for i in xrange(len(y_elements[2][y])):
            if y_elements[2][y][i] != -1:
                for j in xrange(y_elements[2][y][i]):
                    solve[1][y].append(1)
                    solve[2][y].append(1)
            solve[1][y].append(0)
            solve[2][y].append(0)
        if len(solve[1][y]) < x_elements[0]:
            for k in xrange(x_elements[0]-len(solve[1][y])):
                solve[1][y].append(0)
                solve[2][y].append(0)
    #solve.append(solve[1])# = [solve[0],solve[1],solve[1]]
    print solve, 'joed'

def Check_Solution():
    global solve
    state = False; column = -1
    print 'start'
    for x in xrange(len(solve[0])):
        print 'first for', x, solve[0][x]
        for y in xrange(len(solve[0][x])):
            print 'second for', x,y,solve[0][x][y]
            solve[2] = solve[1]
            while not state:
                print 'while', solve[2]
                for x1 in xrange(x+1):
                    print 'while for', x, y, x1, x+1, solve[0][x1][y], solve[2][y], solve[2][y][x1]
                    if solve[0][x1][y] != solve[2][y][x1]:
                        print 'yolo', x, y, solve[0][x1][y], solve[2][y][x1]
                        print 'start', 2, y, solve[2][y], state
                        print 'start', solve[1][y], solve[2][y]
                        state = Line_Shift(2,y)
                        print 'finish', solve[2][y], state
                        print 'finish', solve[1][y], solve[2][y]
                        break
                else:
                    print 'yoda'
                    column = -1
                    solve[1] = solve[2]
                    break
                print 'uber'
                column = x
            if column != -1:
                break
        if column != -1:
            break
    print 'end', column
    return column
                
def Line_Shift(index, RowCol):
    global solve
    state = False; Line = solve[index][RowCol]; Line1 = []; Line2 = []
    print Line
    if Line[len(Line)-1] == 0:
        Line1 = Line
        Line2 = []
        print '1st'
    else:
        print '2nd'
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
        print 'pre return 1', index, solve[1][RowCol], solve[2][RowCol], solve[index][RowCol]
        solve[1][RowCol] = solve[1][RowCol]
        solve[2][RowCol] = solve[2][RowCol]
        solve[index][RowCol] = Line1
        print 'pre return 1', index, solve[1][RowCol], solve[2][RowCol], solve[index][RowCol]
        solve = [solve[0],solve[1],solve[2]]
        del solve[index][RowCol]
        solve[index].insert(RowCol, Line1)
    else:
        print Line2, Line1, solve[index], solve[1][RowCol], solve[2][RowCol]
        solve[index][RowCol] = Line2 + Line1
        print 'Line 2nd', Line, Line1, Line2
        state = True
    return state

def Populate_Grid_Solve(state):
    global solve, grid_solve
    if state:
        grid_solve = solve[1]
    for i in xrange(len(grid_solve)):
        for j in xrange(len(grid_solve[i])):
            grid_solve[i][j] = solve[0][j][i]

def Brute_Solve_1():
    global solutions, solve
    Populate_Solves()
    print solve
    #Populate_Grid_Solve(True)
    print solve
    solutions = [solutions[0],[solutions[1][0]]]
    #while True:
    print Check_Solution()
    #Line = Line_Shift([False, solve[0][1]])
    #print Line
    #print Check_Solution()


View_Solution(0)

go_solve = Button(Main, text="OK", command=Brute_Solve_1)
go_solve.grid(row = 0, column = 0)
view_solve = Button(Main, text="NK", command=View_Solution)
view_solve.grid(row = 1, column = 0)
                                               
Main.mainloop() #The final Thread
