# unet-pytorch
PyTorch implementation of a convolutional neural network (U-Net) for semantic segmentation of biomedical images.

## Overview
This repository contains a PyTorch implementation of the U-Net architecture for semantic segmentation tasks. The U-Net model is widely used in biomedical image segmentation and has shown great performance in various image segmentation challenges.

## Installation
You can install the U-Net model by cloning this repository and installing the required packages.

```bash
git clone https://github.com/giansimone/unet-pytorch.git
cd unet-pytorch
pip install .
```
We recommend using Python 3.11 or later and PyTorch 2.6 or later.

## Usage
To use the U-Net model, you can import the `UNet` class from the `unet.py` file and create an instance of the model. You can then train the model using your own dataset or use one of the provided datasets.

```python
import torch
from unet import UNet
# Create a U-Net model
model = UNet(in_channels=1, out_channels=1)
# Create a random input tensor
input_tensor = torch.randn(1, 1, 572, 572)
# Forward pass
output_tensor = model(input_tensor)
print(output_tensor.shape)  # Should be (1, 1, 388, 388)
```
## Training
To train the model, you can use the `train.py` script. You can specify the dataset, batch size, learning rate, and other hyperparameters in the script. The training loop will save the best model based on validation loss.

```bash
python train.py --dataset your_dataset_path --batch_size 16 --learning_rate 0.001 --num_epochs 50
```
## Evaluation
To evaluate the model, you can use the `evaluate.py` script. You can specify the path to the trained model and the dataset for evaluation. The evaluation script will compute various metrics such as Dice coefficient, IoU, and pixel accuracy.

```bash
python evaluate.py --model_path your_model_path --dataset your_dataset_path
```
## Inference
To perform inference using the trained model, you can use the `inference.py` script. You can specify the path to the trained model and the input image for inference. The script will save the predicted mask to the specified output directory.

```bash
python inference.py --model_path your_model_path --input_image your_input_image_path --output_dir your_output_dir
```
## Directory Structure
```
unet-pytorch/
├── unet.py                # U-Net model implementation
├── train.py               # Training script
├── evaluate.py            # Evaluation script
├── inference.py           # Inference script
├── dataset.py             # Dataset class
├── utils.py               # Utility functions
├── requirements.txt       # Required packages
├── config.py             # Configuration file
├── data/                  # Directory for datasets
│   ├── your_dataset/
│   │   ├── images/       # Directory for input images
│   │   ├── masks/        # Directory for ground truth masks
│   │   ├── train.txt     # File containing paths to training images
│   │   ├── val.txt       # File containing paths to validation images
│   │   └── test.txt      # File containing paths to test images
│   └── ...
├── logs/                 # Directory for training logs
├── models/               # Directory for saved models
├── outputs/              # Directory for output masks
└── README.md             # Project documentation
```
## Training and Evaluation Metrics
The training and evaluation scripts compute various metrics to assess the performance of the model. The following metrics are calculated during training and evaluation:
- **Dice Coefficient**: A measure of overlap between the predicted and ground truth masks. It ranges from 0 to 1, where 1 indicates perfect overlap.
- **Intersection over Union (IoU)**: A measure of the overlap between the predicted and ground truth masks. It is calculated as the intersection divided by the union of the two masks.
- **Pixel Accuracy**: The ratio of correctly predicted pixels to the total number of pixels in the image.
- **Mean Pixel Accuracy**: The average pixel accuracy across all classes.
- **Loss**: The loss function used during training. The default loss function is the binary cross-entropy loss, but you can customize it in the `train.py` script.
- **Learning Rate**: The learning rate used during training. You can adjust the learning rate in the `train.py` script.
- **Batch Size**: The number of samples processed before the model is updated. You can adjust the batch size in the `train.py` script.
- **Epochs**: The number of times the entire training dataset is passed through the model. You can adjust the number of epochs in the `train.py` script.
- **Early Stopping**: The training script includes early stopping functionality to prevent overfitting. You can specify the patience parameter in the `train.py` script, which determines how many epochs to wait before stopping training if no improvement is observed in the validation loss.
- **Learning Rate Scheduler**: The training script includes a learning rate scheduler to adjust the learning rate during training. You can specify the scheduler type and parameters in the `train.py` script.

## Customization
You can customize the U-Net model by modifying the `unet.py` file. You can change the number of input and output channels, the number of filters in each layer, and other hyperparameters. You can also add additional layers or modify the architecture to suit your needs.

## Datasets
The repository includes a few example datasets for testing the model. You can also use your own datasets by following the directory structure of the provided datasets. The dataset should contain images and corresponding masks for training and evaluation.
## Example Datasets
- [ISIC 2018](https://challenge.isic-archive.com/data.html)

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.