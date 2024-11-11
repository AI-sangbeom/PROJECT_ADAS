import os
import random 
import matplotlib.pyplot as plt
import timm
import torch 
import torchvision
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import DataLoader
from torchvision.transforms import transforms
from torchvision import  transforms, models
from PIL import Image 
from utils.functions import *
from utils.dataset import MyDataset

# Data Load
main_path = 'data/Driver Drowsiness Dataset (DDD)/Croped'

drowsy_paths = [os.path.join(main_path, 'Drowsy', p) for p in os.listdir(os.path.join(main_path, 'Drowsy'))]
non_drowsy_paths = [os.path.join(main_path, 'Non Drowsy', p) for p in os.listdir(os.path.join(main_path, 'Non Drowsy'))]

all_dirs = drowsy_paths +  non_drowsy_paths

random.shuffle(all_dirs)

total_size = len(all_dirs)
train_size = total_size
train_paths = all_dirs
random.shuffle(all_dirs)
len_train_paths = total_size


# GPU setting
if torch.cuda.is_available():  
    dev = "cuda:0" 
else:  
    dev = "cpu"  
    
device = torch.device(dev)  

train_transform = transforms.Compose([
    transforms.Resize((224, 224), interpolation=transforms.InterpolationMode.BICUBIC),
    transforms.RandomHorizontalFlip(),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5]), 
])

train_dataset = MyDataset(train_paths, transform=train_transform)
train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)


model = timm.create_model('resnet18', pretrained=True, num_classes=2).cuda()

# Define loss and optimizer

# Train the model
total_step = len(train_loader)
best = 100
learning_rate= 1e-6
num_epochs = 100
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(filter(lambda p: p.requires_grad, 
                                    model.parameters()), 
                             lr=learning_rate,
                             )

checkpoint_path = 'src/Detection/Drowsy/checkpoints'
if len(os.listdir(checkpoint_path)) > 0:
    load_best_model(model, os.path.join(checkpoint_path,'best_model.pth'))

for epoch in range(num_epochs):
    avg_train_loss = train_epoch(model, train_loader, criterion, optimizer,
                                  device, epoch, num_epochs, total_step)
    if best > avg_train_loss:
        best = avg_train_loss
        print(best)
        path=os.path.join(checkpoint_path, 'best_model.pth')
        torch.save(model.state_dict(), path)