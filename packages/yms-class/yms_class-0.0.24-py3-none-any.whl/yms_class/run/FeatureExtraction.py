import argparse
import os
import sys
from collections import defaultdict

import torch
from scipy.io import savemat
from torchvision import transforms
from tqdm import tqdm

from yms_class.tools.dataset import create_dataloaders


def decea_extract_features(encoder, loader, device):
    """从数据集中提取特征"""
    features = defaultdict(list)
    encoder.eval()
    with torch.no_grad():
        for images, labels in tqdm(loader, desc="Extracting features", colour='blue', file=sys.stdout):
            outputs = encoder(images.to(device))
            for label, feat in zip(labels.cpu().numpy(), outputs.cpu().numpy()):
                features[int(label)].append(feat)
    return features


def extract_features(model, loader, device):
    """从数据集中提取特征"""
    all_features = []
    all_labels = []
    model.eval()
    with torch.no_grad():
        for images, labels in tqdm(loader, desc="Extracting feature...", colour='blue', file=sys.stdout):
            outputs = model(images.to(device))
            # 将特征和标签转换为 numpy 数组
            output_features = outputs.cpu().numpy()
            output_labels = labels.cpu().numpy()
            # 将特征和标签添加到对应的列表中
            all_features.extend(output_features)
            all_labels.extend(output_labels)

    return all_features, all_labels


def main(args):
    save_path = args.save_dir
    os.makedirs(save_path, exist_ok=True)

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    transform = transforms.Compose([
        transforms.Resize((160, 160)),
        transforms.Grayscale(),
        transforms.ToTensor(),
        transforms.Normalize([0.5], [0.5])
    ])
    train_loader, val_loader = create_dataloaders(args.data_dir, args.batch_size, transform, train_shuffle=False)

    data_name = os.path.basename(args.data_dir)
    model = torch.load(args.model_path, map_location='cpu', weights_only=False).to(device)
    train_features, train_labels = extract_features(model, train_loader, device)
    val_features, val_labels = extract_features(model, val_loader, device)
    savemat(os.path.join(save_path, f'{data_name}.mat'),
            {'train_features': train_features, 'train_labels': train_labels,
             'val_features': val_features, 'val_labels': val_labels,
             'class': train_loader.dataset.classes})


def parse_args(args=None):
    parser = argparse.ArgumentParser(description='Generate HSA matrix')
    parser.add_argument('--batch_size', type=int, default=100)
    parser.add_argument('--data_dir', default=r'/data/coding/data/D0')
    parser.add_argument('--model_path', default='/data/coding/results/train_D0/models/decae.pt')
    parser.add_argument('--save_dir', default='/data/coding/results/train_D0')
    return parser.parse_args(args if args else [])


if __name__ == '__main__':
    main(parse_args())
