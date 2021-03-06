"""Hyper Class to define a Neural Network composed of Layers

This module contains methods to create different Neural Networks

The module structure is the following:

- The ``NeuralNetwork`` abstract base class is the main definition of
  the necessary functions in order to properly define a NeuralNetwork


---------------------------------------------------------------------
                              SEGNET
            SegNet: A Deep Convolutional Encoder-Decoder
                Architecture for Image Segmentation

Vijay Badrinarayanan, Alex Kendall, Roberto Cipolla, Senior Member, IEEE

- ``SegNet`` definition of the SegNet Architecture
"""
from layer import *
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.nn as nn
from torch import autograd, optim
from torchvision import models


class NeuralNetwork(nn.Module):
    """Abstract Base Class to ensure the optimal quantity of functions."""
    def __init__(self, in_channels, n_classes):
        super(NeuralNetwork, self).__init__()
        pass

    def forward(self, inputs):
        pass


"""SEGNET"""


class SegNet(nn.Module):
    """Derived Class to define a Segnet Architecture of NN

    Attributes
    ----------
    in_channels : int
        The input size of the network.

    n_classes : int
        The output size of the network.

    References
    ----------
    SegNet: A Deep Convolutional Encoder-Decoder Architecture
    for Image Segmentation
    Vijay Badrinarayanan, Alex Kendall, Roberto Cipolla, Senior Member, IEEE,
    """
    def __init__(self, in_channels=3, n_classes=21):
        """Sequential Instanciation of the different Layers"""
        super(SegNet, self).__init__()

        self.layer_1 = SegnetLayer_Encoder(in_channels, 64, 2)
        self.layer_2 = SegnetLayer_Encoder(64, 128, 2)
        self.layer_3 = SegnetLayer_Encoder(128, 256, 3)
        self.layer_4 = SegnetLayer_Encoder(256, 512, 3)
        self.layer_5 = SegnetLayer_Encoder(512, 512, 3)

        self.layer_6 = SegnetLayer_Decoder(512, 512, 3)
        self.layer_7 = SegnetLayer_Decoder(512, 256, 3)
        self.layer_8 = SegnetLayer_Decoder(256, 128, 3)
        self.layer_9 = SegnetLayer_Decoder(128, 64, 2)
        self.layer_10 = SegnetLayer_Decoder(64, n_classes, 2)

    def forward(self, inputs):
        """Sequential Computation, see nn.Module.forward methods PyTorch"""

        down1, indices_1, unpool_shape1 = self.layer_1(inputs=inputs,
                                                       layer_size=2)
        down2, indices_2, unpool_shape2 = self.layer_2(inputs=down1,
                                                       layer_size=2)
        down3, indices_3, unpool_shape3 = self.layer_3(inputs=down2,
                                                       layer_size=3)
        down4, indices_4, unpool_shape4 = self.layer_4(inputs=down3,
                                                       layer_size=3)
        down5, indices_5, unpool_shape5 = self.layer_5(inputs=down4,
                                                       layer_size=3)

        up5 = self.layer_6(inputs=down5, indices=indices_5,
                           output_shape=unpool_shape5, layer_size=3)
        up4 = self.layer_7(inputs=up5, indices=indices_4,
                           output_shape=unpool_shape4, layer_size=3)
        up3 = self.layer_8(inputs=up4, indices=indices_3,
                           output_shape=unpool_shape3, layer_size=3)
        up2 = self.layer_9(inputs=up3, indices=indices_2,
                           output_shape=unpool_shape2, layer_size=2)
        output = self.layer_10(inputs=up2, indices=indices_1,
                               output_shape=unpool_shape1, layer_size=2)

        return output

    def init_encoder(self):
        """Initialize encoder with VGG16 weights for Relu and Conv"""

        vgg = models.vgg16(pretrained=True)

        blocks = [self.layer_1,
                  self.layer_2,
                  self.layer_3,
                  self.layer_4,
                  self.layer_5]

        ranges = [[0, 4], [5, 9], [10, 16], [17, 23], [24, 29]]
        features = list(vgg.features.children())

        vgg_layers = []
        for _layer in features:
            if isinstance(_layer, nn.Conv2d):
                vgg_layers.append(_layer)

        merged_layers = []
        for idx, conv_block in enumerate(blocks):
            if idx < 2:
                units = [conv_block.conv1.cbr_unit,
                         conv_block.conv2.cbr_unit]
            else:
                units = [conv_block.conv1.cbr_unit,
                         conv_block.conv2.cbr_unit,
                         conv_block.conv3.cbr_unit]
            for _unit in units:
                for _layer in _unit:
                    if isinstance(_layer, nn.Conv2d):
                        merged_layers.append(_layer)

        assert len(vgg_layers) == len(merged_layers)

        for l1, l2 in zip(vgg_layers, merged_layers):
            if isinstance(l1, nn.Conv2d) and isinstance(l2, nn.Conv2d):
                assert l1.weight.size() == l2.weight.size()
                assert l1.bias.size() == l2.bias.size()
                l2.weight.data = l1.weight.data
                l2.bias.data = l1.bias.data


