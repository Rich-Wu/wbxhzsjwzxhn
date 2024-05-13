import os

def delete_files_in_folder(folder_path):
    # Iterate over all files in the folder
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        try:
            if os.path.isfile(file_path):
                # Remove the file
                os.remove(file_path)
                print(f"Deleted: {file_path}")
            else:
                print(f"Ignoring: {file_path} (not a file)")
        except Exception as e:
            print(f"Error deleting {file_path}: {e}")

output_folder = "/".join([os.getcwd(), 'out'])
delete_files_in_folder(output_folder)