"""
PyTorch integration module for AutoPipelineDoctor.

This module provides integration with PyTorch, allowing AutoPipelineDoctor
to monitor and optimize PyTorch models and training loops.
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

logger = logging.getLogger(__name__)


class PyTorchIntegration:
    """
    Integration with PyTorch.
    
    This class provides hooks and patches for PyTorch models, optimizers,
    and dataloaders to enable monitoring and optimization.
    
    Attributes:
        doctor: Reference to the Doctor instance
        model: Reference to the PyTorch model
        optimizer: Reference to the PyTorch optimizer
        dataloader: Reference to the PyTorch dataloader
        hooks: Dictionary of registered hooks
        original_methods: Dictionary of original methods that have been patched
    """
    
    def __init__(
        self,
        doctor: Any,
        model: Optional[nn.Module] = None,
        optimizer: Optional[optim.Optimizer] = None,
        dataloader: Optional[DataLoader] = None,
    ):
        """
        Initialize the PyTorch integration.
        
        Args:
            doctor: Reference to the Doctor instance
            model: PyTorch model to monitor
            optimizer: PyTorch optimizer to monitor
            dataloader: PyTorch dataloader to monitor
        """
        self.doctor = doctor
        self.model = model
        self.optimizer = optimizer
        self.dataloader = dataloader
        
        # Initialize hooks
        self.hooks = {}
        
        # Initialize original methods
        self.original_methods = {}
        
        # Initialize metrics
        self.metrics = {
            "forward_times": [],
            "backward_times": [],
            "optimizer_times": [],
            "dataloader_times": [],
            "batch_sizes": [],
            "iteration_times": [],
        }
        
        # Initialize state
        self.current_batch = None
        self.current_batch_size = 0
        self.current_iteration = 0
        self.last_forward_time = 0
        self.last_backward_time = 0
        self.last_optimizer_time = 0
        self.last_dataloader_time = 0
        self.last_iteration_time = 0
        
        logger.info("PyTorch integration initialized")
    
    def register(
        self,
        model: Optional[nn.Module] = None,
        optimizer: Optional[optim.Optimizer] = None,
        dataloader: Optional[DataLoader] = None,
    ):
        """
        Register PyTorch components for monitoring.
        
        Args:
            model: PyTorch model to monitor
            optimizer: PyTorch optimizer to monitor
            dataloader: PyTorch dataloader to monitor
        """
        if model is not None:
            self.model = model
        
        if optimizer is not None:
            self.optimizer = optimizer
        
        if dataloader is not None:
            self.dataloader = dataloader
        
        logger.info("Registered PyTorch components for monitoring")
    
    def attach(self):
        """
        Attach hooks and patches to the registered PyTorch components.
        """
        if self.model:
            self._attach_model_hooks()
        
        if self.optimizer:
            self._patch_optimizer()
        
        if self.dataloader:
            self._patch_dataloader()
        
        logger.info("Attached hooks and patches to PyTorch components")
    
    def detach(self):
        """
        Detach hooks and restore original methods.
        """
        # Remove hooks
        for hook_handle in self.hooks.values():
            hook_handle.remove()
        
        self.hooks = {}
        
        # Restore original methods
        for obj, method_name, original_method in self.original_methods.values():
            if hasattr(obj, method_name):
                setattr(obj, method_name, original_method)
        
        self.original_methods = {}
        
        logger.info("Detached hooks and restored original methods")
    
    def _attach_model_hooks(self):
        """
        Attach hooks to the model.
        """
        # Register forward pre-hook
        forward_pre_hook = self.model.register_forward_pre_hook(self._forward_pre_hook)
        self.hooks["forward_pre"] = forward_pre_hook
        
        # Register forward hook
        forward_hook = self.model.register_forward_hook(self._forward_hook)
        self.hooks["forward"] = forward_hook
        
        # Register backward hook for all parameters
        for name, param in self.model.named_parameters():
            if param.requires_grad:
                backward_hook = param.register_hook(
                    functools.partial(self._backward_hook, name=name)
                )
                self.hooks[f"backward_{name}"] = backward_hook
        
        logger.info("Attached hooks to model")
    
    def _patch_optimizer(self):
        """
        Patch the optimizer's step method.
        """
        if not self.optimizer:
            return
        
        # Get the original step method
        original_step = self.optimizer.step
        
        # Define the patched step method
        @functools.wraps(original_step)
        def patched_step(*args, **kwargs):
            start_time = time.time()
            result = original_step(*args, **kwargs)
            end_time = time.time()
            
            # Record optimizer time
            optimizer_time = end_time - start_time
            self.last_optimizer_time = optimizer_time
            self.metrics["optimizer_times"].append(optimizer_time)
            
            # Update iteration time
            self.last_iteration_time = time.time() - self.last_iteration_time
            self.metrics["iteration_times"].append(self.last_iteration_time)
            
            # Collect metrics
            self._collect_metrics()
            
            # Increment iteration counter
            self.current_iteration += 1
            
            # Reset iteration timer
            self.last_iteration_time = time.time()
            
            return result
        
        # Replace the step method
        self.optimizer.step = patched_step
        
        # Store the original method
        self.original_methods["optimizer_step"] = (self.optimizer, "step", original_step)
        
        logger.info("Patched optimizer step method")
    
    def _patch_dataloader(self):
        """
        Patch the dataloader's __iter__ method.
        """
        if not self.dataloader:
            return
        
        # Get the original __iter__ method
        original_iter = self.dataloader.__iter__
        
        # Define the patched __iter__ method
        @functools.wraps(original_iter)
        def patched_iter(*args, **kwargs):
            iterator = original_iter(*args, **kwargs)
            
            # Get the original __next__ method
            original_next = iterator.__next__
            
            # Define the patched __next__ method
            @functools.wraps(original_next)
            def patched_next(*args, **kwargs):
                start_time = time.time()
                batch = original_next(*args, **kwargs)
                end_time = time.time()
                
                # Record dataloader time
                dataloader_time = end_time - start_time
                self.last_dataloader_time = dataloader_time
                self.metrics["dataloader_times"].append(dataloader_time)
                
                # Store the current batch
                self.current_batch = batch
                
                # Estimate batch size
                if isinstance(batch, (list, tuple)) and len(batch) > 0:
                    if isinstance(batch[0], torch.Tensor):
                        self.current_batch_size = batch[0].shape[0]
                    elif isinstance(batch[0], (list, tuple)) and len(batch[0]) > 0:
                        if isinstance(batch[0][0], torch.Tensor):
                            self.current_batch_size = batch[0][0].shape[0]
                elif isinstance(batch, dict) and len(batch) > 0:
                    first_key = next(iter(batch))
                    if isinstance(batch[first_key], torch.Tensor):
                        self.current_batch_size = batch[first_key].shape[0]
                elif isinstance(batch, torch.Tensor):
                    self.current_batch_size = batch.shape[0]
                
                self.metrics["batch_sizes"].append(self.current_batch_size)
                
                return batch
            
            # Replace the __next__ method
            iterator.__next__ = patched_next
            
            return iterator
        
        # Replace the __iter__ method
        self.dataloader.__iter__ = patched_iter
        
        # Store the original method
        self.original_methods["dataloader_iter"] = (self.dataloader, "__iter__", original_iter)
        
        logger.info("Patched dataloader __iter__ method")
    
    def _forward_pre_hook(self, module, input):
        """
        Hook called before the forward pass.
        
        Args:
            module: Module being executed
            input: Input to the module
        """
        # Record the start time
        self.last_forward_time = time.time()
    
    def _forward_hook(self, module, input, output):
        """
        Hook called after the forward pass.
        
        Args:
            module: Module being executed
            input: Input to the module
            output: Output of the module
        """
        # Calculate forward time
        forward_time = time.time() - self.last_forward_time
        self.metrics["forward_times"].append(forward_time)
    
    def _backward_hook(self, grad, name):
        """
        Hook called during the backward pass.
        
        Args:
            grad: Gradient
            name: Parameter name
        """
        # Record the backward time on the first parameter
        if name == next(iter(dict(self.model.named_parameters()))):
            self.last_backward_time = time.time()
        
        # Calculate backward time on the last parameter
        if name == list(dict(self.model.named_parameters()).keys())[-1]:
            backward_time = time.time() - self.last_backward_time
            self.metrics["backward_times"].append(backward_time)
        
        return grad
    
    def _collect_metrics(self):
        """
        Collect metrics and send them to the doctor.
        """
        if not self.doctor:
            return
        
        # Calculate average times
        avg_forward_time = sum(self.metrics["forward_times"][-10:]) / max(1, len(self.metrics["forward_times"][-10:]))
        avg_backward_time = sum(self.metrics["backward_times"][-10:]) / max(1, len(self.metrics["backward_times"][-10:]))
        avg_optimizer_time = sum(self.metrics["optimizer_times"][-10:]) / max(1, len(self.metrics["optimizer_times"][-10:]))
        avg_dataloader_time = sum(self.metrics["dataloader_times"][-10:]) / max(1, len(self.metrics["dataloader_times"][-10:]))
        avg_iteration_time = sum(self.metrics["iteration_times"][-10:]) / max(1, len(self.metrics["iteration_times"][-10:]))
        avg_batch_size = sum(self.metrics["batch_sizes"][-10:]) / max(1, len(self.metrics["batch_sizes"][-10:]))
        
        # Calculate iterations per second
        iterations_per_second = 1.0 / avg_iteration_time if avg_iteration_time > 0 else 0
        
        # Calculate time breakdown
        total_time = avg_forward_time + avg_backward_time + avg_optimizer_time + avg_dataloader_time
        forward_pct = avg_forward_time / total_time if total_time > 0 else 0
        backward_pct = avg_backward_time / total_time if total_time > 0 else 0
        optimizer_pct = avg_optimizer_time / total_time if total_time > 0 else 0
        dataloader_pct = avg_dataloader_time / total_time if total_time > 0 else 0
        
        # Collect timing metrics
        timing_metrics = {
            "forward_time": avg_forward_time,
            "backward_time": avg_backward_time,
            "optimizer_time": avg_optimizer_time,
            "dataloader_time": avg_dataloader_time,
            "iteration_time": avg_iteration_time,
            "iterations_per_second": iterations_per_second,
            "forward_pct": forward_pct,
            "backward_pct": backward_pct,
            "optimizer_pct": optimizer_pct,
            "dataloader_pct": dataloader_pct,
            "batch_size": avg_batch_size,
            "iteration": self.current_iteration,
        }
        
        # Send metrics to the doctor
        if hasattr(self.doctor, "timing_profiler") and self.doctor.timing_profiler:
            self.doctor.timing_profiler.update_metrics(timing_metrics)
        
        # Collect model metrics
        if self.model:
            model_metrics = self._collect_model_metrics()
            
            # Send metrics to the doctor
            if hasattr(self.doctor, "memory_profiler") and self.doctor.memory_profiler:
                self.doctor.memory_profiler.update_metrics(model_metrics)
        
        # Collect gradient metrics
        if self.model:
            gradient_metrics = self._collect_gradient_metrics()
            
            # Send metrics to the doctor
            if hasattr(self.doctor, "gradient_profiler") and self.doctor.gradient_profiler:
                self.doctor.gradient_profiler.update_metrics(gradient_metrics)
        
        # Collect dataloader metrics
        if self.dataloader:
            dataloader_metrics = self._collect_dataloader_metrics()
            
            # Send metrics to the doctor
            if hasattr(self.doctor, "dataloader_profiler") and self.doctor.dataloader_profiler:
                self.doctor.dataloader_profiler.update_metrics(dataloader_metrics)
    
    def _collect_model_metrics(self) -> Dict[str, Any]:
        """
        Collect metrics about the model.
        
        Returns:
            Dictionary of model metrics
        """
        metrics = {}
        
        # Count parameters
        total_params = sum(p.numel() for p in self.model.parameters())
        trainable_params = sum(p.numel() for p in self.model.parameters() if p.requires_grad)
        
        metrics["total_parameters"] = total_params
        metrics["trainable_parameters"] = trainable_params
        metrics["non_trainable_parameters"] = total_params - trainable_params
        
        # Estimate model size
        model_size_bytes = sum(p.numel() * p.element_size() for p in self.model.parameters())
        metrics["model_size_mb"] = model_size_bytes / (1024 * 1024)
        
        # Check if using CUDA
        if next(self.model.parameters(), None) is not None:
            metrics["device"] = str(next(self.model.parameters()).device)
            metrics["dtype"] = str(next(self.model.parameters()).dtype)
            
            # Check if using CUDA
            if metrics["device"].startswith("cuda"):
                # Get CUDA memory usage
                if torch.cuda.is_available():
                    device_idx = int(metrics["device"].split(":")[-1]) if ":" in metrics["device"] else 0
                    
                    metrics["allocated_memory"] = torch.cuda.memory_allocated(device_idx) / (1024 * 1024)
                    metrics["reserved_memory"] = torch.cuda.memory_reserved(device_idx) / (1024 * 1024)
                    metrics["max_memory"] = torch.cuda.max_memory_allocated(device_idx) / (1024 * 1024)
                    
                    # Calculate memory fragmentation
                    if metrics["reserved_memory"] > 0:
                        metrics["memory_fragmentation"] = 1.0 - (metrics["allocated_memory"] / metrics["reserved_memory"])
                    else:
                        metrics["memory_fragmentation"] = 0.0
                    
                    # Get total GPU memory
                    metrics["total_memory"] = torch.cuda.get_device_properties(device_idx).total_memory / (1024 * 1024)
        
        return metrics
    
    def _collect_gradient_metrics(self) -> Dict[str, Any]:
        """
        Collect metrics about gradients.
        
        Returns:
            Dictionary of gradient metrics
        """
        metrics = {}
        
        # Collect gradient statistics
        grad_norms = []
        grad_means = []
        grad_stds = []
        grad_zeros = 0
        grad_total = 0
        
        for name, param in self.model.named_parameters():
            if param.grad is not None:
                # Calculate gradient norm
                grad_norm = param.grad.norm().item()
                grad_norms.append(grad_norm)
                
                # Calculate gradient mean and std
                grad_mean = param.grad.mean().item()
                grad_std = param.grad.std().item()
                
                grad_means.append(grad_mean)
                grad_stds.append(grad_std)
                
                # Count zero gradients
                grad_zeros += (param.grad == 0).sum().item()
                grad_total += param.grad.numel()
        
        if grad_norms:
            metrics["min_grad_norm"] = min(grad_norms)
            metrics["max_grad_norm"] = max(grad_norms)
            metrics["avg_grad_norm"] = sum(grad_norms) / len(grad_norms)
        
        if grad_means:
            metrics["min_grad_mean"] = min(grad_means)
            metrics["max_grad_mean"] = max(grad_means)
            metrics["avg_grad_mean"] = sum(grad_means) / len(grad_means)
        
        if grad_stds:
            metrics["min_grad_std"] = min(grad_stds)
            metrics["max_grad_std"] = max(grad_stds)
            metrics["avg_grad_std"] = sum(grad_stds) / len(grad_stds)
        
        if grad_total > 0:
            metrics["zero_gradients_pct"] = (grad_zeros / grad_total) * 100
        
        return metrics
    
    def _collect_dataloader_metrics(self) -> Dict[str, Any]:
        """
        Collect metrics about the dataloader.
        
        Returns:
            Dictionary of dataloader metrics
        """
        metrics = {}
        
        # Get dataloader properties
        metrics["batch_size"] = self.dataloader.batch_size
        metrics["num_workers"] = self.dataloader.num_workers
        metrics["pin_memory"] = self.dataloader.pin_memory if hasattr(self.dataloader, "pin_memory") else False
        
        # Calculate dataloader efficiency
        if hasattr(self.dataloader, "num_workers") and self.dataloader.num_workers > 0:
            # Estimate worker utilization
            worker_utilization = min(1.0, self.last_dataloader_time / (self.last_iteration_time - self.last_dataloader_time))
            metrics["worker_utilization"] = worker_utilization
            
            # Estimate optimal number of workers
            if worker_utilization > 0.9:
                # Workers are fully utilized, might need more
                metrics["estimated_optimal_workers"] = self.dataloader.num_workers * 1.5
            elif worker_utilization < 0.5:
                # Workers are underutilized
                metrics["estimated_optimal_workers"] = max(1, int(self.dataloader.num_workers * 0.5))
            else:
                # Workers are well utilized
                metrics["estimated_optimal_workers"] = self.dataloader.num_workers
        
        return metrics
    
    def auto_patch(self):
        """
        Automatically discover and patch PyTorch components in the caller's frame.
        """
        # Get the caller's frame
        frame = inspect.currentframe().f_back
        
        # Find PyTorch components in the caller's frame
        model = None
        optimizer = None
        dataloader = None
        
        for var_name, var_val in frame.f_locals.items():
            if isinstance(var_val, nn.Module):
                model = var_val
            elif isinstance(var_val, optim.Optimizer):
                optimizer = var_val
            elif isinstance(var_val, DataLoader):
                dataloader = var_val
        
        # Register discovered components
        self.register(model, optimizer, dataloader)
        
        # Attach hooks and patches
        self.attach()
        
        logger.info(f"Auto-patched PyTorch components: model={model is not None}, optimizer={optimizer is not None}, dataloader={dataloader is not None}")
    
    def watch(self, train_loop: Callable):
        """
        Watch a training loop.
        
        Args:
            train_loop: Training loop function to watch
        
        Returns:
            Wrapped training loop function
        """
        @functools.wraps(train_loop)
        def wrapped_train_loop(*args, **kwargs):
            # Attach hooks and patches
            self.attach()
            
            try:
                # Run the training loop
                result = train_loop(*args, **kwargs)
                return result
            finally:
                # Detach hooks and restore original methods
                self.detach()
        
        return wrapped_train_loop
    
    def __del__(self):
        """
        Clean up when the integration is deleted.
        """
        self.detach()


class PyTorchHooks:
    """
    Hooks for PyTorch components.
    
    This class provides hooks for PyTorch components that can be used
    to monitor and optimize PyTorch models and training loops.
    """
    
    @staticmethod
    def patch_module(module: nn.Module, doctor: Any) -> nn.Module:
        """
        Patch a PyTorch module to enable monitoring.
        
        Args:
            module: PyTorch module to patch
            doctor: Reference to the Doctor instance
        
        Returns:
            Patched module
        """
        # Create a PyTorch integration
        integration = PyTorchIntegration(doctor, model=module)
        
        # Attach hooks
        integration.attach()
        
        # Store the integration in the module
        module._autopd_integration = integration
        
        return module
    
    @staticmethod
    def patch_optimizer(optimizer: optim.Optimizer, doctor: Any) -> optim.Optimizer:
        """
        Patch a PyTorch optimizer to enable monitoring.
        
        Args:
            optimizer: PyTorch optimizer to patch
            doctor: Reference to the Doctor instance
        
        Returns:
            Patched optimizer
        """
        # Create a PyTorch integration
        integration = PyTorchIntegration(doctor, optimizer=optimizer)
        
        # Attach hooks
        integration.attach()
        
        # Store the integration in the optimizer
        optimizer._autopd_integration = integration
        
        return optimizer
    
    @staticmethod
    def patch_dataloader(dataloader: DataLoader, doctor: Any) -> DataLoader:
        """
        Patch a PyTorch dataloader to enable monitoring.
        
        Args:
            dataloader: PyTorch dataloader to patch
            doctor: Reference to the Doctor instance
        
        Returns:
            Patched dataloader
        """
        # Create a PyTorch integration
        integration = PyTorchIntegration(doctor, dataloader=dataloader)
        
        # Attach hooks
        integration.attach()
        
        # Store the integration in the dataloader
        dataloader._autopd_integration = integration
        
        return dataloader
    
    @staticmethod
    def watch_training(
        model: nn.Module,
        optimizer: optim.Optimizer,
        dataloader: DataLoader,
        doctor: Any,
    ) -> Tuple[nn.Module, optim.Optimizer, DataLoader]:
        """
        Watch a PyTorch training setup.
        
        Args:
            model: PyTorch model to watch
            optimizer: PyTorch optimizer to watch
            dataloader: PyTorch dataloader to watch
            doctor: Reference to the Doctor instance
        
        Returns:
            Tuple of patched model, optimizer, and dataloader
        """
        # Create a PyTorch integration
        integration = PyTorchIntegration(doctor, model, optimizer, dataloader)
        
        # Attach hooks
        integration.attach()
        
        # Store the integration in the components
        model._autopd_integration = integration
        optimizer._autopd_integration = integration
        dataloader._autopd_integration = integration
        
        return model, optimizer, dataloader
