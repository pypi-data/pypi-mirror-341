"""
Hardware-Aware Learning Curve Forecasting (HALCF) module for AutoPipelineDoctor.

This advanced module learns the relationship between hardware specifications, dataset size,
model architecture, and batch size to predict epoch time, optimal resource allocation,
and saturation points for ML training.
"""

import torch
import torch.nn as nn
import numpy as np
import pandas as pd
import logging
import time
import os
import json
import copy
from typing import Dict, List, Tuple, Optional, Union, Any, Callable, Set
from enum import Enum
import threading
from collections import defaultdict, deque
import pickle
import math
import random
from dataclasses import dataclass, field
import re
import platform
import subprocess
import psutil
import warnings
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import ElasticNet
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import mean_squared_error, r2_score
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.optimize import curve_fit

logger = logging.getLogger(__name__)


class HardwareType(Enum):
    """Types of hardware configurations."""
    CPU = "cpu"
    GPU = "gpu"
    TPU = "tpu"
    HYBRID = "hybrid"
    CUSTOM = "custom"


class ModelArchitectureType(Enum):
    """Types of model architectures."""
    CNN = "cnn"
    RNN = "rnn"
    TRANSFORMER = "transformer"
    MLP = "mlp"
    HYBRID = "hybrid"
    CUSTOM = "custom"


class DatasetType(Enum):
    """Types of datasets."""
    IMAGE = "image"
    TEXT = "text"
    TABULAR = "tabular"
    AUDIO = "audio"
    VIDEO = "video"
    MULTIMODAL = "multimodal"
    CUSTOM = "custom"


class PredictionType(Enum):
    """Types of predictions."""
    EPOCH_TIME = "epoch_time"
    BATCH_TIME = "batch_time"
    MEMORY_USAGE = "memory_usage"
    THROUGHPUT = "throughput"
    SATURATION_POINT = "saturation_point"
    OPTIMAL_BATCH_SIZE = "optimal_batch_size"
    OPTIMAL_WORKERS = "optimal_workers"
    RESOURCE_ALLOCATION = "resource_allocation"
    CUSTOM = "custom"


@dataclass
class HardwareProfile:
    """Hardware profile information."""
    hardware_type: HardwareType
    cpu_info: Dict[str, Any] = field(default_factory=dict)
    gpu_info: Dict[str, Any] = field(default_factory=dict)
    tpu_info: Dict[str, Any] = field(default_factory=dict)
    memory_info: Dict[str, Any] = field(default_factory=dict)
    storage_info: Dict[str, Any] = field(default_factory=dict)
    network_info: Dict[str, Any] = field(default_factory=dict)
    custom_info: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ModelArchitectureProfile:
    """Model architecture profile information."""
    architecture_type: ModelArchitectureType
    num_parameters: int = 0
    num_layers: int = 0
    input_shape: Tuple[int, ...] = field(default_factory=tuple)
    output_shape: Tuple[int, ...] = field(default_factory=tuple)
    memory_footprint: int = 0  # in bytes
    flops: int = 0  # floating point operations per forward pass
    custom_info: Dict[str, Any] = field(default_factory=dict)


@dataclass
class DatasetProfile:
    """Dataset profile information."""
    dataset_type: DatasetType
    num_samples: int = 0
    sample_shape: Tuple[int, ...] = field(default_factory=tuple)
    memory_footprint: int = 0  # in bytes per sample
    preprocessing_complexity: float = 1.0  # relative complexity of preprocessing
    custom_info: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TrainingProfile:
    """Training profile information."""
    batch_size: int
    num_workers: int = 0
    optimizer_type: str = "adam"
    learning_rate: float = 0.001
    mixed_precision: bool = False
    distributed_training: bool = False
    gradient_accumulation_steps: int = 1
    custom_info: Dict[str, Any] = field(default_factory=dict)


@dataclass
class PerformanceRecord:
    """Performance record for a training run."""
    hardware_profile: HardwareProfile
    model_profile: ModelArchitectureProfile
    dataset_profile: DatasetProfile
    training_profile: TrainingProfile
    epoch_time: float = 0.0
    batch_time: float = 0.0
    memory_usage: float = 0.0
    throughput: float = 0.0  # samples per second
    saturation_point: Optional[int] = None  # batch size at saturation
    timestamp: float = field(default_factory=time.time)
    custom_metrics: Dict[str, Any] = field(default_factory=dict)


