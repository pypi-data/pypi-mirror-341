"""
Predictive failure forecasting module for AutoPipelineDoctor.

This module provides functionality to predict training failures before they happen,
including OOM errors, overfitting/underfitting, and gradient issues.
"""

import logging
from typing import Dict, Any, Optional, List, Tuple, Union
import time
import numpy as np
from collections import deque

import torch

from autopd.profiler.memory_profiler import MemoryProfiler
from autopd.profiler.gradient_profiler import GradientProfiler

logger = logging.getLogger(__name__)

class OOMPredictor:
    """
    Predictor for Out-of-Memory (OOM) errors.
    
    This class predicts OOM errors before they happen by analyzing memory usage
    patterns and growth rates during training.
    
    Attributes:
        memory_profiler: The memory profiler to use for predictions
        device: The device being monitored
        is_active: Whether prediction is active
        metrics: Dictionary of prediction metrics
        memory_history: Deque of recent memory usage
        warning_threshold: Threshold for warning level (0.0-1.0)
        critical_threshold: Threshold for critical level (0.0-1.0)
    """
    
    def __init__(
        self,
        memory_profiler: Optional[MemoryProfiler] = None,
        device: Optional[Union[str, torch.device]] = None,
        warning_threshold: float = 0.7,
        critical_threshold: float = 0.9,
    ):
        """
        Initialize the OOM predictor.
        
        Args:
            memory_profiler: The memory profiler to use for predictions
            device: The device being monitored
            warning_threshold: Threshold for warning level (0.0-1.0)
            critical_threshold: Threshold for critical level (0.0-1.0)
        """
        self.memory_profiler = memory_profiler
        self.device = device or torch.device("cpu")
        self.is_active = False
        self.metrics = {
            "oom_risk": 0.0,
            "estimated_iterations_to_oom": float('inf'),
            "memory_growth_rate": 0.0,
            "available_memory": 0.0,
            "total_memory": 0.0,
            "risk_level": "low",
        }
        self.memory_history = deque(maxlen=100)  # Store last 100 memory readings
        self.warning_threshold = warning_threshold
        self.critical_threshold = critical_threshold
        self.last_update_time = None
    
    def start(self):
        """Start OOM prediction."""
        self.is_active = True
        self.last_update_time = time.time()
        logger.info("OOM prediction started")
        return self
    
    def stop(self):
        """Stop OOM prediction."""
        self.is_active = False
        logger.info("OOM prediction stopped")
        return self
    
    def update(self):
        """
        Update OOM prediction metrics.
        
        This should be called periodically during training.
        """
        if not self.is_active or self.memory_profiler is None:
            return
        
        # Get current memory metrics
        memory_metrics = self.memory_profiler.get_metrics()
        
        # Add to memory history
        self.memory_history.append(memory_metrics["allocated_memory"])
        
        # Update prediction metrics
        self._update_prediction_metrics(memory_metrics)
        
        # Update last update time
        self.last_update_time = time.time()
    
    def _update_prediction_metrics(self, memory_metrics: Dict[str, Any]):
        """
        Update prediction metrics based on memory metrics.
        
        Args:
            memory_metrics: Memory metrics from the memory profiler
        """
        # Get device properties
        if self.device.type == "cuda" and torch.cuda.is_available():
            total_memory = torch.cuda.get_device_properties(self.device).total_memory / (1024 * 1024)  # MB
        else:
            # For CPU, use system memory
            import psutil
            total_memory = psutil.virtual_memory().total / (1024 * 1024)  # MB
        
        # Calculate available memory
        available_memory = total_memory - memory_metrics["reserved_memory"]
        
        # Calculate memory growth rate
        memory_growth_rate = 0.0
        if len(self.memory_history) >= 2:
            # Use linear regression to estimate growth rate
            x = np.arange(len(self.memory_history))
            y = np.array(self.memory_history)
            
            if len(x) > 1:  # Need at least 2 points for regression
                A = np.vstack([x, np.ones(len(x))]).T
                m, c = np.linalg.lstsq(A, y, rcond=None)[0]
                memory_growth_rate = m  # MB per iteration
        
        # Estimate iterations to OOM
        iterations_to_oom = float('inf')
        if memory_growth_rate > 0:
            iterations_to_oom = available_memory / memory_growth_rate
        
        # Calculate OOM risk
        # Base risk on memory usage percentage and growth rate
        memory_usage_pct = memory_metrics["reserved_memory"] / total_memory
        growth_factor = min(1.0, memory_growth_rate / 10.0)  # Normalize growth rate
        
        # Combine factors with weights
        oom_risk = (memory_usage_pct * 0.7) + (growth_factor * 0.3)
        
        # Determine risk level
        risk_level = "low"
        if oom_risk >= self.critical_threshold:
            risk_level = "critical"
        elif oom_risk >= self.warning_threshold:
            risk_level = "warning"
        
        # Update metrics
        self.metrics["oom_risk"] = oom_risk
        self.metrics["estimated_iterations_to_oom"] = iterations_to_oom
        self.metrics["memory_growth_rate"] = memory_growth_rate
        self.metrics["available_memory"] = available_memory
        self.metrics["total_memory"] = total_memory
        self.metrics["risk_level"] = risk_level
    
    def get_metrics(self) -> Dict[str, Any]:
        """
        Get current prediction metrics.
        
        Returns:
            Dictionary of prediction metrics
        """
        return self.metrics.copy()
    
    def get_warnings(self) -> List[Dict[str, Any]]:
        """
        Get OOM warnings.
        
        Returns:
            List of warning dictionaries
        """
        warnings = []
        
        if not self.is_active:
            return warnings
        
        # Check for critical risk
        if self.metrics["risk_level"] == "critical":
            warnings.append({
                "type": "oom",
                "severity": "critical",
                "message": f"Critical OOM risk detected (risk: {self.metrics['oom_risk']:.2f})",
                "details": f"Estimated iterations to OOM: {int(self.metrics['estimated_iterations_to_oom'])}. "
                          f"Memory growth rate: {self.metrics['memory_growth_rate']:.2f} MB/iteration.",
                "suggestions": [
                    "Reduce batch size",
                    "Enable gradient checkpointing",
                    "Use mixed precision training",
                    "Offload optimizer state to CPU",
                    "Free unused memory with torch.cuda.empty_cache()",
                ],
            })
        
        # Check for warning risk
        elif self.metrics["risk_level"] == "warning":
            warnings.append({
                "type": "oom",
                "severity": "warning",
                "message": f"OOM risk detected (risk: {self.metrics['oom_risk']:.2f})",
                "details": f"Estimated iterations to OOM: {int(self.metrics['estimated_iterations_to_oom'])}. "
                          f"Memory growth rate: {self.metrics['memory_growth_rate']:.2f} MB/iteration.",
                "suggestions": [
                    "Monitor memory usage closely",
                    "Consider reducing batch size",
                    "Consider enabling gradient checkpointing",
                    "Consider using mixed precision training",
                ],
            })
        
        return warnings
    
    def __repr__(self) -> str:
        """String representation of the OOM predictor."""
        status = "active" if self.is_active else "inactive"
        risk = self.metrics["risk_level"]
        return f"OOMPredictor(status={status}, risk_level={risk})"