class SegNet_1(nn.Module):
    """Derived Class to define a Segnet Architecture of NN

    Attributes
    ----------
    in_channels : int
        The input size of the network.

    n_classes : int
        The output size of the network.

    References
    ----------
    SegNet: A Deep Convolutional Encoder-Decoder Architecture
    for Image Segmentation
    Vijay Badrinarayanan, Alex Kendall, Roberto Cipolla, Senior Member, IEEE,
    """
    def __init__(self, in_channels=3, n_classes=21):
        """Sequential Instanciation of the different Layers"""
        super(SegNet_1, self).__init__()

        self.layer_1 = SegnetLayer_Encoder(in_channels, 64, 2)
        self.layer_2 = SegnetLayer_Encoder(64, 128, 2)
        self.layer_3 = SegnetLayer_Encoder(128, 256, 3)
        self.layer_4 = SegnetLayer_Encoder(256, 512, 3)
        self.layer_5 = SegnetLayer_Encoder(512, 1024, 3)
        self.layer_6 = SegnetLayer_Encoder(1024, 1024, 3)

        self.layer_7 = SegnetLayer_Decoder(1024, 1024, 3)
        self.layer_8 = SegnetLayer_Decoder(1024, 512, 3)
        self.layer_9 = SegnetLayer_Decoder(512, 256, 3)
        self.layer_10 = SegnetLayer_Decoder(256, 128, 3)
        self.layer_11 = SegnetLayer_Decoder(128, 64, 2)
        self.layer_12 = SegnetLayer_Decoder(64, n_classes, 2)

    def forward(self, inputs):
        """Sequential Computation, see nn.Module.forward methods PyTorch"""

        down1, indices_1, unpool_shape1 = self.layer_1(inputs=inputs,
                                                       layer_size=2)
        down2, indices_2, unpool_shape2 = self.layer_2(inputs=down1,
                                                       layer_size=2)
        down3, indices_3, unpool_shape3 = self.layer_3(inputs=down2,
                                                       layer_size=3)
        down4, indices_4, unpool_shape4 = self.layer_4(inputs=down3,
                                                       layer_size=3)
        down5, indices_5, unpool_shape5 = self.layer_5(inputs=down4,
                                                       layer_size=3)
        down6, indices_6, unpool_shape6 = self.layer_6(inputs=down5,
                                                       layer_size=3)
        up5 = self.layer_7(inputs=down6, indices=indices_6,
                           output_shape=unpool_shape6, layer_size=3)
        up4 = self.layer_8(inputs=up5, indices=indices_5,
                           output_shape=unpool_shape5, layer_size=3)
        up3 = self.layer_9(inputs=up4, indices=indices_4,
                           output_shape=unpool_shape4, layer_size=3)
        up2 = self.layer_10(inputs=up3, indices=indices_3,
                            output_shape=unpool_shape3, layer_size=3)
        up1 = self.layer_11(inputs=up2, indices=indices_2,
                            output_shape=unpool_shape2, layer_size=2)
        output = self.layer_12(inputs=up1, indices=indices_1,
                               output_shape=unpool_shape1, layer_size=2)

        return output


