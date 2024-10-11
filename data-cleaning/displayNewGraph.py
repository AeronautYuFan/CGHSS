import pandas as pd
import os
import networkx as nx
import matplotlib.pyplot as plt

# Load the filtered CSV file
filtered_df = pd.read_csv("data-cleaning/data-coastguard-only.csv")

# Select the desired columns
new_columns_df = filtered_df[['Entity Empowered', 'Citation', 'Document Type', 'Location', 'Triggering Event']]

# Create a directed graph
G = nx.DiGraph()

# Add edges based on the selected columns
for index, row in new_columns_df.iterrows():
    G.add_edge(row['Entity Empowered'], row['Triggering Event'])
    G.add_edge(row['Triggering Event'], row['Location'])
    G.add_edge(row['Location'], row['Document Type'])

# Define the path for the output PNG file
output_png_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'coastguard_graph.png')

# Draw the graph
plt.figure(figsize=(12, 8))
pos = nx.spring_layout(G)  # positions for all nodes
nx.draw_networkx_nodes(G, pos, node_size=3000)
nx.draw_networkx_edges(G, pos, arrowstyle='-|>', arrowsize=20)
nx.draw_networkx_labels(G, pos, font_size=12, font_family='sans-serif')

# Save the graph as a PNG file
plt.axis('off')  # Turn off the axis
plt.savefig(output_png_path, format='png')
plt.close()

print(f"Directed graph saved as: {output_png_path}")
