"""
Profiler module for AutoPipelineDoctor.
"""

from typing import Dict, List, Optional, Any, Union
import logging
import time
import torch
import torch.nn as nn
import psutil
import os

logger = logging.getLogger(__name__)

class BaseProfiler:
    """Base class for all profilers."""
    
    def __init__(self):
        self.metrics = []
        self.running = False
    
    def start(self):
        """Start profiling."""
        self.running = True
        logger.debug(f"{self.__class__.__name__} started")
    
    def stop(self):
        """Stop profiling."""
        self.running = False
        logger.debug(f"{self.__class__.__name__} stopped")
    
    def get_metrics(self) -> List[Dict[str, Any]]:
        """Get collected metrics."""
        return self.metrics

class HardwareProfiler(BaseProfiler):
    """
    Profiles hardware usage during training.
    
    Monitors CPU, GPU, and memory usage.
    """
    
    def __init__(self, device: Optional[Union[str, torch.device]] = None):
        """
        Initialize the hardware profiler.
        
        Args:
            device: The device to monitor (e.g., 'cuda:0', 'cpu')
        """
        super().__init__()
        
        if device is None:
            self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        else:
            self.device = device if isinstance(device, torch.device) else torch.device(device)
        
        self.use_cuda = self.device.type == 'cuda'
        self.metrics = []
    
    def sample(self):
        """Sample current hardware metrics."""
        if not self.running:
            return
        
        # Get CPU metrics
        cpu_percent = psutil.cpu_percent(interval=0.1)
        memory_info = psutil.virtual_memory()
        
        # Create metrics dict
        metrics = {
            'timestamp': time.time(),
            'cpu_percent': cpu_percent,
            'memory_percent': memory_info.percent,
            'memory_available': memory_info.available,
            'memory_used': memory_info.used,
            'memory_total': memory_info.total
        }
        
        # Add GPU metrics if available
        if self.use_cuda:
            try:
                metrics.update({
                    'gpu_percent': torch.cuda.utilization(self.device.index),
                    'gpu_memory_allocated': torch.cuda.memory_allocated(self.device.index),
                    'gpu_memory_reserved': torch.cuda.memory_reserved(self.device.index),
                    'gpu_memory_total': torch.cuda.get_device_properties(self.device.index).total_memory
                })
            except (AttributeError, RuntimeError) as e:
                logger.warning(f"Could not get GPU metrics: {e}")
        
        self.metrics.append(metrics)
        
        # Log every 10 samples
        if len(self.metrics) % 10 == 0:
            logger.debug(f"Hardware metrics: CPU {cpu_percent}%, Memory {memory_info.percent}%")
    
    def get_summary(self) -> Dict[str, Any]:
        """Get summary of hardware metrics."""
        if not self.metrics:
            return {}
        
        # Calculate averages and maximums
        avg_cpu = sum(m['cpu_percent'] for m in self.metrics) / len(self.metrics)
        max_cpu = max(m['cpu_percent'] for m in self.metrics)
        
        avg_memory = sum(m['memory_percent'] for m in self.metrics) / len(self.metrics)
        max_memory = max(m['memory_percent'] for m in self.metrics)
        
        summary = {
            'avg_cpu_percent': avg_cpu,
            'max_cpu_percent': max_cpu,
            'avg_memory_percent': avg_memory,
            'max_memory_percent': max_memory
        }
        
        # Add GPU summary if available
        if self.use_cuda and 'gpu_percent' in self.metrics[0]:
            avg_gpu = sum(m['gpu_percent'] for m in self.metrics) / len(self.metrics)
            max_gpu = max(m['gpu_percent'] for m in self.metrics)
            
            max_gpu_memory = max(m['gpu_memory_allocated'] for m in self.metrics)
            
            summary.update({
                'avg_gpu_percent': avg_gpu,
                'max_gpu_percent': max_gpu,
                'max_gpu_memory_allocated': max_gpu_memory
            })
        
        return summary