class FittingPredictor:
    """
    Predictor for overfitting and underfitting.
    
    This class predicts overfitting and underfitting by analyzing training
    and validation metrics during training.
    
    Attributes:
        is_active: Whether prediction is active
        metrics: Dictionary of prediction metrics
        train_losses: Deque of recent training losses
        val_losses: Deque of recent validation losses
        warning_threshold: Threshold for warning level
    """
    
    def __init__(self, warning_threshold: float = 0.1):
        """
        Initialize the fitting predictor.
        
        Args:
            warning_threshold: Threshold for warning level
        """
        self.is_active = False
        self.metrics = {
            "overfitting_risk": 0.0,
            "underfitting_risk": 0.0,
            "train_val_gap": 0.0,
            "train_loss_trend": 0.0,
            "val_loss_trend": 0.0,
            "epochs_since_val_improvement": 0,
            "risk_level": "low",
        }
        self.train_losses = deque(maxlen=100)
        self.val_losses = deque(maxlen=100)
        self.warning_threshold = warning_threshold
        self.best_val_loss = float('inf')
        self.epochs_without_improvement = 0
    
    def start(self):
        """Start fitting prediction."""
        self.is_active = True
        logger.info("Fitting prediction started")
        return self
    
    def stop(self):
        """Stop fitting prediction."""
        self.is_active = False
        logger.info("Fitting prediction stopped")
        return self
    
    def update(self, train_loss: float, val_loss: Optional[float] = None):
        """
        Update fitting prediction metrics.
        
        This should be called after each epoch with the training and validation losses.
        
        Args:
            train_loss: Training loss for the current epoch
            val_loss: Validation loss for the current epoch (if available)
        """
        if not self.is_active:
            return
        
        # Add to loss history
        self.train_losses.append(train_loss)
        
        if val_loss is not None:
            self.val_losses.append(val_loss)
            
            # Check for validation improvement
            if val_loss < self.best_val_loss:
                self.best_val_loss = val_loss
                self.epochs_without_improvement = 0
            else:
                self.epochs_without_improvement += 1
        
        # Update prediction metrics
        self._update_prediction_metrics()
    
    def _update_prediction_metrics(self):
        """Update prediction metrics based on loss history."""
        # Calculate train-val gap
        train_val_gap = 0.0
        if self.train_losses and self.val_losses:
            train_val_gap = self.val_losses[-1] - self.train_losses[-1]
        
        # Calculate loss trends using linear regression
        train_loss_trend = 0.0
        val_loss_trend = 0.0
        
        if len(self.train_losses) >= 5:
            x = np.arange(len(self.train_losses))
            y = np.array(self.train_losses)
            A = np.vstack([x, np.ones(len(x))]).T
            m, c = np.linalg.lstsq(A, y, rcond=None)[0]
            train_loss_trend = m
        
        if len(self.val_losses) >= 5:
            x = np.arange(len(self.val_losses))
            y = np.array(self.val_losses)
            A = np.vstack([x, np.ones(len(x))]).T
            m, c = np.linalg.lstsq(A, y, rcond=None)[0]
            val_loss_trend = m
        
        # Calculate overfitting risk
        # Overfitting: train loss decreasing, val loss increasing, large gap
        overfitting_risk = 0.0
        if train_loss_trend < 0 and val_loss_trend > 0:
            # Clear sign of overfitting
            overfitting_risk = 0.8
        elif train_loss_trend < 0 and val_loss_trend < 0 and train_loss_trend < val_loss_trend:
            # Train improving faster than val
            overfitting_risk = 0.5
        elif train_val_gap > self.warning_threshold:
            # Large gap between train and val
            overfitting_risk = 0.7
        elif self.epochs_without_improvement >= 3:
            # No val improvement for several epochs
            overfitting_risk = 0.6
        
        # Calculate underfitting risk
        # Underfitting: both losses high, both decreasing very slowly or flat
        underfitting_risk = 0.0
        if abs(train_loss_trend) < 0.001 and len(self.train_losses) >= 5:
            # Training loss plateaued
            underfitting_risk = 0.7
        elif train_loss_trend > 0:
            # Training loss increasing
            underfitting_risk = 0.8
        
        # Determine risk level
        risk_level = "low"
        if overfitting_risk >= 0.7 or underfitting_risk >= 0.7:
            risk_level = "high"
        elif overfitting_risk >= 0.5 or underfitting_risk >= 0.5:
            risk_level = "medium"
        
        # Update metrics
        self.metrics["overfitting_risk"] = overfitting_risk
        self.metrics["underfitting_risk"] = underfitting_risk
        self.metrics["train_val_gap"] = train_val_gap
        self.metrics["train_loss_trend"] = train_loss_trend
        self.metrics["val_loss_trend"] = val_loss_trend
        self.metrics["epochs_since_val_improvement"] = self.epochs_without_improvement
        self.metrics["risk_level"] = risk_level
    
    def get_metrics(self) -> Dict[str, Any]:
        """
        Get current prediction metrics.
        
        Returns:
            Dictionary of prediction metrics
        """
        return self.metrics.copy()
    
    def get_warnings(self) -> List[Dict[str, Any]]:
        """
        Get fitting warnings.
        
        Returns:
            List of warning dictionaries
        """
        warnings = []
        
        if not self.is_active:
            return warnings
        
        # Check for overfitting
        if self.metrics["overfitting_risk"] >= 0.7:
            warnings.append({
                "type": "overfitting",
                "severity": "high",
                "message": f"Overfitting detected (risk: {self.metrics['overfitting_risk']:.2f})",
                "details": f"Train-val gap: {self.metrics['train_val_gap']:.4f}, "
                          f"Epochs without improvement: {self.metrics['epochs_since_val_improvement']}",
                "suggestions": [
                    "Add regularization (L1/L2)",
                    "Use dropout",
                    "Reduce model complexity",
                    "Increase training data",
                    "Use early stopping",
                    "Use data augmentation",
                ],
            })
        elif self.metrics["overfitting_risk"] >= 0.5:
            warnings.append({
                "type": "overfitting",
                "severity": "medium",
                "message": f"Potential overfitting detected (risk: {self.metrics['overfitting_risk']:.2f})",
                "details": f"Train-val gap: {self.metrics['train_val_gap']:.4f}, "
                          f"Epochs without improvement: {self.metrics['epochs_since_val_improvement']}",
                "suggestions": [
                    "Monitor validation metrics closely",
                    "Consider adding regularization",
                    "Consider using early stopping",
                ],
            })
        
        # Check for underfitting
        if self.metrics["underfitting_risk"] >= 0.7:
            warnings.append({
                "type": "underfitting",
                "severity": "high",
                "message": f"Underfitting detected (risk: {self.metrics['underfitting_risk']:.2f})",
                "details": f"Train loss trend: {self.metrics['train_loss_trend']:.6f}",
                "suggestions": [
                    "Increase model complexity",
                    "Train for more epochs",
                    "Increase learning rate",
                    "Remove excessive regularization",
                    "Check for data issues",
                ],
            })
        elif self.metrics["underfitting_risk"] >= 0.5:
            warnings.append({
                "type": "underfitting",
                "severity": "medium",
                "message": f"Potential underfitting detected (risk: {self.metrics['underfitting_risk']:.2f})",
                "details": f"Train loss trend: {self.metrics['train_loss_trend']:.6f}",
                "suggestions": [
                    "Continue training for more epochs",
                    "Consider increasing model complexity",
                    "Consider adjusting learning rate",
                ],
            })
        
        return warnings
    
    def __repr__(self) -> str:
        """String representation of the fitting predictor."""
        status = "active" if self.is_active else "inactive"
        return f"FittingPredictor(status={status})"


