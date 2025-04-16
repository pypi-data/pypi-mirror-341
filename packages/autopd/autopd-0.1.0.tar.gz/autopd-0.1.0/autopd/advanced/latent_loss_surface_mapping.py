"""
Latent Loss Surface Mapping (LLSM) module for AutoPipelineDoctor.

This advanced module creates 3D visualizations of loss landscapes to identify
problematic training regions, visualize optimization paths, and detect saddle points,
plateaus, and steep cliffs.
"""

import torch
import torch.nn as nn
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import logging
import time
import os
import json
import copy
from typing import Dict, List, Tuple, Optional, Union, Any, Callable, Set
from enum import Enum
import threading
from collections import defaultdict
import pickle
import math
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import io
import base64
from PIL import Image

logger = logging.getLogger(__name__)


class SurfaceType(Enum):
    """Types of loss surfaces that can be mapped."""
    LOSS = "loss_surface"
    GRADIENT_NORM = "gradient_norm_surface"
    HESSIAN_EIGENVALUE = "hessian_eigenvalue_surface"
    ACCURACY = "accuracy_surface"
    CUSTOM = "custom_surface"


class ProjectionMethod(Enum):
    """Methods for projecting high-dimensional parameter space to 2D/3D."""
    PCA = "principal_component_analysis"
    RANDOM = "random_projection"
    CUSTOM = "custom_projection"
    FILTER = "filter_projection"
    LAYER = "layer_projection"
    TSNE = "t_sne"


