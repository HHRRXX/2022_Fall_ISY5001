from PIL import Image
import torch
from torchvision import transforms
# import transforms
from ResNet import resnet34
from torch.utils.data import DataLoader
import ResNet
import numpy as np
# Architecture

def predict(img):
    NUM_CLASSES = 5
    GRAYSCALE = False
    model = resnet34(NUM_CLASSES, GRAYSCALE)
    custom_transform = transforms.Compose([transforms.Resize(128),
                                       transforms.RandomCrop((120, 120)),
                                       transforms.ToTensor()])
    #img = Image.open('img/0.jpg')
    img = custom_transform(img)
    img = torch.reshape(img,(1,3,120,120))

    checkpoint=torch.load('models/model.pt')
    model.load_state_dict(checkpoint)
    model.eval()
    with torch.no_grad():
        a = model(img)
    x , y = a
    ans = x.argmax(1)
    ans = ans.numpy().tolist()
    return ans[0]
'''
custom_transform = transforms.Compose([transforms.Resize(128),
                                       transforms.RandomCrop((120, 120)),
                                       transforms.ToTensor()])
img = Image.open('img/0.jpg')
img = custom_transform(img)
print(img)
'''