class GradientIssuePredictor:
    """
    Predictor for gradient-related issues.
    
    This class predicts gradient-related issues such as vanishing or exploding
    gradients by analyzing gradient statistics during training.
    
    Attributes:
        gradient_profiler: The gradient profiler to use for predictions
        is_active: Whether prediction is active
        metrics: Dictionary of prediction metrics
        warning_threshold: Threshold for warning level
    """
    
    def __init__(
        self,
        gradient_profiler: Optional[GradientProfiler] = None,
        warning_threshold: float = 0.5,
    ):
        """
        Initialize the gradient issue predictor.
        
        Args:
            gradient_profiler: The gradient profiler to use for predictions
            warning_threshold: Threshold for warning level
        """
        self.gradient_profiler = gradient_profiler
        self.is_active = False
        self.metrics = {
            "vanishing_gradient_risk": 0.0,
            "exploding_gradient_risk": 0.0,
            "dead_gradient_pct": 0.0,
            "large_gradient_pct": 0.0,
            "risk_level": "low",
        }
        self.warning_threshold = warning_threshold
    
    def start(self):
        """Start gradient issue prediction."""
        self.is_active = True
        logger.info("Gradient issue prediction started")
        return self
    
    def stop(self):
        """Stop gradient issue prediction."""
        self.is_active = False
        logger.info("Gradient issue prediction stopped")
        return self
    
    def update(self):
        """
        Update gradient issue prediction metrics.
        
        This should be called periodically during training.
        """
        if not self.is_active or self.gradient_profiler is None:
            return
        
        # Get current gradient metrics
        gradient_metrics = self.gradient_profiler.get_metrics()
        
        # Update prediction metrics
        self._update_prediction_metrics(gradient_metrics)
    
    def _update_prediction_metrics(self, gradient_metrics: Dict[str, Any]):
        """
        Update prediction metrics based on gradient metrics.
        
        Args:
            gradient_metrics: Gradient metrics from the gradient profiler
        """
        # Extract relevant metrics
        dead_gradient_pct = gradient_metrics.get("dead_gradients_pct", 0.0)
        exploding_gradient_pct = gradient_metrics.get("exploding_gradients_pct", 0.0)
        
        # Calculate vanishing gradient risk
        vanishing_gradient_risk = min(1.0, dead_gradient_pct / 100.0)
        
        # Calculate exploding gradient risk
        exploding_gradient_risk = min(1.0, exploding_gradient_pct / 50.0)
        
        # Determine risk level
        risk_level = "low"
        if vanishing_gradient_risk >= self.warning_threshold or exploding_gradient_risk >= self.warning_threshold:
            risk_level = "high"
        elif vanishing_gradient_risk >= self.warning_threshold / 2 or exploding_gradient_risk >= self.warning_threshold / 2:
            risk_level = "medium"
        
        # Update metrics
        self.metrics["vanishing_gradient_risk"] = vanishing_gradient_risk
        self.metrics["exploding_gradient_risk"] = exploding_gradient_risk
        self.metrics["dead_gradient_pct"] = dead_gradient_pct
        self.metrics["large_gradient_pct"] = exploding_gradient_pct
        self.metrics["risk_level"] = risk_level
    
    def get_metrics(self) -> Dict[str, Any]:
        """
        Get current prediction metrics.
        
        Returns:
            Dictionary of prediction metrics
        """
        return self.metrics.copy()
    
    def get_warnings(self) -> List[Dict[str, Any]]:
        """
        Get gradient issue warnings.
        
        Returns:
            List of warning dictionaries
        """
        warnings = []
        
        if not self.is_active:
            return warnings
        
        # Check for vanishing gradients
        if self.metrics["vanishing_gradient_risk"] >= self.warning_threshold:
            warnings.append({
                "type": "vanishing_gradients",
                "severity": "high",
                "message": f"Vanishing gradients detected (risk: {self.metrics['vanishing_gradient_risk']:.2f})",
                "details": f"Dead gradient percentage: {self.metrics['dead_gradient_pct']:.1f}%",
                "suggestions": [
                    "Use ReLU or Leaky ReLU activation functions",
                    "Use batch normalization",
                    "Use residual connections",
                    "Initialize weights properly",
                    "Use gradient clipping",
                ],
            })
        
        # Check for exploding gradients
        if self.metrics["exploding_gradient_risk"] >= self.warning_threshold:
            warnings.append({
                "type": "exploding_gradients",
                "severity": "high",
                "message": f"Exploding gradients detected (risk: {self.metrics['exploding_gradient_risk']:.2f})",
                "details": f"Large gradient percentage: {self.metrics['large_gradient_pct']:.1f}%",
                "suggestions": [
                    "Use gradient clipping",
                    "Reduce learning rate",
                    "Use batch normalization",
                    "Initialize weights properly",
                    "Use L2 regularization",
                ],
            })
        
        return warnings
    
    def __repr__(self) -> str:
        """String representation of the gradient issue predictor."""
        status = "active" if self.is_active else "inactive"
        return f"GradientIssuePredictor(status={status})"