class LatentLossSurfaceMapping:
    """
    Latent Loss Surface Mapping (LLSM) for visualizing loss landscapes.
    
    This module creates 3D visualizations of loss landscapes to identify
    problematic training regions, visualize optimization paths, and detect
    saddle points, plateaus, and steep cliffs.
    
    Attributes:
        model: The PyTorch model to analyze
        loss_fn: Loss function to evaluate
        dataloader: Dataloader for evaluation data
        device: Device to run computations on
        projection_method: Method for projecting parameter space
        surface_type: Type of surface to map
        resolution: Resolution of the surface grid
        alpha_range: Range of values for the first projection direction
        beta_range: Range of values for the second projection direction
        normalize_directions: Whether to normalize projection directions
        use_ratio: Whether to use ratio of weights for perturbation
        custom_directions: Custom projection directions
        custom_metric_fn: Custom metric function for surface mapping
        history: History of parameter states and metrics
        current_surface: Currently computed surface
        optimization_path: Path taken by optimizer in parameter space
    """
    
    def __init__(
        self,
        model: Optional[nn.Module] = None,
        loss_fn: Optional[Callable] = None,
        dataloader: Optional[Any] = None,
        device: Optional[torch.device] = None,
        projection_method: Union[str, ProjectionMethod] = ProjectionMethod.PCA,
        surface_type: Union[str, SurfaceType] = SurfaceType.LOSS,
        resolution: int = 20,
        alpha_range: Tuple[float, float] = (-1.0, 1.0),
        beta_range: Tuple[float, float] = (-1.0, 1.0),
        normalize_directions: bool = True,
        use_ratio: bool = False,
        custom_directions: Optional[List[torch.Tensor]] = None,
        custom_metric_fn: Optional[Callable] = None,
    ):
        """
        Initialize the LatentLossSurfaceMapping module.
        
        Args:
            model: The PyTorch model to analyze
            loss_fn: Loss function to evaluate
            dataloader: Dataloader for evaluation data
            device: Device to run computations on
            projection_method: Method for projecting parameter space
            surface_type: Type of surface to map
            resolution: Resolution of the surface grid
            alpha_range: Range of values for the first projection direction
            beta_range: Range of values for the second projection direction
            normalize_directions: Whether to normalize projection directions
            use_ratio: Whether to use ratio of weights for perturbation
            custom_directions: Custom projection directions
            custom_metric_fn: Custom metric function for surface mapping
        """
        self.model = model
        self.loss_fn = loss_fn
        self.dataloader = dataloader
        self.device = device or (torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu"))
        
        # Convert enum strings to enum values if needed
        if isinstance(projection_method, str):
            self.projection_method = ProjectionMethod(projection_method)
        else:
            self.projection_method = projection_method
        
        if isinstance(surface_type, str):
            self.surface_type = SurfaceType(surface_type)
        else:
            self.surface_type = surface_type
        
        self.resolution = resolution
        self.alpha_range = alpha_range
        self.beta_range = beta_range
        self.normalize_directions = normalize_directions
        self.use_ratio = use_ratio
        self.custom_directions = custom_directions
        self.custom_metric_fn = custom_metric_fn
        
        # Initialize history
        self.history = []
        
        # Initialize surface data
        self.current_surface = None
        
        # Initialize optimization path
        self.optimization_path = []
        
        # Initialize projection directions
        self.projection_directions = None
        
        # Initialize thread lock
        self.lock = threading.Lock()
        
        # Initialize computation thread
        self.computation_thread = None
        self.computation_active = False
        
        logger.info("Initialized LatentLossSurfaceMapping")
    
    def register(
        self,
        model: Optional[nn.Module] = None,
        loss_fn: Optional[Callable] = None,
        dataloader: Optional[Any] = None,
        device: Optional[torch.device] = None,
    ) -> None:
        """
        Register components with the module.
        
        Args:
            model: The PyTorch model to analyze
            loss_fn: Loss function to evaluate
            dataloader: Dataloader for evaluation data
            device: Device to run computations on
        """
        if model is not None:
            self.model = model
        
        if loss_fn is not None:
            self.loss_fn = loss_fn
        
        if dataloader is not None:
            self.dataloader = dataloader
        
        if device is not None:
            self.device = device
        
        logger.info("Registered components with LLSM")
    
    def compute_surface(
        self,
        projection_method: Optional[Union[str, ProjectionMethod]] = None,
        surface_type: Optional[Union[str, SurfaceType]] = None,
        resolution: Optional[int] = None,
        alpha_range: Optional[Tuple[float, float]] = None,
        beta_range: Optional[Tuple[float, float]] = None,
        normalize_directions: Optional[bool] = None,
        use_ratio: Optional[bool] = None,
        custom_directions: Optional[List[torch.Tensor]] = None,
        custom_metric_fn: Optional[Callable] = None,
        async_compute: bool = False,
    ) -> Optional[Dict[str, Any]]:
        """
        Compute the loss surface.
        
        Args:
            projection_method: Method for projecting parameter space
            surface_type: Type of surface to map
            resolution: Resolution of the surface grid
            alpha_range: Range of values for the first projection direction
            beta_range: Range of values for the second projection direction
            normalize_directions: Whether to normalize projection directions
            use_ratio: Whether to use ratio of weights for perturbation
            custom_directions: Custom projection directions
            custom_metric_fn: Custom metric function for surface mapping
            async_compute: Whether to compute asynchronously
            
        Returns:
            Surface data or None if computing asynchronously
        """
        # Update parameters if provided
        if projection_method is not None:
            if isinstance(projection_method, str):
                self.projection_method = ProjectionMethod(projection_method)
            else:
                self.projection_method = projection_method
        
        if surface_type is not None:
            if isinstance(surface_type, str):
                self.surface_type = SurfaceType(surface_type)
            else:
                self.surface_type = surface_type
        
        if resolution is not None:
            self.resolution = resolution
        
        if alpha_range is not None:
            self.alpha_range = alpha_range
        
        if beta_range is not None:
            self.beta_range = beta_range
        
        if normalize_directions is not None:
            self.normalize_directions = normalize_directions
        
        if use_ratio is not None:
            self.use_ratio = use_ratio
        
        if custom_directions is not None:
            self.custom_directions = custom_directions
        
        if custom_metric_fn is not None:
            self.custom_metric_fn = custom_metric_fn
        
        # Check if required components are available
        if self.model is None:
            raise ValueError("Model is required for surface computation")
        
        if self.surface_type != SurfaceType.CUSTOM and self.loss_fn is None:
            raise ValueError("Loss function is required for surface computation")
        
        if self.dataloader is None:
            raise ValueError("Dataloader is required for surface computation")
        
        if self.surface_type == SurfaceType.CUSTOM and self.custom_metric_fn is None:
            raise ValueError("Custom metric function is required for custom surface type")
        
        # Compute asynchronously if requested
        if async_compute:
            self._start_async_computation()
            return None
        
        # Compute synchronously
        return self._compute_surface_internal()
    
    def _start_async_computation(self) -> None:
        """Start asynchronous surface computation."""
        if self.computation_active:
            logger.warning("Surface computation is already in progress")
            return
        
        self.computation_active = True
        self.computation_thread = threading.Thread(
            target=self._async_computation_thread,
            daemon=True,
        )
        self.computation_thread.start()
        
        logger.info("Started asynchronous surface computation")
    
    def _async_computation_thread(self) -> None:
        """Thread function for asynchronous surface computation."""
        try:
            with self.lock:
                surface_data = self._compute_surface_internal()
                self.current_surface = surface_data
            
            logger.info("Completed asynchronous surface computation")
        except Exception as e:
            logger.error(f"Error in surface computation: {e}")
        finally:
            self.computation_active = False
    
    def _compute_surface_internal(self) -> Dict[str, Any]:
        """
        Internal function to compute the loss surface.
        
        Returns:
            Surface data
        """
        # Get current model parameters
        current_params = self._get_model_parameters()
        
        # Compute projection directions
        if self.projection_directions is None or self.projection_method != ProjectionMethod.CUSTOM:
            self.projection_directions = self._compute_projection_directions(current_params)
        
        # Create parameter grid
        alpha_values = np.linspace(self.alpha_range[0], self.alpha_range[1], self.resolution)
        beta_values = np.linspace(self.beta_range[0], self.beta_range[1], self.resolution)
        
        # Initialize surface grid
        surface_grid = np.zeros((self.resolution, self.resolution))
        
        # Compute surface values
        total_points = self.resolution * self.resolution
        points_computed = 0
        
        logger.info(f"Computing {self.surface_type.value} with {self.projection_method.value} projection")
        logger.info(f"Grid resolution: {self.resolution}x{self.resolution}")
        
        start_time = time.time()
        
        for i, alpha in enumerate(alpha_values):
            for j, beta in enumerate(beta_values):
                # Update parameters
                self._set_model_parameters(
                    self._perturb_parameters(
                        current_params,
                        self.projection_directions[0],
                        self.projection_directions[1],
                        alpha,
                        beta,
                    )
                )
                
                # Compute surface value
                surface_grid[i, j] = self._compute_surface_value()
                
                # Update progress
                points_computed += 1
                if points_computed % max(1, total_points // 10) == 0:
                    progress = points_computed / total_points * 100
                    elapsed = time.time() - start_time
                    eta = elapsed / points_computed * (total_points - points_computed)
                    logger.info(f"Progress: {progress:.1f}% ({points_computed}/{total_points}), ETA: {eta:.1f}s")
        
        # Restore original parameters
        self._set_model_parameters(current_params)
        
        # Create surface data
        surface_data = {
            "surface_type": self.surface_type.value,
            "projection_method": self.projection_method.value,
            "resolution": self.resolution,
            "alpha_range": self.alpha_range,
            "beta_range": self.beta_range,
            "alpha_values": alpha_values.tolist(),
            "beta_values": beta_values.tolist(),
            "surface_grid": surface_grid.tolist(),
            "computation_time": time.time() - start_time,
        }
        
        # Store as current surface
        self.current_surface = surface_data
        
        logger.info(f"Completed surface computation in {surface_data['computation_time']:.2f}s")
        
        return surface_data
    
    def _get_model_parameters(self) -> List[torch.Tensor]:
        """
        Get current model parameters.
        
        Returns:
            List of parameter tensors
        """
        return [p.data.clone() for p in self.model.parameters() if p.requires_grad]
    
    def _set_model_parameters(self, parameters: List[torch.Tensor]) -> None:
        """
        Set model parameters.
        
        Args:
            parameters: List of parameter tensors
        """
        for param, param_data in zip([p for p in self.model.parameters() if p.requires_grad], parameters):
            param.data.copy_(param_data)
    
    def _compute_projection_directions(self, current_params: List[torch.Tensor]) -> List[List[torch.Tensor]]:
        """
        Compute projection directions based on the selected method.
        
        Args:
            current_params: Current model parameters
            
        Returns:
            List of projection directions
        """
        if self.projection_method == ProjectionMethod.CUSTOM:
            if self.custom_directions is None or len(self.custom_directions) < 2:
                raise ValueError("Custom directions are required for custom projection method")
            
            return self.custom_directions
        
        elif self.projection_method == ProjectionMethod.RANDOM:
            # Create random directions
            direction1 = [torch.randn_like(p) for p in current_params]
            direction2 = [torch.randn_like(p) for p in current_params]
            
            # Make direction2 orthogonal to direction1
            if self.normalize_directions:
                # Compute dot product
                dot_product = sum(torch.sum(d1 * d2) for d1, d2 in zip(direction1, direction2))
                
                # Compute norm of direction1
                norm1 = math.sqrt(sum(torch.sum(d * d) for d in direction1))
                
                # Make direction2 orthogonal to direction1
                direction2 = [d2 - (dot_product / (norm1 * norm1)) * d1 
                             for d1, d2 in zip(direction1, direction2)]
            
            # Normalize directions
            if self.normalize_directions:
                # Normalize direction1
                norm1 = math.sqrt(sum(torch.sum(d * d) for d in direction1))
                direction1 = [d / norm1 for d in direction1]
                
                # Normalize direction2
                norm2 = math.sqrt(sum(torch.sum(d * d) for d in direction2))
                direction2 = [d / norm2 for d in direction2]
            
            return [direction1, direction2]
        
        elif self.projection_method == ProjectionMethod.PCA:
            # Flatten parameters
            flat_params = torch.cat([p.view(-1) for p in current_params])
            
            # Check if we have optimization history
            if len(self.optimization_path) < 3:
                logger.warning("Not enough optimization history for PCA, falling back to random projection")
                return self._compute_projection_directions(current_params)
            
            # Create matrix of parameter history
            param_history = torch.stack([torch.cat([p.view(-1) for p in params]) 
                                        for params in self.optimization_path[-20:]])
            
            # Center the data
            param_history = param_history - param_history.mean(dim=0, keepdim=True)
            
            # Compute PCA
            try:
                U, S, V = torch.pca_lowrank(param_history, q=2)
                
                # Extract principal components
                pc1 = V[:, 0]
                pc2 = V[:, 1]
                
                # Reshape back to parameter shapes
                direction1 = []
                direction2 = []
                
                idx = 0
                for p in current_params:
                    size = p.numel()
                    direction1.append(pc1[idx:idx+size].view_as(p))
                    direction2.append(pc2[idx:idx+size].view_as(p))
                    idx += size
                
                # Normalize directions
                if self.normalize_directions:
                    # Normalize direction1
                    norm1 = math.sqrt(sum(torch.sum(d * d) for d in direction1))
                    direction1 = [d / norm1 for d in direction1]
                    
                    # Normalize direction2
                    norm2 = math.sqrt(sum(torch.sum(d * d) for d in direction2))
                    direction2 = [d / norm2 for d in direction2]
                
                return [direction1, direction2]
            
            except Exception as e:
                logger.warning(f"Error computing PCA: {e}, falling back to random projection")
                return self._compute_projection_directions(current_params)
        
        elif self.projection_method == ProjectionMethod.FILTER:
            # Select specific filters or channels
            # This is a simplified implementation - in practice, you would
            # select specific filters or channels based on importance metrics
            
            # Get first convolutional layer
            conv_layer = None
            for module in self.model.modules():
                if isinstance(module, (nn.Conv1d, nn.Conv2d, nn.Conv3d)):
                    conv_layer = module
                    break
            
            if conv_layer is None:
                logger.warning("No convolutional layer found, falling back to random projection")
                return self._compute_projection_directions(current_params)
            
            # Get weight parameter
            weight = None
            for name, param in self.model.named_parameters():
                if param.requires_grad and "weight" in name and param.shape == conv_layer.weight.shape:
                    weight = param
                    break
            
            if weight is None:
                logger.warning("Could not find weight parameter, falling back to random projection")
                return self._compute_projection_directions(current_params)
            
            # Create filter directions
            direction1 = [torch.zeros_like(p) for p in current_params]
            direction2 = [torch.zeros_like(p) for p in current_params]
            
            # Set first filter in first direction
            for i, (p, d1, d2) in enumerate(zip(current_params, direction1, direction2)):
                if p.shape == weight.shape:
                    if p.dim() >= 4:  # Conv weight
                        d1[0, :, :, :] = 1.0
                        d2[1, :, :, :] = 1.0
                    elif p.dim() == 2:  # Linear weight
                        d1[0, :] = 1.0
                        d2[1, :] = 1.0
                    break
            
            # Normalize directions
            if self.normalize_directions:
                # Normalize direction1
                norm1 = math.sqrt(sum(torch.sum(d * d) for d in direction1))
                direction1 = [d / norm1 for d in direction1]
                
                # Normalize direction2
                norm2 = math.sqrt(sum(torch.sum(d * d) for d in direction2))
                direction2 = [d / norm2 for d in direction2]
            
            return [direction1, direction2]
        
        elif self.projection_method == ProjectionMethod.LAYER:
            # Project along specific layers
            # This is a simplified implementation - in practice, you would
            # select specific layers based on importance metrics
            
            # Find two different parameter groups
            param_groups = []
            current_group = []
            
            for module in self.model.modules():
                if isinstance(module, (nn.Linear, nn.Conv1d, nn.Conv2d, nn.Conv3d)):
                    if current_group:
                        param_groups.append(current_group)
                        current_group = []
                    
                    for name, param in module.named_parameters():
                        if param.requires_grad:
                            current_group.append(id(param))
            
            if current_group:
                param_groups.append(current_group)
            
            if len(param_groups) < 2:
                logger.warning("Not enough parameter groups, falling back to random projection")
                return self._compute_projection_directions(current_params)
            
            # Create layer directions
            direction1 = [torch.zeros_like(p) for p in current_params]
            direction2 = [torch.zeros_like(p) for p in current_params]
            
            # Set first group in first direction, second group in second direction
            param_ids = [id(p) for p in self.model.parameters() if p.requires_grad]
            
            for i, p_id in enumerate(param_ids):
                if i < len(current_params):
                    if p_id in param_groups[0]:
                        direction1[i].fill_(1.0)
                    elif len(param_groups) > 1 and p_id in param_groups[1]:
                        direction2[i].fill_(1.0)
            
            # Normalize directions
            if self.normalize_directions:
                # Normalize direction1
                norm1 = math.sqrt(sum(torch.sum(d * d) for d in direction1))
                if norm1 > 0:
                    direction1 = [d / norm1 for d in direction1]
                
                # Normalize direction2
                norm2 = math.sqrt(sum(torch.sum(d * d) for d in direction2))
                if norm2 > 0:
                    direction2 = [d / norm2 for d in direction2]
            
            return [direction1, direction2]
        
        elif self.projection_method == ProjectionMethod.TSNE:
            # This is a simplified implementation - in practice, t-SNE
            # would be computed on the parameter history
            
            # Check if we have optimization history
            if len(self.optimization_path) < 3:
                logger.warning("Not enough optimization history for t-SNE, falling back to random projection")
                return self._compute_projection_directions(current_params)
            
            # Create matrix of parameter history
            param_history = np.array([torch.cat([p.view(-1) for p in params]).cpu().numpy() 
                                     for params in self.optimization_path[-20:]])
            
            # Compute t-SNE
            try:
                # Use PCA to reduce dimensionality first if parameter space is very large
                if param_history.shape[1] > 10000:
                    pca = PCA(n_components=100)
                    param_history = pca.fit_transform(param_history)
                
                # Compute t-SNE
                tsne = TSNE(n_components=2, random_state=42)
                tsne_result = tsne.fit_transform(param_history)
                
                # Get directions from t-SNE axes
                direction1 = []
                direction2 = []
                
                # This is a simplification - in practice, you would need to
                # map the t-SNE directions back to the parameter space
                for p in current_params:
                    direction1.append(torch.randn_like(p))
                    direction2.append(torch.randn_like(p))
                
                # Make direction2 orthogonal to direction1
                if self.normalize_directions:
                    # Compute dot product
                    dot_product = sum(torch.sum(d1 * d2) for d1, d2 in zip(direction1, direction2))
                    
                    # Compute norm of direction1
                    norm1 = math.sqrt(sum(torch.sum(d * d) for d in direction1))
                    
                    # Make direction2 orthogonal to direction1
                    direction2 = [d2 - (dot_product / (norm1 * norm1)) * d1 
                                 for d1, d2 in zip(direction1, direction2)]
                
                # Normalize directions
                if self.normalize_directions:
                    # Normalize direction1
                    norm1 = math.sqrt(sum(torch.sum(d * d) for d in direction1))
                    direction1 = [d / norm1 for d in direction1]
                    
                    # Normalize direction2
                    norm2 = math.sqrt(sum(torch.sum(d * d) for d in direction2))
                    direction2 = [d / norm2 for d in direction2]
                
                return [direction1, direction2]
            
            except Exception as e:
                logger.warning(f"Error computing t-SNE: {e}, falling back to random projection")
                return self._compute_projection_directions(current_params)
        
        else:
            raise ValueError(f"Unknown projection method: {self.projection_method}")
    
    def _perturb_parameters(
        self,
        current_params: List[torch.Tensor],
        direction1: List[torch.Tensor],
        direction2: List[torch.Tensor],
        alpha: float,
        beta: float,
    ) -> List[torch.Tensor]:
        """
        Perturb parameters along the projection directions.
        
        Args:
            current_params: Current model parameters
            direction1: First projection direction
            direction2: Second projection direction
            alpha: Coefficient for the first direction
            beta: Coefficient for the second direction
            
        Returns:
            Perturbed parameters
        """
        if self.use_ratio:
            # Perturb parameters by ratio
            return [p + alpha * d1 * p + beta * d2 * p 
                   for p, d1, d2 in zip(current_params, direction1, direction2)]
        else:
            # Perturb parameters by absolute values
            return [p + alpha * d1 + beta * d2 
                   for p, d1, d2 in zip(current_params, direction1, direction2)]
    
    def _compute_surface_value(self) -> float:
        """
        Compute the surface value for the current model parameters.
        
        Returns:
            Surface value
        """
        # Set model to evaluation mode
        self.model.eval()
        
        # Compute surface value based on surface type
        if self.surface_type == SurfaceType.CUSTOM:
            # Use custom metric function
            return self.custom_metric_fn(self.model, self.dataloader, self.device)
        
        # For other surface types, we need to evaluate on the dataloader
        total_loss = 0.0
        total_samples = 0
        total_correct = 0
        
        # Disable gradient computation
        with torch.no_grad():
            for batch in self.dataloader:
                # Handle different batch formats
                if isinstance(batch, (list, tuple)) and len(batch) >= 2:
                    inputs, targets = batch[0], batch[1]
                elif isinstance(batch, dict):
                    inputs = batch.get("input") or batch.get("inputs") or batch.get("x")
                    targets = batch.get("target") or batch.get("targets") or batch.get("y") or batch.get("label") or batch.get("labels")
                else:
                    inputs, targets = batch, None
                
                # Move to device
                if isinstance(inputs, torch.Tensor):
                    inputs = inputs.to(self.device)
                
                if isinstance(targets, torch.Tensor):
                    targets = targets.to(self.device)
                
                # Forward pass
                outputs = self.model(inputs)
                
                # Compute loss
                if self.surface_type == SurfaceType.LOSS:
                    if targets is not None and self.loss_fn is not None:
                        loss = self.loss_fn(outputs, targets)
                        total_loss += loss.item() * inputs.size(0)
                        total_samples += inputs.size(0)
                
                # Compute gradient norm
                elif self.surface_type == SurfaceType.GRADIENT_NORM:
                    # Enable gradient computation for this part
                    with torch.enable_grad():
                        if targets is not None and self.loss_fn is not None:
                            # Forward pass with gradient
                            outputs = self.model(inputs)
                            loss = self.loss_fn(outputs, targets)
                            
                            # Compute gradients
                            loss.backward()
                            
                            # Compute gradient norm
                            grad_norm = 0.0
                            for p in self.model.parameters():
                                if p.grad is not None:
                                    grad_norm += p.grad.norm().item() ** 2
                            
                            grad_norm = math.sqrt(grad_norm)
                            
                            # Accumulate
                            total_loss += grad_norm * inputs.size(0)
                            total_samples += inputs.size(0)
                            
                            # Zero gradients
                            for p in self.model.parameters():
                                if p.grad is not None:
                                    p.grad.zero_()
                
                # Compute accuracy
                elif self.surface_type == SurfaceType.ACCURACY:
                    if targets is not None:
                        # Handle different output formats
                        if isinstance(outputs, torch.Tensor):
                            if outputs.size(-1) > 1:  # Classification
                                _, predicted = outputs.max(1)
                                total_correct += predicted.eq(targets).sum().item()
                            else:  # Regression or binary classification
                                predicted = (outputs > 0.5).float()
                                total_correct += predicted.eq(targets).sum().item()
                        
                        total_samples += targets.numel()
                
                # Compute Hessian eigenvalue (approximation)
                elif self.surface_type == SurfaceType.HESSIAN_EIGENVALUE:
                    # This is a simplified approximation of the Hessian eigenvalue
                    # In practice, you would use a more sophisticated method
                    
                    # Enable gradient computation for this part
                    with torch.enable_grad():
                        if targets is not None and self.loss_fn is not None:
                            # Forward pass with gradient
                            outputs = self.model(inputs)
                            loss = self.loss_fn(outputs, targets)
                            
                            # Compute gradients
                            loss.backward(create_graph=True)
                            
                            # Compute gradient norm
                            grad_norm = 0.0
                            grads = []
                            for p in self.model.parameters():
                                if p.grad is not None:
                                    grad_norm += p.grad.norm().item() ** 2
                                    grads.append(p.grad.view(-1))
                            
                            # Concatenate gradients
                            grads = torch.cat(grads)
                            
                            # Compute Hessian-vector product with the gradient
                            hvp = torch.autograd.grad(
                                grads,
                                self.model.parameters(),
                                grad_outputs=grads,
                                retain_graph=False,
                                create_graph=False,
                            )
                            
                            # Compute eigenvalue approximation
                            eigenvalue = sum(torch.sum(g * h) for g, h in zip(grads, hvp)) / (grad_norm + 1e-10)
                            
                            # Accumulate
                            total_loss += eigenvalue.item() * inputs.size(0)
                            total_samples += inputs.size(0)
                            
                            # Zero gradients
                            for p in self.model.parameters():
                                if p.grad is not None:
                                    p.grad.zero_()
                
                # Break after one batch for efficiency
                # In practice, you would use more batches for better estimates
                break
        
        # Compute final value
        if self.surface_type == SurfaceType.ACCURACY:
            return total_correct / max(1, total_samples)
        else:
            return total_loss / max(1, total_samples)
    
    def record_optimization_state(self, metrics: Optional[Dict[str, Any]] = None) -> None:
        """
        Record the current optimization state.
        
        Args:
            metrics: Additional metrics to record
        """
        # Get current model parameters
        current_params = self._get_model_parameters()
        
        # Create state record
        state = {
            "parameters": current_params,
            "timestamp": time.time(),
            "metrics": metrics or {},
        }
        
        # Add to history
        self.history.append(state)
        
        # Add to optimization path
        self.optimization_path.append(current_params)
        
        # Limit history size
        max_history = 100
        if len(self.history) > max_history:
            self.history = self.history[-max_history:]
        
        # Limit optimization path size
        max_path = 50
        if len(self.optimization_path) > max_path:
            self.optimization_path = self.optimization_path[-max_path:]
    
    def visualize_surface(
        self,
        output_path: Optional[str] = None,
        show: bool = False,
        plot_type: str = "3d",
        include_path: bool = True,
        title: Optional[str] = None,
        use_plotly: bool = False,
        colormap: str = "viridis",
    ) -> Optional[str]:
        """
        Visualize the loss surface.
        
        Args:
            output_path: Path to save the visualization
            show: Whether to show the visualization
            plot_type: Type of plot ("3d", "contour", or "both")
            include_path: Whether to include the optimization path
            title: Plot title
            use_plotly: Whether to use Plotly for interactive visualization
            colormap: Colormap to use
            
        Returns:
            Path to the saved visualization or None
        """
        if self.current_surface is None:
            logger.warning("No surface data available for visualization")
            return None
        
        # Extract surface data
        surface_type = self.current_surface["surface_type"]
        projection_method = self.current_surface["projection_method"]
        alpha_values = np.array(self.current_surface["alpha_values"])
        beta_values = np.array(self.current_surface["beta_values"])
        surface_grid = np.array(self.current_surface["surface_grid"])
        
        # Create meshgrid
        alpha_mesh, beta_mesh = np.meshgrid(alpha_values, beta_values)
        
        # Generate title if not provided
        if title is None:
            title = f"{surface_type.replace('_', ' ').title()} with {projection_method.replace('_', ' ').title()}"
        
        # Create visualization
        if use_plotly:
            return self._visualize_surface_plotly(
                alpha_mesh,
                beta_mesh,
                surface_grid,
                output_path,
                show,
                plot_type,
                include_path,
                title,
                colormap,
            )
        else:
            return self._visualize_surface_matplotlib(
                alpha_mesh,
                beta_mesh,
                surface_grid,
                output_path,
                show,
                plot_type,
                include_path,
                title,
                colormap,
            )
    
    def _visualize_surface_matplotlib(
        self,
        alpha_mesh: np.ndarray,
        beta_mesh: np.ndarray,
        surface_grid: np.ndarray,
        output_path: Optional[str] = None,
        show: bool = False,
        plot_type: str = "3d",
        include_path: bool = True,
        title: str = "",
        colormap: str = "viridis",
    ) -> Optional[str]:
        """
        Visualize the loss surface using Matplotlib.
        
        Args:
            alpha_mesh: Mesh grid for alpha values
            beta_mesh: Mesh grid for beta values
            surface_grid: Surface values
            output_path: Path to save the visualization
            show: Whether to show the visualization
            plot_type: Type of plot ("3d", "contour", or "both")
            include_path: Whether to include the optimization path
            title: Plot title
            colormap: Colormap to use
            
        Returns:
            Path to the saved visualization or None
        """
        if plot_type == "both":
            fig = plt.figure(figsize=(18, 8))
            ax1 = fig.add_subplot(121, projection="3d")
            ax2 = fig.add_subplot(122)
        elif plot_type == "3d":
            fig = plt.figure(figsize=(10, 8))
            ax1 = fig.add_subplot(111, projection="3d")
            ax2 = None
        else:  # contour
            fig = plt.figure(figsize=(10, 8))
            ax1 = None
            ax2 = fig.add_subplot(111)
        
        # Plot 3D surface
        if ax1 is not None:
            surf = ax1.plot_surface(
                alpha_mesh,
                beta_mesh,
                surface_grid,
                cmap=colormap,
                linewidth=0,
                antialiased=True,
                alpha=0.8,
            )
            
            # Add color bar
            fig.colorbar(surf, ax=ax1, shrink=0.5, aspect=5)
            
            # Add labels
            ax1.set_xlabel("Direction 1")
            ax1.set_ylabel("Direction 2")
            ax1.set_zlabel("Value")
            
            # Add title
            ax1.set_title(title)
            
            # Add optimization path if available
            if include_path and len(self.optimization_path) > 1 and self.projection_directions is not None:
                # Project optimization path onto the 2D plane
                path_coords = self._project_optimization_path()
                
                if path_coords is not None:
                    # Extract coordinates
                    alphas, betas, values = path_coords
                    
                    # Plot path
                    ax1.plot(alphas, betas, values, "r-", linewidth=2, label="Optimization Path")
                    ax1.plot(alphas, betas, values, "ro", markersize=4)
                    
                    # Add start and end points
                    ax1.plot([alphas[0]], [betas[0]], [values[0]], "go", markersize=8, label="Start")
                    ax1.plot([alphas[-1]], [betas[-1]], [values[-1]], "bo", markersize=8, label="Current")
                    
                    # Add legend
                    ax1.legend()
        
        # Plot contour
        if ax2 is not None:
            contour = ax2.contourf(alpha_mesh, beta_mesh, surface_grid, 50, cmap=colormap)
            
            # Add color bar
            fig.colorbar(contour, ax=ax2)
            
            # Add labels
            ax2.set_xlabel("Direction 1")
            ax2.set_ylabel("Direction 2")
            
            # Add title
            ax2.set_title(title)
            
            # Add optimization path if available
            if include_path and len(self.optimization_path) > 1 and self.projection_directions is not None:
                # Project optimization path onto the 2D plane
                path_coords = self._project_optimization_path()
                
                if path_coords is not None:
                    # Extract coordinates
                    alphas, betas, _ = path_coords
                    
                    # Plot path
                    ax2.plot(alphas, betas, "r-", linewidth=2, label="Optimization Path")
                    ax2.plot(alphas, betas, "ro", markersize=4)
                    
                    # Add start and end points
                    ax2.plot([alphas[0]], [betas[0]], "go", markersize=8, label="Start")
                    ax2.plot([alphas[-1]], [betas[-1]], "bo", markersize=8, label="Current")
                    
                    # Add legend
                    ax2.legend()
        
        # Adjust layout
        plt.tight_layout()
        
        # Save or show
        if output_path:
            plt.savefig(output_path, bbox_inches="tight", dpi=300)
            logger.info(f"Saved surface visualization to {output_path}")
        
        if show:
            plt.show()
        
        plt.close()
        
        return output_path
    
    def _visualize_surface_plotly(
        self,
        alpha_mesh: np.ndarray,
        beta_mesh: np.ndarray,
        surface_grid: np.ndarray,
        output_path: Optional[str] = None,
        show: bool = False,
        plot_type: str = "3d",
        include_path: bool = True,
        title: str = "",
        colormap: str = "viridis",
    ) -> Optional[str]:
        """
        Visualize the loss surface using Plotly.
        
        Args:
            alpha_mesh: Mesh grid for alpha values
            beta_mesh: Mesh grid for beta values
            surface_grid: Surface values
            output_path: Path to save the visualization
            show: Whether to show the visualization
            plot_type: Type of plot ("3d", "contour", or "both")
            include_path: Whether to include the optimization path
            title: Plot title
            colormap: Colormap to use
            
        Returns:
            Path to the saved visualization or None
        """
        if plot_type == "both":
            fig = make_subplots(
                rows=1,
                cols=2,
                specs=[[{"type": "surface"}, {"type": "contour"}]],
                subplot_titles=["3D Surface", "Contour Plot"],
            )
        elif plot_type == "3d":
            fig = go.Figure()
        else:  # contour
            fig = go.Figure()
        
        # Plot 3D surface
        if plot_type in ["3d", "both"]:
            surface = go.Surface(
                x=alpha_mesh,
                y=beta_mesh,
                z=surface_grid,
                colorscale=colormap,
                opacity=0.8,
            )
            
            if plot_type == "both":
                fig.add_trace(surface, row=1, col=1)
            else:
                fig.add_trace(surface)
            
            # Add optimization path if available
            if include_path and len(self.optimization_path) > 1 and self.projection_directions is not None:
                # Project optimization path onto the 2D plane
                path_coords = self._project_optimization_path()
                
                if path_coords is not None:
                    # Extract coordinates
                    alphas, betas, values = path_coords
                    
                    # Plot path
                    path = go.Scatter3d(
                        x=alphas,
                        y=betas,
                        z=values,
                        mode="lines+markers",
                        line=dict(color="red", width=4),
                        marker=dict(size=4, color="red"),
                        name="Optimization Path",
                    )
                    
                    # Add start and end points
                    start = go.Scatter3d(
                        x=[alphas[0]],
                        y=[betas[0]],
                        z=[values[0]],
                        mode="markers",
                        marker=dict(size=8, color="green"),
                        name="Start",
                    )
                    
                    end = go.Scatter3d(
                        x=[alphas[-1]],
                        y=[betas[-1]],
                        z=[values[-1]],
                        mode="markers",
                        marker=dict(size=8, color="blue"),
                        name="Current",
                    )
                    
                    if plot_type == "both":
                        fig.add_trace(path, row=1, col=1)
                        fig.add_trace(start, row=1, col=1)
                        fig.add_trace(end, row=1, col=1)
                    else:
                        fig.add_trace(path)
                        fig.add_trace(start)
                        fig.add_trace(end)
        
        # Plot contour
        if plot_type in ["contour", "both"]:
            contour = go.Contour(
                x=alpha_mesh[0],
                y=beta_mesh[:, 0],
                z=surface_grid,
                colorscale=colormap,
                contours=dict(
                    showlabels=True,
                    labelfont=dict(size=12, color="white"),
                ),
            )
            
            if plot_type == "both":
                fig.add_trace(contour, row=1, col=2)
            else:
                fig.add_trace(contour)
            
            # Add optimization path if available
            if include_path and len(self.optimization_path) > 1 and self.projection_directions is not None:
                # Project optimization path onto the 2D plane
                path_coords = self._project_optimization_path()
                
                if path_coords is not None:
                    # Extract coordinates
                    alphas, betas, _ = path_coords
                    
                    # Plot path
                    path = go.Scatter(
                        x=alphas,
                        y=betas,
                        mode="lines+markers",
                        line=dict(color="red", width=2),
                        marker=dict(size=4, color="red"),
                        name="Optimization Path",
                    )
                    
                    # Add start and end points
                    start = go.Scatter(
                        x=[alphas[0]],
                        y=[betas[0]],
                        mode="markers",
                        marker=dict(size=8, color="green"),
                        name="Start",
                    )
                    
                    end = go.Scatter(
                        x=[alphas[-1]],
                        y=[betas[-1]],
                        mode="markers",
                        marker=dict(size=8, color="blue"),
                        name="Current",
                    )
                    
                    if plot_type == "both":
                        fig.add_trace(path, row=1, col=2)
                        fig.add_trace(start, row=1, col=2)
                        fig.add_trace(end, row=1, col=2)
                    else:
                        fig.add_trace(path)
                        fig.add_trace(start)
                        fig.add_trace(end)
        
        # Update layout
        fig.update_layout(
            title=title,
            scene=dict(
                xaxis_title="Direction 1",
                yaxis_title="Direction 2",
                zaxis_title="Value",
            ),
            xaxis=dict(title="Direction 1"),
            yaxis=dict(title="Direction 2"),
            height=800,
            width=1200 if plot_type == "both" else 800,
        )
        
        # Save or show
        if output_path:
            fig.write_html(output_path)
            logger.info(f"Saved interactive surface visualization to {output_path}")
        
        if show:
            fig.show()
        
        return output_path
    
    def _project_optimization_path(self) -> Optional[Tuple[List[float], List[float], List[float]]]:
        """
        Project the optimization path onto the 2D plane defined by the projection directions.
        
        Returns:
            Tuple of (alphas, betas, values) or None
        """
        if not self.optimization_path or not self.projection_directions:
            return None
        
        # Get current parameters
        current_params = self._get_model_parameters()
        
        # Get projection directions
        direction1, direction2 = self.projection_directions
        
        # Project each point in the optimization path
        alphas = []
        betas = []
        values = []
        
        for params in self.optimization_path:
            # Compute parameter difference
            param_diff = [p - c for p, c in zip(params, current_params)]
            
            # Compute projections
            if self.use_ratio:
                # Project using ratio
                alpha = sum(torch.sum(d * diff / c) for d, diff, c in zip(direction1, param_diff, current_params) if c.abs().sum() > 0)
                beta = sum(torch.sum(d * diff / c) for d, diff, c in zip(direction2, param_diff, current_params) if c.abs().sum() > 0)
            else:
                # Project using absolute values
                alpha = sum(torch.sum(d * diff) for d, diff in zip(direction1, param_diff))
                beta = sum(torch.sum(d * diff) for d, diff in zip(direction2, param_diff))
            
            # Convert to Python floats
            alphas.append(alpha.item())
            betas.append(beta.item())
            
            # Compute surface value at this point
            # For simplicity, we'll interpolate from the surface grid
            # In practice, you might want to compute the actual value
            
            # Find closest grid points
            alpha_idx = np.argmin(np.abs(np.array(self.current_surface["alpha_values"]) - alpha.item()))
            beta_idx = np.argmin(np.abs(np.array(self.current_surface["beta_values"]) - beta.item()))
            
            # Get surface value
            value = self.current_surface["surface_grid"][alpha_idx][beta_idx]
            values.append(value)
        
        return alphas, betas, values
    
    def analyze_surface(self) -> Dict[str, Any]:
        """
        Analyze the loss surface for interesting features.
        
        Returns:
            Dictionary of analysis results
        """
        if self.current_surface is None:
            return {"error": "No surface data available for analysis"}
        
        # Extract surface data
        surface_grid = np.array(self.current_surface["surface_grid"])
        
        # Initialize results
        results = {
            "min_value": float(np.min(surface_grid)),
            "max_value": float(np.max(surface_grid)),
            "mean_value": float(np.mean(surface_grid)),
            "std_value": float(np.std(surface_grid)),
            "features": [],
        }
        
        # Find local minima
        local_minima = []
        for i in range(1, surface_grid.shape[0] - 1):
            for j in range(1, surface_grid.shape[1] - 1):
                if (surface_grid[i, j] < surface_grid[i-1, j] and
                    surface_grid[i, j] < surface_grid[i+1, j] and
                    surface_grid[i, j] < surface_grid[i, j-1] and
                    surface_grid[i, j] < surface_grid[i, j+1]):
                    local_minima.append((i, j, surface_grid[i, j]))
        
        # Sort local minima by value
        local_minima.sort(key=lambda x: x[2])
        
        # Add to results
        results["num_local_minima"] = len(local_minima)
        if local_minima:
            results["global_minimum"] = {
                "alpha_idx": int(local_minima[0][0]),
                "beta_idx": int(local_minima[0][1]),
                "value": float(local_minima[0][2]),
                "alpha": float(self.current_surface["alpha_values"][local_minima[0][0]]),
                "beta": float(self.current_surface["beta_values"][local_minima[0][1]]),
            }
            
            # Add feature
            results["features"].append({
                "type": "global_minimum",
                "description": "Global minimum of the surface",
                "location": (
                    float(self.current_surface["alpha_values"][local_minima[0][0]]),
                    float(self.current_surface["beta_values"][local_minima[0][1]]),
                ),
                "value": float(local_minima[0][2]),
            })
        
        # Find local maxima
        local_maxima = []
        for i in range(1, surface_grid.shape[0] - 1):
            for j in range(1, surface_grid.shape[1] - 1):
                if (surface_grid[i, j] > surface_grid[i-1, j] and
                    surface_grid[i, j] > surface_grid[i+1, j] and
                    surface_grid[i, j] > surface_grid[i, j-1] and
                    surface_grid[i, j] > surface_grid[i, j+1]):
                    local_maxima.append((i, j, surface_grid[i, j]))
        
        # Sort local maxima by value (descending)
        local_maxima.sort(key=lambda x: -x[2])
        
        # Add to results
        results["num_local_maxima"] = len(local_maxima)
        if local_maxima:
            results["global_maximum"] = {
                "alpha_idx": int(local_maxima[0][0]),
                "beta_idx": int(local_maxima[0][1]),
                "value": float(local_maxima[0][2]),
                "alpha": float(self.current_surface["alpha_values"][local_maxima[0][0]]),
                "beta": float(self.current_surface["beta_values"][local_maxima[0][1]]),
            }
            
            # Add feature
            results["features"].append({
                "type": "global_maximum",
                "description": "Global maximum of the surface",
                "location": (
                    float(self.current_surface["alpha_values"][local_maxima[0][0]]),
                    float(self.current_surface["beta_values"][local_maxima[0][1]]),
                ),
                "value": float(local_maxima[0][2]),
            })
        
        # Compute gradient magnitude
        gradient_y, gradient_x = np.gradient(surface_grid)
        gradient_magnitude = np.sqrt(gradient_x**2 + gradient_y**2)
        
        # Find steep regions
        steep_threshold = np.percentile(gradient_magnitude, 90)  # Top 10% steepest regions
        steep_regions = np.where(gradient_magnitude > steep_threshold)
        
        # Add to results
        results["max_gradient"] = float(np.max(gradient_magnitude))
        results["mean_gradient"] = float(np.mean(gradient_magnitude))
        results["num_steep_regions"] = len(steep_regions[0])
        
        if len(steep_regions[0]) > 0:
            # Find steepest point
            steepest_idx = np.argmax(gradient_magnitude)
            steepest_i, steepest_j = np.unravel_index(steepest_idx, gradient_magnitude.shape)
            
            results["steepest_point"] = {
                "alpha_idx": int(steepest_i),
                "beta_idx": int(steepest_j),
                "gradient": float(gradient_magnitude[steepest_i, steepest_j]),
                "alpha": float(self.current_surface["alpha_values"][steepest_i]),
                "beta": float(self.current_surface["beta_values"][steepest_j]),
            }
            
            # Add feature
            results["features"].append({
                "type": "steep_cliff",
                "description": "Steepest region of the surface",
                "location": (
                    float(self.current_surface["alpha_values"][steepest_i]),
                    float(self.current_surface["beta_values"][steepest_j]),
                ),
                "gradient": float(gradient_magnitude[steepest_i, steepest_j]),
            })
        
        # Find flat regions (plateaus)
        flat_threshold = np.percentile(gradient_magnitude, 10)  # Bottom 10% flattest regions
        flat_regions = np.where(gradient_magnitude < flat_threshold)
        
        # Add to results
        results["num_flat_regions"] = len(flat_regions[0])
        
        if len(flat_regions[0]) > 0:
            # Find flattest point
            flattest_idx = np.argmin(gradient_magnitude)
            flattest_i, flattest_j = np.unravel_index(flattest_idx, gradient_magnitude.shape)
            
            results["flattest_point"] = {
                "alpha_idx": int(flattest_i),
                "beta_idx": int(flattest_j),
                "gradient": float(gradient_magnitude[flattest_i, flattest_j]),
                "alpha": float(self.current_surface["alpha_values"][flattest_i]),
                "beta": float(self.current_surface["beta_values"][flattest_j]),
            }
            
            # Add feature
            results["features"].append({
                "type": "plateau",
                "description": "Flattest region of the surface",
                "location": (
                    float(self.current_surface["alpha_values"][flattest_i]),
                    float(self.current_surface["beta_values"][flattest_j]),
                ),
                "gradient": float(gradient_magnitude[flattest_i, flattest_j]),
            })
        
        # Find saddle points (local minima in one direction, local maxima in another)
        saddle_points = []
        for i in range(1, surface_grid.shape[0] - 1):
            for j in range(1, surface_grid.shape[1] - 1):
                # Check if minimum along rows and maximum along columns (or vice versa)
                min_along_row = (surface_grid[i, j] < surface_grid[i, j-1] and
                                surface_grid[i, j] < surface_grid[i, j+1])
                max_along_row = (surface_grid[i, j] > surface_grid[i, j-1] and
                                surface_grid[i, j] > surface_grid[i, j+1])
                min_along_col = (surface_grid[i, j] < surface_grid[i-1, j] and
                                surface_grid[i, j] < surface_grid[i+1, j])
                max_along_col = (surface_grid[i, j] > surface_grid[i-1, j] and
                                surface_grid[i, j] > surface_grid[i+1, j])
                
                if (min_along_row and max_along_col) or (max_along_row and min_along_col):
                    saddle_points.append((i, j, surface_grid[i, j]))
        
        # Add to results
        results["num_saddle_points"] = len(saddle_points)
        
        if saddle_points:
            # Add feature for each saddle point
            for i, (si, sj, sv) in enumerate(saddle_points[:5]):  # Limit to top 5
                results["features"].append({
                    "type": "saddle_point",
                    "description": f"Saddle point {i+1}",
                    "location": (
                        float(self.current_surface["alpha_values"][si]),
                        float(self.current_surface["beta_values"][sj]),
                    ),
                    "value": float(sv),
                })
        
        # Analyze optimization path if available
        if len(self.optimization_path) > 1 and self.projection_directions is not None:
            path_coords = self._project_optimization_path()
            
            if path_coords is not None:
                # Extract coordinates
                alphas, betas, values = path_coords
                
                # Compute path length
                path_length = 0.0
                for i in range(1, len(alphas)):
                    path_length += math.sqrt((alphas[i] - alphas[i-1])**2 + 
                                            (betas[i] - betas[i-1])**2)
                
                # Compute path descent
                path_descent = values[0] - values[-1]
                
                # Add to results
                results["path_length"] = float(path_length)
                results["path_descent"] = float(path_descent)
                results["path_efficiency"] = float(path_descent / max(path_length, 1e-10))
                
                # Check if path is near any features
                for feature in results["features"]:
                    feature_loc = feature["location"]
                    
                    # Compute minimum distance from path to feature
                    min_dist = float('inf')
                    for i in range(len(alphas)):
                        dist = math.sqrt((alphas[i] - feature_loc[0])**2 + 
                                        (betas[i] - feature_loc[1])**2)
                        min_dist = min(min_dist, dist)
                    
                    # Add distance to feature
                    feature["min_distance_from_path"] = float(min_dist)
                    
                    # Check if path passes near feature
                    if min_dist < 0.1 * (self.alpha_range[1] - self.alpha_range[0]):
                        feature["path_passes_nearby"] = True
                    else:
                        feature["path_passes_nearby"] = False
        
        return results
    
    def get_surface_data(self) -> Optional[Dict[str, Any]]:
        """
        Get the current surface data.
        
        Returns:
            Surface data or None if not available
        """
        return self.current_surface
    
    def get_optimization_path(self) -> List[List[torch.Tensor]]:
        """
        Get the optimization path.
        
        Returns:
            List of parameter states
        """
        return self.optimization_path
    
    def get_history(self) -> List[Dict[str, Any]]:
        """
        Get the history of parameter states and metrics.
        
        Returns:
            List of state records
        """
        return self.history
    
    def save_surface(self, path: str) -> None:
        """
        Save the current surface data to a file.
        
        Args:
            path: Path to save the surface data
        """
        if self.current_surface is None:
            logger.warning("No surface data available to save")
            return
        
        try:
            with open(path, 'w') as f:
                json.dump(self.current_surface, f, indent=2)
            
            logger.info(f"Saved surface data to {path}")
        except Exception as e:
            logger.error(f"Failed to save surface data: {e}")
    
    def load_surface(self, path: str) -> bool:
        """
        Load surface data from a file.
        
        Args:
            path: Path to load the surface data from
            
        Returns:
            True if successful, False otherwise
        """
        try:
            with open(path, 'r') as f:
                self.current_surface = json.load(f)
            
            logger.info(f"Loaded surface data from {path}")
            return True
        except Exception as e:
            logger.error(f"Failed to load surface data: {e}")
            return False
    
    def save_state(self, path: str) -> None:
        """
        Save the module state to a file.
        
        Args:
            path: Path to save the state
        """
        state = {
            "current_surface": self.current_surface,
            "projection_method": self.projection_method.value,
            "surface_type": self.surface_type.value,
            "resolution": self.resolution,
            "alpha_range": self.alpha_range,
            "beta_range": self.beta_range,
            "normalize_directions": self.normalize_directions,
            "use_ratio": self.use_ratio,
        }
        
        try:
            with open(path, 'w') as f:
                json.dump(state, f, indent=2)
            
            logger.info(f"Saved LatentLossSurfaceMapping state to {path}")
        except Exception as e:
            logger.error(f"Failed to save state: {e}")
    
    def load_state(self, path: str) -> bool:
        """
        Load the module state from a file.
        
        Args:
            path: Path to load the state from
            
        Returns:
            True if successful, False otherwise
        """
        try:
            with open(path, 'r') as f:
                state = json.load(f)
            
            self.current_surface = state["current_surface"]
            self.projection_method = ProjectionMethod(state["projection_method"])
            self.surface_type = SurfaceType(state["surface_type"])
            self.resolution = state["resolution"]
            self.alpha_range = tuple(state["alpha_range"])
            self.beta_range = tuple(state["beta_range"])
            self.normalize_directions = state["normalize_directions"]
            self.use_ratio = state["use_ratio"]
            
            logger.info(f"Loaded LatentLossSurfaceMapping state from {path}")
            return True
        except Exception as e:
            logger.error(f"Failed to load state: {e}")
            return False
    
    def reset(self) -> None:
        """Reset the module state."""
        # Stop computation if active
        if self.computation_active:
            self.computation_active = False
            if self.computation_thread is not None:
                self.computation_thread.join(timeout=1.0)
                self.computation_thread = None
        
        # Reset state
        self.current_surface = None
        self.projection_directions = None
        self.history = []
        self.optimization_path = []
        
        logger.info("Reset LatentLossSurfaceMapping state")
