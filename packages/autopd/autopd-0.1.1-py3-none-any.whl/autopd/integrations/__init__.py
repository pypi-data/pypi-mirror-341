"""
Integrations module for AutoPipelineDoctor.
"""

from typing import Dict, List, Optional, Any, Union, Callable
import logging
import os
import json
import time
import inspect
import importlib
import sys
from functools import wraps

logger = logging.getLogger(__name__)

class PyTorchIntegration:
    """
    Integration with PyTorch.
    
    This class provides integration with PyTorch models, optimizers, and dataloaders.
    """
    
    def __init__(self):
        """Initialize the PyTorch integration."""
        try:
            import torch
            self.torch = torch
            self.is_available = True
            logger.info(f"PyTorch integration initialized (version {torch.__version__})")
        except ImportError:
            self.torch = None
            self.is_available = False
            logger.warning("PyTorch not installed. PyTorch integration not available.")
    
    def patch_module(self, module):
        """
        Patch a PyTorch module for monitoring.
        
        Args:
            module: PyTorch module to patch
            
        Returns:
            Patched module
        """
        if not self.is_available or module is None:
            return module
        
        original_forward = module.forward
        
        @wraps(original_forward)
        def patched_forward(*args, **kwargs):
            # Record start time
            start_time = time.time()
            
            # Call original forward
            output = original_forward(*args, **kwargs)
            
            # Record end time
            end_time = time.time()
            
            # Store timing information
            if not hasattr(module, '_autopd_stats'):
                module._autopd_stats = {}
            
            if 'forward_times' not in module._autopd_stats:
                module._autopd_stats['forward_times'] = []
            
            module._autopd_stats['forward_times'].append(end_time - start_time)
            
            # Keep only the last 100 times
            if len(module._autopd_stats['forward_times']) > 100:
                module._autopd_stats['forward_times'] = module._autopd_stats['forward_times'][-100:]
            
            return output
        
        # Replace forward method
        module.forward = patched_forward
        
        # Mark as patched
        module._autopd_patched = True
        
        return module
    
    def patch_optimizer(self, optimizer):
        """
        Patch a PyTorch optimizer for monitoring.
        
        Args:
            optimizer: PyTorch optimizer to patch
            
        Returns:
            Patched optimizer
        """
        if not self.is_available or optimizer is None:
            return optimizer
        
        original_step = optimizer.step
        
        @wraps(original_step)
        def patched_step(closure=None):
            # Record start time
            start_time = time.time()
            
            # Call original step
            result = original_step(closure)
            
            # Record end time
            end_time = time.time()
            
            # Store timing information
            if not hasattr(optimizer, '_autopd_stats'):
                optimizer._autopd_stats = {}
            
            if 'step_times' not in optimizer._autopd_stats:
                optimizer._autopd_stats['step_times'] = []
            
            optimizer._autopd_stats['step_times'].append(end_time - start_time)
            
            # Keep only the last 100 times
            if len(optimizer._autopd_stats['step_times']) > 100:
                optimizer._autopd_stats['step_times'] = optimizer._autopd_stats['step_times'][-100:]
            
            return result
        
        # Replace step method
        optimizer.step = patched_step
        
        # Mark as patched
        optimizer._autopd_patched = True
        
        return optimizer
    
    def patch_dataloader(self, dataloader):
        """
        Patch a PyTorch dataloader for monitoring.
        
        Args:
            dataloader: PyTorch dataloader to patch
            
        Returns:
            Patched dataloader
        """
        if not self.is_available or dataloader is None:
            return dataloader
        
        original_iter = dataloader.__iter__
        
        @wraps(original_iter)
        def patched_iter():
            # Get original iterator
            iterator = original_iter()
            
            # Create a wrapper for the iterator
            class TimedIterator:
                def __init__(self, iterator):
                    self.iterator = iterator
                    self.batch_times = []
                
                def __iter__(self):
                    return self
                
                def __next__(self):
                    # Record start time
                    start_time = time.time()
                    
                    try:
                        # Get next batch
                        batch = next(self.iterator)
                        
                        # Record end time
                        end_time = time.time()
                        
                        # Store timing information
                        self.batch_times.append(end_time - start_time)
                        
                        # Keep only the last 100 times
                        if len(self.batch_times) > 100:
                            self.batch_times = self.batch_times[-100:]
                        
                        return batch
                    
                    except StopIteration:
                        # Store batch times in dataloader
                        if not hasattr(dataloader, '_autopd_stats'):
                            dataloader._autopd_stats = {}
                        
                        dataloader._autopd_stats['batch_times'] = self.batch_times
                        
                        raise
            
            return TimedIterator(iterator)
        
        # Replace __iter__ method
        dataloader.__iter__ = patched_iter
        
        # Mark as patched
        dataloader._autopd_patched = True
        
        return dataloader
    
    def get_module_stats(self, module):
        """
        Get statistics for a patched module.
        
        Args:
            module: Patched PyTorch module
            
        Returns:
            Dictionary of statistics
        """
        if not hasattr(module, '_autopd_patched') or not module._autopd_patched:
            return {}
        
        if not hasattr(module, '_autopd_stats'):
            return {}
        
        stats = module._autopd_stats.copy()
        
        # Calculate additional statistics
        if 'forward_times' in stats and stats['forward_times']:
            forward_times = stats['forward_times']
            stats['avg_forward_time'] = sum(forward_times) / len(forward_times)
            stats['min_forward_time'] = min(forward_times)
            stats['max_forward_time'] = max(forward_times)
        
        return stats
    
    def get_optimizer_stats(self, optimizer):
        """
        Get statistics for a patched optimizer.
        
        Args:
            optimizer: Patched PyTorch optimizer
            
        Returns:
            Dictionary of statistics
        """
        if not hasattr(optimizer, '_autopd_patched') or not optimizer._autopd_patched:
            return {}
        
        if not hasattr(optimizer, '_autopd_stats'):
            return {}
        
        stats = optimizer._autopd_stats.copy()
        
        # Calculate additional statistics
        if 'step_times' in stats and stats['step_times']:
            step_times = stats['step_times']
            stats['avg_step_time'] = sum(step_times) / len(step_times)
            stats['min_step_time'] = min(step_times)
            stats['max_step_time'] = max(step_times)
        
        return stats
    
    def get_dataloader_stats(self, dataloader):
        """
        Get statistics for a patched dataloader.
        
        Args:
            dataloader: Patched PyTorch dataloader
            
        Returns:
            Dictionary of statistics
        """
        if not hasattr(dataloader, '_autopd_patched') or not dataloader._autopd_patched:
            return {}
        
        if not hasattr(dataloader, '_autopd_stats'):
            return {}
        
        stats = dataloader._autopd_stats.copy()
        
        # Calculate additional statistics
        if 'batch_times' in stats and stats['batch_times']:
            batch_times = stats['batch_times']
            stats['avg_batch_time'] = sum(batch_times) / len(batch_times)
            stats['min_batch_time'] = min(batch_times)
            stats['max_batch_time'] = max(batch_times)
            
            # Calculate throughput (batches per second)
            stats['throughput'] = 1.0 / stats['avg_batch_time']
        
        return stats
    
    def get_model_info(self, model):
        """
        Get information about a PyTorch model.
        
        Args:
            model: PyTorch model
            
        Returns:
            Dictionary of model information
        """
        if not self.is_available or model is None:
            return {}
        
        try:
            # Get model parameters
            num_params = sum(p.numel() for p in model.parameters())
            num_trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
            
            # Get model structure
            model_str = str(model)
            
            # Get model size in memory
            model_size_bytes = 0
            for param in model.parameters():
                model_size_bytes += param.nelement() * param.element_size()
            
            for buffer in model.buffers():
                model_size_bytes += buffer.nelement() * buffer.element_size()
            
            # Convert to MB
            model_size_mb = model_size_bytes / (1024 * 1024)
            
            # Get model device
            try:
                model_device = next(model.parameters()).device
            except StopIteration:
                model_device = "unknown"
            
            # Get model dtype
            try:
                model_dtype = next(model.parameters()).dtype
            except StopIteration:
                model_dtype = "unknown"
            
            return {
                'num_params': num_params,
                'num_trainable_params': num_trainable_params,
                'model_size_mb': model_size_mb,
                'model_device': str(model_device),
                'model_dtype': str(model_dtype),
                'model_structure': model_str
            }
        
        except Exception as e:
            logger.error(f"Error getting model info: {e}")
            return {}
    
    def get_optimizer_info(self, optimizer):
        """
        Get information about a PyTorch optimizer.
        
        Args:
            optimizer: PyTorch optimizer
            
        Returns:
            Dictionary of optimizer information
        """
        if not self.is_available or optimizer is None:
            return {}
        
        try:
            # Get optimizer type
            optimizer_type = optimizer.__class__.__name__
            
            # Get optimizer parameters
            param_groups = []
            
            for i, group in enumerate(optimizer.param_groups):
                group_info = {}
                
                for key, value in group.items():
                    if key == 'params':
                        group_info['num_params'] = len(value)
                    else:
                        group_info[key] = value
                
                param_groups.append(group_info)
            
            return {
                'optimizer_type': optimizer_type,
                'param_groups': param_groups
            }
        
        except Exception as e:
            logger.error(f"Error getting optimizer info: {e}")
            return {}
    
    def get_dataloader_info(self, dataloader):
        """
        Get information about a PyTorch dataloader.
        
        Args:
            dataloader: PyTorch dataloader
            
        Returns:
            Dictionary of dataloader information
        """
        if not self.is_available or dataloader is None:
            return {}
        
        try:
            # Get dataloader parameters
            batch_size = dataloader.batch_size if hasattr(dataloader, 'batch_size') else None
            num_workers = dataloader.num_workers if hasattr(dataloader, 'num_workers') else None
            pin_memory = dataloader.pin_memory if hasattr(dataloader, 'pin_memory') else None
            
            # Get dataset information
            dataset = dataloader.dataset if hasattr(dataloader, 'dataset') else None
            dataset_len = len(dataset) if dataset is not None else None
            dataset_type = dataset.__class__.__name__ if dataset is not None else None
            
            return {
                'batch_size': batch_size,
                'num_workers': num_workers,
                'pin_memory': pin_memory,
                'dataset_len': dataset_len,
                'dataset_type': dataset_type,
                'num_batches': dataset_len // batch_size if dataset_len is not None and batch_size is not None else None
            }
        
        except Exception as e:
            logger.error(f"Error getting dataloader info: {e}")
            return {}
    
    def get_memory_stats(self):
        """
        Get PyTorch memory statistics.
        
        Returns:
            Dictionary of memory statistics
        """
        if not self.is_available:
            return {}
        
        try:
            # Check if CUDA is available
            if not self.torch.cuda.is_available():
                return {}
            
            # Get memory statistics for each device
            memory_stats = {}
            
            for i in range(self.torch.cuda.device_count()):
                memory_stats[f'cuda:{i}'] = {
                    'allocated': self.torch.cuda.memory_allocated(i) / (1024 * 1024),  # MB
                    'cached': self.torch.cuda.memory_reserved(i) / (1024 * 1024),  # MB
                    'max_allocated': self.torch.cuda.max_memory_allocated(i) / (1024 * 1024),  # MB
                    'max_cached': self.torch.cuda.max_memory_reserved(i) / (1024 * 1024)  # MB
                }
            
            return memory_stats
        
        except Exception as e:
            logger.error(f"Error getting memory stats: {e}")
            return {}

