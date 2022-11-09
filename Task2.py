#Jordan and Desnid

#importing the module which read excel files
from openpyxl import load_workbook
import networkx
import matplotlib.pyplot as plt

#creates an object to the excel sheet with the london undeground data
file = load_workbook("Stations.xlsx") #make sure to run python script in the working directory
#stores the main sheet in variable
sheet = file.active

G = networkx.Graph()

#List of all the stations without duplicates
stations_list = []
#Temporary dictionary of stations and the neighbouring stations
stations_dict = {}
#Permanent dictionary of stations and the neighbouring stations

#iterates through the column 'B' in the excel sheet
for station in sheet["B"]:
    #checks for duplicates by comparing the stations in the column with ones already in added to the statio_list
    if station.value not in stations_list:
        #adds a station to the list if not already in the list
        stations_list.append(station.value)

for station in stations_list:
    #iterates through the column 'B' in the excel sheet
    for cell in sheet["B"]:
        #matching the cell value in column B with the station to see how many time it occurs in column B to link it with the line it is on
        if cell.value == station:
            #appends to dictionary the corresponding value in column A and creates empty liste with the key as a default if the key is not present yet
            stations_dict.setdefault(station, []).append(sheet['A'+str(cell.row)].value)



#makes a station to station_list into node
for station in stations_list:
    G.add_node(station)


#iterates through the station_list (without duplicates) so we can add all the lines each station goes through as values in a dictionary
for station in stations_list:
    #iterates through the column 'E' in the excel sheet
    for cell in sheet["E"]:
        #adds an edge between neighbouring stations on the graph
        if cell.value == station:
            G.add_edge(station, sheet['F'+str(cell.row)].value, weight = sheet['G'+str(cell.row)].value)
            #print (temp_stations_dict)
            #appends to dictionary the corresponding value in column A and creates empty liste with the key as a default if the key is not present yet

#dijskta function with arguements
def dijsktra(graph, source, destination):
    #this used to defelect the exception error 
    try:
        #used to count the index of the line we are in 
        count = 0
        while networkx.has_path(graph, source, destination) == True:
            graph.remove_edge(source, networkx.shortest_path(graph, source, destination)[1])
            for station in networkx.shortest_path(graph, source, destination):
                for cell in sheet["B"]:
                    if cell.value == destination and sheet['B'+str(cell.row+1)].value == networkx.shortest_path(graph, source, destination)[count-1]:
                        print (str(cell.value) + ' via the ' + sheet['A'+str(cell.row)].value + ' line.')
                        break
                for cell in sheet["B"]:        
                    if station == cell.value and networkx.shortest_path(graph, source, destination)[count+1] == sheet['B'+str(cell.row-1)].value:
                        print (str(cell.value) + ' via the ' + sheet['A'+str(cell.row)].value + ' line.')
                count += 1
            break
    except:   
        print ("No route is feasible as all other routes are closed or impossible")
'''for cell in sheet["B"]:
            if cell.value == destination and sheet['B'+str(cell.row+1)].value == route[count-1]:
                print (str(cell.value) + ' via the ' + sheet['A'+str(cell.row)].value + ' line.')        
        for cell in sheet["B"]:        
            if station == cell.value and route[count+1] == sheet['B'+str(cell.row-1)].value:
                print (str(cell.value) + ' via the ' + sheet['A'+str(cell.row)].value + ' line.')
        count += 1'''        

    
src_input = input("Where would you like to start your journey?: ")
dest_input = input("Where would you like to go to?: ")

print (dijsktra(G, src_input, dest_input))
