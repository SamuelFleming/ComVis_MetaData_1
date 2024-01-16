import os
from export_class import MetaDataset

import tkinter as tk
from tkinter import filedialog


'''

This file is a runnable python file that showcases the operation of the roboflow export pickle class
by using the example roboflow export, directory 'roboflow_export' in the project directory.

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



# export_name = get_directory_name() #here the cpde promtps the user to enter the name of the export from the cwd
# export_name = select_directory() # this opens a dialog box using tkinter that allows the user to specify which roboflow export they woudl like to select.



export_name = 'roboflow_export'#here is where the name of the export directory is specified

default_path = os.getcwd() + '/roboflow_export'

Dataset = MetaDataset(default_path)