class LightningIntegration:
    """
    Integration with PyTorch Lightning.
    
    This class provides integration with PyTorch Lightning models and trainers.
    """
    
    def __init__(self):
        """Initialize the PyTorch Lightning integration."""
        try:
            import pytorch_lightning as pl
            self.pl = pl
            self.is_available = True
            logger.info(f"PyTorch Lightning integration initialized (version {pl.__version__})")
        except ImportError:
            self.pl = None
            self.is_available = False
            logger.warning("PyTorch Lightning not installed. Lightning integration not available.")
    
    def create_callback(self, doctor):
        """
        Create a Lightning callback for monitoring.
        
        Args:
            doctor: AutoPipelineDoctor instance
            
        Returns:
            Lightning callback
        """
        if not self.is_available:
            return None
        
        # Create a callback class
        class AutoPDCallback(self.pl.Callback):
            def __init__(self, doctor):
                super().__init__()
                self.doctor = doctor
                self.batch_times = []
                self.epoch_times = []
            
            def on_train_start(self, trainer, pl_module):
                # Record model information
                model_info = {
                    'num_params': sum(p.numel() for p in pl_module.parameters()),
                    'num_trainable_params': sum(p.numel() for p in pl_module.parameters() if p.requires_grad),
                    'model_type': pl_module.__class__.__name__
                }
                
                self.doctor.add_metrics('model', model_info)
            
            def on_train_batch_start(self, trainer, pl_module, batch, batch_idx):
                self.batch_start_time = time.time()
            
            def on_train_batch_end(self, trainer, pl_module, outputs, batch, batch_idx):
                batch_time = time.time() - self.batch_start_time
                self.batch_times.append(batch_time)
                
                # Keep only the last 100 times
                if len(self.batch_times) > 100:
                    self.batch_times = self.batch_times[-100:]
                
                # Add batch metrics
                batch_metrics = {
                    'batch_idx': batch_idx,
                    'batch_time': batch_time,
                    'avg_batch_time': sum(self.batch_times) / len(self.batch_times),
                    'loss': outputs['loss'].item() if isinstance(outputs, dict) and 'loss' in outputs else None
                }
                
                self.doctor.add_metrics('batch', batch_metrics)
            
            def on_train_epoch_start(self, trainer, pl_module):
                self.epoch_start_time = time.time()
            
            def on_train_epoch_end(self, trainer, pl_module):
                epoch_time = time.time() - self.epoch_start_time
                self.epoch_times.append(epoch_time)
                
                # Add epoch metrics
                epoch_metrics = {
                    'epoch': trainer.current_epoch,
                    'epoch_time': epoch_time,
                    'avg_epoch_time': sum(self.epoch_times) / len(self.epoch_times),
                    'learning_rate': trainer.optimizers[0].param_groups[0]['lr'] if trainer.optimizers else None
                }
                
                # Add metrics from trainer
                if hasattr(trainer, 'callback_metrics'):
                    for key, value in trainer.callback_metrics.items():
                        if isinstance(value, self.pl.utilities.types.torch.Tensor):
                            epoch_metrics[key] = value.item()
                        else:
                            epoch_metrics[key] = value
                
                self.doctor.add_metrics('epoch', epoch_metrics)
            
            def on_validation_start(self, trainer, pl_module):
                self.val_start_time = time.time()
            
            def on_validation_end(self, trainer, pl_module):
                val_time = time.time() - self.val_start_time
                
                # Add validation metrics
                val_metrics = {
                    'epoch': trainer.current_epoch,
                    'val_time': val_time
                }
                
                # Add metrics from trainer
                if hasattr(trainer, 'callback_metrics'):
                    for key, value in trainer.callback_metrics.items():
                        if isinstance(value, self.pl.utilities.types.torch.Tensor):
                            val_metrics[key] = value.item()
                        else:
                            val_metrics[key] = value
                
                self.doctor.add_metrics('validation', val_metrics)
            
            def on_test_start(self, trainer, pl_module):
                self.test_start_time = time.time()
            
            def on_test_end(self, trainer, pl_module):
                test_time = time.time() - self.test_start_time
                
                # Add test metrics
                test_metrics = {
                    'test_time': test_time
                }
                
                # Add metrics from trainer
                if hasattr(trainer, 'callback_metrics'):
                    for key, value in trainer.callback_metrics.items():
                        if isinstance(value, self.pl.utilities.types.torch.Tensor):
                            test_metrics[key] = value.item()
                        else:
                            test_metrics[key] = value
                
                self.doctor.add_metrics('test', test_metrics)
            
            def on_exception(self, trainer, pl_module, exception):
                # Add exception as warning
                self.doctor.add_warning(
                    warning_type='exception',
                    message=str(exception),
                    severity='critical',
                    details={'exception_type': exception.__class__.__name__}
                )
        
        return AutoPDCallback(doctor)
    
    def get_trainer_info(self, trainer):
        """
        Get information about a Lightning trainer.
        
        Args:
            trainer: Lightning trainer
            
        Returns:
            Dictionary of trainer information
        """
        if not self.is_available or trainer is None:
            return {}
        
        try:
            # Get trainer parameters
            max_epochs = trainer.max_epochs
            gpus = trainer.num_gpus if hasattr(trainer, 'num_gpus') else None
            precision = trainer.precision
            
            # Get dataloader information
            train_dataloader = trainer.train_dataloader if hasattr(trainer, 'train_dataloader') else None
            val_dataloader = trainer.val_dataloaders if hasattr(trainer, 'val_dataloaders') else None
            
            train_dataloader_info = {}
            if train_dataloader:
                try:
                    train_dataloader_info = {
                        'batch_size': train_dataloader.batch_size if hasattr(train_dataloader, 'batch_size') else None,
                        'num_workers': train_dataloader.num_workers if hasattr(train_dataloader, 'num_workers') else None,
                        'dataset_len': len(train_dataloader.dataset) if hasattr(train_dataloader, 'dataset') else None
                    }
                except:
                    pass
            
            return {
                'max_epochs': max_epochs,
                'gpus': gpus,
                'precision': precision,
                'train_dataloader': train_dataloader_info
            }
        
        except Exception as e:
            logger.error(f"Error getting trainer info: {e}")
            return {}

