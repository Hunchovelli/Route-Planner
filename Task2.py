#Jordan and Desnid

#importing the module which read excel files
from openpyxl import load_workbook
import networkx
import matplotlib.pyplot as plt

#creates an object to the excel sheet with the london undeground data
file = load_workbook("Stations.xlsx") #make sure to run python script in the working directory
#stores the main sheet from the excel file in variable
sheet = file.active

#makes the graph object
G = networkx.Graph()

#List of all the stations without duplicates
stations_list = []

#iterates through the column 'B' in the excel sheet
for station in sheet["B"]:
    #checks for duplicates by comparing the stations in the column with ones already in added to the statio_list
    if station.value not in stations_list:
        #adds a station to the list if not already in the list
        stations_list.append(station.value)

#for each station in station_list we iterate through the list
for station in stations_list:
    #make each station into a node on the graph
    G.add_node(station)


#for each station in station_list we iterate through the list
for station in stations_list:
    #iterates through every cell in column 'E' in the excel sheet
    for cell in sheet["E"]:
        #if the cell content we are currently on in the iteration of the excel sheet column 'E' is equal to the station we are currently on in the iteration of the station_list
        if cell.value == station:
            #make an edge between the current cell we are on in the excel sheet in column 'E' and the adjacent cell in colum 'F'. Also, add the attributes weight/time between the stations which is in column 'G.
            G.add_edge(cell.value, sheet['F'+str(cell.row)].value, weight = sheet['G'+str(cell.row)].value)

#define function dijskta with arguements, graph = the graph of the stations, source = the starting station and destination = the target station.
def dijsktra(graph, source, destination):
    #the counter/variable for the route different routes there are. Initialise variable at 1 to start from Route 1.
    route_count = 1
    #try block so we use the exception block to bypass the error message when there are no longer any possible routes
    try:
        #while loops which continues looping if it is True that there is a path between the source and destination stations on the graph
        while networkx.has_path(graph, source, destination) == True:
            #the counter/variable for index of the list networkx.has_path(graph, source, destination), which returns an array of the journey, with the stations as the items.
            count = 0
            #the counter/variable for to store the time for each route
            time = 0
            #removes the edge between the starting station and the next station in networkx.has_path(graph, source, destination) path created.
            graph.remove_edge(source, networkx.shortest_path(graph, source, destination)[1])
            #labels the route, starting from route 1 and utilise the route_counter variable we initialised earlier.
            print ("\nRoute %s\n" % (route_count))
            #for loops through the items/stations in networkx.has_path(graph, source, destination) array.
            for station in networkx.shortest_path(graph, source, destination):
                #iterates through every cell in column 'B' in the excel sheet.
                for cell in sheet['B']:
                    #when we reach end of array, index error will be araised
                    if station == destination:
                        #hence use continue keyword to exit both for loop we are in and bypass the index error.
                        continue
                    #executes the code if the stations in the array we are looping in with the stations in the cell in column 'B' of the excel sheet and the next station in the array with the station row above in column B. This is to uniquely match the neighboruing stations with certain lines.
                    if cell.value == station and networkx.shortest_path(graph, source, destination)[count+1] == sheet['B'+str(cell.row-1)].value:
                        #prints the route in column form using newlines and formatting techniques
                        print ("%s to %s via the %s line." % (cell.value, networkx.shortest_path(graph, source, destination)[count+1], sheet['A'+str(cell.row)].value))
                        #adds the time from the values in column G for the route between the pair of stations in the same row in the excel sheet
                        time += int(sheet['G'+str(cell.row)].value)
                    #executes the code if the stations in the array we are looping in with the stations in the cell in column 'B' of the excel sheet and the next station in the array with the station row above in column B. This is to uniquely match the neighboruing stations with certain lines. 
                    if cell.value == station and networkx.shortest_path(graph, source, destination)[count+1] == sheet['B'+str(cell.row+1)].value:
                        #prints the route in column form using newlines and formatting techniques
                        print ("%s to %s via the %s line." % (cell.value, networkx.shortest_path(graph, source, destination)[count+1], sheet['A'+str(cell.row)].value))
                        #adds the time from the values in column G for the route between the pair of stations in the same row in the excel sheet
                        time += int(sheet['G'+str(cell.row)].value)
                #used to update the count variable after we have iterated through an item/station in the networkx.has_path(graph, source, destination) array.
                count += 1
            #print the total time for each route after fully iterating through a networkx.has_path(graph, source, destination) array.
            print ("\nTotal Time for Route %s is %s minutes." % (route_count, time))
            #used to update the route_count variable after fully iterating through a networkx.has_path(graph, source, destination) array.
            route_count += 1
    #except block executed if networkx.exception.NetworkXNoPath is raised. Usually raised when no more possible paths from source to the target.  
    except networkx.exception.NetworkXNoPath:
        #instead of the default error message python produces when networkx.exception.NetworkXNoPath is raised, custom print statement is outputted instead.
        print ("No route is feasible as all other routes are closed or impossible.")

#takes the input of starting station from the user
src_input = input("Where would you like to start your journey?: ")
#takes the input of destination station from the user
dest_input = input("Where would you like to go to?: ")

#executes the function defined above using the graph we created, the starting input from the user and the destination input from the user as the arguements.
print (dijsktra(G, src_input, dest_input))
