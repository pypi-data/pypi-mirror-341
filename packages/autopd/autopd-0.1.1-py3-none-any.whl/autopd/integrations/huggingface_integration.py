"""
HuggingFace integration module for AutoPipelineDoctor.

This module provides integration with HuggingFace Transformers, allowing AutoPipelineDoctor
to monitor and optimize Transformer models and training loops.
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
    import transformers
    from transformers import Trainer, TrainingArguments, PreTrainedModel, TrainerCallback
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False
    # Create dummy classes for type hints
    class TrainerCallback:
        pass
    class Trainer:
        pass
    class TrainingArguments:
        pass
    class PreTrainedModel:
        pass

from autopd.integrations.pytorch_integration import PyTorchIntegration

logger = logging.getLogger(__name__)


class HuggingFaceCallback(TrainerCallback):
    """
    HuggingFace Transformers callback for AutoPipelineDoctor.
    
    This callback integrates AutoPipelineDoctor with HuggingFace Transformers,
    allowing monitoring and optimization of Transformer models and training loops.
    
    Attributes:
        doctor: Reference to the Doctor instance
        integration: PyTorch integration instance
        metrics: Dictionary of collected metrics
    """
    
    def __init__(self, doctor: Any):
        """
        Initialize the HuggingFace callback.
        
        Args:
            doctor: Reference to the Doctor instance
        """
        super().__init__()
        
        if not TRANSFORMERS_AVAILABLE:
            raise ImportError("HuggingFace Transformers is not installed. Install with: pip install transformers")
        
        self.doctor = doctor
        self.integration = None
        
        # Initialize metrics
        self.metrics = {
            "epoch_times": [],
            "step_times": [],
            "train_losses": [],
            "eval_losses": [],
            "learning_rates": [],
            "train_batch_sizes": [],
            "eval_batch_sizes": [],
        }
        
        # Initialize state
        self.current_epoch = 0
        self.current_step = 0
        self.epoch_start_time = 0
        self.step_start_time = 0
        self.train_batch_count = 0
        self.eval_batch_count = 0
        self.is_training = True
        
        logger.info("HuggingFace callback initialized")
    
    def on_init_end(self, args: "TrainingArguments", state: "transformers.TrainerState", control: "transformers.TrainerControl", **kwargs):
        """
        Called at the end of trainer initialization.
        
        Args:
            args: Training arguments
            state: Trainer state
            control: Trainer control
            **kwargs: Additional keyword arguments
        """
        # Store training arguments
        self.args = args
        
        logger.info("HuggingFace trainer initialized")
    
    def on_train_begin(self, args: "TrainingArguments", state: "transformers.TrainerState", control: "transformers.TrainerControl", model: "PreTrainedModel", **kwargs):
        """
        Called at the beginning of training.
        
        Args:
            args: Training arguments
            state: Trainer state
            control: Trainer control
            model: Model being trained
            **kwargs: Additional keyword arguments
        """
        # Create PyTorch integration
        self.integration = PyTorchIntegration(
            self.doctor,
            model=model,
            optimizer=kwargs.get("optimizer"),
            dataloader=kwargs.get("train_dataloader"),
        )
        
        # Attach hooks and patches
        self.integration.attach()
        
        # Collect model information
        model_info = self._collect_model_info(model)
        
        # Collect dataset information
        dataset_info = self._collect_dataset_info(kwargs.get("train_dataloader"))
        
        # Collect hardware information
        hardware_info = self._collect_hardware_info()
        
        # Start experience brain if available
        if hasattr(self.doctor, "experience_brain") and self.doctor.experience_brain:
            self.doctor.experience_brain.start(
                model_info=model_info,
                dataset_info=dataset_info,
                hardware_info=hardware_info,
            )
        
        # Set training flag
        self.is_training = True
        
        logger.info("HuggingFace training started")
    
    def on_train_end(self, args: "TrainingArguments", state: "transformers.TrainerState", control: "transformers.TrainerControl", model: "PreTrainedModel", **kwargs):
        """
        Called at the end of training.
        
        Args:
            args: Training arguments
            state: Trainer state
            control: Trainer control
            model: Model being trained
            **kwargs: Additional keyword arguments
        """
        # Detach hooks and restore original methods
        if self.integration:
            self.integration.detach()
            self.integration = None
        
        # Stop experience brain if available
        if hasattr(self.doctor, "experience_brain") and self.doctor.experience_brain:
            self.doctor.experience_brain.stop()
        
        logger.info("HuggingFace training ended")
    
    def on_epoch_begin(self, args: "TrainingArguments", state: "transformers.TrainerState", control: "transformers.TrainerControl", **kwargs):
        """
        Called at the beginning of an epoch.
        
        Args:
            args: Training arguments
            state: Trainer state
            control: Trainer control
            **kwargs: Additional keyword arguments
        """
        self.epoch_start_time = time.time()
        self.current_epoch = state.epoch
        
        logger.info(f"HuggingFace epoch {self.current_epoch} started")
    
    def on_epoch_end(self, args: "TrainingArguments", state: "transformers.TrainerState", control: "transformers.TrainerControl", **kwargs):
        """
        Called at the end of an epoch.
        
        Args:
            args: Training arguments
            state: Trainer state
            control: Trainer control
            **kwargs: Additional keyword arguments
        """
        # Calculate epoch time
        epoch_time = time.time() - self.epoch_start_time
        self.metrics["epoch_times"].append(epoch_time)
        
        # Collect learning rate
        if hasattr(state, "log_history") and state.log_history:
            for entry in reversed(state.log_history):
                if "learning_rate" in entry:
                    self.metrics["learning_rates"].append(entry["learning_rate"])
                    break
        
        # Collect metrics
        self._collect_metrics()
        
        logger.info(f"HuggingFace epoch {self.current_epoch} ended (time: {epoch_time:.2f}s)")
    
    def on_step_begin(self, args: "TrainingArguments", state: "transformers.TrainerState", control: "transformers.TrainerControl", **kwargs):
        """
        Called at the beginning of a step.
        
        Args:
            args: Training arguments
            state: Trainer state
            control: Trainer control
            **kwargs: Additional keyword arguments
        """
        self.step_start_time = time.time()
        self.current_step = state.global_step
    
    def on_step_end(self, args: "TrainingArguments", state: "transformers.TrainerState", control: "transformers.TrainerControl", **kwargs):
        """
        Called at the end of a step.
        
        Args:
            args: Training arguments
            state: Trainer state
            control: Trainer control
            **kwargs: Additional keyword arguments
        """
        # Calculate step time
        step_time = time.time() - self.step_start_time
        self.metrics["step_times"].append(step_time)
        
        # Increment batch counter if training
        if self.is_training:
            self.train_batch_count += 1
        else:
            self.eval_batch_count += 1
        
        # Collect metrics every 10 steps
        if self.current_step % 10 == 0:
            self._collect_metrics()
            
            # Check for overfitting
            self._check_overfitting(state)
    
    def on_evaluate(self, args: "TrainingArguments", state: "transformers.TrainerState", control: "transformers.TrainerControl", **kwargs):
        """
        Called before evaluation.
        
        Args:
            args: Training arguments
            state: Trainer state
            control: Trainer control
            **kwargs: Additional keyword arguments
        """
        # Set training flag
        self.is_training = False
        
        logger.info(f"HuggingFace evaluation started at step {self.current_step}")
    
    def on_evaluate_end(self, args: "TrainingArguments", state: "transformers.TrainerState", control: "transformers.TrainerControl", metrics: Dict[str, float], **kwargs):
        """
        Called at the end of evaluation.
        
        Args:
            args: Training arguments
            state: Trainer state
            control: Trainer control
            metrics: Evaluation metrics
            **kwargs: Additional keyword arguments
        """
        # Set training flag
        self.is_training = True
        
        # Store evaluation loss
        if "eval_loss" in metrics:
            self.metrics["eval_losses"].append(metrics["eval_loss"])
        
        logger.info(f"HuggingFace evaluation ended at step {self.current_step}")
    
    def on_log(self, args: "TrainingArguments", state: "transformers.TrainerState", control: "transformers.TrainerControl", logs: Dict[str, float], **kwargs):
        """
        Called when logs are about to be saved.
        
        Args:
            args: Training arguments
            state: Trainer state
            control: Trainer control
            logs: Log values
            **kwargs: Additional keyword arguments
        """
        # Store training loss
        if "loss" in logs:
            self.metrics["train_losses"].append(logs["loss"])
        
        # Store learning rate
        if "learning_rate" in logs:
            self.metrics["learning_rates"].append(logs["learning_rate"])
        
        # Store batch size
        if self.is_training and "train_batch_size" in logs:
            self.metrics["train_batch_sizes"].append(logs["train_batch_size"])
        elif not self.is_training and "eval_batch_size" in logs:
            self.metrics["eval_batch_sizes"].append(logs["eval_batch_size"])
    
    def on_prediction_step(self, args: "TrainingArguments", state: "transformers.TrainerState", control: "transformers.TrainerControl", **kwargs):
        """
        Called before a prediction step.
        
        Args:
            args: Training arguments
            state: Trainer state
            control: Trainer control
            **kwargs: Additional keyword arguments
        """
        pass
    
    def on_save(self, args: "TrainingArguments", state: "transformers.TrainerState", control: "transformers.TrainerControl", **kwargs):
        """
        Called when a checkpoint is about to be saved.
        
        Args:
            args: Training arguments
            state: Trainer state
            control: Trainer control
            **kwargs: Additional keyword arguments
        """
        # Add optimization to experience brain
        if hasattr(self.doctor, "experience_brain") and self.doctor.experience_brain:
            self.doctor.experience_brain.add_optimization({
                "type": "checkpoint",
                "message": f"Saved checkpoint at step {self.current_step}",
                "details": f"Epoch: {self.current_epoch}, Step: {self.current_step}",
            })
        
        logger.info(f"HuggingFace checkpoint saved at step {self.current_step}")
    
    def _collect_metrics(self):
        """
        Collect metrics and send them to the doctor.
        """
        if not self.doctor:
            return
        
        # Calculate average times
        avg_epoch_time = sum(self.metrics["epoch_times"][-5:]) / max(1, len(self.metrics["epoch_times"][-5:]))
        avg_step_time = sum(self.metrics["step_times"][-20:]) / max(1, len(self.metrics["step_times"][-20:]))
        
        # Collect timing metrics
        timing_metrics = {
            "epoch_time": avg_epoch_time,
            "step_time": avg_step_time,
            "epoch": self.current_epoch,
            "step": self.current_step,
            "train_batch_count": self.train_batch_count,
            "eval_batch_count": self.eval_batch_count,
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
        
        if self.metrics["eval_losses"]:
            training_metrics["eval_loss"] = self.metrics["eval_losses"][-1]
        
        # Send metrics to the doctor
        if hasattr(self.doctor, "experience_brain") and self.doctor.experience_brain:
            self.doctor.experience_brain.update_metrics(training_metrics, category="training")
    
    def _check_overfitting(self, state: "transformers.TrainerState"):
        """
        Check for overfitting based on training and evaluation losses.
        
        Args:
            state: Trainer state
        """
        if len(self.metrics["train_losses"]) < 3 or len(self.metrics["eval_losses"]) < 3:
            return
        
        # Get recent losses
        recent_train_losses = self.metrics["train_losses"][-3:]
        recent_eval_losses = self.metrics["eval_losses"][-3:]
        
        # Check if train loss is decreasing but eval loss is increasing
        train_decreasing = recent_train_losses[0] > recent_train_losses[-1]
        eval_increasing = recent_eval_losses[0] < recent_eval_losses[-1]
        
        if train_decreasing and eval_increasing:
            # Calculate the gap between train and eval loss
            train_eval_gap = recent_eval_losses[-1] - recent_train_losses[-1]
            train_eval_gap_pct = train_eval_gap / recent_train_losses[-1] if recent_train_losses[-1] > 0 else 0
            
            if train_eval_gap_pct > 0.2:
                # Add warning to experience brain
                if hasattr(self.doctor, "experience_brain") and self.doctor.experience_brain:
                    self.doctor.experience_brain.add_warning({
                        "type": "overfitting",
                        "message": f"Potential overfitting detected (gap: {train_eval_gap_pct:.1%})",
                        "details": f"Train loss: {recent_train_losses[-1]:.4f}, Eval loss: {recent_eval_losses[-1]:.4f}",
                        "severity": "high" if train_eval_gap_pct > 0.5 else "medium",
                        "suggestions": [
                            "Add weight decay",
                            "Reduce model complexity",
                            "Increase training data or use data augmentation",
                            "Implement early stopping",
                        ],
                    })
                
                logger.warning(f"Potential overfitting detected (gap: {train_eval_gap_pct:.1%})")
    
    def _collect_model_info(self, model: "PreTrainedModel") -> Dict[str, Any]:
        """
        Collect information about the model.
        
        Args:
            model: HuggingFace model
        
        Returns:
            Dictionary of model information
        """
        model_info = {
            "name": model.__class__.__name__,
            "architecture": model.config.model_type if hasattr(model, "config") and hasattr(model.config, "model_type") else model.__class__.__name__,
        }
        
        # Get model configuration
        if hasattr(model, "config"):
            # Add common configuration attributes
            for attr in ["hidden_size", "num_hidden_layers", "num_attention_heads", "intermediate_size", "vocab_size"]:
                if hasattr(model.config, attr):
                    model_info[attr] = getattr(model.config, attr)
        
        # Count parameters
        total_params = sum(p.numel() for p in model.parameters())
        trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
        
        model_info["num_parameters"] = total_params
        model_info["trainable_parameters"] = trainable_params
        model_info["non_trainable_parameters"] = total_params - trainable_params
        
        # Get model size
        model_size_bytes = sum(p.numel() * p.element_size() for p in model.parameters())
        model_info["model_size_mb"] = model_size_bytes / (1024 * 1024)
        
        return model_info
    
    def _collect_dataset_info(self, dataloader: Optional[DataLoader]) -> Dict[str, Any]:
        """
        Collect information about the dataset.
        
        Args:
            dataloader: PyTorch dataloader
        
        Returns:
            Dictionary of dataset information
        """
        dataset_info = {
            "name": "unknown",
        }
        
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


class HuggingFaceIntegration:
    """
    Integration with HuggingFace Transformers.
    
    This class provides integration with HuggingFace Transformers, allowing AutoPipelineDoctor
    to monitor and optimize Transformer models and training loops.
    
    Attributes:
        doctor: Reference to the Doctor instance
        callback: HuggingFace callback instance
    """
    
    def __init__(self, doctor: Any):
        """
        Initialize the HuggingFace integration.
        
        Args:
            doctor: Reference to the Doctor instance
        """
        if not TRANSFORMERS_AVAILABLE:
            raise ImportError("HuggingFace Transformers is not installed. Install with: pip install transformers")
        
        self.doctor = doctor
        self.callback = HuggingFaceCallback(doctor)
        
        logger.info("HuggingFace integration initialized")
    
    def get_callback(self) -> TrainerCallback:
        """
        Get the HuggingFace callback.
        
        Returns:
            HuggingFace callback
        """
        return self.callback
    
    @staticmethod
    def patch_trainer(trainer: Trainer, doctor: Any) -> Trainer:
        """
        Patch a HuggingFace trainer to enable monitoring.
        
        Args:
            trainer: HuggingFace trainer to patch
            doctor: Reference to the Doctor instance
        
        Returns:
            Patched trainer
        """
        if not TRANSFORMERS_AVAILABLE:
            raise ImportError("HuggingFace Transformers is not installed. Install with: pip install transformers")
        
        # Create callback
        callback = HuggingFaceCallback(doctor)
        
        # Add callback to trainer
        if hasattr(trainer, "callback_handler"):
            trainer.add_callback(callback)
        
        return trainer
    
    @staticmethod
    def create_trainer_with_monitoring(doctor: Any, model: PreTrainedModel, args: TrainingArguments, **trainer_kwargs) -> Trainer:
        """
        Create a HuggingFace trainer with monitoring.
        
        Args:
            doctor: Reference to the Doctor instance
            model: HuggingFace model
            args: Training arguments
            **trainer_kwargs: Keyword arguments for the trainer
        
        Returns:
            HuggingFace trainer with monitoring
        """
        if not TRANSFORMERS_AVAILABLE:
            raise ImportError("HuggingFace Transformers is not installed. Install with: pip install transformers")
        
        # Create callback
        callback = HuggingFaceCallback(doctor)
        
        # Add callback to trainer kwargs
        if "callbacks" in trainer_kwargs:
            if isinstance(trainer_kwargs["callbacks"], list):
                trainer_kwargs["callbacks"].append(callback)
            else:
                trainer_kwargs["callbacks"] = [trainer_kwargs["callbacks"], callback]
        else:
            trainer_kwargs["callbacks"] = [callback]
        
        # Create trainer
        trainer = Trainer(
            model=model,
            args=args,
            **trainer_kwargs
        )
        
        return trainer
