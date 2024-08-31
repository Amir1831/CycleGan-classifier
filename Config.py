import torch
from torchvision import transforms


DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

# Path to data folder
TRAIN_DIR_DATA1 = "./data/data1"
TRAIN_DIR_DATA2 = "./data/data3"

# if you want to load whole weights of cycle gan and their optimizers
LOAD_MODEL = False
PRE_TRAIN_WEIGHTS = "./Checkpoint/PCA_Clf_Vgg_0_"

# if you want to save weights of whole cycle gan model
SAVE_MODEL = True
SAVE_PATH = "./Checkpoint/PCA_Clf_vit_NoCmpile_"

# Where to save models output during training
OUTPUT_PATH = "./output/"

# If want to use classifier during training
USE_CLF = True
# Where to load classifier weights ?
name = "BestWeight_Part_19_Epoch_2_TrainLoss_0.01639417985006382_TestLoss_0.027976555515579093TrainAcc_0.9941451149425288_Testacc_0.9951171875"
CLF_PATH = "./TrackExp/" + name + ".pth"


# If you want to compile all the models
USE_COMPILE = False



BATCH_SIZE = 4
LEARNING_RATE = 2e-4
LAMBDA_IDENTITY = 1
LAMBDA_CYCLE = 10
LAMBDA_CLF = 50
NUM_WORKERS = 4
NUM_EPOCHS = 6
RESIZE_SIZE = 128


train_transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Resize((RESIZE_SIZE,RESIZE_SIZE)),
    transforms.Normalize(mean=[0.5] , std = [0.5])
    
])
