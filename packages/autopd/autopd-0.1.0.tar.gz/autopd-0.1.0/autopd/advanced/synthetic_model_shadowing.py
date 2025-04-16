"""
Synthetic Model Shadowing (SMS) module for AutoPipelineDoctor.

This advanced module creates lightweight synthetic models that mimic the behavior of the
primary model to predict training outcomes, detect divergence, and provide early warnings
without the computational cost of full training.
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
import logging
import time
import os
import json
import copy
from typing import Dict, List, Tuple, Optional, Union, Any, Callable, Set
from enum import Enum
import threading
from collections import defaultdict, deque
import pickle
import math
import random
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)


class ShadowingStrategy(Enum):
    """Strategies for creating and updating shadow models."""
    DISTILLATION = "distillation"
    PARAMETER_SUBSET = "parameter_subset"
    LOW_RANK = "low_rank"
    EARLY_LAYER = "early_layer"
    QUANTIZED = "quantized"
    PRUNED = "pruned"
    HYBRID = "hybrid"


class PredictionTarget(Enum):
    """Targets for shadow model predictions."""
    CONVERGENCE = "convergence"
    OVERFITTING = "overfitting"
    GRADIENT_ISSUES = "gradient_issues"
    PERFORMANCE = "performance"
    GENERALIZATION = "generalization"
    CUSTOM = "custom"


@dataclass
class ShadowModelConfig:
    """Configuration for a shadow model."""
    name: str
    strategy: ShadowingStrategy
    compression_ratio: float = 0.25  # How much smaller the shadow model should be
    update_frequency: int = 10  # How often to update the shadow model (in batches)
    prediction_targets: List[PredictionTarget] = field(default_factory=list)
    prediction_horizon: int = 100  # How many steps ahead to predict
    custom_model_fn: Optional[Callable] = None  # Custom model creation function
    custom_update_fn: Optional[Callable] = None  # Custom update function
    custom_prediction_fn: Optional[Callable] = None  # Custom prediction function
    enabled: bool = True


class ShadowModel:
    """
    A lightweight synthetic model that mimics the behavior of the primary model.
    
    Attributes:
        name: Name of the shadow model
        strategy: Strategy used for shadowing
        model: The shadow model
        primary_model: Reference to the primary model
        config: Configuration for the shadow model
        metrics: Metrics collected by the shadow model
        predictions: Predictions made by the shadow model
        last_update: Timestamp of the last update
        update_count: Number of updates performed
    """
    
    def __init__(
        self,
        name: str,
        strategy: ShadowingStrategy,
        primary_model: nn.Module,
        config: ShadowModelConfig,
    ):
        """
        Initialize the shadow model.
        
        Args:
            name: Name of the shadow model
            strategy: Strategy used for shadowing
            primary_model: Reference to the primary model
            config: Configuration for the shadow model
        """
        self.name = name
        self.strategy = strategy
        self.primary_model = primary_model
        self.config = config
        
        # Initialize shadow model
        self.model = self._create_shadow_model()
        
        # Initialize metrics and predictions
        self.metrics = {}
        self.predictions = {}
        
        # Initialize update tracking
        self.last_update = time.time()
        self.update_count = 0
        
        # Initialize performance metrics
        self.performance_metrics = {
            "creation_time": 0.0,
            "update_time": 0.0,
            "prediction_time": 0.0,
            "memory_usage": 0.0,
        }
        
        # Initialize divergence metrics
        self.divergence_metrics = {
            "parameter_divergence": 0.0,
            "output_divergence": 0.0,
            "gradient_divergence": 0.0,
            "loss_divergence": 0.0,
        }
        
        # Initialize prediction metrics
        self.prediction_metrics = {
            "accuracy": 0.0,
            "precision": 0.0,
            "recall": 0.0,
            "f1_score": 0.0,
        }
        
        # Initialize prediction history
        self.prediction_history = {
            target.value: deque(maxlen=100) for target in self.config.prediction_targets
        }
        
        logger.info(f"Initialized shadow model '{name}' with strategy '{strategy.value}'")
    
    def _create_shadow_model(self) -> nn.Module:
        """
        Create a shadow model based on the selected strategy.
        
        Returns:
            Shadow model
        """
        start_time = time.time()
        
        # Use custom model function if provided
        if self.config.custom_model_fn is not None:
            model = self.config.custom_model_fn(self.primary_model, self.config)
            self.performance_metrics["creation_time"] = time.time() - start_time
            return model
        
        # Create shadow model based on strategy
        if self.strategy == ShadowingStrategy.DISTILLATION:
            model = self._create_distillation_model()
        elif self.strategy == ShadowingStrategy.PARAMETER_SUBSET:
            model = self._create_parameter_subset_model()
        elif self.strategy == ShadowingStrategy.LOW_RANK:
            model = self._create_low_rank_model()
        elif self.strategy == ShadowingStrategy.EARLY_LAYER:
            model = self._create_early_layer_model()
        elif self.strategy == ShadowingStrategy.QUANTIZED:
            model = self._create_quantized_model()
        elif self.strategy == ShadowingStrategy.PRUNED:
            model = self._create_pruned_model()
        elif self.strategy == ShadowingStrategy.HYBRID:
            model = self._create_hybrid_model()
        else:
            raise ValueError(f"Unknown shadowing strategy: {self.strategy}")
        
        self.performance_metrics["creation_time"] = time.time() - start_time
        
        # Calculate memory usage
        self._update_memory_usage()
        
        return model
    
    def _create_distillation_model(self) -> nn.Module:
        """
        Create a smaller model with the same architecture as the primary model.
        
        Returns:
            Distillation shadow model
        """
        # Analyze primary model architecture
        primary_modules = list(self.primary_model.modules())
        
        # Find all linear and convolutional layers
        layer_info = []
        for i, module in enumerate(primary_modules):
            if isinstance(module, (nn.Linear, nn.Conv1d, nn.Conv2d, nn.Conv3d)):
                layer_info.append((i, module))
        
        # Create a smaller model with the same architecture
        shadow_model = copy.deepcopy(self.primary_model)
        
        # Reduce the size of each layer
        for i, module in layer_info:
            if isinstance(module, nn.Linear):
                # Get original dimensions
                in_features = module.in_features
                out_features = module.out_features
                
                # Calculate new dimensions
                new_in_features = max(1, int(in_features * self.config.compression_ratio))
                new_out_features = max(1, int(out_features * self.config.compression_ratio))
                
                # Create new layer
                new_layer = nn.Linear(new_in_features, new_out_features, bias=module.bias is not None)
                
                # Replace layer in shadow model
                for name, child in shadow_model.named_modules():
                    if child is primary_modules[i]:
                        setattr(shadow_model, name, new_layer)
                        break
            
            elif isinstance(module, (nn.Conv1d, nn.Conv2d, nn.Conv3d)):
                # Get original dimensions
                in_channels = module.in_channels
                out_channels = module.out_channels
                
                # Calculate new dimensions
                new_in_channels = max(1, int(in_channels * self.config.compression_ratio))
                new_out_channels = max(1, int(out_channels * self.config.compression_ratio))
                
                # Create new layer
                if isinstance(module, nn.Conv1d):
                    new_layer = nn.Conv1d(
                        new_in_channels,
                        new_out_channels,
                        module.kernel_size,
                        stride=module.stride,
                        padding=module.padding,
                        dilation=module.dilation,
                        groups=max(1, int(module.groups * self.config.compression_ratio)),
                        bias=module.bias is not None,
                        padding_mode=module.padding_mode,
                    )
                elif isinstance(module, nn.Conv2d):
                    new_layer = nn.Conv2d(
                        new_in_channels,
                        new_out_channels,
                        module.kernel_size,
                        stride=module.stride,
                        padding=module.padding,
                        dilation=module.dilation,
                        groups=max(1, int(module.groups * self.config.compression_ratio)),
                        bias=module.bias is not None,
                        padding_mode=module.padding_mode,
                    )
                elif isinstance(module, nn.Conv3d):
                    new_layer = nn.Conv3d(
                        new_in_channels,
                        new_out_channels,
                        module.kernel_size,
                        stride=module.stride,
                        padding=module.padding,
                        dilation=module.dilation,
                        groups=max(1, int(module.groups * self.config.compression_ratio)),
                        bias=module.bias is not None,
                        padding_mode=module.padding_mode,
                    )
                
                # Replace layer in shadow model
                for name, child in shadow_model.named_modules():
                    if child is primary_modules[i]:
                        setattr(shadow_model, name, new_layer)
                        break
        
        return shadow_model
    
    def _create_parameter_subset_model(self) -> nn.Module:
        """
        Create a model that uses a subset of the parameters from the primary model.
        
        Returns:
            Parameter subset shadow model
        """
        # Create a copy of the primary model
        shadow_model = copy.deepcopy(self.primary_model)
        
        # Get all parameters
        params = list(shadow_model.parameters())
        
        # Calculate how many parameters to keep
        total_params = sum(p.numel() for p in params)
        params_to_keep = int(total_params * self.config.compression_ratio)
        
        # Create a mask for each parameter
        param_masks = []
        params_kept = 0
        
        for p in params:
            # Calculate how many parameters to keep in this tensor
            keep_ratio = min(1.0, (params_to_keep - params_kept) / p.numel())
            
            if keep_ratio <= 0:
                # No more parameters to keep
                mask = torch.zeros_like(p, dtype=torch.bool)
            else:
                # Create random mask
                mask = torch.rand_like(p, dtype=torch.float32) < keep_ratio
                params_kept += mask.sum().item()
            
            param_masks.append(mask)
        
        # Apply masks to parameters
        for p, mask in zip(shadow_model.parameters(), param_masks):
            # Zero out parameters that are not kept
            p.data = p.data * mask.float()
            
            # Store mask as buffer
            p._mask = mask
        
        return shadow_model
    
    def _create_low_rank_model(self) -> nn.Module:
        """
        Create a model that uses low-rank approximations of the parameters.
        
        Returns:
            Low-rank shadow model
        """
        # Create a copy of the primary model
        shadow_model = copy.deepcopy(self.primary_model)
        
        # Apply low-rank approximation to each parameter
        for name, param in shadow_model.named_parameters():
            if param.dim() >= 2:
                # Reshape to 2D
                original_shape = param.shape
                param_2d = param.reshape(original_shape[0], -1)
                
                # Calculate rank
                max_rank = min(param_2d.shape)
                rank = max(1, int(max_rank * self.config.compression_ratio))
                
                # Compute SVD
                try:
                    U, S, V = torch.svd(param_2d)
                    
                    # Keep only top-k singular values
                    U_k = U[:, :rank]
                    S_k = S[:rank]
                    V_k = V[:, :rank]
                    
                    # Reconstruct parameter
                    param_approx = U_k @ torch.diag(S_k) @ V_k.t()
                    
                    # Reshape back to original shape
                    param.data = param_approx.reshape(original_shape)
                    
                    # Store low-rank components as buffers
                    param._low_rank_U = U_k
                    param._low_rank_S = S_k
                    param._low_rank_V = V_k
                except Exception as e:
                    logger.warning(f"SVD failed for parameter {name}: {e}")
        
        return shadow_model
    
    def _create_early_layer_model(self) -> nn.Module:
        """
        Create a model that only includes the early layers of the primary model.
        
        Returns:
            Early layer shadow model
        """
        # Create a new sequential model
        layers = []
        
        # Find all modules in the primary model
        for name, module in self.primary_model.named_children():
            # Add module to layers
            layers.append(module)
            
            # Check if we've added enough layers
            if len(layers) >= max(1, int(len(list(self.primary_model.children())) * self.config.compression_ratio)):
                break
        
        # Create shadow model
        shadow_model = nn.Sequential(*layers)
        
        return shadow_model
    
    def _create_quantized_model(self) -> nn.Module:
        """
        Create a quantized version of the primary model.
        
        Returns:
            Quantized shadow model
        """
        # Create a copy of the primary model
        shadow_model = copy.deepcopy(self.primary_model)
        
        # Determine quantization precision based on compression ratio
        if self.config.compression_ratio <= 0.125:
            # 4-bit quantization
            bits = 4
        elif self.config.compression_ratio <= 0.25:
            # 8-bit quantization
            bits = 8
        else:
            # 16-bit quantization
            bits = 16
        
        # Apply quantization to each parameter
        for param in shadow_model.parameters():
            if param.dim() > 0:
                # Get parameter range
                param_min = param.min()
                param_max = param.max()
                param_range = param_max - param_min
                
                # Quantize parameter
                if bits == 4:
                    # 4-bit quantization (16 levels)
                    levels = 16
                    quantized = torch.round((param - param_min) / param_range * (levels - 1))
                    param.data = param_min + quantized * param_range / (levels - 1)
                elif bits == 8:
                    # 8-bit quantization (256 levels)
                    levels = 256
                    quantized = torch.round((param - param_min) / param_range * (levels - 1))
                    param.data = param_min + quantized * param_range / (levels - 1)
                else:  # bits == 16
                    # 16-bit quantization (convert to half precision)
                    param.data = param.half().float()
                
                # Store quantization info as buffer
                param._quantization_bits = bits
                param._quantization_min = param_min
                param._quantization_max = param_max
        
        return shadow_model
    
    def _create_pruned_model(self) -> nn.Module:
        """
        Create a pruned version of the primary model.
        
        Returns:
            Pruned shadow model
        """
        # Create a copy of the primary model
        shadow_model = copy.deepcopy(self.primary_model)
        
        # Calculate pruning threshold
        keep_ratio = self.config.compression_ratio
        
        # Apply pruning to each parameter
        for name, param in shadow_model.named_parameters():
            if param.dim() > 0:
                # Calculate absolute values
                abs_values = param.abs()
                
                # Calculate threshold
                threshold = torch.quantile(abs_values.view(-1), 1 - keep_ratio)
                
                # Create mask
                mask = abs_values > threshold
                
                # Apply mask
                param.data = param.data * mask.float()
                
                # Store mask as buffer
                param._prune_mask = mask
        
        return shadow_model
    
    def _create_hybrid_model(self) -> nn.Module:
        """
        Create a hybrid model that combines multiple shadowing strategies.
        
        Returns:
            Hybrid shadow model
        """
        # Create a copy of the primary model
        shadow_model = copy.deepcopy(self.primary_model)
        
        # Apply different strategies to different parts of the model
        for name, module in shadow_model.named_modules():
            if isinstance(module, nn.Linear):
                # Apply low-rank approximation to linear layers
                for param_name, param in module.named_parameters():
                    if param.dim() >= 2:
                        # Reshape to 2D
                        original_shape = param.shape
                        param_2d = param.reshape(original_shape[0], -1)
                        
                        # Calculate rank
                        max_rank = min(param_2d.shape)
                        rank = max(1, int(max_rank * self.config.compression_ratio))
                        
                        # Compute SVD
                        try:
                            U, S, V = torch.svd(param_2d)
                            
                            # Keep only top-k singular values
                            U_k = U[:, :rank]
                            S_k = S[:rank]
                            V_k = V[:, :rank]
                            
                            # Reconstruct parameter
                            param_approx = U_k @ torch.diag(S_k) @ V_k.t()
                            
                            # Reshape back to original shape
                            param.data = param_approx.reshape(original_shape)
                            
                            # Store low-rank components as buffers
                            param._low_rank_U = U_k
                            param._low_rank_S = S_k
                            param._low_rank_V = V_k
                        except Exception as e:
                            logger.warning(f"SVD failed for parameter {name}.{param_name}: {e}")
            
            elif isinstance(module, (nn.Conv1d, nn.Conv2d, nn.Conv3d)):
                # Apply pruning to convolutional layers
                for param_name, param in module.named_parameters():
                    if param.dim() > 0:
                        # Calculate absolute values
                        abs_values = param.abs()
                        
                        # Calculate threshold
                        threshold = torch.quantile(abs_values.view(-1), 1 - self.config.compression_ratio)
                        
                        # Create mask
                        mask = abs_values > threshold
                        
                        # Apply mask
                        param.data = param.data * mask.float()
                        
                        # Store mask as buffer
                        param._prune_mask = mask
            
            elif isinstance(module, nn.BatchNorm1d) or isinstance(module, nn.BatchNorm2d) or isinstance(module, nn.BatchNorm3d):
                # Apply quantization to batch normalization layers
                for param_name, param in module.named_parameters():
                    if param.dim() > 0:
                        # Get parameter range
                        param_min = param.min()
                        param_max = param.max()
                        param_range = param_max - param_min
                        
                        # 8-bit quantization (256 levels)
                        levels = 256
                        quantized = torch.round((param - param_min) / param_range * (levels - 1))
                        param.data = param_min + quantized * param_range / (levels - 1)
                        
                        # Store quantization info as buffer
                        param._quantization_bits = 8
                        param._quantization_min = param_min
                        param._quantization_max = param_max
        
        return shadow_model
    
    def _update_memory_usage(self) -> None:
        """Update memory usage metrics."""
        # Calculate memory usage
        memory_usage = sum(p.numel() * p.element_size() for p in self.model.parameters())
        primary_memory_usage = sum(p.numel() * p.element_size() for p in self.primary_model.parameters())
        
        # Update metrics
        self.performance_metrics["memory_usage"] = memory_usage
        self.performance_metrics["memory_ratio"] = memory_usage / primary_memory_usage if primary_memory_usage > 0 else 0.0
    
    def update(
        self,
        inputs: torch.Tensor,
        targets: Optional[torch.Tensor] = None,
        primary_outputs: Optional[torch.Tensor] = None,
        primary_loss: Optional[torch.Tensor] = None,
        optimizer: Optional[torch.optim.Optimizer] = None,
        batch_idx: int = 0,
    ) -> None:
        """
        Update the shadow model based on the primary model's behavior.
        
        Args:
            inputs: Input data
            targets: Target data
            primary_outputs: Outputs from the primary model
            primary_loss: Loss from the primary model
            optimizer: Optimizer for the shadow model
            batch_idx: Current batch index
        """
        # Check if update is needed
        if batch_idx % self.config.update_frequency != 0:
            return
        
        # Use custom update function if provided
        if self.config.custom_update_fn is not None:
            self.config.custom_update_fn(
                self,
                inputs,
                targets,
                primary_outputs,
                primary_loss,
                optimizer,
                batch_idx,
            )
            self.update_count += 1
            self.last_update = time.time()
            return
        
        start_time = time.time()
        
        # Update shadow model based on strategy
        if self.strategy == ShadowingStrategy.DISTILLATION:
            self._update_distillation(inputs, targets, primary_outputs, primary_loss, optimizer)
        elif self.strategy == ShadowingStrategy.PARAMETER_SUBSET:
            self._update_parameter_subset(inputs, targets, primary_outputs, primary_loss, optimizer)
        elif self.strategy == ShadowingStrategy.LOW_RANK:
            self._update_low_rank(inputs, targets, primary_outputs, primary_loss, optimizer)
        elif self.strategy == ShadowingStrategy.EARLY_LAYER:
            self._update_early_layer(inputs, targets, primary_outputs, primary_loss, optimizer)
        elif self.strategy == ShadowingStrategy.QUANTIZED:
            self._update_quantized(inputs, targets, primary_outputs, primary_loss, optimizer)
        elif self.strategy == ShadowingStrategy.PRUNED:
            self._update_pruned(inputs, targets, primary_outputs, primary_loss, optimizer)
        elif self.strategy == ShadowingStrategy.HYBRID:
            self._update_hybrid(inputs, targets, primary_outputs, primary_loss, optimizer)
        
        # Update metrics
        self.performance_metrics["update_time"] = time.time() - start_time
        
        # Update divergence metrics
        self._update_divergence_metrics(inputs, targets, primary_outputs, primary_loss)
        
        # Update counter
        self.update_count += 1
        self.last_update = time.time()
    
    def _update_distillation(
        self,
        inputs: torch.Tensor,
        targets: Optional[torch.Tensor],
        primary_outputs: Optional[torch.Tensor],
        primary_loss: Optional[torch.Tensor],
        optimizer: Optional[torch.optim.Optimizer],
    ) -> None:
        """
        Update the distillation shadow model.
        
        Args:
            inputs: Input data
            targets: Target data
            primary_outputs: Outputs from the primary model
            primary_loss: Loss from the primary model
            optimizer: Optimizer for the shadow model
        """
        # Check if we have primary outputs
        if primary_outputs is None:
            # Forward pass on primary model
            with torch.no_grad():
                primary_outputs = self.primary_model(inputs)
        
        # Create optimizer if not provided
        if optimizer is None:
            optimizer = torch.optim.Adam(self.model.parameters(), lr=0.001)
        
        # Train shadow model to mimic primary model
        self.model.train()
        
        # Forward pass
        shadow_outputs = self.model(inputs)
        
        # Compute distillation loss
        loss = F.mse_loss(shadow_outputs, primary_outputs.detach())
        
        # Backward pass and optimize
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        
        # Store metrics
        self.metrics["distillation_loss"] = loss.item()
    
    def _update_parameter_subset(
        self,
        inputs: torch.Tensor,
        targets: Optional[torch.Tensor],
        primary_outputs: Optional[torch.Tensor],
        primary_loss: Optional[torch.Tensor],
        optimizer: Optional[torch.optim.Optimizer],
    ) -> None:
        """
        Update the parameter subset shadow model.
        
        Args:
            inputs: Input data
            targets: Target data
            primary_outputs: Outputs from the primary model
            primary_loss: Loss from the primary model
            optimizer: Optimizer for the shadow model
        """
        # Copy parameters from primary model, respecting masks
        for shadow_param, primary_param in zip(self.model.parameters(), self.primary_model.parameters()):
            if hasattr(shadow_param, "_mask"):
                shadow_param.data = primary_param.data * shadow_param._mask.float()
            else:
                shadow_param.data = primary_param.data
    
    def _update_low_rank(
        self,
        inputs: torch.Tensor,
        targets: Optional[torch.Tensor],
        primary_outputs: Optional[torch.Tensor],
        primary_loss: Optional[torch.Tensor],
        optimizer: Optional[torch.optim.Optimizer],
    ) -> None:
        """
        Update the low-rank shadow model.
        
        Args:
            inputs: Input data
            targets: Target data
            primary_outputs: Outputs from the primary model
            primary_loss: Loss from the primary model
            optimizer: Optimizer for the shadow model
        """
        # Update low-rank approximations
        for shadow_param, primary_param in zip(self.model.parameters(), self.primary_model.parameters()):
            if hasattr(shadow_param, "_low_rank_U") and hasattr(shadow_param, "_low_rank_S") and hasattr(shadow_param, "_low_rank_V"):
                # Get original shape
                original_shape = shadow_param.shape
                
                # Reshape to 2D
                param_2d = primary_param.reshape(original_shape[0], -1)
                
                # Get rank
                rank = shadow_param._low_rank_U.shape[1]
                
                # Compute SVD
                try:
                    U, S, V = torch.svd(param_2d)
                    
                    # Keep only top-k singular values
                    U_k = U[:, :rank]
                    S_k = S[:rank]
                    V_k = V[:, :rank]
                    
                    # Reconstruct parameter
                    param_approx = U_k @ torch.diag(S_k) @ V_k.t()
                    
                    # Reshape back to original shape
                    shadow_param.data = param_approx.reshape(original_shape)
                    
                    # Update low-rank components
                    shadow_param._low_rank_U = U_k
                    shadow_param._low_rank_S = S_k
                    shadow_param._low_rank_V = V_k
                except Exception as e:
                    logger.warning(f"SVD failed during update: {e}")
            else:
                # Direct copy for parameters without low-rank approximation
                shadow_param.data = primary_param.data
    
    def _update_early_layer(
        self,
        inputs: torch.Tensor,
        targets: Optional[torch.Tensor],
        primary_outputs: Optional[torch.Tensor],
        primary_loss: Optional[torch.Tensor],
        optimizer: Optional[torch.optim.Optimizer],
    ) -> None:
        """
        Update the early layer shadow model.
        
        Args:
            inputs: Input data
            targets: Target data
            primary_outputs: Outputs from the primary model
            primary_loss: Loss from the primary model
            optimizer: Optimizer for the shadow model
        """
        # Get primary model layers
        primary_layers = list(self.primary_model.children())
        
        # Get shadow model layers
        shadow_layers = list(self.model.children())
        
        # Update shadow model layers
        for i, shadow_layer in enumerate(shadow_layers):
            if i < len(primary_layers):
                # Copy parameters from primary layer
                for shadow_param, primary_param in zip(shadow_layer.parameters(), primary_layers[i].parameters()):
                    shadow_param.data = primary_param.data
    
    def _update_quantized(
        self,
        inputs: torch.Tensor,
        targets: Optional[torch.Tensor],
        primary_outputs: Optional[torch.Tensor],
        primary_loss: Optional[torch.Tensor],
        optimizer: Optional[torch.optim.Optimizer],
    ) -> None:
        """
        Update the quantized shadow model.
        
        Args:
            inputs: Input data
            targets: Target data
            primary_outputs: Outputs from the primary model
            primary_loss: Loss from the primary model
            optimizer: Optimizer for the shadow model
        """
        # Update quantized parameters
        for shadow_param, primary_param in zip(self.model.parameters(), self.primary_model.parameters()):
            if hasattr(shadow_param, "_quantization_bits"):
                # Get parameter range
                param_min = primary_param.min()
                param_max = primary_param.max()
                param_range = param_max - param_min
                
                # Quantize parameter
                bits = shadow_param._quantization_bits
                
                if bits == 4:
                    # 4-bit quantization (16 levels)
                    levels = 16
                    quantized = torch.round((primary_param - param_min) / param_range * (levels - 1))
                    shadow_param.data = param_min + quantized * param_range / (levels - 1)
                elif bits == 8:
                    # 8-bit quantization (256 levels)
                    levels = 256
                    quantized = torch.round((primary_param - param_min) / param_range * (levels - 1))
                    shadow_param.data = param_min + quantized * param_range / (levels - 1)
                else:  # bits == 16
                    # 16-bit quantization (convert to half precision)
                    shadow_param.data = primary_param.half().float()
                
                # Update quantization info
                shadow_param._quantization_min = param_min
                shadow_param._quantization_max = param_max
            else:
                # Direct copy for parameters without quantization
                shadow_param.data = primary_param.data
    
    def _update_pruned(
        self,
        inputs: torch.Tensor,
        targets: Optional[torch.Tensor],
        primary_outputs: Optional[torch.Tensor],
        primary_loss: Optional[torch.Tensor],
        optimizer: Optional[torch.optim.Optimizer],
    ) -> None:
        """
        Update the pruned shadow model.
        
        Args:
            inputs: Input data
            targets: Target data
            primary_outputs: Outputs from the primary model
            primary_loss: Loss from the primary model
            optimizer: Optimizer for the shadow model
        """
        # Update pruned parameters
        for shadow_param, primary_param in zip(self.model.parameters(), self.primary_model.parameters()):
            if hasattr(shadow_param, "_prune_mask"):
                # Apply mask to primary parameter
                shadow_param.data = primary_param.data * shadow_param._prune_mask.float()
            else:
                # Direct copy for parameters without pruning
                shadow_param.data = primary_param.data
    
    def _update_hybrid(
        self,
        inputs: torch.Tensor,
        targets: Optional[torch.Tensor],
        primary_outputs: Optional[torch.Tensor],
        primary_loss: Optional[torch.Tensor],
        optimizer: Optional[torch.optim.Optimizer],
    ) -> None:
        """
        Update the hybrid shadow model.
        
        Args:
            inputs: Input data
            targets: Target data
            primary_outputs: Outputs from the primary model
            primary_loss: Loss from the primary model
            optimizer: Optimizer for the shadow model
        """
        # Update parameters based on their specific compression strategy
        for shadow_param, primary_param in zip(self.model.parameters(), self.primary_model.parameters()):
            if hasattr(shadow_param, "_low_rank_U") and hasattr(shadow_param, "_low_rank_S") and hasattr(shadow_param, "_low_rank_V"):
                # Update low-rank approximation
                # Get original shape
                original_shape = shadow_param.shape
                
                # Reshape to 2D
                param_2d = primary_param.reshape(original_shape[0], -1)
                
                # Get rank
                rank = shadow_param._low_rank_U.shape[1]
                
                # Compute SVD
                try:
                    U, S, V = torch.svd(param_2d)
                    
                    # Keep only top-k singular values
                    U_k = U[:, :rank]
                    S_k = S[:rank]
                    V_k = V[:, :rank]
                    
                    # Reconstruct parameter
                    param_approx = U_k @ torch.diag(S_k) @ V_k.t()
                    
                    # Reshape back to original shape
                    shadow_param.data = param_approx.reshape(original_shape)
                    
                    # Update low-rank components
                    shadow_param._low_rank_U = U_k
                    shadow_param._low_rank_S = S_k
                    shadow_param._low_rank_V = V_k
                except Exception as e:
                    logger.warning(f"SVD failed during update: {e}")
            
            elif hasattr(shadow_param, "_prune_mask"):
                # Update pruned parameter
                shadow_param.data = primary_param.data * shadow_param._prune_mask.float()
            
            elif hasattr(shadow_param, "_quantization_bits"):
                # Update quantized parameter
                # Get parameter range
                param_min = primary_param.min()
                param_max = primary_param.max()
                param_range = param_max - param_min
                
                # Quantize parameter
                bits = shadow_param._quantization_bits
                
                if bits == 4:
                    # 4-bit quantization (16 levels)
                    levels = 16
                    quantized = torch.round((primary_param - param_min) / param_range * (levels - 1))
                    shadow_param.data = param_min + quantized * param_range / (levels - 1)
                elif bits == 8:
                    # 8-bit quantization (256 levels)
                    levels = 256
                    quantized = torch.round((primary_param - param_min) / param_range * (levels - 1))
                    shadow_param.data = param_min + quantized * param_range / (levels - 1)
                else:  # bits == 16
                    # 16-bit quantization (convert to half precision)
                    shadow_param.data = primary_param.half().float()
                
                # Update quantization info
                shadow_param._quantization_min = param_min
                shadow_param._quantization_max = param_max
            
            else:
                # Direct copy for parameters without specific compression
                shadow_param.data = primary_param.data
    
    def _update_divergence_metrics(
        self,
        inputs: torch.Tensor,
        targets: Optional[torch.Tensor],
        primary_outputs: Optional[torch.Tensor],
        primary_loss: Optional[torch.Tensor],
    ) -> None:
        """
        Update divergence metrics between shadow and primary models.
        
        Args:
            inputs: Input data
            targets: Target data
            primary_outputs: Outputs from the primary model
            primary_loss: Loss from the primary model
        """
        # Parameter divergence
        param_divergence = 0.0
        param_count = 0
        
        for shadow_param, primary_param in zip(self.model.parameters(), self.primary_model.parameters()):
            if shadow_param.shape == primary_param.shape:
                param_divergence += F.mse_loss(shadow_param, primary_param).item()
                param_count += 1
        
        if param_count > 0:
            param_divergence /= param_count
        
        self.divergence_metrics["parameter_divergence"] = param_divergence
        
        # Output divergence
        if primary_outputs is not None:
            # Forward pass on shadow model
            with torch.no_grad():
                shadow_outputs = self.model(inputs)
            
            # Compute output divergence
            output_divergence = F.mse_loss(shadow_outputs, primary_outputs).item()
            self.divergence_metrics["output_divergence"] = output_divergence
        
        # Loss divergence
        if primary_loss is not None and targets is not None:
            # Forward pass on shadow model
            with torch.no_grad():
                shadow_outputs = self.model(inputs)
            
            # Compute shadow loss
            if isinstance(primary_loss, torch.Tensor):
                # Use same loss function as primary model
                shadow_loss = F.mse_loss(shadow_outputs, targets)
                
                # Compute loss divergence
                loss_divergence = abs(shadow_loss.item() - primary_loss.item())
                self.divergence_metrics["loss_divergence"] = loss_divergence
    
    def predict(
        self,
        inputs: Optional[torch.Tensor] = None,
        targets: Optional[torch.Tensor] = None,
        steps_ahead: int = 1,
        prediction_target: Optional[PredictionTarget] = None,
    ) -> Dict[str, Any]:
        """
        Make predictions using the shadow model.
        
        Args:
            inputs: Input data
            targets: Target data
            steps_ahead: Number of steps ahead to predict
            prediction_target: Target for prediction
            
        Returns:
            Prediction results
        """
        # Use custom prediction function if provided
        if self.config.custom_prediction_fn is not None:
            return self.config.custom_prediction_fn(
                self,
                inputs,
                targets,
                steps_ahead,
                prediction_target,
            )
        
        start_time = time.time()
        
        # Initialize predictions
        predictions = {}
        
        # Determine prediction targets
        targets_to_predict = []
        if prediction_target is not None:
            targets_to_predict = [prediction_target]
        else:
            targets_to_predict = self.config.prediction_targets
        
        # Make predictions for each target
        for target in targets_to_predict:
            if target == PredictionTarget.CONVERGENCE:
                predictions[target.value] = self._predict_convergence(inputs, targets, steps_ahead)
            elif target == PredictionTarget.OVERFITTING:
                predictions[target.value] = self._predict_overfitting(inputs, targets, steps_ahead)
            elif target == PredictionTarget.GRADIENT_ISSUES:
                predictions[target.value] = self._predict_gradient_issues(inputs, targets, steps_ahead)
            elif target == PredictionTarget.PERFORMANCE:
                predictions[target.value] = self._predict_performance(inputs, targets, steps_ahead)
            elif target == PredictionTarget.GENERALIZATION:
                predictions[target.value] = self._predict_generalization(inputs, targets, steps_ahead)
            elif target == PredictionTarget.CUSTOM:
                predictions[target.value] = {"message": "Custom prediction not implemented"}
        
        # Update metrics
        self.performance_metrics["prediction_time"] = time.time() - start_time
        
        return predictions
    
    def _predict_convergence(
        self,
        inputs: Optional[torch.Tensor],
        targets: Optional[torch.Tensor],
        steps_ahead: int,
    ) -> Dict[str, Any]:
        """
        Predict convergence behavior.
        
        Args:
            inputs: Input data
            targets: Target data
            steps_ahead: Number of steps ahead to predict
            
        Returns:
            Convergence prediction
        """
        # Initialize prediction
        prediction = {
            "will_converge": True,
            "confidence": 0.0,
            "estimated_steps_to_convergence": 0,
            "estimated_final_loss": 0.0,
            "warning": None,
        }
        
        # Check if we have enough history
        if len(self.prediction_history.get(PredictionTarget.CONVERGENCE.value, [])) < 5:
            prediction["confidence"] = 0.0
            prediction["warning"] = "Not enough history for reliable prediction"
            return prediction
        
        # Get loss history
        loss_history = [item["loss"] for item in self.prediction_history[PredictionTarget.CONVERGENCE.value]]
        
        # Check for NaN or Inf
        if any(math.isnan(loss) or math.isinf(loss) for loss in loss_history):
            prediction["will_converge"] = False
            prediction["confidence"] = 0.9
            prediction["warning"] = "NaN or Inf detected in loss history"
            return prediction
        
        # Check for divergence
        if len(loss_history) >= 10:
            recent_trend = loss_history[-5:]
            if all(recent_trend[i] > recent_trend[i-1] for i in range(1, len(recent_trend))):
                prediction["will_converge"] = False
                prediction["confidence"] = 0.8
                prediction["warning"] = "Loss is consistently increasing"
                return prediction
        
        # Fit exponential decay to loss history
        try:
            import numpy as np
            from scipy.optimize import curve_fit
            
            # Define exponential decay function
            def exp_decay(x, a, b, c):
                return a * np.exp(-b * x) + c
            
            # Prepare data
            x = np.arange(len(loss_history))
            y = np.array(loss_history)
            
            # Fit curve
            params, _ = curve_fit(exp_decay, x, y, maxfev=10000)
            a, b, c = params
            
            # Predict future loss
            future_x = np.arange(len(loss_history), len(loss_history) + steps_ahead)
            future_y = exp_decay(future_x, a, b, c)
            
            # Estimate convergence
            if b > 0:  # Decaying exponential
                # Estimate steps to convergence (when loss is within 1% of asymptotic value)
                threshold = c * 1.01
                steps_to_convergence = int(np.ceil(-np.log((threshold - c) / a) / b)) - len(loss_history)
                steps_to_convergence = max(0, steps_to_convergence)
                
                prediction["will_converge"] = True
                prediction["confidence"] = min(0.9, b * 10)  # Higher decay rate -> higher confidence
                prediction["estimated_steps_to_convergence"] = steps_to_convergence
                prediction["estimated_final_loss"] = float(c)
            else:  # Not decaying
                prediction["will_converge"] = False
                prediction["confidence"] = 0.7
                prediction["warning"] = "Loss is not decaying exponentially"
        
        except Exception as e:
            # Fallback to simple heuristic
            recent_losses = loss_history[-10:]
            
            # Check if loss is decreasing
            is_decreasing = all(recent_losses[i] <= recent_losses[i-1] * 1.01 for i in range(1, len(recent_losses)))
            
            if is_decreasing:
                prediction["will_converge"] = True
                prediction["confidence"] = 0.6
                prediction["estimated_steps_to_convergence"] = steps_ahead
                prediction["estimated_final_loss"] = recent_losses[-1] * 0.9
            else:
                prediction["will_converge"] = False
                prediction["confidence"] = 0.6
                prediction["warning"] = "Loss is not consistently decreasing"
        
        return prediction
    
    def _predict_overfitting(
        self,
        inputs: Optional[torch.Tensor],
        targets: Optional[torch.Tensor],
        steps_ahead: int,
    ) -> Dict[str, Any]:
        """
        Predict overfitting behavior.
        
        Args:
            inputs: Input data
            targets: Target data
            steps_ahead: Number of steps ahead to predict
            
        Returns:
            Overfitting prediction
        """
        # Initialize prediction
        prediction = {
            "is_overfitting": False,
            "confidence": 0.0,
            "train_val_gap_trend": "stable",
            "warning": None,
        }
        
        # Check if we have enough history
        if len(self.prediction_history.get(PredictionTarget.OVERFITTING.value, [])) < 5:
            prediction["confidence"] = 0.0
            prediction["warning"] = "Not enough history for reliable prediction"
            return prediction
        
        # Get train and validation loss history
        history = self.prediction_history[PredictionTarget.OVERFITTING.value]
        train_losses = [item["train_loss"] for item in history if "train_loss" in item]
        val_losses = [item["val_loss"] for item in history if "val_loss" in item]
        
        # Check if we have both train and validation losses
        if len(train_losses) < 5 or len(val_losses) < 5:
            prediction["confidence"] = 0.0
            prediction["warning"] = "Not enough train/val history for reliable prediction"
            return prediction
        
        # Compute train-val gaps
        gaps = [val - train for train, val in zip(train_losses, val_losses)]
        
        # Check for increasing gap
        if len(gaps) >= 5:
            recent_gaps = gaps[-5:]
            
            # Check if gap is consistently increasing
            is_increasing = all(recent_gaps[i] >= recent_gaps[i-1] for i in range(1, len(recent_gaps)))
            
            if is_increasing:
                prediction["is_overfitting"] = True
                prediction["confidence"] = 0.8
                prediction["train_val_gap_trend"] = "increasing"
                prediction["warning"] = "Train-val gap is consistently increasing"
                
                # Check if validation loss is increasing while train loss is decreasing
                recent_train = train_losses[-5:]
                recent_val = val_losses[-5:]
                
                train_decreasing = all(recent_train[i] <= recent_train[i-1] for i in range(1, len(recent_train)))
                val_increasing = all(recent_val[i] >= recent_val[i-1] for i in range(1, len(recent_val)))
                
                if train_decreasing and val_increasing:
                    prediction["confidence"] = 0.9
                    prediction["warning"] = "Train loss decreasing while val loss increasing"
            else:
                # Check if gap is stable
                gap_changes = [abs(recent_gaps[i] - recent_gaps[i-1]) for i in range(1, len(recent_gaps))]
                avg_change = sum(gap_changes) / len(gap_changes)
                
                if avg_change < 0.01 * abs(recent_gaps[-1]):
                    prediction["train_val_gap_trend"] = "stable"
                elif sum(gap_changes) > 0:
                    prediction["train_val_gap_trend"] = "fluctuating_up"
                else:
                    prediction["train_val_gap_trend"] = "fluctuating_down"
        
        # Predict future gap
        try:
            import numpy as np
            from scipy.optimize import curve_fit
            
            # Define polynomial function
            def poly_func(x, a, b, c):
                return a * x**2 + b * x + c
            
            # Prepare data
            x = np.arange(len(gaps))
            y = np.array(gaps)
            
            # Fit curve
            params, _ = curve_fit(poly_func, x, y)
            a, b, c = params
            
            # Predict future gap
            future_x = np.arange(len(gaps), len(gaps) + steps_ahead)
            future_gaps = poly_func(future_x, a, b, c)
            
            # Check if future gap is increasing
            if a > 0 or (a == 0 and b > 0):
                prediction["is_overfitting"] = True
                prediction["confidence"] = min(0.9, abs(a) * 100 + abs(b) * 10)
                prediction["train_val_gap_trend"] = "increasing"
                prediction["warning"] = "Train-val gap is projected to increase"
                prediction["projected_gaps"] = future_gaps.tolist()
            
        except Exception as e:
            # Fallback to simple heuristic
            if prediction["is_overfitting"]:
                # Already determined to be overfitting
                pass
            else:
                # Check if current gap is significant
                current_gap = gaps[-1]
                
                if current_gap > 0.1 * val_losses[-1]:
                    prediction["is_overfitting"] = True
                    prediction["confidence"] = 0.6
                    prediction["warning"] = "Current train-val gap is significant"
        
        return prediction
    
    def _predict_gradient_issues(
        self,
        inputs: Optional[torch.Tensor],
        targets: Optional[torch.Tensor],
        steps_ahead: int,
    ) -> Dict[str, Any]:
        """
        Predict gradient-related issues.
        
        Args:
            inputs: Input data
            targets: Target data
            steps_ahead: Number of steps ahead to predict
            
        Returns:
            Gradient issues prediction
        """
        # Initialize prediction
        prediction = {
            "has_gradient_issues": False,
            "confidence": 0.0,
            "issue_type": None,
            "warning": None,
        }
        
        # Check if we have enough history
        if len(self.prediction_history.get(PredictionTarget.GRADIENT_ISSUES.value, [])) < 5:
            prediction["confidence"] = 0.0
            prediction["warning"] = "Not enough history for reliable prediction"
            return prediction
        
        # Get gradient norm history
        history = self.prediction_history[PredictionTarget.GRADIENT_ISSUES.value]
        grad_norms = [item["grad_norm"] for item in history if "grad_norm" in item]
        
        # Check if we have gradient norms
        if len(grad_norms) < 5:
            prediction["confidence"] = 0.0
            prediction["warning"] = "Not enough gradient history for reliable prediction"
            return prediction
        
        # Check for vanishing gradients
        recent_norms = grad_norms[-5:]
        
        if all(norm < 1e-4 for norm in recent_norms):
            prediction["has_gradient_issues"] = True
            prediction["confidence"] = 0.8
            prediction["issue_type"] = "vanishing"
            prediction["warning"] = "Gradients are vanishingly small"
            return prediction
        
        # Check for exploding gradients
        if any(norm > 1e3 for norm in recent_norms):
            prediction["has_gradient_issues"] = True
            prediction["confidence"] = 0.8
            prediction["issue_type"] = "exploding"
            prediction["warning"] = "Gradients are exploding"
            return prediction
        
        # Check for unstable gradients
        if len(grad_norms) >= 10:
            # Compute gradient norm changes
            norm_changes = [abs(grad_norms[i] - grad_norms[i-1]) / max(1e-10, grad_norms[i-1]) 
                           for i in range(1, len(grad_norms))]
            
            # Check if changes are large
            if any(change > 10.0 for change in norm_changes[-5:]):
                prediction["has_gradient_issues"] = True
                prediction["confidence"] = 0.7
                prediction["issue_type"] = "unstable"
                prediction["warning"] = "Gradient norms are highly unstable"
                return prediction
        
        # Predict future gradient behavior
        try:
            import numpy as np
            from scipy.optimize import curve_fit
            
            # Define exponential function
            def exp_func(x, a, b, c):
                return a * np.exp(b * x) + c
            
            # Prepare data
            x = np.arange(len(grad_norms))
            y = np.array(grad_norms)
            
            # Fit curve
            params, _ = curve_fit(exp_func, x, y, maxfev=10000)
            a, b, c = params
            
            # Predict future gradient norms
            future_x = np.arange(len(grad_norms), len(grad_norms) + steps_ahead)
            future_norms = exp_func(future_x, a, b, c)
            
            # Check for future issues
            if b > 0.1:  # Exponential growth
                prediction["has_gradient_issues"] = True
                prediction["confidence"] = min(0.9, b * 5)
                prediction["issue_type"] = "exploding"
                prediction["warning"] = "Gradients are projected to explode"
                prediction["projected_norms"] = future_norms.tolist()
            elif b < -0.1:  # Exponential decay
                prediction["has_gradient_issues"] = True
                prediction["confidence"] = min(0.9, abs(b) * 5)
                prediction["issue_type"] = "vanishing"
                prediction["warning"] = "Gradients are projected to vanish"
                prediction["projected_norms"] = future_norms.tolist()
            
        except Exception as e:
            # Fallback to simple heuristic
            if prediction["has_gradient_issues"]:
                # Already determined to have issues
                pass
            else:
                # Check if current norm is concerning
                current_norm = grad_norms[-1]
                
                if current_norm < 1e-3:
                    prediction["has_gradient_issues"] = True
                    prediction["confidence"] = 0.6
                    prediction["issue_type"] = "vanishing"
                    prediction["warning"] = "Current gradient norm is very small"
                elif current_norm > 1e2:
                    prediction["has_gradient_issues"] = True
                    prediction["confidence"] = 0.6
                    prediction["issue_type"] = "exploding"
                    prediction["warning"] = "Current gradient norm is very large"
        
        return prediction
    
    def _predict_performance(
        self,
        inputs: Optional[torch.Tensor],
        targets: Optional[torch.Tensor],
        steps_ahead: int,
    ) -> Dict[str, Any]:
        """
        Predict performance-related issues.
        
        Args:
            inputs: Input data
            targets: Target data
            steps_ahead: Number of steps ahead to predict
            
        Returns:
            Performance prediction
        """
        # Initialize prediction
        prediction = {
            "has_performance_issues": False,
            "confidence": 0.0,
            "issue_type": None,
            "warning": None,
        }
        
        # Check if we have enough history
        if len(self.prediction_history.get(PredictionTarget.PERFORMANCE.value, [])) < 5:
            prediction["confidence"] = 0.0
            prediction["warning"] = "Not enough history for reliable prediction"
            return prediction
        
        # Get performance metrics history
        history = self.prediction_history[PredictionTarget.PERFORMANCE.value]
        batch_times = [item["batch_time"] for item in history if "batch_time" in item]
        memory_usage = [item["memory_usage"] for item in history if "memory_usage" in item]
        
        # Check if we have performance metrics
        if len(batch_times) < 5:
            prediction["confidence"] = 0.0
            prediction["warning"] = "Not enough performance history for reliable prediction"
            return prediction
        
        # Check for increasing batch times
        if len(batch_times) >= 5:
            recent_times = batch_times[-5:]
            
            # Check if batch time is consistently increasing
            is_increasing = all(recent_times[i] >= recent_times[i-1] * 1.05 for i in range(1, len(recent_times)))
            
            if is_increasing:
                prediction["has_performance_issues"] = True
                prediction["confidence"] = 0.8
                prediction["issue_type"] = "slowdown"
                prediction["warning"] = "Batch processing time is consistently increasing"
        
        # Check for memory issues
        if len(memory_usage) >= 5:
            recent_memory = memory_usage[-5:]
            
            # Check if memory usage is consistently increasing
            is_increasing = all(recent_memory[i] >= recent_memory[i-1] * 1.02 for i in range(1, len(recent_memory)))
            
            if is_increasing:
                # Estimate future memory usage
                memory_growth_rate = (recent_memory[-1] - recent_memory[0]) / (len(recent_memory) - 1)
                projected_memory = recent_memory[-1] + memory_growth_rate * steps_ahead
                
                # Check if projected memory is concerning
                if projected_memory > 0.9 * self.metrics.get("total_memory", float('inf')):
                    prediction["has_performance_issues"] = True
                    prediction["confidence"] = 0.9
                    prediction["issue_type"] = "memory"
                    prediction["warning"] = "Memory usage is projected to reach critical levels"
                    prediction["projected_memory"] = projected_memory
        
        # Predict future performance
        try:
            import numpy as np
            from scipy.optimize import curve_fit
            
            # Define linear function
            def linear_func(x, a, b):
                return a * x + b
            
            # Prepare data
            x = np.arange(len(batch_times))
            y = np.array(batch_times)
            
            # Fit curve
            params, _ = curve_fit(linear_func, x, y)
            a, b = params
            
            # Predict future batch times
            future_x = np.arange(len(batch_times), len(batch_times) + steps_ahead)
            future_times = linear_func(future_x, a, b)
            
            # Check for future issues
            if a > 0.01 * batch_times[-1]:  # Significant increase
                prediction["has_performance_issues"] = True
                prediction["confidence"] = min(0.9, a * 100 / batch_times[-1])
                prediction["issue_type"] = "slowdown"
                prediction["warning"] = "Batch processing time is projected to increase significantly"
                prediction["projected_times"] = future_times.tolist()
            
        except Exception as e:
            # Fallback to simple heuristic
            if prediction["has_performance_issues"]:
                # Already determined to have issues
                pass
            else:
                # Check if current batch time is concerning
                current_time = batch_times[-1]
                initial_time = batch_times[0]
                
                if current_time > initial_time * 1.5:
                    prediction["has_performance_issues"] = True
                    prediction["confidence"] = 0.6
                    prediction["issue_type"] = "slowdown"
                    prediction["warning"] = "Current batch time is significantly higher than initial time"
        
        return prediction
    
    def _predict_generalization(
        self,
        inputs: Optional[torch.Tensor],
        targets: Optional[torch.Tensor],
        steps_ahead: int,
    ) -> Dict[str, Any]:
        """
        Predict generalization performance.
        
        Args:
            inputs: Input data
            targets: Target data
            steps_ahead: Number of steps ahead to predict
            
        Returns:
            Generalization prediction
        """
        # Initialize prediction
        prediction = {
            "will_generalize_well": True,
            "confidence": 0.0,
            "estimated_test_performance": 0.0,
            "warning": None,
        }
        
        # Check if we have enough history
        if len(self.prediction_history.get(PredictionTarget.GENERALIZATION.value, [])) < 5:
            prediction["confidence"] = 0.0
            prediction["warning"] = "Not enough history for reliable prediction"
            return prediction
        
        # Get performance metrics history
        history = self.prediction_history[PredictionTarget.GENERALIZATION.value]
        train_metrics = [item["train_metric"] for item in history if "train_metric" in item]
        val_metrics = [item["val_metric"] for item in history if "val_metric" in item]
        
        # Check if we have both train and validation metrics
        if len(train_metrics) < 5 or len(val_metrics) < 5:
            prediction["confidence"] = 0.0
            prediction["warning"] = "Not enough train/val history for reliable prediction"
            return prediction
        
        # Compute train-val gaps
        gaps = [abs(val - train) for train, val in zip(train_metrics, val_metrics)]
        
        # Check for large gap
        if len(gaps) >= 5:
            recent_gaps = gaps[-5:]
            avg_gap = sum(recent_gaps) / len(recent_gaps)
            
            # Check if gap is large
            if avg_gap > 0.1 * abs(val_metrics[-1]):
                prediction["will_generalize_well"] = False
                prediction["confidence"] = 0.7
                prediction["warning"] = "Large gap between train and validation performance"
        
        # Check for plateauing validation performance
        if len(val_metrics) >= 10:
            recent_vals = val_metrics[-10:]
            
            # Check if validation performance is plateauing
            is_plateauing = all(abs(recent_vals[i] - recent_vals[i-1]) < 0.01 * abs(recent_vals[i]) 
                               for i in range(1, len(recent_vals)))
            
            if is_plateauing:
                # Not necessarily bad, but worth noting
                prediction["warning"] = "Validation performance is plateauing"
        
        # Predict future generalization
        try:
            import numpy as np
            from scipy.optimize import curve_fit
            
            # Define logarithmic function
            def log_func(x, a, b, c):
                return a * np.log(b * x + 1) + c
            
            # Prepare data
            x = np.arange(len(val_metrics))
            y = np.array(val_metrics)
            
            # Fit curve
            params, _ = curve_fit(log_func, x, y, maxfev=10000)
            a, b, c = params
            
            # Predict future validation performance
            future_x = np.arange(len(val_metrics), len(val_metrics) + steps_ahead)
            future_vals = log_func(future_x, a, b, c)
            
            # Estimate test performance (slightly worse than validation)
            test_performance = future_vals[-1] * 0.95
            
            prediction["estimated_test_performance"] = float(test_performance)
            prediction["confidence"] = 0.7
            
            # Check if future performance is good
            if a > 0:  # Increasing performance is good (assuming higher is better)
                prediction["will_generalize_well"] = True
            else:  # Decreasing performance is bad
                prediction["will_generalize_well"] = False
                prediction["warning"] = "Validation performance is projected to decrease"
            
            prediction["projected_val_performance"] = future_vals.tolist()
            
        except Exception as e:
            # Fallback to simple heuristic
            if prediction["warning"] is not None:
                # Already determined to have issues
                pass
            else:
                # Use recent trend
                recent_vals = val_metrics[-5:]
                
                # Check if validation performance is improving
                is_improving = all(recent_vals[i] >= recent_vals[i-1] for i in range(1, len(recent_vals)))
                
                if is_improving:
                    prediction["will_generalize_well"] = True
                    prediction["confidence"] = 0.6
                    prediction["estimated_test_performance"] = val_metrics[-1] * 0.95
                else:
                    prediction["will_generalize_well"] = False
                    prediction["confidence"] = 0.6
                    prediction["warning"] = "Validation performance is not consistently improving"
                    prediction["estimated_test_performance"] = val_metrics[-1] * 0.9
        
        return prediction
    
    def record_metrics(
        self,
        metrics: Dict[str, Any],
        prediction_target: Optional[PredictionTarget] = None,
    ) -> None:
        """
        Record metrics for future predictions.
        
        Args:
            metrics: Metrics to record
            prediction_target: Target for prediction
        """
        # Record metrics for all targets if not specified
        if prediction_target is None:
            for target in self.config.prediction_targets:
                if target.value in self.prediction_history:
                    self.prediction_history[target.value].append(metrics)
        else:
            # Record metrics for specific target
            if prediction_target.value in self.prediction_history:
                self.prediction_history[prediction_target.value].append(metrics)
    
    def get_metrics(self) -> Dict[str, Any]:
        """
        Get all metrics.
        
        Returns:
            All metrics
        """
        return {
            "performance": self.performance_metrics,
            "divergence": self.divergence_metrics,
            "prediction": self.prediction_metrics,
            "general": self.metrics,
        }
    
    def get_predictions(self) -> Dict[str, Any]:
        """
        Get all predictions.
        
        Returns:
            All predictions
        """
        return self.predictions
    
    def get_model(self) -> nn.Module:
        """
        Get the shadow model.
        
        Returns:
            Shadow model
        """
        return self.model
    
    def save_state(self, path: str) -> None:
        """
        Save the shadow model state.
        
        Args:
            path: Path to save the state
        """
        state = {
            "name": self.name,
            "strategy": self.strategy.value,
            "metrics": self.metrics,
            "predictions": self.predictions,
            "performance_metrics": self.performance_metrics,
            "divergence_metrics": self.divergence_metrics,
            "prediction_metrics": self.prediction_metrics,
            "update_count": self.update_count,
            "last_update": self.last_update,
        }
        
        try:
            # Save state
            with open(path, "w") as f:
                json.dump(state, f, indent=2)
            
            # Save model
            torch.save(self.model.state_dict(), f"{path}.model")
            
            logger.info(f"Saved shadow model state to {path}")
        except Exception as e:
            logger.error(f"Failed to save shadow model state: {e}")
    
    def load_state(self, path: str) -> bool:
        """
        Load the shadow model state.
        
        Args:
            path: Path to load the state from
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Load state
            with open(path, "r") as f:
                state = json.load(f)
            
            self.name = state["name"]
            self.strategy = ShadowingStrategy(state["strategy"])
            self.metrics = state["metrics"]
            self.predictions = state["predictions"]
            self.performance_metrics = state["performance_metrics"]
            self.divergence_metrics = state["divergence_metrics"]
            self.prediction_metrics = state["prediction_metrics"]
            self.update_count = state["update_count"]
            self.last_update = state["last_update"]
            
            # Load model
            self.model.load_state_dict(torch.load(f"{path}.model"))
            
            logger.info(f"Loaded shadow model state from {path}")
            return True
        except Exception as e:
            logger.error(f"Failed to load shadow model state: {e}")
            return False


