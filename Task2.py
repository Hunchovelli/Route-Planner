#Jordan and Desnid

#importing the module which read excel files
from openpyxl import load_workbook

#creates an object to the excel sheet with the london undeground data
file = load_workbook("Stations.xlsx") #make sure to run python script in the working directory
#stores the main sheet in variable
sheet = file.active

#List of all the stations without duplicates
stations_list = []
#Dictionary of stations and the lines that run through them
stations_dict = {}

#iterates through the column 'B' in the excel sheet
for station in sheet["B"]:
    #checks for duplicates by comparing the stations in the column with ones already in added to the statio_list
    if station.value not in stations_list:
        #adds a station to the list if not already in the list
        stations_list.append(station.value)

#iterates through the station_list (without duplicates) so we can add all the lines wach station goes through as values in a dictionary
for station in stations_list:
    #iterates through the column 'B' in the excel sheet
    for cell in sheet["B"]:
        #matching the cell value in column B with the station to see how many time it occurs in column B to link it with the line it is on
        if cell.value == station:
            #appends to dictionary the corresponding value in column A and creates empty liste with the key as a default if the key is not present yet
            stations_dict.setdefault(station, []).append(sheet['A'+str(cell.row)].value)

#iterate thorugh the dictionary to see which stations have only one line       
for station in stations_dict:
    #checks if station/value has only one line/value
    if len(stations_dict[station]) == 1:
        #prints conclusion that it is not feasible to close station as only one line goes through it
        print ('Closure of ' + str(station) + ' is not feasible as it only goes through one line which is the ' + str(stations_dict[station])
        + ' hence it will be inaccesible from other lines if the station is closed.')  