class MemoryProfiler(BaseProfiler):
    """
    Profiles memory usage during training.
    
    Tracks memory consumption, fragmentation, and model size.
    """
    
    def __init__(self, model: nn.Module, device: Optional[Union[str, torch.device]] = None):
        """
        Initialize the memory profiler.
        
        Args:
            model: The model to profile
            device: The device to monitor (e.g., 'cuda:0', 'cpu')
        """
        super().__init__()
        
        self.model = model
        
        if device is None:
            self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        else:
            self.device = device if isinstance(device, torch.device) else torch.device(device)
        
        self.use_cuda = self.device.type == 'cuda'
        self.metrics = []
        
        # Calculate model size
        self.model_size = sum(p.numel() * p.element_size() for p in model.parameters())
        logger.info(f"Model size: {self.model_size / (1024 * 1024):.2f} MB")
    
    def sample(self):
        """Sample current memory metrics."""
        if not self.running:
            return
        
        # Get system memory info
        memory_info = psutil.virtual_memory()
        
        # Create metrics dict
        metrics = {
            'timestamp': time.time(),
            'system_memory_used': memory_info.used,
            'system_memory_available': memory_info.available,
            'system_memory_total': memory_info.total,
            'model_size': self.model_size
        }
        
        # Add GPU memory metrics if available
        if self.use_cuda:
            try:
                metrics.update({
                    'allocated': torch.cuda.memory_allocated(self.device.index),
                    'reserved': torch.cuda.memory_reserved(self.device.index),
                    'max_allocated': torch.cuda.max_memory_allocated(self.device.index),
                    'max_reserved': torch.cuda.max_memory_reserved(self.device.index),
                    'total': torch.cuda.get_device_properties(self.device.index).total_memory
                })
                
                # Calculate fragmentation
                if metrics['reserved'] > 0:
                    metrics['fragmentation'] = 1.0 - (metrics['allocated'] / metrics['reserved'])
                else:
                    metrics['fragmentation'] = 0.0
            except (AttributeError, RuntimeError) as e:
                logger.warning(f"Could not get GPU memory metrics: {e}")
        
        self.metrics.append(metrics)
        
        # Log every 10 samples
        if len(self.metrics) % 10 == 0:
            if self.use_cuda:
                logger.debug(f"Memory metrics: {metrics['allocated'] / (1024 * 1024):.2f} MB allocated, "
                           f"{metrics['fragmentation']:.2%} fragmentation")
            else:
                logger.debug(f"Memory metrics: {memory_info.used / (1024 * 1024):.2f} MB used")
    
    def predict_oom_risk(self) -> Dict[str, Any]:
        """
        Predict risk of out-of-memory (OOM) errors.
        
        Returns:
            Dictionary with OOM risk assessment
        """
        if not self.metrics or not self.use_cuda:
            return {'risk': 'unknown'}
        
        # Get latest metrics
        latest = self.metrics[-1]
        
        # Calculate memory usage trend
        if len(self.metrics) >= 3:
            recent_metrics = self.metrics[-3:]
            allocated_values = [m['allocated'] for m in recent_metrics]
            
            # Calculate growth rate
            if allocated_values[0] > 0:
                growth_rate = (allocated_values[-1] - allocated_values[0]) / allocated_values[0]
            else:
                growth_rate = 0.0
            
            # Calculate current usage percentage
            usage_percent = latest['allocated'] / latest['total']
            
            # Determine risk level
            if usage_percent > 0.9 or (usage_percent > 0.8 and growth_rate > 0.1):
                risk = 'high'
            elif usage_percent > 0.7 or (usage_percent > 0.6 and growth_rate > 0.2):
                risk = 'medium'
            elif usage_percent > 0.5:
                risk = 'low'
            else:
                risk = 'minimal'
            
            return {
                'risk': risk,
                'usage_percent': usage_percent,
                'growth_rate': growth_rate,
                'allocated': latest['allocated'],
                'total': latest['total']
            }
        
        return {'risk': 'unknown'}

