from flask import Flask, render_template
import pandas as pd
import os

app = Flask(__name__, static_folder="static")  # Make sure Flask knows where to find static files

@app.route('/')
def index():
    # Load and process the CSV file
    df = pd.read_csv('data-cleaning/filteredUSCGdata.csv')  # Adjust path if needed

    # Prepare data for rendering
    graph_data = {}
    for index, row in df.iterrows():
        events = row['Triggering Event'].split(',') if pd.notna(row['Triggering Event']) else []
        powers = row['Powers Invoked'].split(',') if pd.notna(row['Powers Invoked']) else []
        citation = row['Citation'].strip() if pd.notna(row['Citation']) else ''
        
        for event in events:
            event = event.strip().strip('"')
            if event not in graph_data:
                graph_data[event] = {}
            
            for power in powers:
                power = power.strip().strip('"')
                if power not in graph_data[event]:
                    graph_data[event][power] = []
                graph_data[event][power].append(citation)

    return render_template('index.html', graph_data=graph_data)

if __name__ == '__main__':
    app.run(debug=True)
