import os
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Set non-interactive backend for rendering and saving images
from packages.aflow.aflow import aflow  # Import the aflow class

def process_triggering_events():
    base_folder = "C:/Users/Aeron/Documents/Repos/CGHSS/by-agency"

    for agency_folder in os.listdir(base_folder):
        agency_folder_path = os.path.join(base_folder, agency_folder)
        if not os.path.isdir(agency_folder_path):
            continue  # Skip non-folder entries

        csv_path = os.path.join(agency_folder_path, "data.csv")
        if not os.path.exists(csv_path):
            continue  # Skip if the CSV file doesn't exist

        print(f"Processing agency folder: {agency_folder}")
        print(f"CSV path: {csv_path}")

        try:
            df = pd.read_csv(csv_path)
        except Exception as e:
            print(f"Error reading CSV file in {agency_folder}: {e}")
            continue

        # Extract unique triggering events
        triggering_events = []
        for event in df["Triggering Event"].dropna():
            if event.startswith('"') and event.endswith('"'):
                # Handle multiple events in a quoted string
                event_list = event[1:-1].split(",")
                triggering_events.extend([e.strip() for e in event_list])
            else:
                triggering_events.append(event.strip())

        unique_events = set(triggering_events)

        # Debug: Save all events to a text file
        debug_path = os.path.join(agency_folder_path, "debug_triggering_events.txt")
        with open(debug_path, "w") as debug_file:
            debug_file.write(f"All Triggering Events in {agency_folder}:\n")
            debug_file.write("\n".join(triggering_events) + "\n\n")
            debug_file.write("Unique Triggering Events:\n")
            debug_file.write("\n".join(unique_events))
        print(f"Debug file saved to: {debug_path}")

        # Generate and save flow charts for each unique event
        for event in unique_events:
            try:
                print(f"Generating flow chart for event: {event}")
                flow = aflow(csv_path)  # Initialize aflow with the current CSV
                flow.render_flow(event)  # Generate flow diagram for the event

                # Save the diagram in the respective agency folder
                save_path = os.path.join(
                    agency_folder_path, f"flow_{event.replace(' ', '_')}.png"
                )
                flow.save_flow(save_path)  # Save flow chart to the file
                print(f"Saved flow chart for '{event}' to {save_path}")
            except Exception as e:
                print(f"Error generating flow chart for '{event}' in {agency_folder}: {e}")

if __name__ == "__main__":
    process_triggering_events()