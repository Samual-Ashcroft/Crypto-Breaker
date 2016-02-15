#-----------------------------------
#The Writer of lists containing lists,str,int,float or bool
#-----------------------------------
#import sys
#sys.path.insert(0, '../Libraries/')
from Libraries import LoaderLibrary

#Example of nasty BS list in list action data to store
file_data = [['Save000','Save001']]
#file_data = [['hokey doke',[[2,3,4],[3,4,5],[6,7,8,['koko',7],9]], 2, 16.3,'hello'],4,5.2,67,'jojo',['koko',82,True, False]]
print file_data
file_name = "Data" #The file to create or overwrite
LoaderLibrary.Write_file(file_data, file_name)
#------------------------------
#The Reader of lists containing lists,str,int,float or bool
#------------------------------
file_data = []
file_data = LoaderLibrary.Read_file(file_name)
print file_data

while True:
    s = raw_input('yoyo')
    if s == 'y':
        break
    file_data = []
    file_data = LoaderLibrary.Read_file(file_name)
    print file_data
