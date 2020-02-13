import torch
from torch import nn
import torch.nn.functional as F

class BboxPredictor(nn.Module):
    """
    Standard classification + bounding box regression layers
    for Fast R-CNN.

    Arguments:
        in_channels (int): number of input channels
        num_classes (int): number of output classes (including background)
    """

    def __init__(self, in_channels, num_classes):
        super(BboxPredictor, self).__init__()
        #self.bbox_fc1 = nn.Linear(in_channels, 512)
        self.bbox_fc2 = nn.Linear(1024, num_classes)
        for m in self.modules():
            if isinstance(m, nn.Linear):
                nn.init.xavier_normal_(m.weight)
                nn.init.constant_(m.bias, 0)

    def forward(self, x):
        #x =  self.bbox_fc1(x)
        bbox_deltas = self.bbox_fc2(x)
        return bbox_deltas