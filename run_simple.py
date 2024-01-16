import os
import export_class


'''

This file is a runnable python file that showcases the operation of the roboflow export pickle class
by using the example roboflow export, directory 'roboflow_export' in the project directory.

This export is of a roboflow computer vision annotated dataset with three subdirectories:
    - train/, test/ and val/
each containing two subdirectories:
    - Images:   containing the image files
    - Labels:   contaning the .txt files of the corresponding polygon annotations.

'''


default_path = os.getcwd() + '/roboflow_export'
print(default_path)