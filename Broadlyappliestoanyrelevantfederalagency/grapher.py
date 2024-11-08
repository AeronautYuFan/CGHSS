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

    # Split the triggering events, locations, and powers invoked into lists
    triggering_events = row["Triggering Event"].split(",")
    locations = row["Location"].split(",")
    powers_invoked = row["Powers Invoked"].split(",")
    citation = row["Citation"]
    agency = row["Specific Agency"]

    # Add nodes and edges for each triggering event
    for event in triggering_events:
        event = event.strip()
        # Add a node for each location linked from each triggering event
        for loc in locations:
            loc = loc.strip()
            G.add_edge(event, loc)
            
            # Add nodes for powers invoked, connecting from each location node
            for power in powers_invoked:
                power = power.strip()
                G.add_edge(loc, power)

                # Add the citation and specific agency as the final node
                G.add_edge(power, citation)
                G.nodes[citation]["label"] = f"{citation}\n{agency}"

    # Draw the graph
    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(G)  # Layout for visualization
    labels = nx.get_node_attributes(G, 'label')
    nx.draw(G, pos, with_labels=True, labels=labels, node_size=3000, node_color="lightblue", font_size=8, font_weight="bold", arrows=True)
    plt.title(f"Graph for {citation}")
    
    # Save the graph as an image
    plt.savefig(f"{output_dir}/graph_{index}_{citation}.png")
    plt.close()

# Generate graphs for each row in the CSV
for index, row in df.iterrows():
    create_graph(row, index)

print(f"Graphs saved in the '{output_dir}' directory.")
