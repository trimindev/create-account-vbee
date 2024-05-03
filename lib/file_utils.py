import os, shutil


def count_files_in_folder(folder_path):
    if not os.path.exists(folder_path):
        raise FileNotFoundError(f"The folder path '{folder_path}' does not exist.")

    file_count = 0

    for _, _, files in os.walk(folder_path):
        file_count += len(files)

    return file_count


def delete_file(file_path):
    try:
        os.remove(file_path)
        print(f"File '{file_path}' deleted successfully.")
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
    except Exception as e:
        print(f"Error occurred while deleting file '{file_path}': {e}")


def get_files_with_extension_in_folder(extension, folder_path):
    if not os.path.exists(folder_path):
        raise FileNotFoundError(f"The folder path '{folder_path}' does not exist.")

    found_files = []

    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith(extension):
                found_files.append(os.path.join(root, file))

    return found_files


def create_new_folder_inside(folder_path, new_folder_name):
    new_folder_path = os.path.join(folder_path, new_folder_name)
    if not os.path.exists(new_folder_path):
        os.makedirs(new_folder_path)
    return new_folder_path


def generate_edited_file_name(file_path, text):
    """
    Generate the edited file name based on the given file path and additional text.
    """
    base_name = os.path.basename(file_path)
    edited_file_name = f"{os.path.splitext(base_name)[0]}_{text}"
    return edited_file_name


def copy_and_rename_folder(src_path: str, dest_path: str, new_folder_name: str):
    new_folder_path = os.path.join(dest_path, new_folder_name)
    try:
        # Copy the entire folder to the destination path
        shutil.copytree(src_path, new_folder_path)

        os.rename(os.path.join(dest_path, os.path.basename(src_path)), new_folder_path)

        print(f"Folder copied and renamed successfully to: {new_folder_path}")

    except OSError as e:
        # print(f"Error: {e}")
        pass

    return new_folder_path
