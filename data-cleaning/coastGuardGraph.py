import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import os

# Load the filtered CSV file
df = pd.read_csv('data-cleaning/filteredUSCGdata.csv')

# Create a directed graph
G = nx.DiGraph()

# Iterate through the DataFrame to add edges
for _, row in df.iterrows():
    triggering_event = row['Triggering Event']
    location = row['Location']
    # Split the powers invoked by comma and strip spaces
    powers_invoked = [power.strip() for power in row['Powers Invoked'].split(',')]
    citation = row['Citation']
    
    # Add edges to the graph
    G.add_edge(triggering_event, location)
    for power in powers_invoked:
        G.add_edge(location, power)
        G.add_edge(power, citation)

# Draw the graph
plt.figure(figsize=(12, 8))
pos = nx.spring_layout(G)  # positions for all nodes
nx.draw(G, pos, with_labels=True, node_size=2000, node_color='lightblue', font_size=10, font_color='black', arrows=True)
plt.title('Directed Graph of Triggering Events, Locations, Powers Invoked, and Citations')

# Get the current script directory
script_dir = os.path.dirname(os.path.abspath(__file__))
# Define the path for the PNG file
png_file_path = os.path.join(script_dir, 'directed_graph.png')

# Save the figure
plt.savefig(png_file_path, format='png')
plt.close()  # Close the plot to free up memory
