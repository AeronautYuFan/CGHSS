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

    # Add nodes for each part of the structure and connect them
    for event in triggering_events:
        event_node = event.strip()
        G.add_node(event_node, label=event_node)
        
        for location in locations:
            location_node = location.strip()
            G.add_node(location_node, label=location_node)
            G.add_edge(event_node, location_node)
            
            for power in powers_invoked:
                power_node = power.strip()
                G.add_node(power_node, label=power_node)
                G.add_edge(location_node, power_node)
                
                # Add citation at the end of each power node
                G.add_node(citation, label=citation)
                G.add_edge(power_node, citation)

    # Draw the graph
    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(G)  # Layout for a tree structure
    nx.draw(G, pos, with_labels=True, node_size=2000, node_color="lightblue", font_size=10, font_weight="bold", edge_color="gray", arrows=True)

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
