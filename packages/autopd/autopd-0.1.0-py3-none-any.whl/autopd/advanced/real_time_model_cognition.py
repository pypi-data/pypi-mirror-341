"""
Real-Time Model Cognition Visualization (MindScope) module for AutoPipelineDoctor.

This advanced module visualizes what the model "pays attention to" during training,
rendering attention heatmaps, neuron firing graphs, and distribution shifts in
activations per epoch.
"""

import os
import time
import logging
import threading
import queue
import json
import pickle
import datetime
import uuid
import traceback
from typing import Dict, List, Tuple, Optional, Union, Any, Set, Callable, Type
from dataclasses import dataclass, field
from collections import defaultdict, deque
from enum import Enum
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.colors import LinearSegmentedColormap
import seaborn as sns
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.hooks import RemovableHandle
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
from scipy.stats import entropy
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
import warnings

logger = logging.getLogger(__name__)


class VisualizationType(Enum):
    """Types of visualizations supported by MindScope."""
    ATTENTION_HEATMAP = "attention_heatmap"
    NEURON_FIRING = "neuron_firing"
    ACTIVATION_DISTRIBUTION = "activation_distribution"
    GRADIENT_FLOW = "gradient_flow"
    FEATURE_SPACE = "feature_space"
    LAYER_SIMILARITY = "layer_similarity"
    CUSTOM = "custom"


class ActivationAggregation(Enum):
    """Methods for aggregating activations across batches."""
    MEAN = "mean"
    MAX = "max"
    MIN = "min"
    STD = "std"
    ENTROPY = "entropy"
    L1_NORM = "l1_norm"
    L2_NORM = "l2_norm"
    CUSTOM = "custom"


class LayerType(Enum):
    """Types of layers for visualization."""
    ATTENTION = "attention"
    CONV = "conv"
    LINEAR = "linear"
    EMBEDDING = "embedding"
    NORMALIZATION = "normalization"
    POOLING = "pooling"
    ACTIVATION = "activation"
    RECURRENT = "recurrent"
    TRANSFORMER = "transformer"
    CUSTOM = "custom"


class OutputFormat(Enum):
    """Output formats for visualizations."""
    MATPLOTLIB = "matplotlib"
    PLOTLY = "plotly"
    HTML = "html"
    PNG = "png"
    JPEG = "jpeg"
    SVG = "svg"
    PDF = "pdf"
    GIF = "gif"
    MP4 = "mp4"
    CUSTOM = "custom"


@dataclass
class LayerInfo:
    """Information about a layer in the model."""
    name: str
    layer: nn.Module
    layer_type: LayerType
    parent_name: Optional[str] = None
    children: List[str] = field(default_factory=list)
    input_shape: Optional[Tuple[int, ...]] = None
    output_shape: Optional[Tuple[int, ...]] = None
    parameters_count: int = 0
    is_trainable: bool = True
    custom_metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ActivationRecord:
    """Record of activations for a layer."""
    layer_name: str
    step: int
    epoch: int
    batch_idx: int
    timestamp: float
    input_activation: Optional[torch.Tensor] = None
    output_activation: Optional[torch.Tensor] = None
    attention_weights: Optional[torch.Tensor] = None
    gradient: Optional[torch.Tensor] = None
    custom_data: Dict[str, Any] = field(default_factory=dict)


@dataclass
class VisualizationConfig:
    """Configuration for a visualization."""
    type: VisualizationType
    layers: List[str]
    aggregation: ActivationAggregation = ActivationAggregation.MEAN
    output_format: OutputFormat = OutputFormat.MATPLOTLIB
    update_interval: float = 1.0  # seconds
    max_history: int = 100
    colormap: str = "viridis"
    include_gradients: bool = False
    normalize: bool = True
    custom_params: Dict[str, Any] = field(default_factory=dict)


