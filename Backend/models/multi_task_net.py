import torch
from torch import nn
import torch.nn.functional as F
import sys
sys.path.append('../')
from . import sub_backbone_new_resnet
from . import sub_class_loss_head
from . import sub_bbox_head


class MultiTastNet(nn.Module):
	def __init__(self, opt):
		self.opt = opt
		super(MultiTastNet, self).__init__()
		#backbone net
		if self.opt.backbone == 'new_resnet18':
			self.backbone_model = sub_backbone_new_resnet.resnet18(pretrained=False)
		if self.opt.backbone == 'old_resnet18':
			self.backbone_model = sub_backbone_old_resnet.resnet18(pretrained=False)
		elif self.opt.backbone == 'resnet18_finger':
			self.backbone_model = sub_backbone_old_resnet.resnet18_finger(use_se=opt.use_se)
		elif self.opt.backbone == 'resnet34':
			self.backbone_model = sub_backbone_new_resnet.resnet34(pretrained=False)
		elif self.opt.backbone == 'resnet50':
			self.backbone_model = sub_backbone_new_resnet.resnet50(pretrained=False)
		elif self.opt.backbone == 'resnet101':
			self.backbone_model = sub_backbone_new_resnet.resnet101(pretrained=False)
		elif self.opt.backbone == 'resnet152':
			self.backbone_model = sub_backbone_new_resnet.resnet152(pretrained=False)
		elif self.opt.backbone == 'resnext50_32x4d':
			self.backbone_model = sub_backbone_new_resnet.resnext50_32x4d(pretrained=False) 
		elif self.opt.backbone == 'resnext101_32x8d':
			self.backbone_model = sub_backbone_new_resnet.resnext101_32x8d(pretrained=False)

		# class head loss
		if self.opt.metric == 'add_margin':
			self.class_head = sub_class_loss_head.AddMarginProduct(in_channels = 512,
															    	out_channels = opt.num_classes, 
															    	s=64, 
															    	m=0.5)
		elif self.opt.metric == 'arc_margin':
			self.class_head = sub_class_loss_head.ArcMarginProduct(in_channels = 512, 
														        	out_channels = opt.num_classes, 
														        	s=64, 
														        	m=0.75,
														        	easy_margin=opt.easy_margin)
		elif self.opt.metric == 'sphere':
			self.class_head = sub_class_loss_head.SphereProduct(in_channels = 512, 
													        	out_channels = opt.num_classes, 
													        	m=4)
		elif self.opt.metric == 'layer':
			self.class_head = torch.nn.Linear(512, opt.num_classes)
			nn.init.xavier_normal_(self.class_head.weight)
			nn.init.constant_(self.class_head.bias, 0)
		
		# bbox head
		self.bbox_head = sub_bbox_head.BboxPredictor(in_channels = 1024, num_classes = 4)


	def forward(self, x, label = None):
		x = self.backbone_model(x)
		#bbox_out = self.bbox_head(x1)
		if self.training:
			x = self.class_head(x, label)
		return x