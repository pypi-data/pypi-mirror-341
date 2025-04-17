"""
Neural network model implementations.
"""

from .resnet import (
    resnet18,
    resnet34,
    resnet50,
    resnet101,
    resnet152
)

from .resnetv2 import (
    resnetv2_18,
    resnetv2_34,
    resnetv2_50,
    resnetv2_101,
    resnetv2_152
)

from .inception_resnet import (
    inception_resnet_v1,
    inception_resnet_v2
)

from .text_lstm import TextLSTM

from .unet import UNet

from .word2vec import (
    Word2Vec,
    Word2VecTrainer,
    train_word2vec
)

from .glove import (
    GloVeModel,
    GloVeTrainer,
    train_glove
)

from .hf_llm import (
    eval_llm,
    get_model_info
)

from .hf_vit import (
    load_vit,
    get_model_info as vit_get_model_info,
    train_vit,
    eval_vit
)

from .vae import (
    VAE,
    VAETrainer,
    visualize_vae,
    example_usage
)

from .gradboost import (
    GradientBooster,
    tune_hyperparameters,
    cross_validate,
    train_gradient_booster
)

__all__ = [
    # CNN models
    'resnet18',
    'resnet34',
    'resnet50',
    'resnet101',
    'resnet152',
    'resnetv2_18',
    'resnetv2_34',
    'resnetv2_50',
    'resnetv2_101',
    'resnetv2_152',
    'inception_resnet_v1',
    'inception_resnet_v2',
    
    # Text models
    'TextLSTM',
    
    # Image segmentation
    'UNet',
    
    # Word embeddings
    'Word2Vec',
    'Word2VecTrainer',
    'train_word2vec',
    'GloVeModel',
    'GloVeTrainer',
    'train_glove',
    
    # LLM utilities
    'eval_llm',
    'get_model_info',
    
    # Vision Transformer models
    'load_vit',
    'vit_get_model_info',
    'train_vit',
    'eval_vit',
    
    # Generative models
    'VAE',
    'VAETrainer',
    'visualize_vae',
    'example_usage',
    
    # Gradient Boosting models
    'GradientBooster',
    'tune_hyperparameters',
    'cross_validate',
    'train_gradient_booster'
]
