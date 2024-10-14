import pandas as pd
import json

# Load the data
df = pd.read_csv('data-cleaning/filteredUSCGdata.csv')

# Initialize a dictionary to store relationships
graph_data = {}

# Iterate through the rows
for index, row in df.iterrows():
    # Use .str.split() to handle the splitting better
    events = row['Triggering Event'].split(',') if pd.notna(row['Triggering Event']) else []
    powers = row['Powers Invoked'].split(',') if pd.notna(row['Powers Invoked']) else []
    citation = row['Citation'].strip() if pd.notna(row['Citation']) else ''
    
    for event in events:
        event = event.strip().strip('"')  # Remove extra whitespace and quotes
        if event not in graph_data:
            graph_data[event] = {}
        
        for power in powers:
            power = power.strip().strip('"')  # Remove extra whitespace and quotes
            if power not in graph_data[event]:
                graph_data[event][power] = []
            
            # Store citations
            graph_data[event][power].append(citation)

# Save graph_data to a JSON file for use in the web app
with open('graph_data.json', 'w') as f:
    json.dump(graph_data, f)
