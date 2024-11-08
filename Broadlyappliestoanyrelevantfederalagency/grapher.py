import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import os

# Load the CSV file
df = pd.read_csv("Broadlyappliestoanyrelevantfederalagency/data.csv")

# Create output directory for images
output_dir = "graph_images"
os.makedirs(output_dir, exist_ok=True)

# Function to create a directed graph based on a row of data
def create_graph(row, index):
    G = nx.DiGraph()

    # Parse the row data
    triggering_events = row['Triggering Event'].split(',')
    locations = row['Location'].split(',')
    powers_invoked = row['Powers Invoked'].split(',')
    citation = row['Citation']
    agency = row['Specific Agency']

    # Color maps for node types
    color_map = {}
    
    # Add nodes for each part of the structure with designated colors
    for event in triggering_events:
        event_node = event.strip()
        G.add_node(event_node, label=event_node)
        color_map[event_node] = 'lightcoral'  # Triggering events: light red
        
        for location in locations:
            location_node = location.strip()
            G.add_node(location_node, label=location_node)
            G.add_edge(event_node, location_node)
            color_map[location_node] = 'orange'  # Location: orange
            
            for power in powers_invoked:
                power_node = power.strip()
                G.add_node(power_node, label=power_node)
                G.add_edge(location_node, power_node)
                color_map[power_node] = 'lightgreen'  # Powers Invoked: green
                
                # Add citation at the end of each power node
                G.add_node(citation, label=citation)
                G.add_edge(power_node, citation)
                color_map[citation] = 'lightblue'  # Citation: blue

    # Draw the graph
    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(G)  # Layout for a tree structure
    node_colors = [color_map[node] for node in G.nodes()]
    
    nx.draw(G, pos, with_labels=True, node_size=2000, font_size=10, font_weight="bold", 
            node_color=node_colors, edge_color="gray", arrows=True)

    # Add the agency name in the top left corner
    plt.text(0.05, 0.95, f"Agency: {agency}", fontsize=12, ha='left', va='top', transform=plt.gca().transAxes)

    # Save the figure
    file_path = os.path.join(output_dir, f"graph_{index}.png")
    plt.savefig(file_path, format="png")
    plt.close()

# Create a graph for each row in the DataFrame
for index, row in df.iterrows():
    create_graph(row, index)

print("Graphs have been generated and saved in the 'graph_images' folder.")