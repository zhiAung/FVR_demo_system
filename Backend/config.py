import os
import copy
import warnings


class DefaultConfig():
    # 一、model
    img_url = '/home/hza/Finger-Vein-Identification-System/Backend/database/imgs'
    ver_img_url = '/home/hza/Finger-Vein-Identification-System/Backend/database/imgs/ver'
    iden_img_url = '/home/hza/Finger-Vein-Identification-System/Backend/database/imgs/iden'
    model_parameters = "/home/hza/deeplearning_project/FingerVeinRecognition/checkpoints/原图-数据增强-Arcface_0.0029_1205_12:12:58.pkl"
    device_ids = [0, 1]
    multi_gpus = True
    # 数据库
    host = "10.108.246.53"
    port = 6379


    
    backbone = 'new_resnet18'
    classify = 'softmax'
    num_classes = 360
    metric = 'arc_margin'
    easy_margin = True
    use_se = False
    multi_task = False
    #loss = 'focal_loss'
    class_loss = 'loss'
    display = True
    optimizer = 'sgd'
    num_workers = 8  # how many workers for loading data
    debug_file = '/tmp/debug'  # if os.path.exists(debug_file): enter ipdb
    result_file = 'result.csv'
    #lr = 1e-1  # initial learning rate
    lr = 0.001
    lr_step = 5
    lr_decay = 0.95  # when val_loss increase, lr = lr*lr_decayS
    weight_decay = 5e-4


    # 二、train
    # 目前的配置参数是目前调出来最好的
    finetune = True
    checkpoints_path = '/home/hza/deeplearning_project/FingerVeinRecognition/checkpoints/'
    #
    model_pretrained_parameters = '/home/hza/.cache/torch/checkpoints/resnet18-5c106cde.pth'
    #model_pretrained_parameters = '/home/hza/deeplearning_project/FingerVeinRecognition/checkpoints/'\
    #'new_resnet18_336_0.5706_0629_08:47:32.pkl'
    train_dataset = "/home/hza/deeplearning_project/FingerVeinRecognition/datasets/data/MMCBNU_6000/ROI/train_360"
    train_bbox_label = '/home/hza/deeplearning_project/FingerVeinRecognition/datasets/data/MMCBNU_6000/Raw/train_bbox_labels.txt'  # 训练集序列化文件 2_train_bmp_aug.pickle \2_train_bmp.pickle
    train_batch_size = 32
    print_freq = 100  # print info every N batch
    max_epoch = 30
    
    # 三、val(test)
    val_dataset = "/home/hza/deeplearning_project/FingerVeinRecognition/datasets/data/MMCBNU_6000/ROI/val_60" # 测试的时候所使用的序列化文件
    val_img_pairs = '/home/hza/deeplearning_project/FingerVeinRecognition/datasets/data/MMCBNU_6000/ROI/val_img_pair_2700_3000.txt'
    
    test_model_pretrain_parameter = "/home/hza/deeplearning_project/FingerVeinRecognition/checkpoints/" \
     "没有数据增强-Arcface_0.0051_1203_14:54:13.pkl"
    # 验证集（测试集）的数据文件，也是测试代码里面获取图像名字列表，以及制作图像对的来源
    test_dataset = '/home/hza/deeplearning_project/FingerVeinRecognition/datasets/data/MMCBNU_6000/ROI/test_180'
    test_img_pairs = '/home/hza/deeplearning_project/FingerVeinRecognition/datasets/data/MMCBNU_6000/ROI/test_img_pair_8100_9000.txt'
    test_batch_size = 32

    def parse(self, kwargs):
        for k, v in kwargs.iteritems():
            if not hasattr(self,k):
                warnings.warn("Warning: opt has not attribut %s" %k)
        setattr(self, k, v)
        print('user config:')
        for k, v in self.__class__.__dict__.iteritems():
            if not k.startswith("__"):
                print(k, getattr(self, k))


opt = DefaultConfig()