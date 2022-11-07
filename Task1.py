#Myron and Ademide

import openpyxl
import networkx as nx
from matplotlib import pyplot as plt
from networkx import single_source_dijkstra

wrkbk = openpyxl.load_workbook("Stations.xlsx")  # Creating a link to the excel file with the London Underground Data
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
for a in rows1:
    if a[1] in station_dict.keys():
        station_dict[a[1]].append(a[0])
        station_dict[a[1]].sort()
    else:
        station_dict[a[1]] = [a[0]]
        station_dict[a[1]].sort()

# Get list of vertices by obtaining all the keys from the dictionary
vertices = station_dict.keys()

# print(vertices)  # Run this for a better idea

# Append all the edges from the excel file
for b in rows2:
    edges.append(b)

# print(edges)   # Run this for a better idea

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

# CONTINUATION OF TASK 1

# Create the graph by passing the list of nodes and edges
G = nx.MultiGraph()
G.add_nodes_from(vertices)
G.add_weighted_edges_from(edges)

# Example for shortest path algorithm. Not going to use this for the final code. Need to implement Dijkstra's algorithm
# print(single_source_dijkstra(G, source="Acton Town", target="Green Park", weight='weight'))


# Main program which will be take the input from user and display route
def get_route():

    # Count the number of times the user will need to change lines
    line_change_counter = 0

    print("Enter the departure stations: ")
    departure = input()
    print("Enter the destination stations: ")
    destination = input()
    route = single_source_dijkstra(G, source=departure, target=destination, weight='weight')
    print("The following route has been generated:")
    print()

    # Print route, station by station along with the line they will use to get there
    for i in route[1]:

        if route[1].index(i) == 0:
            current_line = i
            print(i)
            continue

        print("{} : via the {} line".format(i, station_dict[current_line][0]))

        # Add to the line change counter if line change detected
        if station_dict[current_line][0] != station_dict[i][0]:
            line_change_counter += 1

        # Update the line used after every iteration
        current_line = i

    # Testing stuff
    print()
    print(line_change_counter)
    print()
    print("Total route time will be {} minutes".format(route[0]))


get_route()


