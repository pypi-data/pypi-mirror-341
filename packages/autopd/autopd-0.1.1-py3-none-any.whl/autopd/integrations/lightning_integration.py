"""
PyTorch Lightning integration module for AutoPipelineDoctor.

This module provides integration with PyTorch Lightning, allowing AutoPipelineDoctor
to monitor and optimize Lightning models and training loops.
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
    import pytorch_lightning as pl
    from pytorch_lightning.callbacks import Callback
    LIGHTNING_AVAILABLE = True
except ImportError:
    LIGHTNING_AVAILABLE = False
    # Create dummy classes for type hints
    class Callback:
        pass
    class pl:
        class Trainer:
            pass
        class LightningModule:
            pass

from autopd.integrations.pytorch_integration import PyTorchIntegration

logger = logging.getLogger(__name__)


class LightningCallback(Callback):
    """
    PyTorch Lightning callback for AutoPipelineDoctor.
    
    This callback integrates AutoPipelineDoctor with PyTorch Lightning,
    allowing monitoring and optimization of Lightning models and training loops.
    
    Attributes:
        doctor: Reference to the Doctor instance
        integration: PyTorch integration instance
        metrics: Dictionary of collected metrics
    """
    
    def __init__(self, doctor: Any):
        """
        Initialize the Lightning callback.
        
        Args:
            doctor: Reference to the Doctor instance
        """
        super().__init__()
        
        if not LIGHTNING_AVAILABLE:
            raise ImportError("PyTorch Lightning is not installed. Install with: pip install pytorch-lightning")
        
        self.doctor = doctor
        self.integration = None
        
        # Initialize metrics
        self.metrics = {
            "epoch_times": [],
            "train_batch_times": [],
            "val_batch_times": [],
            "train_losses": [],
            "val_losses": [],
            "learning_rates": [],
        }
        
        # Initialize state
        self.current_epoch = 0
        self.current_batch_idx = 0
        self.epoch_start_time = 0
        self.batch_start_time = 0
        self.train_batch_count = 0
        self.val_batch_count = 0
        
        logger.info("Lightning callback initialized")
    
    def setup(self, trainer: "pl.Trainer", pl_module: "pl.LightningModule", stage: Optional[str] = None):
        """
        Called when fit, validate, test, or predict begins.
        
        Args:
            trainer: Lightning trainer
            pl_module: Lightning module
            stage: Current stage (fit, validate, test, predict)
        """
        # Create PyTorch integration
        self.integration = PyTorchIntegration(
            self.doctor,
            model=pl_module,
            optimizer=self._get_optimizer(pl_module),
            dataloader=self._get_dataloader(trainer),
        )
        
        # Attach hooks and patches
        self.integration.attach()
        
        logger.info(f"Lightning callback setup for stage: {stage}")
    
    def teardown(self, trainer: "pl.Trainer", pl_module: "pl.LightningModule", stage: Optional[str] = None):
        """
        Called when fit, validate, test, or predict ends.
        
        Args:
            trainer: Lightning trainer
            pl_module: Lightning module
            stage: Current stage (fit, validate, test, predict)
        """
        # Detach hooks and restore original methods
        if self.integration:
            self.integration.detach()
            self.integration = None
        
        logger.info(f"Lightning callback teardown for stage: {stage}")
    
    def on_fit_start(self, trainer: "pl.Trainer", pl_module: "pl.LightningModule"):
        """
        Called when fit begins.
        
        Args:
            trainer: Lightning trainer
            pl_module: Lightning module
        """
        # Collect model information
        model_info = self._collect_model_info(pl_module)
        
        # Collect dataset information
        dataset_info = self._collect_dataset_info(trainer)
        
        # Collect hardware information
        hardware_info = self._collect_hardware_info()
        
        # Start experience brain if available
        if hasattr(self.doctor, "experience_brain") and self.doctor.experience_brain:
            self.doctor.experience_brain.start(
                model_info=model_info,
                dataset_info=dataset_info,
                hardware_info=hardware_info,
            )
        
        logger.info("Lightning fit started")
    
    def on_fit_end(self, trainer: "pl.Trainer", pl_module: "pl.LightningModule"):
        """
        Called when fit ends.
        
        Args:
            trainer: Lightning trainer
            pl_module: Lightning module
        """
        # Stop experience brain if available
        if hasattr(self.doctor, "experience_brain") and self.doctor.experience_brain:
            self.doctor.experience_brain.stop()
        
        logger.info("Lightning fit ended")
    
    def on_train_epoch_start(self, trainer: "pl.Trainer", pl_module: "pl.LightningModule"):
        """
        Called when a train epoch begins.
        
        Args:
            trainer: Lightning trainer
            pl_module: Lightning module
        """
        self.epoch_start_time = time.time()
        self.current_epoch = trainer.current_epoch
        self.train_batch_count = 0
        
        logger.info(f"Lightning train epoch {self.current_epoch} started")
    
    def on_train_epoch_end(self, trainer: "pl.Trainer", pl_module: "pl.LightningModule"):
        """
        Called when a train epoch ends.
        
        Args:
            trainer: Lightning trainer
            pl_module: Lightning module
        """
        # Calculate epoch time
        epoch_time = time.time() - self.epoch_start_time
        self.metrics["epoch_times"].append(epoch_time)
        
        # Collect learning rate
        lr = self._get_learning_rate(pl_module)
        if lr is not None:
            self.metrics["learning_rates"].append(lr)
        
        # Collect train loss
        train_loss = self._get_train_loss(trainer)
        if train_loss is not None:
            self.metrics["train_losses"].append(train_loss)
        
        # Collect metrics
        self._collect_metrics()
        
        logger.info(f"Lightning train epoch {self.current_epoch} ended (time: {epoch_time:.2f}s)")
    
    def on_validation_epoch_start(self, trainer: "pl.Trainer", pl_module: "pl.LightningModule"):
        """
        Called when a validation epoch begins.
        
        Args:
            trainer: Lightning trainer
            pl_module: Lightning module
        """
        self.val_batch_count = 0
        
        logger.info(f"Lightning validation epoch {self.current_epoch} started")
    
    def on_validation_epoch_end(self, trainer: "pl.Trainer", pl_module: "pl.LightningModule"):
        """
        Called when a validation epoch ends.
        
        Args:
            trainer: Lightning trainer
            pl_module: Lightning module
        """
        # Collect validation loss
        val_loss = self._get_val_loss(trainer)
        if val_loss is not None:
            self.metrics["val_losses"].append(val_loss)
        
        # Check for overfitting
        self._check_overfitting()
        
        logger.info(f"Lightning validation epoch {self.current_epoch} ended")
    
    def on_train_batch_start(self, trainer: "pl.Trainer", pl_module: "pl.LightningModule", batch: Any, batch_idx: int):
        """
        Called when a train batch begins.
        
        Args:
            trainer: Lightning trainer
            pl_module: Lightning module
            batch: Current batch
            batch_idx: Index of current batch
        """
        self.batch_start_time = time.time()
        self.current_batch_idx = batch_idx
        
        # Update PyTorch integration
        if self.integration:
            self.integration.current_batch = batch
            self.integration.current_batch_size = self._get_batch_size(batch)
            self.integration.last_iteration_time = time.time()
    
    def on_train_batch_end(self, trainer: "pl.Trainer", pl_module: "pl.LightningModule", outputs: Any, batch: Any, batch_idx: int):
        """
        Called when a train batch ends.
        
        Args:
            trainer: Lightning trainer
            pl_module: Lightning module
            outputs: Outputs from the model
            batch: Current batch
            batch_idx: Index of current batch
        """
        # Calculate batch time
        batch_time = time.time() - self.batch_start_time
        self.metrics["train_batch_times"].append(batch_time)
        
        # Increment batch counter
        self.train_batch_count += 1
        
        # Collect metrics every 10 batches
        if self.train_batch_count % 10 == 0:
            self._collect_metrics()
    
    def on_validation_batch_start(self, trainer: "pl.Trainer", pl_module: "pl.LightningModule", batch: Any, batch_idx: int, dataloader_idx: int = 0):
        """
        Called when a validation batch begins.
        
        Args:
            trainer: Lightning trainer
            pl_module: Lightning module
            batch: Current batch
            batch_idx: Index of current batch
            dataloader_idx: Index of current dataloader
        """
        self.batch_start_time = time.time()
    
    def on_validation_batch_end(self, trainer: "pl.Trainer", pl_module: "pl.LightningModule", outputs: Any, batch: Any, batch_idx: int, dataloader_idx: int = 0):
        """
        Called when a validation batch ends.
        
        Args:
            trainer: Lightning trainer
            pl_module: Lightning module
            outputs: Outputs from the model
            batch: Current batch
            batch_idx: Index of current batch
            dataloader_idx: Index of current dataloader
        """
        # Calculate batch time
        batch_time = time.time() - self.batch_start_time
        self.metrics["val_batch_times"].append(batch_time)
        
        # Increment batch counter
        self.val_batch_count += 1
    
    def on_exception(self, trainer: "pl.Trainer", pl_module: "pl.LightningModule", exception: BaseException):
        """
        Called when an exception occurs.
        
        Args:
            trainer: Lightning trainer
            pl_module: Lightning module
            exception: The exception that occurred
        """
        # Add warning to experience brain
        if hasattr(self.doctor, "experience_brain") and self.doctor.experience_brain:
            self.doctor.experience_brain.add_warning({
                "type": "exception",
                "message": f"Exception occurred: {str(exception)}",
                "details": str(exception),
                "severity": "critical",
            })
        
        # Stop experience brain with failed status
        if hasattr(self.doctor, "experience_brain") and self.doctor.experience_brain:
            self.doctor.experience_brain.stop(status="failed")
        
        logger.error(f"Lightning exception: {str(exception)}")
    
    def _collect_metrics(self):
        """
        Collect metrics and send them to the doctor.
        """
        if not self.doctor:
            return
        
        # Calculate average times
        avg_epoch_time = sum(self.metrics["epoch_times"][-5:]) / max(1, len(self.metrics["epoch_times"][-5:]))
        avg_train_batch_time = sum(self.metrics["train_batch_times"][-20:]) / max(1, len(self.metrics["train_batch_times"][-20:]))
        avg_val_batch_time = sum(self.metrics["val_batch_times"][-20:]) / max(1, len(self.metrics["val_batch_times"][-20:]))
        
        # Collect timing metrics
        timing_metrics = {
            "epoch_time": avg_epoch_time,
            "train_batch_time": avg_train_batch_time,
            "val_batch_time": avg_val_batch_time,
            "epoch": self.current_epoch,
            "train_batch_count": self.train_batch_count,
            "val_batch_count": self.val_batch_count,
        }
        
        # Send metrics to the doctor
        if hasattr(self.doctor, "timing_profiler") and self.doctor.timing_profiler:
            self.doctor.timing_profiler.update_metrics(timing_metrics)
        
        # Collect training metrics
        training_metrics = {}
        
        # Add learning rate
        if self.metrics["learning_rates"]:
            training_metrics["learning_rate"] = self.metrics["learning_rates"][-1]
        
        # Add losses
        if self.metrics["train_losses"]:
            training_metrics["train_loss"] = self.metrics["train_losses"][-1]
        
        if self.metrics["val_losses"]:
            training_metrics["val_loss"] = self.metrics["val_losses"][-1]
        
        # Send metrics to the doctor
        if hasattr(self.doctor, "experience_brain") and self.doctor.experience_brain:
            self.doctor.experience_brain.update_metrics(training_metrics, category="training")
    
    def _check_overfitting(self):
        """
        Check for overfitting based on training and validation losses.
        """
        if len(self.metrics["train_losses"]) < 3 or len(self.metrics["val_losses"]) < 3:
            return
        
        # Get recent losses
        recent_train_losses = self.metrics["train_losses"][-3:]
        recent_val_losses = self.metrics["val_losses"][-3:]
        
        # Check if train loss is decreasing but val loss is increasing
        train_decreasing = recent_train_losses[0] > recent_train_losses[-1]
        val_increasing = recent_val_losses[0] < recent_val_losses[-1]
        
        if train_decreasing and val_increasing:
            # Calculate the gap between train and val loss
            train_val_gap = recent_val_losses[-1] - recent_train_losses[-1]
            train_val_gap_pct = train_val_gap / recent_train_losses[-1] if recent_train_losses[-1] > 0 else 0
            
            if train_val_gap_pct > 0.2:
                # Add warning to experience brain
                if hasattr(self.doctor, "experience_brain") and self.doctor.experience_brain:
                    self.doctor.experience_brain.add_warning({
                        "type": "overfitting",
                        "message": f"Potential overfitting detected (gap: {train_val_gap_pct:.1%})",
                        "details": f"Train loss: {recent_train_losses[-1]:.4f}, Val loss: {recent_val_losses[-1]:.4f}",
                        "severity": "high" if train_val_gap_pct > 0.5 else "medium",
                        "suggestions": [
                            "Add regularization (L1, L2, dropout)",
                            "Reduce model complexity",
                            "Increase training data or use data augmentation",
                            "Implement early stopping",
                        ],
                    })
                
                logger.warning(f"Potential overfitting detected (gap: {train_val_gap_pct:.1%})")
    
    def _get_optimizer(self, pl_module: "pl.LightningModule") -> Optional[optim.Optimizer]:
        """
        Get the optimizer from the Lightning module.
        
        Args:
            pl_module: Lightning module
        
        Returns:
            Optimizer or None if not found
        """
        if hasattr(pl_module, "optimizers") and callable(pl_module.optimizers):
            optimizers = pl_module.optimizers()
            if isinstance(optimizers, list) and optimizers:
                return optimizers[0]
            return optimizers
        return None
    
    def _get_dataloader(self, trainer: "pl.Trainer") -> Optional[DataLoader]:
        """
        Get the dataloader from the trainer.
        
        Args:
            trainer: Lightning trainer
        
        Returns:
            Dataloader or None if not found
        """
        if hasattr(trainer, "train_dataloader") and trainer.train_dataloader is not None:
            return trainer.train_dataloader
        return None
    
    def _get_learning_rate(self, pl_module: "pl.LightningModule") -> Optional[float]:
        """
        Get the current learning rate.
        
        Args:
            pl_module: Lightning module
        
        Returns:
            Learning rate or None if not found
        """
        optimizer = self._get_optimizer(pl_module)
        if optimizer and hasattr(optimizer, "param_groups") and optimizer.param_groups:
            return optimizer.param_groups[0].get("lr")
        return None
    
    def _get_train_loss(self, trainer: "pl.Trainer") -> Optional[float]:
        """
        Get the current training loss.
        
        Args:
            trainer: Lightning trainer
        
        Returns:
            Training loss or None if not found
        """
        if hasattr(trainer, "callback_metrics"):
            # Try common loss names
            for name in ["train_loss", "loss", "training_loss"]:
                if name in trainer.callback_metrics:
                    loss = trainer.callback_metrics[name]
                    if isinstance(loss, torch.Tensor):
                        return loss.item()
                    elif isinstance(loss, (int, float)):
                        return float(loss)
        return None
    
    def _get_val_loss(self, trainer: "pl.Trainer") -> Optional[float]:
        """
        Get the current validation loss.
        
        Args:
            trainer: Lightning trainer
        
        Returns:
            Validation loss or None if not found
        """
        if hasattr(trainer, "callback_metrics"):
            # Try common loss names
            for name in ["val_loss", "validation_loss"]:
                if name in trainer.callback_metrics:
                    loss = trainer.callback_metrics[name]
                    if isinstance(loss, torch.Tensor):
                        return loss.item()
                    elif isinstance(loss, (int, float)):
                        return float(loss)
        return None
    
    def _get_batch_size(self, batch: Any) -> int:
        """
        Get the batch size from a batch.
        
        Args:
            batch: Batch to get size from
        
        Returns:
            Batch size
        """
        if isinstance(batch, (list, tuple)) and len(batch) > 0:
            if isinstance(batch[0], torch.Tensor):
                return batch[0].shape[0]
            elif isinstance(batch[0], (list, tuple)) and len(batch[0]) > 0:
                if isinstance(batch[0][0], torch.Tensor):
                    return batch[0][0].shape[0]
        elif isinstance(batch, dict) and len(batch) > 0:
            first_key = next(iter(batch))
            if isinstance(batch[first_key], torch.Tensor):
                return batch[first_key].shape[0]
        elif isinstance(batch, torch.Tensor):
            return batch.shape[0]
        
        return 0
    
    def _collect_model_info(self, pl_module: "pl.LightningModule") -> Dict[str, Any]:
        """
        Collect information about the model.
        
        Args:
            pl_module: Lightning module
        
        Returns:
            Dictionary of model information
        """
        model_info = {
            "name": pl_module.__class__.__name__,
            "architecture": pl_module.__class__.__name__,
        }
        
        # Count parameters
        total_params = sum(p.numel() for p in pl_module.parameters())
        trainable_params = sum(p.numel() for p in pl_module.parameters() if p.requires_grad)
        
        model_info["num_parameters"] = total_params
        model_info["trainable_parameters"] = trainable_params
        model_info["non_trainable_parameters"] = total_params - trainable_params
        
        # Get model size
        model_size_bytes = sum(p.numel() * p.element_size() for p in pl_module.parameters())
        model_info["model_size_mb"] = model_size_bytes / (1024 * 1024)
        
        # Get optimizer info
        optimizer = self._get_optimizer(pl_module)
        if optimizer:
            model_info["optimizer"] = optimizer.__class__.__name__
            
            # Get learning rate
            if hasattr(optimizer, "param_groups") and optimizer.param_groups:
                model_info["learning_rate"] = optimizer.param_groups[0].get("lr")
        
        return model_info
    
    def _collect_dataset_info(self, trainer: "pl.Trainer") -> Dict[str, Any]:
        """
        Collect information about the dataset.
        
        Args:
            trainer: Lightning trainer
        
        Returns:
            Dictionary of dataset information
        """
        dataset_info = {
            "name": "unknown",
        }
        
        # Get dataloader
        dataloader = self._get_dataloader(trainer)
        if dataloader:
            # Get dataset
            if hasattr(dataloader, "dataset"):
                dataset = dataloader.dataset
                
                # Get dataset name
                if hasattr(dataset, "__class__"):
                    dataset_info["name"] = dataset.__class__.__name__
                
                # Get dataset size
                if hasattr(dataset, "__len__"):
                    dataset_info["num_samples"] = len(dataset)
        
        return dataset_info
    
    def _collect_hardware_info(self) -> Dict[str, Any]:
        """
        Collect information about the hardware.
        
        Returns:
            Dictionary of hardware information
        """
        hardware_info = {
            "name": "unknown",
        }
        
        # Check if using CUDA
        if torch.cuda.is_available():
            hardware_info["name"] = f"cuda:{torch.cuda.current_device()}"
            hardware_info["gpu_name"] = torch.cuda.get_device_name(torch.cuda.current_device())
            hardware_info["gpu_count"] = torch.cuda.device_count()
            hardware_info["gpu_memory"] = torch.cuda.get_device_properties(torch.cuda.current_device()).total_memory / (1024 * 1024)
        else:
            hardware_info["name"] = "cpu"
        
        return hardware_info


class LightningIntegration:
    """
    Integration with PyTorch Lightning.
    
    This class provides integration with PyTorch Lightning, allowing AutoPipelineDoctor
    to monitor and optimize Lightning models and training loops.
    
    Attributes:
        doctor: Reference to the Doctor instance
        callback: Lightning callback instance
    """
    
    def __init__(self, doctor: Any):
        """
        Initialize the Lightning integration.
        
        Args:
            doctor: Reference to the Doctor instance
        """
        if not LIGHTNING_AVAILABLE:
            raise ImportError("PyTorch Lightning is not installed. Install with: pip install pytorch-lightning")
        
        self.doctor = doctor
        self.callback = LightningCallback(doctor)
        
        logger.info("Lightning integration initialized")
    
    def get_callback(self) -> Callback:
        """
        Get the Lightning callback.
        
        Returns:
            Lightning callback
        """
        return self.callback
    
    @staticmethod
    def patch_trainer(trainer: "pl.Trainer", doctor: Any) -> "pl.Trainer":
        """
        Patch a Lightning trainer to enable monitoring.
        
        Args:
            trainer: Lightning trainer to patch
            doctor: Reference to the Doctor instance
        
        Returns:
            Patched trainer
        """
        if not LIGHTNING_AVAILABLE:
            raise ImportError("PyTorch Lightning is not installed. Install with: pip install pytorch-lightning")
        
        # Create callback
        callback = LightningCallback(doctor)
        
        # Add callback to trainer
        if hasattr(trainer, "callbacks"):
            trainer.callbacks.append(callback)
        
        return trainer
    
    @staticmethod
    def create_trainer_with_monitoring(doctor: Any, **trainer_kwargs) -> "pl.Trainer":
        """
        Create a Lightning trainer with monitoring.
        
        Args:
            doctor: Reference to the Doctor instance
            **trainer_kwargs: Keyword arguments for the trainer
        
        Returns:
            Lightning trainer with monitoring
        """
        if not LIGHTNING_AVAILABLE:
            raise ImportError("PyTorch Lightning is not installed. Install with: pip install pytorch-lightning")
        
        # Create callback
        callback = LightningCallback(doctor)
        
        # Add callback to trainer kwargs
        if "callbacks" in trainer_kwargs:
            if isinstance(trainer_kwargs["callbacks"], list):
                trainer_kwargs["callbacks"].append(callback)
            else:
                trainer_kwargs["callbacks"] = [trainer_kwargs["callbacks"], callback]
        else:
            trainer_kwargs["callbacks"] = [callback]
        
        # Create trainer
        trainer = pl.Trainer(**trainer_kwargs)
        
        return trainer
