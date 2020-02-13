# -*- coding: utf-8 -*-
import torch.nn as nn
import torch
import sys
sys.path.append('../')
from Backend import config

class FocalLoss(nn.Module):

    def __init__(self, gamma= 0, eps= 1e-7):
        super(FocalLoss, self).__init__()
        self.gamma = gamma
        self.eps = eps
        self.ce = nn.CrossEntropyLoss(reduction='mean')

    def forward(self, input, target):
        logp = self.ce(input, target)
        p = torch.exp(-logp)
        loss = (1-p)**self.gamma*logp
        return loss.mean()

class BboxLoss(nn.Module):

    def __init__(self):
        super(BboxLoss, self).__init__()
        self.bbox_loss = nn.SmoothL1Loss(reduction='sum') #这里如果用mean的话是对每个x 或 y做的平均

    def forward(self, input, target):
        bbox_loss = self.bbox_loss(input, target)
        bbox_loss = bbox_loss / len(target.data.cpu().numpy()) # 这里使用batch size 做平均
        return bbox_loss

class Loss():
    def __init__(self, opt):
        super(Loss, self).__init__()
        if opt.class_loss == 'focal_loss':
            self.class_loss = FocalLoss(gamma=2)
        else:
            self.class_loss = torch.nn.CrossEntropyLoss(reduction='mean')
        self.bbox_loss = BboxLoss()

    def get_class_loss(self):
        return self.class_loss

    def get_bbox_loss(self):
        return self.bbox_loss



    



