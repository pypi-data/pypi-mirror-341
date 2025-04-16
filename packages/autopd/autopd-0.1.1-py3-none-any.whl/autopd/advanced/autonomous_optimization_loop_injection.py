"""
Autonomous Optimization Loop Injection (AOLI) module for AutoPipelineDoctor.

This advanced module monitors training dynamics and injects performance-enhancing
changes in real time, such as enabling AMP, adjusting gradient accumulation,
turning on mixed precision, and triggering activation checkpointing.
"""

import torch
import torch.nn as nn
import logging
import time
import threading
import weakref
import inspect
from typing import Dict, List, Tuple, Optional, Union, Any, Callable, Set
from enum import Enum
import numpy as np
import warnings
from contextlib import contextmanager
import functools
import gc

logger = logging.getLogger(__name__)


class OptimizationType(Enum):
    """Types of optimizations that can be applied."""
    AMP = "automatic_mixed_precision"
    GRADIENT_ACCUMULATION = "gradient_accumulation"
    MIXED_PRECISION = "mixed_precision"
    ACTIVATION_CHECKPOINTING = "activation_checkpointing"
    CHANNELS_LAST = "channels_last"
    OPTIMIZER_FUSION = "optimizer_fusion"
    MEMORY_EFFICIENT_ATTENTION = "memory_efficient_attention"
    GRADIENT_CHECKPOINTING = "gradient_checkpointing"
    BATCH_SIZE_ADJUSTMENT = "batch_size_adjustment"
    WORKER_ADJUSTMENT = "worker_adjustment"
    CUSTOM = "custom_optimization"


class OptimizationStatus(Enum):
    """Status of an optimization."""
    PENDING = "pending"
    APPLIED = "applied"
    FAILED = "failed"
    REVERTED = "reverted"
    INCOMPATIBLE = "incompatible"


