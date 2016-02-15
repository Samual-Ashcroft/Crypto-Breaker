solve = [[],[[1,0,1,0,1,1,1,1,0,0,1,0,1,1,1,1,0,1,1,0,]]]

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
    if Line1.count(1) != 0:
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

def Line_Reset(index, RowCol):
    #First filter
    if solve[index][RowCol][0] == 0:
        for j in xrange(len(solve[index][RowCol])-1):
            if solve[index][RowCol][j] == 1:
                solve[index][RowCol] = solve[index][RowCol][j:] + solve[index][RowCol][0:j]
                break  
    print False, solve[index][RowCol], 'first filter'
    #Second filter
    i = 1
    while True:
        #Second Filter Part 1
        for j in xrange(i, len(solve[index][RowCol])-1):
            if solve[index][RowCol][j] == 0 and solve[index][RowCol][j-1] == 0:
                i = j
                print i, j
                break
        else:
            break
        #Second Filter Part 2
        for k in xrange(i, len(solve[index][RowCol])-1):
            if solve[index][RowCol][k] == 1 and solve[index][RowCol][i:k] != []:
                print 'second filter', i, k
                print solve[index][RowCol][0:i]
                print solve[index][RowCol][k:]
                print solve[index][RowCol][i:k]
                print False, solve[index][RowCol]
                solve[index][RowCol] = solve[index][RowCol][0:i]+solve[index][RowCol][k:]+solve[index][RowCol][i:k]
                print False, solve[index][RowCol]
                break
        else:
            break

print solve[1]
'''
for i in xrange(1703):
    #while True:
    goog = Line_Shift(1, 0)
    print goog, solve[1][0]
    if goog:
        break
    '''
Line_Reset(1, 0)
