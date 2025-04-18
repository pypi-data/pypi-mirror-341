import torch
from torch import nn


class FeatureExtractor(nn.Module):
    def __init__(self):
        super().__init__()
        self.features = nn.Sequential(
            nn.Conv2d(3, 32, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.Conv2d(32, 64, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Conv2d(64, 128, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.Conv2d(128, 256, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2)
        )

    def forward(self, x):
        x = self.features(x)
        x = torch.flatten(x, 1)
        return x


class CNN(nn.Module):
    def __init__(self, num_classes=10):
        super().__init__()
        self.features = FeatureExtractor()
        self.classification = nn.Sequential(
            nn.Linear(256 * 8 * 8, 4096),
            nn.ReLU(),
            nn.Linear(4096, 2048),
            nn.ReLU(),
            nn.Linear(2048, num_classes)
        )

    def save(self, path):
        torch.save(self.features, path)

    def forward(self, x):
        x = self.features(x)
        x = self.classification(x)
        return x