"""UPNET"""


class UpNet(nn.Module):
    """Derived Class to define a UpNet Architecture of NN

    Attributes
    ----------
    in_channels : int
        The input size of the network.

    n_classes : int
        The output size of the network.

    References
    ----------
    Efficient Deep Models for Monocular Road Segmentation
    Gabriel L. Oliveira, Wolfram Burgard and Thomas Brox
    """
    def __init__(self, in_channels=3, n_classes=21):
        """Sequential Instanciation of the different Layers"""
        super(UpNet, self).__init__()

        self.layer_1 = UpNetLayer_ParticularEncoder_2(in_channels, 64, 2)
        self.layer_2 = UpNetLayer_Encoder(64, 128, 2)
        self.layer_3 = UpNetLayer_Encoder(128, 256, 3)
        self.layer_4 = UpNetLayer_Encoder(256, 512, 3)
        self.layer_6 = UpNetLayer_ParticularEncoder(512, 1024, 3)

        self.layer_inter = UpNetLayer_Dropout()

        self.layer_7 = UpNetLayer_Decoder_Particular(1024, 512, 3)
        self.layer_8 = UpNetLayer_Decoder(512, 256, 3)
        self.layer_9 = UpNetLayer_Decoder(256, 128, 3)
        self.layer_10 = UpNetLayer_Decoder(128, 64, 2)
        self.layer_11 = UpNetLayer_Decoder_Particular_2(64, n_classes, 2)

    def forward(self, inputs):
        """Sequential Computation, see nn.Module.forward methods PyTorch"""

        down1, indices_1, unpool_shape1 = self.layer_1(inputs=inputs,
                                                       layer_size=2)
        down2, indices_2, unpool_shape2 = self.layer_2(inputs=down1,
                                                       layer_size=2)
        down3, indices_3, unpool_shape3 = self.layer_3(inputs=down2,
                                                       layer_size=3)
        down4, indices_4, unpool_shape4 = self.layer_4(inputs=down3,
                                                       layer_size=3)
        down5, indices_5, unpool_shape5 = self.layer_6(inputs=down4,
                                                       layer_size=3)

        inter = self.layer_inter(down5)

        up1 = self.layer_7(inputs=inter, indices=indices_5, layer_size=3)

        up2 = self.layer_8(inputs=up1, indices=indices_4, layer_size=3)

        up3 = self.layer_9(inputs=up2, indices=indices_3, layer_size=3)

        up4 = self.layer_10(inputs=up3, indices=indices_2, layer_size=2)

        up5 = self.layer_11(inputs=up4, indices=indices_1, layer_size=2)
        return up5


"""UNET"""


class U_Net(nn.Module):
    """Derived Class to define a UNet Architecture of NN

    Attributes
    ----------
    in_channels : int
        The input size of the network.

    n_classes : int
        The output size of the network.

    References
    ----------
    U-Net: Convolutional Networks for Biomedical Image Segmentation
    """
    def __init__(self, in_channels=3, n_classes=21):
        """Sequential Instanciation of the different Layers"""
        super(U_Net, self).__init__()

        self.layer_0 = UNet_Encoder_Particular(in_channels, 64)

        self.layer_1 = UNet_Encoder(64, 128)
        self.layer_2 = UNet_Encoder(128, 256)
        self.layer_3 = UNet_Encoder(256, 512)
        self.layer_4 = UNet_Encoder(512, 512)

        self.layer_7 = UNet_Decoder(1024, 256)
        self.layer_8 = UNet_Decoder(512, 128)
        self.layer_9 = UNet_Decoder(256, 64)
        self.layer_10 = UNet_Decoder(128, 64)

        self.layer_11 = UNet_Decoder_Particular(64, n_classes)

    def forward(self, inputs):
        """Sequential Computation, see nn.Module.forward methods PyTorch"""

        down0 = self.layer_0(inputs=inputs)
        down1 = self.layer_1(inputs=down0)
        down2 = self.layer_2(inputs=down1)
        down3 = self.layer_3(inputs=down2)
        down4 = self.layer_4(inputs=down3)

        up1 = self.layer_7(down4, down3)

        up2 = self.layer_8(up1, down2)

        up3 = self.layer_9(up2, down1)

        up4 = self.layer_10(up3, down0)

        up5 = self.layer_11(up4)
        return up5


