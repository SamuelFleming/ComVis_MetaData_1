import os
import pickle


class MetaDataset:
    def __init__(self, path='none-specified', img_length = 1280, img_height = 1280):
        '''
        Contrauctor for roboflow datatset class


        Params;\n
            path: the path of the export
        '''
        print("Class Constructed")
        #Have the empty ones here
        self.img_length = img_length
        self.img_height = img_height


        if path == 'none-specified':
            print('[Non Path Specified]')
        else:
            self.path = os.path.abspath(path)
            self.name = os.path.basename(path)
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
        path = os.path.join(dir, self.name + '_meta.pkl')
        self.abs = os.path.abspath(path) #absolute path of the instance storage
        #save self to the absolute path
        with open(self.abs, 'wb') as output_file:
            pickle.dump(self, output_file)
        
    def get_metadata(self):
         
        # self.train_images, self.train_labels = list_txt_files_and_content(self.train_path_labels)
 
        # self.test_images, self.test_labels = list_txt_files_and_content(self.test_path_labels)

        # self.val_images, self.val_labels = list_txt_files_and_content(self.val_path_labels)

        self.train_labels = get_content(self.train_path_labels)
 
        self.test_labels = get_content(self.test_path_labels)

        self.val_labels = get_content(self.val_path_labels)

    def get_split_paths(self, path):
        '''
        Gets the directory paths of the different splits in the dataset from the original path
        '''
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
    
    def collect_all_annotation_centers(self):
        """
        Collects all the center points of the annotations in train, test, and val sets.
        """
        all_centers = []

        for label_set in [self.train_labels, self.test_labels, self.val_labels]:
            for sample in label_set:
                annotations = sample.get_annotations()
                for annotation in annotations:
                    all_centers.append(annotation.center)

        return all_centers
    
    def collect_all_annotation_centers_coords(self):
        """
        Collects all the center points of the annotations in train, test, and val sets.
        """
        all_centers = []

        for label_set in [self.train_labels, self.test_labels, self.val_labels]:
            for sample in label_set:
                annotations = sample.get_annotations()
                for annotation in annotations:
                    all_centers.append(annotation.geo_center)

        return all_centers




def list_txt_files_and_content(directory_path):
    """
    List all .txt files and their contents in the given directory.

    Params:\n
    directory_path: Absolute path to the directory\n

    Return:
    txt_files_data: 2D list of file names and their contents
    """

    txt_files_data = []
    for txt_file in os.listdir(directory_path):
        if txt_file.lower().endswith('.txt'):

            txt_file_path = os.path.join(directory_path, txt_file)


            with open(txt_file_path, 'r', encoding='utf-8') as f:
                content = f.read()

                '''
                Insert logic to derive and convert points here
                '''

                txt_files_data.append([txt_file, content])


    return txt_files_data



def get_content(directory_path):
    """
    List all .txt files and their contents in the given directory.

    Params:\n
    directory_path: Absolute path to the directory\n

    Return:
    txt_files_data: 2D list of file names and their contents
    """

    samples = []
    for txt_file in os.listdir(directory_path):
        if txt_file.lower().endswith('.txt'):

            txt_file_path = os.path.join(directory_path, txt_file)
            samples.append(Sample(txt_file_path))

        
    return samples



