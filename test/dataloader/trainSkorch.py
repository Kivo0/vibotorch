import sys
sys.path.append('../../database/')
sys.path.append('../../nn/')
sys.path.append('../../utils/')
import torch
import torchvision
import numpy as np
from dataloaderSegmentation import ImageFolderSegmentation
from torchvision.transforms import Compose, CenterCrop, Normalize
from torchvision.transforms import ToTensor, ToPILImage
from nn import SegNet
from torch import nn
import torch.nn.functional as F
import torch.optim as optim
from torch.autograd import Variable
from tqdm import tqdm
from metrics import evaluation
from compute_weight import WeightComputationMedian
from compute_weight import NormalizedWeightComputationMedian
import skorch
from skorch import NeuralNet


class NormalizeInput:
    def __call__(self, _input):
        img = np.array(_input, dtype=np.uint8)
        # img = img[:, :, ::-1]
        img = img.astype(np.float64)
        mean = np.array([122.67892, 104.00699, 116.66877])
        img -= mean
        img = img.astype(float) / 255.0
        # # NHWC -> NCHW
        # img = img.transpose(2, 0, 1)

        img = torch.from_numpy(img).float()
        return img


class load_label:
    """Class to convert PIL images to specific format of torch.Tensor."""
    def __call__(self, _input):
        # return torch.from_numpy(np.array(_input)).long().unsqueeze(0)
        return torch.from_numpy(np.array(_input, dtype=np.uint8)).long()


transform = Compose([
    CenterCrop(256),
    ToTensor(),
    # NormalizeInput(),
    # Normalize([105.0332, 108.4089, 110.3310], [69.9046, 72.6910, 72.1259]),
])
label_transform = Compose([
    CenterCrop(256),
    load_label(),
])


image_path = '/data/scene-segmentation/CamVid/train/*.png'

label_path = '/data/scene-segmentation/CamVid/trainannot/*.png'

var = ImageFolderSegmentation(images_path=image_path,
                              label_path=label_path,
                              transform=transform,
                              label_transform=label_transform)

trainloader = torch.utils.data.DataLoader(var, batch_size=10,
                                          shuffle=True, num_workers=10,
                                          pin_memory=True)

#
# image_path2 = '/data/scene-segmentation/CamVid/test/*.png'
#
# label_path2 = '/data/scene-segmentation/CamVid/testannot/*.png'
#
# var2 = ImageFolderSegmentation(images_path=image_path2,
#                                label_path=label_path2,
#                                transform=transform,
#                                label_transform=label_transform)
#
# valloader = torch.utils.data.DataLoader(var2, batch_size=10,
#                                         shuffle=False, num_workers=10,
#                                         pin_memory=True)
#

n_classes = 12

model = SegNet(in_channels=3, n_classes=n_classes)
model.init_encoder()
# model = torch.nn.DataParallel(model,
#                              device_ids=range(torch.cuda.device_count()))
model.cuda()
epochs = [200]
lrs = [0.001]

net = NeuralNet(
    module=model,
    criterion=torch.nn.CrossEntropyLoss,
)

model = Pipeline([
    ('my-features', get_features()),
    ('net', net),
])
model.fit(trainloader)

# saving
with open('testskorch.pkl', 'wb') as f:
    pickle.dump(model, f)
