
from Tkinter import *
import ttk
from time import sleep
from Libraries import LoaderLibrary #Imported from sub directory with blank __init__.py in it
#import font

#Building the main window
'''The namespace 'Main' is being assigned to an object of type
TK from the tkinter library, that object is essentially a form or
window and we will create many more objects to populate it'''
Main = Tk()
'''Here we change a property of the object 'Main' of type TK,
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
x_elements = [7,[[1],[2,1],[2,1],[1],[2,1],[2,1],[1]]]
y_elements = [6,[[2,2],[2,2],[-1],[1,1],[1,1],[3]]]    
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
font_size = 6
solve_check = []
view_toggle_var = True
old_column = 0

#Settings stuff
x_elem_label = Label(Main, font = ("Times", font_size, "bold"), text = 'No. X Elements')
y_elem_label = Label(Main, font = ("Times", font_size, "bold"), text = 'No. Y Elements')
elem_updt_label = Label(Main, font = ("Times", font_size, "bold"), text = 'X/Y, index 0->n')
elem_num_updt_label = Label(Main, font = ("Times", font_size, "bold"), text = 'Run length to add')
spacer_label = Label(Main, font = ("Times", font_size, "bold"), text = '', bd = 5, padx=9, pady=3)
x_plus = Button(Main, text="+", font = ("Times", font_size, "bold"))
x_neg = Button(Main, text="-", font = ("Times", font_size, "bold"))
y_plus = Button(Main, text="+", font = ("Times", font_size, "bold"))
y_neg = Button(Main, text="-", font = ("Times", font_size, "bold"))
xy_select_var = StringVar()
xy_select = ttk.Combobox(Main, font = ("Times", font_size, "bold"), width = 10, textvariable = xy_select_var, state = 'readonly')
xy_select['values'] = ('X axis', 'Y axis')
xy_index_select_var = StringVar()
xy_index_select = ttk.Combobox(Main, font = ("Times", font_size, "bold"), width = 10, textvariable = xy_index_select_var, state = 'readonly')
xy_num_select_var = StringVar()
xy_num_select = ttk.Combobox(Main, font = ("Times", font_size, "bold"), textvariable = xy_num_select_var, state = 'readonly')
go_solve = Button(Main, font = ("Times", font_size, "bold"), text="solve")
view_solve = Button(Main, font = ("Times", font_size, "bold"), text="view")
view_toggle = Button(Main, font = ("Times", font_size, "bold"), text="I/O")
Stepper = Button(Main, font = ("Times", font_size, "bold"), text="stp")
xy_add = Button(Main, font = ("Times", font_size, "bold"), text="Add")
xy_del = Button(Main, font = ("Times", font_size, "bold"), text="Delete")
file_selector_var = StringVar()
file_selector = ttk.Combobox(Main, font = ("Times", font_size, "bold"), width = 40, textvariable = file_selector_var, state = 'readonly')
new = Button(Main, font = ("Times", font_size, "bold"), text="New")
save = Button(Main, font = ("Times", font_size, "bold"), text="Save")
load = Button(Main, font = ("Times", font_size, "bold"), text="Load")

#The File Read/Write Libraries
def Refresh_Save_List(k = 0):
    global x_elements, y_elements, solutions, file_selector_var
    file_name = "Data"
    file_data = []
    file_data = LoaderLibrary.Read_file(file_name)
    temp1 = ()
    '''
    for y in xrange(len(file_data)):
        if y == 0:
            temp1 = (file_data[0][0],)
        else:
            temp1 = temp1 + (file_data[0][y],)
            '''
    if k == 0 and file_data != []:
        temp1 = ()
        for y in xrange(len(file_data[0])):
            if y == 0:
                temp1 = (file_data[0][0],)
            else:
                temp1 = temp1 + (file_data[0][y],)
        file_selector['values'] = temp1
    elif k == 1:
        temp1 = str(len(file_data[0]))
        if len(temp1) < 3:
            for j in xrange(3-len(temp1)):
                temp1 = '0' + temp1
        temp1 = 'Save' + temp1
        file_data[0].append(temp1)
        LoaderLibrary.Write_file(file_data, file_name)
        LoaderLibrary.Write_file([x_elements, y_elements, solutions], temp1)
    elif k == 2:
        LoaderLibrary.Write_file([x_elements, y_elements, solutions], file_selector_var.get())
    elif k == 3:
        temp2 = LoaderLibrary.Read_file(file_selector_var.get())
        x_elements = temp2[0]
        y_elements = temp2[1]
        solutions = temp2[2]
        reinitialize(5)
        

#Creating the Labels
def Create_Labels():
    global x_elements, y_elements, tile_grid, labels, updated, solutions
    labels = [[],[],0,0]; tile_grid = []
    if isinstance(x_elements[1], list):
        for i in xrange(len(x_elements[1])):
            if isinstance(x_elements[1][i], list):
                for j in xrange(len(x_elements[1][i])):
                    if j > labels[2]:
                        labels[2] = j
        if isinstance(y_elements[1], list):
            for i in xrange(len(y_elements[1])):
                if isinstance(y_elements[1][i], list):
                    for j in xrange(len(y_elements[1][i])):
                        if j > labels[3]:
                            labels[3] = j
            k = 0
            for i in xrange(len(x_elements[1])):
                if isinstance(x_elements[1][i], list):
                    for j in xrange(len(x_elements[1][i])):
                        labels[0].append(0)
                        labels[0][k] = StringVar()
                        labels[0][k].set(x_elements[1][i][len(x_elements[1][i])-j-1])
                        labels[0].append(Label(Main, font = ("Times", font_size, "bold"), textvariable=labels[0][k]))
                        labels[0][k+1].grid(row = labels[2]-j, column = labels[3]+1+i)
                        k += 2
            for i in xrange(len(y_elements[1])):
                if isinstance(y_elements[1][i], list):
                    for j in xrange(len(y_elements[1][i])):
                        labels[0].append(0)
                        labels[0][k] = StringVar()
                        labels[0][k].set(y_elements[1][i][len(y_elements[1][i])-j-1])
                        labels[0].append(Label(Main, font = ("Times", font_size, "bold"), textvariable=labels[0][k]))
                        labels[0][k+1].grid(column = labels[3]-j, row = labels[2]+1+i)
                        k += 2
        #Creating the tiles
        for i in xrange(y_elements[0]):
            tile_grid.append([0])
            if i >= len(solutions[1][0]):
                solutions[1][0].append([0])
            for j in xrange(x_elements[0]):
                if j != 0: tile_grid[i].append(0)
                tile_grid[i][j] = Label(Main, relief = SUNKEN, font = ("Times", font_size, "bold"), bg = 'white', bd = 5, padx=5, pady=0)
                tile_grid[i][j].grid(row = i+labels[2]+1, column = j+labels[3]+1)
                tile_grid[i][j].bind("<Button-1>",lambda e,y=i,x=j:Flip(x,y))
                if j >= len(solutions[1][0][i]):
                    solutions[1][0][i].append(0)
    x_elem_label.grid(row = 0, column = labels[3] + x_elements[0]+1, columnspan = 2)
    y_elem_label.grid(row = 2, column = labels[3] + x_elements[0]+1, columnspan = 2)
    spacer_label.grid(row = 0, column = labels[3] + x_elements[0]+3)
    elem_updt_label.grid(row = 0, column = labels[3] + x_elements[0]+4, columnspan = 2)
    x_plus.grid(row = 1, column = labels[3] + x_elements[0]+2)
    x_neg.grid(row = 1, column = labels[3] + x_elements[0]+1)
    y_plus.grid(row = 3, column = labels[3] + x_elements[0]+2)
    y_neg.grid(row = 3, column = labels[3] + x_elements[0]+1)
    xy_select.grid(row = 1, column = labels[3] + x_elements[0]+4, columnspan = 1)
    xy_index_select.grid(row = 1, column = labels[3] + x_elements[0]+5, columnspan = 1)
    elem_num_updt_label.grid(row = 2, column = labels[3] + x_elements[0]+4, columnspan = 2)
    xy_num_select.grid(row = 3, column = labels[3] + x_elements[0]+4, columnspan = 2)
    go_solve.grid(row = 4, column = labels[3] + x_elements[0]+1)
    view_solve.grid(row = 5, column = labels[3] + x_elements[0]+1)
    view_toggle.grid(row = 5, column = labels[3] + x_elements[0]+2)
    Stepper.grid(row = 6, column = labels[3] + x_elements[0]+1)
    xy_add.grid(row = 4, column = labels[3] + x_elements[0]+4)
    xy_del.grid(row = 4, column = labels[3] + x_elements[0]+5)
    file_selector.grid(row = 5, column = labels[3] + x_elements[0]+3, columnspan = 3)
    new.grid(row = 6, column = labels[3] + x_elements[0]+3)
    save.grid(row = 6, column = labels[3] + x_elements[0]+4)
    load.grid(row = 6, column = labels[3] + x_elements[0]+5)
    updated = True

def Flip(x,y):
    global tile_grid, solutions
    View_Solution(-1)
    if tile_grid[y][x].cget("bg") == 'white':
        tile_grid[y][x].configure(bg = 'black')
        solutions[1][0][y][x] = 1
    else:
        tile_grid[y][x].configure(bg = 'white')
        solutions[1][0][y][x] = 0

def View_Solution(k = 0, column = -1):
    global solutions, tile_grid, updated
    if not updated: Create_Labels()
    if k == 0:
        if solutions[0] >= (len(solutions[1])-1):
            solutions[0] = 0
        else:
            solutions[0] += 1
            k = solutions[0]
    elif k == -1:
        k = 0
    if column == -1:
        for i in xrange(len(solutions[1][k])):
            for j in xrange(len(solutions[1][k][i])):
                if solutions[1][k][i][j] == 1:
                    tile_grid[i][j].configure(bg = 'black')
                else:
                    tile_grid[i][j].configure(bg = 'white')
    else:
        for i in xrange(len(solutions[1][k])):
            if solutions[1][k][i][column] == 1:
                tile_grid[i][column].configure(bg = 'black')
            else:
                tile_grid[i][column].configure(bg = 'white')
    Main.update()

def Populate_Solves():
    global x_elements, y_elements, grid_solve, solve
    solve = [[],[]]
    for x in xrange(x_elements[0]):
        solve[0].append([])
        for i in xrange(len(x_elements[1][x])):
            if x_elements[1][x][i] != -1:
                for j in xrange(x_elements[1][x][i]):
                    solve[0][x].append(1)
            if len(solve[0][x]) < y_elements[0]:
                solve[0][x].append(0)
        if len(solve[0][x]) < y_elements[0]:
            for k in xrange(y_elements[0]-len(solve[0][x])):
                solve[0][x].append(0)
    for y in xrange(y_elements[0]):
        solve[1].append([])
        for i in xrange(len(y_elements[1][y])):
            if y_elements[1][y][i] != -1:
                for j in xrange(y_elements[1][y][i]):
                    solve[1][y].append(1)
            if len(solve[1][y]) < x_elements[0]:
                solve[1][y].append(0)
        if len(solve[1][y]) < x_elements[0]:
            for k in xrange(x_elements[0]-len(solve[1][y])):
                solve[1][y].append(0)
    
def Check_Solution():
    global solve, solve_check
    state = False; column = -1; column2 = -1
    nope = False
    for x in xrange(len(solve[0])):
        for y in xrange(len(solve[0][x])):
            if solutions[1][0][y][x] == 1 and solve[0][x][y] != 1:
                column = x
                nope = True
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
            Line_Reset(1,y)
            if column != -1:
                break
        if column != -1:
            break
    if nope:
        solve_check = []
    else:
        solve_check = [column, y]
    return column
                
def Line_Shift(index, RowCol):
    global solve
    Line = solve[index][RowCol]; Line1 = []; Line2 = []
    if Line[-1] == 0:
        Line1 = Line
        Line2 = []
    else:
        for i in xrange(len(Line)-2,-1,-1):
            if i != 0:
                if Line[i] == 0 and Line[i-1] == 0:
                    Line1 = Line[0:i+1]
                    Line2 = Line[i+1:len(Line)]
                    break
        else:
            Line1 = Line
    if Line1.count(1) != 0 and (Line1[0] != 1 and Line1[-1] != 1):
        Line1 = Line1[0:len(Line1)-1]
        for i in xrange(len(Line1)-1,-1,-1):
            if (i == 0 or (i != 0 and Line1[i] == 1 and Line1[i-1] == 0)):
                Line1.insert(i, 0)
                break
        if Line[-1] != 0:
            for j in xrange(len(Line1)-1,-1,-1):
                if (j == 0 or (j != 0 and Line1[j] == 0 and Line1[j-1] == 1)):
                    break
            for i in xrange(len(Line2)-1,-1,-1):
                Line1.insert(j+1, Line2[i])
        solve[index][RowCol] = Line1
        return False
    else:
        solve[index][RowCol] = Line2 + Line1
        return True

def Line_Reset(index, RowCol, element = -1):
    global solve
    #First filter
    if element == -1:
        temp1 = []
        temp2 = solve[index][RowCol]
    else:
        temp1 = solve[index][RowCol][0:element+1]
        temp2 = solve[index][RowCol][element+1:]
    if temp2[0] == 0:
        for j in xrange(len(temp2)-1):
            if temp2[j] == 1:
                temp2 = temp2[j:] + temp2[0:j]
                break
    #Second filter
    i = 1
    while True:
        #Second Filter Part 1
        for j in xrange(i, len(temp2)-1):
            if temp2[j] == 0 and temp2[j-1] == 0:
                i = j
                break
        else:
            break
        #Second Filter Part 2
        for k in xrange(i, len(temp2)-1):
            if temp2[k] == 1 and temp2[i:k] != []:
                temp2 = temp2[0:i]+temp2[k:]+temp2[i:k]
                break
        else:
            break
    temp = temp1+temp2
    temp1 = True
    if element != -1:
        while temp[-1] == 0:
            for i in xrange(element,-1,-1):
                if temp[i] == 0:
                    temp = temp[0:i]+temp[len(temp)-1:]+temp[i:len(temp)-1]
                    break
            else:
                temp = temp[len(temp)-1:]+temp[0:len(temp)-1]
            if temp[element] == 0:
                temp1 = False
                break
        else:
            temp1 = True
    solve[index][RowCol] = temp
    return temp1

def Step_Solve():
    global Step
    if Step == -1:
        Step = 0
    else:
        Step = -1

def Brute_Solve_1():
    global solutions, solve, Step, i, state, view_toggle_var, old_column
    solutions[0] = len(solutions[1])-1
    if Step == -1 or Step == 0 or i == -1:        
        i = len(solve[0][0])-1; state = False
        if solutions[0] != 0:
            for k in xrange(len(solutions[1])-2):
                if solutions[1][len(solutions[1])-1] == solutions[1][k]:
                    del solutions[1][len(solutions[1])-1]
                    solutions[0] -= 1
                    break
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
                Line_Reset(0, j)
            if i != 0:
                state = Line_Shift(0, i-1)
                if state:
                    i -= 1
        else:
            state = Line_Shift(0, i)
            '''
            if solve_check != []:
                if not Line_Reset(0, solve_check[0], solve_check[1]):
                    state = Line_Shift(0, i)
            else:
                state = Line_Shift(0, i)
                '''
        if not state:
            i = Check_Solution()
        for m in xrange(len(solve[0][0])):
            for n in xrange(len(solve[0])):
                solutions[1][solutions[0]][m][n] = solve[0][n][m]
        if view_toggle_var:
            old_column = i
            View_Solution(solutions[0])
        elif old_column != i:
            View_Solution(solutions[0], old_column)
            old_column = i
        monk = False

def xy_select_update(e):
    global xy_select_var, xy_index_select_var, x_elements, y_elements
    if xy_select_var.get() == 'X axis':
        temp = (0,)
        for x in xrange(1,x_elements[0]):
            temp = temp + (x,)
        xy_index_select['values'] = temp
        del temp
        temp = 0
        if len(xy_index_select_var.get()) != 0:
            for x in xrange(len(x_elements[1][int(xy_index_select_var.get())])):
                if x_elements[1][int(xy_index_select_var.get())] != -1:
                    temp = temp + x_elements[1][int(xy_index_select_var.get())][x] + 1
        temp1 = (1,)
        for x in xrange(1,y_elements[0]-temp):
            temp1 = temp1 + (x+1,)
        xy_num_select['values'] = temp1
    elif xy_select_var.get() == 'Y axis':
        temp = (0,)
        for y in xrange(1,y_elements[0]):
            temp = temp + (y,)
        xy_index_select['values'] = temp
        del temp
        temp = 0
        if len(xy_index_select_var.get()) != 0:
            for y in xrange(len(y_elements[1][int(xy_index_select_var.get())])):
                if y_elements[1][int(xy_index_select_var.get())] != -1:
                    temp = temp + y_elements[1][int(xy_index_select_var.get())][y] + 1
        temp1 = (1,)
        for y in xrange(1,x_elements[0]-temp):
            temp1 = temp1 + (y+1,)
        xy_num_select['values'] = temp1

def XY_Add():
    global xy_select_var, xy_index_select_var, xy_num_select_var, x_elements, y_elements
    if len(xy_select_var.get()) != 0 and len(xy_index_select_var.get()) != 0 and len(xy_num_select_var.get()) != 0:
        if xy_select_var.get() == 'X axis':
            if x_elements[1][int(xy_index_select_var.get())] == [-1]:
                x_elements[1][int(xy_index_select_var.get())] = [int(xy_num_select_var.get())]
            else:
                x_elements[1][int(xy_index_select_var.get())].append(int(xy_num_select_var.get()))
        elif xy_select_var.get() == 'Y axis':
            if y_elements[1][int(xy_index_select_var.get())] == [-1]:
                y_elements[1][int(xy_index_select_var.get())] = [int(xy_num_select_var.get())]
            else:
                y_elements[1][int(xy_index_select_var.get())].append(int(xy_num_select_var.get()))
    reinitialize(5)
    
def XY_Del():
    global xy_select_var, xy_index_select_var, xy_num_select_var
    if len(xy_select_var.get()) != 0 and len(xy_index_select_var.get()) != 0 and len(xy_num_select_var.get()) != 0:
        if xy_select_var.get() == 'X axis':
            if len(x_elements[1][int(xy_index_select_var.get())]) == 1:
                x_elements[1][int(xy_index_select_var.get())] = [-1]
            else:
                x_elements[1][int(xy_index_select_var.get())].pop()
        elif xy_select_var.get() == 'Y axis':
            if len(y_elements[1][int(xy_index_select_var.get())]) == 1:
                y_elements[1][int(xy_index_select_var.get())] = [-1]
            else:
                y_elements[1][int(xy_index_select_var.get())].pop()

    reinitialize(5)

def View_Toggle():
    global view_toggle_var, Step
    view_toggle_var = not view_toggle_var
    if Step == -1:
        Step = 0
    else:
        Step = -1

def reinitialize(z=0):
    global x_elements, y_elements, solve, labels, updated, finished, Step, i, state, tile_grid, solutions
    if z == 1:
        x_elements[0] += 1
        while True:
            if len(x_elements[1]) < x_elements[0]:
                x_elements[1].append([-1])
            else:
                break
    elif z == 2:
        if x_elements[0] > 3:
            x_elements[0] -= 1
        while True:
            if len(x_elements[1]) > x_elements[0]:
                del x_elements[1][len(x_elements[1])-1]
            else:
                break
    elif z == 3:
        y_elements[0] += 1
        while True:
            if len(y_elements[1]) < y_elements[0]:
                y_elements[1].append([-1])
            else:
                break
    elif z == 4:
        if y_elements[0] > 3:
            y_elements[0] -= 1
        while True:
            if len(y_elements[1]) > y_elements[0]:
                del y_elements[1][len(y_elements[1])-1]
            else:
                break
    if z != 0:
        del solve[0]; del solve[0]
        solve = [[],[]]
        for j in xrange(2):
            for k in xrange(len(labels[j])):
                if k%2 == 1:
                    labels[j][k].destroy()
        labels = [[],[],0,0]
        updated = False
        finished = -1
        Step = -1; i = 0; state = False
        if len(tile_grid) != 0:
            for j in xrange(len(tile_grid)):
                for k in xrange(len(tile_grid[j])):
                    tile_grid[j][k].destroy()
        tile_grid = []
    Create_Labels()
    Populate_Solves()
    View_Solution(0)
    Refresh_Save_List(0)
    
reinitialize(0)

x_plus.configure(command=lambda var1=1:reinitialize(var1))
x_neg.configure(command=lambda var2=2:reinitialize(var2))
y_plus.configure(command=lambda var3=3:reinitialize(var3))
y_neg.configure(command=lambda var4=4:reinitialize(var4))
new.configure(command=lambda var6=1:Refresh_Save_List(var6))
save.configure(command=lambda var7=2:Refresh_Save_List(var7))
load.configure(command=lambda var8=3:Refresh_Save_List(var8))
xy_select.bind('<<ComboboxSelected>>', xy_select_update)
xy_index_select.bind('<<ComboboxSelected>>', xy_select_update)
file_selector.bind('<<ComboboxSelected>>', lambda e,var5=0:Refresh_Save_List(var5))
go_solve.configure(command=Brute_Solve_1)
view_solve.configure(command=View_Solution)
view_toggle.configure(command=View_Toggle)
Stepper.configure(command=Step_Solve)
xy_add.configure(command=XY_Add)
xy_del.configure(command=XY_Del)
Main.mainloop() #The final Thread