class OptimizationImpact(Enum):
    """Impact level of an optimization."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class OptimizationRisk(Enum):
    """Risk level of an optimization."""
    SAFE = "safe"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class AutonomousOptimizationLoopInjection:
    """
    Autonomous Optimization Loop Injection (AOLI) for real-time training optimization.
    
    This module monitors training dynamics and injects performance-enhancing changes in real time,
    such as enabling AMP, adjusting gradient accumulation, turning on mixed precision, and
    triggering activation checkpointing when memory threshold nears.
    
    Attributes:
        model: The PyTorch model to optimize
        optimizer: The optimizer used for training
        dataloader: The dataloader used for training
        risk_level: Maximum risk level of optimizations to apply
        monitoring_interval: Interval in seconds between monitoring checks
        memory_threshold: Memory usage threshold (0.0-1.0) to trigger optimizations
        performance_threshold: Performance threshold to trigger optimizations
        auto_apply: Whether to automatically apply optimizations
        enable_rollback: Whether to enable rolling back failed optimizations
        optimization_cooldown: Cooldown period in seconds between optimizations
        max_optimizations_per_run: Maximum number of optimizations to apply per run
        custom_optimizations: Custom optimization functions to apply
    """
    
    def __init__(
        self,
        model: Optional[nn.Module] = None,
        optimizer: Optional[torch.optim.Optimizer] = None,
        dataloader: Optional[Any] = None,
        risk_level: str = "medium",
        monitoring_interval: float = 5.0,
        memory_threshold: float = 0.8,
        performance_threshold: float = 0.7,
        auto_apply: bool = True,
        enable_rollback: bool = True,
        optimization_cooldown: float = 30.0,
        max_optimizations_per_run: int = 5,
        custom_optimizations: Optional[List[Callable]] = None,
    ):
        """
        Initialize the AutonomousOptimizationLoopInjection module.
        
        Args:
            model: The PyTorch model to optimize
            optimizer: The optimizer used for training
            dataloader: The dataloader used for training
            risk_level: Maximum risk level of optimizations to apply
            monitoring_interval: Interval in seconds between monitoring checks
            memory_threshold: Memory usage threshold (0.0-1.0) to trigger optimizations
            performance_threshold: Performance threshold to trigger optimizations
            auto_apply: Whether to automatically apply optimizations
            enable_rollback: Whether to enable rolling back failed optimizations
            optimization_cooldown: Cooldown period in seconds between optimizations
            max_optimizations_per_run: Maximum number of optimizations to apply per run
            custom_optimizations: Custom optimization functions to apply
        """
        self.model = model
        self.optimizer = optimizer
        self.dataloader = dataloader
        
        # Convert risk level string to enum
        risk_map = {
            "safe": OptimizationRisk.SAFE,
            "low": OptimizationRisk.LOW,
            "medium": OptimizationRisk.MEDIUM,
            "high": OptimizationRisk.HIGH,
        }
        self.risk_level = risk_map.get(risk_level.lower(), OptimizationRisk.MEDIUM)
        
        self.monitoring_interval = monitoring_interval
        self.memory_threshold = memory_threshold
        self.performance_threshold = performance_threshold
        self.auto_apply = auto_apply
        self.enable_rollback = enable_rollback
        self.optimization_cooldown = optimization_cooldown
        self.max_optimizations_per_run = max_optimizations_per_run
        
        # Initialize monitoring state
        self.monitoring_active = False
        self.monitoring_thread = None
        self.last_check_time = 0
        self.last_optimization_time = 0
        self.optimizations_applied = 0
        
        # Initialize metrics storage
        self.metrics_history = {
            "memory_usage": [],
            "batch_time": [],
            "forward_time": [],
            "backward_time": [],
            "optimizer_time": [],
            "dataloader_time": [],
            "gpu_utilization": [],
            "cpu_utilization": [],
            "throughput": [],
        }
        self.metrics_timestamps = []
        
        # Initialize optimization registry
        self.optimization_registry = self._build_optimization_registry()
        
        # Add custom optimizations
        self.custom_optimizations = custom_optimizations or []
        for opt_func in self.custom_optimizations:
            self._register_custom_optimization(opt_func)
        
        # Track applied optimizations
        self.applied_optimizations = []
        self.failed_optimizations = []
        
        # Original state for rollback
        self.original_state = {}
        
        # Hooks and patches
        self.registered_hooks = []
        self.patched_functions = {}
        
        # Initialize compatibility checker
        self._initialize_compatibility_checker()
        
        logger.info(f"Initialized AutonomousOptimizationLoopInjection with risk_level={risk_level}")
    
    def register(
        self,
        model: Optional[nn.Module] = None,
        optimizer: Optional[torch.optim.Optimizer] = None,
        dataloader: Optional[Any] = None,
    ) -> None:
        """
        Register model, optimizer, and dataloader with the module.
        
        Args:
            model: The PyTorch model to optimize
            optimizer: The optimizer used for training
            dataloader: The dataloader used for training
        """
        if model is not None:
            self.model = model
        
        if optimizer is not None:
            self.optimizer = optimizer
        
        if dataloader is not None:
            self.dataloader = dataloader
        
        # Save original state for potential rollback
        self._save_original_state()
        
        logger.info("Registered model, optimizer, and dataloader with AOLI")
    
    def _save_original_state(self) -> None:
        """Save the original state of the model, optimizer, and dataloader."""
        if self.model is not None:
            # Save model state
            self.original_state["model_state"] = {
                "training": self.model.training,
                "dtype": next(self.model.parameters()).dtype,
                "device": next(self.model.parameters()).device,
                "memory_format": self._get_memory_format(self.model),
            }
        
        if self.optimizer is not None:
            # Save optimizer state (simplified)
            self.original_state["optimizer_type"] = type(self.optimizer).__name__
        
        if self.dataloader is not None:
            # Save dataloader state
            self.original_state["dataloader_state"] = {
                "batch_size": getattr(self.dataloader, "batch_size", None),
                "num_workers": getattr(self.dataloader, "num_workers", None),
                "pin_memory": getattr(self.dataloader, "pin_memory", None),
            }
    
    def _get_memory_format(self, model: nn.Module) -> str:
        """
        Get the memory format of a model.
        
        Args:
            model: PyTorch model
            
        Returns:
            Memory format as string
        """
        try:
            param = next(model.parameters())
            if param.is_contiguous(memory_format=torch.channels_last):
                return "channels_last"
            else:
                return "contiguous"
        except:
            return "unknown"
    
    def start_monitoring(self) -> None:
        """Start the monitoring thread."""
        if self.monitoring_active:
            logger.warning("Monitoring is already active")
            return
        
        self.monitoring_active = True
        self.monitoring_thread = threading.Thread(
            target=self._monitoring_loop,
            daemon=True,
        )
        self.monitoring_thread.start()
        
        logger.info("Started optimization monitoring")
    
    def stop_monitoring(self) -> None:
        """Stop the monitoring thread."""
        if not self.monitoring_active:
            logger.warning("Monitoring is not active")
            return
        
        self.monitoring_active = False
        if self.monitoring_thread:
            self.monitoring_thread.join(timeout=2.0)
            self.monitoring_thread = None
        
        logger.info("Stopped optimization monitoring")
    
    def _monitoring_loop(self) -> None:
        """Main monitoring loop that runs in a separate thread."""
        while self.monitoring_active:
            try:
                current_time = time.time()
                
                # Check if it's time to monitor
                if current_time - self.last_check_time >= self.monitoring_interval:
                    self.last_check_time = current_time
                    
                    # Get current metrics
                    metrics = self._get_current_metrics()
                    
                    # Update metrics history
                    for key, value in metrics.items():
                        if key in self.metrics_history:
                            self.metrics_history[key].append(value)
                    
                    self.metrics_timestamps.append(current_time)
                    
                    # Check if optimizations should be applied
                    if self.auto_apply and self._should_optimize(metrics):
                        # Check cooldown period
                        if current_time - self.last_optimization_time >= self.optimization_cooldown:
                            # Check maximum optimizations
                            if self.optimizations_applied < self.max_optimizations_per_run:
                                self._apply_best_optimization(metrics)
                
                # Sleep to avoid high CPU usage
                time.sleep(min(1.0, self.monitoring_interval / 2))
            
            except Exception as e:
                logger.error(f"Error in monitoring loop: {e}")
                time.sleep(5.0)  # Sleep longer on error
    
    def _get_current_metrics(self) -> Dict[str, float]:
        """
        Get current system and training metrics.
        
        Returns:
            Dictionary of current metrics
        """
        metrics = {}
        
        # Memory usage
        try:
            if torch.cuda.is_available():
                memory_allocated = torch.cuda.memory_allocated()
                memory_reserved = torch.cuda.memory_reserved()
                memory_total = torch.cuda.get_device_properties(0).total_memory
                
                metrics["memory_usage"] = memory_allocated / memory_total
                metrics["memory_reserved"] = memory_reserved / memory_total
            else:
                # CPU fallback
                import psutil
                metrics["memory_usage"] = psutil.virtual_memory().percent / 100.0
        except Exception as e:
            logger.warning(f"Failed to get memory metrics: {e}")
            metrics["memory_usage"] = 0.0
        
        # Placeholder for other metrics that would be collected in a real implementation
        # In practice, these would come from hooks or instrumentation
        metrics["batch_time"] = 0.1
        metrics["forward_time"] = 0.05
        metrics["backward_time"] = 0.04
        metrics["optimizer_time"] = 0.01
        metrics["dataloader_time"] = 0.02
        metrics["gpu_utilization"] = 0.7
        metrics["cpu_utilization"] = 0.3
        metrics["throughput"] = 100.0
        
        return metrics
    
    def _should_optimize(self, metrics: Dict[str, float]) -> bool:
        """
        Determine if optimizations should be applied based on current metrics.
        
        Args:
            metrics: Current system and training metrics
            
        Returns:
            True if optimizations should be applied, False otherwise
        """
        # Check memory threshold
        if metrics.get("memory_usage", 0.0) > self.memory_threshold:
            logger.info(f"Memory usage ({metrics['memory_usage']:.2f}) exceeds threshold ({self.memory_threshold:.2f})")
            return True
        
        # Check performance metrics
        # In a real implementation, this would be more sophisticated
        if len(self.metrics_history["batch_time"]) > 5:
            avg_batch_time = sum(self.metrics_history["batch_time"][-5:]) / 5
            if metrics.get("batch_time", 0.0) > avg_batch_time * 1.2:
                logger.info(f"Batch time ({metrics['batch_time']:.4f}s) significantly higher than average ({avg_batch_time:.4f}s)")
                return True
        
        # Check GPU utilization
        if metrics.get("gpu_utilization", 1.0) < self.performance_threshold:
            logger.info(f"GPU utilization ({metrics['gpu_utilization']:.2f}) below threshold ({self.performance_threshold:.2f})")
            return True
        
        return False
    
    def _build_optimization_registry(self) -> Dict[OptimizationType, Dict[str, Any]]:
        """
        Build the registry of available optimizations.
        
        Returns:
            Dictionary mapping optimization types to their metadata
        """
        registry = {}
        
        # AMP (Automatic Mixed Precision)
        registry[OptimizationType.AMP] = {
            "name": "Automatic Mixed Precision",
            "function": self._apply_amp,
            "rollback_function": self._rollback_amp,
            "check_function": self._check_amp_compatibility,
            "impact": OptimizationImpact.HIGH,
            "risk": OptimizationRisk.LOW,
            "description": "Enables automatic mixed precision training using torch.cuda.amp",
            "requirements": ["cuda", "torch>=1.6.0"],
        }
        
        # Gradient Accumulation
        registry[OptimizationType.GRADIENT_ACCUMULATION] = {
            "name": "Gradient Accumulation",
            "function": self._apply_gradient_accumulation,
            "rollback_function": self._rollback_gradient_accumulation,
            "check_function": self._check_gradient_accumulation_compatibility,
            "impact": OptimizationImpact.MEDIUM,
            "risk": OptimizationRisk.LOW,
            "description": "Accumulates gradients over multiple batches before updating weights",
            "requirements": [],
        }
        
        # Mixed Precision (manual)
        registry[OptimizationType.MIXED_PRECISION] = {
            "name": "Mixed Precision",
            "function": self._apply_mixed_precision,
            "rollback_function": self._rollback_mixed_precision,
            "check_function": self._check_mixed_precision_compatibility,
            "impact": OptimizationImpact.HIGH,
            "risk": OptimizationRisk.MEDIUM,
            "description": "Converts model to use float16 precision where appropriate",
            "requirements": ["cuda"],
        }
        
        # Activation Checkpointing
        registry[OptimizationType.ACTIVATION_CHECKPOINTING] = {
            "name": "Activation Checkpointing",
            "function": self._apply_activation_checkpointing,
            "rollback_function": self._rollback_activation_checkpointing,
            "check_function": self._check_activation_checkpointing_compatibility,
            "impact": OptimizationImpact.HIGH,
            "risk": OptimizationRisk.MEDIUM,
            "description": "Trades compute for memory by recomputing activations during backward pass",
            "requirements": [],
        }
        
        # Channels Last Memory Format
        registry[OptimizationType.CHANNELS_LAST] = {
            "name": "Channels Last Memory Format",
            "function": self._apply_channels_last,
            "rollback_function": self._rollback_channels_last,
            "check_function": self._check_channels_last_compatibility,
            "impact": OptimizationImpact.MEDIUM,
            "risk": OptimizationRisk.LOW,
            "description": "Converts model to channels-last memory format for better performance on CNN models",
            "requirements": ["cuda", "torch>=1.5.0"],
        }
        
        # Optimizer Fusion
        registry[OptimizationType.OPTIMIZER_FUSION] = {
            "name": "Optimizer Fusion",
            "function": self._apply_optimizer_fusion,
            "rollback_function": self._rollback_optimizer_fusion,
            "check_function": self._check_optimizer_fusion_compatibility,
            "impact": OptimizationImpact.MEDIUM,
            "risk": OptimizationRisk.MEDIUM,
            "description": "Fuses optimizer operations for better performance",
            "requirements": ["cuda", "torch>=1.12.0"],
        }
        
        # Memory-Efficient Attention
        registry[OptimizationType.MEMORY_EFFICIENT_ATTENTION] = {
            "name": "Memory-Efficient Attention",
            "function": self._apply_memory_efficient_attention,
            "rollback_function": self._rollback_memory_efficient_attention,
            "check_function": self._check_memory_efficient_attention_compatibility,
            "impact": OptimizationImpact.HIGH,
            "risk": OptimizationRisk.MEDIUM,
            "description": "Uses memory-efficient attention implementation for transformer models",
            "requirements": ["cuda", "torch>=1.12.0"],
        }
        
        # Gradient Checkpointing
        registry[OptimizationType.GRADIENT_CHECKPOINTING] = {
            "name": "Gradient Checkpointing",
            "function": self._apply_gradient_checkpointing,
            "rollback_function": self._rollback_gradient_checkpointing,
            "check_function": self._check_gradient_checkpointing_compatibility,
            "impact": OptimizationImpact.HIGH,
            "risk": OptimizationRisk.LOW,
            "description": "Enables gradient checkpointing to save memory at the cost of computation",
            "requirements": [],
        }
        
        # Batch Size Adjustment
        registry[OptimizationType.BATCH_SIZE_ADJUSTMENT] = {
            "name": "Batch Size Adjustment",
            "function": self._apply_batch_size_adjustment,
            "rollback_function": self._rollback_batch_size_adjustment,
            "check_function": self._check_batch_size_adjustment_compatibility,
            "impact": OptimizationImpact.HIGH,
            "risk": OptimizationRisk.HIGH,
            "description": "Dynamically adjusts batch size based on available memory",
            "requirements": [],
        }
        
        # Worker Adjustment
        registry[OptimizationType.WORKER_ADJUSTMENT] = {
            "name": "Worker Adjustment",
            "function": self._apply_worker_adjustment,
            "rollback_function": self._rollback_worker_adjustment,
            "check_function": self._check_worker_adjustment_compatibility,
            "impact": OptimizationImpact.MEDIUM,
            "risk": OptimizationRisk.LOW,
            "description": "Adjusts number of dataloader workers for optimal performance",
            "requirements": [],
        }
        
        return registry
    
    def _register_custom_optimization(self, opt_func: Callable) -> None:
        """
        Register a custom optimization function.
        
        Args:
            opt_func: Custom optimization function
        """
        # Extract function metadata from docstring or annotations
        func_name = opt_func.__name__
        func_doc = opt_func.__doc__ or ""
        
        # Create a unique ID for this optimization
        opt_id = f"custom_{func_name}"
        
        # Register the optimization
        self.optimization_registry[OptimizationType.CUSTOM] = {
            "name": f"Custom: {func_name}",
            "function": opt_func,
            "rollback_function": getattr(opt_func, "rollback", None),
            "check_function": getattr(opt_func, "check_compatibility", lambda: True),
            "impact": getattr(opt_func, "impact", OptimizationImpact.MEDIUM),
            "risk": getattr(opt_func, "risk", OptimizationRisk.MEDIUM),
            "description": func_doc.strip().split("\n")[0] if func_doc else "Custom optimization",
            "requirements": getattr(opt_func, "requirements", []),
            "custom_id": opt_id,
        }
        
        logger.info(f"Registered custom optimization: {func_name}")
    
    def _initialize_compatibility_checker(self) -> None:
        """Initialize the compatibility checker for optimizations."""
        self.compatibility_cache = {}
        
        # Check torch version
        try:
            self.torch_version = torch.__version__
            major, minor = map(int, self.torch_version.split(".")[:2])
            self.torch_version_tuple = (major, minor)
        except:
            self.torch_version = "unknown"
            self.torch_version_tuple = (0, 0)
        
        # Check CUDA availability
        self.cuda_available = torch.cuda.is_available()
        
        # Check for specific modules
        self.has_apex = False
        try:
            import apex
            self.has_apex = True
        except ImportError:
            pass
        
        # Check for transformers
        self.has_transformers = False
        try:
            import transformers
            self.has_transformers = True
        except ImportError:
            pass
    
    def _apply_best_optimization(self, metrics: Dict[str, float]) -> Optional[Dict[str, Any]]:
        """
        Apply the best optimization based on current metrics.
        
        Args:
            metrics: Current system and training metrics
            
        Returns:
            Dictionary with optimization result or None if no optimization was applied
        """
        # Get compatible optimizations
        compatible_optimizations = self._get_compatible_optimizations()
        
        if not compatible_optimizations:
            logger.info("No compatible optimizations available")
            return None
        
        # Filter by risk level
        risk_filtered = [
            opt for opt in compatible_optimizations
            if self.optimization_registry[opt]["risk"].value <= self.risk_level.value
        ]
        
        if not risk_filtered:
            logger.info(f"No optimizations within risk level {self.risk_level.name}")
            return None
        
        # Select best optimization based on metrics
        best_opt = self._select_best_optimization(risk_filtered, metrics)
        
        if best_opt is None:
            logger.info("No suitable optimization found")
            return None
        
        # Apply the optimization
        result = self._apply_optimization(best_opt)
        
        if result["status"] == OptimizationStatus.APPLIED:
            self.last_optimization_time = time.time()
            self.optimizations_applied += 1
            self.applied_optimizations.append(result)
            
            logger.info(f"Applied optimization: {result['name']}")
            return result
        else:
            self.failed_optimizations.append(result)
            logger.warning(f"Failed to apply optimization: {result['name']}")
            return None
    
    def _get_compatible_optimizations(self) -> List[OptimizationType]:
        """
        Get list of compatible optimizations.
        
        Returns:
            List of compatible optimization types
        """
        compatible = []
        
        for opt_type, opt_info in self.optimization_registry.items():
            # Skip if already applied
            if any(applied["type"] == opt_type for applied in self.applied_optimizations):
                continue
            
            # Check compatibility
            check_func = opt_info["check_function"]
            if check_func is not None:
                try:
                    is_compatible = check_func()
                    self.compatibility_cache[opt_type] = is_compatible
                    
                    if is_compatible:
                        compatible.append(opt_type)
                except Exception as e:
                    logger.warning(f"Error checking compatibility for {opt_type.value}: {e}")
            else:
                # If no check function, assume compatible
                compatible.append(opt_type)
        
        return compatible
    
    def _select_best_optimization(
        self, 
        optimizations: List[OptimizationType],
        metrics: Dict[str, float]
    ) -> Optional[OptimizationType]:
        """
        Select the best optimization based on current metrics.
        
        Args:
            optimizations: List of compatible optimization types
            metrics: Current system and training metrics
            
        Returns:
            Best optimization type or None if no suitable optimization found
        """
        if not optimizations:
            return None
        
        # Prioritize based on current metrics
        memory_pressure = metrics.get("memory_usage", 0.0) > self.memory_threshold
        performance_issue = metrics.get("gpu_utilization", 1.0) < self.performance_threshold
        
        # Score each optimization
        scores = {}
        
        for opt_type in optimizations:
            opt_info = self.optimization_registry[opt_type]
            impact = opt_info["impact"]
            risk = opt_info["risk"]
            
            # Base score from impact
            if impact == OptimizationImpact.LOW:
                base_score = 1
            elif impact == OptimizationImpact.MEDIUM:
                base_score = 2
            elif impact == OptimizationImpact.HIGH:
                base_score = 3
            else:  # CRITICAL
                base_score = 4
            
            # Adjust score based on risk
            if risk == OptimizationRisk.HIGH:
                risk_factor = 0.5
            elif risk == OptimizationRisk.MEDIUM:
                risk_factor = 0.75
            elif risk == OptimizationRisk.LOW:
                risk_factor = 0.9
            else:  # SAFE
                risk_factor = 1.0
            
            # Adjust score based on current issues
            issue_factor = 1.0
            
            # Memory-saving optimizations get priority when memory pressure is high
            if memory_pressure and opt_type in [
                OptimizationType.ACTIVATION_CHECKPOINTING,
                OptimizationType.GRADIENT_CHECKPOINTING,
                OptimizationType.MEMORY_EFFICIENT_ATTENTION,
                OptimizationType.MIXED_PRECISION,
                OptimizationType.AMP,
            ]:
                issue_factor = 1.5
            
            # Performance optimizations get priority when performance is low
            if performance_issue and opt_type in [
                OptimizationType.CHANNELS_LAST,
                OptimizationType.OPTIMIZER_FUSION,
                OptimizationType.WORKER_ADJUSTMENT,
            ]:
                issue_factor = 1.5
            
            # Calculate final score
            scores[opt_type] = base_score * risk_factor * issue_factor
        
        # Select optimization with highest score
        if not scores:
            return None
        
        return max(scores.items(), key=lambda x: x[1])[0]
    
    def _apply_optimization(self, opt_type: OptimizationType) -> Dict[str, Any]:
        """
        Apply a specific optimization.
        
        Args:
            opt_type: Type of optimization to apply
            
        Returns:
            Dictionary with optimization result
        """
        opt_info = self.optimization_registry[opt_type]
        opt_func = opt_info["function"]
        
        result = {
            "type": opt_type,
            "name": opt_info["name"],
            "timestamp": time.time(),
            "description": opt_info["description"],
            "impact": opt_info["impact"],
            "risk": opt_info["risk"],
        }
        
        try:
            # Apply the optimization
            opt_result = opt_func()
            
            if opt_result is True:
                result["status"] = OptimizationStatus.APPLIED
                result["details"] = "Optimization applied successfully"
            else:
                result["status"] = OptimizationStatus.FAILED
                result["details"] = str(opt_result) if opt_result else "Optimization failed"
        except Exception as e:
            result["status"] = OptimizationStatus.FAILED
            result["details"] = str(e)
            logger.error(f"Error applying optimization {opt_type.value}: {e}")
        
        return result
    
    def apply_optimization(self, opt_type: Union[str, OptimizationType]) -> Dict[str, Any]:
        """
        Manually apply a specific optimization.
        
        Args:
            opt_type: Type of optimization to apply
            
        Returns:
            Dictionary with optimization result
        """
        # Convert string to enum if needed
        if isinstance(opt_type, str):
            try:
                opt_type = OptimizationType(opt_type)
            except ValueError:
                return {
                    "status": OptimizationStatus.FAILED,
                    "details": f"Unknown optimization type: {opt_type}"
                }
        
        # Check if optimization exists
        if opt_type not in self.optimization_registry:
            return {
                "status": OptimizationStatus.FAILED,
                "details": f"Optimization not registered: {opt_type.value}"
            }
        
        # Check compatibility
        opt_info = self.optimization_registry[opt_type]
        check_func = opt_info["check_function"]
        
        if check_func is not None:
            try:
                is_compatible = check_func()
                if not is_compatible:
                    return {
                        "type": opt_type,
                        "name": opt_info["name"],
                        "status": OptimizationStatus.INCOMPATIBLE,
                        "details": "Optimization is not compatible with current setup"
                    }
            except Exception as e:
                return {
                    "type": opt_type,
                    "name": opt_info["name"],
                    "status": OptimizationStatus.FAILED,
                    "details": f"Error checking compatibility: {e}"
                }
        
        # Apply the optimization
        result = self._apply_optimization(opt_type)
        
        if result["status"] == OptimizationStatus.APPLIED:
            self.last_optimization_time = time.time()
            self.optimizations_applied += 1
            self.applied_optimizations.append(result)
        else:
            self.failed_optimizations.append(result)
        
        return result
    
    def rollback_optimization(self, opt_type: Union[str, OptimizationType]) -> Dict[str, Any]:
        """
        Rollback a specific optimization.
        
        Args:
            opt_type: Type of optimization to rollback
            
        Returns:
            Dictionary with rollback result
        """
        # Convert string to enum if needed
        if isinstance(opt_type, str):
            try:
                opt_type = OptimizationType(opt_type)
            except ValueError:
                return {
                    "status": OptimizationStatus.FAILED,
                    "details": f"Unknown optimization type: {opt_type}"
                }
        
        # Check if optimization exists
        if opt_type not in self.optimization_registry:
            return {
                "status": OptimizationStatus.FAILED,
                "details": f"Optimization not registered: {opt_type.value}"
            }
        
        # Check if optimization was applied
        applied_opt = None
        for opt in self.applied_optimizations:
            if opt["type"] == opt_type:
                applied_opt = opt
                break
        
        if applied_opt is None:
            return {
                "status": OptimizationStatus.FAILED,
                "details": f"Optimization was not applied: {opt_type.value}"
            }
        
        # Get rollback function
        opt_info = self.optimization_registry[opt_type]
        rollback_func = opt_info["rollback_function"]
        
        if rollback_func is None:
            return {
                "status": OptimizationStatus.FAILED,
                "details": f"No rollback function available for: {opt_type.value}"
            }
        
        # Apply rollback
        result = {
            "type": opt_type,
            "name": opt_info["name"],
            "timestamp": time.time(),
            "original_timestamp": applied_opt["timestamp"],
        }
        
        try:
            # Apply the rollback
            rollback_result = rollback_func()
            
            if rollback_result is True:
                result["status"] = OptimizationStatus.REVERTED
                result["details"] = "Optimization rolled back successfully"
                
                # Remove from applied optimizations
                self.applied_optimizations.remove(applied_opt)
            else:
                result["status"] = OptimizationStatus.FAILED
                result["details"] = str(rollback_result) if rollback_result else "Rollback failed"
        except Exception as e:
            result["status"] = OptimizationStatus.FAILED
            result["details"] = str(e)
            logger.error(f"Error rolling back optimization {opt_type.value}: {e}")
        
        return result
    
    def rollback_all(self) -> List[Dict[str, Any]]:
        """
        Rollback all applied optimizations.
        
        Returns:
            List of rollback results
        """
        results = []
        
        # Rollback in reverse order of application
        for opt in reversed(self.applied_optimizations[:]):
            opt_type = opt["type"]
            result = self.rollback_optimization(opt_type)
            results.append(result)
        
        return results
    
    def get_applied_optimizations(self) -> List[Dict[str, Any]]:
        """
        Get list of applied optimizations.
        
        Returns:
            List of applied optimizations
        """
        return self.applied_optimizations
    
    def get_failed_optimizations(self) -> List[Dict[str, Any]]:
        """
        Get list of failed optimizations.
        
        Returns:
            List of failed optimizations
        """
        return self.failed_optimizations
    
    def get_available_optimizations(self) -> List[Dict[str, Any]]:
        """
        Get list of available optimizations.
        
        Returns:
            List of available optimizations with metadata
        """
        optimizations = []
        
        for opt_type, opt_info in self.optimization_registry.items():
            # Check compatibility
            is_compatible = self.compatibility_cache.get(opt_type)
            if is_compatible is None:
                check_func = opt_info["check_function"]
                if check_func is not None:
                    try:
                        is_compatible = check_func()
                        self.compatibility_cache[opt_type] = is_compatible
                    except:
                        is_compatible = False
                else:
                    is_compatible = True
            
            # Check if already applied
            is_applied = any(applied["type"] == opt_type for applied in self.applied_optimizations)
            
            optimizations.append({
                "type": opt_type,
                "name": opt_info["name"],
                "description": opt_info["description"],
                "impact": opt_info["impact"],
                "risk": opt_info["risk"],
                "compatible": is_compatible,
                "applied": is_applied,
                "requirements": opt_info["requirements"],
            })
        
        return optimizations
    
    def get_metrics_history(self) -> Dict[str, List[float]]:
        """
        Get metrics history.
        
        Returns:
            Dictionary of metrics history
        """
        return {
            "metrics": self.metrics_history,
            "timestamps": self.metrics_timestamps,
        }
    
    def reset(self) -> None:
        """Reset the module state."""
        # Stop monitoring
        if self.monitoring_active:
            self.stop_monitoring()
        
        # Rollback all optimizations
        self.rollback_all()
        
        # Reset metrics history
        self.metrics_history = {key: [] for key in self.metrics_history}
        self.metrics_timestamps = []
        
        # Reset optimization state
        self.last_check_time = 0
        self.last_optimization_time = 0
        self.optimizations_applied = 0
        self.applied_optimizations = []
        self.failed_optimizations = []
        
        # Reset compatibility cache
        self.compatibility_cache = {}
        
        logger.info("Reset AutonomousOptimizationLoopInjection state")
    
    def attach_to_training_loop(self, training_loop: Callable) -> Callable:
        """
        Attach optimization monitoring to a training loop.
        
        Args:
            training_loop: Training loop function
            
        Returns:
            Wrapped training loop function
        """
        @functools.wraps(training_loop)
        def wrapped_training_loop(*args, **kwargs):
            # Start monitoring
            self.start_monitoring()
            
            try:
                # Run the original training loop
                result = training_loop(*args, **kwargs)
                return result
            finally:
                # Stop monitoring
                self.stop_monitoring()
        
        return wrapped_training_loop
    
    def inject_into_loop(self, loop_type: str = "standard") -> None:
        """
        Inject optimization hooks into a training loop.
        
        Args:
            loop_type: Type of training loop ("standard", "lightning", "huggingface", "custom")
        """
        if loop_type == "standard":
            self._inject_into_standard_loop()
        elif loop_type == "lightning":
            self._inject_into_lightning_loop()
        elif loop_type == "huggingface":
            self._inject_into_huggingface_loop()
        else:
            logger.warning(f"Unknown loop type: {loop_type}")
    
    def _inject_into_standard_loop(self) -> None:
        """Inject optimization hooks into a standard PyTorch training loop."""
        if self.model is None:
            logger.warning("No model registered, cannot inject hooks")
            return
        
        # Patch forward method
        original_forward = self.model.forward
        
        @functools.wraps(original_forward)
        def patched_forward(*args, **kwargs):
            # Check if optimizations should be applied
            metrics = self._get_current_metrics()
            if self.auto_apply and self._should_optimize(metrics):
                # Apply optimization if cooldown period has passed
                current_time = time.time()
                if current_time - self.last_optimization_time >= self.optimization_cooldown:
                    if self.optimizations_applied < self.max_optimizations_per_run:
                        self._apply_best_optimization(metrics)
            
            # Call original forward
            return original_forward(*args, **kwargs)
        
        # Apply patch
        self.model.forward = patched_forward
        self.patched_functions["model_forward"] = original_forward
        
        # Register hooks
        if hasattr(self.model, "register_forward_hook"):
            hook = self.model.register_forward_hook(self._forward_hook)
            self.registered_hooks.append(hook)
        
        if hasattr(self.model, "register_backward_hook"):
            hook = self.model.register_backward_hook(self._backward_hook)
            self.registered_hooks.append(hook)
        
        logger.info("Injected hooks into standard PyTorch training loop")
    
    def _inject_into_lightning_loop(self) -> None:
        """Inject optimization hooks into a PyTorch Lightning training loop."""
        try:
            import pytorch_lightning as pl
            
            # Create a callback
            class AOLICallback(pl.Callback):
                def __init__(self, aoli):
                    self.aoli = aoli
                
                def on_train_batch_start(self, trainer, pl_module, batch, batch_idx):
                    # Check if optimizations should be applied
                    metrics = self.aoli._get_current_metrics()
                    if self.aoli.auto_apply and self.aoli._should_optimize(metrics):
                        # Apply optimization if cooldown period has passed
                        current_time = time.time()
                        if current_time - self.aoli.last_optimization_time >= self.aoli.optimization_cooldown:
                            if self.aoli.optimizations_applied < self.aoli.max_optimizations_per_run:
                                self.aoli._apply_best_optimization(metrics)
                
                def on_train_start(self, trainer, pl_module):
                    # Start monitoring
                    self.aoli.start_monitoring()
                
                def on_train_end(self, trainer, pl_module):
                    # Stop monitoring
                    self.aoli.stop_monitoring()
            
            # Store the callback class
            self.lightning_callback = AOLICallback
            
            logger.info("Created PyTorch Lightning callback for optimization injection")
        except ImportError:
            logger.warning("PyTorch Lightning not available, cannot inject hooks")
    
    def _inject_into_huggingface_loop(self) -> None:
        """Inject optimization hooks into a HuggingFace Transformers training loop."""
        try:
            import transformers
            
            # Create a callback
            class AOLICallback(transformers.TrainerCallback):
                def __init__(self, aoli):
                    self.aoli = aoli
                
                def on_step_begin(self, args, state, control, **kwargs):
                    # Check if optimizations should be applied
                    metrics = self.aoli._get_current_metrics()
                    if self.aoli.auto_apply and self.aoli._should_optimize(metrics):
                        # Apply optimization if cooldown period has passed
                        current_time = time.time()
                        if current_time - self.aoli.last_optimization_time >= self.aoli.optimization_cooldown:
                            if self.aoli.optimizations_applied < self.aoli.max_optimizations_per_run:
                                self.aoli._apply_best_optimization(metrics)
                
                def on_train_begin(self, args, state, control, **kwargs):
                    # Start monitoring
                    self.aoli.start_monitoring()
                
                def on_train_end(self, args, state, control, **kwargs):
                    # Stop monitoring
                    self.aoli.stop_monitoring()
            
            # Store the callback class
            self.huggingface_callback = AOLICallback
            
            logger.info("Created HuggingFace Transformers callback for optimization injection")
        except ImportError:
            logger.warning("HuggingFace Transformers not available, cannot inject hooks")
    
    def _forward_hook(self, module, input, output):
        """Hook for model forward pass."""
        # Update metrics
        pass
    
    def _backward_hook(self, module, grad_input, grad_output):
        """Hook for model backward pass."""
        # Update metrics
        pass
    
    def remove_hooks(self) -> None:
        """Remove all registered hooks."""
        # Remove hooks
        for hook in self.registered_hooks:
            hook.remove()
        
        self.registered_hooks = []
        
        # Restore patched functions
        for name, original_func in self.patched_functions.items():
            if name == "model_forward" and self.model is not None:
                self.model.forward = original_func
        
        self.patched_functions = {}
        
        logger.info("Removed all hooks and restored original functions")
    
    # Implementation of specific optimizations
    
    def _check_amp_compatibility(self) -> bool:
        """Check if AMP is compatible with current setup."""
        return (
            self.cuda_available and
            self.torch_version_tuple >= (1, 6) and
            self.model is not None and
            self.optimizer is not None
        )
    
    def _apply_amp(self) -> Union[bool, str]:
        """Apply Automatic Mixed Precision (AMP)."""
        if not self._check_amp_compatibility():
            return "AMP not compatible with current setup"
        
        try:
            from torch.cuda.amp import autocast, GradScaler
            
            # Check if already using AMP
            if hasattr(self, "amp_enabled") and self.amp_enabled:
                return "AMP already enabled"
            
            # Create GradScaler
            self.grad_scaler = GradScaler()
            
            # Patch optimizer step
            original_step = self.optimizer.step
            
            @functools.wraps(original_step)
            def patched_step(*args, **kwargs):
                return self.grad_scaler.step(self.optimizer, *args, **kwargs)
            
            self.optimizer.step = patched_step
            self.patched_functions["optimizer_step"] = original_step
            
            # Patch model forward
            original_forward = self.model.forward
            
            @functools.wraps(original_forward)
            def patched_forward(*args, **kwargs):
                with autocast():
                    return original_forward(*args, **kwargs)
            
            self.model.forward = patched_forward
            self.patched_functions["model_forward_amp"] = original_forward
            
            # Patch backward
            if hasattr(self, "loss"):
                original_backward = self.loss.backward
                
                @functools.wraps(original_backward)
                def patched_backward(*args, **kwargs):
                    self.grad_scaler.scale(self.loss).backward(*args, **kwargs)
                
                self.loss.backward = patched_backward
                self.patched_functions["loss_backward"] = original_backward
            
            self.amp_enabled = True
            return True
        except Exception as e:
            logger.error(f"Error applying AMP: {e}")
            return str(e)
    
    def _rollback_amp(self) -> Union[bool, str]:
        """Rollback Automatic Mixed Precision (AMP)."""
        if not hasattr(self, "amp_enabled") or not self.amp_enabled:
            return "AMP not enabled"
        
        try:
            # Restore optimizer step
            if "optimizer_step" in self.patched_functions and self.optimizer is not None:
                self.optimizer.step = self.patched_functions["optimizer_step"]
                del self.patched_functions["optimizer_step"]
            
            # Restore model forward
            if "model_forward_amp" in self.patched_functions and self.model is not None:
                self.model.forward = self.patched_functions["model_forward_amp"]
                del self.patched_functions["model_forward_amp"]
            
            # Restore backward
            if "loss_backward" in self.patched_functions and hasattr(self, "loss"):
                self.loss.backward = self.patched_functions["loss_backward"]
                del self.patched_functions["loss_backward"]
            
            # Remove GradScaler
            if hasattr(self, "grad_scaler"):
                del self.grad_scaler
            
            self.amp_enabled = False
            return True
        except Exception as e:
            logger.error(f"Error rolling back AMP: {e}")
            return str(e)
    
    def _check_gradient_accumulation_compatibility(self) -> bool:
        """Check if gradient accumulation is compatible with current setup."""
        return self.optimizer is not None
    
    def _apply_gradient_accumulation(self, accumulation_steps: int = 4) -> Union[bool, str]:
        """Apply gradient accumulation."""
        if not self._check_gradient_accumulation_compatibility():
            return "Gradient accumulation not compatible with current setup"
        
        try:
            # Check if already using gradient accumulation
            if hasattr(self, "grad_accum_enabled") and self.grad_accum_enabled:
                return "Gradient accumulation already enabled"
            
            # Store accumulation steps
            self.accumulation_steps = accumulation_steps
            self.current_step = 0
            
            # Patch optimizer step
            original_step = self.optimizer.step
            original_zero_grad = self.optimizer.zero_grad
            
            @functools.wraps(original_step)
            def patched_step(*args, **kwargs):
                self.current_step += 1
                if self.current_step % self.accumulation_steps == 0:
                    result = original_step(*args, **kwargs)
                    return result
                return None
            
            @functools.wraps(original_zero_grad)
            def patched_zero_grad(*args, **kwargs):
                if self.current_step % self.accumulation_steps == 0:
                    result = original_zero_grad(*args, **kwargs)
                    return result
                return None
            
            self.optimizer.step = patched_step
            self.optimizer.zero_grad = patched_zero_grad
            self.patched_functions["optimizer_step_accum"] = original_step
            self.patched_functions["optimizer_zero_grad"] = original_zero_grad
            
            self.grad_accum_enabled = True
            return True
        except Exception as e:
            logger.error(f"Error applying gradient accumulation: {e}")
            return str(e)
    
    def _rollback_gradient_accumulation(self) -> Union[bool, str]:
        """Rollback gradient accumulation."""
        if not hasattr(self, "grad_accum_enabled") or not self.grad_accum_enabled:
            return "Gradient accumulation not enabled"
        
        try:
            # Restore optimizer step
            if "optimizer_step_accum" in self.patched_functions and self.optimizer is not None:
                self.optimizer.step = self.patched_functions["optimizer_step_accum"]
                del self.patched_functions["optimizer_step_accum"]
            
            # Restore optimizer zero_grad
            if "optimizer_zero_grad" in self.patched_functions and self.optimizer is not None:
                self.optimizer.zero_grad = self.patched_functions["optimizer_zero_grad"]
                del self.patched_functions["optimizer_zero_grad"]
            
            # Remove accumulation state
            if hasattr(self, "accumulation_steps"):
                del self.accumulation_steps
            
            if hasattr(self, "current_step"):
                del self.current_step
            
            self.grad_accum_enabled = False
            return True
        except Exception as e:
            logger.error(f"Error rolling back gradient accumulation: {e}")
            return str(e)
    
    def _check_mixed_precision_compatibility(self) -> bool:
        """Check if mixed precision is compatible with current setup."""
        return (
            self.cuda_available and
            self.model is not None
        )
    
    def _apply_mixed_precision(self) -> Union[bool, str]:
        """Apply mixed precision (manual implementation)."""
        if not self._check_mixed_precision_compatibility():
            return "Mixed precision not compatible with current setup"
        
        try:
            # Check if already using mixed precision
            if hasattr(self, "mixed_precision_enabled") and self.mixed_precision_enabled:
                return "Mixed precision already enabled"
            
            # Store original dtype
            self.original_dtype = next(self.model.parameters()).dtype
            
            # Convert model to half precision
            self.model.half()
            
            self.mixed_precision_enabled = True
            return True
        except Exception as e:
            logger.error(f"Error applying mixed precision: {e}")
            return str(e)
    
    def _rollback_mixed_precision(self) -> Union[bool, str]:
        """Rollback mixed precision."""
        if not hasattr(self, "mixed_precision_enabled") or not self.mixed_precision_enabled:
            return "Mixed precision not enabled"
        
        try:
            # Restore original dtype
            if hasattr(self, "original_dtype") and self.model is not None:
                self.model.to(self.original_dtype)
                del self.original_dtype
            
            self.mixed_precision_enabled = False
            return True
        except Exception as e:
            logger.error(f"Error rolling back mixed precision: {e}")
            return str(e)
    
    def _check_activation_checkpointing_compatibility(self) -> bool:
        """Check if activation checkpointing is compatible with current setup."""
        if self.model is None:
            return False
        
        # Check if model has modules that support checkpointing
        has_supported_modules = False
        
        for module in self.model.modules():
            if isinstance(module, (nn.Sequential, nn.TransformerEncoderLayer, nn.TransformerDecoderLayer)):
                has_supported_modules = True
                break
        
        return has_supported_modules
    
    def _apply_activation_checkpointing(self) -> Union[bool, str]:
        """Apply activation checkpointing."""
        if not self._check_activation_checkpointing_compatibility():
            return "Activation checkpointing not compatible with current setup"
        
        try:
            # Check if already using activation checkpointing
            if hasattr(self, "activation_checkpointing_enabled") and self.activation_checkpointing_enabled:
                return "Activation checkpointing already enabled"
            
            # Import checkpoint function
            from torch.utils.checkpoint import checkpoint
            
            # Find modules to apply checkpointing
            checkpointed_modules = []
            
            for name, module in self.model.named_children():
                if isinstance(module, (nn.Sequential, nn.TransformerEncoderLayer, nn.TransformerDecoderLayer)):
                    # Store original forward
                    original_forward = module.forward
                    
                    # Create checkpointed forward
                    @functools.wraps(original_forward)
                    def make_checkpointed_forward(original_forward):
                        def checkpointed_forward(*args, **kwargs):
                            return checkpoint(original_forward, *args, **kwargs)
                        return checkpointed_forward
                    
                    # Apply patch
                    module.forward = make_checkpointed_forward(original_forward)
                    
                    # Store for rollback
                    checkpointed_modules.append((module, original_forward))
            
            # Store checkpointed modules
            self.checkpointed_modules = checkpointed_modules
            
            if not checkpointed_modules:
                return "No suitable modules found for activation checkpointing"
            
            self.activation_checkpointing_enabled = True
            return True
        except Exception as e:
            logger.error(f"Error applying activation checkpointing: {e}")
            return str(e)
    
    def _rollback_activation_checkpointing(self) -> Union[bool, str]:
        """Rollback activation checkpointing."""
        if not hasattr(self, "activation_checkpointing_enabled") or not self.activation_checkpointing_enabled:
            return "Activation checkpointing not enabled"
        
        try:
            # Restore original forward methods
            if hasattr(self, "checkpointed_modules"):
                for module, original_forward in self.checkpointed_modules:
                    module.forward = original_forward
                
                del self.checkpointed_modules
            
            self.activation_checkpointing_enabled = False
            return True
        except Exception as e:
            logger.error(f"Error rolling back activation checkpointing: {e}")
            return str(e)
    
    def _check_channels_last_compatibility(self) -> bool:
        """Check if channels last memory format is compatible with current setup."""
        return (
            self.cuda_available and
            self.torch_version_tuple >= (1, 5) and
            self.model is not None
        )
    
    def _apply_channels_last(self) -> Union[bool, str]:
        """Apply channels last memory format."""
        if not self._check_channels_last_compatibility():
            return "Channels last memory format not compatible with current setup"
        
        try:
            # Check if already using channels last
            if hasattr(self, "channels_last_enabled") and self.channels_last_enabled:
                return "Channels last memory format already enabled"
            
            # Convert model to channels last
            self.model = self.model.to(memory_format=torch.channels_last)
            
            self.channels_last_enabled = True
            return True
        except Exception as e:
            logger.error(f"Error applying channels last memory format: {e}")
            return str(e)
    
    def _rollback_channels_last(self) -> Union[bool, str]:
        """Rollback channels last memory format."""
        if not hasattr(self, "channels_last_enabled") or not self.channels_last_enabled:
            return "Channels last memory format not enabled"
        
        try:
            # Convert model back to contiguous
            if self.model is not None:
                self.model = self.model.to(memory_format=torch.contiguous_format)
            
            self.channels_last_enabled = False
            return True
        except Exception as e:
            logger.error(f"Error rolling back channels last memory format: {e}")
            return str(e)
    
    # Placeholder implementations for other optimizations
    
    def _check_optimizer_fusion_compatibility(self) -> bool:
        return False  # Not implemented
    
    def _apply_optimizer_fusion(self) -> Union[bool, str]:
        return "Optimizer fusion not implemented"
    
    def _rollback_optimizer_fusion(self) -> Union[bool, str]:
        return "Optimizer fusion not implemented"
    
    def _check_memory_efficient_attention_compatibility(self) -> bool:
        return False  # Not implemented
    
    def _apply_memory_efficient_attention(self) -> Union[bool, str]:
        return "Memory-efficient attention not implemented"
    
    def _rollback_memory_efficient_attention(self) -> Union[bool, str]:
        return "Memory-efficient attention not implemented"
    
    def _check_gradient_checkpointing_compatibility(self) -> bool:
        return self.model is not None
    
    def _apply_gradient_checkpointing(self) -> Union[bool, str]:
        """Apply gradient checkpointing."""
        if not self._check_gradient_checkpointing_compatibility():
            return "Gradient checkpointing not compatible with current setup"
        
        try:
            # Check if model has a enable_gradient_checkpointing method (common in HF models)
            if hasattr(self.model, "gradient_checkpointing_enable"):
                self.model.gradient_checkpointing_enable()
                self.gradient_checkpointing_enabled = True
                return True
            
            # Fall back to activation checkpointing
            return self._apply_activation_checkpointing()
        except Exception as e:
            logger.error(f"Error applying gradient checkpointing: {e}")
            return str(e)
    
    def _rollback_gradient_checkpointing(self) -> Union[bool, str]:
        """Rollback gradient checkpointing."""
        if not hasattr(self, "gradient_checkpointing_enabled") or not self.gradient_checkpointing_enabled:
            return "Gradient checkpointing not enabled"
        
        try:
            # Check if model has a disable_gradient_checkpointing method
            if hasattr(self.model, "gradient_checkpointing_disable"):
                self.model.gradient_checkpointing_disable()
                self.gradient_checkpointing_enabled = False
                return True
            
            # Fall back to rolling back activation checkpointing
            return self._rollback_activation_checkpointing()
        except Exception as e:
            logger.error(f"Error rolling back gradient checkpointing: {e}")
            return str(e)
    
    def _check_batch_size_adjustment_compatibility(self) -> bool:
        return self.dataloader is not None
    
    def _apply_batch_size_adjustment(self) -> Union[bool, str]:
        """Apply batch size adjustment."""
        if not self._check_batch_size_adjustment_compatibility():
            return "Batch size adjustment not compatible with current setup"
        
        try:
            # Check if already adjusted
            if hasattr(self, "batch_size_adjusted") and self.batch_size_adjusted:
                return "Batch size already adjusted"
            
            # Get current batch size
            current_batch_size = getattr(self.dataloader, "batch_size", None)
            if current_batch_size is None:
                return "Could not determine current batch size"
            
            # Store original batch size
            self.original_batch_size = current_batch_size
            
            # Calculate new batch size based on memory usage
            metrics = self._get_current_metrics()
            memory_usage = metrics.get("memory_usage", 0.0)
            
            if memory_usage > 0.9:
                # High memory usage, reduce batch size significantly
                new_batch_size = max(1, current_batch_size // 2)
            elif memory_usage > 0.8:
                # Moderate memory usage, reduce batch size slightly
                new_batch_size = max(1, current_batch_size * 3 // 4)
            else:
                # Low memory usage, no need to adjust
                return "Memory usage not high enough to warrant batch size adjustment"
            
            # Create new dataloader with adjusted batch size
            # This is a simplified implementation - in practice, you would need to
            # recreate the dataloader with the same parameters except batch_size
            
            # For now, just log the recommendation
            logger.info(f"Recommend reducing batch size from {current_batch_size} to {new_batch_size}")
            
            self.batch_size_adjusted = True
            return f"Recommended batch size adjustment from {current_batch_size} to {new_batch_size}"
        except Exception as e:
            logger.error(f"Error applying batch size adjustment: {e}")
            return str(e)
    
    def _rollback_batch_size_adjustment(self) -> Union[bool, str]:
        """Rollback batch size adjustment."""
        if not hasattr(self, "batch_size_adjusted") or not self.batch_size_adjusted:
            return "Batch size not adjusted"
        
        try:
            # Log recommendation to restore original batch size
            if hasattr(self, "original_batch_size"):
                logger.info(f"Recommend restoring original batch size: {self.original_batch_size}")
                del self.original_batch_size
            
            self.batch_size_adjusted = False
            return True
        except Exception as e:
            logger.error(f"Error rolling back batch size adjustment: {e}")
            return str(e)
    
    def _check_worker_adjustment_compatibility(self) -> bool:
        return self.dataloader is not None and hasattr(self.dataloader, "num_workers")
    
    def _apply_worker_adjustment(self) -> Union[bool, str]:
        """Apply worker adjustment."""
        if not self._check_worker_adjustment_compatibility():
            return "Worker adjustment not compatible with current setup"
        
        try:
            # Check if already adjusted
            if hasattr(self, "worker_adjusted") and self.worker_adjusted:
                return "Workers already adjusted"
            
            # Get current number of workers
            current_workers = getattr(self.dataloader, "num_workers", 0)
            
            # Store original number of workers
            self.original_workers = current_workers
            
            # Calculate optimal number of workers
            import multiprocessing
            cpu_count = multiprocessing.cpu_count()
            
            # Get metrics
            metrics = self._get_current_metrics()
            dataloader_time = metrics.get("dataloader_time", 0.0)
            batch_time = metrics.get("batch_time", 0.0)
            
            # Calculate dataloader bottleneck ratio
            if batch_time > 0:
                bottleneck_ratio = dataloader_time / batch_time
            else:
                bottleneck_ratio = 0.0
            
            if bottleneck_ratio > 0.3:
                # Dataloader is a bottleneck, increase workers
                new_workers = min(cpu_count, current_workers + 2)
            elif bottleneck_ratio < 0.1 and current_workers > 2:
                # Dataloader is very fast, decrease workers
                new_workers = max(1, current_workers - 1)
            else:
                # No adjustment needed
                return "No worker adjustment needed"
            
            # Log recommendation
            logger.info(f"Recommend adjusting workers from {current_workers} to {new_workers}")
            
            self.worker_adjusted = True
            return f"Recommended worker adjustment from {current_workers} to {new_workers}"
        except Exception as e:
            logger.error(f"Error applying worker adjustment: {e}")
            return str(e)
    
    def _rollback_worker_adjustment(self) -> Union[bool, str]:
        """Rollback worker adjustment."""
        if not hasattr(self, "worker_adjusted") or not self.worker_adjusted:
            return "Workers not adjusted"
        
        try:
            # Log recommendation to restore original workers
            if hasattr(self, "original_workers"):
                logger.info(f"Recommend restoring original workers: {self.original_workers}")
                del self.original_workers
            
            self.worker_adjusted = False
            return True
        except Exception as e:
            logger.error(f"Error rolling back worker adjustment: {e}")
            return str(e)
