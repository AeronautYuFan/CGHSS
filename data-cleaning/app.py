from flask import Flask, render_template
import csv
import pandas as pd

app = Flask(__name__)

@app.route('/')
def index():
    # Use csv.reader to load CSV with special character handling for quotes
    with open('data-cleaning/filteredUSCGdata.csv', 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        headers = next(reader)
        data = [row for row in reader]

    # Convert to DataFrame
    df = pd.DataFrame(data, columns=headers)

    graph_data = {}
    for index, row in df.iterrows():
        # Split Triggering Events as usual
        events = row['Triggering Event'].split(',') if pd.notna(row['Triggering Event']) else []
        
        # Power Invoked Parsing: Retain full quoted strings if they exist
        powers = list(csv.reader([row['Powers Invoked']], skipinitialspace=True))[0] if pd.notna(row['Powers Invoked']) else []
        
        citation = row['Citation'].strip() if pd.notna(row['Citation']) else ''
        
        # Organize data into graph_data structure
        for event in events:
            event = event.strip().strip('"')
            if event not in graph_data:
                graph_data[event] = {}
            
            for power in powers:
                power = power.strip('"')  # Remove extra quotes from each power
                if power not in graph_data[event]:
                    graph_data[event][power] = []  # Initialize citation list
                graph_data[event][power].append(citation)

    return render_template('index.html', graph_data=graph_data)

if __name__ == '__main__':
    app.run(debug=True)
