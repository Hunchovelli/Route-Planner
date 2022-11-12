#Myron and Ademide

import openpyxl
import networkx as nx
from networkx import single_source_dijkstra, NodeNotFound, NetworkXNoPath

wrkbk = openpyxl.load_workbook("Stations_Updated.xlsx")  # Creating a link to the excel file with the London Underground Data
ws = wrkbk['Sheet1']

# This table will be used to create a dictionary with all the stations along with the lines that operate at that station
rows1 = ws.iter_rows(min_row=1, max_row=380, min_col=1, max_col=2, values_only=True)

# This table will be used to create the list of edges with weights needed for the network
rows2 = ws.iter_rows(min_row=1, max_row=377, min_col=5, max_col=7, values_only=True)

# Dictionary to store stations as keys and list of operating lines as values.
# Example: {'Green Park':['Picadilly', 'Jubilee', 'Victoria']}
station_dict = {}

# List of all the edges within our network
edges = []

# Adding the stations to dictionary along with all the lines that operate at the stations
for row in rows1:
    station = row[1].rstrip()  # Using rstrip() to get rid of unnecessary whitespace at end of string if present
    if station in station_dict.keys():
        station_dict[station].append(row[0])
        station_dict[station].sort()
    else:
        station_dict[station] = [row[0]]
        station_dict[station].sort()
    

# Get list of vertices by obtaining all the keys from the dictionary
vertices = station_dict.keys()

# print(vertices)  # Run this for a better idea

# Append all the edges from the excel file
for row in rows2:
    start = row[0].rstrip()
    end = row[1].strip()
    edges.append((start, end, row[2]))

# print(edges)   # Run this for a better idea

##########################################################################################################
# THESE 2 FOR LOOPS ARE NOT PART OF TASK 1
# THEY CAN BE USED AS REFERENCE FOR TASK 2
# Get all the edges linked to one station
# for i in edges:
#     if i[0] == "South Kensington" or i[1] == "South Kensington" or i[2] == "South Kensington":
#         print(i)

# # Remove an edge linked to the station
# for j in edges:
#     if j == ('Gloucester Road', 'South Kensington', 3):
#         edges.remove(j)
###########################################################################################################

# CONTINUATION OF TASK 1

# Create the graph by passing the list of nodes and edges
G = nx.MultiGraph()
G.add_nodes_from(vertices)
G.add_weighted_edges_from(edges)


################ Processing Data for Task 3 ###############################

# Processing data from the Weekly Crowd Traffic spreadsheet
wrkbk2 = openpyxl.load_workbook("WeeklyCrowdTraffic_Updated.xlsx")  # Link to underground crowd traffic data
ws2 = wrkbk2['Sheet1']

rows3 = ws2.iter_rows(min_row=3, max_row=269, min_col=1, max_col=7, values_only=True)

# This dictionary will hold each station as keys and each key will hold its own dictionary of crowd density
# Example: station_density["Green Park"] ------>  {'Weekday': 63355, 'Saturday': 38963, 'Sunday': 27357}
# The numbers in the dictionary are the average number of people at the station on that given day
station_density = {}

for row in rows3:
    station = row[0].rstrip()
    if station in vertices:

        weekday_avg = (row[1] + row[4])/2  # Calculate the average number of people visiting the station on weekdays
        saturday_avg = (row[2] + row[5])/2  # Calculate the average number of people visiting the station on saturdays
        sunday_avg = (row[3] + row[6])/2  # Calculate the average number of people visiting the station on sundays

        # Add the averages to the dictionary
        station_density[station] = {}
        station_density[station]["Weekday"] = int(weekday_avg)
        station_density[station]["Saturday"] = int(saturday_avg)
        station_density[station]["Sunday"] = int(sunday_avg)
#################################################################################################################

# Task 1a
# Main program which will be take the input from user and display route
def get_route():

    # Count the number of times the user will need to change lines
    # Add 5 min to the total time for each line change
    line_change_counter = 0

    print("Enter the departure stations: ")
    departure = input()
    print("Enter the destination stations: ")
    destination = input()
    
    # Handle exceptions occurred from bad input
    try:
        route = single_source_dijkstra(G, source=departure, target=destination, weight='weight')

        # Print route, station by station along with the line they will use to get there
        for i in route[1]:

            # First station will not have an associated line because we assume that user is at the station
            if route[1].index(i) == 0:
                prev_station = i  # Holds the station travelled from
                prev_line = station_dict[i][0]  # Holds the line used to travel to the previous station
                print(i)
                continue

            chosen_line = ""

            # Determine which line the user will take to the new station
            for line in station_dict[i]:
                if line in station_dict[prev_station]:
                    chosen_line = line

            print("{} : via the {} line".format(i, chosen_line))

            # Add to the line change counter if line change detected
            if chosen_line != prev_line:
                line_change_counter += 1

            # Update the previous station and line used
            prev_station = i
            prev_line = chosen_line

        # Add 30 seconds passenger boarding/disembarking time for each station excluding start and end stations
        station_halt_time = ((len(route[1]) - 2) * 30) / 60

        # Add a 5 minute delay each time the user has to switch to another line
        line_change_delay = line_change_counter * 5

        # Calculate the total time for the whole journey including delays
        total_time = int(route[0] + station_halt_time + line_change_delay)

        print("\nTotal route time will be {} minutes including delays".format(total_time))

    except(NodeNotFound, NetworkXNoPath):
        print("Invalid Nodes Entered")
    
    
get_route()