class SyntheticModelShadowing:
    """
    Synthetic Model Shadowing (SMS) for predicting training outcomes.
    
    This module creates lightweight synthetic models that mimic the behavior of the
    primary model to predict training outcomes, detect divergence, and provide early
    warnings without the computational cost of full training.
    
    Attributes:
        primary_model: The primary model to shadow
        shadow_models: Dictionary of shadow models
        device: Device to run computations on
        metrics: Metrics collected by the module
        predictions: Predictions made by the module
    """
    
    def __init__(
        self,
        primary_model: Optional[nn.Module] = None,
        shadow_configs: Optional[List[ShadowModelConfig]] = None,
        device: Optional[torch.device] = None,
    ):
        """
        Initialize the SyntheticModelShadowing module.
        
        Args:
            primary_model: The primary model to shadow
            shadow_configs: Configurations for shadow models
            device: Device to run computations on
        """
        self.primary_model = primary_model
        self.device = device or (torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu"))
        
        # Initialize shadow models
        self.shadow_models = {}
        
        if shadow_configs is not None and primary_model is not None:
            for config in shadow_configs:
                self.add_shadow_model(config)
        
        # Initialize metrics and predictions
        self.metrics = {}
        self.predictions = {}
        
        # Initialize update tracking
        self.last_update = time.time()
        self.update_count = 0
        
        # Initialize performance metrics
        self.performance_metrics = {
            "creation_time": 0.0,
            "update_time": 0.0,
            "prediction_time": 0.0,
            "memory_usage": 0.0,
        }
        
        logger.info("Initialized SyntheticModelShadowing")
    
    def register(
        self,
        primary_model: Optional[nn.Module] = None,
        shadow_configs: Optional[List[ShadowModelConfig]] = None,
        device: Optional[torch.device] = None,
    ) -> None:
        """
        Register components with the module.
        
        Args:
            primary_model: The primary model to shadow
            shadow_configs: Configurations for shadow models
            device: Device to run computations on
        """
        if primary_model is not None:
            self.primary_model = primary_model
        
        if device is not None:
            self.device = device
        
        if shadow_configs is not None and self.primary_model is not None:
            for config in shadow_configs:
                self.add_shadow_model(config)
        
        logger.info("Registered components with SyntheticModelShadowing")
    
    def add_shadow_model(self, config: ShadowModelConfig) -> None:
        """
        Add a shadow model.
        
        Args:
            config: Configuration for the shadow model
        """
        if self.primary_model is None:
            raise ValueError("Primary model must be registered before adding shadow models")
        
        # Create shadow model
        shadow_model = ShadowModel(
            name=config.name,
            strategy=config.strategy,
            primary_model=self.primary_model,
            config=config,
        )
        
        # Add to dictionary
        self.shadow_models[config.name] = shadow_model
        
        logger.info(f"Added shadow model '{config.name}' with strategy '{config.strategy.value}'")
    
    def remove_shadow_model(self, name: str) -> None:
        """
        Remove a shadow model.
        
        Args:
            name: Name of the shadow model to remove
        """
        if name in self.shadow_models:
            del self.shadow_models[name]
            logger.info(f"Removed shadow model '{name}'")
        else:
            logger.warning(f"Shadow model '{name}' not found")
    
    def update(
        self,
        inputs: torch.Tensor,
        targets: Optional[torch.Tensor] = None,
        primary_outputs: Optional[torch.Tensor] = None,
        primary_loss: Optional[torch.Tensor] = None,
        optimizer: Optional[torch.optim.Optimizer] = None,
        batch_idx: int = 0,
    ) -> None:
        """
        Update all shadow models.
        
        Args:
            inputs: Input data
            targets: Target data
            primary_outputs: Outputs from the primary model
            primary_loss: Loss from the primary model
            optimizer: Optimizer for the shadow models
            batch_idx: Current batch index
        """
        start_time = time.time()
        
        # Get primary outputs if not provided
        if primary_outputs is None and self.primary_model is not None:
            with torch.no_grad():
                primary_outputs = self.primary_model(inputs)
        
        # Update each shadow model
        for name, shadow_model in self.shadow_models.items():
            if shadow_model.config.enabled:
                shadow_model.update(
                    inputs,
                    targets,
                    primary_outputs,
                    primary_loss,
                    optimizer,
                    batch_idx,
                )
        
        # Update metrics
        self.performance_metrics["update_time"] = time.time() - start_time
        
        # Update counter
        self.update_count += 1
        self.last_update = time.time()
    
    def predict(
        self,
        inputs: Optional[torch.Tensor] = None,
        targets: Optional[torch.Tensor] = None,
        steps_ahead: int = 1,
        prediction_targets: Optional[List[PredictionTarget]] = None,
    ) -> Dict[str, Dict[str, Any]]:
        """
        Make predictions using all shadow models.
        
        Args:
            inputs: Input data
            targets: Target data
            steps_ahead: Number of steps ahead to predict
            prediction_targets: Targets for prediction
            
        Returns:
            Predictions from all shadow models
        """
        start_time = time.time()
        
        # Initialize predictions
        predictions = {}
        
        # Make predictions with each shadow model
        for name, shadow_model in self.shadow_models.items():
            if shadow_model.config.enabled:
                # Determine prediction targets
                targets_to_predict = []
                if prediction_targets is not None:
                    targets_to_predict = prediction_targets
                else:
                    targets_to_predict = shadow_model.config.prediction_targets
                
                # Make predictions for each target
                model_predictions = {}
                for target in targets_to_predict:
                    target_prediction = shadow_model.predict(
                        inputs,
                        targets,
                        steps_ahead,
                        target,
                    )
                    model_predictions.update(target_prediction)
                
                # Store predictions
                predictions[name] = model_predictions
                shadow_model.predictions = model_predictions
        
        # Update metrics
        self.performance_metrics["prediction_time"] = time.time() - start_time
        
        # Store predictions
        self.predictions = predictions
        
        return predictions
    
    def aggregate_predictions(
        self,
        prediction_target: PredictionTarget,
    ) -> Dict[str, Any]:
        """
        Aggregate predictions from all shadow models for a specific target.
        
        Args:
            prediction_target: Target for prediction
            
        Returns:
            Aggregated prediction
        """
        # Initialize aggregated prediction
        aggregated = {}
        
        # Get predictions for the target
        target_predictions = []
        for name, shadow_model in self.shadow_models.items():
            if shadow_model.config.enabled and prediction_target.value in shadow_model.predictions:
                target_predictions.append(shadow_model.predictions[prediction_target.value])
        
        # Check if we have predictions
        if not target_predictions:
            return {"warning": "No predictions available for this target"}
        
        # Aggregate based on prediction target
        if prediction_target == PredictionTarget.CONVERGENCE:
            # Aggregate convergence predictions
            will_converge_votes = sum(1 for p in target_predictions if p.get("will_converge", False))
            confidence_sum = sum(p.get("confidence", 0.0) for p in target_predictions)
            
            # Compute weighted average for steps to convergence
            steps_to_convergence = 0.0
            total_weight = 0.0
            
            for p in target_predictions:
                if "estimated_steps_to_convergence" in p and "confidence" in p:
                    steps_to_convergence += p["estimated_steps_to_convergence"] * p["confidence"]
                    total_weight += p["confidence"]
            
            if total_weight > 0:
                steps_to_convergence /= total_weight
            
            # Compute weighted average for final loss
            final_loss = 0.0
            total_weight = 0.0
            
            for p in target_predictions:
                if "estimated_final_loss" in p and "confidence" in p:
                    final_loss += p["estimated_final_loss"] * p["confidence"]
                    total_weight += p["confidence"]
            
            if total_weight > 0:
                final_loss /= total_weight
            
            # Collect warnings
            warnings = [p.get("warning") for p in target_predictions if p.get("warning") is not None]
            
            # Create aggregated prediction
            aggregated = {
                "will_converge": will_converge_votes > len(target_predictions) / 2,
                "confidence": confidence_sum / len(target_predictions),
                "estimated_steps_to_convergence": int(steps_to_convergence),
                "estimated_final_loss": float(final_loss),
                "warnings": warnings,
            }
        
        elif prediction_target == PredictionTarget.OVERFITTING:
            # Aggregate overfitting predictions
            is_overfitting_votes = sum(1 for p in target_predictions if p.get("is_overfitting", False))
            confidence_sum = sum(p.get("confidence", 0.0) for p in target_predictions)
            
            # Count trend votes
            trend_votes = {}
            for p in target_predictions:
                trend = p.get("train_val_gap_trend", "stable")
                trend_votes[trend] = trend_votes.get(trend, 0) + 1
            
            # Get most common trend
            most_common_trend = max(trend_votes.items(), key=lambda x: x[1])[0] if trend_votes else "stable"
            
            # Collect warnings
            warnings = [p.get("warning") for p in target_predictions if p.get("warning") is not None]
            
            # Create aggregated prediction
            aggregated = {
                "is_overfitting": is_overfitting_votes > len(target_predictions) / 2,
                "confidence": confidence_sum / len(target_predictions),
                "train_val_gap_trend": most_common_trend,
                "warnings": warnings,
            }
        
        elif prediction_target == PredictionTarget.GRADIENT_ISSUES:
            # Aggregate gradient issues predictions
            has_issues_votes = sum(1 for p in target_predictions if p.get("has_gradient_issues", False))
            confidence_sum = sum(p.get("confidence", 0.0) for p in target_predictions)
            
            # Count issue type votes
            issue_votes = {}
            for p in target_predictions:
                issue_type = p.get("issue_type")
                if issue_type is not None:
                    issue_votes[issue_type] = issue_votes.get(issue_type, 0) + 1
            
            # Get most common issue type
            most_common_issue = max(issue_votes.items(), key=lambda x: x[1])[0] if issue_votes else None
            
            # Collect warnings
            warnings = [p.get("warning") for p in target_predictions if p.get("warning") is not None]
            
            # Create aggregated prediction
            aggregated = {
                "has_gradient_issues": has_issues_votes > len(target_predictions) / 2,
                "confidence": confidence_sum / len(target_predictions),
                "issue_type": most_common_issue,
                "warnings": warnings,
            }
        
        elif prediction_target == PredictionTarget.PERFORMANCE:
            # Aggregate performance predictions
            has_issues_votes = sum(1 for p in target_predictions if p.get("has_performance_issues", False))
            confidence_sum = sum(p.get("confidence", 0.0) for p in target_predictions)
            
            # Count issue type votes
            issue_votes = {}
            for p in target_predictions:
                issue_type = p.get("issue_type")
                if issue_type is not None:
                    issue_votes[issue_type] = issue_votes.get(issue_type, 0) + 1
            
            # Get most common issue type
            most_common_issue = max(issue_votes.items(), key=lambda x: x[1])[0] if issue_votes else None
            
            # Collect warnings
            warnings = [p.get("warning") for p in target_predictions if p.get("warning") is not None]
            
            # Create aggregated prediction
            aggregated = {
                "has_performance_issues": has_issues_votes > len(target_predictions) / 2,
                "confidence": confidence_sum / len(target_predictions),
                "issue_type": most_common_issue,
                "warnings": warnings,
            }
        
        elif prediction_target == PredictionTarget.GENERALIZATION:
            # Aggregate generalization predictions
            will_generalize_votes = sum(1 for p in target_predictions if p.get("will_generalize_well", False))
            confidence_sum = sum(p.get("confidence", 0.0) for p in target_predictions)
            
            # Compute weighted average for test performance
            test_performance = 0.0
            total_weight = 0.0
            
            for p in target_predictions:
                if "estimated_test_performance" in p and "confidence" in p:
                    test_performance += p["estimated_test_performance"] * p["confidence"]
                    total_weight += p["confidence"]
            
            if total_weight > 0:
                test_performance /= total_weight
            
            # Collect warnings
            warnings = [p.get("warning") for p in target_predictions if p.get("warning") is not None]
            
            # Create aggregated prediction
            aggregated = {
                "will_generalize_well": will_generalize_votes > len(target_predictions) / 2,
                "confidence": confidence_sum / len(target_predictions),
                "estimated_test_performance": float(test_performance),
                "warnings": warnings,
            }
        
        return aggregated
    
    def record_metrics(
        self,
        metrics: Dict[str, Any],
        prediction_target: Optional[PredictionTarget] = None,
    ) -> None:
        """
        Record metrics for future predictions.
        
        Args:
            metrics: Metrics to record
            prediction_target: Target for prediction
        """
        # Record metrics for each shadow model
        for name, shadow_model in self.shadow_models.items():
            if shadow_model.config.enabled:
                shadow_model.record_metrics(metrics, prediction_target)
    
    def get_metrics(self) -> Dict[str, Any]:
        """
        Get all metrics.
        
        Returns:
            All metrics
        """
        # Collect metrics from each shadow model
        shadow_metrics = {}
        for name, shadow_model in self.shadow_models.items():
            shadow_metrics[name] = shadow_model.get_metrics()
        
        return {
            "performance": self.performance_metrics,
            "shadow_models": shadow_metrics,
            "general": self.metrics,
        }
    
    def get_predictions(self) -> Dict[str, Any]:
        """
        Get all predictions.
        
        Returns:
            All predictions
        """
        return self.predictions
    
    def get_shadow_models(self) -> Dict[str, ShadowModel]:
        """
        Get all shadow models.
        
        Returns:
            All shadow models
        """
        return self.shadow_models
    
    def save_state(self, path: str) -> None:
        """
        Save the module state.
        
        Args:
            path: Path to save the state
        """
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(path), exist_ok=True)
        
        # Save module state
        state = {
            "metrics": self.metrics,
            "predictions": self.predictions,
            "performance_metrics": self.performance_metrics,
            "update_count": self.update_count,
            "last_update": self.last_update,
        }
        
        try:
            # Save module state
            with open(path, "w") as f:
                json.dump(state, f, indent=2)
            
            # Save shadow models
            for name, shadow_model in self.shadow_models.items():
                shadow_model.save_state(f"{path}.{name}")
            
            logger.info(f"Saved SyntheticModelShadowing state to {path}")
        except Exception as e:
            logger.error(f"Failed to save SyntheticModelShadowing state: {e}")
    
    def load_state(self, path: str) -> bool:
        """
        Load the module state.
        
        Args:
            path: Path to load the state from
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Load module state
            with open(path, "r") as f:
                state = json.load(f)
            
            self.metrics = state["metrics"]
            self.predictions = state["predictions"]
            self.performance_metrics = state["performance_metrics"]
            self.update_count = state["update_count"]
            self.last_update = state["last_update"]
            
            # Load shadow models
            for name, shadow_model in self.shadow_models.items():
                shadow_model.load_state(f"{path}.{name}")
            
            logger.info(f"Loaded SyntheticModelShadowing state from {path}")
            return True
        except Exception as e:
            logger.error(f"Failed to load SyntheticModelShadowing state: {e}")
            return False
    
    def create_default_shadow_models(self) -> None:
        """Create a set of default shadow models."""
        if self.primary_model is None:
            raise ValueError("Primary model must be registered before creating default shadow models")
        
        # Create default configurations
        configs = [
            ShadowModelConfig(
                name="distillation_convergence",
                strategy=ShadowingStrategy.DISTILLATION,
                compression_ratio=0.25,
                update_frequency=10,
                prediction_targets=[PredictionTarget.CONVERGENCE],
                prediction_horizon=100,
            ),
            ShadowModelConfig(
                name="parameter_subset_overfitting",
                strategy=ShadowingStrategy.PARAMETER_SUBSET,
                compression_ratio=0.3,
                update_frequency=10,
                prediction_targets=[PredictionTarget.OVERFITTING],
                prediction_horizon=50,
            ),
            ShadowModelConfig(
                name="low_rank_gradients",
                strategy=ShadowingStrategy.LOW_RANK,
                compression_ratio=0.2,
                update_frequency=5,
                prediction_targets=[PredictionTarget.GRADIENT_ISSUES],
                prediction_horizon=20,
            ),
            ShadowModelConfig(
                name="quantized_performance",
                strategy=ShadowingStrategy.QUANTIZED,
                compression_ratio=0.25,
                update_frequency=20,
                prediction_targets=[PredictionTarget.PERFORMANCE],
                prediction_horizon=50,
            ),
            ShadowModelConfig(
                name="hybrid_generalization",
                strategy=ShadowingStrategy.HYBRID,
                compression_ratio=0.3,
                update_frequency=10,
                prediction_targets=[PredictionTarget.GENERALIZATION],
                prediction_horizon=100,
            ),
        ]
        
        # Create shadow models
        for config in configs:
            self.add_shadow_model(config)
        
        logger.info("Created default shadow models")
