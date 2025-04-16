"""
Memory module for AutoPipelineDoctor.
"""

from typing import Dict, List, Optional, Any, Union, Tuple
import logging
import os
import json
import time
import sqlite3
import pickle
import numpy as np
from datetime import datetime
import hashlib

logger = logging.getLogger(__name__)

class RunRecord:
    """
    Stores comprehensive information about a training run.
    
    This class encapsulates all data related to a single training run,
    including model and dataset information, hardware configuration,
    metrics, warnings, and optimizations applied.
    """
    
    def __init__(self, run_id: Optional[str] = None, 
                model_name: Optional[str] = None,
                dataset_name: Optional[str] = None,
                hardware_info: Optional[Dict[str, Any]] = None,
                config: Optional[Dict[str, Any]] = None):
        """
        Initialize a run record.
        
        Args:
            run_id: Unique identifier for the run (generated if not provided)
            model_name: Name of the model
            dataset_name: Name of the dataset
            hardware_info: Hardware configuration information
            config: Training configuration
        """
        # Set run ID
        if run_id:
            self.run_id = run_id
        else:
            self.run_id = self._generate_run_id()
        
        # Set basic information
        self.model_name = model_name
        self.dataset_name = dataset_name
        self.hardware_info = hardware_info or {}
        self.config = config or {}
        
        # Initialize metrics storage
        self.metrics = {
            'batch': [],
            'epoch': [],
            'memory': [],
            'timing': [],
            'gradients': [],
            'hardware': []
        }
        
        # Initialize events, warnings, and optimizations
        self.events = []
        self.warnings = []
        self.optimizations = []
        
        # Set timestamps
        self.start_time = time.time()
        self.end_time = None
        self.duration = None
        
        # Set status
        self.status = 'running'
        
        # Set tags
        self.tags = []
    
    def _generate_run_id(self) -> str:
        """
        Generate a unique run ID.
        
        Returns:
            Unique run ID
        """
        timestamp = int(time.time())
        random_suffix = os.urandom(4).hex()
        return f"run_{timestamp}_{random_suffix}"
    
    def add_metrics(self, category: str, metrics: Dict[str, Any]):
        """
        Add metrics to the run record.
        
        Args:
            category: Category of metrics (e.g., 'batch', 'memory')
            metrics: Dictionary of metrics
        """
        if category in self.metrics:
            # Add timestamp if not present
            if 'timestamp' not in metrics:
                metrics['timestamp'] = time.time()
            
            self.metrics[category].append(metrics)
        else:
            logger.warning(f"Unknown metrics category: {category}")
    
    def add_event(self, event_type: str, message: str, details: Optional[Dict[str, Any]] = None):
        """
        Add an event to the run record.
        
        Args:
            event_type: Type of event
            message: Event message
            details: Additional event details
        """
        event = {
            'type': event_type,
            'message': message,
            'timestamp': time.time(),
            'details': details or {}
        }
        
        self.events.append(event)
    
    def add_warning(self, warning_type: str, message: str, severity: str = 'medium', 
                   details: Optional[Dict[str, Any]] = None):
        """
        Add a warning to the run record.
        
        Args:
            warning_type: Type of warning
            message: Warning message
            severity: Warning severity ('low', 'medium', 'high', 'critical')
            details: Additional warning details
        """
        warning = {
            'type': warning_type,
            'message': message,
            'severity': severity,
            'timestamp': time.time(),
            'details': details or {}
        }
        
        self.warnings.append(warning)
    
    def add_optimization(self, optimization_type: str, message: str, 
                        applied: bool = False, details: Optional[Dict[str, Any]] = None):
        """
        Add an optimization to the run record.
        
        Args:
            optimization_type: Type of optimization
            message: Optimization message
            applied: Whether the optimization was applied
            details: Additional optimization details
        """
        optimization = {
            'type': optimization_type,
            'message': message,
            'applied': applied,
            'timestamp': time.time(),
            'details': details or {}
        }
        
        self.optimizations.append(optimization)
    
    def add_tag(self, tag: str):
        """
        Add a tag to the run record.
        
        Args:
            tag: Tag to add
        """
        if tag not in self.tags:
            self.tags.append(tag)
    
    def complete(self, status: str = 'completed'):
        """
        Mark the run as complete.
        
        Args:
            status: Final status ('completed', 'failed', 'interrupted')
        """
        self.end_time = time.time()
        self.duration = self.end_time - self.start_time
        self.status = status
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the run record to a dictionary.
        
        Returns:
            Dictionary representation of the run record
        """
        return {
            'run_id': self.run_id,
            'model_name': self.model_name,
            'dataset_name': self.dataset_name,
            'hardware_info': self.hardware_info,
            'config': self.config,
            'metrics': self.metrics,
            'events': self.events,
            'warnings': self.warnings,
            'optimizations': self.optimizations,
            'start_time': self.start_time,
            'end_time': self.end_time,
            'duration': self.duration,
            'status': self.status,
            'tags': self.tags
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'RunRecord':
        """
        Create a run record from a dictionary.
        
        Args:
            data: Dictionary representation of a run record
            
        Returns:
            RunRecord instance
        """
        run_record = cls(
            run_id=data.get('run_id'),
            model_name=data.get('model_name'),
            dataset_name=data.get('dataset_name'),
            hardware_info=data.get('hardware_info'),
            config=data.get('config')
        )
        
        run_record.metrics = data.get('metrics', {})
        run_record.events = data.get('events', [])
        run_record.warnings = data.get('warnings', [])
        run_record.optimizations = data.get('optimizations', [])
        run_record.start_time = data.get('start_time')
        run_record.end_time = data.get('end_time')
        run_record.duration = data.get('duration')
        run_record.status = data.get('status', 'completed')
        run_record.tags = data.get('tags', [])
        
        return run_record
    
    def get_summary(self) -> Dict[str, Any]:
        """
        Get a summary of the run record.
        
        Returns:
            Summary dictionary
        """
        # Count metrics
        metric_counts = {category: len(metrics) for category, metrics in self.metrics.items() if metrics}
        
        # Count warnings by severity
        warning_counts = {'low': 0, 'medium': 0, 'high': 0, 'critical': 0}
        for warning in self.warnings:
            severity = warning.get('severity', 'medium')
            warning_counts[severity] += 1
        
        # Count optimizations
        optimization_counts = {
            'total': len(self.optimizations),
            'applied': sum(1 for opt in self.optimizations if opt.get('applied', False))
        }
        
        # Get duration
        if self.duration is not None:
            duration_str = f"{self.duration:.2f} seconds"
            if self.duration > 60:
                duration_str = f"{self.duration / 60:.2f} minutes"
            if self.duration > 3600:
                duration_str = f"{self.duration / 3600:.2f} hours"
        else:
            duration_str = "N/A"
        
        # Create summary
        summary = {
            'run_id': self.run_id,
            'model_name': self.model_name,
            'dataset_name': self.dataset_name,
            'status': self.status,
            'duration': duration_str,
            'start_time': datetime.fromtimestamp(self.start_time).strftime('%Y-%m-%d %H:%M:%S') if self.start_time else "N/A",
            'end_time': datetime.fromtimestamp(self.end_time).strftime('%Y-%m-%d %H:%M:%S') if self.end_time else "N/A",
            'metric_counts': metric_counts,
            'warning_counts': warning_counts,
            'optimization_counts': optimization_counts,
            'tags': self.tags
        }
        
        return summary

class MemoryStorage:
    """
    Persistent storage backend for run records.
    
    This class provides a database interface for storing and retrieving
    run records, with support for querying and filtering.
    """
    
    def __init__(self, storage_dir: Optional[str] = None):
        """
        Initialize the memory storage.
        
        Args:
            storage_dir: Directory to store the database and run records
        """
        if storage_dir is None:
            self.storage_dir = os.path.join(os.getcwd(), 'autopd_memory')
        else:
            self.storage_dir = storage_dir
        
        # Create storage directory if it doesn't exist
        os.makedirs(self.storage_dir, exist_ok=True)
        
        # Create runs directory for pickle files
        self.runs_dir = os.path.join(self.storage_dir, 'runs')
        os.makedirs(self.runs_dir, exist_ok=True)
        
        # Initialize database
        self.db_path = os.path.join(self.storage_dir, 'memory.db')
        self._initialize_database()
    
    def _initialize_database(self):
        """Initialize the SQLite database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create runs table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS runs (
            run_id TEXT PRIMARY KEY,
            model_name TEXT,
            dataset_name TEXT,
            start_time REAL,
            end_time REAL,
            duration REAL,
            status TEXT,
            hardware_info TEXT,
            config TEXT,
            tags TEXT
        )
        ''')
        
        # Create tags table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS tags (
            tag TEXT,
            run_id TEXT,
            PRIMARY KEY (tag, run_id),
            FOREIGN KEY (run_id) REFERENCES runs (run_id)
        )
        ''')
        
        conn.commit()
        conn.close()
    
    def save_run(self, run: RunRecord) -> bool:
        """
        Save a run record to storage.
        
        Args:
            run: RunRecord to save
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Save run data to pickle file
            run_path = os.path.join(self.runs_dir, f"{run.run_id}.pkl")
            with open(run_path, 'wb') as f:
                pickle.dump(run, f)
            
            # Save metadata to database
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Convert hardware_info and config to JSON strings
            hardware_info_json = json.dumps(run.hardware_info)
            config_json = json.dumps(run.config)
            tags_json = json.dumps(run.tags)
            
            # Insert or update run in database
            cursor.execute('''
            INSERT OR REPLACE INTO runs 
            (run_id, model_name, dataset_name, start_time, end_time, duration, status, hardware_info, config, tags)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                run.run_id, run.model_name, run.dataset_name, run.start_time, run.end_time, 
                run.duration, run.status, hardware_info_json, config_json, tags_json
            ))
            
            # Delete existing tags for this run
            cursor.execute('DELETE FROM tags WHERE run_id = ?', (run.run_id,))
            
            # Insert tags
            for tag in run.tags:
                cursor.execute('INSERT INTO tags (tag, run_id) VALUES (?, ?)', (tag, run.run_id))
            
            conn.commit()
            conn.close()
            
            logger.info(f"Run {run.run_id} saved to storage")
            return True
        
        except Exception as e:
            logger.error(f"Error saving run {run.run_id}: {e}")
            return False
    
    def load_run(self, run_id: str) -> Optional[RunRecord]:
        """
        Load a run record from storage.
        
        Args:
            run_id: ID of the run to load
            
        Returns:
            RunRecord if found, None otherwise
        """
        run_path = os.path.join(self.runs_dir, f"{run_id}.pkl")
        
        if not os.path.exists(run_path):
            logger.warning(f"Run {run_id} not found in storage")
            return None
        
        try:
            with open(run_path, 'rb') as f:
                run = pickle.load(f)
            
            logger.info(f"Run {run_id} loaded from storage")
            return run
        
        except Exception as e:
            logger.error(f"Error loading run {run_id}: {e}")
            return None
    
    def delete_run(self, run_id: str) -> bool:
        """
        Delete a run record from storage.
        
        Args:
            run_id: ID of the run to delete
            
        Returns:
            True if successful, False otherwise
        """
        run_path = os.path.join(self.runs_dir, f"{run_id}.pkl")
        
        if not os.path.exists(run_path):
            logger.warning(f"Run {run_id} not found in storage")
            return False
        
        try:
            # Delete pickle file
            os.remove(run_path)
            
            # Delete from database
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('DELETE FROM tags WHERE run_id = ?', (run_id,))
            cursor.execute('DELETE FROM runs WHERE run_id = ?', (run_id,))
            
            conn.commit()
            conn.close()
            
            logger.info(f"Run {run_id} deleted from storage")
            return True
        
        except Exception as e:
            logger.error(f"Error deleting run {run_id}: {e}")
            return False
    
    def get_run_ids(self, model_name: Optional[str] = None, 
                   dataset_name: Optional[str] = None, 
                   status: Optional[str] = None,
                   tags: Optional[List[str]] = None) -> List[str]:
        """
        Get run IDs matching the specified criteria.
        
        Args:
            model_name: Filter by model name
            dataset_name: Filter by dataset name
            status: Filter by status
            tags: Filter by tags (all tags must match)
            
        Returns:
            List of matching run IDs
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            query = 'SELECT run_id FROM runs WHERE 1=1'
            params = []
            
            if model_name:
                query += ' AND model_name = ?'
                params.append(model_name)
            
            if dataset_name:
                query += ' AND dataset_name = ?'
                params.append(dataset_name)
            
            if status:
                query += ' AND status = ?'
                params.append(status)
            
            cursor.execute(query, params)
            run_ids = [row[0] for row in cursor.fetchall()]
            
            # Filter by tags if specified
            if tags:
                filtered_run_ids = []
                for run_id in run_ids:
                    cursor.execute('SELECT tag FROM tags WHERE run_id = ?', (run_id,))
                    run_tags = [row[0] for row in cursor.fetchall()]
                    
                    if all(tag in run_tags for tag in tags):
                        filtered_run_ids.append(run_id)
                
                run_ids = filtered_run_ids
            
            conn.close()
            return run_ids
        
        except Exception as e:
            logger.error(f"Error getting run IDs: {e}")
            return []
    
    def get_run_summaries(self, run_ids: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        """
        Get summaries of runs.
        
        Args:
            run_ids: List of run IDs to get summaries for (all runs if None)
            
        Returns:
            List of run summaries
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            if run_ids:
                placeholders = ', '.join(['?'] * len(run_ids))
                cursor.execute(f'SELECT * FROM runs WHERE run_id IN ({placeholders})', run_ids)
            else:
                cursor.execute('SELECT * FROM runs')
            
            columns = [col[0] for col in cursor.description]
            summaries = []
            
            for row in cursor.fetchall():
                summary = dict(zip(columns, row))
                
                # Parse JSON strings
                for key in ['hardware_info', 'config', 'tags']:
                    if key in summary and summary[key]:
                        summary[key] = json.loads(summary[key])
                
                # Format timestamps
                for key in ['start_time', 'end_time']:
                    if key in summary and summary[key]:
                        summary[f"{key}_str"] = datetime.fromtimestamp(summary[key]).strftime('%Y-%m-%d %H:%M:%S')
                
                # Format duration
                if 'duration' in summary and summary['duration']:
                    duration = summary['duration']
                    if duration > 3600:
                        summary['duration_str'] = f"{duration / 3600:.2f} hours"
                    elif duration > 60:
                        summary['duration_str'] = f"{duration / 60:.2f} minutes"
                    else:
                        summary['duration_str'] = f"{duration:.2f} seconds"
                
                summaries.append(summary)
            
            conn.close()
            return summaries
        
        except Exception as e:
            logger.error(f"Error getting run summaries: {e}")
            return []
    
    def export_run(self, run_id: str, export_path: str) -> bool:
        """
        Export a run record to a file.
        
        Args:
            run_id: ID of the run to export
            export_path: Path to export the run to
            
        Returns:
            True if successful, False otherwise
        """
        run = self.load_run(run_id)
        
        if not run:
            return False
        
        try:
            with open(export_path, 'wb') as f:
                pickle.dump(run, f)
            
            logger.info(f"Run {run_id} exported to {export_path}")
            return True
        
        except Exception as e:
            logger.error(f"Error exporting run {run_id}: {e}")
            return False
    
    def import_run(self, import_path: str) -> Optional[str]:
        """
        Import a run record from a file.
        
        Args:
            import_path: Path to import the run from
            
        Returns:
            Run ID if successful, None otherwise
        """
        try:
            with open(import_path, 'rb') as f:
                run = pickle.load(f)
            
            if not isinstance(run, RunRecord):
                logger.error(f"File {import_path} does not contain a valid RunRecord")
                return None
            
            if self.save_run(run):
                logger.info(f"Run {run.run_id} imported from {import_path}")
                return run.run_id
            else:
                return None
        
        except Exception as e:
            logger.error(f"Error importing run from {import_path}: {e}")
            return None

class MemoryAnalyzer:
    """
    Analyzes run records to identify patterns and make predictions.
    
    This class provides methods for analyzing run records to identify
    patterns, similarities, and make predictions based on historical data.
    """
    
    def __init__(self, storage: MemoryStorage):
        """
        Initialize the memory analyzer.
        
        Args:
            storage: MemoryStorage instance
        """
        self.storage = storage
    
    def calculate_similarity(self, run1: RunRecord, run2: RunRecord) -> float:
        """
        Calculate similarity between two runs.
        
        Args:
            run1: First run
            run2: Second run
            
        Returns:
            Similarity score (0.0-1.0)
        """
        # Initialize similarity components
        similarities = []
        
        # Compare model and dataset names
        if run1.model_name and run2.model_name and run1.model_name == run2.model_name:
            similarities.append(1.0)
        else:
            similarities.append(0.0)
        
        if run1.dataset_name and run2.dataset_name and run1.dataset_name == run2.dataset_name:
            similarities.append(1.0)
        else:
            similarities.append(0.0)
        
        # Compare hardware info
        if run1.hardware_info and run2.hardware_info:
            hw_keys = set(run1.hardware_info.keys()) & set(run2.hardware_info.keys())
            if hw_keys:
                hw_similarity = sum(1.0 for k in hw_keys if run1.hardware_info[k] == run2.hardware_info[k]) / len(hw_keys)
                similarities.append(hw_similarity)
        
        # Compare config
        if run1.config and run2.config:
            config_keys = set(run1.config.keys()) & set(run2.config.keys())
            if config_keys:
                config_similarity = sum(1.0 for k in config_keys if run1.config[k] == run2.config[k]) / len(config_keys)
                similarities.append(config_similarity)
        
        # Compare metrics
        for category in set(run1.metrics.keys()) & set(run2.metrics.keys()):
            if run1.metrics[category] and run2.metrics[category]:
                # Compare the last metrics in each category
                last_metrics1 = run1.metrics[category][-1]
                last_metrics2 = run2.metrics[category][-1]
                
                common_keys = set(last_metrics1.keys()) & set(last_metrics2.keys()) - {'timestamp', 'iteration'}
                
                if common_keys:
                    # Calculate normalized difference for each metric
                    metric_diffs = []
                    
                    for key in common_keys:
                        val1 = last_metrics1[key]
                        val2 = last_metrics2[key]
                        
                        if isinstance(val1, (int, float)) and isinstance(val2, (int, float)):
                            # Normalize the difference
                            max_val = max(abs(val1), abs(val2))
                            if max_val > 0:
                                diff = 1.0 - min(abs(val1 - val2) / max_val, 1.0)
                            else:
                                diff = 1.0
                            
                            metric_diffs.append(diff)
                    
                    if metric_diffs:
                        similarities.append(sum(metric_diffs) / len(metric_diffs))
        
        # Compare tags
        if run1.tags and run2.tags:
            tag_similarity = len(set(run1.tags) & set(run2.tags)) / len(set(run1.tags) | set(run2.tags))
            similarities.append(tag_similarity)
        
        # Calculate overall similarity
        if similarities:
            return sum(similarities) / len(similarities)
        else:
            return 0.0
    
    def find_similar_runs(self, run: RunRecord, min_similarity: float = 0.7, 
                         max_results: int = 5) -> List[Tuple[str, float]]:
        """
        Find runs similar to the given run.
        
        Args:
            run: Run to find similar runs for
            min_similarity: Minimum similarity score
            max_results: Maximum number of results
            
        Returns:
            List of (run_id, similarity) tuples
        """
        # Get all run IDs
        run_ids = self.storage.get_run_ids()
        
        # Calculate similarity for each run
        similarities = []
        
        for run_id in run_ids:
            if run_id == run.run_id:
                continue
            
            other_run = self.storage.load_run(run_id)
            
            if other_run:
                similarity = self.calculate_similarity(run, other_run)
                
                if similarity >= min_similarity:
                    similarities.append((run_id, similarity))
        
        # Sort by similarity (descending) and limit results
        similarities.sort(key=lambda x: x[1], reverse=True)
        return similarities[:max_results]
    
    def cluster_runs(self, run_ids: Optional[List[str]] = None, 
                    n_clusters: int = 3) -> Dict[int, List[str]]:
        """
        Cluster runs based on similarity.
        
        Args:
            run_ids: List of run IDs to cluster (all runs if None)
            n_clusters: Number of clusters
            
        Returns:
            Dictionary mapping cluster IDs to lists of run IDs
        """
        try:
            # Get run IDs if not provided
            if run_ids is None:
                run_ids = self.storage.get_run_ids()
            
            if len(run_ids) < n_clusters:
                n_clusters = len(run_ids)
            
            if n_clusters <= 1:
                return {0: run_ids}
            
            # Load runs
            runs = [self.storage.load_run(run_id) for run_id in run_ids]
            runs = [run for run in runs if run is not None]
            
            if not runs:
                return {}
            
            # Calculate similarity matrix
            n_runs = len(runs)
            similarity_matrix = np.zeros((n_runs, n_runs))
            
            for i in range(n_runs):
                for j in range(i, n_runs):
                    similarity = self.calculate_similarity(runs[i], runs[j])
                    similarity_matrix[i, j] = similarity
                    similarity_matrix[j, i] = similarity
            
            # Convert to distance matrix (1 - similarity)
            distance_matrix = 1.0 - similarity_matrix
            
            # Perform clustering
            from sklearn.cluster import AgglomerativeClustering
            
            clustering = AgglomerativeClustering(
                n_clusters=n_clusters,
                affinity='precomputed',
                linkage='average'
            )
            
            cluster_labels = clustering.fit_predict(distance_matrix)
            
            # Group run IDs by cluster
            clusters = {}
            for i, cluster_id in enumerate(cluster_labels):
                if cluster_id not in clusters:
                    clusters[cluster_id] = []
                
                clusters[cluster_id].append(runs[i].run_id)
            
            return clusters
        
        except Exception as e:
            logger.error(f"Error clustering runs: {e}")
            return {0: run_ids}
    
    def detect_patterns(self, run_ids: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        """
        Detect patterns in run records.
        
        Args:
            run_ids: List of run IDs to analyze (all runs if None)
            
        Returns:
            List of detected patterns
        """
        # Get run IDs if not provided
        if run_ids is None:
            run_ids = self.storage.get_run_ids()
        
        # Load runs
        runs = [self.storage.load_run(run_id) for run_id in run_ids]
        runs = [run for run in runs if run is not None]
        
        if not runs:
            return []
        
        patterns = []
        
        # Analyze warning patterns
        warning_types = {}
        for run in runs:
            for warning in run.warnings:
                warning_type = warning.get('type', 'unknown')
                if warning_type not in warning_types:
                    warning_types[warning_type] = []
                
                warning_types[warning_type].append(run.run_id)
        
        for warning_type, affected_runs in warning_types.items():
            if len(affected_runs) >= 2:
                pattern = {
                    'type': 'warning_pattern',
                    'warning_type': warning_type,
                    'affected_runs': affected_runs,
                    'frequency': len(affected_runs) / len(runs)
                }
                
                patterns.append(pattern)
        
        # Analyze optimization patterns
        optimization_types = {}
        for run in runs:
            for optimization in run.optimizations:
                optimization_type = optimization.get('type', 'unknown')
                if optimization_type not in optimization_types:
                    optimization_types[optimization_type] = []
                
                optimization_types[optimization_type].append(run.run_id)
        
        for optimization_type, affected_runs in optimization_types.items():
            if len(affected_runs) >= 2:
                pattern = {
                    'type': 'optimization_pattern',
                    'optimization_type': optimization_type,
                    'affected_runs': affected_runs,
                    'frequency': len(affected_runs) / len(runs)
                }
                
                patterns.append(pattern)
        
        # Analyze performance patterns
        if all(run.duration is not None for run in runs):
            durations = [run.duration for run in runs]
            avg_duration = sum(durations) / len(durations)
            
            fast_runs = [run.run_id for run in runs if run.duration < avg_duration * 0.8]
            slow_runs = [run.run_id for run in runs if run.duration > avg_duration * 1.2]
            
            if fast_runs:
                pattern = {
                    'type': 'performance_pattern',
                    'pattern_type': 'fast_runs',
                    'affected_runs': fast_runs,
                    'frequency': len(fast_runs) / len(runs),
                    'avg_duration': sum(run.duration for run in runs if run.run_id in fast_runs) / len(fast_runs)
                }
                
                patterns.append(pattern)
            
            if slow_runs:
                pattern = {
                    'type': 'performance_pattern',
                    'pattern_type': 'slow_runs',
                    'affected_runs': slow_runs,
                    'frequency': len(slow_runs) / len(runs),
                    'avg_duration': sum(run.duration for run in runs if run.run_id in slow_runs) / len(slow_runs)
                }
                
                patterns.append(pattern)
        
        return patterns
    
    def predict_failures(self, run: RunRecord) -> List[Dict[str, Any]]:
        """
        Predict potential failures for a run.
        
        Args:
            run: Run to predict failures for
            
        Returns:
            List of predicted failures
        """
        # Find similar runs
        similar_runs = self.find_similar_runs(run, min_similarity=0.6)
        
        if not similar_runs:
            return []
        
        # Load similar runs
        similar_run_objects = [self.storage.load_run(run_id) for run_id, _ in similar_runs]
        similar_run_objects = [r for r in similar_run_objects if r is not None]
        
        if not similar_run_objects:
            return []
        
        predictions = []
        
        # Check for failed runs
        failed_runs = [r for r in similar_run_objects if r.status == 'failed']
        
        if failed_runs:
            # Group by warning types
            warning_types = {}
            
            for failed_run in failed_runs:
                for warning in failed_run.warnings:
                    warning_type = warning.get('type', 'unknown')
                    if warning_type not in warning_types:
                        warning_types[warning_type] = []
                    
                    warning_types[warning_type].append(failed_run.run_id)
            
            # Predict failures based on warning patterns
            for warning_type, affected_runs in warning_types.items():
                if len(affected_runs) >= 2:
                    prediction = {
                        'type': 'failure_prediction',
                        'warning_type': warning_type,
                        'similar_failed_runs': affected_runs,
                        'confidence': len(affected_runs) / len(failed_runs),
                        'details': f"Similar runs failed with warning type: {warning_type}"
                    }
                    
                    predictions.append(prediction)
        
        # Check for memory-related warnings in similar runs
        memory_warnings = []
        
        for similar_run in similar_run_objects:
            for warning in similar_run.warnings:
                if 'memory' in warning.get('type', '').lower() or 'oom' in warning.get('type', '').lower():
                    memory_warnings.append(warning)
        
        if memory_warnings:
            prediction = {
                'type': 'failure_prediction',
                'warning_type': 'memory_issue',
                'similar_runs_with_warning': len(memory_warnings),
                'confidence': len(memory_warnings) / len(similar_run_objects),
                'details': f"Similar runs had memory-related warnings"
            }
            
            predictions.append(prediction)
        
        return predictions
    
    def recommend_optimizations(self, run: RunRecord) -> List[Dict[str, Any]]:
        """
        Recommend optimizations based on similar runs.
        
        Args:
            run: Run to recommend optimizations for
            
        Returns:
            List of recommended optimizations
        """
        # Find similar runs
        similar_runs = self.find_similar_runs(run, min_similarity=0.6)
        
        if not similar_runs:
            return []
        
        # Load similar runs
        similar_run_objects = [self.storage.load_run(run_id) for run_id, _ in similar_runs]
        similar_run_objects = [r for r in similar_run_objects if r is not None]
        
        if not similar_run_objects:
            return []
        
        # Get optimizations from similar runs
        all_optimizations = []
        
        for similar_run in similar_run_objects:
            for optimization in similar_run.optimizations:
                if optimization.get('applied', False):
                    all_optimizations.append(optimization)
        
        if not all_optimizations:
            return []
        
        # Group optimizations by type
        optimization_types = {}
        
        for optimization in all_optimizations:
            optimization_type = optimization.get('type', 'unknown')
            if optimization_type not in optimization_types:
                optimization_types[optimization_type] = []
            
            optimization_types[optimization_type].append(optimization)
        
        # Generate recommendations
        recommendations = []
        
        for optimization_type, optimizations in optimization_types.items():
            if len(optimizations) >= 2:
                # Check if this optimization is already applied in the current run
                already_applied = False
                
                for opt in run.optimizations:
                    if opt.get('type') == optimization_type and opt.get('applied', False):
                        already_applied = True
                        break
                
                if not already_applied:
                    # Get a representative optimization
                    representative = optimizations[0]
                    
                    recommendation = {
                        'type': 'optimization_recommendation',
                        'optimization_type': optimization_type,
                        'message': representative.get('message', ''),
                        'details': representative.get('details', {}),
                        'confidence': len(optimizations) / len(similar_run_objects),
                        'similar_runs_count': len(optimizations)
                    }
                    
                    recommendations.append(recommendation)
        
        # Sort by confidence
        recommendations.sort(key=lambda x: x['confidence'], reverse=True)
        
        return recommendations

class ExperienceBrain:
    """
    High-level interface for learning from experience.
    
    This class provides a high-level interface for learning from past
    training runs and making intelligent recommendations based on
    historical patterns.
    """
    
    def __init__(self, storage_dir: Optional[str] = None):
        """
        Initialize the experience brain.
        
        Args:
            storage_dir: Directory to store run records
        """
        self.storage = MemoryStorage(storage_dir)
        self.analyzer = MemoryAnalyzer(self.storage)
        self.current_run = None
    
    def start_run(self, model_name: Optional[str] = None, 
                dataset_name: Optional[str] = None,
                hardware_info: Optional[Dict[str, Any]] = None,
                config: Optional[Dict[str, Any]] = None) -> str:
        """
        Start a new run.
        
        Args:
            model_name: Name of the model
            dataset_name: Name of the dataset
            hardware_info: Hardware configuration information
            config: Training configuration
            
        Returns:
            Run ID
        """
        self.current_run = RunRecord(
            model_name=model_name,
            dataset_name=dataset_name,
            hardware_info=hardware_info,
            config=config
        )
        
        logger.info(f"Started new run: {self.current_run.run_id}")
        return self.current_run.run_id
    
    def add_metrics(self, category: str, metrics: Dict[str, Any]):
        """
        Add metrics to the current run.
        
        Args:
            category: Category of metrics
            metrics: Dictionary of metrics
        """
        if self.current_run:
            self.current_run.add_metrics(category, metrics)
        else:
            logger.warning("No active run. Start a run before adding metrics.")
    
    def add_warning(self, warning_type: str, message: str, severity: str = 'medium', 
                   details: Optional[Dict[str, Any]] = None):
        """
        Add a warning to the current run.
        
        Args:
            warning_type: Type of warning
            message: Warning message
            severity: Warning severity
            details: Additional warning details
        """
        if self.current_run:
            self.current_run.add_warning(warning_type, message, severity, details)
        else:
            logger.warning("No active run. Start a run before adding warnings.")
    
    def add_optimization(self, optimization_type: str, message: str, 
                        applied: bool = False, details: Optional[Dict[str, Any]] = None):
        """
        Add an optimization to the current run.
        
        Args:
            optimization_type: Type of optimization
            message: Optimization message
            applied: Whether the optimization was applied
            details: Additional optimization details
        """
        if self.current_run:
            self.current_run.add_optimization(optimization_type, message, applied, details)
        else:
            logger.warning("No active run. Start a run before adding optimizations.")
    
    def add_tag(self, tag: str):
        """
        Add a tag to the current run.
        
        Args:
            tag: Tag to add
        """
        if self.current_run:
            self.current_run.add_tag(tag)
        else:
            logger.warning("No active run. Start a run before adding tags.")
    
    def complete_run(self, status: str = 'completed'):
        """
        Complete the current run.
        
        Args:
            status: Final status
        """
        if self.current_run:
            self.current_run.complete(status)
            self.storage.save_run(self.current_run)
            logger.info(f"Completed run: {self.current_run.run_id}")
            self.current_run = None
        else:
            logger.warning("No active run to complete.")
    
    def get_similar_runs(self, min_similarity: float = 0.7, 
                        max_results: int = 5) -> List[Dict[str, Any]]:
        """
        Get runs similar to the current run.
        
        Args:
            min_similarity: Minimum similarity score
            max_results: Maximum number of results
            
        Returns:
            List of similar run summaries
        """
        if not self.current_run:
            logger.warning("No active run. Start a run before getting similar runs.")
            return []
        
        similar_runs = self.analyzer.find_similar_runs(
            self.current_run, min_similarity, max_results
        )
        
        if not similar_runs:
            return []
        
        # Get summaries for similar runs
        run_ids = [run_id for run_id, _ in similar_runs]
        summaries = self.storage.get_run_summaries(run_ids)
        
        # Add similarity scores
        for summary in summaries:
            for run_id, similarity in similar_runs:
                if summary['run_id'] == run_id:
                    summary['similarity'] = similarity
                    break
        
        # Sort by similarity
        summaries.sort(key=lambda x: x.get('similarity', 0), reverse=True)
        
        return summaries
    
    def predict_failures(self) -> List[Dict[str, Any]]:
        """
        Predict potential failures for the current run.
        
        Returns:
            List of predicted failures
        """
        if not self.current_run:
            logger.warning("No active run. Start a run before predicting failures.")
            return []
        
        return self.analyzer.predict_failures(self.current_run)
    
    def recommend_optimizations(self) -> List[Dict[str, Any]]:
        """
        Recommend optimizations for the current run.
        
        Returns:
            List of recommended optimizations
        """
        if not self.current_run:
            logger.warning("No active run. Start a run before recommending optimizations.")
            return []
        
        return self.analyzer.recommend_optimizations(self.current_run)
    
    def get_run_history(self, model_name: Optional[str] = None, 
                       dataset_name: Optional[str] = None,
                       tags: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        """
        Get history of runs matching the specified criteria.
        
        Args:
            model_name: Filter by model name
            dataset_name: Filter by dataset name
            tags: Filter by tags
            
        Returns:
            List of run summaries
        """
        run_ids = self.storage.get_run_ids(model_name, dataset_name, tags=tags)
        return self.storage.get_run_summaries(run_ids)
    
    def get_run_details(self, run_id: str) -> Optional[Dict[str, Any]]:
        """
        Get detailed information about a run.
        
        Args:
            run_id: ID of the run
            
        Returns:
            Dictionary with run details
        """
        run = self.storage.load_run(run_id)
        
        if not run:
            return None
        
        # Convert to dictionary and add summary
        details = run.to_dict()
        details['summary'] = run.get_summary()
        
        return details
    
    def delete_run(self, run_id: str) -> bool:
        """
        Delete a run from storage.
        
        Args:
            run_id: ID of the run to delete
            
        Returns:
            True if successful, False otherwise
        """
        return self.storage.delete_run(run_id)
    
    def export_run(self, run_id: str, export_path: str) -> bool:
        """
        Export a run to a file.
        
        Args:
            run_id: ID of the run to export
            export_path: Path to export the run to
            
        Returns:
            True if successful, False otherwise
        """
        return self.storage.export_run(run_id, export_path)
    
    def import_run(self, import_path: str) -> Optional[str]:
        """
        Import a run from a file.
        
        Args:
            import_path: Path to import the run from
            
        Returns:
            Run ID if successful, None otherwise
        """
        return self.storage.import_run(import_path)
    
    def get_patterns(self) -> List[Dict[str, Any]]:
        """
        Get patterns from all runs.
        
        Returns:
            List of detected patterns
        """
        return self.analyzer.detect_patterns()
    
    def cluster_runs(self, n_clusters: int = 3) -> Dict[int, List[Dict[str, Any]]]:
        """
        Cluster all runs.
        
        Args:
            n_clusters: Number of clusters
            
        Returns:
            Dictionary mapping cluster IDs to lists of run summaries
        """
        clusters = self.analyzer.cluster_runs(n_clusters=n_clusters)
        
        # Convert to summaries
        cluster_summaries = {}
        
        for cluster_id, run_ids in clusters.items():
            cluster_summaries[cluster_id] = self.storage.get_run_summaries(run_ids)
        
        return cluster_summaries
