"""
Simple models and utilities for text and image classification tasks.

This package provides implementation of:
- Text classification: LSTM-based models and utilities
- Image classification: ResNet-based models and CIFAR-10 utilities
- Gradient Boosting: XGBoost and LightGBM implementations
"""

# Import text classification components
from .textclass import (
    TextDataset,
    BiLSTMClassifier,
    train as train_text,
    evaluate as evaluate_text,
    generate_data as generate_text_data
)

# Import image classification components
from .imgclass import (
    load_cifar10,
    train as train_img,
    evaluate as evaluate_img
)

# Import gradient boosting components
from .gb import (
    train_xgboost,
    train_lightgbm,
    evaluate as evaluate_gb,
    generate_data as generate_gb_data
)

__all__ = [
    # Text classification
    'TextDataset',
    'BiLSTMClassifier',
    'train_text',
    'evaluate_text',
    'generate_text_data',
    
    # Image classification
    'load_cifar10',
    'train_img',
    'evaluate_img',
    
    # Gradient Boosting
    'train_xgboost',
    'train_lightgbm',
    'evaluate_gb',
    'generate_gb_data'
]
