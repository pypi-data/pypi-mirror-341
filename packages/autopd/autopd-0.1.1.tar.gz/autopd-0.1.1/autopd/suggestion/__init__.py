"""
Suggestion module for AutoPipelineDoctor.
"""

from typing import Dict, List, Optional, Any, Union
import logging
import torch
import torch.nn as nn

logger = logging.getLogger(__name__)

class OptimizationAdvisor:
    """
    Provides intelligent optimization suggestions for ML/AI training pipelines.
    
    This class analyzes metrics and bottlenecks to suggest optimizations
    that can improve training performance, memory usage, and convergence.
    """
    
    def __init__(self, risk_level: str = 'medium'):
        """
        Initialize the optimization advisor.
        
        Args:
            risk_level: Risk level for suggestions ('low', 'medium', 'high')
        """
        self.risk_level = risk_level
        self.suggestions = []
        
        # Define risk levels
        self.risk_levels = {
            'low': 0,
            'medium': 1,
            'high': 2
        }
    
    def set_risk_level(self, risk_level: str):
        """
        Set the risk level for suggestions.
        
        Args:
            risk_level: Risk level ('low', 'medium', 'high')
        """
        if risk_level in self.risk_levels:
            self.risk_level = risk_level
            logger.info(f"Risk level set to {risk_level}")
        else:
            logger.warning(f"Invalid risk level: {risk_level}. Using 'medium'.")
            self.risk_level = 'medium'
    
    def analyze(self, metrics: Dict[str, List[Dict[str, Any]]], bottlenecks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Analyze metrics and bottlenecks to generate optimization suggestions.
        
        Args:
            metrics: Dictionary of metrics collected by profilers
            bottlenecks: List of detected bottlenecks
            
        Returns:
            List of optimization suggestions
        """
        self.suggestions = []
        
        # Generate memory optimization suggestions
        self._suggest_memory_optimizations(metrics, bottlenecks)
        
        # Generate performance optimization suggestions
        self._suggest_performance_optimizations(metrics, bottlenecks)
        
        # Generate convergence optimization suggestions
        self._suggest_convergence_optimizations(metrics, bottlenecks)
        
        # Generate dataloader optimization suggestions
        self._suggest_dataloader_optimizations(metrics, bottlenecks)
        
        # Filter suggestions based on risk level
        risk_threshold = self.risk_levels[self.risk_level]
        filtered_suggestions = []
        
        for suggestion in self.suggestions:
            suggestion_risk = self.risk_levels.get(suggestion.get('risk_level', 'medium'), 1)
            if suggestion_risk <= risk_threshold:
                filtered_suggestions.append(suggestion)
        
        # Sort by priority
        priority_map = {'critical': 0, 'high': 1, 'medium': 2, 'low': 3}
        filtered_suggestions.sort(key=lambda x: priority_map.get(x.get('priority', 'medium'), 2))
        
        return filtered_suggestions
    
    def _suggest_memory_optimizations(self, metrics: Dict[str, List[Dict[str, Any]]], bottlenecks: List[Dict[str, Any]]):
        """
        Suggest memory optimizations.
        
        Args:
            metrics: Dictionary of metrics
            bottlenecks: List of detected bottlenecks
        """
        # Check for memory bottlenecks
        memory_bottlenecks = [b for b in bottlenecks if b.get('type') == 'memory']
        
        if memory_bottlenecks:
            # Suggest gradient checkpointing
            self.suggestions.append({
                'category': 'memory',
                'name': 'gradient_checkpointing',
                'priority': memory_bottlenecks[0].get('severity', 'medium'),
                'risk_level': 'low',
                'message': 'Use gradient checkpointing to reduce memory usage',
                'details': 'Gradient checkpointing trades computation for memory by recomputing intermediate activations during the backward pass',
                'code': "from torch.utils.checkpoint import checkpoint\n"
                       "# Modify your model's forward method\n"
                       "def forward(self, x):\n"
                       "    x = checkpoint(self.layer1, x)\n"
                       "    return x"
            })
            
            # Suggest mixed precision training
            self.suggestions.append({
                'category': 'memory',
                'name': 'mixed_precision',
                'priority': memory_bottlenecks[0].get('severity', 'medium'),
                'risk_level': 'low',
                'message': 'Use mixed precision training to reduce memory usage',
                'details': 'Mixed precision training uses float16 for most operations, reducing memory usage and potentially improving performance',
                'code': "from torch.cuda.amp import autocast, GradScaler\n"
                       "scaler = GradScaler()\n"
                       "with autocast():\n"
                       "    outputs = model(inputs)\n"
                       "    loss = criterion(outputs, targets)\n"
                       "scaler.scale(loss).backward()\n"
                       "scaler.step(optimizer)\n"
                       "scaler.update()"
            })
            
            # Suggest optimizer memory optimization
            self.suggestions.append({
                'category': 'memory',
                'name': 'optimizer_memory',
                'priority': 'medium',
                'risk_level': 'medium',
                'message': 'Use memory-efficient optimizer',
                'details': 'Optimizers like Adam store additional state for each parameter, increasing memory usage. Consider using AdamW with fused implementation or SGD for memory savings.',
                'code': "# For PyTorch 2.0+\n"
                       "optimizer = torch.optim.AdamW(model.parameters(), lr=0.001, fused=True)"
            })
        
        # Check memory metrics for high usage
        if 'memory' in metrics and metrics['memory']:
            latest_memory = metrics['memory'][-1]
            
            if 'allocated' in latest_memory and 'total' in latest_memory:
                memory_usage = latest_memory['allocated'] / latest_memory['total']
                
                if memory_usage > 0.8:
                    # Suggest reducing batch size
                    self.suggestions.append({
                        'category': 'memory',
                        'name': 'reduce_batch_size',
                        'priority': 'high',
                        'risk_level': 'low',
                        'message': 'Reduce batch size to decrease memory usage',
                        'details': f'Current memory usage is {memory_usage:.1%} of available memory',
                        'code': "# Reduce batch size and use gradient accumulation to maintain effective batch size\n"
                               "dataloader = DataLoader(dataset, batch_size=batch_size // 2)\n"
                               "accumulation_steps = 2"
                    })
    
    def _suggest_performance_optimizations(self, metrics: Dict[str, List[Dict[str, Any]]], bottlenecks: List[Dict[str, Any]]):
        """
        Suggest performance optimizations.
        
        Args:
            metrics: Dictionary of metrics
            bottlenecks: List of detected bottlenecks
        """
        # Check for timing bottlenecks
        timing_bottlenecks = [b for b in bottlenecks if b.get('type') == 'timing']
        
        if timing_bottlenecks:
            # Suggest torch.compile
            self.suggestions.append({
                'category': 'performance',
                'name': 'torch_compile',
                'priority': timing_bottlenecks[0].get('severity', 'medium'),
                'risk_level': 'medium',
                'message': 'Use torch.compile to optimize model execution',
                'details': 'torch.compile can significantly speed up your model by JIT-compiling it',
                'code': "# PyTorch 2.0+\n"
                       "from torch import compile\n"
                       "model = compile(model)"
            })
            
            # Suggest channels last memory format
            self.suggestions.append({
                'category': 'performance',
                'name': 'channels_last',
                'priority': 'medium',
                'risk_level': 'medium',
                'message': 'Use channels_last memory format for CNN models',
                'details': 'channels_last memory format can improve performance for convolutional models on CUDA',
                'code': "# Convert model and inputs to channels_last format\n"
                       "model = model.to(memory_format=torch.channels_last)\n"
                       "inputs = inputs.to(memory_format=torch.channels_last)"
            })
        
        # Check if CUDA is available
        if 'hardware' in metrics and metrics['hardware'] and any(m.get('device_type') == 'cuda' for m in metrics['hardware']):
            # Suggest using pinned memory
            self.suggestions.append({
                'category': 'performance',
                'name': 'pinned_memory',
                'priority': 'medium',
                'risk_level': 'low',
                'message': 'Use pinned memory for faster CPU to GPU transfers',
                'details': 'Pinned memory can speed up data transfer from CPU to GPU',
                'code': "dataloader = DataLoader(dataset, batch_size=32, pin_memory=True)"
            })
    
    def _suggest_convergence_optimizations(self, metrics: Dict[str, List[Dict[str, Any]]], bottlenecks: List[Dict[str, Any]]):
        """
        Suggest convergence optimizations.
        
        Args:
            metrics: Dictionary of metrics
            bottlenecks: List of detected bottlenecks
        """
        # Check for gradient issues
        gradient_issues = [b for b in bottlenecks if b.get('type') in ['vanishing_gradients', 'exploding_gradients', 'dead_neurons']]
        
        if gradient_issues:
            issue_type = gradient_issues[0].get('type')
            
            if issue_type == 'vanishing_gradients':
                # Suggest gradient clipping
                self.suggestions.append({
                    'category': 'convergence',
                    'name': 'gradient_clipping',
                    'priority': 'high',
                    'risk_level': 'low',
                    'message': 'Use gradient clipping to prevent vanishing gradients',
                    'details': 'Gradient clipping can help stabilize training by preventing gradients from becoming too small',
                    'code': "# Clip gradients by norm\n"
                           "torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)"
                })
                
                # Suggest different activation function
                self.suggestions.append({
                    'category': 'convergence',
                    'name': 'activation_function',
                    'priority': 'medium',
                    'risk_level': 'medium',
                    'message': 'Consider using different activation functions',
                    'details': 'ReLU can cause vanishing gradients due to dying neurons. Consider using LeakyReLU, GELU, or Swish.',
                    'code': "# Replace ReLU with LeakyReLU\n"
                           "model = nn.Sequential(\n"
                           "    nn.Linear(10, 50),\n"
                           "    nn.LeakyReLU(negative_slope=0.01),\n"
                           "    nn.Linear(50, 10)\n"
                           ")"
                })
            
            elif issue_type == 'exploding_gradients':
                # Suggest gradient clipping
                self.suggestions.append({
                    'category': 'convergence',
                    'name': 'gradient_clipping',
                    'priority': 'high',
                    'risk_level': 'low',
                    'message': 'Use gradient clipping to prevent exploding gradients',
                    'details': 'Gradient clipping can help stabilize training by preventing gradients from becoming too large',
                    'code': "# Clip gradients by norm\n"
                           "torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)"
                })
                
                # Suggest learning rate reduction
                self.suggestions.append({
                    'category': 'convergence',
                    'name': 'reduce_learning_rate',
                    'priority': 'high',
                    'risk_level': 'low',
                    'message': 'Reduce learning rate to prevent exploding gradients',
                    'details': 'A high learning rate can cause exploding gradients',
                    'code': "# Reduce learning rate\n"
                           "for param_group in optimizer.param_groups:\n"
                           "    param_group['lr'] *= 0.1"
                })
            
            elif issue_type == 'dead_neurons':
                # Suggest different activation function
                self.suggestions.append({
                    'category': 'convergence',
                    'name': 'activation_function',
                    'priority': 'high',
                    'risk_level': 'medium',
                    'message': 'Replace ReLU with LeakyReLU to prevent dead neurons',
                    'details': 'ReLU can cause neurons to die when they only receive negative inputs',
                    'code': "# Replace ReLU with LeakyReLU\n"
                           "model = nn.Sequential(\n"
                           "    nn.Linear(10, 50),\n"
                           "    nn.LeakyReLU(negative_slope=0.01),\n"
                           "    nn.Linear(50, 10)\n"
                           ")"
                })
        
        # Check batch metrics for loss patterns
        if 'batch' in metrics and len(metrics['batch']) > 10:
            loss_values = [m.get('loss', float('nan')) for m in metrics['batch'] if 'loss' in m]
            
            if loss_values and all(not isinstance(v, float) or not torch.isnan(torch.tensor(v)) for v in loss_values):
                # Check for plateauing loss
                recent_losses = loss_values[-5:]
                if max(recent_losses) - min(recent_losses) < 0.01 * recent_losses[0]:
                    # Suggest learning rate scheduler
                    self.suggestions.append({
                        'category': 'convergence',
                        'name': 'learning_rate_scheduler',
                        'priority': 'medium',
                        'risk_level': 'low',
                        'message': 'Use learning rate scheduler to overcome plateaus',
                        'details': 'Loss appears to be plateauing. A learning rate scheduler can help overcome plateaus.',
                        'code': "# Use ReduceLROnPlateau scheduler\n"
                               "scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(optimizer, 'min', patience=5, factor=0.1)"
                    })
    
    def _suggest_dataloader_optimizations(self, metrics: Dict[str, List[Dict[str, Any]]], bottlenecks: List[Dict[str, Any]]):
        """
        Suggest dataloader optimizations.
        
        Args:
            metrics: Dictionary of metrics
            bottlenecks: List of detected bottlenecks
        """
        # Check for dataloader bottlenecks
        dataloader_bottlenecks = [b for b in bottlenecks if b.get('type') == 'dataloader']
        
        if dataloader_bottlenecks:
            # Suggest increasing num_workers
            self.suggestions.append({
                'category': 'dataloader',
                'name': 'increase_workers',
                'priority': dataloader_bottlenecks[0].get('severity', 'medium'),
                'risk_level': 'low',
                'message': 'Increase number of dataloader workers',
                'details': 'More workers can improve data loading performance',
                'code': "dataloader = DataLoader(dataset, batch_size=32, num_workers=4, pin_memory=True)"
            })
            
            # Suggest prefetch factor
            self.suggestions.append({
                'category': 'dataloader',
                'name': 'prefetch_factor',
                'priority': 'medium',
                'risk_level': 'low',
                'message': 'Increase prefetch factor for dataloader',
                'details': 'Prefetch factor controls how many batches each worker prefetches',
                'code': "# PyTorch 1.7+\n"
                       "dataloader = DataLoader(dataset, batch_size=32, num_workers=4, prefetch_factor=2)"
            })
        
        # Check dataloader metrics for slow loading
        if 'timing' in metrics and metrics['timing']:
            timing_metrics = metrics['timing']
            
            # Check if dataloader time is significant
            dataloader_times = [m.get('dataloader_time', 0) for m in timing_metrics if 'dataloader_time' in m]
            forward_times = [m.get('forward_time', 0) for m in timing_metrics if 'forward_time' in m]
            
            if dataloader_times and forward_times:
                avg_dataloader_time = sum(dataloader_times) / len(dataloader_times)
                avg_forward_time = sum(forward_times) / len(forward_times)
                
                if avg_dataloader_time > avg_forward_time * 0.5:
                    # Suggest data preprocessing
                    self.suggestions.append({
                        'category': 'dataloader',
                        'name': 'data_preprocessing',
                        'priority': 'medium',
                        'risk_level': 'medium',
                        'message': 'Preprocess data to reduce loading time',
                        'details': 'Data loading is taking significant time. Consider preprocessing data or using a more efficient format.',
                        'code': "# Example: Convert images to .pt files\n"
                               "import torch\n"
                               "from PIL import Image\n"
                               "import os\n\n"
                               "for img_path in image_paths:\n"
                               "    img = Image.open(img_path)\n"
                               "    tensor = transforms(img)\n"
                               "    torch.save(tensor, os.path.splitext(img_path)[0] + '.pt')"
                    })
    
    def apply_optimization(self, model: nn.Module, optimization: str, **kwargs) -> bool:
        """
        Apply an optimization to the model.
        
        Args:
            model: The model to optimize
            optimization: Name of the optimization to apply
            **kwargs: Additional arguments for the optimization
            
        Returns:
            True if optimization was applied successfully, False otherwise
        """
        try:
            if optimization == 'gradient_checkpointing':
                # Enable gradient checkpointing
                if hasattr(model, 'gradient_checkpointing_enable'):
                    model.gradient_checkpointing_enable()
                    logger.info("Gradient checkpointing enabled")
                    return True
                else:
                    logger.warning("Model does not support gradient_checkpointing_enable method")
                    return False
            
            elif optimization == 'channels_last':
                # Convert model to channels_last format
                model = model.to(memory_format=torch.channels_last)
                logger.info("Model converted to channels_last format")
                return True
            
            elif optimization == 'torch_compile':
                # Compile model with torch.compile
                if hasattr(torch, 'compile'):
                    compiled_model = torch.compile(model)
                    logger.info("Model compiled with torch.compile")
                    return True
                else:
                    logger.warning("torch.compile not available (requires PyTorch 2.0+)")
                    return False
            
            else:
                logger.warning(f"Unknown optimization: {optimization}")
                return False
        
        except Exception as e:
            logger.error(f"Error applying optimization {optimization}: {e}")
            return False