class ScalingPredictor:
    """
    Predictor for compute/data scaling issues.
    
    This class predicts scaling issues such as imbalanced compute/data scaling
    by analyzing performance metrics during training.
    
    Attributes:
        is_active: Whether prediction is active
        metrics: Dictionary of prediction metrics
        batch_sizes: List of batch sizes used
        throughputs: List of throughputs (samples/second) for each batch size
    """
    
    def __init__(self):
        """Initialize the scaling predictor."""
        self.is_active = False
        self.metrics = {
            "scaling_efficiency": 1.0,
            "optimal_batch_size": 0,
            "current_batch_size": 0,
            "max_throughput": 0.0,
            "current_throughput": 0.0,
            "risk_level": "low",
        }
        self.batch_sizes = []
        self.throughputs = []
    
    def start(self):
        """Start scaling prediction."""
        self.is_active = True
        logger.info("Scaling prediction started")
        return self
    
    def stop(self):
        """Stop scaling prediction."""
        self.is_active = False
        logger.info("Scaling prediction stopped")
        return self
    
    def update(self, batch_size: int, samples_per_second: float):
        """
        Update scaling prediction metrics.
        
        This should be called periodically during training with the current
        batch size and throughput.
        
        Args:
            batch_size: Current batch size
            samples_per_second: Current throughput in samples per second
        """
        if not self.is_active:
            return
        
        # Check if we've seen this batch size before
        if batch_size in self.batch_sizes:
            # Update existing entry
            idx = self.batch_sizes.index(batch_size)
            # Use exponential moving average to update throughput
            alpha = 0.1
            self.throughputs[idx] = (1 - alpha) * self.throughputs[idx] + alpha * samples_per_second
        else:
            # Add new entry
            self.batch_sizes.append(batch_size)
            self.throughputs.append(samples_per_second)
        
        # Update prediction metrics
        self._update_prediction_metrics(batch_size, samples_per_second)
    
    def _update_prediction_metrics(self, current_batch_size: int, current_throughput: float):
        """
        Update prediction metrics based on current batch size and throughput.
        
        Args:
            current_batch_size: Current batch size
            current_throughput: Current throughput in samples per second
        """
        # Find max throughput and corresponding batch size
        max_throughput = max(self.throughputs) if self.throughputs else 0.0
        max_idx = self.throughputs.index(max_throughput) if self.throughputs else 0
        optimal_batch_size = self.batch_sizes[max_idx] if self.batch_sizes else 0
        
        # Calculate scaling efficiency
        scaling_efficiency = 1.0
        if max_throughput > 0:
            scaling_efficiency = current_throughput / max_throughput
        
        # Determine risk level
        risk_level = "low"
        if scaling_efficiency < 0.7:
            risk_level = "high"
        elif scaling_efficiency < 0.9:
            risk_level = "medium"
        
        # Update metrics
        self.metrics["scaling_efficiency"] = scaling_efficiency
        self.metrics["optimal_batch_size"] = optimal_batch_size
        self.metrics["current_batch_size"] = current_batch_size
        self.metrics["max_throughput"] = max_throughput
        self.metrics["current_throughput"] = current_throughput
        self.metrics["risk_level"] = risk_level
    
    def get_metrics(self) -> Dict[str, Any]:
        """
        Get current prediction metrics.
        
        Returns:
            Dictionary of prediction metrics
        """
        return self.metrics.copy()
    
    def get_warnings(self) -> List[Dict[str, Any]]:
        """
        Get scaling warnings.
        
        Returns:
            List of warning dictionaries
        """
        warnings = []
        
        if not self.is_active:
            return warnings
        
        # Check for scaling inefficiency
        if self.metrics["scaling_efficiency"] < 0.7:
            warnings.append({
                "type": "scaling_inefficiency",
                "severity": "high",
                "message": f"Scaling inefficiency detected (efficiency: {self.metrics['scaling_efficiency']:.2f})",
                "details": f"Current batch size: {self.metrics['current_batch_size']}, "
                          f"Optimal batch size: {self.metrics['optimal_batch_size']}, "
                          f"Current throughput: {self.metrics['current_throughput']:.1f} samples/s, "
                          f"Max throughput: {self.metrics['max_throughput']:.1f} samples/s",
                "suggestions": [
                    f"Change batch size to {self.metrics['optimal_batch_size']}",
                    "Optimize dataloader (increase num_workers)",
                    "Use mixed precision training",
                    "Check for CPU bottlenecks",
                ],
            })
        elif self.metrics["scaling_efficiency"] < 0.9:
            warnings.append({
                "type": "scaling_inefficiency",
                "severity": "medium",
                "message": f"Potential scaling inefficiency detected (efficiency: {self.metrics['scaling_efficiency']:.2f})",
                "details": f"Current batch size: {self.metrics['current_batch_size']}, "
                          f"Optimal batch size: {self.metrics['optimal_batch_size']}",
                "suggestions": [
                    f"Consider changing batch size to {self.metrics['optimal_batch_size']}",
                    "Monitor throughput with different batch sizes",
                ],
            })
        
        return warnings
    
    def __repr__(self) -> str:
        """String representation of the scaling predictor."""
        status = "active" if self.is_active else "inactive"
        return f"ScalingPredictor(status={status})"


