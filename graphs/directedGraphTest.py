import csv
import networkx as nx
import matplotlib.pyplot as plt
import os

# Path to your CSV file
file_path = 'graphs/temp1.csv'

# Create an empty directed graph
G = nx.DiGraph()

# Open the CSV file and read the contents
with open(file_path, mode='r') as file:
    csv_reader = csv.DictReader(file)
    data = list(csv_reader)

    # Create dictionaries to group students by instrument, year, and school
    instrument_dict = {}
    year_dict = {}
    school_dict = {}
    
    for row in data:
        student = row['Student']
        instrument = row['Instrument'].strip()  # Remove any extra spaces
        year = row['Year'].strip()
        school = row['School'].strip()

        # Group by instrument
        if instrument not in instrument_dict:
            instrument_dict[instrument] = []
        instrument_dict[instrument].append(student)

        # Group by year
        if year not in year_dict:
            year_dict[year] = []
        year_dict[year].append(student)

        # Group by school
        if school not in school_dict:
            school_dict[school] = []
        school_dict[school].append(student)

    # Add directed edges based on instruments, years, and schools with colors
    edge_colors = []

    for instrument, students in instrument_dict.items():
        for i in range(len(students)):
            for j in range(len(students)):
                if i != j:
                    G.add_edge(students[i], students[j])
                    edge_colors.append('blue')  # Color for instrument connections

    for year, students in year_dict.items():
        for i in range(len(students)):
            for j in range(len(students)):
                if i != j:
                    G.add_edge(students[i], students[j])
                    edge_colors.append('green')  # Color for year connections

    for school, students in school_dict.items():
        for i in range(len(students)):
            for j in range(len(students)):
                if i != j:
                    G.add_edge(students[i], students[j])
                    edge_colors.append('orange')  # Color for school connections

# Optionally, print the nodes and edges
print("Nodes in the graph:", G.nodes())
print("Edges in the graph:", G.edges())

# Draw the directed graph with colored edges
plt.figure(figsize=(12, 8))
edges = G.edges()
nx.draw(G, with_labels=True, node_color='lightblue', node_size=2000, font_size=10, font_color='black', font_weight='bold', edge_color=edge_colors, arrows=True)
plt.title("Directed Graph of Students by Instrument, Year, and School with Colored Edges")

# Create the graphs directory if it doesn't exist
if not os.path.exists('graphs'):
    os.makedirs('graphs')

# Save the graph as a PNG file in the graphs folder
plt.savefig(os.path.join('graphs', "students_graph_directed.png"), format="png", bbox_inches='tight')

# Show the graph
plt.show()
