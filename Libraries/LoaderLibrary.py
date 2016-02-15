Write_Count = 0; Buffer_Size = 30; text_file = None; Read_Buffer = ["",""]

def Write_Counter(length, text_file):
    global Write_Count#, text_file#making that counter global to this recursive function
    Write_Count += length
    if Write_Count >= Buffer_Size: #making the txt file go a new line if it has created a long enough buffer
        Write_Count = 0 #reset the buffer counter length
        text_file.write('\n') #insert the carriage return

def Write_List(List, text_file):
    for i in xrange(len(List)): #iterating across the base length of the inputed list
        if type(List[i]) == list: #the recursive part
            text_file.write('l,') #record that this element is a list
            Write_Counter(4, text_file)
            Write_List(List[i], text_file) #recursively launch this function within itself...   recursion is fun
            text_file.write(';,') #once that sub launch of this function finishes, cap the list
            Write_Counter(2, text_file)
        else:
            buff = ''
            if type(List[i]) == str:
                buff = 's,'+ str(List[i])+ ',' #record a str element
            elif type(List[i]) == int:
                buff = 'i,'+ str(List[i])+ ',' #record an int element
            elif type(List[i]) == float:
                buff = 'f,'+ str(List[i])+ ',' #record a float element
            elif type(List[i]) == bool:
                if List[i]: #record a boolean element
                    buff = 'b,1,'
                else:
                    buff = 'b,0,'
            text_file.write(buff) #write the data
            Write_Counter(len(buff), text_file) #update the buffer length, maybe newline

def Write_file(List, file_name):
    global Write_Count, Buffer_Size, text_file, Read_Buffer
    Write_Count = 0; Buffer_Size = 30; text_file = None; Read_Buffer = ["",""]
    text_file = open(file_name, 'w')
    text_file.seek(0)
    Write_List(List, text_file)
    text_file.close()
    Write_Count = 0; Buffer_Size = 30; text_file = None; Read_Buffer = ["",""]

def Refill_Buffer():
    global Read_Buffer, text_file
    Read_Buffer[0] = Read_Buffer[0]+Read_Buffer[1]
    Read_Buffer[1] = text_file.readline()
    Read_Buffer[1] = Read_Buffer[1][0:len(Read_Buffer[1])-1]

def Read_List():
    global Read_Buffer
    variable = []; typ = ''
    while True:
        #grapping the type label
        typ = Read_Buffer[0][0:Read_Buffer[0].find(',')]
        #removing that type label from the buffer
        Read_Buffer[0] = Read_Buffer[0][Read_Buffer[0].find(',')+1:
                                        len(Read_Buffer[0])]
        #The Breaker, either calls a buffer refill or breaks when there is no more buffer
        if ((len(Read_Buffer[0]) < 25) and (Read_Buffer[1] != '')):
            Refill_Buffer()
        elif ((Read_Buffer[1] == '') and ((Read_Buffer[0] == '') or (Read_Buffer[0] == ';'))): 
            break
        if (typ == ';'): #incase of refill 'and' end of list
            break
        #Effective Switch Case for the type label
        if typ == 'l': #The recursive call...  will it work...
            variable.append(Read_List())
        else:
            if typ == 's':
                variable.append(Read_Buffer[0][0:Read_Buffer[0].find(',')])
            elif typ == 'i':
                variable.append(int(Read_Buffer[0][0:Read_Buffer[0].find(',')]))
            elif typ == 'f':
                variable.append(float(Read_Buffer[0][0:Read_Buffer[0].find(',')]))
            elif typ == 'b':
                if Read_Buffer[0][0:Read_Buffer[0].find(',')] == '1':
                    variable.append(True)
                else:
                    variable.append(False)
            #removing that entry from the buffer
            Read_Buffer[0] = Read_Buffer[0][Read_Buffer[0].find(',')+1:len(Read_Buffer[0])]
    #if len(variable) == 1:
    #    variable = variable[0]
    return variable

def Read_file(file_name):
    global Write_Count, Buffer_Size, text_file, Read_Buffer
    Write_Count = 0; Buffer_Size = 30; text_file = None; Read_Buffer = ["",""]
    text_file = open(file_name, 'r')
    text_file.seek(0)
    Refill_Buffer()
    Refill_Buffer()
    file_data = Read_List()
    text_file.close()
    Write_Count = 0; Buffer_Size = 30; text_file = None; Read_Buffer = ["",""]
    return file_data



    
