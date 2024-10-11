import pandas as pd

# Load the CSV file
df = pd.read_csv('NCDMPH_Data.csv')

# Filter the DataFrame for rows where 'Entity Empowered' contains the specified string
filtered_df = df[df['Entity Empowered'].str.contains("Department of Homeland Security - Coast Guard", na=False)]

# Save the filtered DataFrame to a new CSV file
filtered_df.to_csv('Filtered_NCDMPH_Data.csv', index=False)
