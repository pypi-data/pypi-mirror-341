"""
DeepSpeed integration module for AutoPipelineDoctor.

This module provides integration with DeepSpeed, allowing AutoPipelineDoctor
to monitor and optimize DeepSpeed-accelerated training.
"""

import logging
import time
import functools
import inspect
import weakref
from typing import Dict, Any, Optional, List, Tuple, Union, Callable, Type

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader

try:
    import deepspeed
    from deepspeed import DeepSpeedEngine
    from deepspeed.runtime.engine import DeepSpeedEngine
    from deepspeed.runtime.config import DeepSpeedConfig
    DEEPSPEED_AVAILABLE = True
except ImportError:
    DEEPSPEED_AVAILABLE = False
    # Create dummy classes for type hints
    class DeepSpeedEngine:
        pass
    class DeepSpeedConfig:
        pass

from autopd.integrations.pytorch_integration import PyTorchIntegration

logger = logging.getLogger(__name__)


class DeepSpeedIntegration:
    """
    Integration with DeepSpeed.
    
    This class provides hooks and patches for DeepSpeed engines to enable
    monitoring and optimization of DeepSpeed-accelerated training.
    
    Attributes:
        doctor: Reference to the Doctor instance
        engine: Reference to the DeepSpeed engine
        integration: PyTorch integration instance
        original_methods: Dictionary of original methods that have been patched
        metrics: Dictionary of collected metrics
    """
    
    def __init__(
        self,
        doctor: Any,
        engine: Optional["DeepSpeedEngine"] = None,
    ):
        """
        Initialize the DeepSpeed integration.
        
        Args:
            doctor: Reference to the Doctor instance
            engine: DeepSpeed engine to monitor
        """
        if not DEEPSPEED_AVAILABLE:
            raise ImportError("DeepSpeed is not installed. Install with: pip install deepspeed")
        
        self.doctor = doctor
        self.engine = engine
        self.integration = None
        
        # Initialize original methods
        self.original_methods = {}
        
        # Initialize metrics
        self.metrics = {
            "step_times": [],
            "forward_times": [],
            "backward_times": [],
            "optimizer_times": [],
            "batch_sizes": [],
            "losses": [],
            "grad_norms": [],
            "learning_rates": [],
        }
        
        # Initialize state
        self.current_step = 0
        self.step_start_time = 0
        self.forward_start_time = 0
        self.backward_start_time = 0
        self.optimizer_start_time = 0
        
        logger.info("DeepSpeed integration initialized")
    
    def register(self, engine: "DeepSpeedEngine"):
        """
        Register a DeepSpeed engine for monitoring.
        
        Args:
            engine: DeepSpeed engine to monitor
        """
        self.engine = engine
        
        # Create PyTorch integration for the model
        if hasattr(engine, "module") and engine.module is not None:
            self.integration = PyTorchIntegration(
                self.doctor,
                model=engine.module,
            )
        
        logger.info("Registered DeepSpeed engine for monitoring")
    
    def attach(self):
        """
        Attach hooks and patches to the registered DeepSpeed engine.
        """
        if not self.engine:
            logger.warning("No DeepSpeed engine registered")
            return
        
        # Attach PyTorch integration hooks
        if self.integration:
            self.integration.attach()
        
        # Patch DeepSpeed methods
        self._patch_forward()
        self._patch_backward()
        self._patch_step()
        
        logger.info("Attached hooks and patches to DeepSpeed engine")
    
    def detach(self):
        """
        Detach hooks and restore original methods.
        """
        # Detach PyTorch integration hooks
        if self.integration:
            self.integration.detach()
        
        # Restore original methods
        for obj, method_name, original_method in self.original_methods.values():
            if hasattr(obj, method_name):
                setattr(obj, method_name, original_method)
        
        self.original_methods = {}
        
        logger.info("Detached hooks and restored original methods")
    
    def _patch_forward(self):
        """
        Patch the DeepSpeed engine's forward method.
        """
        if not self.engine:
            return
        
        # Get the original forward method
        original_forward = self.engine.forward
        
        # Define the patched forward method
        @functools.wraps(original_forward)
        def patched_forward(*args, **kwargs):
            self.forward_start_time = time.time()
            result = original_forward(*args, **kwargs)
            forward_time = time.time() - self.forward_start_time
            
            # Record forward time
            self.metrics["forward_times"].append(forward_time)
            
            # Estimate batch size
            if args and isinstance(args[0], torch.Tensor):
                self.metrics["batch_sizes"].append(args[0].shape[0])
            
            return result
        
        # Replace the forward method
        self.engine.forward = patched_forward
        
        # Store the original method
        self.original_methods["forward"] = (self.engine, "forward", original_forward)
        
        logger.info("Patched DeepSpeed forward method")
    
    def _patch_backward(self):
        """
        Patch the DeepSpeed engine's backward method.
        """
        if not self.engine:
            return
        
        # Get the original backward method
        original_backward = self.engine.backward
        
        # Define the patched backward method
        @functools.wraps(original_backward)
        def patched_backward(*args, **kwargs):
            self.backward_start_time = time.time()
            result = original_backward(*args, **kwargs)
            backward_time = time.time() - self.backward_start_time
            
            # Record backward time
            self.metrics["backward_times"].append(backward_time)
            
            # Record loss if available
            if args and isinstance(args[0], torch.Tensor):
                self.metrics["losses"].append(args[0].item())
            
            return result
        
        # Replace the backward method
        self.engine.backward = patched_backward
        
        # Store the original method
        self.original_methods["backward"] = (self.engine, "backward", original_backward)
        
        logger.info("Patched DeepSpeed backward method")
    
    def _patch_step(self):
        """
        Patch the DeepSpeed engine's step method.
        """
        if not self.engine:
            return
        
        # Get the original step method
        original_step = self.engine.step
        
        # Define the patched step method
        @functools.wraps(original_step)
        def patched_step(*args, **kwargs):
            self.optimizer_start_time = time.time()
            result = original_step(*args, **kwargs)
            optimizer_time = time.time() - self.optimizer_start_time
            
            # Record optimizer time
            self.metrics["optimizer_times"].append(optimizer_time)
            
            # Record step time
            step_time = time.time() - self.step_start_time if self.step_start_time > 0 else 0
            if step_time > 0:
                self.metrics["step_times"].append(step_time)
            
            # Increment step counter
            self.current_step += 1
            
            # Collect metrics every 10 steps
            if self.current_step % 10 == 0:
                self._collect_metrics()
            
            # Reset step timer
            self.step_start_time = time.time()
            
            return result
        
        # Replace the step method
        self.engine.step = patched_step
        
        # Store the original method
        self.original_methods["step"] = (self.engine, "step", original_step)
        
        # Initialize step timer
        self.step_start_time = time.time()
        
        logger.info("Patched DeepSpeed step method")
    
    def _collect_metrics(self):
        """
        Collect metrics and send them to the doctor.
        """
        if not self.doctor:
            return
        
        # Calculate average times
        avg_step_time = sum(self.metrics["step_times"][-10:]) / max(1, len(self.metrics["step_times"][-10:]))
        avg_forward_time = sum(self.metrics["forward_times"][-10:]) / max(1, len(self.metrics["forward_times"][-10:]))
        avg_backward_time = sum(self.metrics["backward_times"][-10:]) / max(1, len(self.metrics["backward_times"][-10:]))
        avg_optimizer_time = sum(self.metrics["optimizer_times"][-10:]) / max(1, len(self.metrics["optimizer_times"][-10:]))
        
        # Calculate iterations per second
        iterations_per_second = 1.0 / avg_step_time if avg_step_time > 0 else 0
        
        # Calculate time breakdown
        total_time = avg_forward_time + avg_backward_time + avg_optimizer_time
        forward_pct = avg_forward_time / total_time if total_time > 0 else 0
        backward_pct = avg_backward_time / total_time if total_time > 0 else 0
        optimizer_pct = avg_optimizer_time / total_time if total_time > 0 else 0
        
        # Calculate average batch size
        avg_batch_size = sum(self.metrics["batch_sizes"][-10:]) / max(1, len(self.metrics["batch_sizes"][-10:]))
        
        # Collect timing metrics
        timing_metrics = {
            "step_time": avg_step_time,
            "forward_time": avg_forward_time,
            "backward_time": avg_backward_time,
            "optimizer_time": avg_optimizer_time,
            "iterations_per_second": iterations_per_second,
            "forward_pct": forward_pct,
            "backward_pct": backward_pct,
            "optimizer_pct": optimizer_pct,
            "batch_size": avg_batch_size,
            "step": self.current_step,
        }
        
        # Send metrics to the doctor
        if hasattr(self.doctor, "timing_profiler") and self.doctor.timing_profiler:
            self.doctor.timing_profiler.update_metrics(timing_metrics)
        
        # Collect DeepSpeed-specific metrics
        deepspeed_metrics = self._collect_deepspeed_metrics()
        
        # Send metrics to the doctor
        if hasattr(self.doctor, "experience_brain") and self.doctor.experience_brain:
            self.doctor.experience_brain.update_metrics(deepspeed_metrics, category="deepspeed")
        
        # Check for performance issues
        self._check_performance_issues(timing_metrics, deepspeed_metrics)
    
    def _collect_deepspeed_metrics(self) -> Dict[str, Any]:
        """
        Collect DeepSpeed-specific metrics.
        
        Returns:
            Dictionary of DeepSpeed metrics
        """
        metrics = {}
        
        if not self.engine:
            return metrics
        
        # Get DeepSpeed configuration
        if hasattr(self.engine, "config"):
            config = self.engine.config
            
            # Add ZeRO stage
            if hasattr(config, "zero_optimization") and config.zero_optimization:
                metrics["zero_stage"] = config.zero_optimization.get("stage", 0)
            
            # Add optimizer configuration
            if hasattr(config, "optimizer"):
                metrics["optimizer_type"] = config.optimizer.get("type", "unknown")
                metrics["learning_rate"] = config.optimizer.get("params", {}).get("lr", 0)
                
                # Add current learning rate
                if hasattr(self.engine, "optimizer") and self.engine.optimizer:
                    for param_group in self.engine.optimizer.param_groups:
                        if "lr" in param_group:
                            metrics["current_learning_rate"] = param_group["lr"]
                            self.metrics["learning_rates"].append(param_group["lr"])
                            break
            
            # Add gradient clipping
            if hasattr(config, "gradient_clipping"):
                metrics["gradient_clipping"] = config.gradient_clipping
            
            # Add precision
            if hasattr(config, "fp16") and config.fp16:
                metrics["precision"] = "fp16"
            elif hasattr(config, "bf16") and config.bf16:
                metrics["precision"] = "bf16"
            else:
                metrics["precision"] = "fp32"
        
        # Get communication stats
        if hasattr(self.engine, "comm_size_history") and self.engine.comm_size_history:
            metrics["avg_communication_size"] = sum(self.engine.comm_size_history) / len(self.engine.comm_size_history)
        
        # Get gradient norm
        if hasattr(self.engine, "get_global_grad_norm"):
            try:
                grad_norm = self.engine.get_global_grad_norm()
                if isinstance(grad_norm, torch.Tensor):
                    grad_norm = grad_norm.item()
                metrics["gradient_norm"] = grad_norm
                self.metrics["grad_norms"].append(grad_norm)
            except:
                pass
        
        # Get loss
        if self.metrics["losses"]:
            metrics["loss"] = self.metrics["losses"][-1]
        
        return metrics
    
    def _check_performance_issues(self, timing_metrics: Dict[str, Any], deepspeed_metrics: Dict[str, Any]):
        """
        Check for performance issues and add warnings if necessary.
        
        Args:
            timing_metrics: Timing metrics
            deepspeed_metrics: DeepSpeed metrics
        """
        if not hasattr(self.doctor, "experience_brain") or not self.doctor.experience_brain:
            return
        
        # Check for slow iterations
        if timing_metrics.get("iterations_per_second", 0) < 1:
            self.doctor.experience_brain.add_warning({
                "type": "slow_training",
                "message": f"Training is very slow ({timing_metrics.get('iterations_per_second', 0):.2f} iterations/second)",
                "details": "Consider using a smaller model, optimizing DeepSpeed configuration, or using more efficient hardware",
                "severity": "high",
            })
        
        # Check for communication bottlenecks
        if deepspeed_metrics.get("avg_communication_size", 0) > 100 * 1024 * 1024:  # 100 MB
            self.doctor.experience_brain.add_warning({
                "type": "communication_bottleneck",
                "message": f"Large communication volume ({deepspeed_metrics.get('avg_communication_size', 0) / (1024 * 1024):.2f} MB)",
                "details": "Consider using a higher ZeRO stage, gradient accumulation, or reducing model size",
                "severity": "medium",
            })
        
        # Check for gradient issues
        if "gradient_norm" in deepspeed_metrics:
            grad_norm = deepspeed_metrics["gradient_norm"]
            
            if grad_norm < 0.001:
                self.doctor.experience_brain.add_warning({
                    "type": "vanishing_gradients",
                    "message": f"Gradients may be vanishing (norm: {grad_norm:.6f})",
                    "details": "Consider using a different activation function, initialization, or learning rate",
                    "severity": "high",
                })
            elif grad_norm > 100:
                self.doctor.experience_brain.add_warning({
                    "type": "exploding_gradients",
                    "message": f"Gradients may be exploding (norm: {grad_norm:.2f})",
                    "details": "Consider using gradient clipping, a smaller learning rate, or a different initialization",
                    "severity": "high",
                })
    
    def watch(self, train_func: Callable) -> Callable:
        """
        Watch a training function.
        
        Args:
            train_func: Training function to watch
        
        Returns:
            Wrapped training function
        """
        @functools.wraps(train_func)
        def wrapped_train_func(*args, **kwargs):
            # Try to find DeepSpeed engine in arguments
            engine = None
            for arg in args:
                if isinstance(arg, DeepSpeedEngine):
                    engine = arg
                    break
            
            if engine is None:
                for _, arg in kwargs.items():
                    if isinstance(arg, DeepSpeedEngine):
                        engine = arg
                        break
            
            # Register engine if found
            if engine:
                self.register(engine)
                self.attach()
            
            try:
                # Run the training function
                result = train_func(*args, **kwargs)
                return result
            finally:
                # Detach hooks and restore original methods
                self.detach()
        
        return wrapped_train_func
    
    @staticmethod
    def patch_engine(engine: "DeepSpeedEngine", doctor: Any) -> "DeepSpeedEngine":
        """
        Patch a DeepSpeed engine to enable monitoring.
        
        Args:
            engine: DeepSpeed engine to patch
            doctor: Reference to the Doctor instance
        
        Returns:
            Patched engine
        """
        if not DEEPSPEED_AVAILABLE:
            raise ImportError("DeepSpeed is not installed. Install with: pip install deepspeed")
        
        # Create integration
        integration = DeepSpeedIntegration(doctor, engine)
        
        # Attach hooks and patches
        integration.attach()
        
        # Store the integration in the engine
        engine._autopd_integration = integration
        
        return engine
    
    @staticmethod
    def initialize_with_monitoring(
        model: nn.Module,
        optimizer: Optional[optim.Optimizer] = None,
        config: Optional[Union[Dict, DeepSpeedConfig]] = None,
        doctor: Optional[Any] = None,
        **kwargs
    ) -> "DeepSpeedEngine":
        """
        Initialize a DeepSpeed engine with monitoring.
        
        Args:
            model: PyTorch model
            optimizer: PyTorch optimizer
            config: DeepSpeed configuration
            doctor: Reference to the Doctor instance
            **kwargs: Additional keyword arguments for DeepSpeed initialization
        
        Returns:
            DeepSpeed engine with monitoring
        """
        if not DEEPSPEED_AVAILABLE:
            raise ImportError("DeepSpeed is not installed. Install with: pip install deepspeed")
        
        # Initialize DeepSpeed engine
        engine = deepspeed.initialize(model=model, optimizer=optimizer, config=config, **kwargs)
        
        # Patch engine if doctor is provided
        if doctor:
            engine = DeepSpeedIntegration.patch_engine(engine, doctor)
        
        return engine


