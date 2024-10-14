from flask import Flask, render_template
import json
import pandas as pd

app = Flask(__name__)

@app.route('/')
def index():
    # Load and process the CSV file from the data-cleaning directory
    df = pd.read_csv('data-cleaning/filteredUSCGdata.csv')
    
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
                if power not in graph_data:
                    graph_data[power] = []  # Store citations directly under powers
                
                graph_data[power].append(citation)  # Store citations for each power

    return render_template('index.html', graph_data=graph_data)

if __name__ == '__main__':
    app.run(debug=True)
