"""
Anomaly-Activated Alert System (AAA-Sentry) module for AutoPipelineDoctor.

This advanced module monitors for sudden spikes in resource usage, loss, latency,
and idle periods, automatically taking snapshots of logs, metrics, and model state,
and sending alerts through various channels.
"""

import torch
import numpy as np
import pandas as pd
import logging
import time
import os
import json
import threading
import queue
import datetime
import pickle
import copy
import re
import traceback
import warnings
import smtplib
import requests
import socket
import psutil
import signal
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from typing import Dict, List, Tuple, Optional, Union, Any, Callable, Set, Type
from enum import Enum
from dataclasses import dataclass, field
from collections import defaultdict, deque
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

logger = logging.getLogger(__name__)


class AnomalyType(Enum):
    """Types of anomalies that can be detected."""
    MEMORY_SPIKE = "memory_spike"
    GPU_USAGE_SPIKE = "gpu_usage_spike"
    CPU_USAGE_SPIKE = "cpu_usage_spike"
    LOSS_SPIKE = "loss_spike"
    LOSS_NAN = "loss_nan"
    LOSS_INF = "loss_inf"
    LOSS_STAGNATION = "loss_stagnation"
    GRADIENT_EXPLOSION = "gradient_explosion"
    GRADIENT_VANISHING = "gradient_vanishing"
    LATENCY_SPIKE = "latency_spike"
    THROUGHPUT_DROP = "throughput_drop"
    IDLE_PERIOD = "idle_period"
    DATALOADER_STALL = "dataloader_stall"
    OOM_RISK = "oom_risk"
    HARDWARE_FAILURE = "hardware_failure"
    CUSTOM = "custom"


