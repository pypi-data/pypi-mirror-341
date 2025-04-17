"""
UNet implementation based on "U-Net: Convolutional Networks for Biomedical Image Segmentation"
https://arxiv.org/abs/1505.04597
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import Optional, List, Union, Dict


class DoubleConv(nn.Module):
    """Double convolution block: conv -> bn -> relu -> conv -> bn -> relu"""
    
    def __init__(
        self, 
        in_channels: int, 
        out_channels: int, 
        mid_channels: Optional[int] = None,
        kernel_size: int = 3,
        padding: int = 1,
        bias: bool = False
    ) -> None:
        super().__init__()
        if mid_channels is None:
            mid_channels = out_channels
            
        self.double_conv = nn.Sequential(
            nn.Conv2d(in_channels, mid_channels, kernel_size=kernel_size, padding=padding, bias=bias),
            nn.BatchNorm2d(mid_channels),
            nn.ReLU(inplace=True),
            nn.Conv2d(mid_channels, out_channels, kernel_size=kernel_size, padding=padding, bias=bias),
            nn.BatchNorm2d(out_channels),
            nn.ReLU(inplace=True)
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.double_conv(x)


class Down(nn.Module):
    """Downscaling with maxpool then double conv"""
    
    def __init__(
        self, 
        in_channels: int, 
        out_channels: int, 
        pooling_size: int = 2
    ) -> None:
        super().__init__()
        self.maxpool_conv = nn.Sequential(
            nn.MaxPool2d(pooling_size),
            DoubleConv(in_channels, out_channels)
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.maxpool_conv(x)


class Up(nn.Module):
    """Upscaling then double conv"""
    
    def __init__(
        self, 
        in_channels: int, 
        out_channels: int, 
        bilinear: bool = True
    ) -> None:
        super().__init__()

        # if bilinear, use the normal convolutions to reduce the number of channels
        if bilinear:
            self.up = nn.Upsample(scale_factor=2, mode='bilinear', align_corners=True)
            self.conv = DoubleConv(in_channels, out_channels, in_channels // 2)
        else:
            self.up = nn.ConvTranspose2d(in_channels, in_channels // 2, kernel_size=2, stride=2)
            self.conv = DoubleConv(in_channels, out_channels)

    def forward(self, x1: torch.Tensor, x2: torch.Tensor) -> torch.Tensor:
        x1 = self.up(x1)
        
        # Adjust dimensions if needed
        diffY = x2.size()[2] - x1.size()[2]
        diffX = x2.size()[3] - x1.size()[3]

        x1 = F.pad(x1, [diffX // 2, diffX - diffX // 2,
                        diffY // 2, diffY - diffY // 2])
        
        # Concatenate along the channel dimension
        x = torch.cat([x2, x1], dim=1)
        return self.conv(x)


class OutConv(nn.Module):
    """Final 1x1 convolution layer"""
    
    def __init__(self, in_channels: int, out_channels: int) -> None:
        super().__init__()
        self.conv = nn.Conv2d(in_channels, out_channels, kernel_size=1)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.conv(x)


class UNet(nn.Module):
    """UNet architecture for image segmentation tasks"""
    
    def __init__(
        self, 
        in_channels: int = 3, 
        out_channels: int = 1,
        depth: int = 5,
        base_features: int = 64, 
        bilinear: bool = True,
        features: Optional[List[int]] = None
    ) -> None:
        """
        Args:
            in_channels: Number of input channels (e.g., 3 for RGB)
            out_channels: Number of output channels (e.g., 1 for binary segmentation)
            depth: Depth of the UNet (number of down/up operations)
            base_features: Number of features in the first layer
            bilinear: Whether to use bilinear upsampling (True) or transposed convolutions (False)
            features: List of feature dimensions for each layer (if None, generated based on depth and base_features)
        """
        super().__init__()
        self.in_channels = in_channels
        self.out_channels = out_channels
        self.bilinear = bilinear
        
        # Generate feature dimensions for each level if not provided
        if features is None:
            features = [base_features * (2 ** i) for i in range(depth)]
        
        # Initial double convolution
        self.inc = DoubleConv(in_channels, features[0])
        
        # Downsampling path
        self.downs = nn.ModuleList()
        for i in range(len(features) - 1):
            self.downs.append(Down(features[i], features[i + 1]))
        
        # Upsampling path
        self.ups = nn.ModuleList()
        for i in reversed(range(1, len(features))):
            in_feat = features[i]
            out_feat = features[i - 1]
            self.ups.append(Up(in_feat, out_feat, bilinear))
        
        # Final convolution
        self.outc = OutConv(features[0], out_channels)
        
        # Initialize weights
        self._init_weights()
        
    def _init_weights(self) -> None:
        """Initialize model weights for better convergence"""
        for m in self.modules():
            if isinstance(m, nn.Conv2d):
                nn.init.kaiming_normal_(m.weight, mode='fan_out', nonlinearity='relu')
                if m.bias is not None:
                    nn.init.constant_(m.bias, 0)
            elif isinstance(m, nn.BatchNorm2d):
                nn.init.constant_(m.weight, 1)
                nn.init.constant_(m.bias, 0)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # Initial feature extraction
        x1 = self.inc(x)
        
        # Contracting path with skip connections
        skip_connections = [x1]
        for down in self.downs:
            x = down(skip_connections[-1])
            skip_connections.append(x)
        
        # Remove the last feature map (bottom of the U)
        x = skip_connections.pop()
        
        # Expansive path
        for up in self.ups:
            skip = skip_connections.pop()
            x = up(x, skip)
            
        # Final convolution
        return self.outc(x)
