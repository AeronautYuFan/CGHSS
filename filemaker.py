from packages.aflow.aflow import aflow

# Initialize the aflow instance with a CSV file
flow = aflow("DepartmentofAgriculture/data.csv")

# Render a flowchart based on a triggering event
flow.render_flow("Your Triggering Event")

# Optionally save the flowchart to a file
flow.save_flow("output_flowchart.png")