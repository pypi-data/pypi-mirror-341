"""
Memory profiler for monitoring model memory usage.

This module provides functionality to monitor memory usage of PyTorch models
during training, including tensor allocations, fragmentation, and peak usage.
"""

import logging
import gc
from typing import Dict, Any, Optional, Union, List

import torch
import psutil

logger = logging.getLogger(__name__)

class MemoryProfiler:
    """
    Profiler for monitoring memory usage of PyTorch models.
    
    This class tracks memory usage, tensor allocations, and memory fragmentation
    during model training.
    
    Attributes:
        model: The PyTorch model to monitor
        device: The device the model is on (CPU or GPU)
        is_profiling: Whether profiling is active
        metrics: Dictionary of collected metrics
    """
    
    def __init__(
        self, 
        model: Optional[torch.nn.Module] = None,
        device: Optional[Union[str, torch.device]] = None
    ):
        """
        Initialize the memory profiler.
        
        Args:
            model: The PyTorch model to monitor
            device: The device the model is on (CPU or GPU)
        """
        self.model = model
        self.device = device or (
            next(model.parameters()).device if model is not None else torch.device("cpu")
        )
        self.is_profiling = False
        self.metrics = {
            "allocated_memory": 0,
            "reserved_memory": 0,
            "max_allocated_memory": 0,
            "max_reserved_memory": 0,
            "memory_fragmentation": 0.0,
            "model_size": 0,
            "parameter_count": 0,
            "buffer_count": 0,
            "largest_layer_memory": 0,
            "largest_layer_name": "",
        }
        
        if model is not None:
            self._init_model_metrics()
    
    def _init_model_metrics(self):
        """Initialize model-specific metrics."""
        if self.model is None:
            return
        
        # Count parameters and buffers
        parameter_count = sum(p.numel() for p in self.model.parameters())
        buffer_count = sum(b.numel() for b in self.model.buffers())
        
        # Calculate model size in MB
        model_size = sum(p.numel() * p.element_size() for p in self.model.parameters())
        model_size += sum(b.numel() * b.element_size() for b in self.model.buffers())
        model_size = model_size / (1024 * 1024)  # Convert to MB
        
        # Find largest layer
        largest_size = 0
        largest_name = ""
        
        for name, module in self.model.named_modules():
            params_size = sum(p.numel() * p.element_size() for p in module.parameters(recurse=False))
            buffers_size = sum(b.numel() * b.element_size() for b in module.buffers(recurse=False))
            total_size = params_size + buffers_size
            
            if total_size > largest_size:
                largest_size = total_size
                largest_name = name
        
        largest_size = largest_size / (1024 * 1024)  # Convert to MB
        
        # Update metrics
        self.metrics["parameter_count"] = parameter_count
        self.metrics["buffer_count"] = buffer_count
        self.metrics["model_size"] = model_size
        self.metrics["largest_layer_memory"] = largest_size
        self.metrics["largest_layer_name"] = largest_name
    
    def start(self):
        """Start profiling memory usage."""
        self.is_profiling = True
        
        # Reset peak memory stats
        if self.device.type == "cuda" and torch.cuda.is_available():
            torch.cuda.reset_peak_memory_stats(self.device)
        
        logger.info("Memory profiling started")
        return self
    
    def stop(self):
        """Stop profiling memory usage."""
        self.is_profiling = False
        logger.info("Memory profiling stopped")
        return self
    
    def _update_memory_metrics(self):
        """Update memory-related metrics."""
        if self.device.type == "cuda" and torch.cuda.is_available():
            # CUDA memory stats
            self.metrics["allocated_memory"] = torch.cuda.memory_allocated(self.device) / (1024 * 1024)  # MB
            self.metrics["reserved_memory"] = torch.cuda.memory_reserved(self.device) / (1024 * 1024)  # MB
            self.metrics["max_allocated_memory"] = torch.cuda.max_memory_allocated(self.device) / (1024 * 1024)  # MB
            self.metrics["max_reserved_memory"] = torch.cuda.max_memory_reserved(self.device) / (1024 * 1024)  # MB
            
            # Calculate fragmentation
            if self.metrics["reserved_memory"] > 0:
                self.metrics["memory_fragmentation"] = 1.0 - (self.metrics["allocated_memory"] / self.metrics["reserved_memory"])
        else:
            # CPU memory stats (less detailed)
            process = psutil.Process()
            memory_info = process.memory_info()
            
            self.metrics["allocated_memory"] = memory_info.rss / (1024 * 1024)  # MB
            self.metrics["reserved_memory"] = memory_info.vms / (1024 * 1024)  # MB
            
            # These are just estimates for CPU
            self.metrics["max_allocated_memory"] = max(self.metrics["max_allocated_memory"], self.metrics["allocated_memory"])
            self.metrics["max_reserved_memory"] = max(self.metrics["max_reserved_memory"], self.metrics["reserved_memory"])
            
            # Rough estimate of fragmentation
            if self.metrics["reserved_memory"] > 0:
                self.metrics["memory_fragmentation"] = 1.0 - (self.metrics["allocated_memory"] / self.metrics["reserved_memory"])
    
    def get_layer_memory_usage(self) -> Dict[str, float]:
        """
        Get memory usage by layer.
        
        Returns:
            Dictionary mapping layer names to memory usage in MB
        """
        if self.model is None:
            return {}
        
        layer_memory = {}
        
        for name, module in self.model.named_modules():
            params_size = sum(p.numel() * p.element_size() for p in module.parameters(recurse=False))
            buffers_size = sum(b.numel() * b.element_size() for b in module.buffers(recurse=False))
            total_size = (params_size + buffers_size) / (1024 * 1024)  # Convert to MB
            
            if total_size > 0:
                layer_memory[name] = total_size
        
        return layer_memory
    
    def get_metrics(self) -> Dict[str, Any]:
        """
        Get current memory metrics.
        
        Returns:
            Dictionary of memory metrics
        """
        if self.is_profiling:
            self._update_memory_metrics()
        
        return self.metrics.copy()
    
    def predict_oom_risk(self) -> float:
        """
        Predict risk of out-of-memory error.
        
        Returns:
            Risk score between 0.0 and 1.0
        """
        if self.device.type != "cuda" or not torch.cuda.is_available():
            return 0.0
        
        # Get total GPU memory
        total_memory = torch.cuda.get_device_properties(self.device).total_memory / (1024 * 1024)  # MB
        
        # Calculate current usage percentage
        usage_percent = self.metrics["reserved_memory"] / total_memory
        
        # Calculate growth rate (simplified)
        growth_rate = 1.0
        if self.metrics["max_reserved_memory"] > 0:
            growth_rate = self.metrics["reserved_memory"] / self.metrics["max_reserved_memory"]
        
        # Calculate fragmentation penalty
        frag_penalty = self.metrics["memory_fragmentation"] * 0.5
        
        # Calculate OOM risk score
        risk_score = (usage_percent * 0.7) + (growth_rate * 0.2) + frag_penalty
        
        # Clamp between 0 and 1
        risk_score = max(0.0, min(1.0, risk_score))
        
        return risk_score
    
    def __repr__(self) -> str:
        """String representation of the memory profiler."""
        status = "profiling" if self.is_profiling else "not profiling"
        device = self.device
        return f"MemoryProfiler(status={status}, device={device})"
