"""
Gradient profiler for monitoring gradient statistics.

This module provides functionality to monitor gradient statistics during model training,
including gradient norms, gradient clipping, and dead/exploding gradients detection.
"""

import logging
from typing import Dict, Any, Optional, List, Tuple, Union
from collections import deque

import torch
import numpy as np

logger = logging.getLogger(__name__)

class GradientProfiler:
    """
    Profiler for monitoring gradient statistics.
    
    This class tracks gradient statistics during model training, including
    gradient norms, gradient clipping, and dead/exploding gradients detection.
    
    Attributes:
        model: The PyTorch model to monitor
        is_profiling: Whether profiling is active
        metrics: Dictionary of collected metrics
        grad_norms: Deque of recent gradient norms
    """
    
    def __init__(self, model: Optional[torch.nn.Module] = None):
        """
        Initialize the gradient profiler.
        
        Args:
            model: The PyTorch model to monitor
        """
        self.model = model
        self.is_profiling = False
        self.metrics = {
            "avg_grad_norm": 0.0,
            "max_grad_norm": 0.0,
            "min_grad_norm": 0.0,
            "dead_gradients_pct": 0.0,
            "exploding_gradients_pct": 0.0,
            "clipped_gradients_pct": 0.0,
            "param_groups": 0,
            "total_params": 0,
            "params_with_grad": 0,
        }
        self.grad_norms = deque(maxlen=100)  # Store last 100 gradient norms
        self.hooks = []
        self.param_grad_stats = {}
        
        if model is not None:
            self._init_model_metrics()
    
    def _init_model_metrics(self):
        """Initialize model-specific metrics."""
        if self.model is None:
            return
        
        # Count parameters
        total_params = sum(p.numel() for p in self.model.parameters())
        params_with_grad = sum(p.numel() for p in self.model.parameters() if p.requires_grad)
        
        self.metrics["total_params"] = total_params
        self.metrics["params_with_grad"] = params_with_grad
    
    def start(self):
        """Start profiling gradient statistics."""
        if self.model is None:
            logger.warning("Cannot start gradient profiling without a model")
            return self
        
        self.is_profiling = True
        
        # Register hooks for all parameters
        for name, param in self.model.named_parameters():
            if param.requires_grad:
                hook = param.register_hook(lambda grad, name=name: self._grad_hook(grad, name))
                self.hooks.append(hook)
                self.param_grad_stats[name] = {
                    "zero_count": 0,
                    "large_count": 0,
                    "total_count": 0,
                    "last_norm": 0.0,
                }
        
        logger.info("Gradient profiling started")
        return self
    
    def stop(self):
        """Stop profiling gradient statistics."""
        # Remove hooks
        for hook in self.hooks:
            hook.remove()
        self.hooks = []
        
        self.is_profiling = False
        logger.info("Gradient profiling stopped")
        return self
    
    def _grad_hook(self, grad: torch.Tensor, name: str):
        """
        Hook function called when gradients are computed.
        
        Args:
            grad: The gradient tensor
            name: Name of the parameter
        
        Returns:
            The gradient tensor (unchanged)
        """
        if not self.is_profiling:
            return grad
        
        # Calculate gradient norm
        if grad is not None:
            with torch.no_grad():
                grad_norm = grad.norm().item()
                
                # Update parameter-specific stats
                if name in self.param_grad_stats:
                    stats = self.param_grad_stats[name]
                    stats["total_count"] += 1
                    stats["last_norm"] = grad_norm
                    
                    # Check for zero gradients (dead)
                    if grad_norm < 1e-8:
                        stats["zero_count"] += 1
                    
                    # Check for large gradients (exploding)
                    if grad_norm > 1.0:
                        stats["large_count"] += 1
        
        return grad
    
    def after_backward(self):
        """
        Record gradient statistics after backward pass.
        
        This should be called after each backward pass.
        """
        if not self.is_profiling or self.model is None:
            return
        
        # Calculate global gradient norm
        total_norm = 0.0
        for p in self.model.parameters():
            if p.grad is not None:
                param_norm = p.grad.data.norm(2)
                total_norm += param_norm.item() ** 2
        total_norm = total_norm ** 0.5
        
        # Add to gradient norms
        self.grad_norms.append(total_norm)
        
        # Update metrics
        self._update_grad_metrics()
    
    def _update_grad_metrics(self):
        """Update gradient-related metrics."""
        if not self.grad_norms:
            return
        
        # Calculate statistics for gradient norms
        grad_norms = np.array(self.grad_norms)
        self.metrics["avg_grad_norm"] = np.mean(grad_norms)
        self.metrics["max_grad_norm"] = np.max(grad_norms)
        self.metrics["min_grad_norm"] = np.min(grad_norms)
        
        # Calculate dead and exploding gradients percentages
        total_params = 0
        zero_grads = 0
        large_grads = 0
        
        for name, stats in self.param_grad_stats.items():
            if stats["total_count"] > 0:
                total_params += 1
                zero_pct = stats["zero_count"] / stats["total_count"]
                large_pct = stats["large_count"] / stats["total_count"]
                
                if zero_pct > 0.9:  # If >90% of gradients are zero
                    zero_grads += 1
                
                if large_pct > 0.1:  # If >10% of gradients are large
                    large_grads += 1
        
        if total_params > 0:
            self.metrics["dead_gradients_pct"] = (zero_grads / total_params) * 100
            self.metrics["exploding_gradients_pct"] = (large_grads / total_params) * 100
    
    def get_metrics(self) -> Dict[str, Any]:
        """
        Get current gradient metrics.
        
        Returns:
            Dictionary of gradient metrics
        """
        return self.metrics.copy()
    
    def get_layer_grad_norms(self) -> Dict[str, float]:
        """
        Get gradient norms by layer.
        
        Returns:
            Dictionary mapping layer names to gradient norms
        """
        layer_norms = {}
        
        for name, stats in self.param_grad_stats.items():
            if stats["total_count"] > 0:
                layer_norms[name] = stats["last_norm"]
        
        return layer_norms
    
    def get_optimization_suggestions(self) -> List[Dict[str, Any]]:
        """
        Get optimization suggestions based on gradient statistics.
        
        Returns:
            List of optimization suggestions
        """
        suggestions = []
        
        if not self.is_profiling or not self.grad_norms:
            return suggestions
        
        # Check for dead gradients
        if self.metrics["dead_gradients_pct"] > 20:
            suggestions.append({
                "type": "dead_gradients",
                "severity": "high",
                "message": f"Dead gradients detected in {self.metrics['dead_gradients_pct']:.1f}% of parameters",
                "details": "Many parameters have near-zero gradients. This may indicate vanishing gradients or dead neurons.",
                "code": "# Consider these options:\n"
                        "# 1. Change activation functions (e.g., from sigmoid to ReLU)\n"
                        "# 2. Use batch normalization\n"
                        "# 3. Adjust learning rate\n"
                        "# 4. Initialize weights differently",
            })
        
        # Check for exploding gradients
        if self.metrics["exploding_gradients_pct"] > 10:
            suggestions.append({
                "type": "exploding_gradients",
                "severity": "high",
                "message": f"Exploding gradients detected in {self.metrics['exploding_gradients_pct']:.1f}% of parameters",
                "details": "Many parameters have very large gradients. This may cause training instability.",
                "code": "# Consider these options:\n"
                        "# 1. Use gradient clipping\n"
                        "# 2. Reduce learning rate\n"
                        "# 3. Use weight normalization\n"
                        "# 4. Add regularization",
            })
        
        # Check for gradient clipping need
        if self.metrics["max_grad_norm"] > 10.0:
            suggestions.append({
                "type": "gradient_clipping",
                "severity": "medium",
                "message": f"Consider using gradient clipping (max norm: {self.metrics['max_grad_norm']:.2f})",
                "details": "Gradient norms are high. Gradient clipping can help stabilize training.",
                "code": "# Add gradient clipping to your optimizer step\n"
                        "torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)",
            })
        
        return suggestions
    
    def __repr__(self) -> str:
        """String representation of the gradient profiler."""
        status = "profiling" if self.is_profiling else "not profiling"
        return f"GradientProfiler(status={status})"