class HardwareAwareLearningCurveForecasting:
    """
    Hardware-Aware Learning Curve Forecasting (HALCF) for predicting training performance.
    
    This module learns the relationship between hardware specifications, dataset size,
    model architecture, and batch size to predict epoch time, optimal resource allocation,
    and saturation points for ML training.
    
    Attributes:
        hardware_profile: Current hardware profile
        performance_records: Historical performance records
        prediction_models: Trained prediction models
        feature_extractors: Feature extraction functions
        feature_scalers: Feature scaling transformers
        metrics: Metrics collected by the module
        predictions: Predictions made by the module
    """
    
    def __init__(
        self,
        hardware_profile: Optional[HardwareProfile] = None,
        load_pretrained: bool = True,
        pretrained_path: Optional[str] = None,
    ):
        """
        Initialize the HardwareAwareLearningCurveForecasting module.
        
        Args:
            hardware_profile: Current hardware profile
            load_pretrained: Whether to load pretrained prediction models
            pretrained_path: Path to pretrained models
        """
        # Initialize hardware profile
        self.hardware_profile = hardware_profile or self._detect_hardware()
        
        # Initialize performance records
        self.performance_records: List[PerformanceRecord] = []
        
        # Initialize prediction models
        self.prediction_models: Dict[str, Any] = {}
        
        # Initialize feature extractors
        self.feature_extractors: Dict[str, Callable] = self._create_feature_extractors()
        
        # Initialize feature scalers
        self.feature_scalers: Dict[str, Any] = {}
        
        # Initialize metrics and predictions
        self.metrics: Dict[str, Any] = {}
        self.predictions: Dict[str, Any] = {}
        
        # Initialize performance metrics
        self.performance_metrics: Dict[str, Any] = {
            "prediction_time": 0.0,
            "training_time": 0.0,
            "feature_extraction_time": 0.0,
            "prediction_accuracy": {},
        }
        
        # Initialize database connection
        self.db_connection = None
        
        # Load pretrained models if requested
        if load_pretrained:
            self._load_pretrained_models(pretrained_path)
        
        logger.info("Initialized HardwareAwareLearningCurveForecasting")
    
    def _detect_hardware(self) -> HardwareProfile:
        """
        Detect hardware configuration.
        
        Returns:
            Hardware profile
        """
        logger.info("Detecting hardware configuration")
        
        # Initialize hardware profile
        hardware_profile = HardwareProfile(hardware_type=HardwareType.CPU)
        
        try:
            # Detect CPU information
            cpu_info = {
                "processor": platform.processor(),
                "architecture": platform.machine(),
                "num_physical_cores": psutil.cpu_count(logical=False),
                "num_logical_cores": psutil.cpu_count(logical=True),
                "frequency": psutil.cpu_freq().max if psutil.cpu_freq() else None,
            }
            
            # Try to get more detailed CPU info on Linux
            if platform.system() == "Linux":
                try:
                    # Get CPU model name
                    with open("/proc/cpuinfo", "r") as f:
                        for line in f:
                            if "model name" in line:
                                cpu_info["model_name"] = line.split(":")[1].strip()
                                break
                except Exception as e:
                    logger.warning(f"Failed to get detailed CPU info: {e}")
            
            hardware_profile.cpu_info = cpu_info
            
            # Detect memory information
            memory = psutil.virtual_memory()
            hardware_profile.memory_info = {
                "total": memory.total,
                "available": memory.available,
                "used": memory.used,
                "percent": memory.percent,
            }
            
            # Detect storage information
            disk = psutil.disk_usage("/")
            hardware_profile.storage_info = {
                "total": disk.total,
                "used": disk.used,
                "free": disk.free,
                "percent": disk.percent,
            }
            
            # Detect GPU information if available
            try:
                import torch
                
                if torch.cuda.is_available():
                    hardware_profile.hardware_type = HardwareType.GPU
                    
                    gpu_info = {
                        "num_gpus": torch.cuda.device_count(),
                        "cuda_version": torch.version.cuda,
                        "devices": [],
                    }
                    
                    for i in range(torch.cuda.device_count()):
                        device_info = {
                            "name": torch.cuda.get_device_name(i),
                            "capability": torch.cuda.get_device_capability(i),
                            "total_memory": torch.cuda.get_device_properties(i).total_memory,
                        }
                        gpu_info["devices"].append(device_info)
                    
                    hardware_profile.gpu_info = gpu_info
                    
                    # Try to get more detailed GPU info on Linux
                    if platform.system() == "Linux":
                        try:
                            # Use nvidia-smi to get more detailed GPU info
                            result = subprocess.run(
                                ["nvidia-smi", "--query-gpu=name,memory.total,memory.free,memory.used,temperature.gpu,utilization.gpu", "--format=csv,noheader,nounits"],
                                capture_output=True,
                                text=True,
                            )
                            
                            if result.returncode == 0:
                                lines = result.stdout.strip().split("\n")
                                for i, line in enumerate(lines):
                                    if i < len(gpu_info["devices"]):
                                        values = [v.strip() for v in line.split(",")]
                                        if len(values) >= 6:
                                            gpu_info["devices"][i]["memory_total_mb"] = float(values[1])
                                            gpu_info["devices"][i]["memory_free_mb"] = float(values[2])
                                            gpu_info["devices"][i]["memory_used_mb"] = float(values[3])
                                            gpu_info["devices"][i]["temperature"] = float(values[4])
                                            gpu_info["devices"][i]["utilization"] = float(values[5])
                        except Exception as e:
                            logger.warning(f"Failed to get detailed GPU info: {e}")
            except ImportError:
                logger.warning("PyTorch not available, cannot detect GPU information")
            
            # Detect TPU information if available
            try:
                import torch_xla.core.xla_model as xm
                
                hardware_profile.hardware_type = HardwareType.TPU
                
                tpu_info = {
                    "num_devices": xm.xrt_world_size(),
                    "device_type": "TPU",
                }
                
                hardware_profile.tpu_info = tpu_info
            except ImportError:
                # TPU support not available
                pass
            
            # Detect network information
            try:
                net_io = psutil.net_io_counters()
                hardware_profile.network_info = {
                    "bytes_sent": net_io.bytes_sent,
                    "bytes_recv": net_io.bytes_recv,
                    "packets_sent": net_io.packets_sent,
                    "packets_recv": net_io.packets_recv,
                }
            except Exception as e:
                logger.warning(f"Failed to get network information: {e}")
            
            # Set hardware type based on detected devices
            if hardware_profile.tpu_info:
                hardware_profile.hardware_type = HardwareType.TPU
            elif hardware_profile.gpu_info:
                hardware_profile.hardware_type = HardwareType.GPU
            else:
                hardware_profile.hardware_type = HardwareType.CPU
        
        except Exception as e:
            logger.error(f"Error detecting hardware: {e}")
        
        return hardware_profile
    
    def _create_feature_extractors(self) -> Dict[str, Callable]:
        """
        Create feature extraction functions.
        
        Returns:
            Dictionary of feature extractors
        """
        extractors = {}
        
        # Hardware feature extractor
        def extract_hardware_features(hardware_profile: HardwareProfile) -> Dict[str, Any]:
            features = {
                "hardware_type": hardware_profile.hardware_type.value,
            }
            
            # CPU features
            if hardware_profile.cpu_info:
                features.update({
                    "cpu_cores": hardware_profile.cpu_info.get("num_logical_cores", 0),
                    "cpu_physical_cores": hardware_profile.cpu_info.get("num_physical_cores", 0),
                    "cpu_frequency": hardware_profile.cpu_info.get("frequency", 0),
                })
            
            # Memory features
            if hardware_profile.memory_info:
                features.update({
                    "memory_total": hardware_profile.memory_info.get("total", 0) / (1024 ** 3),  # GB
                    "memory_available": hardware_profile.memory_info.get("available", 0) / (1024 ** 3),  # GB
                })
            
            # GPU features
            if hardware_profile.gpu_info:
                features.update({
                    "num_gpus": hardware_profile.gpu_info.get("num_gpus", 0),
                })
                
                # Add features for first GPU
                if hardware_profile.gpu_info.get("devices"):
                    first_gpu = hardware_profile.gpu_info["devices"][0]
                    features.update({
                        "gpu_memory": first_gpu.get("total_memory", 0) / (1024 ** 3),  # GB
                    })
                    
                    # Add capability as a feature if available
                    if "capability" in first_gpu:
                        cap = first_gpu["capability"]
                        if isinstance(cap, (list, tuple)) and len(cap) >= 2:
                            features["gpu_capability"] = cap[0] + 0.1 * cap[1]
            
            # TPU features
            if hardware_profile.tpu_info:
                features.update({
                    "num_tpus": hardware_profile.tpu_info.get("num_devices", 0),
                })
            
            return features
        
        # Model architecture feature extractor
        def extract_model_features(model_profile: ModelArchitectureProfile) -> Dict[str, Any]:
            features = {
                "architecture_type": model_profile.architecture_type.value,
                "num_parameters": model_profile.num_parameters,
                "num_layers": model_profile.num_layers,
                "memory_footprint": model_profile.memory_footprint / (1024 ** 2),  # MB
                "flops": model_profile.flops,
            }
            
            # Add input shape as a feature
            if model_profile.input_shape:
                # For simplicity, use the product of dimensions as a feature
                features["input_size"] = np.prod(model_profile.input_shape)
            
            # Add output shape as a feature
            if model_profile.output_shape:
                # For simplicity, use the product of dimensions as a feature
                features["output_size"] = np.prod(model_profile.output_shape)
            
            return features
        
        # Dataset feature extractor
        def extract_dataset_features(dataset_profile: DatasetProfile) -> Dict[str, Any]:
            features = {
                "dataset_type": dataset_profile.dataset_type.value,
                "num_samples": dataset_profile.num_samples,
                "memory_footprint": dataset_profile.memory_footprint,
                "preprocessing_complexity": dataset_profile.preprocessing_complexity,
            }
            
            # Add sample shape as a feature
            if dataset_profile.sample_shape:
                # For simplicity, use the product of dimensions as a feature
                features["sample_size"] = np.prod(dataset_profile.sample_shape)
            
            return features
        
        # Training feature extractor
        def extract_training_features(training_profile: TrainingProfile) -> Dict[str, Any]:
            features = {
                "batch_size": training_profile.batch_size,
                "num_workers": training_profile.num_workers,
                "optimizer_type": training_profile.optimizer_type,
                "learning_rate": training_profile.learning_rate,
                "mixed_precision": int(training_profile.mixed_precision),
                "distributed_training": int(training_profile.distributed_training),
                "gradient_accumulation_steps": training_profile.gradient_accumulation_steps,
            }
            
            return features
        
        # Combined feature extractor
        def extract_all_features(record: PerformanceRecord) -> Dict[str, Any]:
            features = {}
            
            # Extract features from each component
            hardware_features = extract_hardware_features(record.hardware_profile)
            model_features = extract_model_features(record.model_profile)
            dataset_features = extract_dataset_features(record.dataset_profile)
            training_features = extract_training_features(record.training_profile)
            
            # Combine all features
            features.update(hardware_features)
            features.update(model_features)
            features.update(dataset_features)
            features.update(training_features)
            
            # Add derived features
            features["samples_per_batch"] = features["batch_size"]
            features["total_samples"] = features["num_samples"]
            features["parameters_per_sample"] = features["num_parameters"] / features["sample_size"] if features.get("sample_size", 0) > 0 else 0
            features["memory_ratio"] = features["memory_footprint"] * features["batch_size"] / features["memory_total"] if features.get("memory_total", 0) > 0 else 0
            
            if "gpu_memory" in features and features["gpu_memory"] > 0:
                features["gpu_memory_ratio"] = features["memory_footprint"] * features["batch_size"] / (features["gpu_memory"] * 1024) if features.get("gpu_memory", 0) > 0 else 0
            
            return features
        
        # Register extractors
        extractors["hardware"] = extract_hardware_features
        extractors["model"] = extract_model_features
        extractors["dataset"] = extract_dataset_features
        extractors["training"] = extract_training_features
        extractors["all"] = extract_all_features
        
        return extractors
    
    def _load_pretrained_models(self, path: Optional[str] = None) -> None:
        """
        Load pretrained prediction models.
        
        Args:
            path: Path to pretrained models
        """
        # Default path if not provided
        if path is None:
            path = os.path.join(os.path.dirname(__file__), "pretrained")
        
        # Check if path exists
        if not os.path.exists(path):
            logger.warning(f"Pretrained models path does not exist: {path}")
            return
        
        # Load models for each prediction type
        for pred_type in PredictionType:
            model_path = os.path.join(path, f"{pred_type.value}_model.joblib")
            scaler_path = os.path.join(path, f"{pred_type.value}_scaler.joblib")
            
            if os.path.exists(model_path) and os.path.exists(scaler_path):
                try:
                    # Load model and scaler
                    model = joblib.load(model_path)
                    scaler = joblib.load(scaler_path)
                    
                    # Register model and scaler
                    self.prediction_models[pred_type.value] = model
                    self.feature_scalers[pred_type.value] = scaler
                    
                    logger.info(f"Loaded pretrained model for {pred_type.value}")
                except Exception as e:
                    logger.error(f"Failed to load pretrained model for {pred_type.value}: {e}")
    
    def register_hardware_profile(self, hardware_profile: HardwareProfile) -> None:
        """
        Register a hardware profile.
        
        Args:
            hardware_profile: Hardware profile to register
        """
        self.hardware_profile = hardware_profile
        logger.info("Registered hardware profile")
    
    def detect_model_architecture(self, model: nn.Module) -> ModelArchitectureProfile:
        """
        Detect model architecture profile.
        
        Args:
            model: PyTorch model
            
        Returns:
            Model architecture profile
        """
        logger.info("Detecting model architecture")
        
        # Initialize model profile
        model_profile = ModelArchitectureProfile(architecture_type=ModelArchitectureType.CUSTOM)
        
        try:
            # Count parameters
            num_parameters = sum(p.numel() for p in model.parameters() if p.requires_grad)
            model_profile.num_parameters = num_parameters
            
            # Estimate memory footprint (parameters + buffers)
            memory_footprint = 0
            for p in model.parameters():
                memory_footprint += p.numel() * p.element_size()
            for b in model.buffers():
                memory_footprint += b.numel() * b.element_size()
            model_profile.memory_footprint = memory_footprint
            
            # Count layers
            num_layers = 0
            for module in model.modules():
                if isinstance(module, (nn.Conv1d, nn.Conv2d, nn.Conv3d, nn.Linear, nn.LSTM, nn.GRU, nn.RNN, nn.Transformer)):
                    num_layers += 1
            model_profile.num_layers = num_layers
            
            # Determine architecture type
            if any(isinstance(module, (nn.Conv1d, nn.Conv2d, nn.Conv3d)) for module in model.modules()):
                if any(isinstance(module, (nn.LSTM, nn.GRU, nn.RNN)) for module in model.modules()):
                    model_profile.architecture_type = ModelArchitectureType.HYBRID
                else:
                    model_profile.architecture_type = ModelArchitectureType.CNN
            elif any(isinstance(module, (nn.LSTM, nn.GRU, nn.RNN)) for module in model.modules()):
                model_profile.architecture_type = ModelArchitectureType.RNN
            elif any(isinstance(module, nn.Transformer) for module in model.modules()) or "attention" in str(model).lower():
                model_profile.architecture_type = ModelArchitectureType.TRANSFORMER
            elif any(isinstance(module, nn.Linear) for module in model.modules()):
                model_profile.architecture_type = ModelArchitectureType.MLP
            
            # Estimate FLOPs (very rough approximation)
            flops = 0
            for module in model.modules():
                if isinstance(module, nn.Conv2d):
                    # For each output pixel, we do kernel_size*kernel_size*in_channels multiplications
                    # and (kernel_size*kernel_size*in_channels - 1) additions
                    kernel_size = module.kernel_size[0] * module.kernel_size[1]
                    output_size = (module.out_channels * module.kernel_size[0] * module.kernel_size[1]) // (module.stride[0] * module.stride[1])
                    flops += 2 * module.in_channels * kernel_size * output_size
                elif isinstance(module, nn.Linear):
                    # For each output, we do in_features multiplications and in_features-1 additions
                    flops += 2 * module.in_features * module.out_features
            model_profile.flops = flops
            
            # Try to determine input and output shapes
            # This is a best-effort approach and may not work for all models
            try:
                # Check if model has a forward_shape method
                if hasattr(model, "forward_shape") and callable(getattr(model, "forward_shape")):
                    input_shape, output_shape = model.forward_shape()
                    model_profile.input_shape = input_shape
                    model_profile.output_shape = output_shape
                else:
                    # Try to infer from the first and last layers
                    modules = list(model.modules())
                    
                    # Find first layer with input shape
                    for module in modules:
                        if hasattr(module, "in_features"):
                            model_profile.input_shape = (module.in_features,)
                            break
                        elif hasattr(module, "in_channels"):
                            # Assume standard input size for the architecture type
                            if model_profile.architecture_type == ModelArchitectureType.CNN:
                                model_profile.input_shape = (module.in_channels, 224, 224)
                            break
                    
                    # Find last layer with output shape
                    for module in reversed(modules):
                        if hasattr(module, "out_features"):
                            model_profile.output_shape = (module.out_features,)
                            break
                        elif hasattr(module, "out_channels"):
                            # Assume standard output size for the architecture type
                            if model_profile.architecture_type == ModelArchitectureType.CNN:
                                model_profile.output_shape = (module.out_channels, 1, 1)
                            break
            except Exception as e:
                logger.warning(f"Failed to determine input/output shapes: {e}")
        
        except Exception as e:
            logger.error(f"Error detecting model architecture: {e}")
        
        return model_profile
    
    def detect_dataset_profile(
        self,
        dataset: Any,
        dataloader: Optional[Any] = None,
        sample_batch: Optional[Any] = None,
    ) -> DatasetProfile:
        """
        Detect dataset profile.
        
        Args:
            dataset: Dataset object
            dataloader: DataLoader object
            sample_batch: Sample batch from the dataset
            
        Returns:
            Dataset profile
        """
        logger.info("Detecting dataset profile")
        
        # Initialize dataset profile
        dataset_profile = DatasetProfile(dataset_type=DatasetType.CUSTOM)
        
        try:
            # Get number of samples
            if hasattr(dataset, "__len__"):
                dataset_profile.num_samples = len(dataset)
            elif dataloader is not None and hasattr(dataloader, "dataset") and hasattr(dataloader.dataset, "__len__"):
                dataset_profile.num_samples = len(dataloader.dataset)
            
            # Get sample shape
            if sample_batch is not None:
                if isinstance(sample_batch, (list, tuple)) and len(sample_batch) > 0:
                    # Assume first element is input data
                    sample = sample_batch[0]
                    if isinstance(sample, torch.Tensor):
                        dataset_profile.sample_shape = tuple(sample.shape[1:])  # Remove batch dimension
                        
                        # Estimate memory footprint
                        dataset_profile.memory_footprint = sample.element_size() * np.prod(sample.shape[1:])
                else:
                    # Assume sample_batch is the input data
                    if isinstance(sample_batch, torch.Tensor):
                        dataset_profile.sample_shape = tuple(sample_batch.shape[1:])  # Remove batch dimension
                        
                        # Estimate memory footprint
                        dataset_profile.memory_footprint = sample_batch.element_size() * np.prod(sample_batch.shape[1:])
            elif hasattr(dataset, "__getitem__"):
                try:
                    # Try to get the first item
                    sample = dataset[0]
                    
                    if isinstance(sample, (list, tuple)) and len(sample) > 0:
                        # Assume first element is input data
                        data = sample[0]
                        if isinstance(data, torch.Tensor):
                            dataset_profile.sample_shape = tuple(data.shape)
                            
                            # Estimate memory footprint
                            dataset_profile.memory_footprint = data.element_size() * np.prod(data.shape)
                        elif isinstance(data, np.ndarray):
                            dataset_profile.sample_shape = tuple(data.shape)
                            
                            # Estimate memory footprint
                            dataset_profile.memory_footprint = data.itemsize * np.prod(data.shape)
                    elif isinstance(sample, torch.Tensor):
                        dataset_profile.sample_shape = tuple(sample.shape)
                        
                        # Estimate memory footprint
                        dataset_profile.memory_footprint = sample.element_size() * np.prod(sample.shape)
                    elif isinstance(sample, np.ndarray):
                        dataset_profile.sample_shape = tuple(sample.shape)
                        
                        # Estimate memory footprint
                        dataset_profile.memory_footprint = sample.itemsize * np.prod(sample.shape)
                except Exception as e:
                    logger.warning(f"Failed to get sample from dataset: {e}")
            
            # Determine dataset type
            if dataset_profile.sample_shape:
                if len(dataset_profile.sample_shape) == 3 and dataset_profile.sample_shape[0] in [1, 3, 4]:
                    # Likely image data (channels, height, width)
                    dataset_profile.dataset_type = DatasetType.IMAGE
                elif len(dataset_profile.sample_shape) == 1:
                    # Likely tabular or text data
                    dataset_profile.dataset_type = DatasetType.TABULAR
                elif len(dataset_profile.sample_shape) == 2:
                    # Could be text (sequence length, embedding dim) or audio (time, features)
                    dataset_profile.dataset_type = DatasetType.TEXT
                elif len(dataset_profile.sample_shape) == 4:
                    # Likely video data (frames, channels, height, width)
                    dataset_profile.dataset_type = DatasetType.VIDEO
            
            # Try to determine preprocessing complexity
            # This is a best-effort approach and may not be accurate
            dataset_profile.preprocessing_complexity = 1.0  # Default value
            
            # Check if dataset has a transform attribute
            if hasattr(dataset, "transform") and dataset.transform is not None:
                transform_str = str(dataset.transform)
                
                # Count the number of transforms
                num_transforms = len(re.findall(r"Compose\(|\)|\],", transform_str))
                
                # Adjust complexity based on number of transforms
                dataset_profile.preprocessing_complexity = max(1.0, num_transforms / 3)
                
                # Check for computationally expensive transforms
                if "Resize" in transform_str or "RandomResizedCrop" in transform_str:
                    dataset_profile.preprocessing_complexity += 0.5
                if "RandomAugment" in transform_str or "AutoAugment" in transform_str:
                    dataset_profile.preprocessing_complexity += 1.0
                if "ColorJitter" in transform_str:
                    dataset_profile.preprocessing_complexity += 0.3
                if "RandomAffine" in transform_str or "RandomRotation" in transform_str:
                    dataset_profile.preprocessing_complexity += 0.5
            
            # Check if dataloader has a collate_fn
            if dataloader is not None and hasattr(dataloader, "collate_fn") and dataloader.collate_fn is not None:
                # Custom collate functions may add complexity
                if dataloader.collate_fn.__name__ != "default_collate":
                    dataset_profile.preprocessing_complexity += 0.5
        
        except Exception as e:
            logger.error(f"Error detecting dataset profile: {e}")
        
        return dataset_profile
    
    def create_training_profile(
        self,
        batch_size: int,
        num_workers: int = 0,
        optimizer_type: str = "adam",
        learning_rate: float = 0.001,
        mixed_precision: bool = False,
        distributed_training: bool = False,
        gradient_accumulation_steps: int = 1,
        custom_info: Optional[Dict[str, Any]] = None,
    ) -> TrainingProfile:
        """
        Create a training profile.
        
        Args:
            batch_size: Batch size
            num_workers: Number of dataloader workers
            optimizer_type: Type of optimizer
            learning_rate: Learning rate
            mixed_precision: Whether mixed precision is used
            distributed_training: Whether distributed training is used
            gradient_accumulation_steps: Number of gradient accumulation steps
            custom_info: Custom information
            
        Returns:
            Training profile
        """
        return TrainingProfile(
            batch_size=batch_size,
            num_workers=num_workers,
            optimizer_type=optimizer_type,
            learning_rate=learning_rate,
            mixed_precision=mixed_precision,
            distributed_training=distributed_training,
            gradient_accumulation_steps=gradient_accumulation_steps,
            custom_info=custom_info or {},
        )
    
    def record_performance(
        self,
        model_profile: ModelArchitectureProfile,
        dataset_profile: DatasetProfile,
        training_profile: TrainingProfile,
        epoch_time: float,
        batch_time: float,
        memory_usage: float,
        throughput: Optional[float] = None,
        saturation_point: Optional[int] = None,
        custom_metrics: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Record performance for a training run.
        
        Args:
            model_profile: Model architecture profile
            dataset_profile: Dataset profile
            training_profile: Training profile
            epoch_time: Time per epoch in seconds
            batch_time: Time per batch in seconds
            memory_usage: Memory usage in bytes
            throughput: Throughput in samples per second
            saturation_point: Batch size at saturation
            custom_metrics: Custom metrics
        """
        # Calculate throughput if not provided
        if throughput is None and batch_time > 0:
            throughput = training_profile.batch_size / batch_time
        
        # Create performance record
        record = PerformanceRecord(
            hardware_profile=self.hardware_profile,
            model_profile=model_profile,
            dataset_profile=dataset_profile,
            training_profile=training_profile,
            epoch_time=epoch_time,
            batch_time=batch_time,
            memory_usage=memory_usage,
            throughput=throughput or 0.0,
            saturation_point=saturation_point,
            timestamp=time.time(),
            custom_metrics=custom_metrics or {},
        )
        
        # Add to performance records
        self.performance_records.append(record)
        
        logger.info(f"Recorded performance: epoch_time={epoch_time:.4f}s, batch_time={batch_time:.4f}s, throughput={throughput:.2f} samples/s")
        
        # Update prediction models if we have enough records
        if len(self.performance_records) >= 10:
            self._update_prediction_models()
    
    def _update_prediction_models(self) -> None:
        """Update prediction models with current performance records."""
        logger.info("Updating prediction models")
        
        start_time = time.time()
        
        # Extract features and targets from performance records
        features_list = []
        targets = {
            PredictionType.EPOCH_TIME.value: [],
            PredictionType.BATCH_TIME.value: [],
            PredictionType.MEMORY_USAGE.value: [],
            PredictionType.THROUGHPUT.value: [],
            PredictionType.SATURATION_POINT.value: [],
        }
        
        for record in self.performance_records:
            # Extract features
            features = self.feature_extractors["all"](record)
            features_list.append(features)
            
            # Extract targets
            targets[PredictionType.EPOCH_TIME.value].append(record.epoch_time)
            targets[PredictionType.BATCH_TIME.value].append(record.batch_time)
            targets[PredictionType.MEMORY_USAGE.value].append(record.memory_usage)
            targets[PredictionType.THROUGHPUT.value].append(record.throughput)
            
            if record.saturation_point is not None:
                targets[PredictionType.SATURATION_POINT.value].append(record.saturation_point)
        
        # Convert features to DataFrame
        features_df = pd.DataFrame(features_list)
        
        # Train models for each prediction type
        for pred_type, target_values in targets.items():
            if not target_values:
                continue
            
            # Skip if we don't have enough data
            if len(target_values) < 5:
                logger.warning(f"Not enough data to train model for {pred_type}")
                continue
            
            try:
                # Convert target to numpy array
                y = np.array(target_values)
                
                # Select relevant features
                X = features_df.copy()
                
                # Handle categorical features
                cat_features = [col for col in X.columns if X[col].dtype == 'object']
                num_features = [col for col in X.columns if col not in cat_features]
                
                # Create preprocessing pipeline
                preprocessor = ColumnTransformer(
                    transformers=[
                        ('num', StandardScaler(), num_features),
                        ('cat', OneHotEncoder(handle_unknown='ignore'), cat_features)
                    ])
                
                # Create model pipeline
                if pred_type == PredictionType.SATURATION_POINT.value:
                    # For saturation point, use gradient boosting
                    model = Pipeline([
                        ('preprocessor', preprocessor),
                        ('regressor', GradientBoostingRegressor(random_state=42))
                    ])
                else:
                    # For other targets, use random forest
                    model = Pipeline([
                        ('preprocessor', preprocessor),
                        ('regressor', RandomForestRegressor(random_state=42))
                    ])
                
                # Train model
                model.fit(X, y)
                
                # Save model and preprocessor
                self.prediction_models[pred_type] = model
                self.feature_scalers[pred_type] = preprocessor
                
                # Evaluate model
                y_pred = model.predict(X)
                mse = mean_squared_error(y, y_pred)
                r2 = r2_score(y, y_pred)
                
                # Store metrics
                self.performance_metrics["prediction_accuracy"][pred_type] = {
                    "mse": mse,
                    "rmse": np.sqrt(mse),
                    "r2": r2,
                }
                
                logger.info(f"Trained model for {pred_type}: MSE={mse:.4f}, R2={r2:.4f}")
            
            except Exception as e:
                logger.error(f"Failed to train model for {pred_type}: {e}")
        
        # Update training time
        self.performance_metrics["training_time"] = time.time() - start_time
    
    def predict(
        self,
        model_profile: ModelArchitectureProfile,
        dataset_profile: DatasetProfile,
        training_profile: TrainingProfile,
        prediction_type: PredictionType = PredictionType.EPOCH_TIME,
        hardware_profile: Optional[HardwareProfile] = None,
    ) -> Dict[str, Any]:
        """
        Make a prediction for a specific configuration.
        
        Args:
            model_profile: Model architecture profile
            dataset_profile: Dataset profile
            training_profile: Training profile
            prediction_type: Type of prediction to make
            hardware_profile: Hardware profile (uses current hardware if None)
            
        Returns:
            Prediction results
        """
        start_time = time.time()
        
        # Use current hardware profile if not provided
        hardware_profile = hardware_profile or self.hardware_profile
        
        # Check if we have a model for this prediction type
        if prediction_type.value not in self.prediction_models:
            return {
                "error": f"No prediction model available for {prediction_type.value}",
                "value": None,
                "confidence": 0.0,
            }
        
        # Create performance record for feature extraction
        record = PerformanceRecord(
            hardware_profile=hardware_profile,
            model_profile=model_profile,
            dataset_profile=dataset_profile,
            training_profile=training_profile,
            epoch_time=0.0,
            batch_time=0.0,
            memory_usage=0.0,
            throughput=0.0,
        )
        
        # Extract features
        features = self.feature_extractors["all"](record)
        
        # Convert features to DataFrame
        features_df = pd.DataFrame([features])
        
        # Make prediction
        try:
            model = self.prediction_models[prediction_type.value]
            prediction = model.predict(features_df)[0]
            
            # Calculate confidence (simplified approach)
            confidence = 0.8  # Default confidence
            
            # Adjust confidence based on similarity to training data
            if len(self.performance_records) > 0:
                # Find most similar record in training data
                similarity_scores = []
                
                for train_record in self.performance_records:
                    train_features = self.feature_extractors["all"](train_record)
                    
                    # Calculate similarity score (simplified)
                    score = 0.0
                    count = 0
                    
                    for key in features:
                        if key in train_features and isinstance(features[key], (int, float)) and isinstance(train_features[key], (int, float)):
                            # Calculate relative difference
                            if abs(features[key]) > 1e-10 and abs(train_features[key]) > 1e-10:
                                diff = abs(features[key] - train_features[key]) / max(abs(features[key]), abs(train_features[key]))
                                score += 1.0 - min(1.0, diff)
                                count += 1
                    
                    if count > 0:
                        score /= count
                        similarity_scores.append(score)
                
                if similarity_scores:
                    # Use maximum similarity as confidence factor
                    max_similarity = max(similarity_scores)
                    confidence = max(0.5, min(0.95, max_similarity))
            
            # Adjust confidence based on model accuracy
            if prediction_type.value in self.performance_metrics["prediction_accuracy"]:
                r2 = self.performance_metrics["prediction_accuracy"][prediction_type.value].get("r2", 0.0)
                confidence = confidence * (0.5 + 0.5 * max(0.0, min(1.0, r2)))
            
            # Store prediction
            result = {
                "value": float(prediction),
                "confidence": float(confidence),
                "prediction_time": time.time() - start_time,
            }
            
            # Add prediction to metrics
            self.predictions[prediction_type.value] = result
            
            return result
        
        except Exception as e:
            logger.error(f"Prediction error for {prediction_type.value}: {e}")
            return {
                "error": str(e),
                "value": None,
                "confidence": 0.0,
            }
    
    def predict_optimal_batch_size(
        self,
        model_profile: ModelArchitectureProfile,
        dataset_profile: DatasetProfile,
        min_batch_size: int = 1,
        max_batch_size: int = 512,
        num_steps: int = 10,
        optimization_target: str = "throughput",
        hardware_profile: Optional[HardwareProfile] = None,
    ) -> Dict[str, Any]:
        """
        Predict the optimal batch size for a given configuration.
        
        Args:
            model_profile: Model architecture profile
            dataset_profile: Dataset profile
            min_batch_size: Minimum batch size to consider
            max_batch_size: Maximum batch size to consider
            num_steps: Number of batch sizes to evaluate
            optimization_target: Target metric to optimize ("throughput" or "memory")
            hardware_profile: Hardware profile (uses current hardware if None)
            
        Returns:
            Prediction results with optimal batch size
        """
        # Use current hardware profile if not provided
        hardware_profile = hardware_profile or self.hardware_profile
        
        # Generate batch sizes to evaluate
        batch_sizes = np.geomspace(min_batch_size, max_batch_size, num_steps).astype(int)
        batch_sizes = np.unique(batch_sizes)  # Remove duplicates
        
        # Initialize results
        results = {
            "batch_sizes": batch_sizes.tolist(),
            "throughput": [],
            "memory_usage": [],
            "batch_time": [],
            "optimal_batch_size": None,
            "optimal_value": None,
            "confidence": 0.0,
        }
        
        # Evaluate each batch size
        for batch_size in batch_sizes:
            # Create training profile
            training_profile = self.create_training_profile(batch_size=int(batch_size))
            
            # Predict throughput
            throughput_pred = self.predict(
                model_profile=model_profile,
                dataset_profile=dataset_profile,
                training_profile=training_profile,
                prediction_type=PredictionType.THROUGHPUT,
                hardware_profile=hardware_profile,
            )
            
            # Predict memory usage
            memory_pred = self.predict(
                model_profile=model_profile,
                dataset_profile=dataset_profile,
                training_profile=training_profile,
                prediction_type=PredictionType.MEMORY_USAGE,
                hardware_profile=hardware_profile,
            )
            
            # Predict batch time
            batch_time_pred = self.predict(
                model_profile=model_profile,
                dataset_profile=dataset_profile,
                training_profile=training_profile,
                prediction_type=PredictionType.BATCH_TIME,
                hardware_profile=hardware_profile,
            )
            
            # Store predictions
            results["throughput"].append(throughput_pred.get("value", 0.0))
            results["memory_usage"].append(memory_pred.get("value", 0.0))
            results["batch_time"].append(batch_time_pred.get("value", 0.0))
        
        # Find optimal batch size
        if optimization_target == "throughput":
            # Find batch size with maximum throughput
            if results["throughput"]:
                optimal_idx = np.argmax(results["throughput"])
                results["optimal_batch_size"] = int(batch_sizes[optimal_idx])
                results["optimal_value"] = results["throughput"][optimal_idx]
                
                # Calculate confidence as average of prediction confidences
                confidence = 0.0
                count = 0
                
                for batch_size in batch_sizes:
                    training_profile = self.create_training_profile(batch_size=int(batch_size))
                    pred = self.predict(
                        model_profile=model_profile,
                        dataset_profile=dataset_profile,
                        training_profile=training_profile,
                        prediction_type=PredictionType.THROUGHPUT,
                        hardware_profile=hardware_profile,
                    )
                    if "confidence" in pred:
                        confidence += pred["confidence"]
                        count += 1
                
                if count > 0:
                    results["confidence"] = confidence / count
        
        elif optimization_target == "memory":
            # Find largest batch size that doesn't exceed memory limits
            if results["memory_usage"]:
                # Get available memory
                available_memory = 0.0
                
                if hardware_profile.hardware_type == HardwareType.GPU and hardware_profile.gpu_info:
                    # Use GPU memory
                    if hardware_profile.gpu_info.get("devices"):
                        available_memory = hardware_profile.gpu_info["devices"][0].get("total_memory", 0.0)
                else:
                    # Use system memory
                    available_memory = hardware_profile.memory_info.get("total", 0.0)
                
                # Find largest batch size that uses less than 80% of available memory
                memory_threshold = 0.8 * available_memory
                valid_indices = [i for i, mem in enumerate(results["memory_usage"]) if mem < memory_threshold]
                
                if valid_indices:
                    optimal_idx = valid_indices[-1]  # Largest valid batch size
                    results["optimal_batch_size"] = int(batch_sizes[optimal_idx])
                    results["optimal_value"] = results["memory_usage"][optimal_idx]
                    
                    # Calculate confidence as average of prediction confidences
                    confidence = 0.0
                    count = 0
                    
                    for batch_size in batch_sizes:
                        training_profile = self.create_training_profile(batch_size=int(batch_size))
                        pred = self.predict(
                            model_profile=model_profile,
                            dataset_profile=dataset_profile,
                            training_profile=training_profile,
                            prediction_type=PredictionType.MEMORY_USAGE,
                            hardware_profile=hardware_profile,
                        )
                        if "confidence" in pred:
                            confidence += pred["confidence"]
                            count += 1
                    
                    if count > 0:
                        results["confidence"] = confidence / count
        
        return results
    
    def predict_optimal_workers(
        self,
        model_profile: ModelArchitectureProfile,
        dataset_profile: DatasetProfile,
        training_profile: TrainingProfile,
        min_workers: int = 0,
        max_workers: int = 16,
        hardware_profile: Optional[HardwareProfile] = None,
    ) -> Dict[str, Any]:
        """
        Predict the optimal number of dataloader workers.
        
        Args:
            model_profile: Model architecture profile
            dataset_profile: Dataset profile
            training_profile: Training profile
            min_workers: Minimum number of workers to consider
            max_workers: Maximum number of workers to consider
            hardware_profile: Hardware profile (uses current hardware if None)
            
        Returns:
            Prediction results with optimal number of workers
        """
        # Use current hardware profile if not provided
        hardware_profile = hardware_profile or self.hardware_profile
        
        # Generate worker counts to evaluate
        worker_counts = list(range(min_workers, max_workers + 1))
        
        # Initialize results
        results = {
            "worker_counts": worker_counts,
            "throughput": [],
            "batch_time": [],
            "optimal_workers": None,
            "optimal_value": None,
            "confidence": 0.0,
        }
        
        # Evaluate each worker count
        for num_workers in worker_counts:
            # Create training profile with current worker count
            current_profile = copy.deepcopy(training_profile)
            current_profile.num_workers = num_workers
            
            # Predict throughput
            throughput_pred = self.predict(
                model_profile=model_profile,
                dataset_profile=dataset_profile,
                training_profile=current_profile,
                prediction_type=PredictionType.THROUGHPUT,
                hardware_profile=hardware_profile,
            )
            
            # Predict batch time
            batch_time_pred = self.predict(
                model_profile=model_profile,
                dataset_profile=dataset_profile,
                training_profile=current_profile,
                prediction_type=PredictionType.BATCH_TIME,
                hardware_profile=hardware_profile,
            )
            
            # Store predictions
            results["throughput"].append(throughput_pred.get("value", 0.0))
            results["batch_time"].append(batch_time_pred.get("value", 0.0))
        
        # Find optimal worker count (maximum throughput)
        if results["throughput"]:
            optimal_idx = np.argmax(results["throughput"])
            results["optimal_workers"] = worker_counts[optimal_idx]
            results["optimal_value"] = results["throughput"][optimal_idx]
            
            # Calculate confidence as average of prediction confidences
            confidence = 0.0
            count = 0
            
            for num_workers in worker_counts:
                current_profile = copy.deepcopy(training_profile)
                current_profile.num_workers = num_workers
                
                pred = self.predict(
                    model_profile=model_profile,
                    dataset_profile=dataset_profile,
                    training_profile=current_profile,
                    prediction_type=PredictionType.THROUGHPUT,
                    hardware_profile=hardware_profile,
                )
                
                if "confidence" in pred:
                    confidence += pred["confidence"]
                    count += 1
            
            if count > 0:
                results["confidence"] = confidence / count
        
        # Add heuristic-based recommendation
        # Rule of thumb: use number of CPU cores for CPU-bound preprocessing
        cpu_cores = hardware_profile.cpu_info.get("num_logical_cores", 0)
        
        if cpu_cores > 0:
            # Adjust based on preprocessing complexity
            preprocessing_complexity = dataset_profile.preprocessing_complexity
            
            if preprocessing_complexity > 1.5:
                # Complex preprocessing benefits from more workers
                heuristic_workers = min(cpu_cores, max_workers)
            elif preprocessing_complexity > 0.5:
                # Moderate preprocessing
                heuristic_workers = min(cpu_cores // 2, max_workers)
            else:
                # Simple preprocessing
                heuristic_workers = min(2, max_workers)
            
            results["heuristic_recommendation"] = heuristic_workers
        
        return results
    
    def predict_saturation_curve(
        self,
        model_profile: ModelArchitectureProfile,
        dataset_profile: DatasetProfile,
        min_batch_size: int = 1,
        max_batch_size: int = 512,
        num_points: int = 20,
        hardware_profile: Optional[HardwareProfile] = None,
    ) -> Dict[str, Any]:
        """
        Predict the saturation curve for batch size vs. throughput.
        
        Args:
            model_profile: Model architecture profile
            dataset_profile: Dataset profile
            min_batch_size: Minimum batch size to consider
            max_batch_size: Maximum batch size to consider
            num_points: Number of points on the curve
            hardware_profile: Hardware profile (uses current hardware if None)
            
        Returns:
            Prediction results with saturation curve
        """
        # Use current hardware profile if not provided
        hardware_profile = hardware_profile or self.hardware_profile
        
        # Generate batch sizes to evaluate
        batch_sizes = np.geomspace(min_batch_size, max_batch_size, num_points).astype(int)
        batch_sizes = np.unique(batch_sizes)  # Remove duplicates
        
        # Initialize results
        results = {
            "batch_sizes": batch_sizes.tolist(),
            "throughput": [],
            "memory_usage": [],
            "batch_time": [],
            "saturation_point": None,
            "confidence": 0.0,
        }
        
        # Evaluate each batch size
        for batch_size in batch_sizes:
            # Create training profile
            training_profile = self.create_training_profile(batch_size=int(batch_size))
            
            # Predict throughput
            throughput_pred = self.predict(
                model_profile=model_profile,
                dataset_profile=dataset_profile,
                training_profile=training_profile,
                prediction_type=PredictionType.THROUGHPUT,
                hardware_profile=hardware_profile,
            )
            
            # Predict memory usage
            memory_pred = self.predict(
                model_profile=model_profile,
                dataset_profile=dataset_profile,
                training_profile=training_profile,
                prediction_type=PredictionType.MEMORY_USAGE,
                hardware_profile=hardware_profile,
            )
            
            # Predict batch time
            batch_time_pred = self.predict(
                model_profile=model_profile,
                dataset_profile=dataset_profile,
                training_profile=training_profile,
                prediction_type=PredictionType.BATCH_TIME,
                hardware_profile=hardware_profile,
            )
            
            # Store predictions
            results["throughput"].append(throughput_pred.get("value", 0.0))
            results["memory_usage"].append(memory_pred.get("value", 0.0))
            results["batch_time"].append(batch_time_pred.get("value", 0.0))
        
        # Detect saturation point
        if len(results["throughput"]) > 3:
            # Convert to numpy arrays
            batch_sizes_np = np.array(batch_sizes)
            throughput_np = np.array(results["throughput"])
            
            # Fit saturation curve
            try:
                # Define saturation function (Michaelis-Menten kinetics)
                def saturation_func(x, vmax, km):
                    return vmax * x / (km + x)
                
                # Fit curve
                params, _ = curve_fit(
                    saturation_func,
                    batch_sizes_np,
                    throughput_np,
                    bounds=([0, 0], [np.inf, np.inf]),
                    maxfev=10000,
                )
                
                vmax, km = params
                
                # Saturation point is where throughput reaches 95% of vmax
                saturation_throughput = 0.95 * vmax
                
                # Find batch size that achieves this throughput
                saturation_batch_size = km * saturation_throughput / (vmax - saturation_throughput)
                
                # Find closest actual batch size
                closest_idx = np.argmin(np.abs(batch_sizes_np - saturation_batch_size))
                results["saturation_point"] = int(batch_sizes_np[closest_idx])
                
                # Add curve fit parameters
                results["curve_fit"] = {
                    "vmax": float(vmax),
                    "km": float(km),
                    "fitted_values": saturation_func(batch_sizes_np, vmax, km).tolist(),
                }
                
                # Calculate confidence based on curve fit quality
                r2 = 1.0 - np.sum((throughput_np - saturation_func(batch_sizes_np, vmax, km))**2) / np.sum((throughput_np - np.mean(throughput_np))**2)
                results["confidence"] = float(max(0.5, min(0.95, r2)))
            
            except Exception as e:
                logger.warning(f"Failed to fit saturation curve: {e}")
                
                # Fallback: find point where throughput stops increasing significantly
                throughput_increases = np.diff(throughput_np) / throughput_np[:-1]
                
                # Find first point where throughput increase is less than 5%
                saturation_indices = np.where(throughput_increases < 0.05)[0]
                
                if len(saturation_indices) > 0:
                    saturation_idx = saturation_indices[0] + 1  # +1 because diff reduces array length by 1
                    results["saturation_point"] = int(batch_sizes_np[saturation_idx])
                    results["confidence"] = 0.7
        
        return results
    
    def predict_resource_allocation(
        self,
        model_profile: ModelArchitectureProfile,
        dataset_profile: DatasetProfile,
        available_devices: List[Dict[str, Any]],
        optimization_target: str = "throughput",
    ) -> Dict[str, Any]:
        """
        Predict optimal resource allocation across multiple devices.
        
        Args:
            model_profile: Model architecture profile
            dataset_profile: Dataset profile
            available_devices: List of available devices with their profiles
            optimization_target: Target metric to optimize ("throughput" or "time")
            
        Returns:
            Prediction results with optimal resource allocation
        """
        # Initialize results
        results = {
            "device_allocations": [],
            "total_throughput": 0.0,
            "total_time": 0.0,
            "confidence": 0.0,
        }
        
        # Evaluate each device
        device_predictions = []
        
        for device_idx, device_info in enumerate(available_devices):
            # Create hardware profile for this device
            if "hardware_profile" in device_info:
                hardware_profile = device_info["hardware_profile"]
            else:
                # Create minimal hardware profile
                hardware_type = HardwareType.GPU if "gpu" in device_info else HardwareType.CPU
                
                hardware_profile = HardwareProfile(hardware_type=hardware_type)
                
                if hardware_type == HardwareType.GPU:
                    hardware_profile.gpu_info = {
                        "num_gpus": 1,
                        "devices": [{
                            "name": device_info.get("name", "Unknown GPU"),
                            "total_memory": device_info.get("memory", 0),
                        }],
                    }
                else:
                    hardware_profile.cpu_info = {
                        "num_logical_cores": device_info.get("cores", 1),
                    }
                
                hardware_profile.memory_info = {
                    "total": device_info.get("memory", 0),
                }
            
            # Predict optimal batch size for this device
            batch_size_pred = self.predict_optimal_batch_size(
                model_profile=model_profile,
                dataset_profile=dataset_profile,
                hardware_profile=hardware_profile,
                optimization_target=optimization_target,
            )
            
            # Predict optimal workers for this device
            optimal_batch_size = batch_size_pred.get("optimal_batch_size", 32)
            
            training_profile = self.create_training_profile(batch_size=optimal_batch_size)
            
            workers_pred = self.predict_optimal_workers(
                model_profile=model_profile,
                dataset_profile=dataset_profile,
                training_profile=training_profile,
                hardware_profile=hardware_profile,
            )
            
            # Get throughput and time predictions
            optimal_workers = workers_pred.get("optimal_workers", 2)
            
            training_profile.num_workers = optimal_workers
            
            throughput_pred = self.predict(
                model_profile=model_profile,
                dataset_profile=dataset_profile,
                training_profile=training_profile,
                prediction_type=PredictionType.THROUGHPUT,
                hardware_profile=hardware_profile,
            )
            
            epoch_time_pred = self.predict(
                model_profile=model_profile,
                dataset_profile=dataset_profile,
                training_profile=training_profile,
                prediction_type=PredictionType.EPOCH_TIME,
                hardware_profile=hardware_profile,
            )
            
            # Store device prediction
            device_pred = {
                "device_idx": device_idx,
                "device_name": device_info.get("name", f"Device {device_idx}"),
                "optimal_batch_size": optimal_batch_size,
                "optimal_workers": optimal_workers,
                "throughput": throughput_pred.get("value", 0.0),
                "epoch_time": epoch_time_pred.get("value", 0.0),
                "confidence": (throughput_pred.get("confidence", 0.0) + epoch_time_pred.get("confidence", 0.0)) / 2,
            }
            
            device_predictions.append(device_pred)
        
        # Allocate resources based on optimization target
        if optimization_target == "throughput":
            # Sort devices by throughput (descending)
            device_predictions.sort(key=lambda x: x["throughput"], reverse=True)
            
            # Allocate samples proportionally to throughput
            total_throughput = sum(pred["throughput"] for pred in device_predictions)
            total_samples = dataset_profile.num_samples
            
            for pred in device_predictions:
                if total_throughput > 0:
                    # Allocate samples proportionally to throughput
                    allocation_ratio = pred["throughput"] / total_throughput
                    samples_allocated = int(total_samples * allocation_ratio)
                    
                    # Add allocation to results
                    results["device_allocations"].append({
                        "device_idx": pred["device_idx"],
                        "device_name": pred["device_name"],
                        "batch_size": pred["optimal_batch_size"],
                        "num_workers": pred["optimal_workers"],
                        "samples_allocated": samples_allocated,
                        "allocation_ratio": allocation_ratio,
                    })
        
        elif optimization_target == "time":
            # Sort devices by epoch time (ascending)
            device_predictions.sort(key=lambda x: x["epoch_time"])
            
            # Allocate to minimize total time
            # This is a simplified approach; a more sophisticated algorithm would be needed for optimal allocation
            total_samples = dataset_profile.num_samples
            remaining_samples = total_samples
            
            for pred in device_predictions:
                # Allocate samples inversely proportional to epoch time
                if remaining_samples > 0:
                    # Simple heuristic: allocate more to faster devices
                    inverse_times = [1.0 / max(0.001, p["epoch_time"]) for p in device_predictions]
                    total_inverse_time = sum(inverse_times)
                    
                    if total_inverse_time > 0:
                        allocation_ratio = (1.0 / max(0.001, pred["epoch_time"])) / total_inverse_time
                        samples_allocated = min(remaining_samples, int(total_samples * allocation_ratio))
                        remaining_samples -= samples_allocated
                        
                        # Add allocation to results
                        results["device_allocations"].append({
                            "device_idx": pred["device_idx"],
                            "device_name": pred["device_name"],
                            "batch_size": pred["optimal_batch_size"],
                            "num_workers": pred["optimal_workers"],
                            "samples_allocated": samples_allocated,
                            "allocation_ratio": allocation_ratio,
                        })
        
        # Calculate total throughput and time
        results["total_throughput"] = sum(pred["throughput"] for pred in device_predictions)
        
        # Estimate total time based on allocations
        if results["device_allocations"]:
            max_time = 0.0
            
            for alloc, pred in zip(results["device_allocations"], device_predictions):
                # Estimate time for this allocation
                if pred["throughput"] > 0:
                    time_estimate = alloc["samples_allocated"] / pred["throughput"]
                    max_time = max(max_time, time_estimate)
            
            results["total_time"] = max_time
        
        # Calculate overall confidence
        if device_predictions:
            results["confidence"] = sum(pred["confidence"] for pred in device_predictions) / len(device_predictions)
        
        return results
    
    def visualize_predictions(
        self,
        predictions: Dict[str, Any],
        plot_type: str = "batch_size_throughput",
        output_path: Optional[str] = None,
        show_plot: bool = False,
    ) -> Optional[str]:
        """
        Visualize predictions.
        
        Args:
            predictions: Prediction results
            plot_type: Type of plot to generate
            output_path: Path to save the visualization
            show_plot: Whether to show the plot
            
        Returns:
            Path to the saved visualization or None
        """
        plt.figure(figsize=(10, 6))
        
        if plot_type == "batch_size_throughput":
            # Plot batch size vs. throughput
            if "batch_sizes" in predictions and "throughput" in predictions:
                batch_sizes = predictions["batch_sizes"]
                throughput = predictions["throughput"]
                
                plt.plot(batch_sizes, throughput, "o-", label="Predicted Throughput")
                
                # Plot fitted curve if available
                if "curve_fit" in predictions and "fitted_values" in predictions["curve_fit"]:
                    fitted_values = predictions["curve_fit"]["fitted_values"]
                    plt.plot(batch_sizes, fitted_values, "--", label="Fitted Curve")
                
                # Mark saturation point if available
                if "saturation_point" in predictions and predictions["saturation_point"] is not None:
                    saturation_point = predictions["saturation_point"]
                    saturation_idx = batch_sizes.index(saturation_point)
                    saturation_throughput = throughput[saturation_idx]
                    
                    plt.axvline(x=saturation_point, color="r", linestyle="--", alpha=0.5)
                    plt.plot([saturation_point], [saturation_throughput], "ro", markersize=8, label=f"Saturation Point (BS={saturation_point})")
                
                # Mark optimal batch size if available
                if "optimal_batch_size" in predictions and predictions["optimal_batch_size"] is not None:
                    optimal_batch_size = predictions["optimal_batch_size"]
                    
                    try:
                        optimal_idx = batch_sizes.index(optimal_batch_size)
                        optimal_throughput = throughput[optimal_idx]
                        
                        plt.plot([optimal_batch_size], [optimal_throughput], "go", markersize=8, label=f"Optimal Batch Size (BS={optimal_batch_size})")
                    except ValueError:
                        pass
                
                plt.xscale("log")
                plt.xlabel("Batch Size")
                plt.ylabel("Throughput (samples/s)")
                plt.title("Batch Size vs. Throughput")
                plt.grid(True, alpha=0.3)
                plt.legend()
        
        elif plot_type == "batch_size_memory":
            # Plot batch size vs. memory usage
            if "batch_sizes" in predictions and "memory_usage" in predictions:
                batch_sizes = predictions["batch_sizes"]
                memory_usage = predictions["memory_usage"]
                
                plt.plot(batch_sizes, memory_usage, "o-", label="Predicted Memory Usage")
                
                # Mark optimal batch size if available
                if "optimal_batch_size" in predictions and predictions["optimal_batch_size"] is not None:
                    optimal_batch_size = predictions["optimal_batch_size"]
                    
                    try:
                        optimal_idx = batch_sizes.index(optimal_batch_size)
                        optimal_memory = memory_usage[optimal_idx]
                        
                        plt.plot([optimal_batch_size], [optimal_memory], "go", markersize=8, label=f"Optimal Batch Size (BS={optimal_batch_size})")
                    except ValueError:
                        pass
                
                plt.xscale("log")
                plt.xlabel("Batch Size")
                plt.ylabel("Memory Usage (bytes)")
                plt.title("Batch Size vs. Memory Usage")
                plt.grid(True, alpha=0.3)
                plt.legend()
        
        elif plot_type == "workers_throughput":
            # Plot number of workers vs. throughput
            if "worker_counts" in predictions and "throughput" in predictions:
                worker_counts = predictions["worker_counts"]
                throughput = predictions["throughput"]
                
                plt.plot(worker_counts, throughput, "o-", label="Predicted Throughput")
                
                # Mark optimal workers if available
                if "optimal_workers" in predictions and predictions["optimal_workers"] is not None:
                    optimal_workers = predictions["optimal_workers"]
                    
                    try:
                        optimal_idx = worker_counts.index(optimal_workers)
                        optimal_throughput = throughput[optimal_idx]
                        
                        plt.plot([optimal_workers], [optimal_throughput], "go", markersize=8, label=f"Optimal Workers (N={optimal_workers})")
                    except ValueError:
                        pass
                
                # Mark heuristic recommendation if available
                if "heuristic_recommendation" in predictions:
                    heuristic_workers = predictions["heuristic_recommendation"]
                    
                    try:
                        heuristic_idx = worker_counts.index(heuristic_workers)
                        heuristic_throughput = throughput[heuristic_idx]
                        
                        plt.plot([heuristic_workers], [heuristic_throughput], "mo", markersize=8, label=f"Heuristic Recommendation (N={heuristic_workers})")
                    except ValueError:
                        pass
                
                plt.xlabel("Number of Workers")
                plt.ylabel("Throughput (samples/s)")
                plt.title("Number of Workers vs. Throughput")
                plt.grid(True, alpha=0.3)
                plt.legend()
        
        elif plot_type == "resource_allocation":
            # Plot resource allocation
            if "device_allocations" in predictions:
                allocations = predictions["device_allocations"]
                
                if allocations:
                    # Extract data
                    device_names = [alloc["device_name"] for alloc in allocations]
                    samples_allocated = [alloc["samples_allocated"] for alloc in allocations]
                    
                    # Create bar chart
                    plt.bar(device_names, samples_allocated)
                    
                    plt.xlabel("Device")
                    plt.ylabel("Samples Allocated")
                    plt.title("Resource Allocation")
                    plt.xticks(rotation=45, ha="right")
                    plt.tight_layout()
        
        # Save or show plot
        if output_path:
            plt.savefig(output_path, bbox_inches="tight", dpi=300)
            logger.info(f"Saved visualization to {output_path}")
        
        if show_plot:
            plt.show()
        
        plt.close()
        
        return output_path if output_path else None
    
    def save_models(self, path: str) -> None:
        """
        Save prediction models.
        
        Args:
            path: Path to save the models
        """
        # Create directory if it doesn't exist
        os.makedirs(path, exist_ok=True)
        
        # Save models for each prediction type
        for pred_type, model in self.prediction_models.items():
            model_path = os.path.join(path, f"{pred_type}_model.joblib")
            
            try:
                joblib.dump(model, model_path)
                logger.info(f"Saved model for {pred_type} to {model_path}")
            except Exception as e:
                logger.error(f"Failed to save model for {pred_type}: {e}")
        
        # Save feature scalers
        for pred_type, scaler in self.feature_scalers.items():
            scaler_path = os.path.join(path, f"{pred_type}_scaler.joblib")
            
            try:
                joblib.dump(scaler, scaler_path)
                logger.info(f"Saved scaler for {pred_type} to {scaler_path}")
            except Exception as e:
                logger.error(f"Failed to save scaler for {pred_type}: {e}")
    
    def load_models(self, path: str) -> bool:
        """
        Load prediction models.
        
        Args:
            path: Path to load the models from
            
        Returns:
            True if successful, False otherwise
        """
        success = True
        
        # Load models for each prediction type
        for pred_type in PredictionType:
            model_path = os.path.join(path, f"{pred_type.value}_model.joblib")
            scaler_path = os.path.join(path, f"{pred_type.value}_scaler.joblib")
            
            if os.path.exists(model_path) and os.path.exists(scaler_path):
                try:
                    # Load model and scaler
                    model = joblib.load(model_path)
                    scaler = joblib.load(scaler_path)
                    
                    # Register model and scaler
                    self.prediction_models[pred_type.value] = model
                    self.feature_scalers[pred_type.value] = scaler
                    
                    logger.info(f"Loaded model for {pred_type.value}")
                except Exception as e:
                    logger.error(f"Failed to load model for {pred_type.value}: {e}")
                    success = False
        
        return success
    
    def save_performance_records(self, path: str) -> None:
        """
        Save performance records.
        
        Args:
            path: Path to save the records
        """
        try:
            with open(path, "wb") as f:
                pickle.dump(self.performance_records, f)
            
            logger.info(f"Saved performance records to {path}")
        except Exception as e:
            logger.error(f"Failed to save performance records: {e}")
    
    def load_performance_records(self, path: str) -> bool:
        """
        Load performance records.
        
        Args:
            path: Path to load the records from
            
        Returns:
            True if successful, False otherwise
        """
        try:
            with open(path, "rb") as f:
                self.performance_records = pickle.load(f)
            
            logger.info(f"Loaded performance records from {path}")
            return True
        except Exception as e:
            logger.error(f"Failed to load performance records: {e}")
            return False
    
    def get_metrics(self) -> Dict[str, Any]:
        """
        Get all metrics.
        
        Returns:
            All metrics
        """
        return self.metrics
    
    def get_predictions(self) -> Dict[str, Any]:
        """
        Get all predictions.
        
        Returns:
            All predictions
        """
        return self.predictions
    
    def get_performance_records(self) -> List[PerformanceRecord]:
        """
        Get all performance records.
        
        Returns:
            All performance records
        """
        return self.performance_records
    
    def get_hardware_profile(self) -> HardwareProfile:
        """
        Get the current hardware profile.
        
        Returns:
            Hardware profile
        """
        return self.hardware_profile
