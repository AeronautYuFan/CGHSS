import os
import pandas as pd
from packages.aflow.aflow import aflow

def extract_triggering_events(file_path):
    """
    Extract unique triggering events from the given CSV file.
    """
    # Load the data
    df = pd.read_csv(file_path)

    # Ensure 'Triggering Event' column exists
    if "Triggering Event" not in df.columns:
        return set()

    # Initialize a set to store unique triggering events
    unique_events = set()

    # Iterate through each row in the 'Triggering Event' column
    for events in df["Triggering Event"].dropna():
        # Normalize event strings (split by commas and strip whitespace)
        event_list = [event.strip() for event in events.split(",")]
        unique_events.update(event_list)  # Add each event individually to the set

    return unique_events

def generate_flow_charts(base_folder):
    """
    Iterate through agency folders, extract triggering events, and generate flow charts.
    """
    for agency_folder in os.listdir(base_folder):
        agency_folder_path = os.path.join(base_folder, agency_folder)

        # Ensure it's a directory
        if not os.path.isdir(agency_folder_path):
            continue

        csv_path = os.path.join(agency_folder_path, "data.csv")
        if not os.path.exists(csv_path):
            print(f"No data.csv found in {agency_folder}")
            continue

        print(f"Processing agency folder: {agency_folder}")
        print(f"CSV path: {csv_path}")

        # Extract unique triggering events
        unique_events = extract_triggering_events(csv_path)

        # --- Debugging Section: Save all triggering events to a text file ---
        debug_file_path = os.path.join(agency_folder_path, "debug_triggering_events.txt")
        with open(debug_file_path, "w") as debug_file:
            debug_file.write(f"All Triggering Events in {agency_folder}:\n")
            for events in pd.read_csv(csv_path)["Triggering Event"].dropna().unique():
                debug_file.write(f"{events}\n")
            debug_file.write("\nUnique Triggering Events:\n")
            for event in unique_events:
                debug_file.write(f"{event}\n")
        print(f"Debug file saved to: {debug_file_path}")
        # --- End Debugging Section ---

        # Generate a flow chart for each triggering event
        for event in unique_events:
            print(f"Generating flow chart for event: {event}")
            try:
                flow = aflow(csv_path)
                save_path = os.path.join(agency_folder_path, f"flow_{event.replace(' ', '_')}.png")
                flow.render_flow(event)  # Render the flow chart
                flow.save_flow(save_path)  # Save the flow chart in the agency folder
                print(f"Saved flow chart for '{event}' to {save_path}")
            except Exception as e:
                print(f"Error generating flow chart for '{event}': {e}")

# Define the base folder containing the agency subfolders
base_folder = "C:/Users/Aeron/Documents/Repos/CGHSS/by-agency"

# Generate flow charts for all unique triggering events
generate_flow_charts(base_folder)
