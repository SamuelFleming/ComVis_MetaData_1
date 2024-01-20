import os
from export_class import MetaDataset

import tkinter as tk
from tkinter import filedialog


'''

This file is a runnable python file that showcases the operation of the roboflow export pickle class.
The user selects the robo flow export directory and it calls the constructor to the class which saves the pickle file.

This export is of a roboflow computer vision annotated dataset with three subdirectories:
    - train/, test/ and val/
each containing two subdirectories:
    - Images:   containing the image files
    - Labels:   contaning the .txt files of the corresponding polygon annotations.

'''

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

export_name = select_directory()

if export_name:  # Checks if a directory was selected
    absolute_path = os.path.abspath(export_name)  # Converts the selected path to an absolute path
else:
    # Fallback to default path if no folder is selected
    absolute_path = os.path.abspath(os.getcwd() + '/roboflow_export')

Dataset = MetaDataset(absolute_path)  # Initialize the MetaDataset with the absolute path

