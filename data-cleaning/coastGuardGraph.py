import pandas as pd
import networkx as nx
import plotly.graph_objects as go
import os

# Load the filtered CSV file
df = pd.read_csv('data-cleaning/filteredUSCGdata.csv')

# Create a directed graph
G = nx.DiGraph()

# Iterate through the DataFrame to add edges
for _, row in df.iterrows():
    # Split the triggering event by comma and strip spaces
    triggering_events = [event.strip() for event in row['Triggering Event'].split(',')]
    powers_invoked = [power.strip() for power in row['Powers Invoked'].split(',')]
    citation = row['Citation']
    
    # Add edges to the graph
    for triggering_event in triggering_events:
        for power in powers_invoked:
            G.add_edge(triggering_event, power)
            G.add_edge(power, citation)

# Get positions for the nodes
pos = nx.spring_layout(G)

# Create a Plotly figure
edge_x = []
edge_y = []
for edge in G.edges():
    x0, y0 = pos[edge[0]]
    x1, y1 = pos[edge[1]]
    edge_x.append(x0)
    edge_x.append(x1)
    edge_x.append(None)  # None to break the line
    edge_y.append(y0)
    edge_y.append(y1)
    edge_y.append(None)  # None to break the line

edge_trace = go.Scatter(
    x=edge_x, y=edge_y,
    line=dict(width=0.5, color='#888'),
    hoverinfo='none',
    mode='lines')

node_x = []
node_y = []
for node in G.nodes():
    x, y = pos[node]
    node_x.append(x)
    node_y.append(y)

node_trace = go.Scatter(
    x=node_x, y=node_y,
    mode='markers+text',
    hoverinfo='text',
    marker=dict(showscale=True, colorscale='YlGnBu', size=10, color=[]),
    text=[node for node in G.nodes()])

# Create the figure
fig = go.Figure(data=[edge_trace, node_trace],
                layout=go.Layout(
                    title='Interactive Directed Graph (Modified)',
                    titlefont=dict(size=16),
                    showlegend=False,
                    hovermode='closest',
                    margin=dict(b=0, l=0, r=0, t=40),
                    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                )

# Save the figure as an HTML file
script_dir = os.path.dirname(os.path.abspath(__file__))
html_file_path = os.path.join(script_dir, 'interactive_graph_modified.html')
fig.write_html(html_file_path)

# Optionally, show the figure in a web browser
fig.show()
