#Myron and Ademide

import openpyxl
import networkx as nx
from matplotlib import pyplot as plt
from networkx import single_source_dijkstra

wrkbk = openpyxl.load_workbook("Stations.xlsx")  # Creating a link to the excel file with the London Underground Data
ws = wrkbk['Sheet1']

# This table will be used to create a dictionary with all the stations along with the lines that operate at that station
rows1 = ws.iter_rows(min_row=1, max_row=380, min_col=2, max_col=2, values_only=True)

# This table will be used to create the list of edges with weights needed for the network
rows2 = ws.iter_rows(min_row=1, max_row=377, min_col=5, max_col=7, values_only=True)

# Dictionary to store stations as keys and list of operating lines as values.
# Example: {'Green Park':['Picadilly', 'Jubilee', 'Victoria']}
station_dict = {}

# List of all the edges within our network
edges = []

# Initially only add the stations without the operating lines
for a in rows1:
    if a[0] in station_dict.keys():
        continue
    else:
        station_dict[a[0]] = []

# Get list of vertices by obtaining all the keys from the dictionary
vertices = station_dict.keys()

# print(vertices)  # Run this for a better idea

# Append all the edges from the excel file
for b in rows2:
    edges.append(b)

# print(edges)   # Run this for a better idea

# Create the graph by passing the list of nodes and edges
G = nx.MultiGraph()
G.add_nodes_from(vertices)
G.add_weighted_edges_from(edges)


pos = nx.random_layout(G)
nx.draw(G, pos, with_labels=1)  # Plotting the actual Graph (Not helpful so ignore)
# plt.show() # You can run this but it won't be that helpful

# Converting the created graph to a dictionary because easier to apply dijkstra algorithm
temp_dict = nx.to_dict_of_dicts(G)

# The created dictionary above is gonna be messy. This is why I have further refined it below to a more readable second
# dictionary
graph_dict = {}

for i in vertices:
    edge_keys = temp_dict[i].keys()
    graph_dict[i] = dict()
    for j in edge_keys:
        graph_dict[i][j] = temp_dict[i][j][0]["weight"]

# This new dictionary should be much clearer to understand. Consists of a dictionary where each key is a station and
# the value for each key is a nested dictionary which holds the neighbours of that station along with time taken
# for each
print(graph_dict["Green Park"]) # Example

# Example for shortest path algorithm. Not going to use this for the final code. Need to implement Dijkstra's algorithm
print(single_source_dijkstra(G, source="Acton Town", target="Green Park", weight='weight'))