class Sample:
    def __init__(self, txt_file_path, length = 1280, height = 1280):
        print('\n sample constructed\n')
        self.pixel_len = length
        self.pixel_wid = height
        self.label_path = txt_file_path
        self.image_path = self.get_image_path_from_annotation()
        self.coords = self.get_coords(self.get_image_name())
    
    def get_annotations(self):
        annotations = []
        txt_file_path = self.label_path
        with open(txt_file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    annotations.append(Annotation(line, self.pixel_len, self.pixel_wid, self.coords))
        return annotations



    def get_image_name(self):
        """
        Extracts the original image name from the given absolute path.

        Params:\n
        image_path: Absolute path to the image file\n

        Return:
        original_image_name: Original name of the image file
        """
        # Extract the base name from the absolute path
        base_name = os.path.basename(self.image_path)

        # Split the base name at '.jpg' and take the first part
        # This is necessary to remove additional suffixes added by roboflow or other tools
        original_image_name = base_name.split('.jpg')[0] + '.jpg'

        return original_image_name

    def get_coords(self, image_name):
        """
        Take a filename of an image sample, replace hyphens with dots only if they are
        not at the start or not prefixed by an underscore, and return its identifying coordinates.
        
        Splits the image name at its underscores, removes the extension, 
        and returns the four values split by the underscores.

        Params:
        image_name: Name of the image file

        Return:
        values: Four values split by the underscores (array of size four)
        """
        # Replace hyphens with dots except if at the start or prefixed by an underscore
        modified_name = ''
        for i, char in enumerate(image_name):
            if char == '-' and i != 0 and image_name[i - 1] != '_':
                modified_name += '.'
            else:
                modified_name += char

        # Remove the file extension
        name_without_extension = modified_name.rsplit('.', 1)[0]

        # Split at underscores and take the first four values
        values = name_without_extension.split('_')[:4]
        print(values)

        return values


        

    def get_image_path_from_annotation(self):
        """
        Given the path of a .txt annotation file, returns the absolute path of the corresponding .jpg image file.

        Params:\n
        annotation_path: Absolute path to the annotation (.txt) file\n

        Return:
        image_path: Absolute path to the corresponding image (.jpg) file
        """
        annotation_path = self.label_path
        # Base directory for images and labels (assuming they share the same root)
        base_directory = os.path.dirname(os.path.dirname(annotation_path))

        # Extract relative path of the txt file from its directory
        relative_annotation_path = os.path.relpath(annotation_path, base_directory)

        # Construct the relative path for the image
        relative_image_path = relative_annotation_path.replace('labels', 'images').replace('.txt', '.jpg')

        # Construct the absolute path for the image
        image_path = os.path.join(base_directory, relative_image_path)

        return image_path


class Annotation:
    def __init__(self, data, sample_l, sample_h, sample_coords):
        self.class_id, coords = self.process_line(data)
        self.pixel_coords = self.convert_points_to_pixel(coords, sample_l, sample_h)
        self.center = self.get_center_polygon()
        self.geo_center = self.convert_to_geo_coordinates(self.center, sample_coords)

    @staticmethod
    def process_line(line):
        """
        Process the line and return the parsed data.

        Assuming the format is: class_id x1 y1 x2 y2 ... xn yn x1 y1
        """
        data = line.strip().split()
        class_id = int(data[0])
        coords = [float(coord) for coord in data[1:]]
        return class_id, coords
        
    @staticmethod
    def convert_to_geo_coordinates(center, sample_coords):
        """
        Convert the center pixel coordinates to latitude and longitude.

        :param center: Tuple of (x, y) center pixel coordinates.
        :param sample_coords: Tuple of (lat_min, lon_min, lat_max, lon_max).
        :return: Tuple of (latitude, longitude).
        """
        image_size = 1280  # Assuming a constant image size - adjust if needed
        x, y = center

        # Ensure the coordinates are floats
        lat_min, lon_min, lat_max, lon_max = map(float, sample_coords)

        delta_lat = abs(lat_max - lat_min)
        delta_lon = abs(lon_max - lon_min)

        px_x = x / image_size
        px_y = y / image_size

        lat_coords = lat_max - delta_lat * px_y
        lon_coords = lon_min + delta_lon * px_x

        return lat_coords, lon_coords

    def convert_points_to_pixel(self, coords, img_length, img_height):
        """
        Convert normalized coordinates to pixel coordinates.

        :param coords: List of normalized coordinates (x, y pairs).
        :param img_width: Width of the image in pixels.
        :param img_height: Height of the image in pixels.
        :return: List of pixel coordinates.
        """
        pixel_coords = []
        for i in range(0, len(coords), 2):
            x_normalized, y_normalized = coords[i], coords[i + 1]
            x_pixel = round(x_normalized * img_length)
            y_pixel = round(y_normalized * img_height)
            pixel_coords.extend([x_pixel, y_pixel])
        return pixel_coords

    def get_center_polygon(self):
        '''
        Take a set of pixel coordinates that make a shape and return the center of that shape by finding the 
        centroid of a polygon. Dependent on the pixel coordinates being a polygon.
        '''
        pixel_coords = self.pixel_coords
        x_sum = 0
        y_sum = 0
        n = len(pixel_coords) // 2  # Number of points

        for i in range(0, len(pixel_coords), 2):
            x_sum += pixel_coords[i]
            y_sum += pixel_coords[i + 1]

        centroid_x = round(x_sum / n)
        centroid_y = round(y_sum / n)
        center = (centroid_x, centroid_y)

        return center