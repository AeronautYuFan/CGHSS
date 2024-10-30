import pandas as pd
import file_utils
import os
import time

start_time = time.time()

fullDataSet = pd.read_csv(file_utils.get_airtable())

cleaned_dataSet = fullDataSet[['Citation', 'Entity Empowered', 'Triggering Event', 'Location']]

cleaned_dataSet.to_csv('flowChartData.csv', index=False)

# Create a directory for agency-specific files
output_dir = 'by-agency'
os.makedirs(output_dir, exist_ok=True)

# Parse the "Entity Empowered" column and split by commas
agencies_processed = set()  # To keep track of processed agencies
for index, row in cleaned_dataSet.iterrows():
    agencies = row['Entity Empowered'].split(',')
    for agency in agencies:
        agency = agency.strip()  # Remove leading/trailing whitespace
        if agency not in agencies_processed:
            # Create a subfolder for the agency (without spaces)
            agency_folder = os.path.join(output_dir, agency.replace(" ", ""))
            os.makedirs(agency_folder, exist_ok=True)

            # Define the filtered DataFrame for the current agency
            filtered_data = cleaned_dataSet[cleaned_dataSet['Entity Empowered'].str.contains(agency, na=False)]

            # Save the filtered data to data.csv in the corresponding agency folder
            filtered_data.to_csv(os.path.join(agency_folder, 'data.csv'), index=False)

            # Add the agency to the processed set
            agencies_processed.add(agency)

# End time for runtime metric
end_time = time.time()
runtime = end_time - start_time

print(f"CSV files have been created for {len(agencies_processed)} agencies.")
print(f"Total runtime: {runtime:.2f} seconds.")