class FailureForecaster:
    """
    Main forecaster for predicting training failures.
    
    This class orchestrates multiple predictors to forecast various types of
    training failures before they happen.
    
    Attributes:
        predictors: Dictionary of active predictors
        is_forecasting: Whether forecasting is active
    """
    
    def __init__(
        self,
        memory_profiler: Optional[MemoryProfiler] = None,
        gradient_profiler: Optional[GradientProfiler] = None,
        device: Optional[Union[str, torch.device]] = None,
    ):
        """
        Initialize the failure forecaster.
        
        Args:
            memory_profiler: Memory profiler to use for OOM prediction
            gradient_profiler: Gradient profiler to use for gradient issue prediction
            device: Device being monitored
        """
        self.device = device or torch.device("cpu")
        self.is_forecasting = False
        
        # Initialize predictors
        self.predictors = {
            "oom": OOMPredictor(memory_profiler, self.device),
            "fitting": FittingPredictor(),
            "gradient": GradientIssuePredictor(gradient_profiler),
            "scaling": ScalingPredictor(),
        }
    
    def start(self):
        """Start failure forecasting."""
        self.is_forecasting = True
        
        # Start all predictors
        for name, predictor in self.predictors.items():
            predictor.start()
        
        logger.info("Failure forecasting started")
        return self
    
    def stop(self):
        """Stop failure forecasting."""
        # Stop all predictors
        for name, predictor in self.predictors.items():
            predictor.stop()
        
        self.is_forecasting = False
        logger.info("Failure forecasting stopped")
        return self
    
    def update(self):
        """
        Update all predictors.
        
        This should be called periodically during training.
        """
        if not self.is_forecasting:
            return
        
        # Update OOM and gradient predictors
        self.predictors["oom"].update()
        self.predictors["gradient"].update()
    
    def update_fitting(self, train_loss: float, val_loss: Optional[float] = None):
        """
        Update fitting predictor.
        
        This should be called after each epoch with the training and validation losses.
        
        Args:
            train_loss: Training loss for the current epoch
            val_loss: Validation loss for the current epoch (if available)
        """
        if not self.is_forecasting:
            return
        
        self.predictors["fitting"].update(train_loss, val_loss)
    
    def update_scaling(self, batch_size: int, samples_per_second: float):
        """
        Update scaling predictor.
        
        This should be called periodically during training with the current
        batch size and throughput.
        
        Args:
            batch_size: Current batch size
            samples_per_second: Current throughput in samples per second
        """
        if not self.is_forecasting:
            return
        
        self.predictors["scaling"].update(batch_size, samples_per_second)
    
    def get_metrics(self) -> Dict[str, Dict[str, Any]]:
        """
        Get metrics from all predictors.
        
        Returns:
            Dictionary mapping predictor names to their metrics
        """
        metrics = {}
        
        for name, predictor in self.predictors.items():
            metrics[name] = predictor.get_metrics()
        
        return metrics
    
    def get_warnings(self) -> List[Dict[str, Any]]:
        """
        Get warnings from all predictors.
        
        Returns:
            List of warning dictionaries
        """
        warnings = []
        
        for name, predictor in self.predictors.items():
            warnings.extend(predictor.get_warnings())
        
        # Sort by severity
        severity_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
        warnings.sort(key=lambda w: severity_order.get(w.get("severity", "low"), 4))
        
        return warnings
    
    def __repr__(self) -> str:
        """String representation of the failure forecaster."""
        status = "forecasting" if self.is_forecasting else "not forecasting"
        return f"FailureForecaster(status={status})"
