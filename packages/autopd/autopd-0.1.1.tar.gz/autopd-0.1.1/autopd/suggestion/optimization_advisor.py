"""
Optimization advisor module for AutoPipelineDoctor.

This module provides intelligent optimization suggestions and automatic
application of optimizations for ML/AI training pipelines.
"""

import logging
import os
from typing import Dict, Any, Optional, List, Tuple, Union, Callable
import inspect
import functools
import warnings
from enum import Enum, auto

import torch
from torch.optim import Optimizer
from torch.utils.data import DataLoader

from autopd.profiler.memory_profiler import MemoryProfiler
from autopd.profiler.timing_profiler import TimingProfiler
from autopd.profiler.dataloader_profiler import DataloaderProfiler
from autopd.profiler.gradient_profiler import GradientProfiler
from autopd.bottleneck.failure_forecaster import FailureForecaster

logger = logging.getLogger(__name__)


class OptimizationLevel(Enum):
    """Optimization level for automatic optimizations."""
    NONE = auto()  # No optimizations
    CONSERVATIVE = auto()  # Safe optimizations only
    BALANCED = auto()  # Balance between performance and safety
    AGGRESSIVE = auto()  # Aggressive optimizations for maximum performance


class OptimizationCategory(Enum):
    """Category of optimization."""
    MEMORY = auto()  # Memory-related optimizations
    PERFORMANCE = auto()  # Performance-related optimizations
    CONVERGENCE = auto()  # Training convergence-related optimizations
    DATALOADER = auto()  # Dataloader-related optimizations
    PRECISION = auto()  # Precision-related optimizations
    SCHEDULER = auto()  # Learning rate scheduler-related optimizations


