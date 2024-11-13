import os
import pandas as pd
from aflow import aflow  # Import the aflow class from aflow.py

# Print the current working directory
print("Current working directory:", os.getcwd())

# Initialize the aflow class with the CSV file path
flow = aflow("DepartmentofAgriculture/data.csv")

# Specify a valid save path
save_path = 'C:/Users/Aeron/Documents/Repos/CGHSS/DepartmentofAgriculture/flow_diagram.png'

# Verify save path
print("Saving to:", save_path)

# Render and save the flow diagram
flow.render_flow('Potential Public Health Emergency', save_path=save_path)