class AlertSeverity(Enum):
    """Severity levels for alerts."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class AlertChannel(Enum):
    """Channels for sending alerts."""
    CLI = "cli"
    LOG = "log"
    EMAIL = "email"
    SLACK = "slack"
    WEBHOOK = "webhook"
    CUSTOM = "custom"


@dataclass
class AlertConfig:
    """Configuration for an alert."""
    enabled: bool = True
    severity_threshold: AlertSeverity = AlertSeverity.MEDIUM
    channels: List[AlertChannel] = field(default_factory=lambda: [AlertChannel.CLI, AlertChannel.LOG])
    cooldown_seconds: float = 300.0  # Minimum time between alerts of the same type
    max_alerts_per_hour: int = 10
    custom_handler: Optional[Callable] = None


@dataclass
class ChannelConfig:
    """Configuration for an alert channel."""
    enabled: bool = True
    # Email configuration
    email_server: str = ""
    email_port: int = 587
    email_use_tls: bool = True
    email_username: str = ""
    email_password: str = ""
    email_from: str = ""
    email_to: List[str] = field(default_factory=list)
    # Slack configuration
    slack_webhook_url: str = ""
    slack_channel: str = ""
    slack_username: str = "AutoPipelineDoctor"
    # Webhook configuration
    webhook_url: str = ""
    webhook_headers: Dict[str, str] = field(default_factory=dict)
    # Custom configuration
    custom_config: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AnomalyDetectionConfig:
    """Configuration for anomaly detection."""
    # Memory spike detection
    memory_spike_threshold: float = 0.2  # Fractional increase
    memory_spike_window: int = 5  # Number of samples to consider
    # GPU usage spike detection
    gpu_spike_threshold: float = 0.3  # Fractional increase
    gpu_spike_window: int = 5  # Number of samples to consider
    # CPU usage spike detection
    cpu_spike_threshold: float = 0.3  # Fractional increase
    cpu_spike_window: int = 5  # Number of samples to consider
    # Loss spike detection
    loss_spike_threshold: float = 0.5  # Fractional increase
    loss_spike_window: int = 5  # Number of samples to consider
    # Loss stagnation detection
    loss_stagnation_threshold: float = 0.01  # Minimum expected decrease
    loss_stagnation_window: int = 20  # Number of samples to consider
    # Gradient explosion detection
    gradient_explosion_threshold: float = 100.0  # Absolute value
    # Gradient vanishing detection
    gradient_vanishing_threshold: float = 1e-7  # Absolute value
    # Latency spike detection
    latency_spike_threshold: float = 0.5  # Fractional increase
    latency_spike_window: int = 5  # Number of samples to consider
    # Throughput drop detection
    throughput_drop_threshold: float = 0.3  # Fractional decrease
    throughput_drop_window: int = 5  # Number of samples to consider
    # Idle period detection
    idle_threshold: float = 0.1  # Maximum CPU/GPU usage to consider idle
    idle_period_threshold: float = 30.0  # Seconds
    # Dataloader stall detection
    dataloader_stall_threshold: float = 5.0  # Seconds
    # OOM risk detection
    oom_risk_threshold: float = 0.9  # Fraction of available memory
    # Custom detection
    custom_config: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SnapshotConfig:
    """Configuration for snapshots."""
    enabled: bool = True
    include_logs: bool = True
    include_metrics: bool = True
    include_model_state: bool = True
    include_gradients: bool = False  # Can be large
    include_optimizer_state: bool = False  # Can be large
    include_inputs: bool = False  # Can be large
    include_outputs: bool = False  # Can be large
    include_system_info: bool = True
    max_snapshots: int = 10
    snapshot_dir: str = "./snapshots"
    custom_snapshot_handler: Optional[Callable] = None


@dataclass
class Alert:
    """Alert information."""
    anomaly_type: AnomalyType
    severity: AlertSeverity
    message: str
    details: Dict[str, Any]
    timestamp: float
    snapshot_path: Optional[str] = None
    metrics: Dict[str, Any] = field(default_factory=dict)
    resolved: bool = False
    resolution_timestamp: Optional[float] = None
    resolution_message: Optional[str] = None


@dataclass
class Snapshot:
    """Snapshot information."""
    timestamp: float
    anomaly_type: AnomalyType
    logs: Optional[List[str]] = None
    metrics: Optional[Dict[str, Any]] = None
    model_state: Optional[Dict[str, Any]] = None
    gradients: Optional[Dict[str, Any]] = None
    optimizer_state: Optional[Dict[str, Any]] = None
    inputs: Optional[Any] = None
    outputs: Optional[Any] = None
    system_info: Optional[Dict[str, Any]] = None
    custom_data: Optional[Dict[str, Any]] = None


class AnomalyActivatedAlertSystem:
    """
    Anomaly-Activated Alert System (AAA-Sentry) for monitoring and alerting on training anomalies.
    
    This module monitors for sudden spikes in resource usage, loss, latency, and idle periods,
    automatically taking snapshots of logs, metrics, and model state, and sending alerts
    through various channels.
    
    Attributes:
        alert_configs: Configurations for different types of alerts
        channel_config: Configuration for alert channels
        anomaly_config: Configuration for anomaly detection
        snapshot_config: Configuration for snapshots
        metrics_history: History of collected metrics
        alerts: List of generated alerts
        snapshots: List of created snapshots
        last_alert_times: Timestamps of last alerts by type
        alert_counts: Counts of alerts by type and hour
        detection_thread: Thread for anomaly detection
        alert_thread: Thread for alert processing
        running: Whether the system is running
    """
    
    def __init__(
        self,
        alert_configs: Optional[Dict[AnomalyType, AlertConfig]] = None,
        channel_config: Optional[ChannelConfig] = None,
        anomaly_config: Optional[AnomalyDetectionConfig] = None,
        snapshot_config: Optional[SnapshotConfig] = None,
    ):
        """
        Initialize the AnomalyActivatedAlertSystem.
        
        Args:
            alert_configs: Configurations for different types of alerts
            channel_config: Configuration for alert channels
            anomaly_config: Configuration for anomaly detection
            snapshot_config: Configuration for snapshots
        """
        # Initialize configurations
        self.alert_configs = alert_configs or self._default_alert_configs()
        self.channel_config = channel_config or ChannelConfig()
        self.anomaly_config = anomaly_config or AnomalyDetectionConfig()
        self.snapshot_config = snapshot_config or SnapshotConfig()
        
        # Initialize metrics history
        self.metrics_history: Dict[str, deque] = defaultdict(lambda: deque(maxlen=100))
        
        # Initialize alerts and snapshots
        self.alerts: List[Alert] = []
        self.snapshots: List[Snapshot] = []
        
        # Initialize alert tracking
        self.last_alert_times: Dict[AnomalyType, float] = defaultdict(float)
        self.alert_counts: Dict[Tuple[AnomalyType, int], int] = defaultdict(int)  # (type, hour) -> count
        
        # Initialize threads
        self.detection_thread: Optional[threading.Thread] = None
        self.alert_thread: Optional[threading.Thread] = None
        self.alert_queue: queue.Queue = queue.Queue()
        
        # Initialize state
        self.running: bool = False
        self.paused: bool = False
        
        # Initialize locks
        self.metrics_lock = threading.Lock()
        self.alert_lock = threading.Lock()
        self.snapshot_lock = threading.Lock()
        
        # Initialize snapshot directory
        if self.snapshot_config.enabled:
            os.makedirs(self.snapshot_config.snapshot_dir, exist_ok=True)
        
        # Initialize logger capture
        self.log_capture_handler = None
        self.captured_logs = []
        
        # Initialize model and optimizer references
        self.model: Optional[torch.nn.Module] = None
        self.optimizer: Optional[torch.optim.Optimizer] = None
        
        # Initialize current batch information
        self.current_inputs: Optional[Any] = None
        self.current_outputs: Optional[Any] = None
        
        # Initialize system monitoring
        self.last_system_check_time: float = time.time()
        self.last_activity_time: float = time.time()
        
        logger.info("Initialized AnomalyActivatedAlertSystem")
    
    def _default_alert_configs(self) -> Dict[AnomalyType, AlertConfig]:
        """
        Create default alert configurations.
        
        Returns:
            Default alert configurations
        """
        configs = {}
        
        # Critical alerts
        for anomaly_type in [
            AnomalyType.LOSS_NAN,
            AnomalyType.LOSS_INF,
            AnomalyType.GRADIENT_EXPLOSION,
            AnomalyType.OOM_RISK,
            AnomalyType.HARDWARE_FAILURE,
        ]:
            configs[anomaly_type] = AlertConfig(
                enabled=True,
                severity_threshold=AlertSeverity.CRITICAL,
                channels=[AlertChannel.CLI, AlertChannel.LOG, AlertChannel.EMAIL],
                cooldown_seconds=60.0,
                max_alerts_per_hour=20,
            )
        
        # High severity alerts
        for anomaly_type in [
            AnomalyType.MEMORY_SPIKE,
            AnomalyType.GPU_USAGE_SPIKE,
            AnomalyType.LOSS_SPIKE,
            AnomalyType.GRADIENT_VANISHING,
            AnomalyType.DATALOADER_STALL,
        ]:
            configs[anomaly_type] = AlertConfig(
                enabled=True,
                severity_threshold=AlertSeverity.HIGH,
                channels=[AlertChannel.CLI, AlertChannel.LOG],
                cooldown_seconds=300.0,
                max_alerts_per_hour=10,
            )
        
        # Medium severity alerts
        for anomaly_type in [
            AnomalyType.CPU_USAGE_SPIKE,
            AnomalyType.LOSS_STAGNATION,
            AnomalyType.LATENCY_SPIKE,
            AnomalyType.THROUGHPUT_DROP,
        ]:
            configs[anomaly_type] = AlertConfig(
                enabled=True,
                severity_threshold=AlertSeverity.MEDIUM,
                channels=[AlertChannel.CLI, AlertChannel.LOG],
                cooldown_seconds=600.0,
                max_alerts_per_hour=5,
            )
        
        # Low severity alerts
        for anomaly_type in [
            AnomalyType.IDLE_PERIOD,
            AnomalyType.CUSTOM,
        ]:
            configs[anomaly_type] = AlertConfig(
                enabled=True,
                severity_threshold=AlertSeverity.LOW,
                channels=[AlertChannel.CLI, AlertChannel.LOG],
                cooldown_seconds=1800.0,
                max_alerts_per_hour=3,
            )
        
        return configs
    
    def start(self) -> None:
        """Start the anomaly detection and alert system."""
        if self.running:
            logger.warning("AnomalyActivatedAlertSystem is already running")
            return
        
        logger.info("Starting AnomalyActivatedAlertSystem")
        
        # Start log capture
        self._start_log_capture()
        
        # Start detection thread
        self.running = True
        self.paused = False
        self.detection_thread = threading.Thread(target=self._detection_loop, daemon=True)
        self.detection_thread.start()
        
        # Start alert thread
        self.alert_thread = threading.Thread(target=self._alert_loop, daemon=True)
        self.alert_thread.start()
        
        logger.info("AnomalyActivatedAlertSystem started")
    
    def stop(self) -> None:
        """Stop the anomaly detection and alert system."""
        if not self.running:
            logger.warning("AnomalyActivatedAlertSystem is not running")
            return
        
        logger.info("Stopping AnomalyActivatedAlertSystem")
        
        # Stop threads
        self.running = False
        
        # Wait for threads to finish
        if self.detection_thread:
            self.detection_thread.join(timeout=5.0)
        
        if self.alert_thread:
            self.alert_thread.join(timeout=5.0)
        
        # Stop log capture
        self._stop_log_capture()
        
        logger.info("AnomalyActivatedAlertSystem stopped")
    
    def pause(self) -> None:
        """Pause the anomaly detection and alert system."""
        if not self.running:
            logger.warning("AnomalyActivatedAlertSystem is not running")
            return
        
        if self.paused:
            logger.warning("AnomalyActivatedAlertSystem is already paused")
            return
        
        logger.info("Pausing AnomalyActivatedAlertSystem")
        self.paused = True
    
    def resume(self) -> None:
        """Resume the anomaly detection and alert system."""
        if not self.running:
            logger.warning("AnomalyActivatedAlertSystem is not running")
            return
        
        if not self.paused:
            logger.warning("AnomalyActivatedAlertSystem is not paused")
            return
        
        logger.info("Resuming AnomalyActivatedAlertSystem")
        self.paused = False
    
    def _start_log_capture(self) -> None:
        """Start capturing logs."""
        if self.log_capture_handler is not None:
            return
        
        # Create log capture handler
        class LogCaptureHandler(logging.Handler):
            def __init__(self, log_list):
                super().__init__()
                self.log_list = log_list
            
            def emit(self, record):
                try:
                    log_entry = self.format(record)
                    self.log_list.append(log_entry)
                    
                    # Limit the number of captured logs
                    while len(self.log_list) > 1000:
                        self.log_list.pop(0)
                except Exception:
                    self.handleError(record)
        
        # Add handler to root logger
        root_logger = logging.getLogger()
        self.log_capture_handler = LogCaptureHandler(self.captured_logs)
        self.log_capture_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
        root_logger.addHandler(self.log_capture_handler)
    
    def _stop_log_capture(self) -> None:
        """Stop capturing logs."""
        if self.log_capture_handler is None:
            return
        
        # Remove handler from root logger
        root_logger = logging.getLogger()
        root_logger.removeHandler(self.log_capture_handler)
        self.log_capture_handler = None
    
    def _detection_loop(self) -> None:
        """Main loop for anomaly detection."""
        logger.info("Starting anomaly detection loop")
        
        while self.running:
            try:
                if not self.paused:
                    # Check for anomalies
                    self._check_anomalies()
                
                # Sleep for a short time
                time.sleep(1.0)
            
            except Exception as e:
                logger.error(f"Error in anomaly detection loop: {e}")
                logger.error(traceback.format_exc())
                time.sleep(5.0)  # Sleep longer after an error
    
    def _alert_loop(self) -> None:
        """Main loop for alert processing."""
        logger.info("Starting alert processing loop")
        
        while self.running:
            try:
                # Get alert from queue with timeout
                try:
                    alert = self.alert_queue.get(timeout=1.0)
                except queue.Empty:
                    continue
                
                # Process alert
                self._process_alert(alert)
                
                # Mark as done
                self.alert_queue.task_done()
            
            except Exception as e:
                logger.error(f"Error in alert processing loop: {e}")
                logger.error(traceback.format_exc())
                time.sleep(5.0)  # Sleep longer after an error
    
    def _check_anomalies(self) -> None:
        """Check for anomalies in the collected metrics."""
        # Update system metrics
        self._update_system_metrics()
        
        # Check for memory spikes
        self._check_memory_spike()
        
        # Check for GPU usage spikes
        self._check_gpu_usage_spike()
        
        # Check for CPU usage spikes
        self._check_cpu_usage_spike()
        
        # Check for loss spikes and anomalies
        self._check_loss_anomalies()
        
        # Check for gradient anomalies
        self._check_gradient_anomalies()
        
        # Check for latency spikes
        self._check_latency_spike()
        
        # Check for throughput drops
        self._check_throughput_drop()
        
        # Check for idle periods
        self._check_idle_period()
        
        # Check for dataloader stalls
        self._check_dataloader_stall()
        
        # Check for OOM risk
        self._check_oom_risk()
    
    def _update_system_metrics(self) -> None:
        """Update system metrics."""
        current_time = time.time()
        
        # Only update every second
        if current_time - self.last_system_check_time < 1.0:
            return
        
        self.last_system_check_time = current_time
        
        try:
            # Get CPU usage
            cpu_percent = psutil.cpu_percent()
            self.record_metric("cpu_usage", cpu_percent)
            
            # Get memory usage
            memory = psutil.virtual_memory()
            self.record_metric("memory_used", memory.used)
            self.record_metric("memory_available", memory.available)
            self.record_metric("memory_percent", memory.percent)
            
            # Get GPU usage if available
            try:
                import torch
                
                if torch.cuda.is_available():
                    # Get GPU memory usage
                    for i in range(torch.cuda.device_count()):
                        memory_allocated = torch.cuda.memory_allocated(i)
                        memory_reserved = torch.cuda.memory_reserved(i)
                        
                        self.record_metric(f"gpu{i}_memory_allocated", memory_allocated)
                        self.record_metric(f"gpu{i}_memory_reserved", memory_reserved)
                        
                        # Try to get GPU utilization using pynvml
                        try:
                            import pynvml
                            
                            pynvml.nvmlInit()
                            handle = pynvml.nvmlDeviceGetHandleByIndex(i)
                            utilization = pynvml.nvmlDeviceGetUtilizationRates(handle)
                            
                            self.record_metric(f"gpu{i}_utilization", utilization.gpu)
                            self.record_metric(f"gpu{i}_memory_utilization", utilization.memory)
                        except (ImportError, Exception):
                            pass
            except (ImportError, Exception):
                pass
        
        except Exception as e:
            logger.warning(f"Error updating system metrics: {e}")
    
    def _check_memory_spike(self) -> None:
        """Check for memory usage spikes."""
        if AnomalyType.MEMORY_SPIKE not in self.alert_configs or not self.alert_configs[AnomalyType.MEMORY_SPIKE].enabled:
            return
        
        # Get memory usage history
        memory_history = self.get_metric_history("memory_percent")
        
        if len(memory_history) < self.anomaly_config.memory_spike_window:
            return
        
        # Calculate average of previous values
        prev_avg = sum(memory_history[-self.anomaly_config.memory_spike_window:-1]) / (self.anomaly_config.memory_spike_window - 1)
        
        # Get current value
        current = memory_history[-1]
        
        # Check for spike
        if prev_avg > 0 and current > prev_avg * (1 + self.anomaly_config.memory_spike_threshold):
            # Calculate spike percentage
            spike_percent = (current - prev_avg) / prev_avg * 100
            
            # Create alert
            self._create_alert(
                anomaly_type=AnomalyType.MEMORY_SPIKE,
                severity=AlertSeverity.HIGH,
                message=f"Memory usage spike detected: {current:.1f}% (increased by {spike_percent:.1f}%)",
                details={
                    "current_memory_percent": current,
                    "previous_average": prev_avg,
                    "spike_percent": spike_percent,
                    "threshold_percent": self.anomaly_config.memory_spike_threshold * 100,
                },
            )
    
    def _check_gpu_usage_spike(self) -> None:
        """Check for GPU usage spikes."""
        if AnomalyType.GPU_USAGE_SPIKE not in self.alert_configs or not self.alert_configs[AnomalyType.GPU_USAGE_SPIKE].enabled:
            return
        
        # Check each GPU
        for i in range(10):  # Check up to 10 GPUs
            # Get GPU memory usage history
            memory_history = self.get_metric_history(f"gpu{i}_memory_allocated")
            
            if len(memory_history) < self.anomaly_config.gpu_spike_window:
                continue
            
            # Calculate average of previous values
            prev_avg = sum(memory_history[-self.anomaly_config.gpu_spike_window:-1]) / (self.anomaly_config.gpu_spike_window - 1)
            
            # Get current value
            current = memory_history[-1]
            
            # Check for spike
            if prev_avg > 0 and current > prev_avg * (1 + self.anomaly_config.gpu_spike_threshold):
                # Calculate spike percentage
                spike_percent = (current - prev_avg) / prev_avg * 100
                
                # Convert to MB for readability
                current_mb = current / (1024 * 1024)
                prev_avg_mb = prev_avg / (1024 * 1024)
                
                # Create alert
                self._create_alert(
                    anomaly_type=AnomalyType.GPU_USAGE_SPIKE,
                    severity=AlertSeverity.HIGH,
                    message=f"GPU {i} memory spike detected: {current_mb:.1f} MB (increased by {spike_percent:.1f}%)",
                    details={
                        "gpu_id": i,
                        "current_memory_mb": current_mb,
                        "previous_average_mb": prev_avg_mb,
                        "spike_percent": spike_percent,
                        "threshold_percent": self.anomaly_config.gpu_spike_threshold * 100,
                    },
                )
            
            # Check GPU utilization if available
            utilization_history = self.get_metric_history(f"gpu{i}_utilization")
            
            if len(utilization_history) < self.anomaly_config.gpu_spike_window:
                continue
            
            # Calculate average of previous values
            prev_avg = sum(utilization_history[-self.anomaly_config.gpu_spike_window:-1]) / (self.anomaly_config.gpu_spike_window - 1)
            
            # Get current value
            current = utilization_history[-1]
            
            # Check for spike
            if prev_avg > 0 and current > prev_avg * (1 + self.anomaly_config.gpu_spike_threshold):
                # Calculate spike percentage
                spike_percent = (current - prev_avg) / prev_avg * 100
                
                # Create alert
                self._create_alert(
                    anomaly_type=AnomalyType.GPU_USAGE_SPIKE,
                    severity=AlertSeverity.MEDIUM,
                    message=f"GPU {i} utilization spike detected: {current:.1f}% (increased by {spike_percent:.1f}%)",
                    details={
                        "gpu_id": i,
                        "current_utilization": current,
                        "previous_average": prev_avg,
                        "spike_percent": spike_percent,
                        "threshold_percent": self.anomaly_config.gpu_spike_threshold * 100,
                    },
                )
    
    def _check_cpu_usage_spike(self) -> None:
        """Check for CPU usage spikes."""
        if AnomalyType.CPU_USAGE_SPIKE not in self.alert_configs or not self.alert_configs[AnomalyType.CPU_USAGE_SPIKE].enabled:
            return
        
        # Get CPU usage history
        cpu_history = self.get_metric_history("cpu_usage")
        
        if len(cpu_history) < self.anomaly_config.cpu_spike_window:
            return
        
        # Calculate average of previous values
        prev_avg = sum(cpu_history[-self.anomaly_config.cpu_spike_window:-1]) / (self.anomaly_config.cpu_spike_window - 1)
        
        # Get current value
        current = cpu_history[-1]
        
        # Check for spike
        if prev_avg > 0 and current > prev_avg * (1 + self.anomaly_config.cpu_spike_threshold):
            # Calculate spike percentage
            spike_percent = (current - prev_avg) / prev_avg * 100
            
            # Create alert
            self._create_alert(
                anomaly_type=AnomalyType.CPU_USAGE_SPIKE,
                severity=AlertSeverity.MEDIUM,
                message=f"CPU usage spike detected: {current:.1f}% (increased by {spike_percent:.1f}%)",
                details={
                    "current_cpu_percent": current,
                    "previous_average": prev_avg,
                    "spike_percent": spike_percent,
                    "threshold_percent": self.anomaly_config.cpu_spike_threshold * 100,
                },
            )
    
    def _check_loss_anomalies(self) -> None:
        """Check for loss spikes and other anomalies."""
        # Check for loss spikes
        self._check_loss_spike()
        
        # Check for NaN/Inf loss
        self._check_loss_nan_inf()
        
        # Check for loss stagnation
        self._check_loss_stagnation()
    
    def _check_loss_spike(self) -> None:
        """Check for loss spikes."""
        if AnomalyType.LOSS_SPIKE not in self.alert_configs or not self.alert_configs[AnomalyType.LOSS_SPIKE].enabled:
            return
        
        # Get loss history
        loss_history = self.get_metric_history("loss")
        
        if len(loss_history) < self.anomaly_config.loss_spike_window:
            return
        
        # Calculate average of previous values
        prev_avg = sum(loss_history[-self.anomaly_config.loss_spike_window:-1]) / (self.anomaly_config.loss_spike_window - 1)
        
        # Get current value
        current = loss_history[-1]
        
        # Check for spike
        if prev_avg > 0 and current > prev_avg * (1 + self.anomaly_config.loss_spike_threshold):
            # Calculate spike percentage
            spike_percent = (current - prev_avg) / prev_avg * 100
            
            # Create alert
            self._create_alert(
                anomaly_type=AnomalyType.LOSS_SPIKE,
                severity=AlertSeverity.HIGH,
                message=f"Loss spike detected: {current:.4f} (increased by {spike_percent:.1f}%)",
                details={
                    "current_loss": current,
                    "previous_average": prev_avg,
                    "spike_percent": spike_percent,
                    "threshold_percent": self.anomaly_config.loss_spike_threshold * 100,
                },
            )
    
    def _check_loss_nan_inf(self) -> None:
        """Check for NaN or Inf loss values."""
        # Get loss history
        loss_history = self.get_metric_history("loss")
        
        if not loss_history:
            return
        
        # Get current value
        current = loss_history[-1]
        
        # Check for NaN
        if AnomalyType.LOSS_NAN in self.alert_configs and self.alert_configs[AnomalyType.LOSS_NAN].enabled:
            if np.isnan(current):
                # Create alert
                self._create_alert(
                    anomaly_type=AnomalyType.LOSS_NAN,
                    severity=AlertSeverity.CRITICAL,
                    message="NaN loss detected",
                    details={
                        "current_loss": "NaN",
                        "previous_loss": loss_history[-2] if len(loss_history) > 1 else None,
                    },
                )
        
        # Check for Inf
        if AnomalyType.LOSS_INF in self.alert_configs and self.alert_configs[AnomalyType.LOSS_INF].enabled:
            if np.isinf(current):
                # Create alert
                self._create_alert(
                    anomaly_type=AnomalyType.LOSS_INF,
                    severity=AlertSeverity.CRITICAL,
                    message="Infinite loss detected",
                    details={
                        "current_loss": "Inf",
                        "previous_loss": loss_history[-2] if len(loss_history) > 1 else None,
                    },
                )
    
    def _check_loss_stagnation(self) -> None:
        """Check for loss stagnation."""
        if AnomalyType.LOSS_STAGNATION not in self.alert_configs or not self.alert_configs[AnomalyType.LOSS_STAGNATION].enabled:
            return
        
        # Get loss history
        loss_history = self.get_metric_history("loss")
        
        if len(loss_history) < self.anomaly_config.loss_stagnation_window:
            return
        
        # Get initial and final values in window
        initial = loss_history[-self.anomaly_config.loss_stagnation_window]
        final = loss_history[-1]
        
        # Check for stagnation (not decreasing enough)
        if initial > 0 and final > initial * (1 - self.anomaly_config.loss_stagnation_threshold):
            # Calculate stagnation percentage
            stagnation_percent = (initial - final) / initial * 100
            
            # Create alert
            self._create_alert(
                anomaly_type=AnomalyType.LOSS_STAGNATION,
                severity=AlertSeverity.MEDIUM,
                message=f"Loss stagnation detected: decreased by only {stagnation_percent:.2f}% over {self.anomaly_config.loss_stagnation_window} steps",
                details={
                    "initial_loss": initial,
                    "final_loss": final,
                    "decrease_percent": stagnation_percent,
                    "window_size": self.anomaly_config.loss_stagnation_window,
                    "threshold_percent": self.anomaly_config.loss_stagnation_threshold * 100,
                },
            )
    
    def _check_gradient_anomalies(self) -> None:
        """Check for gradient anomalies."""
        # Check for gradient explosion
        self._check_gradient_explosion()
        
        # Check for gradient vanishing
        self._check_gradient_vanishing()
    
    def _check_gradient_explosion(self) -> None:
        """Check for gradient explosion."""
        if AnomalyType.GRADIENT_EXPLOSION not in self.alert_configs or not self.alert_configs[AnomalyType.GRADIENT_EXPLOSION].enabled:
            return
        
        # Get gradient norm history
        grad_norm_history = self.get_metric_history("gradient_norm")
        
        if not grad_norm_history:
            return
        
        # Get current value
        current = grad_norm_history[-1]
        
        # Check for explosion
        if current > self.anomaly_config.gradient_explosion_threshold:
            # Create alert
            self._create_alert(
                anomaly_type=AnomalyType.GRADIENT_EXPLOSION,
                severity=AlertSeverity.CRITICAL,
                message=f"Gradient explosion detected: norm = {current:.2f}",
                details={
                    "gradient_norm": current,
                    "threshold": self.anomaly_config.gradient_explosion_threshold,
                    "previous_norm": grad_norm_history[-2] if len(grad_norm_history) > 1 else None,
                },
            )
    
    def _check_gradient_vanishing(self) -> None:
        """Check for gradient vanishing."""
        if AnomalyType.GRADIENT_VANISHING not in self.alert_configs or not self.alert_configs[AnomalyType.GRADIENT_VANISHING].enabled:
            return
        
        # Get gradient norm history
        grad_norm_history = self.get_metric_history("gradient_norm")
        
        if not grad_norm_history:
            return
        
        # Get current value
        current = grad_norm_history[-1]
        
        # Check for vanishing
        if current < self.anomaly_config.gradient_vanishing_threshold and current > 0:
            # Create alert
            self._create_alert(
                anomaly_type=AnomalyType.GRADIENT_VANISHING,
                severity=AlertSeverity.HIGH,
                message=f"Gradient vanishing detected: norm = {current:.8f}",
                details={
                    "gradient_norm": current,
                    "threshold": self.anomaly_config.gradient_vanishing_threshold,
                    "previous_norm": grad_norm_history[-2] if len(grad_norm_history) > 1 else None,
                },
            )
    
    def _check_latency_spike(self) -> None:
        """Check for latency spikes."""
        if AnomalyType.LATENCY_SPIKE not in self.alert_configs or not self.alert_configs[AnomalyType.LATENCY_SPIKE].enabled:
            return
        
        # Get batch time history
        batch_time_history = self.get_metric_history("batch_time")
        
        if len(batch_time_history) < self.anomaly_config.latency_spike_window:
            return
        
        # Calculate average of previous values
        prev_avg = sum(batch_time_history[-self.anomaly_config.latency_spike_window:-1]) / (self.anomaly_config.latency_spike_window - 1)
        
        # Get current value
        current = batch_time_history[-1]
        
        # Check for spike
        if prev_avg > 0 and current > prev_avg * (1 + self.anomaly_config.latency_spike_threshold):
            # Calculate spike percentage
            spike_percent = (current - prev_avg) / prev_avg * 100
            
            # Create alert
            self._create_alert(
                anomaly_type=AnomalyType.LATENCY_SPIKE,
                severity=AlertSeverity.MEDIUM,
                message=f"Batch latency spike detected: {current:.4f}s (increased by {spike_percent:.1f}%)",
                details={
                    "current_batch_time": current,
                    "previous_average": prev_avg,
                    "spike_percent": spike_percent,
                    "threshold_percent": self.anomaly_config.latency_spike_threshold * 100,
                },
            )
    
    def _check_throughput_drop(self) -> None:
        """Check for throughput drops."""
        if AnomalyType.THROUGHPUT_DROP not in self.alert_configs or not self.alert_configs[AnomalyType.THROUGHPUT_DROP].enabled:
            return
        
        # Get throughput history
        throughput_history = self.get_metric_history("throughput")
        
        if len(throughput_history) < self.anomaly_config.throughput_drop_window:
            return
        
        # Calculate average of previous values
        prev_avg = sum(throughput_history[-self.anomaly_config.throughput_drop_window:-1]) / (self.anomaly_config.throughput_drop_window - 1)
        
        # Get current value
        current = throughput_history[-1]
        
        # Check for drop
        if prev_avg > 0 and current < prev_avg * (1 - self.anomaly_config.throughput_drop_threshold):
            # Calculate drop percentage
            drop_percent = (prev_avg - current) / prev_avg * 100
            
            # Create alert
            self._create_alert(
                anomaly_type=AnomalyType.THROUGHPUT_DROP,
                severity=AlertSeverity.MEDIUM,
                message=f"Throughput drop detected: {current:.2f} samples/s (decreased by {drop_percent:.1f}%)",
                details={
                    "current_throughput": current,
                    "previous_average": prev_avg,
                    "drop_percent": drop_percent,
                    "threshold_percent": self.anomaly_config.throughput_drop_threshold * 100,
                },
            )
    
    def _check_idle_period(self) -> None:
        """Check for idle periods."""
        if AnomalyType.IDLE_PERIOD not in self.alert_configs or not self.alert_configs[AnomalyType.IDLE_PERIOD].enabled:
            return
        
        # Get CPU and GPU usage
        cpu_usage = self.get_latest_metric("cpu_usage")
        
        if cpu_usage is None:
            return
        
        # Check if system is idle
        is_idle = cpu_usage < self.anomaly_config.idle_threshold
        
        # Check GPU if available
        for i in range(10):  # Check up to 10 GPUs
            gpu_util = self.get_latest_metric(f"gpu{i}_utilization")
            
            if gpu_util is not None:
                is_idle = is_idle and gpu_util < self.anomaly_config.idle_threshold
        
        # Update activity time if not idle
        if not is_idle:
            self.last_activity_time = time.time()
            return
        
        # Check idle duration
        idle_duration = time.time() - self.last_activity_time
        
        if idle_duration > self.anomaly_config.idle_period_threshold:
            # Create alert
            self._create_alert(
                anomaly_type=AnomalyType.IDLE_PERIOD,
                severity=AlertSeverity.LOW,
                message=f"System idle detected for {idle_duration:.1f} seconds",
                details={
                    "idle_duration": idle_duration,
                    "cpu_usage": cpu_usage,
                    "threshold_duration": self.anomaly_config.idle_period_threshold,
                },
            )
            
            # Update activity time to prevent repeated alerts
            self.last_activity_time = time.time()
    
    def _check_dataloader_stall(self) -> None:
        """Check for dataloader stalls."""
        if AnomalyType.DATALOADER_STALL not in self.alert_configs or not self.alert_configs[AnomalyType.DATALOADER_STALL].enabled:
            return
        
        # Get dataloader time history
        dataloader_time_history = self.get_metric_history("dataloader_time")
        
        if not dataloader_time_history:
            return
        
        # Get current value
        current = dataloader_time_history[-1]
        
        # Check for stall
        if current > self.anomaly_config.dataloader_stall_threshold:
            # Create alert
            self._create_alert(
                anomaly_type=AnomalyType.DATALOADER_STALL,
                severity=AlertSeverity.HIGH,
                message=f"Dataloader stall detected: {current:.2f}s",
                details={
                    "dataloader_time": current,
                    "threshold": self.anomaly_config.dataloader_stall_threshold,
                    "previous_time": dataloader_time_history[-2] if len(dataloader_time_history) > 1 else None,
                },
            )
    
    def _check_oom_risk(self) -> None:
        """Check for out-of-memory risk."""
        if AnomalyType.OOM_RISK not in self.alert_configs or not self.alert_configs[AnomalyType.OOM_RISK].enabled:
            return
        
        # Check GPU memory if available
        for i in range(10):  # Check up to 10 GPUs
            allocated = self.get_latest_metric(f"gpu{i}_memory_allocated")
            reserved = self.get_latest_metric(f"gpu{i}_memory_reserved")
            
            if allocated is not None and reserved is not None:
                # Calculate usage ratio
                if reserved > 0:
                    usage_ratio = allocated / reserved
                    
                    if usage_ratio > self.anomaly_config.oom_risk_threshold:
                        # Create alert
                        self._create_alert(
                            anomaly_type=AnomalyType.OOM_RISK,
                            severity=AlertSeverity.CRITICAL,
                            message=f"GPU {i} OOM risk detected: {usage_ratio:.1%} of reserved memory used",
                            details={
                                "gpu_id": i,
                                "memory_allocated": allocated,
                                "memory_reserved": reserved,
                                "usage_ratio": usage_ratio,
                                "threshold": self.anomaly_config.oom_risk_threshold,
                            },
                        )
        
        # Check system memory
        memory_percent = self.get_latest_metric("memory_percent")
        
        if memory_percent is not None and memory_percent > self.anomaly_config.oom_risk_threshold * 100:
            # Create alert
            self._create_alert(
                anomaly_type=AnomalyType.OOM_RISK,
                severity=AlertSeverity.CRITICAL,
                message=f"System memory OOM risk detected: {memory_percent:.1f}% used",
                details={
                    "memory_percent": memory_percent,
                    "threshold_percent": self.anomaly_config.oom_risk_threshold * 100,
                },
            )
    
    def _create_alert(
        self,
        anomaly_type: AnomalyType,
        severity: AlertSeverity,
        message: str,
        details: Dict[str, Any],
    ) -> None:
        """
        Create an alert.
        
        Args:
            anomaly_type: Type of anomaly
            severity: Severity level
            message: Alert message
            details: Alert details
        """
        # Check if alert is enabled
        if anomaly_type not in self.alert_configs or not self.alert_configs[anomaly_type].enabled:
            return
        
        # Check severity threshold
        alert_config = self.alert_configs[anomaly_type]
        severity_values = {
            AlertSeverity.CRITICAL: 4,
            AlertSeverity.HIGH: 3,
            AlertSeverity.MEDIUM: 2,
            AlertSeverity.LOW: 1,
            AlertSeverity.INFO: 0,
        }
        
        if severity_values[severity] < severity_values[alert_config.severity_threshold]:
            return
        
        # Check cooldown
        current_time = time.time()
        last_alert_time = self.last_alert_times[anomaly_type]
        
        if current_time - last_alert_time < alert_config.cooldown_seconds:
            return
        
        # Check alert count limit
        current_hour = int(current_time / 3600)
        alert_count = self.alert_counts[(anomaly_type, current_hour)]
        
        if alert_count >= alert_config.max_alerts_per_hour:
            return
        
        # Update tracking
        self.last_alert_times[anomaly_type] = current_time
        self.alert_counts[(anomaly_type, current_hour)] += 1
        
        # Create snapshot if enabled
        snapshot_path = None
        
        if self.snapshot_config.enabled:
            snapshot_path = self._create_snapshot(anomaly_type)
        
        # Create alert
        alert = Alert(
            anomaly_type=anomaly_type,
            severity=severity,
            message=message,
            details=details,
            timestamp=current_time,
            snapshot_path=snapshot_path,
            metrics=self._get_current_metrics(),
        )
        
        # Add to alerts list
        with self.alert_lock:
            self.alerts.append(alert)
        
        # Add to alert queue for processing
        self.alert_queue.put(alert)
        
        logger.info(f"Created alert: {message}")
    
    def _process_alert(self, alert: Alert) -> None:
        """
        Process an alert.
        
        Args:
            alert: Alert to process
        """
        # Get alert configuration
        alert_config = self.alert_configs.get(alert.anomaly_type)
        
        if not alert_config:
            logger.warning(f"No configuration found for alert type: {alert.anomaly_type}")
            return
        
        # Process alert through each channel
        for channel in alert_config.channels:
            try:
                if channel == AlertChannel.CLI:
                    self._send_cli_alert(alert)
                elif channel == AlertChannel.LOG:
                    self._send_log_alert(alert)
                elif channel == AlertChannel.EMAIL:
                    self._send_email_alert(alert)
                elif channel == AlertChannel.SLACK:
                    self._send_slack_alert(alert)
                elif channel == AlertChannel.WEBHOOK:
                    self._send_webhook_alert(alert)
                elif channel == AlertChannel.CUSTOM and alert_config.custom_handler:
                    alert_config.custom_handler(alert)
            except Exception as e:
                logger.error(f"Error sending alert through channel {channel}: {e}")
                logger.error(traceback.format_exc())
    
    def _send_cli_alert(self, alert: Alert) -> None:
        """
        Send alert to CLI.
        
        Args:
            alert: Alert to send
        """
        # Format alert message
        severity_colors = {
            AlertSeverity.CRITICAL: "\033[1;31m",  # Bold Red
            AlertSeverity.HIGH: "\033[31m",  # Red
            AlertSeverity.MEDIUM: "\033[33m",  # Yellow
            AlertSeverity.LOW: "\033[36m",  # Cyan
            AlertSeverity.INFO: "\033[37m",  # White
        }
        
        reset_color = "\033[0m"
        
        # Format timestamp
        timestamp = datetime.datetime.fromtimestamp(alert.timestamp).strftime("%Y-%m-%d %H:%M:%S")
        
        # Format message
        message = (
            f"{severity_colors[alert.severity]}[{alert.severity.value.upper()}] "
            f"{alert.anomaly_type.value} - {timestamp}{reset_color}\n"
            f"{alert.message}"
        )
        
        # Print to console
        print(message)
    
    def _send_log_alert(self, alert: Alert) -> None:
        """
        Send alert to log.
        
        Args:
            alert: Alert to send
        """
        # Map severity to log level
        severity_levels = {
            AlertSeverity.CRITICAL: logging.CRITICAL,
            AlertSeverity.HIGH: logging.ERROR,
            AlertSeverity.MEDIUM: logging.WARNING,
            AlertSeverity.LOW: logging.INFO,
            AlertSeverity.INFO: logging.INFO,
        }
        
        # Log message
        logger.log(
            severity_levels[alert.severity],
            f"[{alert.anomaly_type.value}] {alert.message}",
            extra={"alert": alert},
        )
    
    def _send_email_alert(self, alert: Alert) -> None:
        """
        Send alert via email.
        
        Args:
            alert: Alert to send
        """
        if not self.channel_config.enabled:
            return
        
        if not self.channel_config.email_server or not self.channel_config.email_from or not self.channel_config.email_to:
            logger.warning("Email configuration incomplete, cannot send email alert")
            return
        
        try:
            # Create message
            msg = MIMEMultipart()
            msg["From"] = self.channel_config.email_from
            msg["To"] = ", ".join(self.channel_config.email_to)
            msg["Subject"] = f"[{alert.severity.value.upper()}] AutoPipelineDoctor Alert: {alert.anomaly_type.value}"
            
            # Format timestamp
            timestamp = datetime.datetime.fromtimestamp(alert.timestamp).strftime("%Y-%m-%d %H:%M:%S")
            
            # Create HTML body
            html = f"""
            <html>
            <head>
                <style>
                    body {{ font-family: Arial, sans-serif; }}
                    .alert-header {{ padding: 10px; border-radius: 5px; margin-bottom: 20px; }}
                    .critical {{ background-color: #ffcccc; border: 1px solid #ff0000; }}
                    .high {{ background-color: #ffddcc; border: 1px solid #ff6600; }}
                    .medium {{ background-color: #ffffcc; border: 1px solid #ffcc00; }}
                    .low {{ background-color: #e6f2ff; border: 1px solid #0066cc; }}
                    .info {{ background-color: #f2f2f2; border: 1px solid #999999; }}
                    .details {{ background-color: #f9f9f9; border: 1px solid #ddd; padding: 10px; }}
                    table {{ border-collapse: collapse; width: 100%; }}
                    th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                    th {{ background-color: #f2f2f2; }}
                </style>
            </head>
            <body>
                <div class="alert-header {alert.severity.value}">
                    <h2>AutoPipelineDoctor Alert</h2>
                    <p><strong>Type:</strong> {alert.anomaly_type.value}</p>
                    <p><strong>Severity:</strong> {alert.severity.value.upper()}</p>
                    <p><strong>Time:</strong> {timestamp}</p>
                </div>
                
                <h3>Message</h3>
                <p>{alert.message}</p>
                
                <h3>Details</h3>
                <div class="details">
                    <table>
                        <tr>
                            <th>Key</th>
                            <th>Value</th>
                        </tr>
            """
            
            # Add details
            for key, value in alert.details.items():
                html += f"""
                        <tr>
                            <td>{key}</td>
                            <td>{value}</td>
                        </tr>
                """
            
            html += """
                    </table>
                </div>
            </body>
            </html>
            """
            
            # Attach HTML body
            msg.attach(MIMEText(html, "html"))
            
            # Attach snapshot if available
            if alert.snapshot_path and os.path.exists(alert.snapshot_path):
                with open(alert.snapshot_path, "rb") as f:
                    attachment = MIMEApplication(f.read(), Name=os.path.basename(alert.snapshot_path))
                    attachment["Content-Disposition"] = f'attachment; filename="{os.path.basename(alert.snapshot_path)}"'
                    msg.attach(attachment)
            
            # Connect to server and send
            server = smtplib.SMTP(self.channel_config.email_server, self.channel_config.email_port)
            
            if self.channel_config.email_use_tls:
                server.starttls()
            
            if self.channel_config.email_username and self.channel_config.email_password:
                server.login(self.channel_config.email_username, self.channel_config.email_password)
            
            server.sendmail(self.channel_config.email_from, self.channel_config.email_to, msg.as_string())
            server.quit()
            
            logger.info(f"Sent email alert to {', '.join(self.channel_config.email_to)}")
        
        except Exception as e:
            logger.error(f"Failed to send email alert: {e}")
            logger.error(traceback.format_exc())
    
    def _send_slack_alert(self, alert: Alert) -> None:
        """
        Send alert via Slack.
        
        Args:
            alert: Alert to send
        """
        if not self.channel_config.enabled:
            return
        
        if not self.channel_config.slack_webhook_url:
            logger.warning("Slack configuration incomplete, cannot send Slack alert")
            return
        
        try:
            # Format timestamp
            timestamp = datetime.datetime.fromtimestamp(alert.timestamp).strftime("%Y-%m-%d %H:%M:%S")
            
            # Map severity to color
            severity_colors = {
                AlertSeverity.CRITICAL: "#FF0000",  # Red
                AlertSeverity.HIGH: "#FFA500",  # Orange
                AlertSeverity.MEDIUM: "#FFFF00",  # Yellow
                AlertSeverity.LOW: "#0000FF",  # Blue
                AlertSeverity.INFO: "#808080",  # Gray
            }
            
            # Create message payload
            payload = {
                "username": self.channel_config.slack_username,
                "icon_emoji": ":robot_face:",
                "attachments": [
                    {
                        "fallback": f"[{alert.severity.value.upper()}] {alert.anomaly_type.value}: {alert.message}",
                        "color": severity_colors[alert.severity],
                        "title": f"AutoPipelineDoctor Alert: {alert.anomaly_type.value}",
                        "text": alert.message,
                        "fields": [
                            {
                                "title": "Severity",
                                "value": alert.severity.value.upper(),
                                "short": True,
                            },
                            {
                                "title": "Time",
                                "value": timestamp,
                                "short": True,
                            },
                        ],
                        "footer": "AutoPipelineDoctor",
                        "ts": int(alert.timestamp),
                    }
                ],
            }
            
            # Add details as fields
            for key, value in alert.details.items():
                payload["attachments"][0]["fields"].append({
                    "title": key,
                    "value": str(value),
                    "short": True,
                })
            
            # Add channel if specified
            if self.channel_config.slack_channel:
                payload["channel"] = self.channel_config.slack_channel
            
            # Send request
            response = requests.post(
                self.channel_config.slack_webhook_url,
                json=payload,
                headers={"Content-Type": "application/json"},
            )
            
            if response.status_code != 200:
                logger.warning(f"Failed to send Slack alert: {response.status_code} {response.text}")
            else:
                logger.info("Sent Slack alert")
        
        except Exception as e:
            logger.error(f"Failed to send Slack alert: {e}")
            logger.error(traceback.format_exc())
    
    def _send_webhook_alert(self, alert: Alert) -> None:
        """
        Send alert via webhook.
        
        Args:
            alert: Alert to send
        """
        if not self.channel_config.enabled:
            return
        
        if not self.channel_config.webhook_url:
            logger.warning("Webhook configuration incomplete, cannot send webhook alert")
            return
        
        try:
            # Format timestamp
            timestamp = datetime.datetime.fromtimestamp(alert.timestamp).strftime("%Y-%m-%d %H:%M:%S")
            
            # Create payload
            payload = {
                "alert_type": alert.anomaly_type.value,
                "severity": alert.severity.value,
                "message": alert.message,
                "details": alert.details,
                "timestamp": alert.timestamp,
                "formatted_timestamp": timestamp,
            }
            
            # Add metrics if available
            if alert.metrics:
                payload["metrics"] = alert.metrics
            
            # Send request
            response = requests.post(
                self.channel_config.webhook_url,
                json=payload,
                headers=self.channel_config.webhook_headers or {"Content-Type": "application/json"},
            )
            
            if response.status_code < 200 or response.status_code >= 300:
                logger.warning(f"Failed to send webhook alert: {response.status_code} {response.text}")
            else:
                logger.info("Sent webhook alert")
        
        except Exception as e:
            logger.error(f"Failed to send webhook alert: {e}")
            logger.error(traceback.format_exc())
    
    def _create_snapshot(self, anomaly_type: AnomalyType) -> Optional[str]:
        """
        Create a snapshot of the current state.
        
        Args:
            anomaly_type: Type of anomaly
            
        Returns:
            Path to the snapshot file or None
        """
        if not self.snapshot_config.enabled:
            return None
        
        try:
            # Create snapshot directory if it doesn't exist
            os.makedirs(self.snapshot_config.snapshot_dir, exist_ok=True)
            
            # Generate snapshot filename
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"snapshot_{anomaly_type.value}_{timestamp}.pkl"
            filepath = os.path.join(self.snapshot_config.snapshot_dir, filename)
            
            # Create snapshot object
            snapshot = Snapshot(
                timestamp=time.time(),
                anomaly_type=anomaly_type,
            )
            
            # Add logs if enabled
            if self.snapshot_config.include_logs:
                snapshot.logs = list(self.captured_logs)
            
            # Add metrics if enabled
            if self.snapshot_config.include_metrics:
                snapshot.metrics = self._get_current_metrics()
            
            # Add model state if enabled and model is available
            if self.snapshot_config.include_model_state and self.model is not None:
                try:
                    snapshot.model_state = {
                        "state_dict": copy.deepcopy(self.model.state_dict()),
                        "model_structure": str(self.model),
                    }
                except Exception as e:
                    logger.warning(f"Failed to capture model state: {e}")
            
            # Add gradients if enabled and model is available
            if self.snapshot_config.include_gradients and self.model is not None:
                try:
                    gradients = {}
                    
                    for name, param in self.model.named_parameters():
                        if param.grad is not None:
                            gradients[name] = param.grad.detach().cpu().numpy()
                    
                    snapshot.gradients = gradients
                except Exception as e:
                    logger.warning(f"Failed to capture gradients: {e}")
            
            # Add optimizer state if enabled and optimizer is available
            if self.snapshot_config.include_optimizer_state and self.optimizer is not None:
                try:
                    snapshot.optimizer_state = copy.deepcopy(self.optimizer.state_dict())
                except Exception as e:
                    logger.warning(f"Failed to capture optimizer state: {e}")
            
            # Add inputs and outputs if enabled and available
            if self.snapshot_config.include_inputs and self.current_inputs is not None:
                try:
                    if isinstance(self.current_inputs, torch.Tensor):
                        snapshot.inputs = self.current_inputs.detach().cpu().numpy()
                    else:
                        snapshot.inputs = self.current_inputs
                except Exception as e:
                    logger.warning(f"Failed to capture inputs: {e}")
            
            if self.snapshot_config.include_outputs and self.current_outputs is not None:
                try:
                    if isinstance(self.current_outputs, torch.Tensor):
                        snapshot.outputs = self.current_outputs.detach().cpu().numpy()
                    else:
                        snapshot.outputs = self.current_outputs
                except Exception as e:
                    logger.warning(f"Failed to capture outputs: {e}")
            
            # Add system info if enabled
            if self.snapshot_config.include_system_info:
                try:
                    system_info = {
                        "cpu_percent": psutil.cpu_percent(),
                        "memory": dict(psutil.virtual_memory()._asdict()),
                        "disk": dict(psutil.disk_usage("/")._asdict()),
                        "hostname": socket.gethostname(),
                        "pid": os.getpid(),
                        "process": dict(psutil.Process().as_dict(attrs=[
                            "cpu_percent", "memory_percent", "memory_info", "create_time", "num_threads"
                        ])),
                    }
                    
                    # Add GPU info if available
                    try:
                        import torch
                        
                        if torch.cuda.is_available():
                            gpu_info = {
                                "device_count": torch.cuda.device_count(),
                                "current_device": torch.cuda.current_device(),
                                "devices": [],
                            }
                            
                            for i in range(torch.cuda.device_count()):
                                device_info = {
                                    "name": torch.cuda.get_device_name(i),
                                    "memory_allocated": torch.cuda.memory_allocated(i),
                                    "memory_reserved": torch.cuda.memory_reserved(i),
                                }
                                
                                gpu_info["devices"].append(device_info)
                            
                            system_info["gpu"] = gpu_info
                    except (ImportError, Exception):
                        pass
                    
                    snapshot.system_info = system_info
                except Exception as e:
                    logger.warning(f"Failed to capture system info: {e}")
            
            # Add custom data if handler is available
            if self.snapshot_config.custom_snapshot_handler is not None:
                try:
                    snapshot.custom_data = self.snapshot_config.custom_snapshot_handler()
                except Exception as e:
                    logger.warning(f"Failed to capture custom data: {e}")
            
            # Save snapshot
            with open(filepath, "wb") as f:
                pickle.dump(snapshot, f)
            
            # Add to snapshots list
            with self.snapshot_lock:
                self.snapshots.append(snapshot)
                
                # Remove old snapshots if needed
                while len(self.snapshots) > self.snapshot_config.max_snapshots:
                    self.snapshots.pop(0)
            
            logger.info(f"Created snapshot: {filepath}")
            
            return filepath
        
        except Exception as e:
            logger.error(f"Failed to create snapshot: {e}")
            logger.error(traceback.format_exc())
            return None
    
    def _get_current_metrics(self) -> Dict[str, Any]:
        """
        Get current metrics.
        
        Returns:
            Current metrics
        """
        metrics = {}
        
        with self.metrics_lock:
            for key, values in self.metrics_history.items():
                if values:
                    metrics[key] = values[-1]
        
        return metrics
    
    def record_metric(self, name: str, value: Any) -> None:
        """
        Record a metric.
        
        Args:
            name: Metric name
            value: Metric value
        """
        with self.metrics_lock:
            self.metrics_history[name].append(value)
            
            # Update last activity time
            self.last_activity_time = time.time()
    
    def get_metric_history(self, name: str) -> List[Any]:
        """
        Get history of a metric.
        
        Args:
            name: Metric name
            
        Returns:
            Metric history
        """
        with self.metrics_lock:
            return list(self.metrics_history.get(name, []))
    
    def get_latest_metric(self, name: str) -> Optional[Any]:
        """
        Get latest value of a metric.
        
        Args:
            name: Metric name
            
        Returns:
            Latest metric value or None
        """
        with self.metrics_lock:
            values = self.metrics_history.get(name, [])
            return values[-1] if values else None
    
    def register_model(self, model: torch.nn.Module) -> None:
        """
        Register a model for monitoring.
        
        Args:
            model: PyTorch model
        """
        self.model = model
        logger.info(f"Registered model: {type(model).__name__}")
    
    def register_optimizer(self, optimizer: torch.optim.Optimizer) -> None:
        """
        Register an optimizer for monitoring.
        
        Args:
            optimizer: PyTorch optimizer
        """
        self.optimizer = optimizer
        logger.info(f"Registered optimizer: {type(optimizer).__name__}")
    
    def record_batch(self, inputs: Any, outputs: Any) -> None:
        """
        Record current batch inputs and outputs.
        
        Args:
            inputs: Batch inputs
            outputs: Batch outputs
        """
        self.current_inputs = inputs
        self.current_outputs = outputs
    
    def record_loss(self, loss: float) -> None:
        """
        Record loss value.
        
        Args:
            loss: Loss value
        """
        self.record_metric("loss", loss)
    
    def record_batch_time(self, batch_time: float) -> None:
        """
        Record batch processing time.
        
        Args:
            batch_time: Batch processing time in seconds
        """
        self.record_metric("batch_time", batch_time)
    
    def record_dataloader_time(self, dataloader_time: float) -> None:
        """
        Record dataloader time.
        
        Args:
            dataloader_time: Dataloader time in seconds
        """
        self.record_metric("dataloader_time", dataloader_time)
    
    def record_throughput(self, throughput: float) -> None:
        """
        Record throughput.
        
        Args:
            throughput: Throughput in samples per second
        """
        self.record_metric("throughput", throughput)
    
    def record_gradient_norm(self, norm: float) -> None:
        """
        Record gradient norm.
        
        Args:
            norm: Gradient norm
        """
        self.record_metric("gradient_norm", norm)
    
    def compute_gradient_norm(self) -> Optional[float]:
        """
        Compute gradient norm for the registered model.
        
        Returns:
            Gradient norm or None
        """
        if self.model is None:
            return None
        
        try:
            total_norm = 0.0
            
            for param in self.model.parameters():
                if param.grad is not None:
                    param_norm = param.grad.data.norm(2)
                    total_norm += param_norm.item() ** 2
            
            total_norm = total_norm ** 0.5
            
            # Record the norm
            self.record_gradient_norm(total_norm)
            
            return total_norm
        
        except Exception as e:
            logger.warning(f"Failed to compute gradient norm: {e}")
            return None
    
    def get_alerts(self, anomaly_type: Optional[AnomalyType] = None, max_count: Optional[int] = None) -> List[Alert]:
        """
        Get alerts.
        
        Args:
            anomaly_type: Filter by anomaly type
            max_count: Maximum number of alerts to return
            
        Returns:
            List of alerts
        """
        with self.alert_lock:
            if anomaly_type is not None:
                filtered_alerts = [alert for alert in self.alerts if alert.anomaly_type == anomaly_type]
            else:
                filtered_alerts = list(self.alerts)
            
            # Sort by timestamp (newest first)
            filtered_alerts.sort(key=lambda x: x.timestamp, reverse=True)
            
            if max_count is not None:
                filtered_alerts = filtered_alerts[:max_count]
            
            return filtered_alerts
    
    def get_snapshots(self, anomaly_type: Optional[AnomalyType] = None, max_count: Optional[int] = None) -> List[Snapshot]:
        """
        Get snapshots.
        
        Args:
            anomaly_type: Filter by anomaly type
            max_count: Maximum number of snapshots to return
            
        Returns:
            List of snapshots
        """
        with self.snapshot_lock:
            if anomaly_type is not None:
                filtered_snapshots = [snapshot for snapshot in self.snapshots if snapshot.anomaly_type == anomaly_type]
            else:
                filtered_snapshots = list(self.snapshots)
            
            # Sort by timestamp (newest first)
            filtered_snapshots.sort(key=lambda x: x.timestamp, reverse=True)
            
            if max_count is not None:
                filtered_snapshots = filtered_snapshots[:max_count]
            
            return filtered_snapshots
    
    def load_snapshot(self, path: str) -> Optional[Snapshot]:
        """
        Load a snapshot from file.
        
        Args:
            path: Path to snapshot file
            
        Returns:
            Loaded snapshot or None
        """
        try:
            with open(path, "rb") as f:
                snapshot = pickle.load(f)
            
            if not isinstance(snapshot, Snapshot):
                logger.warning(f"File does not contain a valid snapshot: {path}")
                return None
            
            return snapshot
        
        except Exception as e:
            logger.error(f"Failed to load snapshot: {e}")
            return None
    
    def visualize_metrics(
        self,
        metric_names: List[str],
        window: Optional[int] = None,
        output_path: Optional[str] = None,
        show_alerts: bool = True,
    ) -> Optional[str]:
        """
        Visualize metrics.
        
        Args:
            metric_names: Names of metrics to visualize
            window: Number of recent values to show
            output_path: Path to save the visualization
            show_alerts: Whether to show alerts on the plot
            
        Returns:
            Path to the saved visualization or None
        """
        try:
            # Create figure
            fig, axes = plt.subplots(len(metric_names), 1, figsize=(10, 3 * len(metric_names)), sharex=True)
            
            # Handle single metric case
            if len(metric_names) == 1:
                axes = [axes]
            
            # Plot each metric
            for i, metric_name in enumerate(metric_names):
                # Get metric history
                history = self.get_metric_history(metric_name)
                
                if not history:
                    axes[i].text(0.5, 0.5, f"No data for {metric_name}", ha="center", va="center")
                    axes[i].set_title(metric_name)
                    continue
                
                # Apply window if specified
                if window is not None and len(history) > window:
                    history = history[-window:]
                
                # Create x-axis (just indices)
                x = list(range(len(history)))
                
                # Plot metric
                axes[i].plot(x, history, ".-")
                axes[i].set_title(metric_name)
                axes[i].grid(True, alpha=0.3)
                
                # Show alerts if requested
                if show_alerts:
                    # Get alerts for this metric
                    alerts_for_metric = []
                    
                    with self.alert_lock:
                        for alert in self.alerts:
                            if metric_name in alert.metrics:
                                alerts_for_metric.append(alert)
                    
                    # Plot alert points
                    for alert in alerts_for_metric:
                        # Find the index of this alert in the history
                        try:
                            value = alert.metrics[metric_name]
                            
                            # Find closest value in history
                            closest_idx = min(range(len(history)), key=lambda i: abs(history[i] - value))
                            
                            # Plot alert point
                            color = "red" if alert.severity in [AlertSeverity.CRITICAL, AlertSeverity.HIGH] else "orange"
                            axes[i].plot(closest_idx, history[closest_idx], "o", color=color, markersize=8)
                        except (KeyError, ValueError):
                            continue
            
            # Adjust layout
            plt.tight_layout()
            
            # Save or show plot
            if output_path:
                plt.savefig(output_path, bbox_inches="tight", dpi=300)
                logger.info(f"Saved metrics visualization to {output_path}")
                plt.close(fig)
                return output_path
            else:
                plt.show()
                plt.close(fig)
                return None
        
        except Exception as e:
            logger.error(f"Failed to visualize metrics: {e}")
            return None
    
    def visualize_alert_history(
        self,
        output_path: Optional[str] = None,
        max_alerts: int = 100,
    ) -> Optional[str]:
        """
        Visualize alert history.
        
        Args:
            output_path: Path to save the visualization
            max_alerts: Maximum number of alerts to include
            
        Returns:
            Path to the saved visualization or None
        """
        try:
            # Get alerts
            with self.alert_lock:
                alerts = list(self.alerts)
            
            if not alerts:
                logger.warning("No alerts to visualize")
                return None
            
            # Sort by timestamp
            alerts.sort(key=lambda x: x.timestamp)
            
            # Limit number of alerts
            if len(alerts) > max_alerts:
                alerts = alerts[-max_alerts:]
            
            # Create figure
            plt.figure(figsize=(12, 6))
            
            # Create x-axis (timestamps)
            timestamps = [alert.timestamp for alert in alerts]
            x = list(range(len(timestamps)))
            
            # Map severity to numeric value
            severity_values = {
                AlertSeverity.CRITICAL: 4,
                AlertSeverity.HIGH: 3,
                AlertSeverity.MEDIUM: 2,
                AlertSeverity.LOW: 1,
                AlertSeverity.INFO: 0,
            }
            
            y = [severity_values[alert.severity] for alert in alerts]
            
            # Map severity to color
            severity_colors = {
                AlertSeverity.CRITICAL: "red",
                AlertSeverity.HIGH: "orange",
                AlertSeverity.MEDIUM: "yellow",
                AlertSeverity.LOW: "blue",
                AlertSeverity.INFO: "gray",
            }
            
            colors = [severity_colors[alert.severity] for alert in alerts]
            
            # Create scatter plot
            plt.scatter(x, y, c=colors, s=100, alpha=0.7)
            
            # Add labels
            plt.yticks(
                list(severity_values.values()),
                [severity.value.upper() for severity in severity_values.keys()],
            )
            
            # Format x-axis with timestamps
            if len(timestamps) > 10:
                # Show fewer ticks for readability
                tick_indices = list(range(0, len(timestamps), len(timestamps) // 10))
                if tick_indices[-1] != len(timestamps) - 1:
                    tick_indices.append(len(timestamps) - 1)
            else:
                tick_indices = list(range(len(timestamps)))
            
            plt.xticks(
                tick_indices,
                [datetime.datetime.fromtimestamp(timestamps[i]).strftime("%H:%M:%S") for i in tick_indices],
                rotation=45,
            )
            
            # Add grid and labels
            plt.grid(True, alpha=0.3)
            plt.xlabel("Time")
            plt.ylabel("Severity")
            plt.title("Alert History")
            
            # Adjust layout
            plt.tight_layout()
            
            # Save or show plot
            if output_path:
                plt.savefig(output_path, bbox_inches="tight", dpi=300)
                logger.info(f"Saved alert history visualization to {output_path}")
                plt.close()
                return output_path
            else:
                plt.show()
                plt.close()
                return None
        
        except Exception as e:
            logger.error(f"Failed to visualize alert history: {e}")
            return None
    
    def save_config(self, path: str) -> bool:
        """
        Save configuration to file.
        
        Args:
            path: Path to save the configuration
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Create configuration dictionary
            config = {
                "alert_configs": {k.value: {
                    "enabled": v.enabled,
                    "severity_threshold": v.severity_threshold.value,
                    "channels": [c.value for c in v.channels],
                    "cooldown_seconds": v.cooldown_seconds,
                    "max_alerts_per_hour": v.max_alerts_per_hour,
                } for k, v in self.alert_configs.items()},
                "channel_config": {
                    "enabled": self.channel_config.enabled,
                    "email_server": self.channel_config.email_server,
                    "email_port": self.channel_config.email_port,
                    "email_use_tls": self.channel_config.email_use_tls,
                    "email_username": self.channel_config.email_username,
                    "email_from": self.channel_config.email_from,
                    "email_to": self.channel_config.email_to,
                    "slack_webhook_url": self.channel_config.slack_webhook_url,
                    "slack_channel": self.channel_config.slack_channel,
                    "slack_username": self.channel_config.slack_username,
                    "webhook_url": self.channel_config.webhook_url,
                    "webhook_headers": self.channel_config.webhook_headers,
                    "custom_config": self.channel_config.custom_config,
                },
                "anomaly_config": {
                    "memory_spike_threshold": self.anomaly_config.memory_spike_threshold,
                    "memory_spike_window": self.anomaly_config.memory_spike_window,
                    "gpu_spike_threshold": self.anomaly_config.gpu_spike_threshold,
                    "gpu_spike_window": self.anomaly_config.gpu_spike_window,
                    "cpu_spike_threshold": self.anomaly_config.cpu_spike_threshold,
                    "cpu_spike_window": self.anomaly_config.cpu_spike_window,
                    "loss_spike_threshold": self.anomaly_config.loss_spike_threshold,
                    "loss_spike_window": self.anomaly_config.loss_spike_window,
                    "loss_stagnation_threshold": self.anomaly_config.loss_stagnation_threshold,
                    "loss_stagnation_window": self.anomaly_config.loss_stagnation_window,
                    "gradient_explosion_threshold": self.anomaly_config.gradient_explosion_threshold,
                    "gradient_vanishing_threshold": self.anomaly_config.gradient_vanishing_threshold,
                    "latency_spike_threshold": self.anomaly_config.latency_spike_threshold,
                    "latency_spike_window": self.anomaly_config.latency_spike_window,
                    "throughput_drop_threshold": self.anomaly_config.throughput_drop_threshold,
                    "throughput_drop_window": self.anomaly_config.throughput_drop_window,
                    "idle_threshold": self.anomaly_config.idle_threshold,
                    "idle_period_threshold": self.anomaly_config.idle_period_threshold,
                    "dataloader_stall_threshold": self.anomaly_config.dataloader_stall_threshold,
                    "oom_risk_threshold": self.anomaly_config.oom_risk_threshold,
                    "custom_config": self.anomaly_config.custom_config,
                },
                "snapshot_config": {
                    "enabled": self.snapshot_config.enabled,
                    "include_logs": self.snapshot_config.include_logs,
                    "include_metrics": self.snapshot_config.include_metrics,
                    "include_model_state": self.snapshot_config.include_model_state,
                    "include_gradients": self.snapshot_config.include_gradients,
                    "include_optimizer_state": self.snapshot_config.include_optimizer_state,
                    "include_inputs": self.snapshot_config.include_inputs,
                    "include_outputs": self.snapshot_config.include_outputs,
                    "include_system_info": self.snapshot_config.include_system_info,
                    "max_snapshots": self.snapshot_config.max_snapshots,
                    "snapshot_dir": self.snapshot_config.snapshot_dir,
                },
            }
            
            # Save to file
            with open(path, "w") as f:
                json.dump(config, f, indent=2)
            
            logger.info(f"Saved configuration to {path}")
            return True
        
        except Exception as e:
            logger.error(f"Failed to save configuration: {e}")
            return False
    
    def load_config(self, path: str) -> bool:
        """
        Load configuration from file.
        
        Args:
            path: Path to load the configuration from
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Load from file
            with open(path, "r") as f:
                config = json.load(f)
            
            # Parse alert configs
            if "alert_configs" in config:
                alert_configs = {}
                
                for anomaly_type_str, cfg in config["alert_configs"].items():
                    try:
                        anomaly_type = AnomalyType(anomaly_type_str)
                        
                        severity_threshold = AlertSeverity(cfg["severity_threshold"])
                        
                        channels = [AlertChannel(c) for c in cfg["channels"]]
                        
                        alert_configs[anomaly_type] = AlertConfig(
                            enabled=cfg["enabled"],
                            severity_threshold=severity_threshold,
                            channels=channels,
                            cooldown_seconds=cfg["cooldown_seconds"],
                            max_alerts_per_hour=cfg["max_alerts_per_hour"],
                        )
                    except (ValueError, KeyError) as e:
                        logger.warning(f"Failed to parse alert config for {anomaly_type_str}: {e}")
                
                self.alert_configs = alert_configs
            
            # Parse channel config
            if "channel_config" in config:
                cfg = config["channel_config"]
                
                self.channel_config = ChannelConfig(
                    enabled=cfg.get("enabled", True),
                    email_server=cfg.get("email_server", ""),
                    email_port=cfg.get("email_port", 587),
                    email_use_tls=cfg.get("email_use_tls", True),
                    email_username=cfg.get("email_username", ""),
                    email_password=cfg.get("email_password", ""),  # Note: Password might be missing for security
                    email_from=cfg.get("email_from", ""),
                    email_to=cfg.get("email_to", []),
                    slack_webhook_url=cfg.get("slack_webhook_url", ""),
                    slack_channel=cfg.get("slack_channel", ""),
                    slack_username=cfg.get("slack_username", "AutoPipelineDoctor"),
                    webhook_url=cfg.get("webhook_url", ""),
                    webhook_headers=cfg.get("webhook_headers", {}),
                    custom_config=cfg.get("custom_config", {}),
                )
            
            # Parse anomaly config
            if "anomaly_config" in config:
                cfg = config["anomaly_config"]
                
                self.anomaly_config = AnomalyDetectionConfig(
                    memory_spike_threshold=cfg.get("memory_spike_threshold", 0.2),
                    memory_spike_window=cfg.get("memory_spike_window", 5),
                    gpu_spike_threshold=cfg.get("gpu_spike_threshold", 0.3),
                    gpu_spike_window=cfg.get("gpu_spike_window", 5),
                    cpu_spike_threshold=cfg.get("cpu_spike_threshold", 0.3),
                    cpu_spike_window=cfg.get("cpu_spike_window", 5),
                    loss_spike_threshold=cfg.get("loss_spike_threshold", 0.5),
                    loss_spike_window=cfg.get("loss_spike_window", 5),
                    loss_stagnation_threshold=cfg.get("loss_stagnation_threshold", 0.01),
                    loss_stagnation_window=cfg.get("loss_stagnation_window", 20),
                    gradient_explosion_threshold=cfg.get("gradient_explosion_threshold", 100.0),
                    gradient_vanishing_threshold=cfg.get("gradient_vanishing_threshold", 1e-7),
                    latency_spike_threshold=cfg.get("latency_spike_threshold", 0.5),
                    latency_spike_window=cfg.get("latency_spike_window", 5),
                    throughput_drop_threshold=cfg.get("throughput_drop_threshold", 0.3),
                    throughput_drop_window=cfg.get("throughput_drop_window", 5),
                    idle_threshold=cfg.get("idle_threshold", 0.1),
                    idle_period_threshold=cfg.get("idle_period_threshold", 30.0),
                    dataloader_stall_threshold=cfg.get("dataloader_stall_threshold", 5.0),
                    oom_risk_threshold=cfg.get("oom_risk_threshold", 0.9),
                    custom_config=cfg.get("custom_config", {}),
                )
            
            # Parse snapshot config
            if "snapshot_config" in config:
                cfg = config["snapshot_config"]
                
                self.snapshot_config = SnapshotConfig(
                    enabled=cfg.get("enabled", True),
                    include_logs=cfg.get("include_logs", True),
                    include_metrics=cfg.get("include_metrics", True),
                    include_model_state=cfg.get("include_model_state", True),
                    include_gradients=cfg.get("include_gradients", False),
                    include_optimizer_state=cfg.get("include_optimizer_state", False),
                    include_inputs=cfg.get("include_inputs", False),
                    include_outputs=cfg.get("include_outputs", False),
                    include_system_info=cfg.get("include_system_info", True),
                    max_snapshots=cfg.get("max_snapshots", 10),
                    snapshot_dir=cfg.get("snapshot_dir", "./snapshots"),
                )
            
            logger.info(f"Loaded configuration from {path}")
            return True
        
        except Exception as e:
            logger.error(f"Failed to load configuration: {e}")
            return False
    
    def clear_alerts(self) -> None:
        """Clear all alerts."""
        with self.alert_lock:
            self.alerts = []
        
        logger.info("Cleared all alerts")
    
    def clear_snapshots(self) -> None:
        """Clear all snapshots."""
        with self.snapshot_lock:
            self.snapshots = []
        
        logger.info("Cleared all snapshots")
    
    def clear_metrics(self) -> None:
        """Clear all metrics."""
        with self.metrics_lock:
            self.metrics_history.clear()
        
        logger.info("Cleared all metrics")
    
    def clear_all(self) -> None:
        """Clear all data."""
        self.clear_alerts()
        self.clear_snapshots()
        self.clear_metrics()
        
        logger.info("Cleared all data")
    
    def get_status(self) -> Dict[str, Any]:
        """
        Get system status.
        
        Returns:
            System status
        """
        return {
            "running": self.running,
            "paused": self.paused,
            "alert_count": len(self.alerts),
            "snapshot_count": len(self.snapshots),
            "metrics_count": len(self.metrics_history),
            "last_activity_time": self.last_activity_time,
            "idle_duration": time.time() - self.last_activity_time,
        }
    
    def __del__(self) -> None:
        """Clean up resources."""
        self.stop()
