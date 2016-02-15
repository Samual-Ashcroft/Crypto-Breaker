
# Import the Tkinter classes and functions
from Tkinter import *#Tk, Label, Button
from time import sleep
# Importing math
#from math import *

##### DEVELOP YOUR SOLUTION HERE #####
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
y_elements = [7,3,[[2,2],[2,2],[-1],[-1],[1,1],[1,1],[3]]]    
'''
The tile grid is merely a 2d array, Y
encases X, it contains the tile objects
'''
tile_grid = []
solutions = [[[1,0,0,0,1],[0,1,0,1,0],[0,0,1,0,0],[0,1,0,1,0],[1,0,0,0,1]],[]]
'''
The x_solve holds proposed solutions,
first we lay out the most basic pattern of x,
then we iterate, cycling the right most line first
all the way through, if no solve then we iterate the next one
once and reiterate the right most etc until we find a solve.
Ideally we iterate past the solve to see if there are multiple
solves and store them, but for now we go till solve.
'''
x_solve = x_elements[2]
grid_solve = []
labels = [[],[],0,0]
updated = False
finished = -1

#Creating the Labels
def Create_Labels():
    global x_elements, y_elements, tile_grid, labels, updated
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
        for i in xrange(x_elements[0]):
            tile_grid.append([0])
            for j in xrange(y_elements[0]):
                if j != 0: tile_grid[i].append(0)
                tile_grid[i][j] = Label(Main, bg = 'white', bd = 5, padx=9, pady=3)
                tile_grid[i][j].grid(row = i+labels[2]+1, column = j+labels[3]+1)
    updated = True
Create_Labels()

def View_Solution(k = 0):
    global solutions, tile_grid, updated
    if not updated: Create_Labels()
    for i in xrange(len(solutions[k])):
        for j in xrange(len(solutions[k][i])):
            if solutions[k][i][j] == 1:
                tile_grid[i][j].configure(bg = 'black')
            else:
                tile_grid[i][j].configure(bg = 'white')
    Main.update()

def Populate_Grid_Solve():
    global x_solve, grid_solve
    for i in xrange(len(grid_solve)):
        for j in xrange(len(grid_solve[i])):
            grid_solve[i][j] = 0
    for i in xrange(len(x_solve)):
        if x_solve[i][0][0] != -1:
            for j in xrange(len(x_solve[i])):
                for k in xrange(x_solve[i][j][0]):
                    grid_solve[x_solve[i][j][1]+k][i] = 1

def Check_Solution():
    global grid_solve, y_elements
    concaten = 0
    y_solve = []
    for i in xrange(len(grid_solve)):
        y_solve.append([-1])
        for j in xrange(len(grid_solve[i])):
            if grid_solve[i][j] == 1:
                concaten += 1
            else:
                if (y_solve[i][0] == -1 and concaten != 0):
                    y_solve[i][0] = concaten
                elif concaten != 0:
                    y_solve[i].append(concaten)
                concaten = 0
        else:
            if (y_solve[i][0] == -1 and concaten != 0):
                y_solve[i][0] = concaten
            elif concaten != 0:
                y_solve[i].append(concaten)
            concaten = 0            
        concaten = 0
        if y_solve[i] != y_elements[2][i]:
            break
    return y_solve == y_elements[2]

def Step_Solver(y_length):
    global finished, x_solve
    break_it = False
    for i in xrange(len(x_solve)-1,-1,-1):
        if x_solve[i][0][0] != -1:
            for j in xrange(len(x_solve[i])-1,-1,-1):
                if (x_solve[i][j][0]+x_solve[i][j][1] < y_length):
                    if (j == len(x_solve[i])-1):
                        x_solve[i][j][1] += 1
                        break_it = True
                        break
                    elif(x_solve[i][j][0]+x_solve[i][j][1] < x_solve[i][j+1][1]-1):
                        x_solve[i][j][1] += 1
                        for m in xrange(j+1, len(x_solve[i])):
                            x_solve[i][m][1] = x_solve[i][m-1][0]+x_solve[i][m-1][1]+1
                        break_it = True
                        break
            else:
                if ( i < len(x_solve)):
                    #k is counting the min pos an element can be put at on this column stack
                    k = 0
                    #iterating from 0 to the max columns, default is 0 to 4
                    for m in xrange(i, len(x_solve)):
                        #asking if there are no elements here
                        if x_solve[m][0][0] != -1:
                            #since this will be the first element in a column, we are incrementing k by the run number+1
                            k += x_solve[m][0][0]+1
                            #reinitializing the element as a 2 point array, run number and position, first pos will of course be zero
                            x_solve[m][0][1] = 0
                            #iterating from zero, the max number of run_numbers there are
                            for n in xrange(len(x_solve[m])):
                                #this if statement causes it to skip the first element which was already done outside the for loop
                                if n != 0:
                                    #reinit the element and give it's place holder the value of k
                                    x_solve[m][n][1] = k
                                    #incrementing k again to reflect that extra run_number+1
                                    k += x_solve[m][n][0]+1
                        else:
                            #if there were no elements, we format it but indicate no elements
                            x_solve[i][0][1] = -1
                        #reinitializing k before the next column        
                        k = 0
            if break_it:
                break
    else:
        finished = 1
        
def Brute_Solve_1():
    global solutions, x_elements, y_elements, finished, x_solve, grid_solve
    if finished == -1:
        x_solve = x_elements[2]
        grid_solve = []
        #initialize the grid_solve
        for i in xrange(x_elements[0]):
            grid_solve.append([0])
            for j in xrange(y_elements[0]):
                if j != 0: grid_solve[i].append(0)
        #initialize the x_solve
        #k is counting the min pos an element can be put at on this column stack
        k = 0
        #iterating from 0 to the max columns, default is 0 to 4
        for i in xrange(len(x_solve)):
            #asking if there are no elements here
            if x_solve[i][0] != -1:
                j = 0;
                while j < len(x_solve[i]):
                    #iterating across the length of the x_element 'item' to determine appropriateness
                    for m in xrange(x_solve[i][j]):
                        if(y_elements[2][k+m][0] == -1):
                            k +=1
                            break 
                    else:
                        #reinit the element and give it's place holder the value of k
                        x_solve[i][j] = [x_solve[i][j], k]
                        #registering the additions to the grid_solve
                        for m in xrange(x_solve[i][j][0]):
                            grid_solve[i][k+m] = 1
                        #incrementing k again to reflect that extra run_number+1
                        k += x_solve[i][j][0]+1
                        j += 1
            else:
                #if there were no elements, we format it but indicate no elements
                x_solve[i][0] = [x_solve[i][0], -1]
            #reinitializing k before the next column        
            k = 0
        print grid_solve
        solutions[1] = grid_solve
        View_Solution(1)
        finished = 0
        if not Check_Solution():
            Main.after(0, Brute_Solve_1)
        else:
            solutions[0] = grid_solve
            View_Solution(0)
    elif finished == 0: 
        Step_Solver(y_elements[0])
        Populate_Grid_Solve()
        solutions[1] = grid_solve
        View_Solution(1)
        if not Check_Solution():
            Main.after(0, Brute_Solve_1)
        else:
            solutions[0] = grid_solve
            View_Solution(0)
    else:
        View_Solution(0)
        
View_Solution(0)

b = Button(Main, text="OK", command=Brute_Solve_1)
b.grid(row = 0, column = 0)
c = Button(Main, text="NK", command=View_Solution)
c.grid(row = 1, column = 0)
                                               
Main.mainloop() #The final Thread

