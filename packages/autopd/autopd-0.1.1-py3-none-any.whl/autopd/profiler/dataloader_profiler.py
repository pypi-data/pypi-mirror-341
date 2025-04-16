"""
Dataloader profiler for monitoring dataloader performance.

This module provides functionality to monitor PyTorch dataloader performance,
including loading times, worker utilization, and batch processing times.
"""

import logging
import time
from typing import Dict, Any, Optional, List, Tuple
from collections import deque

import torch
from torch.utils.data import DataLoader

logger = logging.getLogger(__name__)

class DataloaderProfiler:
    """
    Profiler for monitoring dataloader performance.
    
    This class tracks dataloader performance metrics including loading times,
    worker utilization, and batch processing times.
    
    Attributes:
        dataloader: The PyTorch dataloader to monitor
        is_profiling: Whether profiling is active
        metrics: Dictionary of collected metrics
        batch_times: Deque of recent batch loading times
    """
    
    def __init__(self, dataloader: Optional[DataLoader] = None):
        """
        Initialize the dataloader profiler.
        
        Args:
            dataloader: The PyTorch dataloader to monitor
        """
        self.dataloader = dataloader
        self.is_profiling = False
        self.metrics = {
            "avg_batch_time": 0.0,
            "min_batch_time": 0.0,
            "max_batch_time": 0.0,
            "std_batch_time": 0.0,
            "num_workers": 0,
            "batch_size": 0,
            "dataset_size": 0,
            "worker_utilization": 0.0,
            "estimated_optimal_workers": 0,
        }
        self.batch_times = deque(maxlen=100)  # Store last 100 batch times
        self.last_batch_time = None
        
        if dataloader is not None:
            self._init_dataloader_metrics()
    
    def _init_dataloader_metrics(self):
        """Initialize dataloader-specific metrics."""
        if self.dataloader is None:
            return
        
        # Get dataloader properties
        self.metrics["num_workers"] = getattr(self.dataloader, "num_workers", 0)
        self.metrics["batch_size"] = getattr(self.dataloader, "batch_size", 1)
        
        # Get dataset size
        dataset_size = 0
        if hasattr(self.dataloader, "dataset"):
            dataset_size = len(self.dataloader.dataset)
        self.metrics["dataset_size"] = dataset_size
    
    def start(self):
        """Start profiling dataloader performance."""
        self.is_profiling = True
        self.last_batch_time = time.time()
        logger.info("Dataloader profiling started")
        return self
    
    def stop(self):
        """Stop profiling dataloader performance."""
        self.is_profiling = False
        logger.info("Dataloader profiling stopped")
        return self
    
    def batch_loaded(self):
        """
        Record that a batch has been loaded.
        
        This should be called after each batch is loaded from the dataloader.
        """
        if not self.is_profiling or self.last_batch_time is None:
            self.last_batch_time = time.time()
            return
        
        current_time = time.time()
        batch_time = current_time - self.last_batch_time
        self.last_batch_time = current_time
        
        # Add to batch times
        self.batch_times.append(batch_time)
        
        # Update metrics
        self._update_batch_metrics()
    
    def _update_batch_metrics(self):
        """Update batch-related metrics."""
        if not self.batch_times:
            return
        
        import numpy as np
        
        # Calculate statistics
        batch_times = np.array(self.batch_times)
        self.metrics["avg_batch_time"] = np.mean(batch_times)
        self.metrics["min_batch_time"] = np.min(batch_times)
        self.metrics["max_batch_time"] = np.max(batch_times)
        self.metrics["std_batch_time"] = np.std(batch_times)
        
        # Estimate worker utilization
        if self.metrics["num_workers"] > 0:
            # Simplified model: if batch loading is fast, workers are underutilized
            # If batch loading is slow, workers are overutilized
            cpu_count = torch.multiprocessing.cpu_count()
            
            # Estimate time per sample
            time_per_sample = self.metrics["avg_batch_time"] / self.metrics["batch_size"]
            
            # Estimate optimal number of workers
            # This is a heuristic: we assume linear scaling with number of workers
            current_workers = max(1, self.metrics["num_workers"])
            
            # Target batch time (heuristic: 10ms per sample is a good target)
            target_time_per_sample = 0.01  # 10ms
            
            if time_per_sample > 0:
                optimal_workers = int(current_workers * (time_per_sample / target_time_per_sample))
                # Clamp to reasonable values
                optimal_workers = max(1, min(cpu_count, optimal_workers))
                self.metrics["estimated_optimal_workers"] = optimal_workers
            
            # Calculate utilization
            if current_workers > 0:
                # If we need more workers, utilization is high
                if self.metrics["estimated_optimal_workers"] > current_workers:
                    self.metrics["worker_utilization"] = 1.0
                else:
                    # If we need fewer workers, utilization is proportional
                    self.metrics["worker_utilization"] = min(
                        1.0, self.metrics["estimated_optimal_workers"] / current_workers
                    )
    
    def get_metrics(self) -> Dict[str, Any]:
        """
        Get current dataloader metrics.
        
        Returns:
            Dictionary of dataloader metrics
        """
        return self.metrics.copy()
    
    def get_optimization_suggestions(self) -> List[Dict[str, Any]]:
        """
        Get optimization suggestions for the dataloader.
        
        Returns:
            List of optimization suggestions
        """
        suggestions = []
        
        if not self.is_profiling or not self.batch_times:
            return suggestions
        
        # Check if we need more workers
        if (self.metrics["estimated_optimal_workers"] > self.metrics["num_workers"] and
            self.metrics["worker_utilization"] > 0.9):
            suggestions.append({
                "type": "dataloader_workers",
                "severity": "medium",
                "message": f"Consider increasing num_workers from {self.metrics['num_workers']} to {self.metrics['estimated_optimal_workers']}",
                "details": "DataLoader workers are fully utilized. Increasing num_workers may improve performance.",
                "code": f"dataloader = torch.utils.data.DataLoader(..., num_workers={self.metrics['estimated_optimal_workers']}, ...)",
            })
        
        # Check if we have too many workers
        elif (self.metrics["estimated_optimal_workers"] < self.metrics["num_workers"] * 0.5 and
              self.metrics["num_workers"] > 1):
            suggested_workers = max(1, self.metrics["estimated_optimal_workers"])
            suggestions.append({
                "type": "dataloader_workers",
                "severity": "low",
                "message": f"Consider decreasing num_workers from {self.metrics['num_workers']} to {suggested_workers}",
                "details": "DataLoader workers are underutilized. Decreasing num_workers may free up resources.",
                "code": f"dataloader = torch.utils.data.DataLoader(..., num_workers={suggested_workers}, ...)",
            })
        
        # Check if batch size could be increased
        if self.metrics["avg_batch_time"] < 0.05:  # Very fast batch loading
            suggested_batch_size = self.metrics["batch_size"] * 2
            suggestions.append({
                "type": "batch_size",
                "severity": "low",
                "message": f"Consider increasing batch_size from {self.metrics['batch_size']} to {suggested_batch_size}",
                "details": "Batch loading is very fast. Increasing batch_size may improve throughput.",
                "code": f"dataloader = torch.utils.data.DataLoader(..., batch_size={suggested_batch_size}, ...)",
            })
        
        return suggestions
    
    def __repr__(self) -> str:
        """String representation of the dataloader profiler."""
        status = "profiling" if self.is_profiling else "not profiling"
        workers = self.metrics["num_workers"]
        batch_size = self.metrics["batch_size"]
        return f"DataloaderProfiler(status={status}, workers={workers}, batch_size={batch_size})"
