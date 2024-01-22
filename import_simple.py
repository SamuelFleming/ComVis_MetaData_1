import pickle
import json
import os
from export_class import MetaDataset

import tkinter as tk
from tkinter import filedialog

def load_metadata_from_pickle(file_path):
    """
    Load a MetaDataset object from a pickle file.

    Params:\n
        file_path: The path of the pickle file to be loaded.

    Return:\n
        Returns the MetaDataset object stored in the pickle file.
    """
    with open(file_path, 'rb') as input_file:
        dataset = pickle.load(input_file)
    return dataset

def get_directory_name():
    """
    Prompts the user to provide a directory name within the current working directory.
    Reprompts if the provided name does not correspond to an existing directory.
    """
    while True:
        directory_name = input("Please enter the name of a directory in the current working directory: ")
        full_path = os.path.join(os.getcwd(), directory_name)

        if os.path.isdir(full_path):
            print(f"Directory found: {full_path}")
            return directory_name
        else:
            print(f"The directory '{directory_name}' does not exist in the current working directory. Please try again.")


def select_directory():
    """
    Opens a file explorer window for the user to select a directory.
    Returns the path of the selected directory.
    """
    root = tk.Tk()
    root.withdraw()  # Hides the small tkinter window

    # Opens the directory selection dialog
    directory_path = filedialog.askdirectory()
    
    return directory_path

def select_pickle_file():
    """
    Opens a file explorer window for the user to select a pickle file.
    Returns the path of the selected file.
    """
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    # Set the options for opening a file
    options = {
        'defaultextension': '.pkl',
        'filetypes': [('pickle files', '*.pkl')],
        'title': 'Select a pickle file'
    }

    # Open the file selection dialog
    file_path = filedialog.askopenfilename(**options)

    if file_path:
        print(f"Pickle file selected: {file_path}")
        return file_path
    else:
        print("No file was selected.")
        return None

import_name = select_pickle_file()

if import_name:  # Checks if a directory was selected
    absolute_path = os.path.abspath(import_name)  # Converts the selected path to an absolute path
else:
    # Fallback to default path if no folder is selected
    absolute_path = os.path.abspath(os.getcwd() + '/roboflow_export')

loaded_dataset = load_metadata_from_pickle(absolute_path)

centers = loaded_dataset.database_import_ready()
#print(centers)
#print(len(centers))

# Saving the centers to a JSON file
with open('dataset_bridges.json', 'w') as file:
    json.dump(centers, file, indent=4)