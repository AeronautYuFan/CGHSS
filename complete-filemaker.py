import os
import pandas as pd
from packages.aflow.aflow import aflow  # Importing the aflow class

def list_all_triggering_events():
    # Set the base directory
    base_dir = 'C:/Users/Aeron/Documents/Repos/CGHSS/by-agency'

    # Loop through each agency folder
    for agency_folder in os.listdir(base_dir):
        folder_path = os.path.join(base_dir, agency_folder)
        csv_path = os.path.join(folder_path, 'data.csv')

        # Check if the path is a directory and contains the CSV file
        if os.path.isdir(folder_path) and os.path.isfile(csv_path):
            print(f"\nProcessing agency folder: {agency_folder}")

            # Load CSV file
            df = pd.read_csv(csv_path)

            # Initialize a set to collect unique triggering events
            unique_events = set()
            all_events = []  # To store all events for debugging

            # Loop through "Triggering Event" column and parse events
            for events in df['Triggering Event']:
                if pd.notna(events):
                    # Check for quoted events (indicating multiple events)
                    if events.startswith('"') and events.endswith('"'):
                        events_list = events[1:-1].split(',')  # Remove quotes and split
                    else:
                        events_list = [events]  # Single event

                    # Strip whitespace and add each event to the set and list
                    processed_events = [event.strip() for event in events_list]
                    unique_events.update(processed_events)
                    all_events.extend(processed_events)  # Collect all events for debugging

            # Debugging: Write all events to a text file in each agency folder
            # --------------------------------------------------------------
            debug_file_path = os.path.join(folder_path, 'debug_triggering_events.txt')
            with open(debug_file_path, 'w') as debug_file:
                debug_file.write(f"All Triggering Events in {agency_folder}:\n")
                debug_file.write("\n".join(all_events))
                debug_file.write("\n\nUnique Triggering Events:\n")
                debug_file.write("\n".join(unique_events))
            # --------------------------------------------------------------

            print(f"Unique Triggering Events for {agency_folder}: {unique_events}")

# Run the function to get triggering events for all agencies
list_all_triggering_events()
