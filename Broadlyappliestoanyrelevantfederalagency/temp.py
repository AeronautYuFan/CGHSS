import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import os

# Load the data
df = pd.read_csv('Broadlyappliestoanyrelevantfederalagency/minidata.csv')

# Create output directory if it doesn't exist
output_dir = "graphs"
os.makedirs(output_dir, exist_ok=True)

# Iterate over each unique triggering event to create a separate graph
for triggering_event in df['Triggering Event'].unique():
    # Filter the data for the current triggering event
    subset_df = df[df['Triggering Event'] == triggering_event]

    # Create a directed graph
    G = nx.DiGraph()
    
    # Add the head node (triggering event)
    G.add_node(triggering_event)

    # Dictionary to hold labels for nodes to print identically
    node_labels = {triggering_event: triggering_event}

    # Process each row in the filtered data
    for _, row in subset_df.iterrows():
        location = row['Location']
        powers = row['Powers Invoked'].split(',')
        citation = row['Citation']
        
        # Create location nodes
        if location == "Both":
            G.add_node("Domestic")
            G.add_node("International")
            G.add_edge(triggering_event, "Domestic")
            G.add_edge(triggering_event, "International")
            node_labels["Domestic"] = "Domestic"
            node_labels["International"] = "International"
        else:
            G.add_node(location)
            G.add_edge(triggering_event, location)
            node_labels[location] = location

        # Add powers invoked with location-specific nodes
        for power in powers:
            power_name = power.strip()  # Remove any whitespace
            if location == "Both":
                # Unique IDs for domestic and international versions
                domestic_power_node = f"Domestic - {power_name}"
                international_power_node = f"International - {power_name}"
                
                G.add_node(domestic_power_node)
                G.add_node(international_power_node)
                
                G.add_edge("Domestic", domestic_power_node)
                G.add_edge("International", international_power_node)
                
                # Use the same label for both nodes
                node_labels[domestic_power_node] = power_name
                node_labels[international_power_node] = power_name
                
                # Link power nodes to citation
                G.add_edge(domestic_power_node, citation)
                G.add_edge(international_power_node, citation)
            else:
                # Unique ID for location-specific power node
                location_power_node = f"{location} - {power_name}"
                
                G.add_node(location_power_node)
                G.add_edge(location, location_power_node)
                
                # Use the same label
                node_labels[location_power_node] = power_name
                
                # Link power node to citation
                G.add_edge(location_power_node, citation)

        # Add the citation node and label it
        G.add_node(citation)
        node_labels[citation] = citation

    # Draw and save the graph
    pos = nx.spring_layout(G)  # Position nodes for visualization
    plt.figure(figsize=(12, 8))
    nx.draw(G, pos, with_labels=True, labels=node_labels, node_size=2000, node_color="skyblue", font_size=10, font_weight="bold", edge_color="gray")
    plt.title(f"Graph for Triggering Event: {triggering_event}")
    
    # Save the graph image
    plt.savefig(os.path.join(output_dir, f"{triggering_event}_graph.png"))
    plt.close()