class HuggingFaceIntegration:
    """
    Integration with HuggingFace Transformers.
    
    This class provides integration with HuggingFace Transformers models and trainers.
    """
    
    def __init__(self):
        """Initialize the HuggingFace integration."""
        try:
            import transformers
            self.transformers = transformers
            self.is_available = True
            logger.info(f"HuggingFace integration initialized (version {transformers.__version__})")
        except ImportError:
            self.transformers = None
            self.is_available = False
            logger.warning("HuggingFace Transformers not installed. HuggingFace integration not available.")
    
    def create_callback(self, doctor):
        """
        Create a HuggingFace callback for monitoring.
        
        Args:
            doctor: AutoPipelineDoctor instance
            
        Returns:
            HuggingFace callback
        """
        if not self.is_available:
            return None
        
        # Create a callback class
        class AutoPDCallback(self.transformers.TrainerCallback):
            def __init__(self, doctor):
                self.doctor = doctor
                self.step_times = []
                self.epoch_times = []
            
            def on_train_begin(self, args, state, control, model=None, **kwargs):
                # Record model information
                if model:
                    model_info = {
                        'num_params': sum(p.numel() for p in model.parameters()),
                        'num_trainable_params': sum(p.numel() for p in model.parameters() if p.requires_grad),
                        'model_type': model.__class__.__name__
                    }
                    
                    self.doctor.add_metrics('model', model_info)
                
                # Record training arguments
                if args:
                    args_dict = args.to_dict()
                    self.doctor.add_metrics('args', args_dict)
            
            def on_step_begin(self, args, state, control, **kwargs):
                self.step_start_time = time.time()
            
            def on_step_end(self, args, state, control, **kwargs):
                step_time = time.time() - self.step_start_time
                self.step_times.append(step_time)
                
                # Keep only the last 100 times
                if len(self.step_times) > 100:
                    self.step_times = self.step_times[-100:]
                
                # Add step metrics
                step_metrics = {
                    'step': state.global_step,
                    'step_time': step_time,
                    'avg_step_time': sum(self.step_times) / len(self.step_times),
                    'loss': state.log_history[-1]['loss'] if state.log_history else None
                }
                
                self.doctor.add_metrics('step', step_metrics)
            
            def on_epoch_begin(self, args, state, control, **kwargs):
                self.epoch_start_time = time.time()
            
            def on_epoch_end(self, args, state, control, **kwargs):
                epoch_time = time.time() - self.epoch_start_time
                self.epoch_times.append(epoch_time)
                
                # Add epoch metrics
                epoch_metrics = {
                    'epoch': state.epoch,
                    'epoch_time': epoch_time,
                    'avg_epoch_time': sum(self.epoch_times) / len(self.epoch_times)
                }
                
                # Add metrics from log history
                if state.log_history:
                    last_log = state.log_history[-1]
                    for key, value in last_log.items():
                        if key not in ['epoch', 'step']:
                            epoch_metrics[key] = value
                
                self.doctor.add_metrics('epoch', epoch_metrics)
            
            def on_evaluate(self, args, state, control, metrics=None, **kwargs):
                # Add evaluation metrics
                if metrics:
                    eval_metrics = metrics.copy()
                    eval_metrics['epoch'] = state.epoch
                    eval_metrics['step'] = state.global_step
                    
                    self.doctor.add_metrics('evaluation', eval_metrics)
            
            def on_log(self, args, state, control, logs=None, **kwargs):
                # Add log metrics
                if logs:
                    log_metrics = logs.copy()
                    log_metrics['epoch'] = state.epoch
                    log_metrics['step'] = state.global_step
                    
                    self.doctor.add_metrics('log', log_metrics)
            
            def on_train_end(self, args, state, control, **kwargs):
                # Add final metrics
                final_metrics = {
                    'total_steps': state.global_step,
                    'total_epochs': state.epoch
                }
                
                self.doctor.add_metrics('final', final_metrics)
        
        return AutoPDCallback(doctor)
    
    def get_model_info(self, model):
        """
        Get information about a HuggingFace model.
        
        Args:
            model: HuggingFace model
            
        Returns:
            Dictionary of model information
        """
        if not self.is_available or model is None:
            return {}
        
        try:
            # Check if it's a HuggingFace model
            is_hf_model = hasattr(model, 'config') and hasattr(model.config, 'to_dict')
            
            if not is_hf_model:
                return {}
            
            # Get model parameters
            num_params = sum(p.numel() for p in model.parameters())
            num_trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
            
            # Get model configuration
            config = model.config.to_dict()
            
            # Get model size in memory
            model_size_bytes = 0
            for param in model.parameters():
                model_size_bytes += param.nelement() * param.element_size()
            
            for buffer in model.buffers():
                model_size_bytes += buffer.nelement() * buffer.element_size()
            
            # Convert to MB
            model_size_mb = model_size_bytes / (1024 * 1024)
            
            return {
                'num_params': num_params,
                'num_trainable_params': num_trainable_params,
                'model_size_mb': model_size_mb,
                'model_type': model.__class__.__name__,
                'config': config
            }
        
        except Exception as e:
            logger.error(f"Error getting HuggingFace model info: {e}")
            return {}
    
    def get_trainer_info(self, trainer):
        """
        Get information about a HuggingFace trainer.
        
        Args:
            trainer: HuggingFace trainer
            
        Returns:
            Dictionary of trainer information
        """
        if not self.is_available or trainer is None:
            return {}
        
        try:
            # Get trainer arguments
            args = trainer.args.to_dict() if hasattr(trainer, 'args') and hasattr(trainer.args, 'to_dict') else {}
            
            # Get model information
            model_info = self.get_model_info(trainer.model) if hasattr(trainer, 'model') else {}
            
            # Get optimizer information
            optimizer_info = {}
            if hasattr(trainer, 'optimizer') and trainer.optimizer:
                optimizer_type = trainer.optimizer.__class__.__name__
                
                param_groups = []
                for i, group in enumerate(trainer.optimizer.param_groups):
                    group_info = {}
                    
                    for key, value in group.items():
                        if key == 'params':
                            group_info['num_params'] = len(value)
                        else:
                            group_info[key] = value
                    
                    param_groups.append(group_info)
                
                optimizer_info = {
                    'optimizer_type': optimizer_type,
                    'param_groups': param_groups
                }
            
            return {
                'args': args,
                'model': model_info,
                'optimizer': optimizer_info
            }
        
        except Exception as e:
            logger.error(f"Error getting HuggingFace trainer info: {e}")
            return {}

