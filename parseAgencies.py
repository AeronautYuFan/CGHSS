import pandas as pd
import os
import time

start_time = time.time()

# Define the parent directory where the agency folders are located
parent_dir = 'by-agency'

# Iterate through each agency folder
for agency_folder in os.listdir(parent_dir):
    folder_path = os.path.join(parent_dir, agency_folder)
    
    # Check if it's a directory
    if os.path.isdir(folder_path):
        # Path to the data.csv file
        csv_file_path = os.path.join(folder_path, 'data.csv')
        
        # Check if the data.csv file exists
        if os.path.exists(csv_file_path):
            # Define the new Python script's path
            script_path = os.path.join(folder_path, 'load_data.py')
            
            # Create the new script
            with open(script_path, 'w') as file:
                file.write(f"""import pandas as pd

# Load the data from the CSV file
df = pd.read_csv('{csv_file_path}')

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
""")
            
            print(f"Created {script_path} to load data for {agency_folder}.")
        else:
            print(f"Warning: {csv_file_path} does not exist for {agency_folder}.")

# runtime calculator
end_time = time.time()
runtime = end_time - start_time
print(f"Total runtime: {runtime:.5f} seconds.")