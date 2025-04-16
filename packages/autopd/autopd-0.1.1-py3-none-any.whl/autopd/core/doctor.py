"""
Core Doctor class for AutoPipelineDoctor.

This module contains the main Doctor class that serves as the central controller
for monitoring, diagnosing, and optimizing ML/AI pipelines.
"""

import logging
from typing import Any, Callable, Dict, List, Optional, Union, Tuple

import torch
from torch.optim import Optimizer
from torch.utils.data import DataLoader

from autopd.profiler.hardware_profiler import HardwareProfiler
from autopd.profiler.memory_profiler import MemoryProfiler
from autopd.profiler.timing_profiler import TimingProfiler
from autopd.profiler.dataloader_profiler import DataloaderProfiler
from autopd.profiler.gradient_profiler import GradientProfiler

logger = logging.getLogger(__name__)

class Doctor:
    """
    Main controller class for AutoPipelineDoctor.
    
    The Doctor class orchestrates all monitoring, diagnosis, and optimization
    activities for ML/AI pipelines. It serves as the main entry point for users.
    
    Attributes:
        model: The PyTorch model to monitor
        optimizer: The optimizer used for training
        dataloader: The dataloader used for training
        device: The device the model is on (CPU or GPU)
        profilers: Dictionary of active profilers
        is_watching: Whether monitoring is active
        config: Configuration dictionary
    """
    
    def __init__(
        self,
        model: Optional[torch.nn.Module] = None,
        optimizer: Optional[Optimizer] = None,
        dataloader: Optional[DataLoader] = None,
        device: Optional[Union[str, torch.device]] = None,
        config: Optional[Dict[str, Any]] = None,
    ):
        """
        Initialize the Doctor.
        
        Args:
            model: The PyTorch model to monitor
            optimizer: The optimizer used for training
            dataloader: The dataloader used for training
            device: The device the model is on (CPU or GPU)
            config: Configuration dictionary
        """
        self.model = model
        self.optimizer = optimizer
        self.dataloader = dataloader
        self.device = device or (
            next(model.parameters()).device if model is not None else torch.device("cpu")
        )
        self.config = config or {}
        self.profilers = {}
        self.is_watching = False
        self.suggestions = []
        self.history = []
        
        # Initialize profilers if components are provided
        if model is not None:
            self._init_profilers()
        
        logger.info("AutoPipelineDoctor initialized")
    
    def _init_profilers(self):
        """Initialize all profilers."""
        self.profilers["hardware"] = HardwareProfiler(self.device)
        self.profilers["memory"] = MemoryProfiler(self.model, self.device)
        self.profilers["timing"] = TimingProfiler()
        
        if self.dataloader is not None:
            self.profilers["dataloader"] = DataloaderProfiler(self.dataloader)
        
        if self.model is not None and self.optimizer is not None:
            self.profilers["gradient"] = GradientProfiler(self.model)
    
    def attach(
        self,
        model: Optional[torch.nn.Module] = None,
        optimizer: Optional[Optimizer] = None,
        dataloader: Optional[DataLoader] = None,
    ):
        """
        Attach the Doctor to model, optimizer, and dataloader.
        
        Args:
            model: The PyTorch model to monitor
            optimizer: The optimizer used for training
            dataloader: The dataloader used for training
        """
        if model is not None:
            self.model = model
            self.device = next(model.parameters()).device
        
        if optimizer is not None:
            self.optimizer = optimizer
        
        if dataloader is not None:
            self.dataloader = dataloader
        
        self._init_profilers()
        logger.info("Components attached to Doctor")
        return self
    
    def watch(self, train_loop: Optional[Callable] = None):
        """
        Start monitoring the training process.
        
        Args:
            train_loop: Optional function to wrap and monitor
        
        Returns:
            The wrapped train_loop function if provided, otherwise self
        """
        self.is_watching = True
        
        # Start all profilers
        for name, profiler in self.profilers.items():
            profiler.start()
        
        logger.info("Doctor is now watching")
        
        if train_loop is not None:
            # Wrap the train loop function to monitor it
            def wrapped_train_loop(*args, **kwargs):
                self.profilers["timing"].start_timer("train_loop")
                result = train_loop(*args, **kwargs)
                self.profilers["timing"].stop_timer("train_loop")
                return result
            
            return wrapped_train_loop
        
        return self
    
    def stop(self):
        """Stop monitoring the training process."""
        if not self.is_watching:
            logger.warning("Doctor is not watching, nothing to stop")
            return self
        
        # Stop all profilers
        for name, profiler in self.profilers.items():
            profiler.stop()
        
        self.is_watching = False
        logger.info("Doctor has stopped watching")
        return self
    
    def get_metrics(self) -> Dict[str, Any]:
        """
        Get current metrics from all profilers.
        
        Returns:
            Dictionary of metrics from all profilers
        """
        metrics = {}
        for name, profiler in self.profilers.items():
            metrics[name] = profiler.get_metrics()
        
        return metrics
    
    def get_suggestions(self) -> List[Dict[str, Any]]:
        """
        Get optimization suggestions.
        
        Returns:
            List of optimization suggestions
        """
        # This will be implemented in the suggestion engine module
        # For now, return placeholder suggestions
        return [
            {
                "type": "dataloader",
                "severity": "medium",
                "message": "Consider increasing num_workers in DataLoader",
                "details": "DataLoader is a bottleneck. Increasing num_workers may improve performance.",
                "code": "dataloader = torch.utils.data.DataLoader(..., num_workers=8, ...)",
            }
        ]
    
    def auto_optimize(self) -> bool:
        """
        Automatically apply optimization suggestions.
        
        Returns:
            True if optimizations were applied, False otherwise
        """
        # This will be implemented in the optimization advisor module
        # For now, return placeholder
        return False
    
    def explain(self, query: str) -> str:
        """
        Explain aspects of the training process in natural language.
        
        Args:
            query: The question to answer
        
        Returns:
            Natural language explanation
        """
        # This will be implemented in the LLM interface module
        # For now, return placeholder
        return f"I'll answer your question about '{query}' when the LLM interface is implemented."
    
    def auto_patch(self):
        """
        Automatically patch the training process for monitoring.
        
        This method uses monkey patching to intercept and monitor
        key functions in the training process.
        """
        # This will be implemented in the core module
        # For now, just log a message
        logger.info("Auto-patching will be implemented in a future version")
        return self
    
    def generate_report(self) -> str:
        """
        Generate a comprehensive report of the training process.
        
        Returns:
            Markdown formatted report
        """
        # This will be implemented in the visualization module
        # For now, return placeholder
        metrics = self.get_metrics()
        report = "# AutoPipelineDoctor Report\n\n"
        
        for profiler_name, profiler_metrics in metrics.items():
            report += f"## {profiler_name.capitalize()} Metrics\n\n"
            for metric_name, metric_value in profiler_metrics.items():
                report += f"- **{metric_name}**: {metric_value}\n"
            report += "\n"
        
        return report
    
    def __repr__(self) -> str:
        """String representation of the Doctor."""
        status = "watching" if self.is_watching else "not watching"
        device = self.device
        profilers = list(self.profilers.keys())
        return f"Doctor(status={status}, device={device}, profilers={profilers})"
