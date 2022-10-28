#Jordan and Desnid

#importing the module which read excel files
from openpyxl import load_workbook

#creates an object to the excel sheet with the london undeground data
wrkbk2 = load_workbook("Stations.xlsx") #make sure to run python script in the working directory
#stores the main sheet in variable
sheet = wrkbk2.active
print (sheet)