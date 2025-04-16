"""
Federated Training Synchronization Monitor for AutoPipelineDoctor.

This module provides monitoring and optimization for federated learning training
processes, ensuring efficient synchronization and convergence across distributed nodes.
"""

import os
import time
import math
import json
import logging
import threading
import numpy as np
from typing import Dict, List, Optional, Union, Any, Tuple, Callable, Set
from collections import defaultdict, deque
import socket
import pickle
import hashlib
from datetime import datetime

import torch
import torch.nn as nn
from torch.optim import Optimizer

logger = logging.getLogger(__name__)


class FederatedTrainingSynchronizationMonitor:
    """
    Federated Training Synchronization Monitor for distributed deep learning.
    
    This class monitors and optimizes federated learning processes, ensuring efficient
    synchronization and convergence across distributed nodes. It tracks model updates,
    detects drift between nodes, optimizes communication patterns, and provides
    insights into the federated training process.
    
    Attributes:
        model: The PyTorch model being trained in federated setting
        node_id: Identifier for the current node
        total_nodes: Total number of nodes in the federated system
        sync_interval: Interval between synchronization events
        drift_threshold: Threshold for model drift detection
        output_dir: Directory to save monitoring results
        running: Whether the monitor is currently running
        node_states: States of all nodes in the system
        sync_history: History of synchronization events
        drift_metrics: Metrics for model drift between nodes
        communication_patterns: Patterns of communication between nodes
        monitoring_thread: Thread for continuous monitoring
    """
    
    def __init__(
        self,
        model: nn.Module,
        node_id: Optional[str] = None,
        total_nodes: int = 2,
        sync_interval: int = 10,
        drift_threshold: float = 0.1,
        communication_optimization: bool = True,
        output_dir: Optional[str] = None,
    ):
        """
        Initialize the FederatedTrainingSynchronizationMonitor.
        
        Args:
            model: PyTorch model being trained in federated setting
            node_id: Identifier for the current node (default: auto-generated)
            total_nodes: Total number of nodes in the federated system
            sync_interval: Interval between synchronization events (in iterations)
            drift_threshold: Threshold for model drift detection
            communication_optimization: Whether to optimize communication patterns
            output_dir: Directory to save monitoring results (optional)
        """
        self.model = model
        self.node_id = node_id or self._generate_node_id()
        self.total_nodes = max(2, total_nodes)
        self.sync_interval = max(1, sync_interval)
        self.drift_threshold = max(0.001, drift_threshold)
        self.communication_optimization = communication_optimization
        self.output_dir = output_dir or os.path.join(os.getcwd(), "federated_monitor_output")
        
        # Create output directory if it doesn't exist
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Initialize monitoring state
        self.running = False
        self.node_states = self._initialize_node_states()
        self.sync_history = []
        self.drift_metrics = {}
        self.communication_patterns = self._initialize_communication_patterns()
        self.monitoring_thread = None
        self.lock = threading.Lock()
        
        # Initialize model state tracking
        self.model_state_history = deque(maxlen=10)  # Keep last 10 model states
        self.current_iteration = 0
        self.last_sync_iteration = 0
        self.model_fingerprints = {}
        
        # Initialize performance metrics
        self.performance_metrics = {
            "sync_time": [],
            "communication_volume": [],
            "drift_over_time": [],
            "convergence_rate": [],
        }
        
        logger.info(f"Initialized FederatedTrainingSynchronizationMonitor for node {self.node_id} "
                   f"in a system with {self.total_nodes} nodes")
    
    def _generate_node_id(self) -> str:
        """
        Generate a unique node identifier.
        
        Returns:
            Unique node identifier
        """
        # Use hostname and timestamp to generate a unique ID
        hostname = socket.gethostname()
        timestamp = int(time.time())
        unique_string = f"{hostname}_{timestamp}_{os.getpid()}"
        
        # Create a hash of the unique string
        node_hash = hashlib.md5(unique_string.encode()).hexdigest()[:8]
        
        return f"node_{node_hash}"
    
    def _initialize_node_states(self) -> Dict[str, Dict[str, Any]]:
        """
        Initialize states for all nodes in the federated system.
        
        Returns:
            Dictionary mapping node IDs to their states
        """
        node_states = {}
        
        # Initialize current node
        node_states[self.node_id] = {
            "last_update_time": time.time(),
            "iterations_completed": 0,
            "model_fingerprint": self._compute_model_fingerprint(),
            "sync_count": 0,
            "drift_history": [],
            "performance_metrics": {
                "compute_capacity": self._estimate_compute_capacity(),
                "network_bandwidth": self._estimate_network_bandwidth(),
                "data_size": self._estimate_data_size(),
            },
            "online": True,
        }
        
        # Initialize placeholder states for other nodes
        for i in range(1, self.total_nodes):
            other_node_id = f"node_{i}" if f"node_{i}" != self.node_id else f"node_{i+1}"
            
            node_states[other_node_id] = {
                "last_update_time": 0,
                "iterations_completed": 0,
                "model_fingerprint": None,
                "sync_count": 0,
                "drift_history": [],
                "performance_metrics": {
                    "compute_capacity": 1.0,  # Placeholder
                    "network_bandwidth": 1.0,  # Placeholder
                    "data_size": 1.0,  # Placeholder
                },
                "online": False,  # Assume other nodes are offline until discovered
            }
        
        return node_states
    
    def _initialize_communication_patterns(self) -> Dict[str, Dict[str, Any]]:
        """
        Initialize communication patterns between nodes.
        
        Returns:
            Dictionary containing communication patterns
        """
        patterns = {}
        
        # Initialize patterns for all node pairs
        for node1 in self.node_states.keys():
            patterns[node1] = {}
            
            for node2 in self.node_states.keys():
                if node1 != node2:
                    patterns[node1][node2] = {
                        "last_sync_time": 0,
                        "sync_count": 0,
                        "avg_sync_duration": 0,
                        "communication_volume": 0,
                        "success_rate": 1.0,
                    }
        
        return patterns
    
    def _compute_model_fingerprint(self) -> str:
        """
        Compute a fingerprint of the current model state.
        
        Returns:
            Fingerprint string representing the model state
        """
        # Get model state dict
        state_dict = self.model.state_dict()
        
        # Compute statistics for each parameter tensor
        param_stats = {}
        
        for name, param in state_dict.items():
            if isinstance(param, torch.Tensor):
                tensor = param.detach().cpu().numpy()
                param_stats[name] = {
                    "mean": float(np.mean(tensor)),
                    "std": float(np.std(tensor)),
                    "norm": float(np.linalg.norm(tensor)),
                    "shape": list(tensor.shape),
                }
        
        # Create a deterministic string representation
        stats_str = json.dumps(param_stats, sort_keys=True)
        
        # Compute hash of the string
        fingerprint = hashlib.sha256(stats_str.encode()).hexdigest()[:16]
        
        return fingerprint
    
    def _estimate_compute_capacity(self) -> float:
        """
        Estimate the compute capacity of the current node.
        
        Returns:
            Relative compute capacity score
        """
        # Perform a simple benchmark
        start_time = time.time()
        
        # Create a test tensor and perform operations
        test_size = 1000
        test_tensor = torch.randn(test_size, test_size)
        
        # Perform matrix multiplication
        for _ in range(5):
            result = torch.matmul(test_tensor, test_tensor)
            _ = result.sum().item()
        
        # Measure time taken
        elapsed_time = time.time() - start_time
        
        # Normalize to a relative score (lower is better)
        # This is a simplified benchmark, in practice would be more comprehensive
        compute_capacity = 1.0 / max(0.001, elapsed_time)
        
        return compute_capacity
    
    def _estimate_network_bandwidth(self) -> float:
        """
        Estimate the network bandwidth of the current node.
        
        Returns:
            Estimated network bandwidth in MB/s
        """
        # This is a placeholder. In a real implementation, would perform
        # actual network tests or use system information.
        # For now, return a reasonable default value
        return 10.0  # 10 MB/s as a default
    
    def _estimate_data_size(self) -> float:
        """
        Estimate the size of the local training data.
        
        Returns:
            Estimated data size in MB
        """
        # This is a placeholder. In a real implementation, would measure
        # actual dataset size. For now, return a reasonable default value
        return 100.0  # 100 MB as a default
    
    def start(self) -> None:
        """Start the federated training synchronization monitor."""
        if self.running:
            logger.warning("Federated Training Synchronization Monitor is already running")
            return
        
        self.running = True
        self.monitoring_thread = threading.Thread(target=self._monitoring_loop)
        self.monitoring_thread.daemon = True
        self.monitoring_thread.start()
        
        logger.info(f"Started Federated Training Synchronization Monitor for node {self.node_id}")
    
    def stop(self) -> None:
        """Stop the federated training synchronization monitor."""
        if not self.running:
            logger.warning("Federated Training Synchronization Monitor is not running")
            return
        
        self.running = False
        if self.monitoring_thread is not None:
            self.monitoring_thread.join(timeout=5.0)
        
        logger.info(f"Stopped Federated Training Synchronization Monitor for node {self.node_id}")
    
    def _monitoring_loop(self) -> None:
        """Main monitoring loop for federated training."""
        while self.running:
            try:
                # Update node state
                self._update_node_state()
                
                # Check if synchronization is needed
                if self._should_synchronize():
                    self._perform_synchronization()
                
                # Monitor model drift
                self._monitor_model_drift()
                
                # Optimize communication patterns
                if self.communication_optimization:
                    self._optimize_communication_patterns()
                
                # Generate insights periodically
                if self.current_iteration % 50 == 0:
                    self._generate_insights()
                
                # Sleep to avoid consuming too many resources
                time.sleep(1.0)
            
            except Exception as e:
                logger.error(f"Error in federated monitoring loop: {e}")
                logger.exception(e)
                time.sleep(5.0)  # Sleep longer on error
    
    def _update_node_state(self) -> None:
        """Update the state of the current node."""
        with self.lock:
            # Update current node state
            self.node_states[self.node_id]["last_update_time"] = time.time()
            self.node_states[self.node_id]["iterations_completed"] = self.current_iteration
            self.node_states[self.node_id]["model_fingerprint"] = self._compute_model_fingerprint()
            
            # Save current model state for drift monitoring
            if self.current_iteration % 5 == 0:  # Save every 5 iterations to avoid excessive memory use
                self._save_current_model_state()
    
    def _save_current_model_state(self) -> None:
        """Save the current model state for later comparison."""
        # Compute fingerprint
        fingerprint = self._compute_model_fingerprint()
        
        # Save fingerprint with timestamp
        self.model_fingerprints[self.current_iteration] = {
            "fingerprint": fingerprint,
            "timestamp": time.time(),
        }
        
        # Save lightweight representation of model state
        state_summary = {}
        
        for name, param in self.model.state_dict().items():
            if isinstance(param, torch.Tensor):
                tensor = param.detach().cpu().numpy()
                # Save statistics instead of full tensors to save memory
                state_summary[name] = {
                    "mean": float(np.mean(tensor)),
                    "std": float(np.std(tensor)),
                    "norm": float(np.linalg.norm(tensor)),
                    "shape": list(tensor.shape),
                }
        
        # Add to history
        self.model_state_history.append({
            "iteration": self.current_iteration,
            "timestamp": time.time(),
            "fingerprint": fingerprint,
            "state_summary": state_summary,
        })
    
    def _should_synchronize(self) -> bool:
        """
        Determine if model synchronization is needed.
        
        Returns:
            True if synchronization is needed, False otherwise
        """
        # Check if enough iterations have passed since last sync
        iterations_since_sync = self.current_iteration - self.last_sync_iteration
        
        if iterations_since_sync >= self.sync_interval:
            return True
        
        # Check if model drift exceeds threshold
        if self._get_current_drift() > self.drift_threshold:
            logger.info(f"Model drift exceeds threshold ({self._get_current_drift():.4f} > {self.drift_threshold:.4f}), "
                       f"triggering synchronization")
            return True
        
        return False
    
    def _get_current_drift(self) -> float:
        """
        Calculate the current model drift.
        
        Returns:
            Current model drift value
        """
        # If no history, return 0
        if len(self.model_state_history) < 2:
            return 0.0
        
        # Get the most recent and the oldest state in history
        latest_state = self.model_state_history[-1]
        oldest_state = self.model_state_history[0]
        
        # Calculate drift based on parameter statistics
        drift_values = []
        
        for name, latest_stats in latest_state["state_summary"].items():
            if name in oldest_state["state_summary"]:
                oldest_stats = oldest_state["state_summary"][name]
                
                # Calculate relative changes in statistics
                mean_change = abs(latest_stats["mean"] - oldest_stats["mean"]) / (abs(oldest_stats["mean"]) + 1e-8)
                std_change = abs(latest_stats["std"] - oldest_stats["std"]) / (abs(oldest_stats["std"]) + 1e-8)
                norm_change = abs(latest_stats["norm"] - oldest_stats["norm"]) / (abs(oldest_stats["norm"]) + 1e-8)
                
                # Combine changes
                param_drift = (mean_change + std_change + norm_change) / 3.0
                drift_values.append(param_drift)
        
        # Return average drift across all parameters
        if drift_values:
            return sum(drift_values) / len(drift_values)
        else:
            return 0.0
    
    def _perform_synchronization(self) -> None:
        """Perform model synchronization with other nodes."""
        logger.info(f"Performing synchronization at iteration {self.current_iteration}")
        
        sync_start_time = time.time()
        
        # In a real implementation, this would involve actual communication
        # with other nodes. For this simulation, we'll update the sync history
        # and communication patterns.
        
        # Record synchronization event
        sync_event = {
            "iteration": self.current_iteration,
            "timestamp": time.time(),
            "node_id": self.node_id,
            "participating_nodes": list(self.node_states.keys()),
            "model_fingerprint": self._compute_model_fingerprint(),
        }
        
        # Simulate communication with other nodes
        for other_node_id, other_node_state in self.node_states.items():
            if other_node_id != self.node_id and other_node_state["online"]:
                # Update communication pattern
                self.communication_patterns[self.node_id][other_node_id]["last_sync_time"] = time.time()
                self.communication_patterns[self.node_id][other_node_id]["sync_count"] += 1
                
                # Estimate communication volume (model size in MB)
                model_size_mb = self._estimate_model_size_mb()
                self.communication_patterns[self.node_id][other_node_id]["communication_volume"] += model_size_mb
                
                # Record in performance metrics
                self.performance_metrics["communication_volume"].append(model_size_mb)
        
        # Update sync counters
        self.node_states[self.node_id]["sync_count"] += 1
        self.last_sync_iteration = self.current_iteration
        
        # Record sync duration
        sync_duration = time.time() - sync_start_time
        self.performance_metrics["sync_time"].append(sync_duration)
        
        # Add to sync history
        self.sync_history.append(sync_event)
        
        logger.info(f"Synchronization completed in {sync_duration:.2f} seconds")
    
    def _estimate_model_size_mb(self) -> float:
        """
        Estimate the size of the model in megabytes.
        
        Returns:
            Estimated model size in MB
        """
        total_bytes = 0
        
        for param in self.model.parameters():
            # Calculate bytes for this parameter
            numel = param.numel()
            element_size = param.element_size()
            total_bytes += numel * element_size
        
        # Convert to MB
        total_mb = total_bytes / (1024 * 1024)
        
        return total_mb
    
    def _monitor_model_drift(self) -> None:
        """Monitor and analyze model drift between nodes."""
        # In a real implementation, this would involve comparing model
        # states between nodes. For this simulation, we'll track drift
        # over time for the current node.
        
        current_drift = self._get_current_drift()
        
        # Record drift
        self.node_states[self.node_id]["drift_history"].append({
            "iteration": self.current_iteration,
            "timestamp": time.time(),
            "drift": current_drift,
        })
        
        # Add to performance metrics
        self.performance_metrics["drift_over_time"].append({
            "iteration": self.current_iteration,
            "drift": current_drift,
        })
        
        # Check for excessive drift
        if current_drift > self.drift_threshold * 2:
            logger.warning(f"Excessive model drift detected: {current_drift:.4f}")
    
    def _optimize_communication_patterns(self) -> None:
        """Optimize communication patterns between nodes."""
        if not self.communication_optimization:
            return
        
        # In a real implementation, this would involve analyzing communication
        # patterns and adjusting synchronization strategies. For this simulation,
        # we'll update the sync interval based on drift and performance.
        
        # Adjust sync interval based on drift
        avg_drift = np.mean([event["drift"] for event in self.node_states[self.node_id]["drift_history"][-5:]]) if self.node_states[self.node_id]["drift_history"] else 0
        
        if avg_drift > self.drift_threshold * 1.5:
            # High drift, decrease interval
            self.sync_interval = max(1, int(self.sync_interval * 0.8))
            logger.info(f"High drift detected, decreasing sync interval to {self.sync_interval}")
        elif avg_drift < self.drift_threshold * 0.5:
            # Low drift, increase interval
            self.sync_interval = min(50, int(self.sync_interval * 1.2))
            logger.info(f"Low drift detected, increasing sync interval to {self.sync_interval}")
    
    def _generate_insights(self) -> Dict[str, Any]:
        """
        Generate insights from monitoring data.
        
        Returns:
            Dictionary containing insights
        """
        insights = {
            "timestamp": time.time(),
            "iteration": self.current_iteration,
            "node_id": self.node_id,
            "sync_efficiency": {},
            "drift_analysis": {},
            "communication_efficiency": {},
            "recommendations": [],
        }
        
        # Analyze synchronization efficiency
        if self.performance_metrics["sync_time"]:
            avg_sync_time = np.mean(self.performance_metrics["sync_time"])
            insights["sync_efficiency"]["avg_sync_time"] = avg_sync_time
            insights["sync_efficiency"]["sync_frequency"] = self.sync_interval
            
            if avg_sync_time > 5.0:
                insights["recommendations"].append({
                    "type": "sync_optimization",
                    "message": f"Synchronization is taking {avg_sync_time:.2f} seconds on average. "
                              f"Consider optimizing model size or network communication.",
                    "priority": "high" if avg_sync_time > 10.0 else "medium",
                })
        
        # Analyze drift
        if self.performance_metrics["drift_over_time"]:
            recent_drift = [item["drift"] for item in self.performance_metrics["drift_over_time"][-10:]]
            avg_drift = np.mean(recent_drift)
            max_drift = np.max(recent_drift)
            
            insights["drift_analysis"]["avg_drift"] = avg_drift
            insights["drift_analysis"]["max_drift"] = max_drift
            insights["drift_analysis"]["drift_threshold"] = self.drift_threshold
            
            if avg_drift > self.drift_threshold:
                insights["recommendations"].append({
                    "type": "drift_management",
                    "message": f"Average model drift ({avg_drift:.4f}) exceeds threshold ({self.drift_threshold:.4f}). "
                              f"Consider decreasing synchronization interval or using a more robust aggregation method.",
                    "priority": "high" if avg_drift > self.drift_threshold * 2 else "medium",
                })
        
        # Analyze communication efficiency
        if self.performance_metrics["communication_volume"]:
            total_volume = sum(self.performance_metrics["communication_volume"])
            avg_volume = np.mean(self.performance_metrics["communication_volume"])
            
            insights["communication_efficiency"]["total_volume_mb"] = total_volume
            insights["communication_efficiency"]["avg_volume_per_sync_mb"] = avg_volume
            
            if avg_volume > 100:  # If average sync is more than 100MB
                insights["recommendations"].append({
                    "type": "communication_optimization",
                    "message": f"Communication volume is high ({avg_volume:.2f} MB per sync). "
                              f"Consider using model compression, quantization, or partial updates.",
                    "priority": "medium",
                })
        
        # Save insights to file
        self._save_insights(insights)
        
        return insights
    
    def _save_insights(self, insights: Dict[str, Any]) -> None:
        """
        Save insights to file.
        
        Args:
            insights: Dictionary containing insights
        """
        # Create filename with timestamp
        timestamp = datetime.fromtimestamp(insights["timestamp"]).strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(self.output_dir, f"insights_{self.node_id}_{timestamp}.json")
        
        # Save to file
        with open(filename, "w") as f:
            json.dump(insights, f, indent=2)
        
        logger.info(f"Saved insights to {filename}")
    
    def on_iteration_complete(self, iteration: int, metrics: Optional[Dict[str, Any]] = None) -> None:
        """
        Update monitor with information about completed iteration.
        
        Args:
            iteration: Current iteration number
            metrics: Training metrics for this iteration (optional)
        """
        with self.lock:
            self.current_iteration = iteration
            
            # Record convergence rate if loss is provided
            if metrics and "loss" in metrics:
                self.performance_metrics["convergence_rate"].append({
                    "iteration": iteration,
                    "loss": metrics["loss"],
                })
            
            # Update node state
            self._update_node_state()
    
    def register_node(self, node_id: str, performance_metrics: Optional[Dict[str, Any]] = None) -> None:
        """
        Register a new node in the federated system.
        
        Args:
            node_id: Identifier for the node
            performance_metrics: Performance metrics for the node (optional)
        """
        with self.lock:
            if node_id not in self.node_states:
                # Add new node
                self.node_states[node_id] = {
                    "last_update_time": time.time(),
                    "iterations_completed": 0,
                    "model_fingerprint": None,
                    "sync_count": 0,
                    "drift_history": [],
                    "performance_metrics": performance_metrics or {
                        "compute_capacity": 1.0,
                        "network_bandwidth": 1.0,
                        "data_size": 1.0,
                    },
                    "online": True,
                }
                
                # Update communication patterns
                self.communication_patterns[node_id] = {}
                for other_node_id in self.node_states.keys():
                    if other_node_id != node_id:
                        self.communication_patterns[node_id][other_node_id] = {
                            "last_sync_time": 0,
                            "sync_count": 0,
                            "avg_sync_duration": 0,
                            "communication_volume": 0,
                            "success_rate": 1.0,
                        }
                        
                        self.communication_patterns[other_node_id][node_id] = {
                            "last_sync_time": 0,
                            "sync_count": 0,
                            "avg_sync_duration": 0,
                            "communication_volume": 0,
                            "success_rate": 1.0,
                        }
                
                logger.info(f"Registered new node: {node_id}")
            else:
                # Update existing node
                self.node_states[node_id]["last_update_time"] = time.time()
                self.node_states[node_id]["online"] = True
                
                if performance_metrics:
                    self.node_states[node_id]["performance_metrics"] = performance_metrics
                
                logger.info(f"Updated existing node: {node_id}")
    
    def update_node_state(self, node_id: str, state_update: Dict[str, Any]) -> None:
        """
        Update the state of a node in the federated system.
        
        Args:
            node_id: Identifier for the node
            state_update: Dictionary containing state updates
        """
        with self.lock:
            if node_id in self.node_states:
                # Update node state
                for key, value in state_update.items():
                    if key in self.node_states[node_id]:
                        self.node_states[node_id][key] = value
                
                # Update last update time
                self.node_states[node_id]["last_update_time"] = time.time()
                self.node_states[node_id]["online"] = True
                
                logger.debug(f"Updated state for node: {node_id}")
            else:
                logger.warning(f"Attempted to update unknown node: {node_id}")
    
    def get_node_states(self) -> Dict[str, Dict[str, Any]]:
        """
        Get the current states of all nodes.
        
        Returns:
            Dictionary mapping node IDs to their states
        """
        with self.lock:
            # Create a copy to avoid threading issues
            return {node_id: state.copy() for node_id, state in self.node_states.items()}
    
    def get_sync_history(self) -> List[Dict[str, Any]]:
        """
        Get the history of synchronization events.
        
        Returns:
            List of synchronization events
        """
        with self.lock:
            # Create a copy to avoid threading issues
            return [event.copy() for event in self.sync_history]
    
    def get_performance_metrics(self) -> Dict[str, Any]:
        """
        Get performance metrics for the federated training.
        
        Returns:
            Dictionary containing performance metrics
        """
        with self.lock:
            # Create a copy to avoid threading issues
            return {key: value.copy() if isinstance(value, list) else value 
                   for key, value in self.performance_metrics.items()}
    
    def get_recommendations(self) -> List[Dict[str, Any]]:
        """
        Get recommendations for improving federated training.
        
        Returns:
            List of recommendations
        """
        # Generate insights to get latest recommendations
        insights = self._generate_insights()
        
        return insights["recommendations"]
    
    def visualize_drift(self, output_file: Optional[str] = None) -> Dict[str, Any]:
        """
        Generate visualization data for model drift.
        
        Args:
            output_file: Path to save visualization data (optional)
            
        Returns:
            Dictionary containing visualization data
        """
        with self.lock:
            # Extract drift history
            drift_data = []
            
            for item in self.performance_metrics["drift_over_time"]:
                drift_data.append({
                    "iteration": item["iteration"],
                    "drift": item["drift"],
                })
            
            # Add threshold line
            threshold_data = [
                {"iteration": 0, "value": self.drift_threshold},
                {"iteration": self.current_iteration, "value": self.drift_threshold},
            ]
            
            # Create visualization data
            visualization = {
                "title": "Model Drift Over Time",
                "x_label": "Iteration",
                "y_label": "Drift",
                "series": [
                    {
                        "name": "Model Drift",
                        "data": drift_data,
                    },
                    {
                        "name": "Drift Threshold",
                        "data": threshold_data,
                    },
                ],
                "sync_events": [
                    {"iteration": event["iteration"]}
                    for event in self.sync_history
                ],
            }
            
            # Save to file if requested
            if output_file:
                with open(output_file, "w") as f:
                    json.dump(visualization, f, indent=2)
                
                logger.info(f"Saved drift visualization to {output_file}")
            
            return visualization
    
    def visualize_communication(self, output_file: Optional[str] = None) -> Dict[str, Any]:
        """
        Generate visualization data for communication patterns.
        
        Args:
            output_file: Path to save visualization data (optional)
            
        Returns:
            Dictionary containing visualization data
        """
        with self.lock:
            # Extract communication volume data
            volume_data = []
            
            for i, volume in enumerate(self.performance_metrics["communication_volume"]):
                volume_data.append({
                    "sync_index": i,
                    "volume_mb": volume,
                })
            
            # Create node connection graph
            nodes = []
            edges = []
            
            for node_id in self.node_states.keys():
                nodes.append({
                    "id": node_id,
                    "online": self.node_states[node_id]["online"],
                    "sync_count": self.node_states[node_id]["sync_count"],
                })
            
            for node1 in self.communication_patterns.keys():
                for node2, pattern in self.communication_patterns[node1].items():
                    if pattern["sync_count"] > 0:
                        edges.append({
                            "source": node1,
                            "target": node2,
                            "sync_count": pattern["sync_count"],
                            "volume_mb": pattern["communication_volume"],
                        })
            
            # Create visualization data
            visualization = {
                "title": "Federated Communication Patterns",
                "volume_chart": {
                    "title": "Communication Volume Over Time",
                    "x_label": "Synchronization Index",
                    "y_label": "Volume (MB)",
                    "data": volume_data,
                },
                "network_graph": {
                    "nodes": nodes,
                    "edges": edges,
                },
            }
            
            # Save to file if requested
            if output_file:
                with open(output_file, "w") as f:
                    json.dump(visualization, f, indent=2)
                
                logger.info(f"Saved communication visualization to {output_file}")
            
            return visualization
    
    def generate_report(self, output_file: Optional[str] = None) -> Dict[str, Any]:
        """
        Generate a comprehensive report on federated training.
        
        Args:
            output_file: Path to save report (optional)
            
        Returns:
            Dictionary containing report data
        """
        with self.lock:
            # Create report structure
            report = {
                "title": "Federated Training Synchronization Report",
                "timestamp": time.time(),
                "node_id": self.node_id,
                "total_nodes": self.total_nodes,
                "current_iteration": self.current_iteration,
                "sync_interval": self.sync_interval,
                "drift_threshold": self.drift_threshold,
                "total_syncs": len(self.sync_history),
                "node_states": self.get_node_states(),
                "performance_summary": self._generate_performance_summary(),
                "drift_analysis": self._generate_drift_analysis(),
                "communication_analysis": self._generate_communication_analysis(),
                "recommendations": self.get_recommendations(),
                "visualizations": {
                    "drift": self.visualize_drift(),
                    "communication": self.visualize_communication(),
                },
            }
            
            # Save to file if requested
            if output_file:
                with open(output_file, "w") as f:
                    json.dump(report, f, indent=2)
                
                logger.info(f"Saved federated training report to {output_file}")
            
            return report
    
    def _generate_performance_summary(self) -> Dict[str, Any]:
        """
        Generate a summary of performance metrics.
        
        Returns:
            Dictionary containing performance summary
        """
        summary = {
            "sync_time": {},
            "communication_volume": {},
            "convergence": {},
        }
        
        # Sync time statistics
        if self.performance_metrics["sync_time"]:
            sync_times = self.performance_metrics["sync_time"]
            summary["sync_time"] = {
                "avg": float(np.mean(sync_times)),
                "min": float(np.min(sync_times)),
                "max": float(np.max(sync_times)),
                "total": float(np.sum(sync_times)),
            }
        
        # Communication volume statistics
        if self.performance_metrics["communication_volume"]:
            volumes = self.performance_metrics["communication_volume"]
            summary["communication_volume"] = {
                "avg_per_sync": float(np.mean(volumes)),
                "total": float(np.sum(volumes)),
                "syncs": len(volumes),
            }
        
        # Convergence statistics
        if self.performance_metrics["convergence_rate"]:
            losses = [item["loss"] for item in self.performance_metrics["convergence_rate"]]
            iterations = [item["iteration"] for item in self.performance_metrics["convergence_rate"]]
            
            if losses:
                summary["convergence"] = {
                    "initial_loss": float(losses[0]),
                    "final_loss": float(losses[-1]),
                    "improvement": float(losses[0] - losses[-1]) / float(losses[0]) if losses[0] != 0 else 0,
                    "iterations": len(losses),
                }
        
        return summary
    
    def _generate_drift_analysis(self) -> Dict[str, Any]:
        """
        Generate analysis of model drift.
        
        Returns:
            Dictionary containing drift analysis
        """
        analysis = {
            "current_drift": self._get_current_drift(),
            "threshold": self.drift_threshold,
            "drift_triggered_syncs": 0,
            "drift_over_time": {},
        }
        
        # Count drift-triggered synchronizations
        for i in range(1, len(self.sync_history)):
            prev_sync = self.sync_history[i-1]
            curr_sync = self.sync_history[i]
            
            iterations_between = curr_sync["iteration"] - prev_sync["iteration"]
            
            if iterations_between < self.sync_interval:
                analysis["drift_triggered_syncs"] += 1
        
        # Analyze drift over time
        if self.performance_metrics["drift_over_time"]:
            drifts = [item["drift"] for item in self.performance_metrics["drift_over_time"]]
            
            analysis["drift_over_time"] = {
                "avg": float(np.mean(drifts)),
                "max": float(np.max(drifts)),
                "min": float(np.min(drifts)),
                "std": float(np.std(drifts)),
                "above_threshold_percent": float(np.mean([1 if d > self.drift_threshold else 0 for d in drifts])) * 100,
            }
        
        return analysis
    
    def _generate_communication_analysis(self) -> Dict[str, Any]:
        """
        Generate analysis of communication patterns.
        
        Returns:
            Dictionary containing communication analysis
        """
        analysis = {
            "total_volume_mb": sum(self.performance_metrics["communication_volume"]),
            "total_syncs": len(self.sync_history),
            "avg_volume_per_sync_mb": np.mean(self.performance_metrics["communication_volume"]) if self.performance_metrics["communication_volume"] else 0,
            "node_connectivity": {},
        }
        
        # Analyze node connectivity
        for node_id in self.node_states.keys():
            if node_id in self.communication_patterns:
                connections = 0
                total_volume = 0
                
                for other_node_id, pattern in self.communication_patterns[node_id].items():
                    if pattern["sync_count"] > 0:
                        connections += 1
                        total_volume += pattern["communication_volume"]
                
                analysis["node_connectivity"][node_id] = {
                    "connections": connections,
                    "total_volume_mb": total_volume,
                    "online": self.node_states[node_id]["online"],
                }
        
        return analysis
    
    def simulate_node_failure(self, node_id: Optional[str] = None) -> None:
        """
        Simulate a node failure for testing recovery mechanisms.
        
        Args:
            node_id: ID of node to simulate failure for (default: random node)
        """
        with self.lock:
            # If no node specified, choose a random one (not self)
            if node_id is None:
                other_nodes = [nid for nid in self.node_states.keys() if nid != self.node_id]
                if other_nodes:
                    node_id = random.choice(other_nodes)
                else:
                    logger.warning("No other nodes to simulate failure for")
                    return
            
            # Mark node as offline
            if node_id in self.node_states:
                self.node_states[node_id]["online"] = False
                logger.info(f"Simulated failure for node {node_id}")
            else:
                logger.warning(f"Cannot simulate failure for unknown node: {node_id}")
    
    def simulate_node_recovery(self, node_id: Optional[str] = None) -> None:
        """
        Simulate a node recovery after failure.
        
        Args:
            node_id: ID of node to simulate recovery for (default: all failed nodes)
        """
        with self.lock:
            if node_id is None:
                # Recover all failed nodes
                for nid, state in self.node_states.items():
                    if not state["online"]:
                        state["online"] = True
                        state["last_update_time"] = time.time()
                        logger.info(f"Simulated recovery for node {nid}")
            elif node_id in self.node_states:
                # Recover specific node
                self.node_states[node_id]["online"] = True
                self.node_states[node_id]["last_update_time"] = time.time()
                logger.info(f"Simulated recovery for node {node_id}")
            else:
                logger.warning(f"Cannot simulate recovery for unknown node: {node_id}")
    
    def apply_optimal_sync_strategy(self) -> Dict[str, Any]:
        """
        Apply the optimal synchronization strategy based on monitoring data.
        
        Returns:
            Dictionary containing applied changes and recommendations
        """
        with self.lock:
            # Analyze drift and sync patterns
            drift_analysis = self._generate_drift_analysis()
            performance_summary = self._generate_performance_summary()
            
            changes = {}
            recommendations = []
            
            # Adjust sync interval based on drift
            old_sync_interval = self.sync_interval
            
            if drift_analysis["drift_over_time"].get("above_threshold_percent", 0) > 50:
                # High drift frequency, decrease interval
                self.sync_interval = max(1, int(self.sync_interval * 0.7))
                changes["sync_interval"] = {
                    "old": old_sync_interval,
                    "new": self.sync_interval,
                    "reason": "High drift frequency",
                }
            elif drift_analysis["drift_over_time"].get("above_threshold_percent", 0) < 10:
                # Low drift frequency, increase interval
                self.sync_interval = min(50, int(self.sync_interval * 1.3))
                changes["sync_interval"] = {
                    "old": old_sync_interval,
                    "new": self.sync_interval,
                    "reason": "Low drift frequency",
                }
            
            # Adjust drift threshold based on observed drift
            old_threshold = self.drift_threshold
            
            if drift_analysis["drift_over_time"].get("avg", 0) > self.drift_threshold * 2:
                # Average drift much higher than threshold, increase threshold
                self.drift_threshold = min(0.5, self.drift_threshold * 1.5)
                changes["drift_threshold"] = {
                    "old": old_threshold,
                    "new": self.drift_threshold,
                    "reason": "Average drift much higher than threshold",
                }
            elif drift_analysis["drift_over_time"].get("max", 0) < self.drift_threshold * 0.5:
                # Maximum drift much lower than threshold, decrease threshold
                self.drift_threshold = max(0.001, self.drift_threshold * 0.7)
                changes["drift_threshold"] = {
                    "old": old_threshold,
                    "new": self.drift_threshold,
                    "reason": "Maximum drift much lower than threshold",
                }
            
            # Generate recommendations
            if performance_summary.get("communication_volume", {}).get("avg_per_sync", 0) > 50:
                recommendations.append({
                    "type": "communication_optimization",
                    "message": "Consider implementing model compression or quantization to reduce communication volume.",
                    "priority": "medium",
                })
            
            if performance_summary.get("sync_time", {}).get("avg", 0) > 2.0:
                recommendations.append({
                    "type": "sync_optimization",
                    "message": "Synchronization is taking longer than optimal. Consider optimizing network communication or reducing model size.",
                    "priority": "medium",
                })
            
            # Log changes
            if changes:
                logger.info(f"Applied optimal sync strategy: {changes}")
            
            return {
                "changes": changes,
                "recommendations": recommendations,
            }
    
    def get_monitoring_status(self) -> Dict[str, Any]:
        """
        Get the current status of the federated monitoring.
        
        Returns:
            Dictionary containing monitoring status
        """
        with self.lock:
            return {
                "running": self.running,
                "node_id": self.node_id,
                "total_nodes": self.total_nodes,
                "online_nodes": sum(1 for state in self.node_states.values() if state["online"]),
                "current_iteration": self.current_iteration,
                "sync_interval": self.sync_interval,
                "drift_threshold": self.drift_threshold,
                "last_sync_iteration": self.last_sync_iteration,
                "current_drift": self._get_current_drift(),
                "total_syncs": len(self.sync_history),
                "output_dir": self.output_dir,
            }