class DeepSpeedIntegration:
    """
    Integration with DeepSpeed.
    
    This class provides integration with DeepSpeed for distributed training.
    """
    
    def __init__(self):
        """Initialize the DeepSpeed integration."""
        try:
            import deepspeed
            self.deepspeed = deepspeed
            self.is_available = True
            logger.info(f"DeepSpeed integration initialized (version {deepspeed.__version__})")
        except ImportError:
            self.deepspeed = None
            self.is_available = False
            logger.warning("DeepSpeed not installed. DeepSpeed integration not available.")
    
    def get_engine_info(self, engine):
        """
        Get information about a DeepSpeed engine.
        
        Args:
            engine: DeepSpeed engine
            
        Returns:
            Dictionary of engine information
        """
        if not self.is_available or engine is None:
            return {}
        
        try:
            # Check if it's a DeepSpeed engine
            is_ds_engine = hasattr(engine, 'module') and hasattr(engine, 'optimizer')
            
            if not is_ds_engine:
                return {}
            
            # Get model information
            model_info = {}
            if hasattr(engine, 'module'):
                model = engine.module
                model_info = {
                    'num_params': sum(p.numel() for p in model.parameters()),
                    'num_trainable_params': sum(p.numel() for p in model.parameters() if p.requires_grad),
                    'model_type': model.__class__.__name__
                }
            
            # Get optimizer information
            optimizer_info = {}
            if hasattr(engine, 'optimizer') and engine.optimizer:
                optimizer_type = engine.optimizer.__class__.__name__
                optimizer_info = {
                    'optimizer_type': optimizer_type
                }
            
            # Get DeepSpeed configuration
            config = {}
            if hasattr(engine, 'config'):
                config = engine.config
            
            # Get ZeRO information
            zero_info = {}
            if 'zero_optimization' in config:
                zero_info = config['zero_optimization']
            
            return {
                'model': model_info,
                'optimizer': optimizer_info,
                'zero_stage': zero_info.get('stage', 0) if zero_info else 0,
                'offload': zero_info.get('offload_optimizer', False) if zero_info else False,
                'config': config
            }
        
        except Exception as e:
            logger.error(f"Error getting DeepSpeed engine info: {e}")
            return {}
    
    def create_callback(self, doctor):
        """
        Create a DeepSpeed callback for monitoring.
        
        Args:
            doctor: AutoPipelineDoctor instance
            
        Returns:
            DeepSpeed callback
        """
        if not self.is_available:
            return None
        
        # Create a callback class
        class AutoPDCallback:
            def __init__(self, doctor):
                self.doctor = doctor
                self.step_times = []
                self.forward_times = []
                self.backward_times = []
                self.optimizer_times = []
            
            def on_step_begin(self, engine):
                self.step_start_time = time.time()
            
            def on_step_end(self, engine):
                step_time = time.time() - self.step_start_time
                self.step_times.append(step_time)
                
                # Keep only the last 100 times
                if len(self.step_times) > 100:
                    self.step_times = self.step_times[-100:]
                
                # Add step metrics
                step_metrics = {
                    'step_time': step_time,
                    'avg_step_time': sum(self.step_times) / len(self.step_times)
                }
                
                self.doctor.add_metrics('step', step_metrics)
            
            def on_forward_begin(self, engine):
                self.forward_start_time = time.time()
            
            def on_forward_end(self, engine):
                forward_time = time.time() - self.forward_start_time
                self.forward_times.append(forward_time)
                
                # Keep only the last 100 times
                if len(self.forward_times) > 100:
                    self.forward_times = self.forward_times[-100:]
                
                # Add forward metrics
                forward_metrics = {
                    'forward_time': forward_time,
                    'avg_forward_time': sum(self.forward_times) / len(self.forward_times)
                }
                
                self.doctor.add_metrics('forward', forward_metrics)
            
            def on_backward_begin(self, engine):
                self.backward_start_time = time.time()
            
            def on_backward_end(self, engine):
                backward_time = time.time() - self.backward_start_time
                self.backward_times.append(backward_time)
                
                # Keep only the last 100 times
                if len(self.backward_times) > 100:
                    self.backward_times = self.backward_times[-100:]
                
                # Add backward metrics
                backward_metrics = {
                    'backward_time': backward_time,
                    'avg_backward_time': sum(self.backward_times) / len(self.backward_times)
                }
                
                self.doctor.add_metrics('backward', backward_metrics)
            
            def on_optimizer_step_begin(self, engine):
                self.optimizer_start_time = time.time()
            
            def on_optimizer_step_end(self, engine):
                optimizer_time = time.time() - self.optimizer_start_time
                self.optimizer_times.append(optimizer_time)
                
                # Keep only the last 100 times
                if len(self.optimizer_times) > 100:
                    self.optimizer_times = self.optimizer_times[-100:]
                
                # Add optimizer metrics
                optimizer_metrics = {
                    'optimizer_time': optimizer_time,
                    'avg_optimizer_time': sum(self.optimizer_times) / len(self.optimizer_times)
                }
                
                self.doctor.add_metrics('optimizer', optimizer_metrics)
        
        return AutoPDCallback(doctor)
    
    def patch_engine(self, engine, callback):
        """
        Patch a DeepSpeed engine with the callback.
        
        Args:
            engine: DeepSpeed engine
            callback: DeepSpeed callback
            
        Returns:
            Patched engine
        """
        if not self.is_available or engine is None or callback is None:
            return engine
        
        try:
            # Store original methods
            original_step = engine.step
            original_forward = engine.forward
            original_backward = engine.backward
            original_optimizer_step = engine.optimizer_step
            
            # Patch step method
            @wraps(original_step)
            def patched_step(closure=None):
                callback.on_step_begin(engine)
                result = original_step(closure)
                callback.on_step_end(engine)
                return result
            
            # Patch forward method
            @wraps(original_forward)
            def patched_forward(*args, **kwargs):
                callback.on_forward_begin(engine)
                result = original_forward(*args, **kwargs)
                callback.on_forward_end(engine)
                return result
            
            # Patch backward method
            @wraps(original_backward)
            def patched_backward(*args, **kwargs):
                callback.on_backward_begin(engine)
                result = original_backward(*args, **kwargs)
                callback.on_backward_end(engine)
                return result
            
            # Patch optimizer_step method
            @wraps(original_optimizer_step)
            def patched_optimizer_step(*args, **kwargs):
                callback.on_optimizer_step_begin(engine)
                result = original_optimizer_step(*args, **kwargs)
                callback.on_optimizer_step_end(engine)
                return result
            
            # Replace methods
            engine.step = patched_step
            engine.forward = patched_forward
            engine.backward = patched_backward
            engine.optimizer_step = patched_optimizer_step
            
            # Mark as patched
            engine._autopd_patched = True
            
            return engine
        
        except Exception as e:
            logger.error(f"Error patching DeepSpeed engine: {e}")
            return engine