'''
Multi Modality Using Segnet
'''


class MultiSegNet(nn.Module):
    """Derived Class to define a Segnet Architecture of NN

    Attributes
    ----------
    in_channels : int
        The input size of the network.

    n_classes : int
        The output size of the network.

    References
    ----------
    SegNet: A Deep Convolutional Encoder-Decoder Architecture
    for Image Segmentation
    Vijay Badrinarayanan, Alex Kendall, Roberto Cipolla, Senior Member, IEEE,
    """
    def __init__(self, in_channels=3, in_channels1=3, n_classes=21):
        """Sequential Instanciation of the different Layers"""
        super(SegNet, self).__init__()

        self.layer_1 = SegnetLayer_Encoder(in_channels, 64, 2)
        self.layer_2 = SegnetLayer_Encoder(64, 128, 2)
        self.layer_3 = SegnetLayer_Encoder(128, 256, 3)
        self.layer_4 = SegnetLayer_Encoder(256, 512, 3)
        self.layer_5 = SegnetLayer_Encoder(512, 512, 3)

        self.layer_6 = SegnetLayer_Decoder(512, 512, 3)
        self.layer_7 = SegnetLayer_Decoder(512, 256, 3)
        self.layer_8 = SegnetLayer_Decoder(256, 128, 3)
        self.layer_9 = SegnetLayer_Decoder(128, 64, 2)
        self.layer_10 = SegnetLayer_Decoder(64, n_classes, 2)

        self.layer_11 = SegnetLayer_Encoder(in_channels1, 64, 2)
        self.layer_12 = SegnetLayer_Encoder(64, 128, 2)
        self.layer_13 = SegnetLayer_Encoder(128, 256, 3)
        self.layer_14 = SegnetLayer_Encoder(256, 512, 3)
        self.layer_15 = SegnetLayer_Encoder(512, 512, 3)

        self.layer_16 = SegnetLayer_Decoder(512, 512, 3)
        self.layer_17 = SegnetLayer_Decoder(512, 256, 3)
        self.layer_18 = SegnetLayer_Decoder(256, 128, 3)
        self.layer_19 = SegnetLayer_Decoder(128, 64, 2)
        self.layer_110 = SegnetLayer_Decoder(64, n_classes, 2)

        self.layer_1110 = UNet_Decoder_Particular(n_classes * 2, n_classes)

    def forward(self, inputs, inputs1):
        """Sequential Computation, see nn.Module.forward methods PyTorch"""

        down1, indices_1, unpool_shape1 = self.layer_1(inputs=inputs,
                                                       layer_size=2)
        down2, indices_2, unpool_shape2 = self.layer_2(inputs=down1,
                                                       layer_size=2)
        down3, indices_3, unpool_shape3 = self.layer_3(inputs=down2,
                                                       layer_size=3)
        down4, indices_4, unpool_shape4 = self.layer_4(inputs=down3,
                                                       layer_size=3)
        down5, indices_5, unpool_shape5 = self.layer_5(inputs=down4,
                                                       layer_size=3)

        up5 = self.layer_6(inputs=down5, indices=indices_5,
                           output_shape=unpool_shape5, layer_size=3)
        up4 = self.layer_7(inputs=up5, indices=indices_4,
                           output_shape=unpool_shape4, layer_size=3)
        up3 = self.layer_8(inputs=up4, indices=indices_3,
                           output_shape=unpool_shape3, layer_size=3)
        up2 = self.layer_9(inputs=up3, indices=indices_2,
                           output_shape=unpool_shape2, layer_size=2)
        output = self.layer_10(inputs=up2, indices=indices_1,
                               output_shape=unpool_shape1, layer_size=2)

        # Second Modality

        down11, indices_11, unpool_shape11 = self.layer_11(inputs=inputs,
                                                           layer_size=2)
        down12, indices_12, unpool_shape12 = self.layer_12(inputs=down1,
                                                           layer_size=2)
        down13, indices_13, unpool_shape13 = self.layer_13(inputs=down2,
                                                           layer_size=3)
        down14, indices_14, unpool_shape14 = self.layer_14(inputs=down3,
                                                           layer_size=3)
        down15, indices_15, unpool_shape15 = self.layer_15(inputs=down4,
                                                           layer_size=3)

        up15 = self.layer_16(inputs=down15, indices=indices_15,
                             output_shape=unpool_shape15, layer_size=3)
        up14 = self.layer_17(inputs=up15, indices=indices_14,
                             output_shape=unpool_shape4, layer_size=3)
        up13 = self.layer_18(inputs=up14, indices=indices_13,
                             output_shape=unpool_shape13, layer_size=3)
        up12 = self.layer_19(inputs=up13, indices=indices_12,
                             output_shape=unpool_shape12, layer_size=2)
        output1 = self.layer_110(inputs=up12, indices=indices_11,
                                 output_shape=unpool_shape11, layer_size=2)

        # End Pipe

        Concat = torch.cat((output, output1), 1)

        finalout = self.layer_1110(Concat)

        return finalout

    def init_encoder(self):
        """Initialize encoder with VGG16 weights for Relu and Conv"""

        vgg = models.vgg16(pretrained=True)

        blocks = [self.layer_1,
                  self.layer_2,
                  self.layer_3,
                  self.layer_4,
                  self.layer_5]

        ranges = [[0, 4], [5, 9], [10, 16], [17, 23], [24, 29]]
        features = list(vgg.features.children())

        vgg_layers = []
        for _layer in features:
            if isinstance(_layer, nn.Conv2d):
                vgg_layers.append(_layer)

        merged_layers = []
        for idx, conv_block in enumerate(blocks):
            if idx < 2:
                units = [conv_block.conv1.cbr_unit,
                         conv_block.conv2.cbr_unit]
            else:
                units = [conv_block.conv1.cbr_unit,
                         conv_block.conv2.cbr_unit,
                         conv_block.conv3.cbr_unit]
            for _unit in units:
                for _layer in _unit:
                    if isinstance(_layer, nn.Conv2d):
                        merged_layers.append(_layer)

        assert len(vgg_layers) == len(merged_layers)

        for l1, l2 in zip(vgg_layers, merged_layers):
            if isinstance(l1, nn.Conv2d) and isinstance(l2, nn.Conv2d):
                assert l1.weight.size() == l2.weight.size()
                assert l1.bias.size() == l2.bias.size()
                l2.weight.data = l1.weight.data
                l2.bias.data = l1.bias.data

        blocks = [self.layer_11,
                  self.layer_12,
                  self.layer_13,
                  self.layer_14,
                  self.layer_15]

        ranges = [[0, 4], [5, 9], [10, 16], [17, 23], [24, 29]]
        features = list(vgg.features.children())

        vgg_layers = []
        for _layer in features:
            if isinstance(_layer, nn.Conv2d):
                vgg_layers.append(_layer)

        merged_layers = []
        for idx, conv_block in enumerate(blocks):
            if idx < 2:
                units = [conv_block.conv1.cbr_unit,
                         conv_block.conv2.cbr_unit]
            else:
                units = [conv_block.conv1.cbr_unit,
                         conv_block.conv2.cbr_unit,
                         conv_block.conv3.cbr_unit]
            for _unit in units:
                for _layer in _unit:
                    if isinstance(_layer, nn.Conv2d):
                        merged_layers.append(_layer)

        assert len(vgg_layers) == len(merged_layers)

        for l1, l2 in zip(vgg_layers, merged_layers):
            if isinstance(l1, nn.Conv2d) and isinstance(l2, nn.Conv2d):
                assert l1.weight.size() == l2.weight.size()
                assert l1.bias.size() == l2.bias.size()
                l2.weight.data = l1.weight.data
                l2.bias.data = l1.bias.data
