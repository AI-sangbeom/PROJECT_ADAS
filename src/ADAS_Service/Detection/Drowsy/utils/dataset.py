from PIL import Image
from utils.functions import extract_class_name
from torch.utils.data import Dataset

class MyDataset(Dataset):
    def __init__(self, image_paths, transform=None):
        self.image_paths = image_paths
        self.transform = transform
        
    def __len__(self):
        return len(self.image_paths)

    def __getitem__(self, idx):
        img_path = self.image_paths[idx]
        image = Image.open(img_path)        
        label = extract_class_name(img_path)

        if self.transform:
            image = self.transform(image)
        
        label = 0 if label == 'Drowsy' else 1

        return image, label