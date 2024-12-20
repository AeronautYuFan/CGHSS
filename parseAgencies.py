import pandas as pd
import os
import matplotlib.pyplot as plt
import networkx as nx

def create_agency_graph(df, agency):
    # Iterate over each row to process the triggering events
    for _, group in df.groupby('Triggering Event'):
        # Split the triggering events by commas and strip whitespace
        triggering_events = [event.strip() for event in group['Triggering Event'].values[0].split(',')]
        
        for triggering_event in triggering_events:
            G = nx.DiGraph()
            # Create a new graph for each triggering event
            for _, row in group.iterrows():
                # Only process rows for the current triggering event
                if triggering_event in row['Triggering Event']:
                    location = row['Location']
                    powers_invoked = row['Powers Invoked']
                    citation = row['Citation']

                    # Add nodes and edges to the graph
                    G.add_node(triggering_event)
                    G.add_node(location)
                    G.add_node(powers_invoked)
                    G.add_node(citation)

                    G.add_edge(triggering_event, location)
                    G.add_edge(location, powers_invoked)
                    G.add_edge(powers_invoked, citation)

            # Draw the graph if it has nodes
            if len(G.nodes) > 0:
                plt.figure(figsize=(8, 6))
                pos = nx.spring_layout(G)
                nx.draw(G, pos, with_labels=True, arrows=True, node_size=2000, node_color='lightblue', font_size=10)
                
                # Add agency label at the top
                plt.title(f"Agency: {agency}", fontsize=14, fontweight='bold')
                
                # Save the figure in the agency's folder
                output_folder = 'by-agency'
                image_path = os.path.join(output_folder, agency.replace(" ", ""), f"{triggering_event}.png")
                plt.savefig(image_path)
                plt.close()  # Close the figure to free memory

# Example usage for processing agency folders
parent_dir = 'by-agency'
for agency_folder in os.listdir(parent_dir):
    folder_path = os.path.join(parent_dir, agency_folder)
    
    if os.path.isdir(folder_path):
        csv_file_path = os.path.join(folder_path, 'data.csv')
        
        if os.path.exists(csv_file_path):
            df = pd.read_csv(csv_file_path)
            create_agency_graph(df, agency_folder)
        else:
            print(f"Warning: {csv_file_path} does not exist for {agency_folder}.")

print("Graph creation complete for all agencies.")