class TimingProfiler(BaseProfiler):
    """
    Profiles timing of training operations.
    
    Measures execution times for forward/backward passes and identifies bottlenecks.
    """
    
    def __init__(self):
        """Initialize the timing profiler."""
        super().__init__()
        self.metrics = []
        self.current_batch = {}
        self.start_times = {}
    
    def start_timer(self, name: str):
        """
        Start a timer for a specific operation.
        
        Args:
            name: Name of the operation
        """
        if not self.running:
            return
        
        self.start_times[name] = time.time()
    
    def stop_timer(self, name: str):
        """
        Stop a timer for a specific operation.
        
        Args:
            name: Name of the operation
        """
        if not self.running or name not in self.start_times:
            return
        
        elapsed = time.time() - self.start_times[name]
        self.current_batch[f"{name}_time"] = elapsed
        
        logger.debug(f"{name} took {elapsed:.4f} seconds")
    
    def record_batch(self, iteration: int):
        """
        Record timing metrics for a batch.
        
        Args:
            iteration: Current iteration number
        """
        if not self.running:
            return
        
        # Add batch info
        self.current_batch['iteration'] = iteration
        self.current_batch['timestamp'] = time.time()
        
        # Add to metrics
        self.metrics.append(self.current_batch.copy())
        
        # Reset current batch
        self.current_batch = {}
        self.start_times = {}
    
    def get_bottlenecks(self) -> List[Dict[str, Any]]:
        """
        Identify timing bottlenecks.
        
        Returns:
            List of bottlenecks
        """
        if not self.metrics:
            return []
        
        bottlenecks = []
        
        # Calculate average times
        time_keys = [k for k in self.metrics[0].keys() if k.endswith('_time')]
        
        if not time_keys:
            return []
        
        avg_times = {}
        for key in time_keys:
            values = [m[key] for m in self.metrics if key in m]
            if values:
                avg_times[key] = sum(values) / len(values)
        
        # Find the slowest operation
        slowest_op = max(avg_times.items(), key=lambda x: x[1])
        
        # Calculate total time
        total_time = sum(avg_times.values())
        
        # Check if the slowest operation is a bottleneck
        if slowest_op[1] > total_time * 0.5:
            bottlenecks.append({
                'operation': slowest_op[0].replace('_time', ''),
                'average_time': slowest_op[1],
                'percent_of_total': slowest_op[1] / total_time,
                'severity': 'high' if slowest_op[1] / total_time > 0.7 else 'medium'
            })
        
        return bottlenecks

class DataloaderProfiler(BaseProfiler):
    """
    Profiles dataloader performance.
    
    Analyzes dataloader performance and worker utilization.
    """
    
    def __init__(self, dataloader):
        """
        Initialize the dataloader profiler.
        
        Args:
            dataloader: The dataloader to profile
        """
        super().__init__()
        self.dataloader = dataloader
        self.metrics = []
        self.batch_start_time = None
    
    def start_batch(self):
        """Start timing a batch load."""
        if not self.running:
            return
        
        self.batch_start_time = time.time()
    
    def end_batch(self, batch_size: int):
        """
        End timing a batch load.
        
        Args:
            batch_size: Size of the batch
        """
        if not self.running or self.batch_start_time is None:
            return
        
        elapsed = time.time() - self.batch_start_time
        
        # Get worker info if available
        num_workers = getattr(self.dataloader, 'num_workers', 0)
        
        # Create metrics dict
        metrics = {
            'timestamp': time.time(),
            'batch_load_time': elapsed,
            'batch_size': batch_size,
            'num_workers': num_workers,
            'samples_per_second': batch_size / elapsed if elapsed > 0 else 0
        }
        
        # Estimate worker utilization
        if num_workers > 0:
            # This is a rough estimate
            worker_util = min(1.0, (batch_size / elapsed) / (num_workers * 10))
            metrics['worker_utilization'] = worker_util
        
        self.metrics.append(metrics)
        self.batch_start_time = None
        
        # Log every 10 batches
        if len(self.metrics) % 10 == 0:
            logger.debug(f"Dataloader metrics: {metrics['samples_per_second']:.2f} samples/sec")
    
    def get_optimal_workers(self) -> int:
        """
        Estimate the optimal number of dataloader workers.
        
        Returns:
            Estimated optimal number of workers
        """
        if not self.metrics:
            return os.cpu_count() or 4
        
        # Get current number of workers
        current_workers = self.metrics[0]['num_workers']
        
        # If no workers, recommend based on CPU count
        if current_workers == 0:
            return min(os.cpu_count() or 4, 8)
        
        # Check worker utilization
        if 'worker_utilization' in self.metrics[0]:
            avg_util = sum(m['worker_utilization'] for m in self.metrics) / len(self.metrics)
            
            if avg_util > 0.8:
                # Workers are well utilized, might need more
                return current_workers + 2
            elif avg_util < 0.3:
                # Workers are underutilized
                return max(1, current_workers - 2)
        
        # No clear indication, keep current
        return current_workers

