import pandas as pd

# Load the data
df = pd.read_csv('filteredUSCGdata.csv')

# Initialize a dictionary to store relationships
graph_data = {}

# Iterate through the rows
for index, row in df.iterrows():
    events = row['Triggering Event'].split(',')
    powers = row['Powers Invoked'].split(',')
    citation = row['Citation']
    
    for event in events:
        event = event.strip()
        
        if event not in graph_data:
            graph_data[event] = {}
        
        for power in powers:
            power = power.strip()
            
            if power not in graph_data[event]:
                graph_data[event][power] = []
            
            # Store citations
            graph_data[event][power].append(citation)

# Save graph_data to a JSON file for use in the web app
import json
with open('graph_data.json', 'w') as f:
    json.dump(graph_data, f)
