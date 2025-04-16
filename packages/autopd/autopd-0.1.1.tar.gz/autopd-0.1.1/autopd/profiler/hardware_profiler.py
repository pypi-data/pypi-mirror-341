"""
Hardware profiler for monitoring CPU and GPU usage.

This module provides functionality to monitor hardware resources
including CPU, GPU, and memory usage during model training.
"""

import logging
import time
from typing import Dict, Any, Optional, Union

import psutil
import torch

# Conditionally import GPU monitoring tools
try:
    import pynvml
    PYNVML_AVAILABLE = True
except ImportError:
    PYNVML_AVAILABLE = False

try:
    import gputil
    GPUTIL_AVAILABLE = True
except ImportError:
    GPUTIL_AVAILABLE = False

logger = logging.getLogger(__name__)

class HardwareProfiler:
    """
    Profiler for monitoring hardware resources.
    
    This class monitors CPU, GPU, and memory usage during model training.
    
    Attributes:
        device: The device to monitor (CPU or GPU)
        is_profiling: Whether profiling is active
        metrics: Dictionary of collected metrics
        gpu_id: ID of the GPU to monitor (if applicable)
    """
    
    def __init__(self, device: Optional[Union[str, torch.device]] = None):
        """
        Initialize the hardware profiler.
        
        Args:
            device: The device to monitor (CPU or GPU)
        """
        self.device = device or torch.device("cpu")
        self.is_profiling = False
        self.metrics = {
            "cpu_percent": 0.0,
            "memory_percent": 0.0,
            "gpu_percent": 0.0,
            "gpu_memory_percent": 0.0,
            "gpu_temperature": 0.0,
        }
        self.gpu_id = None
        
        # Initialize GPU monitoring if on GPU
        if self.device.type == "cuda":
            if PYNVML_AVAILABLE:
                try:
                    pynvml.nvmlInit()
                    if isinstance(self.device, torch.device) and hasattr(self.device, "index"):
                        self.gpu_id = self.device.index
                    else:
                        # Try to get the default GPU
                        self.gpu_id = 0
                    logger.info(f"GPU monitoring initialized for GPU {self.gpu_id}")
                except Exception as e:
                    logger.warning(f"Failed to initialize NVML: {e}")
            elif GPUTIL_AVAILABLE:
                try:
                    # GPUtil uses a different indexing system, try to match it
                    gpus = gputil.getGPUs()
                    if gpus and isinstance(self.device, torch.device) and hasattr(self.device, "index"):
                        self.gpu_id = self.device.index
                    else:
                        self.gpu_id = 0
                    logger.info(f"GPU monitoring initialized using GPUtil for GPU {self.gpu_id}")
                except Exception as e:
                    logger.warning(f"Failed to initialize GPUtil: {e}")
            else:
                logger.warning("Neither pynvml nor gputil is available. GPU monitoring will be limited.")
    
    def start(self):
        """Start profiling hardware resources."""
        self.is_profiling = True
        logger.info("Hardware profiling started")
        return self
    
    def stop(self):
        """Stop profiling hardware resources."""
        self.is_profiling = False
        logger.info("Hardware profiling stopped")
        return self
    
    def _update_cpu_metrics(self):
        """Update CPU-related metrics."""
        self.metrics["cpu_percent"] = psutil.cpu_percent(interval=0.1)
        self.metrics["memory_percent"] = psutil.virtual_memory().percent
    
    def _update_gpu_metrics(self):
        """Update GPU-related metrics if on GPU."""
        if self.device.type != "cuda" or self.gpu_id is None:
            return
        
        if PYNVML_AVAILABLE:
            try:
                handle = pynvml.nvmlDeviceGetHandleByIndex(self.gpu_id)
                
                # Get GPU utilization
                utilization = pynvml.nvmlDeviceGetUtilizationRates(handle)
                self.metrics["gpu_percent"] = utilization.gpu
                
                # Get GPU memory
                memory_info = pynvml.nvmlDeviceGetMemoryInfo(handle)
                self.metrics["gpu_memory_percent"] = (memory_info.used / memory_info.total) * 100
                
                # Get GPU temperature
                self.metrics["gpu_temperature"] = pynvml.nvmlDeviceGetTemperature(
                    handle, pynvml.NVML_TEMPERATURE_GPU
                )
            except Exception as e:
                logger.warning(f"Failed to get GPU metrics with NVML: {e}")
        
        elif GPUTIL_AVAILABLE:
            try:
                gpus = gputil.getGPUs()
                if gpus and self.gpu_id < len(gpus):
                    gpu = gpus[self.gpu_id]
                    self.metrics["gpu_percent"] = gpu.load * 100
                    self.metrics["gpu_memory_percent"] = gpu.memoryUtil * 100
                    self.metrics["gpu_temperature"] = gpu.temperature
            except Exception as e:
                logger.warning(f"Failed to get GPU metrics with GPUtil: {e}")
    
    def get_metrics(self) -> Dict[str, Any]:
        """
        Get current hardware metrics.
        
        Returns:
            Dictionary of hardware metrics
        """
        if self.is_profiling:
            self._update_cpu_metrics()
            self._update_gpu_metrics()
        
        return self.metrics.copy()
    
    def __repr__(self) -> str:
        """String representation of the hardware profiler."""
        status = "profiling" if self.is_profiling else "not profiling"
        device = self.device
        return f"HardwareProfiler(status={status}, device={device})"