class ModelCognitionVisualizer:
    """
    Real-Time Model Cognition Visualization (MindScope).
    
    This module visualizes what the model "pays attention to" during training,
    rendering attention heatmaps, neuron firing graphs, and distribution shifts in
    activations per epoch.
    
    Attributes:
        model: PyTorch model
        config: Visualization configuration
        layer_info: Information about layers in the model
        activation_history: History of activations
        hooks: Registered hooks
        visualization_thread: Thread for visualization
        visualization_queue: Queue for visualization tasks
        running: Whether the visualizer is running
        output_dir: Directory for saving visualizations
    """
    
    def __init__(
        self,
        model: nn.Module,
        config: Optional[VisualizationConfig] = None,
        output_dir: str = "./mindscope_output",
    ):
        """
        Initialize the ModelCognitionVisualizer.
        
        Args:
            model: PyTorch model
            config: Visualization configuration
            output_dir: Directory for saving visualizations
        """
        self.model = model
        self.config = config or VisualizationConfig(
            type=VisualizationType.ATTENTION_HEATMAP,
            layers=[],
            aggregation=ActivationAggregation.MEAN,
            output_format=OutputFormat.MATPLOTLIB,
            update_interval=1.0,
            max_history=100,
            colormap="viridis",
            include_gradients=False,
            normalize=True,
        )
        
        self.layer_info: Dict[str, LayerInfo] = {}
        self.activation_history: Dict[str, List[ActivationRecord]] = defaultdict(list)
        self.hooks: Dict[str, RemovableHandle] = {}
        
        self.visualization_thread: Optional[threading.Thread] = None
        self.visualization_queue: queue.Queue = queue.Queue()
        self.running: bool = False
        
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
        # Initialize layer info
        self._initialize_layer_info()
        
        logger.info(f"Initialized ModelCognitionVisualizer with {len(self.layer_info)} layers")
    
    def _initialize_layer_info(self) -> None:
        """Initialize information about layers in the model."""
        # Clear existing info
        self.layer_info = {}
        
        # Register layers
        self._register_layers(self.model, "")
        
        # Update children information
        for name, info in self.layer_info.items():
            if info.parent_name:
                parent_info = self.layer_info.get(info.parent_name)
                if parent_info:
                    parent_info.children.append(name)
        
        # If no layers specified in config, use all layers
        if not self.config.layers:
            self.config.layers = list(self.layer_info.keys())
    
    def _register_layers(self, module: nn.Module, parent_name: str) -> None:
        """
        Recursively register layers in the model.
        
        Args:
            module: PyTorch module
            parent_name: Name of the parent module
        """
        for name, layer in module.named_children():
            # Create full name
            full_name = f"{parent_name}.{name}" if parent_name else name
            
            # Determine layer type
            layer_type = self._determine_layer_type(layer)
            
            # Count parameters
            parameters_count = sum(p.numel() for p in layer.parameters() if p.requires_grad)
            
            # Create layer info
            layer_info = LayerInfo(
                name=full_name,
                layer=layer,
                layer_type=layer_type,
                parent_name=parent_name,
                parameters_count=parameters_count,
                is_trainable=any(p.requires_grad for p in layer.parameters()),
            )
            
            # Add to layer info
            self.layer_info[full_name] = layer_info
            
            # Recursively register children
            self._register_layers(layer, full_name)
    
    def _determine_layer_type(self, layer: nn.Module) -> LayerType:
        """
        Determine the type of a layer.
        
        Args:
            layer: PyTorch layer
            
        Returns:
            Layer type
        """
        # Check for attention layers
        if any(attention_name in layer.__class__.__name__.lower() for attention_name in ["attention", "mha", "multihead"]):
            return LayerType.ATTENTION
        
        # Check for convolutional layers
        elif isinstance(layer, (nn.Conv1d, nn.Conv2d, nn.Conv3d, nn.ConvTranspose1d, nn.ConvTranspose2d, nn.ConvTranspose3d)):
            return LayerType.CONV
        
        # Check for linear layers
        elif isinstance(layer, nn.Linear):
            return LayerType.LINEAR
        
        # Check for embedding layers
        elif isinstance(layer, nn.Embedding):
            return LayerType.EMBEDDING
        
        # Check for normalization layers
        elif isinstance(layer, (nn.BatchNorm1d, nn.BatchNorm2d, nn.BatchNorm3d, nn.LayerNorm, nn.GroupNorm, nn.InstanceNorm1d, nn.InstanceNorm2d, nn.InstanceNorm3d)):
            return LayerType.NORMALIZATION
        
        # Check for pooling layers
        elif isinstance(layer, (nn.MaxPool1d, nn.MaxPool2d, nn.MaxPool3d, nn.AvgPool1d, nn.AvgPool2d, nn.AvgPool3d, nn.AdaptiveMaxPool1d, nn.AdaptiveMaxPool2d, nn.AdaptiveMaxPool3d, nn.AdaptiveAvgPool1d, nn.AdaptiveAvgPool2d, nn.AdaptiveAvgPool3d)):
            return LayerType.POOLING
        
        # Check for activation layers
        elif isinstance(layer, (nn.ReLU, nn.LeakyReLU, nn.PReLU, nn.ELU, nn.SELU, nn.GELU, nn.Sigmoid, nn.Tanh, nn.Softmax, nn.Softplus, nn.Softsign, nn.Hardtanh, nn.Hardshrink, nn.Hardsigmoid)):
            return LayerType.ACTIVATION
        
        # Check for recurrent layers
        elif isinstance(layer, (nn.RNN, nn.LSTM, nn.GRU)):
            return LayerType.RECURRENT
        
        # Check for transformer layers
        elif "transformer" in layer.__class__.__name__.lower():
            return LayerType.TRANSFORMER
        
        # Default to custom
        else:
            return LayerType.CUSTOM
    
    def register_hooks(self) -> None:
        """Register hooks for capturing activations."""
        # Clear existing hooks
        self.remove_hooks()
        
        # Register hooks for specified layers
        for layer_name in self.config.layers:
            if layer_name in self.layer_info:
                layer_info = self.layer_info[layer_name]
                
                # Register forward hook
                forward_hook = layer_info.layer.register_forward_hook(
                    lambda module, input, output, name=layer_name:
                    self._forward_hook(module, input, output, name)
                )
                
                self.hooks[f"{layer_name}_forward"] = forward_hook
                
                # Register backward hook if gradients are included
                if self.config.include_gradients:
                    if hasattr(layer_info.layer, "weight") and layer_info.layer.weight is not None:
                        backward_hook = layer_info.layer.weight.register_hook(
                            lambda grad, name=layer_name:
                            self._backward_hook(grad, name)
                        )
                        
                        self.hooks[f"{layer_name}_backward"] = backward_hook
        
        logger.info(f"Registered hooks for {len(self.config.layers)} layers")
    
    def remove_hooks(self) -> None:
        """Remove registered hooks."""
        for hook_name, hook in self.hooks.items():
            hook.remove()
        
        self.hooks = {}
        
        logger.info("Removed all hooks")
    
    def _forward_hook(
        self,
        module: nn.Module,
        input_tensor: Tuple[torch.Tensor, ...],
        output_tensor: torch.Tensor,
        layer_name: str,
    ) -> None:
        """
        Forward hook for capturing activations.
        
        Args:
            module: PyTorch module
            input_tensor: Input tensor
            output_tensor: Output tensor
            layer_name: Name of the layer
        """
        try:
            # Skip if not running
            if not self.running:
                return
            
            # Get current step information
            step = getattr(self, "current_step", 0)
            epoch = getattr(self, "current_epoch", 0)
            batch_idx = getattr(self, "current_batch_idx", 0)
            
            # Create activation record
            record = ActivationRecord(
                layer_name=layer_name,
                step=step,
                epoch=epoch,
                batch_idx=batch_idx,
                timestamp=time.time(),
                input_activation=input_tensor[0].detach().cpu() if isinstance(input_tensor, tuple) and len(input_tensor) > 0 else None,
                output_activation=output_tensor.detach().cpu() if isinstance(output_tensor, torch.Tensor) else None,
            )
            
            # Check for attention weights in transformer layers
            if self.layer_info[layer_name].layer_type == LayerType.ATTENTION or "attention" in layer_name.lower():
                # Try to extract attention weights
                if hasattr(module, "attention_weights") and module.attention_weights is not None:
                    record.attention_weights = module.attention_weights.detach().cpu()
                elif hasattr(module, "attn_weights") and module.attn_weights is not None:
                    record.attention_weights = module.attn_weights.detach().cpu()
                elif hasattr(module, "attn_output_weights") and module.attn_output_weights is not None:
                    record.attention_weights = module.attn_output_weights.detach().cpu()
            
            # Add to history
            self.activation_history[layer_name].append(record)
            
            # Limit history size
            if len(self.activation_history[layer_name]) > self.config.max_history:
                self.activation_history[layer_name] = self.activation_history[layer_name][-self.config.max_history:]
            
            # Update layer info with shapes
            layer_info = self.layer_info[layer_name]
            if isinstance(input_tensor, tuple) and len(input_tensor) > 0:
                layer_info.input_shape = tuple(input_tensor[0].shape)
            if isinstance(output_tensor, torch.Tensor):
                layer_info.output_shape = tuple(output_tensor.shape)
        
        except Exception as e:
            logger.error(f"Error in forward hook for layer {layer_name}: {e}")
            logger.error(traceback.format_exc())
    
    def _backward_hook(
        self,
        grad: torch.Tensor,
        layer_name: str,
    ) -> None:
        """
        Backward hook for capturing gradients.
        
        Args:
            grad: Gradient tensor
            layer_name: Name of the layer
        """
        try:
            # Skip if not running
            if not self.running:
                return
            
            # Find the latest activation record for this layer
            if layer_name in self.activation_history and self.activation_history[layer_name]:
                latest_record = self.activation_history[layer_name][-1]
                
                # Update with gradient
                latest_record.gradient = grad.detach().cpu()
        
        except Exception as e:
            logger.error(f"Error in backward hook for layer {layer_name}: {e}")
            logger.error(traceback.format_exc())
    
    def start(
        self,
        step: int = 0,
        epoch: int = 0,
        batch_idx: int = 0,
    ) -> None:
        """
        Start the visualizer.
        
        Args:
            step: Current step
            epoch: Current epoch
            batch_idx: Current batch index
        """
        if self.running:
            logger.warning("Visualizer is already running")
            return
        
        # Set current step information
        self.current_step = step
        self.current_epoch = epoch
        self.current_batch_idx = batch_idx
        
        # Register hooks
        self.register_hooks()
        
        # Start visualization thread
        self.running = True
        self.visualization_thread = threading.Thread(target=self._visualization_loop)
        self.visualization_thread.daemon = True
        self.visualization_thread.start()
        
        logger.info("Started ModelCognitionVisualizer")
    
    def stop(self) -> None:
        """Stop the visualizer."""
        if not self.running:
            logger.warning("Visualizer is not running")
            return
        
        # Stop visualization thread
        self.running = False
        if self.visualization_thread:
            self.visualization_thread.join(timeout=5.0)
            self.visualization_thread = None
        
        # Remove hooks
        self.remove_hooks()
        
        logger.info("Stopped ModelCognitionVisualizer")
    
    def update_step(
        self,
        step: int,
        epoch: Optional[int] = None,
        batch_idx: Optional[int] = None,
    ) -> None:
        """
        Update the current step.
        
        Args:
            step: Current step
            epoch: Current epoch
            batch_idx: Current batch index
        """
        self.current_step = step
        
        if epoch is not None:
            self.current_epoch = epoch
        
        if batch_idx is not None:
            self.current_batch_idx = batch_idx
    
    def _visualization_loop(self) -> None:
        """Visualization loop."""
        last_update_time = 0.0
        
        while self.running:
            try:
                # Check if it's time to update
                current_time = time.time()
                if current_time - last_update_time >= self.config.update_interval:
                    # Generate visualization
                    self._generate_visualization()
                    
                    # Update last update time
                    last_update_time = current_time
                
                # Process visualization queue
                try:
                    # Get task with timeout
                    task = self.visualization_queue.get(timeout=0.1)
                    
                    # Process task
                    task()
                    
                    # Mark task as done
                    self.visualization_queue.task_done()
                
                except queue.Empty:
                    # No tasks in queue
                    pass
                
                # Sleep to avoid high CPU usage
                time.sleep(0.01)
            
            except Exception as e:
                logger.error(f"Error in visualization loop: {e}")
                logger.error(traceback.format_exc())
                time.sleep(1.0)  # Sleep longer on error
    
    def _generate_visualization(self) -> None:
        """Generate visualization based on configuration."""
        try:
            # Skip if no activation history
            if not any(self.activation_history.values()):
                return
            
            # Generate visualization based on type
            if self.config.type == VisualizationType.ATTENTION_HEATMAP:
                self._visualize_attention_heatmaps()
            
            elif self.config.type == VisualizationType.NEURON_FIRING:
                self._visualize_neuron_firing()
            
            elif self.config.type == VisualizationType.ACTIVATION_DISTRIBUTION:
                self._visualize_activation_distributions()
            
            elif self.config.type == VisualizationType.GRADIENT_FLOW:
                self._visualize_gradient_flow()
            
            elif self.config.type == VisualizationType.FEATURE_SPACE:
                self._visualize_feature_space()
            
            elif self.config.type == VisualizationType.LAYER_SIMILARITY:
                self._visualize_layer_similarity()
            
            elif self.config.type == VisualizationType.CUSTOM:
                self._visualize_custom()
        
        except Exception as e:
            logger.error(f"Error generating visualization: {e}")
            logger.error(traceback.format_exc())
    
    def _visualize_attention_heatmaps(self) -> None:
        """Visualize attention heatmaps."""
        # Find layers with attention weights
        attention_layers = []
        
        for layer_name in self.config.layers:
            if layer_name in self.activation_history and self.activation_history[layer_name]:
                latest_record = self.activation_history[layer_name][-1]
                
                if latest_record.attention_weights is not None:
                    attention_layers.append(layer_name)
        
        if not attention_layers:
            logger.warning("No attention weights found in specified layers")
            return
        
        # Create figure
        n_layers = len(attention_layers)
        fig_width = min(15, 5 * n_layers)
        fig_height = min(10, 3 * n_layers)
        
        if self.config.output_format == OutputFormat.MATPLOTLIB:
            fig, axes = plt.subplots(1, n_layers, figsize=(fig_width, fig_height))
            
            # Handle single layer case
            if n_layers == 1:
                axes = [axes]
            
            for i, layer_name in enumerate(attention_layers):
                latest_record = self.activation_history[layer_name][-1]
                attention_weights = latest_record.attention_weights
                
                # Reshape if needed
                if len(attention_weights.shape) > 2:
                    # For multi-head attention, average across heads
                    if len(attention_weights.shape) == 3:
                        attention_weights = attention_weights.mean(dim=0)
                    # For batched multi-head attention, average across batch and heads
                    elif len(attention_weights.shape) == 4:
                        attention_weights = attention_weights.mean(dim=(0, 1))
                
                # Plot heatmap
                im = axes[i].imshow(
                    attention_weights.numpy(),
                    cmap=self.config.colormap,
                    aspect='auto',
                )
                
                axes[i].set_title(f"{layer_name}\nEpoch {latest_record.epoch}, Batch {latest_record.batch_idx}")
                
                # Add colorbar
                plt.colorbar(im, ax=axes[i])
            
            plt.tight_layout()
            
            # Save figure
            output_path = os.path.join(
                self.output_dir,
                f"attention_heatmap_step_{self.current_step}.png"
            )
            plt.savefig(output_path, dpi=300, bbox_inches="tight")
            plt.close(fig)
            
            logger.info(f"Saved attention heatmap to {output_path}")
        
        elif self.config.output_format == OutputFormat.PLOTLY:
            # Create subplots
            fig = make_subplots(rows=1, cols=n_layers, subplot_titles=[
                f"{layer_name}\nEpoch {self.activation_history[layer_name][-1].epoch}, Batch {self.activation_history[layer_name][-1].batch_idx}"
                for layer_name in attention_layers
            ])
            
            for i, layer_name in enumerate(attention_layers):
                latest_record = self.activation_history[layer_name][-1]
                attention_weights = latest_record.attention_weights
                
                # Reshape if needed
                if len(attention_weights.shape) > 2:
                    # For multi-head attention, average across heads
                    if len(attention_weights.shape) == 3:
                        attention_weights = attention_weights.mean(dim=0)
                    # For batched multi-head attention, average across batch and heads
                    elif len(attention_weights.shape) == 4:
                        attention_weights = attention_weights.mean(dim=(0, 1))
                
                # Add heatmap
                fig.add_trace(
                    go.Heatmap(
                        z=attention_weights.numpy(),
                        colorscale=self.config.colormap,
                    ),
                    row=1, col=i+1,
                )
            
            fig.update_layout(
                title_text=f"Attention Heatmaps (Step {self.current_step})",
                height=600,
                width=300 * n_layers,
            )
            
            # Save figure
            output_path = os.path.join(
                self.output_dir,
                f"attention_heatmap_step_{self.current_step}.html"
            )
            fig.write_html(output_path)
            
            logger.info(f"Saved attention heatmap to {output_path}")
    
    def _visualize_neuron_firing(self) -> None:
        """Visualize neuron firing patterns."""
        # Find layers with output activations
        activation_layers = []
        
        for layer_name in self.config.layers:
            if layer_name in self.activation_history and self.activation_history[layer_name]:
                latest_record = self.activation_history[layer_name][-1]
                
                if latest_record.output_activation is not None:
                    activation_layers.append(layer_name)
        
        if not activation_layers:
            logger.warning("No output activations found in specified layers")
            return
        
        # Create figure
        n_layers = len(activation_layers)
        fig_width = min(15, 5 * n_layers)
        fig_height = min(10, 3 * n_layers)
        
        if self.config.output_format == OutputFormat.MATPLOTLIB:
            fig, axes = plt.subplots(1, n_layers, figsize=(fig_width, fig_height))
            
            # Handle single layer case
            if n_layers == 1:
                axes = [axes]
            
            for i, layer_name in enumerate(activation_layers):
                # Get activation history for this layer
                layer_history = self.activation_history[layer_name]
                
                # Get the last few records
                history_length = min(len(layer_history), 10)
                recent_history = layer_history[-history_length:]
                
                # Extract activations and aggregate
                activations = []
                
                for record in recent_history:
                    output_activation = record.output_activation
                    
                    # Reshape to 2D (neurons x batch*spatial)
                    if len(output_activation.shape) > 2:
                        # For convolutional layers, reshape to (channels, batch*height*width)
                        output_activation = output_activation.reshape(output_activation.shape[0], -1)
                    
                    # Aggregate across batch/spatial dimensions
                    if self.config.aggregation == ActivationAggregation.MEAN:
                        aggregated = output_activation.mean(dim=1)
                    elif self.config.aggregation == ActivationAggregation.MAX:
                        aggregated = output_activation.max(dim=1)[0]
                    elif self.config.aggregation == ActivationAggregation.MIN:
                        aggregated = output_activation.min(dim=1)[0]
                    elif self.config.aggregation == ActivationAggregation.STD:
                        aggregated = output_activation.std(dim=1)
                    elif self.config.aggregation == ActivationAggregation.ENTROPY:
                        # Normalize to probabilities
                        probs = F.softmax(output_activation, dim=1)
                        aggregated = torch.tensor([entropy(p.numpy()) for p in probs])
                    elif self.config.aggregation == ActivationAggregation.L1_NORM:
                        aggregated = torch.norm(output_activation, p=1, dim=1)
                    elif self.config.aggregation == ActivationAggregation.L2_NORM:
                        aggregated = torch.norm(output_activation, p=2, dim=1)
                    else:
                        aggregated = output_activation.mean(dim=1)
                    
                    activations.append(aggregated.numpy())
                
                # Convert to numpy array
                activations = np.array(activations)
                
                # Limit to top neurons for visualization
                max_neurons = 100
                if activations.shape[1] > max_neurons:
                    # Get top neurons by activation variance
                    neuron_variance = np.var(activations, axis=0)
                    top_indices = np.argsort(neuron_variance)[-max_neurons:]
                    activations = activations[:, top_indices]
                
                # Plot heatmap
                im = axes[i].imshow(
                    activations.T,
                    cmap=self.config.colormap,
                    aspect='auto',
                )
                
                axes[i].set_title(f"{layer_name}\nNeuron Firing Patterns")
                axes[i].set_xlabel("Time Step")
                axes[i].set_ylabel("Neuron Index")
                
                # Add colorbar
                plt.colorbar(im, ax=axes[i])
            
            plt.tight_layout()
            
            # Save figure
            output_path = os.path.join(
                self.output_dir,
                f"neuron_firing_step_{self.current_step}.png"
            )
            plt.savefig(output_path, dpi=300, bbox_inches="tight")
            plt.close(fig)
            
            logger.info(f"Saved neuron firing visualization to {output_path}")
        
        elif self.config.output_format == OutputFormat.PLOTLY:
            # Create subplots
            fig = make_subplots(rows=1, cols=n_layers, subplot_titles=[
                f"{layer_name}\nNeuron Firing Patterns"
                for layer_name in activation_layers
            ])
            
            for i, layer_name in enumerate(activation_layers):
                # Get activation history for this layer
                layer_history = self.activation_history[layer_name]
                
                # Get the last few records
                history_length = min(len(layer_history), 10)
                recent_history = layer_history[-history_length:]
                
                # Extract activations and aggregate
                activations = []
                
                for record in recent_history:
                    output_activation = record.output_activation
                    
                    # Reshape to 2D (neurons x batch*spatial)
                    if len(output_activation.shape) > 2:
                        # For convolutional layers, reshape to (channels, batch*height*width)
                        output_activation = output_activation.reshape(output_activation.shape[0], -1)
                    
                    # Aggregate across batch/spatial dimensions
                    if self.config.aggregation == ActivationAggregation.MEAN:
                        aggregated = output_activation.mean(dim=1)
                    elif self.config.aggregation == ActivationAggregation.MAX:
                        aggregated = output_activation.max(dim=1)[0]
                    elif self.config.aggregation == ActivationAggregation.MIN:
                        aggregated = output_activation.min(dim=1)[0]
                    elif self.config.aggregation == ActivationAggregation.STD:
                        aggregated = output_activation.std(dim=1)
                    elif self.config.aggregation == ActivationAggregation.ENTROPY:
                        # Normalize to probabilities
                        probs = F.softmax(output_activation, dim=1)
                        aggregated = torch.tensor([entropy(p.numpy()) for p in probs])
                    elif self.config.aggregation == ActivationAggregation.L1_NORM:
                        aggregated = torch.norm(output_activation, p=1, dim=1)
                    elif self.config.aggregation == ActivationAggregation.L2_NORM:
                        aggregated = torch.norm(output_activation, p=2, dim=1)
                    else:
                        aggregated = output_activation.mean(dim=1)
                    
                    activations.append(aggregated.numpy())
                
                # Convert to numpy array
                activations = np.array(activations)
                
                # Limit to top neurons for visualization
                max_neurons = 100
                if activations.shape[1] > max_neurons:
                    # Get top neurons by activation variance
                    neuron_variance = np.var(activations, axis=0)
                    top_indices = np.argsort(neuron_variance)[-max_neurons:]
                    activations = activations[:, top_indices]
                
                # Add heatmap
                fig.add_trace(
                    go.Heatmap(
                        z=activations.T,
                        colorscale=self.config.colormap,
                    ),
                    row=1, col=i+1,
                )
                
                # Update axes
                fig.update_xaxes(title_text="Time Step", row=1, col=i+1)
                fig.update_yaxes(title_text="Neuron Index", row=1, col=i+1)
            
            fig.update_layout(
                title_text=f"Neuron Firing Patterns (Step {self.current_step})",
                height=600,
                width=300 * n_layers,
            )
            
            # Save figure
            output_path = os.path.join(
                self.output_dir,
                f"neuron_firing_step_{self.current_step}.html"
            )
            fig.write_html(output_path)
            
            logger.info(f"Saved neuron firing visualization to {output_path}")
    
    def _visualize_activation_distributions(self) -> None:
        """Visualize activation distributions."""
        # Find layers with output activations
        activation_layers = []
        
        for layer_name in self.config.layers:
            if layer_name in self.activation_history and len(self.activation_history[layer_name]) >= 2:
                # Need at least 2 records to compare distributions
                records = self.activation_history[layer_name]
                
                if all(record.output_activation is not None for record in records[-2:]):
                    activation_layers.append(layer_name)
        
        if not activation_layers:
            logger.warning("No output activations found in specified layers or not enough history")
            return
        
        # Create figure
        n_layers = len(activation_layers)
        fig_width = min(15, 5 * n_layers)
        fig_height = min(10, 3 * n_layers)
        
        if self.config.output_format == OutputFormat.MATPLOTLIB:
            fig, axes = plt.subplots(1, n_layers, figsize=(fig_width, fig_height))
            
            # Handle single layer case
            if n_layers == 1:
                axes = [axes]
            
            for i, layer_name in enumerate(activation_layers):
                # Get activation history for this layer
                layer_history = self.activation_history[layer_name]
                
                # Get the last two records
                current_record = layer_history[-1]
                previous_record = layer_history[-2]
                
                # Extract activations
                current_activation = current_record.output_activation
                previous_activation = previous_record.output_activation
                
                # Flatten activations
                current_flat = current_activation.flatten().numpy()
                previous_flat = previous_activation.flatten().numpy()
                
                # Plot distributions
                axes[i].hist(previous_flat, bins=50, alpha=0.5, label=f"Epoch {previous_record.epoch}, Batch {previous_record.batch_idx}")
                axes[i].hist(current_flat, bins=50, alpha=0.5, label=f"Epoch {current_record.epoch}, Batch {current_record.batch_idx}")
                
                axes[i].set_title(f"{layer_name}\nActivation Distribution")
                axes[i].set_xlabel("Activation Value")
                axes[i].set_ylabel("Frequency")
                axes[i].legend()
                
                # Add distribution statistics
                current_mean = np.mean(current_flat)
                current_std = np.std(current_flat)
                previous_mean = np.mean(previous_flat)
                previous_std = np.std(previous_flat)
                
                stats_text = f"Current: μ={current_mean:.4f}, σ={current_std:.4f}\n"
                stats_text += f"Previous: μ={previous_mean:.4f}, σ={previous_std:.4f}"
                
                axes[i].text(
                    0.05, 0.95, stats_text,
                    transform=axes[i].transAxes,
                    verticalalignment='top',
                    bbox=dict(boxstyle='round', facecolor='white', alpha=0.8)
                )
            
            plt.tight_layout()
            
            # Save figure
            output_path = os.path.join(
                self.output_dir,
                f"activation_distribution_step_{self.current_step}.png"
            )
            plt.savefig(output_path, dpi=300, bbox_inches="tight")
            plt.close(fig)
            
            logger.info(f"Saved activation distribution visualization to {output_path}")
        
        elif self.config.output_format == OutputFormat.PLOTLY:
            # Create subplots
            fig = make_subplots(rows=1, cols=n_layers, subplot_titles=[
                f"{layer_name}\nActivation Distribution"
                for layer_name in activation_layers
            ])
            
            for i, layer_name in enumerate(activation_layers):
                # Get activation history for this layer
                layer_history = self.activation_history[layer_name]
                
                # Get the last two records
                current_record = layer_history[-1]
                previous_record = layer_history[-2]
                
                # Extract activations
                current_activation = current_record.output_activation
                previous_activation = previous_record.output_activation
                
                # Flatten activations
                current_flat = current_activation.flatten().numpy()
                previous_flat = previous_activation.flatten().numpy()
                
                # Add histograms
                fig.add_trace(
                    go.Histogram(
                        x=previous_flat,
                        opacity=0.5,
                        name=f"Epoch {previous_record.epoch}, Batch {previous_record.batch_idx}",
                        nbinsx=50,
                    ),
                    row=1, col=i+1,
                )
                
                fig.add_trace(
                    go.Histogram(
                        x=current_flat,
                        opacity=0.5,
                        name=f"Epoch {current_record.epoch}, Batch {current_record.batch_idx}",
                        nbinsx=50,
                    ),
                    row=1, col=i+1,
                )
                
                # Calculate statistics
                current_mean = np.mean(current_flat)
                current_std = np.std(current_flat)
                previous_mean = np.mean(previous_flat)
                previous_std = np.std(previous_flat)
                
                # Add statistics as annotations
                fig.add_annotation(
                    text=f"Current: μ={current_mean:.4f}, σ={current_std:.4f}<br>Previous: μ={previous_mean:.4f}, σ={previous_std:.4f}",
                    xref=f"x{i+1}",
                    yref=f"y{i+1}",
                    x=0.05,
                    y=0.95,
                    showarrow=False,
                    bgcolor="white",
                    opacity=0.8,
                )
                
                # Update axes
                fig.update_xaxes(title_text="Activation Value", row=1, col=i+1)
                fig.update_yaxes(title_text="Frequency", row=1, col=i+1)
            
            fig.update_layout(
                title_text=f"Activation Distributions (Step {self.current_step})",
                height=600,
                width=300 * n_layers,
                barmode='overlay',
            )
            
            # Save figure
            output_path = os.path.join(
                self.output_dir,
                f"activation_distribution_step_{self.current_step}.html"
            )
            fig.write_html(output_path)
            
            logger.info(f"Saved activation distribution visualization to {output_path}")
    
    def _visualize_gradient_flow(self) -> None:
        """Visualize gradient flow through the model."""
        # Check if gradients are included
        if not self.config.include_gradients:
            logger.warning("Gradient visualization requires include_gradients=True")
            return
        
        # Find layers with gradients
        gradient_layers = []
        
        for layer_name in self.config.layers:
            if layer_name in self.activation_history and self.activation_history[layer_name]:
                latest_record = self.activation_history[layer_name][-1]
                
                if latest_record.gradient is not None:
                    gradient_layers.append(layer_name)
        
        if not gradient_layers:
            logger.warning("No gradients found in specified layers")
            return
        
        # Create figure
        if self.config.output_format == OutputFormat.MATPLOTLIB:
            plt.figure(figsize=(10, 6))
            
            # Extract gradient norms
            layer_names = []
            gradient_norms = []
            
            for layer_name in gradient_layers:
                latest_record = self.activation_history[layer_name][-1]
                gradient = latest_record.gradient
                
                # Calculate norm
                norm = torch.norm(gradient).item()
                
                layer_names.append(layer_name.split('.')[-1])  # Use last part of name for clarity
                gradient_norms.append(norm)
            
            # Plot gradient norms
            plt.barh(range(len(layer_names)), gradient_norms, align='center')
            plt.yticks(range(len(layer_names)), layer_names)
            plt.xlabel('Gradient Norm')
            plt.title(f'Gradient Flow (Step {self.current_step})')
            plt.grid(axis='x')
            
            # Add colormap
            sm = plt.cm.ScalarMappable(cmap=self.config.colormap)
            sm.set_array(gradient_norms)
            plt.colorbar(sm)
            
            plt.tight_layout()
            
            # Save figure
            output_path = os.path.join(
                self.output_dir,
                f"gradient_flow_step_{self.current_step}.png"
            )
            plt.savefig(output_path, dpi=300, bbox_inches="tight")
            plt.close()
            
            logger.info(f"Saved gradient flow visualization to {output_path}")
        
        elif self.config.output_format == OutputFormat.PLOTLY:
            # Extract gradient norms
            layer_names = []
            gradient_norms = []
            
            for layer_name in gradient_layers:
                latest_record = self.activation_history[layer_name][-1]
                gradient = latest_record.gradient
                
                # Calculate norm
                norm = torch.norm(gradient).item()
                
                layer_names.append(layer_name.split('.')[-1])  # Use last part of name for clarity
                gradient_norms.append(norm)
            
            # Create figure
            fig = go.Figure()
            
            # Add bar chart
            fig.add_trace(
                go.Bar(
                    y=layer_names,
                    x=gradient_norms,
                    orientation='h',
                    marker=dict(
                        color=gradient_norms,
                        colorscale=self.config.colormap,
                        colorbar=dict(title='Gradient Norm'),
                    ),
                )
            )
            
            fig.update_layout(
                title=f'Gradient Flow (Step {self.current_step})',
                xaxis_title='Gradient Norm',
                height=600,
                width=800,
            )
            
            # Save figure
            output_path = os.path.join(
                self.output_dir,
                f"gradient_flow_step_{self.current_step}.html"
            )
            fig.write_html(output_path)
            
            logger.info(f"Saved gradient flow visualization to {output_path}")
    
    def _visualize_feature_space(self) -> None:
        """Visualize feature space using dimensionality reduction."""
        # Find layers with output activations
        activation_layers = []
        
        for layer_name in self.config.layers:
            if layer_name in self.activation_history and self.activation_history[layer_name]:
                latest_record = self.activation_history[layer_name][-1]
                
                if latest_record.output_activation is not None:
                    activation_layers.append(layer_name)
        
        if not activation_layers:
            logger.warning("No output activations found in specified layers")
            return
        
        # Create figure
        n_layers = min(len(activation_layers), 3)  # Limit to 3 layers for visualization
        fig_width = min(15, 5 * n_layers)
        fig_height = min(10, 5 * n_layers)
        
        if self.config.output_format == OutputFormat.MATPLOTLIB:
            fig, axes = plt.subplots(1, n_layers, figsize=(fig_width, fig_height))
            
            # Handle single layer case
            if n_layers == 1:
                axes = [axes]
            
            for i, layer_name in enumerate(activation_layers[:n_layers]):
                latest_record = self.activation_history[layer_name][-1]
                activation = latest_record.output_activation
                
                # Reshape activation for PCA
                if len(activation.shape) > 2:
                    # For convolutional layers, reshape to (batch*height*width, channels)
                    activation = activation.permute(0, 2, 3, 1).reshape(-1, activation.shape[1])
                
                # Limit to 1000 samples for efficiency
                if activation.shape[0] > 1000:
                    indices = torch.randperm(activation.shape[0])[:1000]
                    activation = activation[indices]
                
                # Apply PCA
                pca = PCA(n_components=2)
                
                try:
                    activation_pca = pca.fit_transform(activation.numpy())
                    
                    # Plot PCA
                    scatter = axes[i].scatter(
                        activation_pca[:, 0],
                        activation_pca[:, 1],
                        c=np.linalg.norm(activation.numpy(), axis=1),
                        cmap=self.config.colormap,
                        alpha=0.7,
                    )
                    
                    axes[i].set_title(f"{layer_name}\nFeature Space (PCA)")
                    axes[i].set_xlabel(f"PC1 ({pca.explained_variance_ratio_[0]:.2%})")
                    axes[i].set_ylabel(f"PC2 ({pca.explained_variance_ratio_[1]:.2%})")
                    
                    # Add colorbar
                    plt.colorbar(scatter, ax=axes[i], label="Activation Norm")
                
                except Exception as e:
                    logger.error(f"Error applying PCA to layer {layer_name}: {e}")
                    axes[i].text(0.5, 0.5, f"PCA Error: {str(e)}", ha='center', va='center')
                    axes[i].set_title(f"{layer_name}\nFeature Space (Error)")
            
            plt.tight_layout()
            
            # Save figure
            output_path = os.path.join(
                self.output_dir,
                f"feature_space_step_{self.current_step}.png"
            )
            plt.savefig(output_path, dpi=300, bbox_inches="tight")
            plt.close(fig)
            
            logger.info(f"Saved feature space visualization to {output_path}")
        
        elif self.config.output_format == OutputFormat.PLOTLY:
            # Create subplots
            fig = make_subplots(rows=1, cols=n_layers, subplot_titles=[
                f"{layer_name}\nFeature Space (PCA)"
                for layer_name in activation_layers[:n_layers]
            ])
            
            for i, layer_name in enumerate(activation_layers[:n_layers]):
                latest_record = self.activation_history[layer_name][-1]
                activation = latest_record.output_activation
                
                # Reshape activation for PCA
                if len(activation.shape) > 2:
                    # For convolutional layers, reshape to (batch*height*width, channels)
                    activation = activation.permute(0, 2, 3, 1).reshape(-1, activation.shape[1])
                
                # Limit to 1000 samples for efficiency
                if activation.shape[0] > 1000:
                    indices = torch.randperm(activation.shape[0])[:1000]
                    activation = activation[indices]
                
                # Apply PCA
                pca = PCA(n_components=2)
                
                try:
                    activation_pca = pca.fit_transform(activation.numpy())
                    activation_norms = np.linalg.norm(activation.numpy(), axis=1)
                    
                    # Add scatter plot
                    fig.add_trace(
                        go.Scatter(
                            x=activation_pca[:, 0],
                            y=activation_pca[:, 1],
                            mode='markers',
                            marker=dict(
                                color=activation_norms,
                                colorscale=self.config.colormap,
                                colorbar=dict(title='Activation Norm'),
                                opacity=0.7,
                            ),
                            showlegend=False,
                        ),
                        row=1, col=i+1,
                    )
                    
                    # Update axes
                    fig.update_xaxes(
                        title_text=f"PC1 ({pca.explained_variance_ratio_[0]:.2%})",
                        row=1, col=i+1,
                    )
                    fig.update_yaxes(
                        title_text=f"PC2 ({pca.explained_variance_ratio_[1]:.2%})",
                        row=1, col=i+1,
                    )
                
                except Exception as e:
                    logger.error(f"Error applying PCA to layer {layer_name}: {e}")
                    
                    # Add error text
                    fig.add_annotation(
                        text=f"PCA Error: {str(e)}",
                        xref=f"x{i+1}",
                        yref=f"y{i+1}",
                        x=0.5,
                        y=0.5,
                        showarrow=False,
                    )
            
            fig.update_layout(
                title_text=f"Feature Space Visualization (Step {self.current_step})",
                height=600,
                width=300 * n_layers,
            )
            
            # Save figure
            output_path = os.path.join(
                self.output_dir,
                f"feature_space_step_{self.current_step}.html"
            )
            fig.write_html(output_path)
            
            logger.info(f"Saved feature space visualization to {output_path}")
    
    def _visualize_layer_similarity(self) -> None:
        """Visualize similarity between layer activations."""
        # Find layers with output activations
        activation_layers = []
        
        for layer_name in self.config.layers:
            if layer_name in self.activation_history and self.activation_history[layer_name]:
                latest_record = self.activation_history[layer_name][-1]
                
                if latest_record.output_activation is not None:
                    activation_layers.append(layer_name)
        
        if len(activation_layers) < 2:
            logger.warning("Need at least 2 layers with activations for similarity visualization")
            return
        
        # Extract activation statistics
        layer_stats = {}
        
        for layer_name in activation_layers:
            latest_record = self.activation_history[layer_name][-1]
            activation = latest_record.output_activation
            
            # Flatten activation
            if len(activation.shape) > 2:
                activation = activation.reshape(activation.shape[0], -1)
            
            # Calculate statistics
            mean = activation.mean(dim=0).numpy()
            std = activation.std(dim=0).numpy()
            
            layer_stats[layer_name] = {
                "mean": mean,
                "std": std,
                "shape": activation.shape,
            }
        
        # Calculate similarity matrix
        n_layers = len(activation_layers)
        similarity_matrix = np.zeros((n_layers, n_layers))
        
        for i, layer1 in enumerate(activation_layers):
            for j, layer2 in enumerate(activation_layers):
                # Skip same layer
                if i == j:
                    similarity_matrix[i, j] = 1.0
                    continue
                
                # Get statistics
                mean1 = layer_stats[layer1]["mean"]
                mean2 = layer_stats[layer2]["mean"]
                
                # Resize if needed
                if len(mean1) != len(mean2):
                    # Resize to smaller dimension
                    min_dim = min(len(mean1), len(mean2))
                    mean1 = mean1[:min_dim] if len(mean1) > min_dim else np.pad(mean1, (0, min_dim - len(mean1)))
                    mean2 = mean2[:min_dim] if len(mean2) > min_dim else np.pad(mean2, (0, min_dim - len(mean2)))
                
                # Calculate correlation
                try:
                    correlation = np.corrcoef(mean1, mean2)[0, 1]
                    
                    # Handle NaN
                    if np.isnan(correlation):
                        correlation = 0.0
                    
                    similarity_matrix[i, j] = correlation
                
                except Exception as e:
                    logger.error(f"Error calculating correlation between {layer1} and {layer2}: {e}")
                    similarity_matrix[i, j] = 0.0
        
        # Create figure
        if self.config.output_format == OutputFormat.MATPLOTLIB:
            plt.figure(figsize=(10, 8))
            
            # Plot similarity matrix
            im = plt.imshow(similarity_matrix, cmap=self.config.colormap, vmin=-1, vmax=1)
            
            # Add labels
            plt.xticks(range(n_layers), [layer.split('.')[-1] for layer in activation_layers], rotation=45, ha='right')
            plt.yticks(range(n_layers), [layer.split('.')[-1] for layer in activation_layers])
            
            plt.title(f"Layer Activation Similarity (Step {self.current_step})")
            
            # Add colorbar
            plt.colorbar(im, label="Correlation")
            
            plt.tight_layout()
            
            # Save figure
            output_path = os.path.join(
                self.output_dir,
                f"layer_similarity_step_{self.current_step}.png"
            )
            plt.savefig(output_path, dpi=300, bbox_inches="tight")
            plt.close()
            
            logger.info(f"Saved layer similarity visualization to {output_path}")
        
        elif self.config.output_format == OutputFormat.PLOTLY:
            # Create figure
            fig = go.Figure()
            
            # Add heatmap
            fig.add_trace(
                go.Heatmap(
                    z=similarity_matrix,
                    x=[layer.split('.')[-1] for layer in activation_layers],
                    y=[layer.split('.')[-1] for layer in activation_layers],
                    colorscale=self.config.colormap,
                    zmin=-1,
                    zmax=1,
                    colorbar=dict(title='Correlation'),
                )
            )
            
            fig.update_layout(
                title=f"Layer Activation Similarity (Step {self.current_step})",
                height=800,
                width=800,
            )
            
            # Save figure
            output_path = os.path.join(
                self.output_dir,
                f"layer_similarity_step_{self.current_step}.html"
            )
            fig.write_html(output_path)
            
            logger.info(f"Saved layer similarity visualization to {output_path}")
    
    def _visualize_custom(self) -> None:
        """Visualize custom data."""
        # Check if custom visualization function is provided
        custom_visualize_func = self.config.custom_params.get("visualize_func")
        
        if not custom_visualize_func or not callable(custom_visualize_func):
            logger.warning("Custom visualization requires a visualize_func in custom_params")
            return
        
        try:
            # Call custom visualization function
            output_path = os.path.join(
                self.output_dir,
                f"custom_visualization_step_{self.current_step}.png"
            )
            
            custom_visualize_func(
                self.activation_history,
                self.layer_info,
                self.current_step,
                self.current_epoch,
                self.current_batch_idx,
                output_path,
            )
            
            logger.info(f"Saved custom visualization to {output_path}")
        
        except Exception as e:
            logger.error(f"Error in custom visualization: {e}")
            logger.error(traceback.format_exc())
    
    def create_animation(
        self,
        visualization_type: VisualizationType,
        layer_name: str,
        output_path: Optional[str] = None,
        fps: int = 5,
        max_frames: int = 50,
    ) -> Optional[str]:
        """
        Create an animation of visualizations over time.
        
        Args:
            visualization_type: Type of visualization
            layer_name: Name of the layer
            output_path: Path to save the animation
            fps: Frames per second
            max_frames: Maximum number of frames
            
        Returns:
            Path to the saved animation or None
        """
        # Check if layer exists
        if layer_name not in self.layer_info:
            logger.warning(f"Layer {layer_name} not found")
            return None
        
        # Check if layer has activation history
        if layer_name not in self.activation_history or not self.activation_history[layer_name]:
            logger.warning(f"No activation history for layer {layer_name}")
            return None
        
        # Get activation history
        history = self.activation_history[layer_name]
        
        # Limit to max_frames
        if len(history) > max_frames:
            # Use evenly spaced frames
            indices = np.linspace(0, len(history) - 1, max_frames, dtype=int)
            history = [history[i] for i in indices]
        
        # Create output path if not provided
        if output_path is None:
            output_path = os.path.join(
                self.output_dir,
                f"{visualization_type.value}_{layer_name.replace('.', '_')}_animation.gif"
            )
        
        try:
            # Create animation based on visualization type
            if visualization_type == VisualizationType.ATTENTION_HEATMAP:
                self._create_attention_heatmap_animation(history, output_path, fps)
            
            elif visualization_type == VisualizationType.NEURON_FIRING:
                self._create_neuron_firing_animation(history, output_path, fps)
            
            elif visualization_type == VisualizationType.ACTIVATION_DISTRIBUTION:
                self._create_activation_distribution_animation(history, output_path, fps)
            
            else:
                logger.warning(f"Animation not supported for visualization type {visualization_type.value}")
                return None
            
            logger.info(f"Saved animation to {output_path}")
            return output_path
        
        except Exception as e:
            logger.error(f"Error creating animation: {e}")
            logger.error(traceback.format_exc())
            return None
    
    def _create_attention_heatmap_animation(
        self,
        history: List[ActivationRecord],
        output_path: str,
        fps: int,
    ) -> None:
        """
        Create an animation of attention heatmaps.
        
        Args:
            history: Activation history
            output_path: Path to save the animation
            fps: Frames per second
        """
        # Check if history has attention weights
        if not all(record.attention_weights is not None for record in history):
            logger.warning("Not all records have attention weights")
            return
        
        # Create figure
        fig, ax = plt.subplots(figsize=(8, 6))
        
        # Initialize heatmap
        first_record = history[0]
        attention_weights = first_record.attention_weights
        
        # Reshape if needed
        if len(attention_weights.shape) > 2:
            # For multi-head attention, average across heads
            if len(attention_weights.shape) == 3:
                attention_weights = attention_weights.mean(dim=0)
            # For batched multi-head attention, average across batch and heads
            elif len(attention_weights.shape) == 4:
                attention_weights = attention_weights.mean(dim=(0, 1))
        
        im = ax.imshow(
            attention_weights.numpy(),
            cmap=self.config.colormap,
            aspect='auto',
            animated=True,
        )
        
        title = ax.set_title(f"Epoch {first_record.epoch}, Batch {first_record.batch_idx}")
        
        # Add colorbar
        plt.colorbar(im, ax=ax)
        
        # Animation update function
        def update(frame):
            record = history[frame]
            attention_weights = record.attention_weights
            
            # Reshape if needed
            if len(attention_weights.shape) > 2:
                # For multi-head attention, average across heads
                if len(attention_weights.shape) == 3:
                    attention_weights = attention_weights.mean(dim=0)
                # For batched multi-head attention, average across batch and heads
                elif len(attention_weights.shape) == 4:
                    attention_weights = attention_weights.mean(dim=(0, 1))
            
            im.set_array(attention_weights.numpy())
            title.set_text(f"Epoch {record.epoch}, Batch {record.batch_idx}")
            return [im, title]
        
        # Create animation
        ani = animation.FuncAnimation(
            fig,
            update,
            frames=len(history),
            interval=1000 / fps,
            blit=True,
        )
        
        # Save animation
        ani.save(output_path, writer='pillow', fps=fps)
        plt.close(fig)
    
    def _create_neuron_firing_animation(
        self,
        history: List[ActivationRecord],
        output_path: str,
        fps: int,
    ) -> None:
        """
        Create an animation of neuron firing patterns.
        
        Args:
            history: Activation history
            output_path: Path to save the animation
            fps: Frames per second
        """
        # Check if history has output activations
        if not all(record.output_activation is not None for record in history):
            logger.warning("Not all records have output activations")
            return
        
        # Create figure
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Initialize with first record
        first_record = history[0]
        output_activation = first_record.output_activation
        
        # Reshape to 2D (neurons x batch*spatial)
        if len(output_activation.shape) > 2:
            # For convolutional layers, reshape to (channels, batch*height*width)
            output_activation = output_activation.reshape(output_activation.shape[0], -1)
        
        # Aggregate across batch/spatial dimensions
        if self.config.aggregation == ActivationAggregation.MEAN:
            aggregated = output_activation.mean(dim=1)
        elif self.config.aggregation == ActivationAggregation.MAX:
            aggregated = output_activation.max(dim=1)[0]
        elif self.config.aggregation == ActivationAggregation.MIN:
            aggregated = output_activation.min(dim=1)[0]
        elif self.config.aggregation == ActivationAggregation.STD:
            aggregated = output_activation.std(dim=1)
        elif self.config.aggregation == ActivationAggregation.ENTROPY:
            # Normalize to probabilities
            probs = F.softmax(output_activation, dim=1)
            aggregated = torch.tensor([entropy(p.numpy()) for p in probs])
        elif self.config.aggregation == ActivationAggregation.L1_NORM:
            aggregated = torch.norm(output_activation, p=1, dim=1)
        elif self.config.aggregation == ActivationAggregation.L2_NORM:
            aggregated = torch.norm(output_activation, p=2, dim=1)
        else:
            aggregated = output_activation.mean(dim=1)
        
        # Limit to top neurons for visualization
        max_neurons = 100
        if len(aggregated) > max_neurons:
            # Get top neurons by activation value
            top_indices = torch.argsort(aggregated, descending=True)[:max_neurons]
            aggregated = aggregated[top_indices]
        
        # Plot bar chart
        bars = ax.bar(range(len(aggregated)), aggregated.numpy())
        
        title = ax.set_title(f"Neuron Firing (Epoch {first_record.epoch}, Batch {first_record.batch_idx})")
        ax.set_xlabel("Neuron Index")
        ax.set_ylabel("Activation")
        
        # Animation update function
        def update(frame):
            record = history[frame]
            output_activation = record.output_activation
            
            # Reshape to 2D (neurons x batch*spatial)
            if len(output_activation.shape) > 2:
                # For convolutional layers, reshape to (channels, batch*height*width)
                output_activation = output_activation.reshape(output_activation.shape[0], -1)
            
            # Aggregate across batch/spatial dimensions
            if self.config.aggregation == ActivationAggregation.MEAN:
                aggregated = output_activation.mean(dim=1)
            elif self.config.aggregation == ActivationAggregation.MAX:
                aggregated = output_activation.max(dim=1)[0]
            elif self.config.aggregation == ActivationAggregation.MIN:
                aggregated = output_activation.min(dim=1)[0]
            elif self.config.aggregation == ActivationAggregation.STD:
                aggregated = output_activation.std(dim=1)
            elif self.config.aggregation == ActivationAggregation.ENTROPY:
                # Normalize to probabilities
                probs = F.softmax(output_activation, dim=1)
                aggregated = torch.tensor([entropy(p.numpy()) for p in probs])
            elif self.config.aggregation == ActivationAggregation.L1_NORM:
                aggregated = torch.norm(output_activation, p=1, dim=1)
            elif self.config.aggregation == ActivationAggregation.L2_NORM:
                aggregated = torch.norm(output_activation, p=2, dim=1)
            else:
                aggregated = output_activation.mean(dim=1)
            
            # Limit to top neurons for visualization
            if len(aggregated) > max_neurons:
                # Get top neurons by activation value
                top_indices = torch.argsort(aggregated, descending=True)[:max_neurons]
                aggregated = aggregated[top_indices]
            
            # Update bar heights
            for i, bar in enumerate(bars):
                bar.set_height(aggregated[i].item())
            
            title.set_text(f"Neuron Firing (Epoch {record.epoch}, Batch {record.batch_idx})")
            
            return bars + [title]
        
        # Create animation
        ani = animation.FuncAnimation(
            fig,
            update,
            frames=len(history),
            interval=1000 / fps,
            blit=True,
        )
        
        # Save animation
        ani.save(output_path, writer='pillow', fps=fps)
        plt.close(fig)
    
    def _create_activation_distribution_animation(
        self,
        history: List[ActivationRecord],
        output_path: str,
        fps: int,
    ) -> None:
        """
        Create an animation of activation distributions.
        
        Args:
            history: Activation history
            output_path: Path to save the animation
            fps: Frames per second
        """
        # Check if history has output activations
        if not all(record.output_activation is not None for record in history):
            logger.warning("Not all records have output activations")
            return
        
        # Create figure
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Initialize with first record
        first_record = history[0]
        output_activation = first_record.output_activation
        
        # Flatten activation
        flat_activation = output_activation.flatten().numpy()
        
        # Plot histogram
        n, bins, patches = ax.hist(flat_activation, bins=50, alpha=0.7)
        
        title = ax.set_title(f"Activation Distribution (Epoch {first_record.epoch}, Batch {first_record.batch_idx})")
        ax.set_xlabel("Activation Value")
        ax.set_ylabel("Frequency")
        
        # Add statistics
        mean = np.mean(flat_activation)
        std = np.std(flat_activation)
        
        stats_text = ax.text(
            0.05, 0.95, f"μ={mean:.4f}, σ={std:.4f}",
            transform=ax.transAxes,
            verticalalignment='top',
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.8)
        )
        
        # Animation update function
        def update(frame):
            record = history[frame]
            output_activation = record.output_activation
            
            # Flatten activation
            flat_activation = output_activation.flatten().numpy()
            
            # Update histogram
            n, bins = np.histogram(flat_activation, bins=50)
            
            for i, rect in enumerate(patches):
                rect.set_height(n[i])
            
            title.set_text(f"Activation Distribution (Epoch {record.epoch}, Batch {record.batch_idx})")
            
            # Update statistics
            mean = np.mean(flat_activation)
            std = np.std(flat_activation)
            stats_text.set_text(f"μ={mean:.4f}, σ={std:.4f}")
            
            return patches + [title, stats_text]
        
        # Create animation
        ani = animation.FuncAnimation(
            fig,
            update,
            frames=len(history),
            interval=1000 / fps,
            blit=True,
        )
        
        # Save animation
        ani.save(output_path, writer='pillow', fps=fps)
        plt.close(fig)
    
    def save_activation_history(self, output_path: Optional[str] = None) -> Optional[str]:
        """
        Save activation history to a file.
        
        Args:
            output_path: Path to save the history
            
        Returns:
            Path to the saved file or None
        """
        if not output_path:
            output_path = os.path.join(
                self.output_dir,
                f"activation_history_step_{self.current_step}.pkl"
            )
        
        try:
            # Convert activation history to serializable format
            serializable_history = {}
            
            for layer_name, records in self.activation_history.items():
                serializable_records = []
                
                for record in records:
                    # Convert tensors to numpy arrays
                    serializable_record = {
                        "layer_name": record.layer_name,
                        "step": record.step,
                        "epoch": record.epoch,
                        "batch_idx": record.batch_idx,
                        "timestamp": record.timestamp,
                    }
                    
                    if record.input_activation is not None:
                        serializable_record["input_activation"] = record.input_activation.numpy()
                    
                    if record.output_activation is not None:
                        serializable_record["output_activation"] = record.output_activation.numpy()
                    
                    if record.attention_weights is not None:
                        serializable_record["attention_weights"] = record.attention_weights.numpy()
                    
                    if record.gradient is not None:
                        serializable_record["gradient"] = record.gradient.numpy()
                    
                    if record.custom_data:
                        serializable_record["custom_data"] = record.custom_data
                    
                    serializable_records.append(serializable_record)
                
                serializable_history[layer_name] = serializable_records
            
            # Save to file
            with open(output_path, "wb") as f:
                pickle.dump(serializable_history, f)
            
            logger.info(f"Saved activation history to {output_path}")
            return output_path
        
        except Exception as e:
            logger.error(f"Error saving activation history: {e}")
            logger.error(traceback.format_exc())
            return None
    
    def load_activation_history(self, input_path: str) -> bool:
        """
        Load activation history from a file.
        
        Args:
            input_path: Path to the history file
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Load from file
            with open(input_path, "rb") as f:
                serializable_history = pickle.load(f)
            
            # Convert to activation records
            activation_history = {}
            
            for layer_name, serializable_records in serializable_history.items():
                records = []
                
                for serializable_record in serializable_records:
                    # Convert numpy arrays to tensors
                    record = ActivationRecord(
                        layer_name=serializable_record["layer_name"],
                        step=serializable_record["step"],
                        epoch=serializable_record["epoch"],
                        batch_idx=serializable_record["batch_idx"],
                        timestamp=serializable_record["timestamp"],
                    )
                    
                    if "input_activation" in serializable_record:
                        record.input_activation = torch.from_numpy(serializable_record["input_activation"])
                    
                    if "output_activation" in serializable_record:
                        record.output_activation = torch.from_numpy(serializable_record["output_activation"])
                    
                    if "attention_weights" in serializable_record:
                        record.attention_weights = torch.from_numpy(serializable_record["attention_weights"])
                    
                    if "gradient" in serializable_record:
                        record.gradient = torch.from_numpy(serializable_record["gradient"])
                    
                    if "custom_data" in serializable_record:
                        record.custom_data = serializable_record["custom_data"]
                    
                    records.append(record)
                
                activation_history[layer_name] = records
            
            # Update activation history
            self.activation_history = activation_history
            
            logger.info(f"Loaded activation history from {input_path}")
            return True
        
        except Exception as e:
            logger.error(f"Error loading activation history: {e}")
            logger.error(traceback.format_exc())
            return False
    
    def generate_report(self, output_path: Optional[str] = None) -> Optional[str]:
        """
        Generate a comprehensive report of model cognition.
        
        Args:
            output_path: Path to save the report
            
        Returns:
            Path to the saved report or None
        """
        if not output_path:
            output_path = os.path.join(
                self.output_dir,
                f"model_cognition_report_step_{self.current_step}.html"
            )
        
        try:
            # Create report
            report = []
            
            # Add header
            report.append("<html>")
            report.append("<head>")
            report.append("<title>Model Cognition Report</title>")
            report.append("<style>")
            report.append("body { font-family: Arial, sans-serif; margin: 20px; }")
            report.append("h1, h2, h3 { color: #333; }")
            report.append("table { border-collapse: collapse; width: 100%; }")
            report.append("th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }")
            report.append("th { background-color: #f2f2f2; }")
            report.append("tr:nth-child(even) { background-color: #f9f9f9; }")
            report.append("img { max-width: 100%; height: auto; }")
            report.append(".section { margin-bottom: 30px; }")
            report.append("</style>")
            report.append("</head>")
            report.append("<body>")
            
            # Add title
            report.append(f"<h1>Model Cognition Report (Step {self.current_step})</h1>")
            
            # Add model summary
            report.append("<div class='section'>")
            report.append("<h2>Model Summary</h2>")
            report.append("<table>")
            report.append("<tr><th>Layer</th><th>Type</th><th>Parameters</th><th>Input Shape</th><th>Output Shape</th></tr>")
            
            for layer_name, layer_info in self.layer_info.items():
                report.append("<tr>")
                report.append(f"<td>{layer_name}</td>")
                report.append(f"<td>{layer_info.layer_type.value}</td>")
                report.append(f"<td>{layer_info.parameters_count:,}</td>")
                report.append(f"<td>{layer_info.input_shape if layer_info.input_shape else 'N/A'}</td>")
                report.append(f"<td>{layer_info.output_shape if layer_info.output_shape else 'N/A'}</td>")
                report.append("</tr>")
            
            report.append("</table>")
            report.append("</div>")
            
            # Add visualizations
            report.append("<div class='section'>")
            report.append("<h2>Visualizations</h2>")
            
            # Generate visualizations if not already generated
            visualization_types = [
                (VisualizationType.ATTENTION_HEATMAP, "Attention Heatmaps"),
                (VisualizationType.NEURON_FIRING, "Neuron Firing Patterns"),
                (VisualizationType.ACTIVATION_DISTRIBUTION, "Activation Distributions"),
                (VisualizationType.GRADIENT_FLOW, "Gradient Flow"),
                (VisualizationType.FEATURE_SPACE, "Feature Space"),
                (VisualizationType.LAYER_SIMILARITY, "Layer Similarity"),
            ]
            
            for vis_type, vis_name in visualization_types:
                # Check if visualization exists
                vis_path = os.path.join(
                    self.output_dir,
                    f"{vis_type.value}_step_{self.current_step}.png"
                )
                
                if not os.path.exists(vis_path):
                    # Generate visualization
                    original_type = self.config.type
                    self.config.type = vis_type
                    self._generate_visualization()
                    self.config.type = original_type
                
                # Add to report if exists
                if os.path.exists(vis_path):
                    report.append(f"<h3>{vis_name}</h3>")
                    report.append(f"<img src='{vis_path}' alt='{vis_name}'>")
            
            report.append("</div>")
            
            # Add activation statistics
            report.append("<div class='section'>")
            report.append("<h2>Activation Statistics</h2>")
            report.append("<table>")
            report.append("<tr><th>Layer</th><th>Mean</th><th>Std</th><th>Min</th><th>Max</th></tr>")
            
            for layer_name in self.config.layers:
                if layer_name in self.activation_history and self.activation_history[layer_name]:
                    latest_record = self.activation_history[layer_name][-1]
                    
                    if latest_record.output_activation is not None:
                        activation = latest_record.output_activation
                        flat_activation = activation.flatten().numpy()
                        
                        mean = np.mean(flat_activation)
                        std = np.std(flat_activation)
                        min_val = np.min(flat_activation)
                        max_val = np.max(flat_activation)
                        
                        report.append("<tr>")
                        report.append(f"<td>{layer_name}</td>")
                        report.append(f"<td>{mean:.4f}</td>")
                        report.append(f"<td>{std:.4f}</td>")
                        report.append(f"<td>{min_val:.4f}</td>")
                        report.append(f"<td>{max_val:.4f}</td>")
                        report.append("</tr>")
            
            report.append("</table>")
            report.append("</div>")
            
            # Add footer
            report.append("<div class='section'>")
            report.append("<h2>Report Information</h2>")
            report.append(f"<p>Generated at: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>")
            report.append(f"<p>Step: {self.current_step}</p>")
            report.append(f"<p>Epoch: {self.current_epoch}</p>")
            report.append(f"<p>Batch: {self.current_batch_idx}</p>")
            report.append("</div>")
            
            report.append("</body>")
            report.append("</html>")
            
            # Save report
            with open(output_path, "w") as f:
                f.write("\n".join(report))
            
            logger.info(f"Generated model cognition report at {output_path}")
            return output_path
        
        except Exception as e:
            logger.error(f"Error generating report: {e}")
            logger.error(traceback.format_exc())
            return None
    
    def clear_history(self) -> None:
        """Clear activation history."""
        self.activation_history = defaultdict(list)
        logger.info("Cleared activation history")
    
    def get_layer_info(self, layer_name: Optional[str] = None) -> Union[Dict[str, LayerInfo], Optional[LayerInfo]]:
        """
        Get information about layers.
        
        Args:
            layer_name: Name of the layer or None for all layers
            
        Returns:
            Layer information
        """
        if layer_name:
            return self.layer_info.get(layer_name)
        return self.layer_info
    
    def get_activation_history(self, layer_name: Optional[str] = None) -> Union[Dict[str, List[ActivationRecord]], List[ActivationRecord]]:
        """
        Get activation history.
        
        Args:
            layer_name: Name of the layer or None for all layers
            
        Returns:
            Activation history
        """
        if layer_name:
            return self.activation_history.get(layer_name, [])
        return self.activation_history
    
    def __del__(self) -> None:
        """Clean up resources."""
        self.stop()


class ModelCognitionHook:
    """
    Hook for integrating ModelCognitionVisualizer with training loops.
    
    This class provides a simple way to integrate the ModelCognitionVisualizer
    with training loops in PyTorch, PyTorch Lightning, and other frameworks.
    
    Attributes:
        visualizer: ModelCognitionVisualizer instance
        update_interval: Interval for updating visualizations (in steps)
        save_interval: Interval for saving visualizations (in steps)
        report_interval: Interval for generating reports (in steps)
        animation_interval: Interval for creating animations (in steps)
        current_step: Current step
        current_epoch: Current epoch
        current_batch_idx: Current batch index
    """
    
    def __init__(
        self,
        model: nn.Module,
        config: Optional[VisualizationConfig] = None,
        output_dir: str = "./mindscope_output",
        update_interval: int = 10,
        save_interval: int = 100,
        report_interval: int = 500,
        animation_interval: int = 1000,
    ):
        """
        Initialize the ModelCognitionHook.
        
        Args:
            model: PyTorch model
            config: Visualization configuration
            output_dir: Directory for saving visualizations
            update_interval: Interval for updating visualizations (in steps)
            save_interval: Interval for saving visualizations (in steps)
            report_interval: Interval for generating reports (in steps)
            animation_interval: Interval for creating animations (in steps)
        """
        self.visualizer = ModelCognitionVisualizer(model, config, output_dir)
        self.update_interval = update_interval
        self.save_interval = save_interval
        self.report_interval = report_interval
        self.animation_interval = animation_interval
        
        self.current_step = 0
        self.current_epoch = 0
        self.current_batch_idx = 0
        
        logger.info(f"Initialized ModelCognitionHook with update_interval={update_interval}, save_interval={save_interval}")
    
    def on_train_start(self) -> None:
        """Called when training starts."""
        self.visualizer.start(self.current_step, self.current_epoch, self.current_batch_idx)
        logger.info("Started ModelCognitionHook")
    
    def on_train_end(self) -> None:
        """Called when training ends."""
        # Generate final report
        self.visualizer.generate_report()
        
        # Save activation history
        self.visualizer.save_activation_history()
        
        # Stop visualizer
        self.visualizer.stop()
        
        logger.info("Stopped ModelCognitionHook")
    
    def on_epoch_start(self, epoch: int) -> None:
        """
        Called when an epoch starts.
        
        Args:
            epoch: Current epoch
        """
        self.current_epoch = epoch
        self.visualizer.update_step(self.current_step, self.current_epoch, self.current_batch_idx)
    
    def on_epoch_end(self, epoch: int) -> None:
        """
        Called when an epoch ends.
        
        Args:
            epoch: Current epoch
        """
        # Generate report at epoch end if report_interval is reached
        if self.current_epoch > 0 and self.current_epoch % max(1, self.report_interval // 10) == 0:
            self.visualizer.generate_report()
    
    def on_batch_start(self, batch_idx: int) -> None:
        """
        Called when a batch starts.
        
        Args:
            batch_idx: Current batch index
        """
        self.current_batch_idx = batch_idx
        self.visualizer.update_step(self.current_step, self.current_epoch, self.current_batch_idx)
    
    def on_batch_end(self, batch_idx: int) -> None:
        """
        Called when a batch ends.
        
        Args:
            batch_idx: Current batch index
        """
        self.current_step += 1
        self.visualizer.update_step(self.current_step, self.current_epoch, self.current_batch_idx)
        
        # Update visualizations if update_interval is reached
        if self.current_step % self.update_interval == 0:
            # This is handled automatically by the visualizer's internal thread
            pass
        
        # Save visualizations if save_interval is reached
        if self.current_step % self.save_interval == 0:
            # Save current visualization
            original_type = self.visualizer.config.type
            
            for vis_type in [
                VisualizationType.ATTENTION_HEATMAP,
                VisualizationType.NEURON_FIRING,
                VisualizationType.ACTIVATION_DISTRIBUTION,
                VisualizationType.GRADIENT_FLOW,
            ]:
                self.visualizer.config.type = vis_type
                self.visualizer._generate_visualization()
            
            # Restore original type
            self.visualizer.config.type = original_type
        
        # Create animations if animation_interval is reached
        if self.current_step % self.animation_interval == 0:
            # Create animations for attention layers
            for layer_name in self.visualizer.config.layers:
                if layer_name in self.visualizer.activation_history and self.visualizer.activation_history[layer_name]:
                    latest_record = self.visualizer.activation_history[layer_name][-1]
                    
                    if latest_record.attention_weights is not None:
                        self.visualizer.create_animation(
                            VisualizationType.ATTENTION_HEATMAP,
                            layer_name,
                        )
    
    def on_backward_end(self) -> None:
        """Called after backward pass."""
        # This is when gradients are available
        pass
    
    def pytorch_hook(self, model: nn.Module, optimizer: torch.optim.Optimizer) -> Callable:
        """
        Create a hook for PyTorch training loops.
        
        Args:
            model: PyTorch model
            optimizer: PyTorch optimizer
            
        Returns:
            Hook function
        """
        def hook(engine, batch):
            # Call appropriate hooks based on engine state
            if engine.state.iteration == 1:
                self.on_train_start()
            
            if engine.state.epoch_length and engine.state.iteration % engine.state.epoch_length == 1:
                self.on_epoch_start(engine.state.epoch)
            
            batch_idx = engine.state.iteration % engine.state.epoch_length if engine.state.epoch_length else engine.state.iteration
            self.on_batch_start(batch_idx)
            
            # Forward pass
            inputs, targets = batch
            outputs = model(inputs)
            loss = engine.state.loss_fn(outputs, targets)
            
            # Backward pass
            optimizer.zero_grad()
            loss.backward()
            self.on_backward_end()
            optimizer.step()
            
            self.on_batch_end(batch_idx)
            
            if engine.state.epoch_length and engine.state.iteration % engine.state.epoch_length == 0:
                self.on_epoch_end(engine.state.epoch)
            
            if engine.state.max_epochs and engine.state.epoch >= engine.state.max_epochs:
                self.on_train_end()
            
            return loss.item()
        
        return hook
    
    def lightning_hooks(self) -> Dict[str, Callable]:
        """
        Create hooks for PyTorch Lightning.
        
        Returns:
            Dictionary of hook functions
        """
        hooks = {
            "on_train_start": lambda trainer, pl_module: self.on_train_start(),
            "on_train_end": lambda trainer, pl_module: self.on_train_end(),
            "on_train_epoch_start": lambda trainer, pl_module: self.on_epoch_start(trainer.current_epoch),
            "on_train_epoch_end": lambda trainer, pl_module: self.on_epoch_end(trainer.current_epoch),
            "on_train_batch_start": lambda trainer, pl_module, batch, batch_idx: self.on_batch_start(batch_idx),
            "on_train_batch_end": lambda trainer, pl_module, outputs, batch, batch_idx: self.on_batch_end(batch_idx),
            "on_after_backward": lambda trainer, pl_module: self.on_backward_end(),
        }
        
        return hooks
    
    def huggingface_hooks(self) -> Dict[str, Callable]:
        """
        Create hooks for HuggingFace Transformers.
        
        Returns:
            Dictionary of hook functions
        """
        hooks = {
            "on_train_begin": lambda args, state, control: self.on_train_start(),
            "on_train_end": lambda args, state, control: self.on_train_end(),
            "on_epoch_begin": lambda args, state, control: self.on_epoch_start(state.epoch),
            "on_epoch_end": lambda args, state, control: self.on_epoch_end(state.epoch),
            "on_step_begin": lambda args, state, control: self.on_batch_start(state.global_step),
            "on_step_end": lambda args, state, control: self.on_batch_end(state.global_step),
            "on_backward": lambda args, state, control: self.on_backward_end(),
        }
        
        return hooks
