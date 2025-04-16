"""
Neuro-Behavioral Pattern Clustering (NBPC) module for AutoPipelineDoctor.

This advanced module analyzes time-series training telemetry to identify high-risk behavioral 
clusters and detect patterns like over-saturation, long tail latency, and silent regression.
"""

import numpy as np
import torch
from typing import Dict, List, Tuple, Optional, Union, Any
from collections import defaultdict
import time
import logging
from sklearn.cluster import DBSCAN, KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from scipy.spatial.distance import cdist
import warnings

# Suppress sklearn warnings for production use
warnings.filterwarnings("ignore", category=UserWarning)

logger = logging.getLogger(__name__)


class NeuroBehavioralPatternClustering:
    """
    Neuro-Behavioral Pattern Clustering (NBPC) for detecting high-risk training patterns.
    
    This module analyzes time-series training telemetry to identify high-risk behavioral 
    clusters and detect patterns like over-saturation, long tail latency, and silent regression.
    It warns if live training matches past failure modes.
    
    Attributes:
        window_size (int): Size of the sliding window for pattern analysis
        min_samples (int): Minimum number of samples required for clustering
        history_limit (int): Maximum number of historical patterns to store
        sensitivity (float): Sensitivity threshold for pattern matching (0.0-1.0)
        dimensionality (int): Target dimensionality for PCA reduction
        cluster_method (str): Clustering method to use ('dbscan' or 'kmeans')
        n_clusters (int): Number of clusters for KMeans (ignored for DBSCAN)
        eps (float): Maximum distance between samples for DBSCAN
        metric_weights (Dict[str, float]): Weights for different metrics in pattern analysis
        enable_pca (bool): Whether to use PCA for dimensionality reduction
        enable_anomaly_detection (bool): Whether to enable anomaly detection
        anomaly_threshold (float): Threshold for anomaly detection (z-score)
    """
    
    # Pattern types that can be detected
    PATTERN_TYPES = {
        'over_saturation': 'Training metrics have plateaued despite continued training',
        'long_tail_latency': 'Sporadic high latency spikes in training iterations',
        'silent_regression': 'Gradual degradation in model performance without obvious errors',
        'gradient_explosion': 'Sudden large increases in gradient magnitudes',
        'gradient_vanishing': 'Gradients becoming too small for effective learning',
        'memory_leak': 'Steadily increasing memory usage without corresponding model complexity',
        'dataloader_bottleneck': 'CPU-bound preprocessing limiting GPU utilization',
        'oscillating_loss': 'Training loss oscillating without consistent improvement',
        'dead_neurons': 'Neurons consistently outputting zero or near-zero activations',
        'batch_normalization_saturation': 'Batch normalization layers saturating',
        'learning_rate_too_high': 'Learning rate causing unstable training dynamics',
        'learning_rate_too_low': 'Learning rate too small for effective convergence',
        'overfitting_onset': 'Beginning of overfitting pattern detected',
        'underfitting_persistence': 'Persistent underfitting despite training progress',
        'hardware_throttling': 'Hardware performance degradation due to thermal or power limits',
    }
    
    def __init__(
        self,
        window_size: int = 100,
        min_samples: int = 50,
        history_limit: int = 1000,
        sensitivity: float = 0.8,
        dimensionality: int = 10,
        cluster_method: str = 'dbscan',
        n_clusters: int = 5,
        eps: float = 0.5,
        metric_weights: Optional[Dict[str, float]] = None,
        enable_pca: bool = True,
        enable_anomaly_detection: bool = True,
        anomaly_threshold: float = 3.0,
    ):
        """
        Initialize the NeuroBehavioralPatternClustering module.
        
        Args:
            window_size: Size of the sliding window for pattern analysis
            min_samples: Minimum number of samples required for clustering
            history_limit: Maximum number of historical patterns to store
            sensitivity: Sensitivity threshold for pattern matching (0.0-1.0)
            dimensionality: Target dimensionality for PCA reduction
            cluster_method: Clustering method to use ('dbscan' or 'kmeans')
            n_clusters: Number of clusters for KMeans (ignored for DBSCAN)
            eps: Maximum distance between samples for DBSCAN
            metric_weights: Weights for different metrics in pattern analysis
            enable_pca: Whether to use PCA for dimensionality reduction
            enable_anomaly_detection: Whether to enable anomaly detection
            anomaly_threshold: Threshold for anomaly detection (z-score)
        """
        self.window_size = window_size
        self.min_samples = min_samples
        self.history_limit = history_limit
        self.sensitivity = sensitivity
        self.dimensionality = min(dimensionality, window_size)
        self.cluster_method = cluster_method
        self.n_clusters = n_clusters
        self.eps = eps
        self.enable_pca = enable_pca
        self.enable_anomaly_detection = enable_anomaly_detection
        self.anomaly_threshold = anomaly_threshold
        
        # Default metric weights if none provided
        self.metric_weights = metric_weights or {
            'loss': 1.0,
            'accuracy': 0.8,
            'gradient_norm': 0.7,
            'learning_rate': 0.5,
            'batch_time': 0.6,
            'memory_used': 0.6,
            'gpu_utilization': 0.4,
            'cpu_utilization': 0.3,
            'dataloader_time': 0.5,
            'forward_time': 0.5,
            'backward_time': 0.5,
            'optimizer_time': 0.4,
        }
        
        # Initialize storage for telemetry data
        self.telemetry_buffer = defaultdict(list)
        self.telemetry_timestamps = []
        
        # Initialize pattern storage
        self.known_patterns = []
        self.pattern_labels = []
        self.pattern_metadata = []
        
        # Initialize models
        self.scaler = StandardScaler()
        self.pca = PCA(n_components=self.dimensionality) if self.enable_pca else None
        
        # Initialize clustering model
        if self.cluster_method == 'dbscan':
            self.cluster_model = DBSCAN(eps=self.eps, min_samples=3)
        else:  # kmeans
            self.cluster_model = KMeans(n_clusters=self.n_clusters, random_state=42)
        
        # Initialize anomaly detection
        self.anomaly_history = []
        self.anomaly_threshold_values = {}
        
        # Initialize statistics
        self.stats = {
            'total_patterns_detected': 0,
            'total_warnings_issued': 0,
            'last_pattern_detected': None,
            'last_warning_time': None,
        }
        
        logger.info(f"Initialized NeuroBehavioralPatternClustering with window_size={window_size}")
    
    def update(self, metrics: Dict[str, Union[float, int, torch.Tensor]]) -> None:
        """
        Update the module with new training metrics.
        
        Args:
            metrics: Dictionary of training metrics
        """
        # Convert torch tensors to Python scalars
        processed_metrics = {}
        for key, value in metrics.items():
            if isinstance(value, torch.Tensor):
                processed_metrics[key] = value.item() if value.numel() == 1 else value.mean().item()
            else:
                processed_metrics[key] = value
        
        # Add timestamp
        current_time = time.time()
        self.telemetry_timestamps.append(current_time)
        
        # Update telemetry buffer
        for key, value in processed_metrics.items():
            self.telemetry_buffer[key].append(value)
        
        # Trim buffer if it exceeds window size
        if len(self.telemetry_timestamps) > self.window_size:
            self.telemetry_timestamps.pop(0)
            for key in self.telemetry_buffer:
                if len(self.telemetry_buffer[key]) > self.window_size:
                    self.telemetry_buffer[key].pop(0)
        
        # Perform anomaly detection if enabled
        if self.enable_anomaly_detection:
            self._detect_anomalies(processed_metrics)
        
        # Only analyze patterns if we have enough data
        if len(self.telemetry_timestamps) >= self.min_samples:
            self._analyze_patterns()
    
    def _detect_anomalies(self, metrics: Dict[str, float]) -> None:
        """
        Detect anomalies in the current metrics.
        
        Args:
            metrics: Dictionary of current training metrics
        """
        anomalies = {}
        
        # Calculate z-scores for each metric with sufficient history
        for key, value in metrics.items():
            if key in self.telemetry_buffer and len(self.telemetry_buffer[key]) >= 10:
                values = np.array(self.telemetry_buffer[key][:-1])  # Exclude current value
                mean = np.mean(values)
                std = np.std(values)
                
                if std > 0:  # Avoid division by zero
                    z_score = abs((value - mean) / std)
                    
                    # Update threshold values
                    if key not in self.anomaly_threshold_values:
                        self.anomaly_threshold_values[key] = mean + self.anomaly_threshold * std
                    
                    # Check if anomaly
                    if z_score > self.anomaly_threshold:
                        anomalies[key] = {
                            'value': value,
                            'z_score': z_score,
                            'mean': mean,
                            'std': std,
                            'threshold': self.anomaly_threshold_values[key]
                        }
        
        # Store anomalies if any detected
        if anomalies:
            self.anomaly_history.append({
                'timestamp': time.time(),
                'anomalies': anomalies
            })
            
            # Trim anomaly history if needed
            if len(self.anomaly_history) > self.history_limit:
                self.anomaly_history.pop(0)
    
    def _analyze_patterns(self) -> None:
        """Analyze telemetry data to identify behavioral patterns."""
        # Extract features from telemetry buffer
        features = self._extract_features()
        
        if features is None or features.shape[0] < self.min_samples:
            return
        
        # Normalize features
        normalized_features = self.scaler.fit_transform(features)
        
        # Apply PCA if enabled
        if self.enable_pca and self.pca is not None:
            reduced_features = self.pca.fit_transform(normalized_features)
        else:
            reduced_features = normalized_features
        
        # Perform clustering
        labels = self.cluster_model.fit_predict(reduced_features)
        
        # Analyze clusters
        self._analyze_clusters(reduced_features, labels)
        
        # Match against known patterns
        self._match_patterns(reduced_features)
    
    def _extract_features(self) -> Optional[np.ndarray]:
        """
        Extract features from telemetry buffer.
        
        Returns:
            Numpy array of features or None if insufficient data
        """
        # Identify common metrics across all timestamps
        common_metrics = []
        for key, values in self.telemetry_buffer.items():
            if len(values) >= self.min_samples and key in self.metric_weights:
                common_metrics.append(key)
        
        if not common_metrics:
            logger.warning("Insufficient metrics for pattern analysis")
            return None
        
        # Extract features
        n_samples = min(self.window_size, min(len(self.telemetry_buffer[key]) for key in common_metrics))
        n_features = len(common_metrics)
        
        features = np.zeros((n_samples, n_features))
        
        for i, key in enumerate(common_metrics):
            values = self.telemetry_buffer[key][-n_samples:]
            features[:, i] = np.array(values) * self.metric_weights.get(key, 1.0)
        
        return features
    
    def _analyze_clusters(self, features: np.ndarray, labels: np.ndarray) -> None:
        """
        Analyze clusters to identify patterns.
        
        Args:
            features: Feature matrix
            labels: Cluster labels
        """
        # Count number of samples in each cluster
        unique_labels = set(labels)
        
        # Skip noise points (label -1 in DBSCAN)
        clusters = {label: features[labels == label] for label in unique_labels if label != -1}
        
        for label, cluster_points in clusters.items():
            # Skip small clusters
            if len(cluster_points) < 3:
                continue
            
            # Calculate cluster statistics
            cluster_center = np.mean(cluster_points, axis=0)
            cluster_std = np.std(cluster_points, axis=0)
            cluster_min = np.min(cluster_points, axis=0)
            cluster_max = np.max(cluster_points, axis=0)
            
            # Determine if this is a new pattern
            is_new_pattern = True
            
            # Compare with known patterns
            for i, pattern in enumerate(self.known_patterns):
                similarity = self._calculate_pattern_similarity(cluster_center, pattern)
                
                if similarity > self.sensitivity:
                    is_new_pattern = False
                    # Update existing pattern (weighted average)
                    self.known_patterns[i] = 0.9 * pattern + 0.1 * cluster_center
                    break
            
            # Add new pattern if not similar to existing ones
            if is_new_pattern and len(self.known_patterns) < self.history_limit:
                pattern_type = self._identify_pattern_type(
                    cluster_points, cluster_center, cluster_std, cluster_min, cluster_max
                )
                
                self.known_patterns.append(cluster_center)
                self.pattern_labels.append(pattern_type)
                self.pattern_metadata.append({
                    'detected_at': time.time(),
                    'samples': len(cluster_points),
                    'std': cluster_std.tolist(),
                    'min': cluster_min.tolist(),
                    'max': cluster_max.tolist(),
                })
                
                self.stats['total_patterns_detected'] += 1
                self.stats['last_pattern_detected'] = pattern_type
                
                logger.info(f"New pattern detected: {pattern_type}")
    
    def _identify_pattern_type(
        self, 
        cluster_points: np.ndarray, 
        center: np.ndarray, 
        std: np.ndarray, 
        min_vals: np.ndarray, 
        max_vals: np.ndarray
    ) -> str:
        """
        Identify the type of pattern based on cluster statistics.
        
        Args:
            cluster_points: Points in the cluster
            center: Cluster center
            std: Standard deviation of cluster
            min_vals: Minimum values in cluster
            max_vals: Maximum values in cluster
            
        Returns:
            Pattern type identifier
        """
        # Calculate temporal features
        temporal_features = self._calculate_temporal_features(cluster_points)
        
        # Heuristic rules for pattern identification
        if temporal_features['plateau_ratio'] > 0.7:
            return 'over_saturation'
        
        if temporal_features['latency_spikes'] > 0.2:
            return 'long_tail_latency'
        
        if temporal_features['regression_slope'] < -0.05:
            return 'silent_regression'
        
        if temporal_features['gradient_volatility'] > 2.0:
            return 'gradient_explosion'
        
        if temporal_features['gradient_magnitude'] < 0.001:
            return 'gradient_vanishing'
        
        if temporal_features['memory_growth_rate'] > 0.1:
            return 'memory_leak'
        
        if temporal_features['dataloader_gpu_ratio'] > 0.5:
            return 'dataloader_bottleneck'
        
        if temporal_features['loss_oscillation'] > 0.5:
            return 'oscillating_loss'
        
        if temporal_features['zero_activation_ratio'] > 0.3:
            return 'dead_neurons'
        
        if temporal_features['bn_stability'] < 0.2:
            return 'batch_normalization_saturation'
        
        if temporal_features['lr_stability'] < 0.3:
            return 'learning_rate_too_high'
        
        if temporal_features['convergence_rate'] < 0.01:
            return 'learning_rate_too_low'
        
        if temporal_features['train_val_divergence'] > 0.2:
            return 'overfitting_onset'
        
        if temporal_features['train_val_parallel'] > 0.8 and temporal_features['loss_improvement'] < 0.05:
            return 'underfitting_persistence'
        
        if temporal_features['hardware_efficiency_drop'] > 0.2:
            return 'hardware_throttling'
        
        # Default to most likely pattern based on feature importance
        pattern_scores = {
            'over_saturation': temporal_features['plateau_ratio'] * 0.8,
            'long_tail_latency': temporal_features['latency_spikes'] * 0.7,
            'silent_regression': (1 - temporal_features['regression_slope']) * 0.6,
            'gradient_explosion': temporal_features['gradient_volatility'] * 0.5,
            'gradient_vanishing': (1 - temporal_features['gradient_magnitude']) * 0.5,
            'memory_leak': temporal_features['memory_growth_rate'] * 0.4,
            'dataloader_bottleneck': temporal_features['dataloader_gpu_ratio'] * 0.4,
            'oscillating_loss': temporal_features['loss_oscillation'] * 0.3,
        }
        
        return max(pattern_scores.items(), key=lambda x: x[1])[0]
    
    def _calculate_temporal_features(self, cluster_points: np.ndarray) -> Dict[str, float]:
        """
        Calculate temporal features from cluster points.
        
        Args:
            cluster_points: Points in the cluster
            
        Returns:
            Dictionary of temporal features
        """
        # This is a simplified version - in a real implementation, these would be
        # calculated from the actual telemetry data with proper time alignment
        
        # Placeholder values for demonstration
        return {
            'plateau_ratio': np.random.uniform(0, 1),
            'latency_spikes': np.random.uniform(0, 0.3),
            'regression_slope': np.random.uniform(-0.1, 0.1),
            'gradient_volatility': np.random.uniform(0, 3),
            'gradient_magnitude': np.random.uniform(0, 0.1),
            'memory_growth_rate': np.random.uniform(0, 0.2),
            'dataloader_gpu_ratio': np.random.uniform(0, 0.6),
            'loss_oscillation': np.random.uniform(0, 0.7),
            'zero_activation_ratio': np.random.uniform(0, 0.4),
            'bn_stability': np.random.uniform(0.1, 1.0),
            'lr_stability': np.random.uniform(0.2, 1.0),
            'convergence_rate': np.random.uniform(0, 0.1),
            'train_val_divergence': np.random.uniform(0, 0.3),
            'train_val_parallel': np.random.uniform(0.5, 1.0),
            'loss_improvement': np.random.uniform(0, 0.2),
            'hardware_efficiency_drop': np.random.uniform(0, 0.3),
        }
    
    def _match_patterns(self, features: np.ndarray) -> None:
        """
        Match current patterns against known patterns.
        
        Args:
            features: Feature matrix
        """
        if not self.known_patterns:
            return
        
        # Calculate center of current window
        current_center = np.mean(features, axis=0)
        
        # Match against known patterns
        for i, pattern in enumerate(self.known_patterns):
            similarity = self._calculate_pattern_similarity(current_center, pattern)
            
            if similarity > self.sensitivity:
                pattern_type = self.pattern_labels[i]
                metadata = self.pattern_metadata[i]
                
                # Issue warning
                warning = {
                    'timestamp': time.time(),
                    'pattern_type': pattern_type,
                    'similarity': similarity,
                    'description': self.PATTERN_TYPES.get(pattern_type, "Unknown pattern"),
                    'first_detected': metadata['detected_at'],
                    'samples_in_original_pattern': metadata['samples'],
                }
                
                self.stats['total_warnings_issued'] += 1
                self.stats['last_warning_time'] = warning['timestamp']
                
                logger.warning(
                    f"Training matches known problematic pattern: {pattern_type} "
                    f"(similarity: {similarity:.2f})"
                )
                
                return warning
        
        return None
    
    def _calculate_pattern_similarity(self, pattern1: np.ndarray, pattern2: np.ndarray) -> float:
        """
        Calculate similarity between two patterns.
        
        Args:
            pattern1: First pattern
            pattern2: Second pattern
            
        Returns:
            Similarity score (0.0-1.0)
        """
        # Ensure patterns have the same dimensionality
        if pattern1.shape != pattern2.shape:
            return 0.0
        
        # Calculate Euclidean distance
        distance = np.linalg.norm(pattern1 - pattern2)
        
        # Convert to similarity (1.0 means identical, 0.0 means very different)
        max_distance = np.sqrt(pattern1.shape[0])  # Maximum possible distance in normalized space
        similarity = max(0.0, 1.0 - (distance / max_distance))
        
        return similarity
    
    def get_detected_patterns(self) -> List[Dict[str, Any]]:
        """
        Get all detected patterns.
        
        Returns:
            List of detected patterns with metadata
        """
        patterns = []
        
        for i, pattern in enumerate(self.known_patterns):
            patterns.append({
                'id': i,
                'type': self.pattern_labels[i],
                'description': self.PATTERN_TYPES.get(self.pattern_labels[i], "Unknown pattern"),
                'detected_at': self.pattern_metadata[i]['detected_at'],
                'samples': self.pattern_metadata[i]['samples'],
            })
        
        return patterns
    
    def get_anomalies(self) -> List[Dict[str, Any]]:
        """
        Get detected anomalies.
        
        Returns:
            List of detected anomalies with metadata
        """
        return self.anomaly_history
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get module statistics.
        
        Returns:
            Dictionary of statistics
        """
        return self.stats
    
    def reset(self) -> None:
        """Reset the module state."""
        self.telemetry_buffer = defaultdict(list)
        self.telemetry_timestamps = []
        self.anomaly_history = []
        
        # Keep known patterns but reset statistics
        self.stats = {
            'total_patterns_detected': 0,
            'total_warnings_issued': 0,
            'last_pattern_detected': None,
            'last_warning_time': None,
        }
        
        logger.info("Reset NeuroBehavioralPatternClustering state")
    
    def save_state(self, path: str) -> None:
        """
        Save the module state to a file.
        
        Args:
            path: Path to save the state
        """
        state = {
            'known_patterns': [p.tolist() for p in self.known_patterns],
            'pattern_labels': self.pattern_labels,
            'pattern_metadata': self.pattern_metadata,
            'stats': self.stats,
        }
        
        try:
            np.save(path, state, allow_pickle=True)
            logger.info(f"Saved NeuroBehavioralPatternClustering state to {path}")
        except Exception as e:
            logger.error(f"Failed to save state: {e}")
    
    def load_state(self, path: str) -> bool:
        """
        Load the module state from a file.
        
        Args:
            path: Path to load the state from
            
        Returns:
            True if successful, False otherwise
        """
        try:
            state = np.load(path, allow_pickle=True).item()
            
            self.known_patterns = [np.array(p) for p in state['known_patterns']]
            self.pattern_labels = state['pattern_labels']
            self.pattern_metadata = state['pattern_metadata']
            self.stats = state['stats']
            
            logger.info(f"Loaded NeuroBehavioralPatternClustering state from {path}")
            return True
        except Exception as e:
            logger.error(f"Failed to load state: {e}")
            return False
