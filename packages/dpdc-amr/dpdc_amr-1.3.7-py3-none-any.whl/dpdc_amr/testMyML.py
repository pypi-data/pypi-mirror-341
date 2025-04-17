from PIL import Image
import os
from ultralytics import YOLO

current_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(current_dir, 'weights/best_cls.pt')



def getModel():
    model = YOLO(model_path)
    return model




def examine(model, imgFile):
    class_names = ['IllegibleMeter', 'Calculator', 'Meter', 'Non-Meter']

    # Load model to GPU if available
    device = 'cuda' if model.device.type == 'cuda' else 'cpu'
    model.to(device)

    # Load image
    img = Image.open(imgFile)

    # Run prediction on GPU
    results = model(img)

    pred = results[0].probs.top1
    confidence = results[0].probs.top1conf.item()

    return  class_names[pred]