class GradientProfiler(BaseProfiler):
    """
    Profiles gradient statistics during training.
    
    Monitors gradient statistics and detects issues like vanishing/exploding gradients.
    """
    
    def __init__(self, model: nn.Module):
        """
        Initialize the gradient profiler.
        
        Args:
            model: The model to profile
        """
        super().__init__()
        self.model = model
        self.metrics = []
    
    def sample(self):
        """Sample current gradient statistics."""
        if not self.running:
            return
        
        # Collect gradient statistics
        grad_stats = {}
        
        # Check if gradients exist
        has_grads = False
        for name, param in self.model.named_parameters():
            if param.grad is not None:
                has_grads = True
                break
        
        if not has_grads:
            logger.debug("No gradients available for sampling")
            return
        
        # Calculate statistics
        grad_norms = []
        grad_means = []
        grad_maxs = []
        grad_mins = []
        zero_grad_count = 0
        total_params = 0
        
        for name, param in self.model.named_parameters():
            if param.grad is not None:
                grad = param.grad.detach()
                grad_norms.append(grad.norm().item())
                grad_means.append(grad.abs().mean().item())
                grad_maxs.append(grad.abs().max().item())
                grad_mins.append(grad.abs().min().item())
                
                # Count zero gradients
                zero_grad_count += (grad == 0).sum().item()
                total_params += grad.numel()
        
        if grad_norms:
            # Create metrics dict
            metrics = {
                'timestamp': time.time(),
                'avg_grad_norm': sum(grad_norms) / len(grad_norms),
                'max_grad_norm': max(grad_norms),
                'min_grad_norm': min(grad_norms),
                'avg_grad_mean': sum(grad_means) / len(grad_means),
                'max_grad_value': max(grad_maxs),
                'min_grad_value': min(grad_mins),
                'zero_grad_percent': zero_grad_count / total_params if total_params > 0 else 0
            }
            
            self.metrics.append(metrics)
            
            # Log every 10 samples
            if len(self.metrics) % 10 == 0:
                logger.debug(f"Gradient metrics: norm={metrics['avg_grad_norm']:.4e}, "
                           f"max={metrics['max_grad_value']:.4e}, "
                           f"zeros={metrics['zero_grad_percent']:.2%}")
    
    def detect_issues(self) -> List[Dict[str, Any]]:
        """
        Detect gradient-related issues.
        
        Returns:
            List of detected issues
        """
        if not self.metrics:
            return []
        
        issues = []
        
        # Get latest metrics
        latest = self.metrics[-1]
        
        # Check for vanishing gradients
        if latest['avg_grad_norm'] < 1e-7:
            issues.append({
                'type': 'vanishing_gradients',
                'severity': 'high',
                'message': 'Vanishing gradients detected',
                'details': f"Average gradient norm is {latest['avg_grad_norm']:.2e}",
                'timestamp': latest['timestamp']
            })
        
        # Check for exploding gradients
        if latest['max_grad_value'] > 1e3:
            issues.append({
                'type': 'exploding_gradients',
                'severity': 'high',
                'message': 'Exploding gradients detected',
                'details': f"Maximum gradient value is {latest['max_grad_value']:.2e}",
                'timestamp': latest['timestamp']
            })
        
        # Check for dead neurons (too many zero gradients)
        if latest['zero_grad_percent'] > 0.5:
            issues.append({
                'type': 'dead_neurons',
                'severity': 'medium',
                'message': 'Potential dead neurons detected',
                'details': f"{latest['zero_grad_percent']:.1%} of gradients are zero",
                'timestamp': latest['timestamp']
            })
        
        return issues
