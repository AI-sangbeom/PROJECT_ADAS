# load libraries
import os
import numpy as np
from huggingface_hub import hf_hub_download
from ultralytics import YOLO
from supervision import Detections
from PIL import Image

# download model
model_path = hf_hub_download(repo_id="arnabdhar/YOLOv8-Face-Detection", filename="model.pt")

# load model
model = YOLO(model_path)

# inference
image_path = "./../../../data/Driver Drowsiness Dataset (DDD)/Augmentation/Drowsy/20241108_140133.png"
img = Image.open(image_path)
output = model(img)
results = Detections.from_ultralytics(output[0])

base_path = './../../../data/Driver Drowsiness Dataset (DDD)/'
Augdir = "Augmentation/Drowsy/"
dirs = os.listdir(os.path.join(base_path, Augdir))

# Drowsy
for path in dirs:
    image_path = os.path.join(base_path, Augdir, path)
    image = Image.open(image_path)

    model_path = hf_hub_download(repo_id="arnabdhar/YOLOv8-Face-Detection", filename="model.pt")
    detection_model = YOLO(model_path)
    output = model(image)
    results = Detections.from_ultralytics(output[0])
    bbox = results.xyxy[0].astype(int)+ np.array([-40, -70, 40, 30])
    x1, y1, x2, y2 = bbox
    image = image.crop((x1, y1, x2, y2))

    image.save(os.path.join(base_path, "Croped/Drowsy/", path))


# Non Drowsy
Augdir_Non = "Augmentation/Non Drowsy/"
dirs_Non = os.listdir(os.path.join(base_path, Augdir_Non))

for path in dirs_Non:
    image_path = os.path.join(base_path, Augdir_Non, path)
    image = Image.open(image_path)

    model_path = hf_hub_download(repo_id="arnabdhar/YOLOv8-Face-Detection", filename="model.pt")
    detection_model = YOLO(model_path)
    output = model(image)
    results = Detections.from_ultralytics(output[0])
    bbox = results.xyxy[0].astype(int)+ np.array([-40, -70, 40, 30])
    x1, y1, x2, y2 = bbox
    image = image.crop((x1, y1, x2, y2))

    image.save(os.path.join(base_path, "Croped/Non Drowsy/", path))