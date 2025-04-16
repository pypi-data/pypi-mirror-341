"""
Timing profiler for monitoring execution times.

This module provides functionality to monitor execution times of various
operations during model training, including forward pass, backward pass,
optimizer step, and data loading.
"""

import logging
import time
from typing import Dict, Any, Optional, List, Tuple

import torch

logger = logging.getLogger(__name__)

class TimingProfiler:
    """
    Profiler for monitoring execution times.
    
    This class tracks execution times of various operations during model training.
    
    Attributes:
        is_profiling: Whether profiling is active
        metrics: Dictionary of collected metrics
        timers: Dictionary of active timers
        history: Dictionary of historical timing data
    """
    
    def __init__(self):
        """Initialize the timing profiler."""
        self.is_profiling = False
        self.metrics = {
            "forward_time": 0.0,
            "backward_time": 0.0,
            "optimizer_time": 0.0,
            "dataloader_time": 0.0,
            "total_time": 0.0,
            "iterations": 0,
            "iterations_per_second": 0.0,
        }
        self.timers = {}
        self.history = {
            "forward_time": [],
            "backward_time": [],
            "optimizer_time": [],
            "dataloader_time": [],
            "total_time": [],
        }
        self.start_time = None
    
    def start(self):
        """Start profiling execution times."""
        self.is_profiling = True
        self.start_time = time.time()
        logger.info("Timing profiling started")
        return self
    
    def stop(self):
        """Stop profiling execution times."""
        self.is_profiling = False
        logger.info("Timing profiling stopped")
        return self
    
    def start_timer(self, name: str):
        """
        Start a timer with the given name.
        
        Args:
            name: Name of the timer
        """
        if not self.is_profiling:
            return
        
        self.timers[name] = time.time()
    
    def stop_timer(self, name: str):
        """
        Stop a timer with the given name and record the elapsed time.
        
        Args:
            name: Name of the timer
        
        Returns:
            Elapsed time in seconds
        """
        if not self.is_profiling or name not in self.timers:
            return 0.0
        
        elapsed = time.time() - self.timers[name]
        
        # Update metrics based on timer name
        if name == "forward":
            self.metrics["forward_time"] = elapsed
            self.history["forward_time"].append(elapsed)
        elif name == "backward":
            self.metrics["backward_time"] = elapsed
            self.history["backward_time"].append(elapsed)
        elif name == "optimizer":
            self.metrics["optimizer_time"] = elapsed
            self.history["optimizer_time"].append(elapsed)
        elif name == "dataloader":
            self.metrics["dataloader_time"] = elapsed
            self.history["dataloader_time"].append(elapsed)
        elif name == "iteration":
            self.metrics["total_time"] = elapsed
            self.history["total_time"].append(elapsed)
            self.metrics["iterations"] += 1
            
            # Calculate iterations per second
            if self.start_time is not None:
                total_time = time.time() - self.start_time
                self.metrics["iterations_per_second"] = self.metrics["iterations"] / total_time
        
        # Remove the timer
        del self.timers[name]
        
        return elapsed
    
    def get_metrics(self) -> Dict[str, Any]:
        """
        Get current timing metrics.
        
        Returns:
            Dictionary of timing metrics
        """
        return self.metrics.copy()
    
    def get_history(self) -> Dict[str, List[float]]:
        """
        Get historical timing data.
        
        Returns:
            Dictionary of historical timing data
        """
        return self.history.copy()
    
    def get_bottlenecks(self) -> List[Tuple[str, float]]:
        """
        Identify timing bottlenecks.
        
        Returns:
            List of (operation_name, time_percentage) tuples, sorted by percentage
        """
        if self.metrics["total_time"] == 0:
            return []
        
        bottlenecks = []
        total = self.metrics["total_time"]
        
        bottlenecks.append(("forward", self.metrics["forward_time"] / total))
        bottlenecks.append(("backward", self.metrics["backward_time"] / total))
        bottlenecks.append(("optimizer", self.metrics["optimizer_time"] / total))
        bottlenecks.append(("dataloader", self.metrics["dataloader_time"] / total))
        
        # Calculate "other" time
        accounted_time = (
            self.metrics["forward_time"] +
            self.metrics["backward_time"] +
            self.metrics["optimizer_time"] +
            self.metrics["dataloader_time"]
        )
        other_time = max(0, total - accounted_time)
        bottlenecks.append(("other", other_time / total))
        
        # Sort by percentage (descending)
        bottlenecks.sort(key=lambda x: x[1], reverse=True)
        
        return bottlenecks
    
    def __repr__(self) -> str:
        """String representation of the timing profiler."""
        status = "profiling" if self.is_profiling else "not profiling"
        iterations = self.metrics["iterations"]
        return f"TimingProfiler(status={status}, iterations={iterations})"
