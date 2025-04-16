"""
Bottleneck detection module for AutoPipelineDoctor.
"""

from typing import Dict, List, Optional, Any

import logging

logger = logging.getLogger(__name__)

class BottleneckDetector:
    """
    Detects performance bottlenecks in ML/AI training pipelines.
    
    This class analyzes metrics collected by profilers to identify
    bottlenecks in the training process.
    """
    
    def __init__(self, threshold: float = 0.7):
        """
        Initialize the bottleneck detector.
        
        Args:
            threshold: Threshold for bottleneck detection (0.0-1.0)
        """
        self.threshold = threshold
        self.bottlenecks = []
    
    def analyze(self, metrics: Dict[str, List[Dict[str, Any]]]) -> List[Dict[str, Any]]:
        """
        Analyze metrics to detect bottlenecks.
        
        Args:
            metrics: Dictionary of metrics collected by profilers
            
        Returns:
            List of detected bottlenecks
        """
        self.bottlenecks = []
        
        # Analyze memory bottlenecks
        if 'memory' in metrics and metrics['memory']:
            self._analyze_memory_bottlenecks(metrics['memory'])
        
        # Analyze timing bottlenecks
        if 'timing' in metrics and metrics['timing']:
            self._analyze_timing_bottlenecks(metrics['timing'])
        
        # Analyze dataloader bottlenecks
        if 'dataloader' in metrics and metrics['dataloader']:
            self._analyze_dataloader_bottlenecks(metrics['dataloader'])
        
        return self.bottlenecks
    
    def _analyze_memory_bottlenecks(self, memory_metrics: List[Dict[str, Any]]):
        """
        Analyze memory metrics to detect bottlenecks.
        
        Args:
            memory_metrics: List of memory metrics
        """
        # Example implementation
        if not memory_metrics:
            return
        
        # Check for high memory usage
        max_memory = max(m.get('allocated', 0) for m in memory_metrics)
        total_memory = max(m.get('total', 1) for m in memory_metrics)
        
        if max_memory / total_memory > self.threshold:
            self.bottlenecks.append({
                'type': 'memory',
                'severity': 'high',
                'message': 'High memory usage detected',
                'details': f'Memory usage is at {max_memory / total_memory:.1%} of available memory',
                'timestamp': memory_metrics[-1].get('timestamp')
            })
    
    def _analyze_timing_bottlenecks(self, timing_metrics: List[Dict[str, Any]]):
        """
        Analyze timing metrics to detect bottlenecks.
        
        Args:
            timing_metrics: List of timing metrics
        """
        # Example implementation
        if not timing_metrics:
            return
        
        # Check for slow forward pass
        forward_times = [m.get('forward_time', 0) for m in timing_metrics]
        backward_times = [m.get('backward_time', 0) for m in timing_metrics]
        dataloader_times = [m.get('dataloader_time', 0) for m in timing_metrics]
        
        if forward_times and sum(forward_times) > sum(backward_times) * 1.5:
            self.bottlenecks.append({
                'type': 'timing',
                'severity': 'medium',
                'message': 'Slow forward pass detected',
                'details': 'Forward pass is significantly slower than backward pass',
                'timestamp': timing_metrics[-1].get('timestamp')
            })
        
        if dataloader_times and sum(dataloader_times) > (sum(forward_times) + sum(backward_times)) * 0.5:
            self.bottlenecks.append({
                'type': 'timing',
                'severity': 'medium',
                'message': 'Slow data loading detected',
                'details': 'Data loading is taking a significant portion of training time',
                'timestamp': timing_metrics[-1].get('timestamp')
            })
    
    def _analyze_dataloader_bottlenecks(self, dataloader_metrics: List[Dict[str, Any]]):
        """
        Analyze dataloader metrics to detect bottlenecks.
        
        Args:
            dataloader_metrics: List of dataloader metrics
        """
        # Example implementation
        if not dataloader_metrics:
            return
        
        # Check for worker utilization
        worker_util = [m.get('worker_utilization', 0) for m in dataloader_metrics]
        
        if worker_util and sum(worker_util) / len(worker_util) < 0.5:
            self.bottlenecks.append({
                'type': 'dataloader',
                'severity': 'low',
                'message': 'Low worker utilization detected',
                'details': 'Dataloader workers are underutilized',
                'timestamp': dataloader_metrics[-1].get('timestamp')
            })
    
    def get_recommendations(self) -> List[Dict[str, Any]]:
        """
        Get recommendations for fixing detected bottlenecks.
        
        Returns:
            List of recommendations
        """
        recommendations = []
        
        for bottleneck in self.bottlenecks:
            if bottleneck['type'] == 'memory':
                recommendations.append({
                    'type': 'memory',
                    'priority': bottleneck['severity'],
                    'message': 'Consider using gradient checkpointing to reduce memory usage',
                    'details': 'Gradient checkpointing trades computation for memory by recomputing intermediate activations during the backward pass',
                    'code': "from torch.utils.checkpoint import checkpoint\n"
                           "# Modify your model's forward method\n"
                           "def forward(self, x):\n"
                           "    x = checkpoint(self.layer1, x)\n"
                           "    return x"
                })
            
            elif bottleneck['type'] == 'timing' and 'forward pass' in bottleneck['message'].lower():
                recommendations.append({
                    'type': 'timing',
                    'priority': bottleneck['severity'],
                    'message': 'Consider using torch.compile to optimize forward pass',
                    'details': 'torch.compile can speed up your model by JIT-compiling it',
                    'code': "# PyTorch 2.0+\n"
                           "from torch import compile\n"
                           "model = compile(model)"
                })
            
            elif bottleneck['type'] == 'dataloader':
                recommendations.append({
                    'type': 'dataloader',
                    'priority': bottleneck['severity'],
                    'message': 'Increase number of dataloader workers',
                    'details': 'More workers can improve data loading performance',
                    'code': "dataloader = DataLoader(dataset, batch_size=32, num_workers=4, pin_memory=True)"
                })
        
        return recommendations