class TorchDynamoIntegration:
    """
    Integration with TorchDynamo and TorchCompile.
    
    This class provides integration with TorchDynamo and TorchCompile for compiled models.
    """
    
    def __init__(self):
        """Initialize the TorchDynamo integration."""
        try:
            import torch
            if hasattr(torch, '_dynamo') and hasattr(torch, 'compile'):
                self.torch = torch
                self.is_available = True
                logger.info(f"TorchDynamo integration initialized (PyTorch version {torch.__version__})")
            else:
                self.torch = None
                self.is_available = False
                logger.warning("TorchDynamo not available in this PyTorch version.")
        except ImportError:
            self.torch = None
            self.is_available = False
            logger.warning("PyTorch not installed. TorchDynamo integration not available.")
    
    def patch_compile(self, doctor):
        """
        Patch torch.compile to monitor compilation and execution.
        
        Args:
            doctor: AutoPipelineDoctor instance
            
        Returns:
            True if patched successfully, False otherwise
        """
        if not self.is_available:
            return False
        
        try:
            original_compile = self.torch.compile
            
            @wraps(original_compile)
            def patched_compile(model, *args, **kwargs):
                # Record compilation start time
                compile_start_time = time.time()
                
                # Call original compile
                compiled_model = original_compile(model, *args, **kwargs)
                
                # Record compilation end time
                compile_end_time = time.time()
                compile_time = compile_end_time - compile_start_time
                
                # Add compilation metrics
                compilation_metrics = {
                    'compile_time': compile_time,
                    'backend': kwargs.get('backend', 'inductor'),
                    'mode': kwargs.get('mode', 'default'),
                    'fullgraph': kwargs.get('fullgraph', False),
                    'dynamic': kwargs.get('dynamic', False)
                }
                
                doctor.add_metrics('compilation', compilation_metrics)
                
                # Store original forward
                original_forward = compiled_model.forward
                
                # Create a wrapper for the forward method
                @wraps(original_forward)
                def wrapped_forward(*fargs, **fkwargs):
                    # Record start time
                    start_time = time.time()
                    
                    # Call original forward
                    output = original_forward(*fargs, **fkwargs)
                    
                    # Record end time
                    end_time = time.time()
                    
                    # Store timing information
                    if not hasattr(compiled_model, '_autopd_stats'):
                        compiled_model._autopd_stats = {
                            'forward_times': []
                        }
                    
                    compiled_model._autopd_stats['forward_times'].append(end_time - start_time)
                    
                    # Keep only the last 100 times
                    if len(compiled_model._autopd_stats['forward_times']) > 100:
                        compiled_model._autopd_stats['forward_times'] = compiled_model._autopd_stats['forward_times'][-100:]
                    
                    # Add metrics
                    forward_metrics = {
                        'forward_time': end_time - start_time,
                        'avg_forward_time': sum(compiled_model._autopd_stats['forward_times']) / len(compiled_model._autopd_stats['forward_times']),
                        'compiled': True
                    }
                    
                    doctor.add_metrics('compiled_forward', forward_metrics)
                    
                    return output
                
                # Replace forward method
                compiled_model.forward = wrapped_forward
                
                # Mark as patched
                compiled_model._autopd_patched = True
                
                return compiled_model
            
            # Replace torch.compile
            self.torch.compile = patched_compile
            
            return True
        
        except Exception as e:
            logger.error(f"Error patching torch.compile: {e}")
            return False
    
    def get_dynamo_stats(self):
        """
        Get TorchDynamo statistics.
        
        Returns:
            Dictionary of TorchDynamo statistics
        """
        if not self.is_available:
            return {}
        
        try:
            # Check if counters are available
            if hasattr(self.torch._dynamo, 'utils') and hasattr(self.torch._dynamo.utils, 'counters'):
                counters = self.torch._dynamo.utils.counters
                
                # Get counter values
                stats = {}
                
                for name, value in counters.items():
                    stats[name] = value
                
                return stats
            
            return {}
        
        except Exception as e:
            logger.error(f"Error getting TorchDynamo stats: {e}")
            return {}
