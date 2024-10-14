from flask import Flask, render_template
import csv
import pandas as pd

app = Flask(__name__)

@app.route('/')
def index():
    with open('data-cleaning/filteredUSCGdata.csv', 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        headers = next(reader)
        data = [row for row in reader]

    df = pd.DataFrame(data, columns=headers)

    # Initialize graph data storage
    graph_data = {}
    unique_nodes = set()
    unique_edges = set()

    for index, row in df.iterrows():
        events = row['Triggering Event'].split(',') if pd.notna(row['Triggering Event']) else []
        powers = list(csv.reader([row['Powers Invoked']], skipinitialspace=True))[0] if pd.notna(row['Powers Invoked']) else []
        citation = row['Citation'].strip() if pd.notna(row['Citation']) else ''

        for event in events:
            event = event.strip().strip('"')
            unique_nodes.add(event)
            if event not in graph_data:
                graph_data[event] = {}

            for power in powers:
                power = power.strip().strip('"')
                unique_nodes.add(power)

                # Create unique edges
                unique_edges.add((event, power))
                if power not in graph_data[event]:
                    graph_data[event][power] = []
                if citation not in graph_data[event][power]:
                    graph_data[event][power].append(citation)

    # Remove duplicates post-processing
    # Ensure each event has unique powers
    for event, powers in graph_data.items():
        unique_powers = {}
        for power, citations in powers.items():
            unique_powers[power] = list(set(citations))  # Remove duplicate citations for each power
        graph_data[event] = unique_powers

    # Filter nodes in graph_data based on unique_edges to remove disconnected or duplicate nodes
    filtered_graph_data = {
        event: powers for event, powers in graph_data.items() if any((event, power) in unique_edges for power in powers)
    }

    return render_template('index.html', graph_data=filtered_graph_data)

if __name__ == '__main__':
    app.run(debug=True)
