import os
import shutil
# file_utils.py

# Returns the name of the main CSV file. Update this as needed
def get_airtable():
    return "fullDataset.csv"

source_dir = 'C:/Users/Aeron/Documents/Repos/CGHSS/by-agency'
destination_dir = 'C:/Users/Aeron/Documents/Repos/CGHSS/duplicated_by_agency'
debug_file_path = 'C:/Users/Aeron/Documents/Repos/CGHSS/duplicated_by_agency/debug_no_images.txt'

# Function to duplicate folder structure and copy images
def duplicate_folder_structure_and_copy_images():
    # Open the debug file to log folder names with no images
    with open(debug_file_path, 'w') as debug_file:
        # Walk through the source directory (by-agency)
        for root, dirs, files in os.walk(source_dir):
            # Create the corresponding directory in the destination path
            relative_path = os.path.relpath(root, source_dir)  # Get the relative path of the folder
            destination_path = os.path.join(destination_dir, relative_path)  # Full destination path
            os.makedirs(destination_path, exist_ok=True)  # Create the folder if it doesn't exist

            # List to hold image files
            image_files = [file for file in files if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]

            # Copy over all the image files if any exist
            if image_files:
                for file in image_files:
                    source_file_path = os.path.join(root, file)
                    destination_file_path = os.path.join(destination_path, file)
                    shutil.copy2(source_file_path, destination_file_path)  # Copy the file preserving metadata
                    print(f"Copied {file} to {destination_file_path}")
            else:
                # If no image files are found, log the folder name to the debug file
                debug_file.write(f"{relative_path}\n")
                print(f"No images found in folder: {relative_path}")

    print(f"Folder structure duplicated and images copied. Debug information saved to {debug_file_path}.")

# Run the function
duplicate_folder_structure_and_copy_images()
