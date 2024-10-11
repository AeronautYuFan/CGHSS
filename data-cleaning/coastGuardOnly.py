import pandas as pd
import os
# from ..file_utils import *


# Load the CSV file
# df = pd.read_csv(get_csv_filenames())
df = pd.read_csv("NCDMPH_Data.csv")

# Filter the DataFrame for rows where 'Entity Empowered' contains the specified string
filtered_df = df[df['Entity Empowered'].str.contains("Department of Homeland Security - Coast Guard", na=False)]

# Get the directory of the current script
script_directory = os.path.dirname(os.path.abspath(__file__))

# Define the path for the new CSV file
new_file_path = os.path.join(script_directory, 'data-coastguard-only.csv')

# Save the filtered DataFrame to the new CSV file
filtered_df.to_csv(new_file_path, index=False)

print(f"Filtered data saved to: {new_file_path}")
