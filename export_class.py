import os
import pickle


class MetaDataset:
    def __init__(self, path='none-specified'):
        '''
        Contrauctor for roboflow datatset class


        Params;\n
            path: the path of the export
        '''
        print("Class Constructed")

        if path == 'none-specified':
            print('[Non Path Specified]')
        else:
            self.path = os.path.abspath(path)
            self.get_split_paths(path)
            self.get_metadata()
            self.save_metadata_default()
        

    
    def save_metadata_default(self):
        if self.path == 'none-specified':
            print('[Non Path Specified]')
        else:
            self.save(self.path)

    def save(self, dir):
        #if save directory doesnt exist, create it (very rare case)
        if not os.path.exists(dir):
            os.makedirs(dir)
        path = os.path.join(dir, 'meta.pkl')
        self.abs = os.path.abspath(path) #absolute path of the instance storage
        #save self to the absolute path
        with open(self.abs, 'wb') as output_file:
            pickle.dump(self, output_file)
        
    def get_metadata(self):
        self.train_images = list_jpg_files(self.train_path_image)
        self.train_labels = list_txt_files_and_content(self.train_path_labels)

        self.test_images = list_jpg_files(self.test_path_image)
        self.test_labels = list_txt_files_and_content(self.test_path_labels)

        self.val_images = list_jpg_files(self.val_path_image)
        self.val_labels = list_txt_files_and_content(self.val_path_labels)

    def get_split_paths(self, path):
        images_dirname = 'images'
        labels_dirname = 'labels'
        self.train_path = os.path.join(path, 'train')
        self.train_path_image = os.path.join(self.train_path, images_dirname)
        self.train_path_labels = os.path.join(self.train_path, labels_dirname)

        self.test_path = os.path.join(path, 'test')
        self.test_path_image = os.path.join(self.test_path, images_dirname)
        self.test_path_labels = os.path.join(self.test_path, labels_dirname)

        self.val_path = os.path.join(path, 'valid')
        self.val_path_image = os.path.join(self.val_path, images_dirname)
        self.val_path_labels = os.path.join(self.val_path, labels_dirname)

def list_jpg_files(directory_path):
    """
    List all .jpg files in the given directory.

    :param directory_path: Absolute path to the directory
    :return: List of .jpg file names
    """
    jpg_files = []
    for file in os.listdir(directory_path):
        if file.lower().endswith('.jpg'):
            jpg_files.append(file)

    return jpg_files

def list_txt_files_and_content(directory_path):
    """
    List all .txt files and their contents in the given directory.

    :param directory_path: Absolute path to the directory
    :return: 2D list of file names and their contents
    """
    txt_files_data = []
    for file in os.listdir(directory_path):
        if file.lower().endswith('.txt'):
            file_path = os.path.join(directory_path, file)
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                txt_files_data.append([file, content])

    return txt_files_data