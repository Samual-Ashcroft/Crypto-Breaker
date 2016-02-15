solve = [[],[[1,0,1,1,1,0,1,0,1,1,1,0,1,0,1,1,1,0,1,0,1,1,1,0,1]]]

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
        temp1 = solve[index][RowCol][0:element]
        temp2 = solve[index][RowCol][element:]
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
                temp1 = True
                break
        else:
            temp1 = False
    solve[index][RowCol] = temp
    return temp1
    
print solve[1]

for i in xrange(1):
    #while True:
    goog = Line_Shift(1, 0)
    print goog, solve[1][0]
    if goog:
        break
    '''
print Line_Reset(1, 0, 4)
print solve[1]
print 'yolo'

jig = True
print jig
jig = not jig
print jig
'''
