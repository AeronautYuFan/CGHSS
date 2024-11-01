import os

# Define the parent directory where the agency folders are located
parent_dir = 'by-agency'

# Initialize a counter for deleted files
deleted_count = 0

# Iterate through each agency folder
for agency_folder in os.listdir(parent_dir):
    folder_path = os.path.join(parent_dir, agency_folder)

    # Check if it's a directory
    if os.path.isdir(folder_path):
        # Iterate through files in the agency folder
        for filename in os.listdir(folder_path):
            if filename.endswith('.png'):
                file_path = os.path.join(folder_path, filename)
                os.remove(file_path)  # Delete the .png file
                print(f"Deleted: {file_path}")
                deleted_count += 1  # Increment the counter

# Print the total number of deleted files
print(f"Total .png files deleted: {deleted_count}")
