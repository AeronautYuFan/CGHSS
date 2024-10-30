import pandas as pd

# Load the data from the CSV file
df = pd.read_csv('by-agency\POTUSorExecutiveOfficeofthePresidentoftheUnitedStates\data.csv')

# Assign each column to a variable
citation = df['Citation']
entity_empowered = df['Entity Empowered']
triggering_event = df['Triggering Event']
location = df['Location']

# Print the variables (optional)
print("Citation:", citation.tolist())
print("Entity Empowered:", entity_empowered.tolist())
print("Triggering Event:", triggering_event.tolist())
print("Location:", location.tolist())