class TorchDynamoIntegration:
    """
    Integration with TorchDynamo and torch.compile.
    
    This class provides hooks and patches for TorchDynamo and torch.compile
    to enable monitoring and optimization of compiled models.
    
    Attributes:
        doctor: Reference to the Doctor instance
        original_compile: Original torch.compile function
    """
    
    def __init__(self, doctor: Any):
        """
        Initialize the TorchDynamo integration.
        
        Args:
            doctor: Reference to the Doctor instance
        """
        self.doctor = doctor
        self.original_compile = None
        
        logger.info("TorchDynamo integration initialized")
    
    def attach(self):
        """
        Attach hooks and patches to TorchDynamo and torch.compile.
        """
        # Patch torch.compile if available
        if hasattr(torch, "compile"):
            self.original_compile = torch.compile
            torch.compile = self._patched_compile
            logger.info("Patched torch.compile")
    
    def detach(self):
        """
        Detach hooks and restore original methods.
        """
        # Restore torch.compile
        if self.original_compile:
            torch.compile = self.original_compile
            self.original_compile = None
            logger.info("Restored original torch.compile")
    
    def _patched_compile(self, model, *args, **kwargs):
        """
        Patched version of torch.compile.
        
        Args:
            model: Model to compile
            *args: Additional positional arguments
            **kwargs: Additional keyword arguments
        
        Returns:
            Compiled model
        """
        # Record compilation start time
        start_time = time.time()
        
        # Call original compile
        compiled_model = self.original_compile(model, *args, **kwargs)
        
        # Record compilation time
        compilation_time = time.time() - start_time
        
        # Add optimization to experience brain
        if hasattr(self.doctor, "experience_brain") and self.doctor.experience_brain:
            self.doctor.experience_brain.add_optimization({
                "type": "torch_compile",
                "message": f"Model compiled with torch.compile",
                "details": f"Compilation time: {compilation_time:.2f}s, Backend: {kwargs.get('backend', 'default')}",
            })
        
        logger.info(f"Model compiled with torch.compile (time: {compilation_time:.2f}s)")
        
        return compiled_model
    
    @staticmethod
    def enable_monitoring(doctor: Any):
        """
        Enable monitoring for TorchDynamo and torch.compile.
        
        Args:
            doctor: Reference to the Doctor instance
        """
        integration = TorchDynamoIntegration(doctor)
        integration.attach()
        
        # Store the integration in the doctor
        doctor._torchdynamo_integration = integration
        
        return integration
