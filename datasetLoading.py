import torch
from PIL import Image
from torch.utils.data import Dataset
import os
import tifffile as tiff
import numpy as np
class CustomData(Dataset):
    def __init__(self , root_data1 , root_data2 , transforms = None):
        super().__init__()
        # Store images path
        self.data1_path = root_data1
        self.data2_path = root_data2
        # Store the images names
        self.data1_images = os.listdir(root_data1)
        self.data2_images = os.listdir(root_data2)
        # Initial Transforms
        self.transforms = transforms
        # Store data lenght
        self.dataset_length = max(len(self.data1_images) , len(self.data2_images))
        # Store len data1
        self.len_data1 = len(self.data1_images)
        self.len_data2 = len(self.data2_images)
    def __len__(self):
        return self.dataset_length

    def __getitem__(self , index):
        # define images
        Name_image1 = self.data1_images[index % self.len_data1]
        Name_image2 = self.data2_images[index % self.len_data2]
        # define image path
        image1_path = os.path.join(self.data1_path , Name_image1)
        image2_path = os.path.join(self.data2_path , Name_image2)
        # Read images
        image1 = np.array(Image.open(image1_path))
        image2 = np.array(Image.open(image2_path))
        # image2 = tiff.imread(image2_path)
        # image2 = np.array([image2 , image2 , image2])
        # Apply transforms
        if self.transforms:
            image1 = self.transforms(image1)
            image2 = self.transforms(image2)
        
        return torch.unsqueeze(image1[0],axis=0) , image2 , str(Name_image1) , str(Name_image2)
        