class OptimizationAdvisor:
    """
    Advisor for ML/AI training pipeline optimizations.
    
    This class provides intelligent optimization suggestions and automatic
    application of optimizations for ML/AI training pipelines.
    
    Attributes:
        model: The PyTorch model to optimize
        optimizer: The optimizer used for training
        dataloader: The dataloader used for training
        device: The device the model is on (CPU or GPU)
        memory_profiler: Memory profiler for memory-related optimizations
        timing_profiler: Timing profiler for performance-related optimizations
        dataloader_profiler: Dataloader profiler for dataloader-related optimizations
        gradient_profiler: Gradient profiler for gradient-related optimizations
        failure_forecaster: Failure forecaster for predictive optimizations
        optimization_level: Level of automatic optimizations to apply
        is_active: Whether the advisor is active
        applied_optimizations: List of optimizations that have been applied
        available_optimizations: Dictionary of available optimizations
    """
    
    def __init__(
        self,
        model: Optional[torch.nn.Module] = None,
        optimizer: Optional[Optimizer] = None,
        dataloader: Optional[DataLoader] = None,
        device: Optional[Union[str, torch.device]] = None,
        memory_profiler: Optional[MemoryProfiler] = None,
        timing_profiler: Optional[TimingProfiler] = None,
        dataloader_profiler: Optional[DataloaderProfiler] = None,
        gradient_profiler: Optional[GradientProfiler] = None,
        failure_forecaster: Optional[FailureForecaster] = None,
        optimization_level: OptimizationLevel = OptimizationLevel.BALANCED,
    ):
        """
        Initialize the optimization advisor.
        
        Args:
            model: The PyTorch model to optimize
            optimizer: The optimizer used for training
            dataloader: The dataloader used for training
            device: The device the model is on (CPU or GPU)
            memory_profiler: Memory profiler for memory-related optimizations
            timing_profiler: Timing profiler for performance-related optimizations
            dataloader_profiler: Dataloader profiler for dataloader-related optimizations
            gradient_profiler: Gradient profiler for gradient-related optimizations
            failure_forecaster: Failure forecaster for predictive optimizations
            optimization_level: Level of automatic optimizations to apply
        """
        self.model = model
        self.optimizer = optimizer
        self.dataloader = dataloader
        self.device = device or (
            next(model.parameters()).device if model is not None else torch.device("cpu")
        )
        self.memory_profiler = memory_profiler
        self.timing_profiler = timing_profiler
        self.dataloader_profiler = dataloader_profiler
        self.gradient_profiler = gradient_profiler
        self.failure_forecaster = failure_forecaster
        self.optimization_level = optimization_level
        self.is_active = False
        self.applied_optimizations = []
        
        # Register available optimizations
        self.available_optimizations = {
            "amp": self._optimize_amp,
            "bfloat16": self._optimize_bfloat16,
            "dataloader_workers": self._optimize_dataloader_workers,
            "batch_size": self._optimize_batch_size,
            "gradient_checkpointing": self._optimize_gradient_checkpointing,
            "memory_efficient_attention": self._optimize_memory_efficient_attention,
            "optimizer_memory": self._optimize_optimizer_memory,
            "scheduler": self._optimize_scheduler,
            "gradient_accumulation": self._optimize_gradient_accumulation,
            "channels_last": self._optimize_channels_last,
            "compile": self._optimize_compile,
        }
    
    def start(self):
        """Start the optimization advisor."""
        self.is_active = True
        logger.info("Optimization advisor started")
        return self
    
    def stop(self):
        """Stop the optimization advisor."""
        self.is_active = False
        logger.info("Optimization advisor stopped")
        return self
    
    def get_suggestions(
        self,
        categories: Optional[List[OptimizationCategory]] = None,
        max_suggestions: int = 5,
    ) -> List[Dict[str, Any]]:
        """
        Get optimization suggestions.
        
        Args:
            categories: List of optimization categories to consider
            max_suggestions: Maximum number of suggestions to return
        
        Returns:
            List of optimization suggestions
        """
        if not self.is_active:
            return []
        
        suggestions = []
        
        # Get memory-related suggestions
        if categories is None or OptimizationCategory.MEMORY in categories:
            suggestions.extend(self._get_memory_suggestions())
        
        # Get performance-related suggestions
        if categories is None or OptimizationCategory.PERFORMANCE in categories:
            suggestions.extend(self._get_performance_suggestions())
        
        # Get dataloader-related suggestions
        if categories is None or OptimizationCategory.DATALOADER in categories:
            suggestions.extend(self._get_dataloader_suggestions())
        
        # Get precision-related suggestions
        if categories is None or OptimizationCategory.PRECISION in categories:
            suggestions.extend(self._get_precision_suggestions())
        
        # Get scheduler-related suggestions
        if categories is None or OptimizationCategory.SCHEDULER in categories:
            suggestions.extend(self._get_scheduler_suggestions())
        
        # Get convergence-related suggestions
        if categories is None or OptimizationCategory.CONVERGENCE in categories:
            suggestions.extend(self._get_convergence_suggestions())
        
        # Sort by priority (higher is more important)
        suggestions.sort(key=lambda s: s.get("priority", 0), reverse=True)
        
        # Limit to max_suggestions
        return suggestions[:max_suggestions]
    
    def auto_optimize(
        self,
        categories: Optional[List[OptimizationCategory]] = None,
        max_optimizations: int = 3,
    ) -> List[Dict[str, Any]]:
        """
        Automatically apply optimizations.
        
        Args:
            categories: List of optimization categories to consider
            max_optimizations: Maximum number of optimizations to apply
        
        Returns:
            List of applied optimizations
        """
        if not self.is_active:
            return []
        
        # Get suggestions
        suggestions = self.get_suggestions(categories=categories)
        
        # Filter suggestions based on optimization level
        filtered_suggestions = self._filter_suggestions_by_level(suggestions)
        
        # Limit to max_optimizations
        filtered_suggestions = filtered_suggestions[:max_optimizations]
        
        # Apply optimizations
        applied = []
        for suggestion in filtered_suggestions:
            optimization_type = suggestion.get("type")
            if optimization_type in self.available_optimizations:
                try:
                    result = self.available_optimizations[optimization_type]()
                    if result:
                        applied.append(suggestion)
                        self.applied_optimizations.append(suggestion)
                        logger.info(f"Applied optimization: {optimization_type}")
                except Exception as e:
                    logger.error(f"Failed to apply optimization {optimization_type}: {e}")
        
        return applied
    
    def _filter_suggestions_by_level(
        self, suggestions: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Filter suggestions based on optimization level.
        
        Args:
            suggestions: List of optimization suggestions
        
        Returns:
            Filtered list of suggestions
        """
        if self.optimization_level == OptimizationLevel.NONE:
            return []
        
        filtered = []
        for suggestion in suggestions:
            risk_level = suggestion.get("risk_level", "medium")
            
            if self.optimization_level == OptimizationLevel.CONSERVATIVE:
                # Only low-risk optimizations
                if risk_level == "low":
                    filtered.append(suggestion)
            
            elif self.optimization_level == OptimizationLevel.BALANCED:
                # Low and medium-risk optimizations
                if risk_level in ["low", "medium"]:
                    filtered.append(suggestion)
            
            elif self.optimization_level == OptimizationLevel.AGGRESSIVE:
                # All optimizations
                filtered.append(suggestion)
        
        return filtered
    
    def _get_memory_suggestions(self) -> List[Dict[str, Any]]:
        """
        Get memory-related optimization suggestions.
        
        Returns:
            List of memory-related optimization suggestions
        """
        suggestions = []
        
        # Check if we have the necessary profilers
        if self.memory_profiler is None:
            return suggestions
        
        memory_metrics = self.memory_profiler.get_metrics()
        
        # Check for high memory usage
        if memory_metrics.get("memory_fragmentation", 0.0) > 0.3:
            suggestions.append({
                "type": "memory_defragmentation",
                "category": OptimizationCategory.MEMORY,
                "priority": 80,
                "risk_level": "low",
                "message": "High memory fragmentation detected",
                "details": f"Memory fragmentation: {memory_metrics.get('memory_fragmentation', 0.0):.2f}",
                "code": "torch.cuda.empty_cache()",
                "function": "_optimize_memory_defragmentation",
            })
        
        # Check if gradient checkpointing would help
        if (self.model is not None and 
            memory_metrics.get("max_allocated_memory", 0) > 1000 and  # >1GB
            self.device.type == "cuda"):
            suggestions.append({
                "type": "gradient_checkpointing",
                "category": OptimizationCategory.MEMORY,
                "priority": 70,
                "risk_level": "medium",
                "message": "Consider using gradient checkpointing to reduce memory usage",
                "details": "Gradient checkpointing trades computation for memory by recomputing intermediate activations during the backward pass",
                "code": "model.gradient_checkpointing_enable()",
                "function": "_optimize_gradient_checkpointing",
            })
        
        # Check if optimizer state is using a lot of memory
        if self.optimizer is not None and memory_metrics.get("max_allocated_memory", 0) > 2000:  # >2GB
            suggestions.append({
                "type": "optimizer_memory",
                "category": OptimizationCategory.MEMORY,
                "priority": 60,
                "risk_level": "medium",
                "message": "Consider using memory-efficient optimizer settings",
                "details": "Optimizer states can use significant memory. Consider using optimizer settings that reduce memory usage.",
                "code": "# For Adam optimizer:\noptimizer = torch.optim.Adam(model.parameters(), eps=1e-4)",
                "function": "_optimize_optimizer_memory",
            })
        
        # Check if memory-efficient attention would help for transformer models
        if self.model is not None and self._is_transformer_model(self.model):
            suggestions.append({
                "type": "memory_efficient_attention",
                "category": OptimizationCategory.MEMORY,
                "priority": 65,
                "risk_level": "medium",
                "message": "Consider using memory-efficient attention for transformer models",
                "details": "Memory-efficient attention implementations can significantly reduce memory usage for transformer models",
                "code": "# If using HuggingFace transformers:\nmodel.config.attention_implementation = 'flash_attention_2'",
                "function": "_optimize_memory_efficient_attention",
            })
        
        return suggestions
    
    def _get_performance_suggestions(self) -> List[Dict[str, Any]]:
        """
        Get performance-related optimization suggestions.
        
        Returns:
            List of performance-related optimization suggestions
        """
        suggestions = []
        
        # Check if we have the necessary profilers
        if self.timing_profiler is None:
            return suggestions
        
        timing_metrics = self.timing_profiler.get_metrics()
        
        # Check if channels_last memory format would help
        if (self.model is not None and 
            self._is_cnn_model(self.model) and 
            self.device.type == "cuda"):
            suggestions.append({
                "type": "channels_last",
                "category": OptimizationCategory.PERFORMANCE,
                "priority": 60,
                "risk_level": "low",
                "message": "Consider using channels_last memory format for CNN models",
                "details": "channels_last memory format can improve performance for CNN models on CUDA devices",
                "code": "model = model.to(memory_format=torch.channels_last)",
                "function": "_optimize_channels_last",
            })
        
        # Check if torch.compile would help
        if (self.model is not None and 
            hasattr(torch, 'compile') and 
            timing_metrics.get("forward_time", 0) > 0.01):  # >10ms forward pass
            suggestions.append({
                "type": "compile",
                "category": OptimizationCategory.PERFORMANCE,
                "priority": 75,
                "risk_level": "medium",
                "message": "Consider using torch.compile for performance improvement",
                "details": "torch.compile can significantly improve performance by optimizing the model's computation graph",
                "code": "model = torch.compile(model)",
                "function": "_optimize_compile",
            })
        
        # Check if gradient accumulation would help
        if (self.optimizer is not None and 
            timing_metrics.get("optimizer_time", 0) > 0.05):  # >50ms optimizer step
            suggestions.append({
                "type": "gradient_accumulation",
                "category": OptimizationCategory.PERFORMANCE,
                "priority": 55,
                "risk_level": "medium",
                "message": "Consider using gradient accumulation for better performance",
                "details": "Gradient accumulation can improve performance by reducing the frequency of optimizer steps",
                "code": "# Accumulate gradients over multiple batches\naccumulation_steps = 4\nfor i, batch in enumerate(dataloader):\n    loss = model(batch) / accumulation_steps\n    loss.backward()\n    if (i + 1) % accumulation_steps == 0:\n        optimizer.step()\n        optimizer.zero_grad()",
                "function": "_optimize_gradient_accumulation",
            })
        
        return suggestions
    
    def _get_dataloader_suggestions(self) -> List[Dict[str, Any]]:
        """
        Get dataloader-related optimization suggestions.
        
        Returns:
            List of dataloader-related optimization suggestions
        """
        suggestions = []
        
        # Check if we have the necessary profilers
        if self.dataloader_profiler is None:
            return suggestions
        
        # Get dataloader suggestions from the profiler
        if hasattr(self.dataloader_profiler, "get_optimization_suggestions"):
            profiler_suggestions = self.dataloader_profiler.get_optimization_suggestions()
            
            for suggestion in profiler_suggestions:
                if suggestion["type"] == "dataloader_workers":
                    suggestions.append({
                        "type": "dataloader_workers",
                        "category": OptimizationCategory.DATALOADER,
                        "priority": 70,
                        "risk_level": "low",
                        "message": suggestion["message"],
                        "details": suggestion["details"],
                        "code": suggestion["code"],
                        "function": "_optimize_dataloader_workers",
                        "params": {
                            "num_workers": suggestion.get("num_workers", self.dataloader_profiler.metrics.get("estimated_optimal_workers", 4))
                        }
                    })
                elif suggestion["type"] == "batch_size":
                    suggestions.append({
                        "type": "batch_size",
                        "category": OptimizationCategory.DATALOADER,
                        "priority": 65,
                        "risk_level": "medium",
                        "message": suggestion["message"],
                        "details": suggestion["details"],
                        "code": suggestion["code"],
                        "function": "_optimize_batch_size",
                        "params": {
                            "batch_size": int(suggestion.get("batch_size", self.dataloader_profiler.metrics.get("batch_size", 32) * 2))
                        }
                    })
        
        return suggestions
    
    def _get_precision_suggestions(self) -> List[Dict[str, Any]]:
        """
        Get precision-related optimization suggestions.
        
        Returns:
            List of precision-related optimization suggestions
        """
        suggestions = []
        
        # Check if we have the necessary components
        if self.model is None or self.device is None:
            return suggestions
        
        # Check if AMP would help
        if (self.device.type == "cuda" and 
            torch.cuda.is_available() and 
            hasattr(torch.cuda, 'amp') and
            not self._is_using_amp()):
            suggestions.append({
                "type": "amp",
                "category": OptimizationCategory.PRECISION,
                "priority": 90,
                "risk_level": "low",
                "message": "Consider using Automatic Mixed Precision (AMP) for better performance",
                "details": "AMP can significantly improve performance and reduce memory usage by using FP16 precision where appropriate",
                "code": "# Initialize scaler\nscaler = torch.cuda.amp.GradScaler()\n\n# Training loop\nfor batch in dataloader:\n    optimizer.zero_grad()\n    with torch.cuda.amp.autocast():\n        loss = model(batch)\n    scaler.scale(loss).backward()\n    scaler.step(optimizer)\n    scaler.update()",
                "function": "_optimize_amp",
            })
        
        # Check if bfloat16 would help
        if (self.device.type == "cuda" and 
            torch.cuda.is_available() and 
            torch.cuda.get_device_capability(self.device)[0] >= 8 and  # Ampere or newer
            not self._is_using_bfloat16()):
            suggestions.append({
                "type": "bfloat16",
                "category": OptimizationCategory.PRECISION,
                "priority": 85,
                "risk_level": "low",
                "message": "Consider using bfloat16 precision for better performance",
                "details": "bfloat16 precision can improve performance and reduce memory usage while maintaining numerical stability",
                "code": "# Convert model to bfloat16\nmodel = model.to(torch.bfloat16)\n\n# Training loop\nfor batch in dataloader:\n    batch = {k: v.to(torch.bfloat16) if torch.is_floating_point(v) else v for k, v in batch.items()}\n    loss = model(batch)\n    loss.backward()\n    optimizer.step()",
                "function": "_optimize_bfloat16",
            })
        
        return suggestions
    
    def _get_scheduler_suggestions(self) -> List[Dict[str, Any]]:
        """
        Get scheduler-related optimization suggestions.
        
        Returns:
            List of scheduler-related optimization suggestions
        """
        suggestions = []
        
        # Check if we have the necessary components
        if self.optimizer is None:
            return suggestions
        
        # Check if a learning rate scheduler would help
        if not self._has_lr_scheduler():
            suggestions.append({
                "type": "scheduler",
                "category": OptimizationCategory.SCHEDULER,
                "priority": 60,
                "risk_level": "medium",
                "message": "Consider using a learning rate scheduler",
                "details": "A learning rate scheduler can improve training convergence and final model performance",
                "code": "# OneCycleLR scheduler\nfrom torch.optim.lr_scheduler import OneCycleLR\nscheduler = OneCycleLR(optimizer, max_lr=1e-3, epochs=num_epochs, steps_per_epoch=len(dataloader))",
                "function": "_optimize_scheduler",
            })
        
        return suggestions
    
    def _get_convergence_suggestions(self) -> List[Dict[str, Any]]:
        """
        Get convergence-related optimization suggestions.
        
        Returns:
            List of convergence-related optimization suggestions
        """
        suggestions = []
        
        # Check if we have the necessary components
        if self.failure_forecaster is None:
            return suggestions
        
        # Get warnings from the failure forecaster
        warnings = self.failure_forecaster.get_warnings()
        
        for warning in warnings:
            if warning["type"] == "overfitting":
                suggestions.append({
                    "type": "overfitting_mitigation",
                    "category": OptimizationCategory.CONVERGENCE,
                    "priority": 80,
                    "risk_level": "medium",
                    "message": warning["message"],
                    "details": warning["details"],
                    "code": "# Add regularization\noptimizer = torch.optim.Adam(model.parameters(), weight_decay=1e-4)",
                    "function": "_optimize_overfitting_mitigation",
                })
            elif warning["type"] == "underfitting":
                suggestions.append({
                    "type": "underfitting_mitigation",
                    "category": OptimizationCategory.CONVERGENCE,
                    "priority": 80,
                    "risk_level": "medium",
                    "message": warning["message"],
                    "details": warning["details"],
                    "code": "# Increase model capacity or train longer\n# Consider increasing learning rate",
                    "function": "_optimize_underfitting_mitigation",
                })
            elif warning["type"] == "vanishing_gradients":
                suggestions.append({
                    "type": "vanishing_gradients_mitigation",
                    "category": OptimizationCategory.CONVERGENCE,
                    "priority": 85,
                    "risk_level": "high",
                    "message": warning["message"],
                    "details": warning["details"],
                    "code": "# Use batch normalization\n# Use residual connections\n# Use ReLU or Leaky ReLU activation functions",
                    "function": "_optimize_vanishing_gradients_mitigation",
                })
            elif warning["type"] == "exploding_gradients":
                suggestions.append({
                    "type": "exploding_gradients_mitigation",
                    "category": OptimizationCategory.CONVERGENCE,
                    "priority": 85,
                    "risk_level": "high",
                    "message": warning["message"],
                    "details": warning["details"],
                    "code": "# Use gradient clipping\ntorch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)",
                    "function": "_optimize_exploding_gradients_mitigation",
                })
        
        return suggestions
    
    def _optimize_amp(self) -> bool:
        """
        Optimize using Automatic Mixed Precision (AMP).
        
        Returns:
            True if optimization was applied, False otherwise
        """
        if self.model is None or self.device.type != "cuda" or not torch.cuda.is_available():
            return False
        
        try:
            # Create a wrapper function for the model's forward method
            original_forward = self.model.forward
            
            @functools.wraps(original_forward)
            def amp_forward(*args, **kwargs):
                with torch.cuda.amp.autocast():
                    return original_forward(*args, **kwargs)
            
            self.model.forward = amp_forward
            
            # Create a GradScaler
            self.grad_scaler = torch.cuda.amp.GradScaler()
            
            # Monkey patch the optimizer's step method
            if self.optimizer is not None:
                original_step = self.optimizer.step
                
                @functools.wraps(original_step)
                def scaler_step(*args, **kwargs):
                    self.grad_scaler.step(self.optimizer)
                    self.grad_scaler.update()
                    return None
                
                self.optimizer.step = scaler_step
            
            logger.info("Applied AMP optimization")
            return True
        
        except Exception as e:
            logger.error(f"Failed to apply AMP optimization: {e}")
            return False
    
    def _optimize_bfloat16(self) -> bool:
        """
        Optimize using bfloat16 precision.
        
        Returns:
            True if optimization was applied, False otherwise
        """
        if (self.model is None or 
            self.device.type != "cuda" or 
            not torch.cuda.is_available() or
            torch.cuda.get_device_capability(self.device)[0] < 8):  # Ampere or newer required
            return False
        
        try:
            # Convert model to bfloat16
            self.model = self.model.to(torch.bfloat16)
            
            logger.info("Applied bfloat16 optimization")
            return True
        
        except Exception as e:
            logger.error(f"Failed to apply bfloat16 optimization: {e}")
            return False
    
    def _optimize_dataloader_workers(self) -> bool:
        """
        Optimize dataloader workers.
        
        Returns:
            True if optimization was applied, False otherwise
        """
        if self.dataloader is None or self.dataloader_profiler is None:
            return False
        
        try:
            # Get optimal number of workers
            optimal_workers = self.dataloader_profiler.metrics.get("estimated_optimal_workers", 4)
            
            # Create a new dataloader with optimal workers
            new_dataloader = DataLoader(
                dataset=self.dataloader.dataset,
                batch_size=self.dataloader.batch_size,
                shuffle=getattr(self.dataloader, "shuffle", True),
                num_workers=optimal_workers,
                pin_memory=getattr(self.dataloader, "pin_memory", True),
                drop_last=getattr(self.dataloader, "drop_last", False),
                collate_fn=getattr(self.dataloader, "collate_fn", None),
            )
            
            # Replace the dataloader
            self.dataloader = new_dataloader
            
            logger.info(f"Applied dataloader workers optimization: {optimal_workers} workers")
            return True
        
        except Exception as e:
            logger.error(f"Failed to apply dataloader workers optimization: {e}")
            return False
    
    def _optimize_batch_size(self) -> bool:
        """
        Optimize batch size.
        
        Returns:
            True if optimization was applied, False otherwise
        """
        if self.dataloader is None or self.memory_profiler is None:
            return False
        
        try:
            # Get current batch size
            current_batch_size = self.dataloader.batch_size
            
            # Estimate optimal batch size based on memory usage
            memory_metrics = self.memory_profiler.get_metrics()
            
            # Get total GPU memory
            if self.device.type == "cuda" and torch.cuda.is_available():
                total_memory = torch.cuda.get_device_properties(self.device).total_memory / (1024 * 1024)  # MB
            else:
                # For CPU, use system memory
                import psutil
                total_memory = psutil.virtual_memory().total / (1024 * 1024)  # MB
            
            # Calculate available memory
            available_memory = total_memory - memory_metrics.get("reserved_memory", 0)
            
            # Estimate memory per sample
            memory_per_sample = memory_metrics.get("allocated_memory", 0) / current_batch_size
            
            # Calculate optimal batch size (with 20% safety margin)
            optimal_batch_size = int(available_memory / memory_per_sample * 0.8)
            
            # Ensure batch size is at least 1
            optimal_batch_size = max(1, optimal_batch_size)
            
            # Ensure batch size is not too large (arbitrary limit)
            optimal_batch_size = min(1024, optimal_batch_size)
            
            # If optimal batch size is not significantly different, don't change
            if 0.8 <= optimal_batch_size / current_batch_size <= 1.2:
                return False
            
            # Create a new dataloader with optimal batch size
            new_dataloader = DataLoader(
                dataset=self.dataloader.dataset,
                batch_size=optimal_batch_size,
                shuffle=getattr(self.dataloader, "shuffle", True),
                num_workers=getattr(self.dataloader, "num_workers", 0),
                pin_memory=getattr(self.dataloader, "pin_memory", True),
                drop_last=getattr(self.dataloader, "drop_last", False),
                collate_fn=getattr(self.dataloader, "collate_fn", None),
            )
            
            # Replace the dataloader
            self.dataloader = new_dataloader
            
            logger.info(f"Applied batch size optimization: {current_batch_size} -> {optimal_batch_size}")
            return True
        
        except Exception as e:
            logger.error(f"Failed to apply batch size optimization: {e}")
            return False
    
    def _optimize_gradient_checkpointing(self) -> bool:
        """
        Optimize using gradient checkpointing.
        
        Returns:
            True if optimization was applied, False otherwise
        """
        if self.model is None:
            return False
        
        try:
            # Check if the model has gradient checkpointing
            if hasattr(self.model, "gradient_checkpointing_enable"):
                self.model.gradient_checkpointing_enable()
                logger.info("Applied gradient checkpointing optimization")
                return True
            
            # For HuggingFace models
            if hasattr(self.model, "config") and hasattr(self.model.config, "gradient_checkpointing"):
                self.model.config.gradient_checkpointing = True
                logger.info("Applied gradient checkpointing optimization (HuggingFace)")
                return True
            
            # For custom implementation
            # This is a simplified version and may not work for all models
            for module in self.model.modules():
                if isinstance(module, torch.nn.Sequential):
                    original_forward = module.forward
                    
                    def checkpointed_forward(*args, **kwargs):
                        return torch.utils.checkpoint.checkpoint(original_forward, *args, **kwargs)
                    
                    module.forward = checkpointed_forward
            
            logger.info("Applied gradient checkpointing optimization (custom)")
            return True
        
        except Exception as e:
            logger.error(f"Failed to apply gradient checkpointing optimization: {e}")
            return False
    
    def _optimize_memory_efficient_attention(self) -> bool:
        """
        Optimize using memory-efficient attention.
        
        Returns:
            True if optimization was applied, False otherwise
        """
        if self.model is None:
            return False
        
        try:
            # Check if the model is a HuggingFace transformer
            if hasattr(self.model, "config") and hasattr(self.model.config, "attention_implementation"):
                # Check if flash attention is available
                try:
                    import flash_attn
                    self.model.config.attention_implementation = "flash_attention_2"
                    logger.info("Applied memory-efficient attention optimization (flash_attention_2)")
                    return True
                except ImportError:
                    # Fall back to memory-efficient attention
                    self.model.config.attention_implementation = "sdpa"
                    logger.info("Applied memory-efficient attention optimization (sdpa)")
                    return True
            
            # For PyTorch native transformers
            for module in self.model.modules():
                if isinstance(module, torch.nn.MultiheadAttention):
                    # Enable memory-efficient attention
                    if hasattr(module, "batch_first"):
                        module.batch_first = True
                    if hasattr(module, "_qkv_same_embed_dim"):
                        module._qkv_same_embed_dim = True
            
            logger.info("Applied memory-efficient attention optimization (PyTorch)")
            return True
        
        except Exception as e:
            logger.error(f"Failed to apply memory-efficient attention optimization: {e}")
            return False
    
    def _optimize_optimizer_memory(self) -> bool:
        """
        Optimize optimizer memory usage.
        
        Returns:
            True if optimization was applied, False otherwise
        """
        if self.optimizer is None or self.model is None:
            return False
        
        try:
            # Get optimizer type
            optimizer_type = type(self.optimizer).__name__
            
            if optimizer_type == "Adam" or optimizer_type == "AdamW":
                # Get current parameters
                lr = self.optimizer.param_groups[0]["lr"]
                weight_decay = self.optimizer.param_groups[0].get("weight_decay", 0)
                
                # Create a new optimizer with memory-efficient settings
                if optimizer_type == "Adam":
                    new_optimizer = torch.optim.Adam(
                        self.model.parameters(),
                        lr=lr,
                        weight_decay=weight_decay,
                        eps=1e-4,  # Larger epsilon for better numerical stability and less memory
                    )
                else:  # AdamW
                    new_optimizer = torch.optim.AdamW(
                        self.model.parameters(),
                        lr=lr,
                        weight_decay=weight_decay,
                        eps=1e-4,  # Larger epsilon for better numerical stability and less memory
                    )
                
                # Replace the optimizer
                self.optimizer = new_optimizer
                
                logger.info(f"Applied optimizer memory optimization for {optimizer_type}")
                return True
            
            return False
        
        except Exception as e:
            logger.error(f"Failed to apply optimizer memory optimization: {e}")
            return False
    
    def _optimize_scheduler(self) -> bool:
        """
        Optimize learning rate scheduler.
        
        Returns:
            True if optimization was applied, False otherwise
        """
        if self.optimizer is None or self.dataloader is None:
            return False
        
        try:
            # Check if a scheduler already exists
            if self._has_lr_scheduler():
                return False
            
            # Create a OneCycleLR scheduler
            from torch.optim.lr_scheduler import OneCycleLR
            
            # Get current learning rate
            lr = self.optimizer.param_groups[0]["lr"]
            
            # Estimate number of steps
            steps_per_epoch = len(self.dataloader)
            num_epochs = 10  # Default value, can be adjusted
            
            scheduler = OneCycleLR(
                self.optimizer,
                max_lr=lr * 10,  # 10x current lr as max
                epochs=num_epochs,
                steps_per_epoch=steps_per_epoch,
            )
            
            # Attach scheduler to optimizer
            self.optimizer.scheduler = scheduler
            
            logger.info("Applied learning rate scheduler optimization (OneCycleLR)")
            return True
        
        except Exception as e:
            logger.error(f"Failed to apply scheduler optimization: {e}")
            return False
    
    def _optimize_gradient_accumulation(self) -> bool:
        """
        Optimize using gradient accumulation.
        
        Returns:
            True if optimization was applied, False otherwise
        """
        if self.optimizer is None:
            return False
        
        try:
            # Set gradient accumulation steps
            self.gradient_accumulation_steps = 4
            
            # Monkey patch the optimizer's step method
            original_step = self.optimizer.step
            original_zero_grad = self.optimizer.zero_grad
            
            # Counter for tracking steps
            self.step_counter = 0
            
            @functools.wraps(original_step)
            def accumulation_step(*args, **kwargs):
                self.step_counter += 1
                if self.step_counter % self.gradient_accumulation_steps == 0:
                    result = original_step(*args, **kwargs)
                    original_zero_grad()
                    return result
                return None
            
            @functools.wraps(original_zero_grad)
            def accumulation_zero_grad(*args, **kwargs):
                if self.step_counter % self.gradient_accumulation_steps == 0:
                    return original_zero_grad(*args, **kwargs)
                return None
            
            self.optimizer.step = accumulation_step
            self.optimizer.zero_grad = accumulation_zero_grad
            
            logger.info(f"Applied gradient accumulation optimization: {self.gradient_accumulation_steps} steps")
            return True
        
        except Exception as e:
            logger.error(f"Failed to apply gradient accumulation optimization: {e}")
            return False
    
    def _optimize_channels_last(self) -> bool:
        """
        Optimize using channels_last memory format.
        
        Returns:
            True if optimization was applied, False otherwise
        """
        if self.model is None or self.device.type != "cuda":
            return False
        
        try:
            # Check if the model is a CNN
            if not self._is_cnn_model(self.model):
                return False
            
            # Convert model to channels_last
            self.model = self.model.to(memory_format=torch.channels_last)
            
            logger.info("Applied channels_last memory format optimization")
            return True
        
        except Exception as e:
            logger.error(f"Failed to apply channels_last optimization: {e}")
            return False
    
    def _optimize_compile(self) -> bool:
        """
        Optimize using torch.compile.
        
        Returns:
            True if optimization was applied, False otherwise
        """
        if self.model is None or not hasattr(torch, 'compile'):
            return False
        
        try:
            # Compile the model
            self.model = torch.compile(self.model)
            
            logger.info("Applied torch.compile optimization")
            return True
        
        except Exception as e:
            logger.error(f"Failed to apply torch.compile optimization: {e}")
            return False
    
    def _optimize_memory_defragmentation(self) -> bool:
        """
        Optimize memory by defragmenting.
        
        Returns:
            True if optimization was applied, False otherwise
        """
        if self.device.type != "cuda" or not torch.cuda.is_available():
            return False
        
        try:
            # Empty CUDA cache
            torch.cuda.empty_cache()
            
            logger.info("Applied memory defragmentation optimization")
            return True
        
        except Exception as e:
            logger.error(f"Failed to apply memory defragmentation optimization: {e}")
            return False
    
    def _is_using_amp(self) -> bool:
        """
        Check if AMP is already being used.
        
        Returns:
            True if AMP is being used, False otherwise
        """
        if self.model is None:
            return False
        
        # Check if forward method is wrapped with autocast
        forward_source = inspect.getsource(self.model.forward)
        if "autocast" in forward_source or "amp.autocast" in forward_source:
            return True
        
        # Check if optimizer step is wrapped with scaler
        if self.optimizer is not None:
            step_source = inspect.getsource(self.optimizer.step)
            if "scaler" in step_source or "GradScaler" in step_source:
                return True
        
        return False
    
    def _is_using_bfloat16(self) -> bool:
        """
        Check if bfloat16 precision is already being used.
        
        Returns:
            True if bfloat16 is being used, False otherwise
        """
        if self.model is None:
            return False
        
        # Check if any parameter is bfloat16
        for param in self.model.parameters():
            if param.dtype == torch.bfloat16:
                return True
        
        return False
    
    def _has_lr_scheduler(self) -> bool:
        """
        Check if a learning rate scheduler is already being used.
        
        Returns:
            True if a scheduler is being used, False otherwise
        """
        if self.optimizer is None:
            return False
        
        # Check if optimizer has a scheduler attribute
        if hasattr(self.optimizer, "scheduler"):
            return True
        
        # Check common scheduler attribute names
        for attr in ["scheduler", "lr_scheduler", "_scheduler"]:
            if hasattr(self.optimizer, attr):
                return True
        
        return False
    
    def _is_transformer_model(self, model: torch.nn.Module) -> bool:
        """
        Check if the model is a transformer.
        
        Args:
            model: The model to check
        
        Returns:
            True if the model is a transformer, False otherwise
        """
        # Check for HuggingFace transformers
        if hasattr(model, "config") and hasattr(model.config, "model_type"):
            return True
        
        # Check for PyTorch transformers
        for module in model.modules():
            if isinstance(module, torch.nn.TransformerEncoder) or isinstance(module, torch.nn.TransformerDecoder):
                return True
            if isinstance(module, torch.nn.MultiheadAttention):
                return True
            if "Attention" in module.__class__.__name__:
                return True
        
        return False
    
    def _is_cnn_model(self, model: torch.nn.Module) -> bool:
        """
        Check if the model is a CNN.
        
        Args:
            model: The model to check
        
        Returns:
            True if the model is a CNN, False otherwise
        """
        # Check for convolutional layers
        for module in model.modules():
            if isinstance(module, torch.nn.Conv2d) or isinstance(module, torch.nn.Conv3d):
                return True
        
        return False
    
    def __repr__(self) -> str:
        """String representation of the optimization advisor."""
        status = "active" if self.is_active else "inactive"
        level = self.optimization_level.name.lower()
        return f"OptimizationAdvisor(status={status}, level={level})"
