import pandas as pd
import os
import file_utils_old


# Load the CSV file
# df = pd.read_csv(get_csv_filenames())
df = pd.read_csv(file_utils_old.get_airtable())

# Filter the DataFrame for rows where 'Entity Empowered' contains the specified string
filtered_df = df[df['Entity Empowered'].str.contains("Department of Homeland Security - Coast Guard", na=False)]

# Get the directory of the current script
script_directory = os.path.dirname(os.path.abspath(__file__))

# Define the path for the new CSV file
new_file_path = os.path.join(script_directory, 'data-coastguard-only.csv')

# Save the filtered DataFrame to the new CSV file
filtered_df.to_csv(new_file_path, index=False)

print(f"Filtered data saved to: {new_file_path}")

##########################################

dCG = pd.read_csv(new_file_path)

new_df = dCG[['Citation', 'Triggering Event', 'Location', 'Powers Invoked']]

# Get the current script directory
script_dir = os.path.dirname(os.path.abspath(__file__))

# Define the path for the new CSV file
new_file_path = os.path.join(script_dir, 'filteredUSCGdata.csv')

# Save the new DataFrame to the specified path
new_df.to_csv(new_file_path, index=False)
