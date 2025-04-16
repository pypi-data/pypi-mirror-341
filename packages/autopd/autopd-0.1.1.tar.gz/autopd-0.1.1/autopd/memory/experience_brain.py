"""
Historical memory system module for AutoPipelineDoctor.

This module provides functionality to store, retrieve, and analyze historical
training runs to provide better recommendations based on past experiences.
"""

import logging
import os
import json
import time
import sqlite3
import pickle
import hashlib
from typing import Dict, Any, Optional, List, Tuple, Union, Callable
from datetime import datetime
import tempfile
from pathlib import Path
import shutil
import re

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

logger = logging.getLogger(__name__)


class RunRecord:
    """
    Record of a single training run.
    
    This class represents a record of a single training run, including
    metrics, warnings, optimizations, and other information.
    
    Attributes:
        run_id: Unique identifier for the run
        model_info: Information about the model
        dataset_info: Information about the dataset
        hardware_info: Information about the hardware
        metrics: Dictionary of metrics collected during the run
        warnings: List of warnings generated during the run
        optimizations: List of optimizations applied during the run
        start_time: Start time of the run
        end_time: End time of the run
        status: Status of the run (e.g., "completed", "failed")
        metadata: Additional metadata about the run
    """
    
    def __init__(
        self,
        run_id: Optional[str] = None,
        model_info: Optional[Dict[str, Any]] = None,
        dataset_info: Optional[Dict[str, Any]] = None,
        hardware_info: Optional[Dict[str, Any]] = None,
        metrics: Optional[Dict[str, Any]] = None,
        warnings: Optional[List[Dict[str, Any]]] = None,
        optimizations: Optional[List[Dict[str, Any]]] = None,
        start_time: Optional[float] = None,
        end_time: Optional[float] = None,
        status: str = "running",
        metadata: Optional[Dict[str, Any]] = None,
    ):
        """
        Initialize a run record.
        
        Args:
            run_id: Unique identifier for the run
            model_info: Information about the model
            dataset_info: Information about the dataset
            hardware_info: Information about the hardware
            metrics: Dictionary of metrics collected during the run
            warnings: List of warnings generated during the run
            optimizations: List of optimizations applied during the run
            start_time: Start time of the run
            end_time: End time of the run
            status: Status of the run (e.g., "completed", "failed")
            metadata: Additional metadata about the run
        """
        self.run_id = run_id or self._generate_run_id()
        self.model_info = model_info or {}
        self.dataset_info = dataset_info or {}
        self.hardware_info = hardware_info or {}
        self.metrics = metrics or {}
        self.warnings = warnings or []
        self.optimizations = optimizations or []
        self.start_time = start_time or time.time()
        self.end_time = end_time
        self.status = status
        self.metadata = metadata or {}
    
    def _generate_run_id(self) -> str:
        """
        Generate a unique run ID.
        
        Returns:
            Unique run ID
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        random_suffix = hashlib.md5(str(time.time()).encode()).hexdigest()[:8]
        return f"run_{timestamp}_{random_suffix}"
    
    def update_metrics(self, metrics: Dict[str, Any], category: str = "general"):
        """
        Update metrics for the run.
        
        Args:
            metrics: Dictionary of metrics to update
            category: Category of metrics
        """
        if category not in self.metrics:
            self.metrics[category] = []
        
        # Add timestamp to metrics
        metrics_with_time = metrics.copy()
        metrics_with_time["timestamp"] = time.time()
        
        # Append to metrics
        self.metrics[category].append(metrics_with_time)
    
    def add_warning(self, warning: Dict[str, Any]):
        """
        Add a warning to the run.
        
        Args:
            warning: Warning dictionary
        """
        # Add timestamp to warning
        warning_with_time = warning.copy()
        warning_with_time["timestamp"] = time.time()
        
        # Append to warnings
        self.warnings.append(warning_with_time)
    
    def add_optimization(self, optimization: Dict[str, Any]):
        """
        Add an optimization to the run.
        
        Args:
            optimization: Optimization dictionary
        """
        # Add timestamp to optimization
        optimization_with_time = optimization.copy()
        optimization_with_time["timestamp"] = time.time()
        
        # Append to optimizations
        self.optimizations.append(optimization_with_time)
    
    def complete(self, status: str = "completed"):
        """
        Mark the run as completed.
        
        Args:
            status: Status of the run (e.g., "completed", "failed")
        """
        self.end_time = time.time()
        self.status = status
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the run record to a dictionary.
        
        Returns:
            Dictionary representation of the run record
        """
        return {
            "run_id": self.run_id,
            "model_info": self.model_info,
            "dataset_info": self.dataset_info,
            "hardware_info": self.hardware_info,
            "metrics": self.metrics,
            "warnings": self.warnings,
            "optimizations": self.optimizations,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "status": self.status,
            "metadata": self.metadata,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "RunRecord":
        """
        Create a run record from a dictionary.
        
        Args:
            data: Dictionary representation of a run record
        
        Returns:
            RunRecord instance
        """
        return cls(
            run_id=data.get("run_id"),
            model_info=data.get("model_info"),
            dataset_info=data.get("dataset_info"),
            hardware_info=data.get("hardware_info"),
            metrics=data.get("metrics"),
            warnings=data.get("warnings"),
            optimizations=data.get("optimizations"),
            start_time=data.get("start_time"),
            end_time=data.get("end_time"),
            status=data.get("status", "completed"),
            metadata=data.get("metadata"),
        )
    
    def __repr__(self) -> str:
        """String representation of the run record."""
        duration = (self.end_time or time.time()) - self.start_time
        return f"RunRecord(id={self.run_id}, status={self.status}, duration={duration:.2f}s)"


class MemoryStorage:
    """
    Storage backend for historical run records.
    
    This class provides functionality to store and retrieve run records
    from a persistent storage backend.
    
    Attributes:
        storage_dir: Directory to store run records
        db_path: Path to the SQLite database
        connection: SQLite database connection
    """
    
    def __init__(self, storage_dir: Optional[str] = None):
        """
        Initialize the memory storage.
        
        Args:
            storage_dir: Directory to store run records
        """
        self.storage_dir = storage_dir or os.path.join(os.path.expanduser("~"), ".autopd", "memory")
        os.makedirs(self.storage_dir, exist_ok=True)
        
        # Initialize SQLite database
        self.db_path = os.path.join(self.storage_dir, "runs.db")
        self.connection = self._initialize_database()
        
        logger.info(f"Memory storage initialized with storage directory: {self.storage_dir}")
    
    def _initialize_database(self) -> sqlite3.Connection:
        """
        Initialize the SQLite database.
        
        Returns:
            SQLite database connection
        """
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        
        # Create runs table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS runs (
            run_id TEXT PRIMARY KEY,
            model_name TEXT,
            dataset_name TEXT,
            hardware_name TEXT,
            start_time REAL,
            end_time REAL,
            status TEXT,
            data_path TEXT,
            created_at REAL
        )
        """)
        
        # Create model_info table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS model_info (
            model_name TEXT PRIMARY KEY,
            architecture TEXT,
            num_parameters INTEGER,
            data TEXT,
            created_at REAL
        )
        """)
        
        # Create dataset_info table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS dataset_info (
            dataset_name TEXT PRIMARY KEY,
            num_samples INTEGER,
            num_classes INTEGER,
            data TEXT,
            created_at REAL
        )
        """)
        
        # Create hardware_info table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS hardware_info (
            hardware_name TEXT PRIMARY KEY,
            gpu_name TEXT,
            cpu_name TEXT,
            data TEXT,
            created_at REAL
        )
        """)
        
        # Create tags table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS tags (
            run_id TEXT,
            tag TEXT,
            created_at REAL,
            PRIMARY KEY (run_id, tag),
            FOREIGN KEY (run_id) REFERENCES runs (run_id)
        )
        """)
        
        connection.commit()
        return connection
    
    def save_run(self, run: RunRecord) -> bool:
        """
        Save a run record to storage.
        
        Args:
            run: Run record to save
        
        Returns:
            True if successful, False otherwise
        """
        try:
            cursor = self.connection.cursor()
            
            # Save model info
            model_name = run.model_info.get("name", "unknown_model")
            cursor.execute(
                """
                INSERT OR REPLACE INTO model_info
                (model_name, architecture, num_parameters, data, created_at)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    model_name,
                    run.model_info.get("architecture", "unknown"),
                    run.model_info.get("num_parameters", 0),
                    json.dumps(run.model_info),
                    time.time(),
                ),
            )
            
            # Save dataset info
            dataset_name = run.dataset_info.get("name", "unknown_dataset")
            cursor.execute(
                """
                INSERT OR REPLACE INTO dataset_info
                (dataset_name, num_samples, num_classes, data, created_at)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    dataset_name,
                    run.dataset_info.get("num_samples", 0),
                    run.dataset_info.get("num_classes", 0),
                    json.dumps(run.dataset_info),
                    time.time(),
                ),
            )
            
            # Save hardware info
            hardware_name = run.hardware_info.get("name", "unknown_hardware")
            cursor.execute(
                """
                INSERT OR REPLACE INTO hardware_info
                (hardware_name, gpu_name, cpu_name, data, created_at)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    hardware_name,
                    run.hardware_info.get("gpu_name", "unknown"),
                    run.hardware_info.get("cpu_name", "unknown"),
                    json.dumps(run.hardware_info),
                    time.time(),
                ),
            )
            
            # Save run data to file
            data_path = os.path.join(self.storage_dir, f"{run.run_id}.pickle")
            with open(data_path, "wb") as f:
                pickle.dump(run.to_dict(), f)
            
            # Save run metadata to database
            cursor.execute(
                """
                INSERT OR REPLACE INTO runs
                (run_id, model_name, dataset_name, hardware_name, start_time, end_time, status, data_path, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    run.run_id,
                    model_name,
                    dataset_name,
                    hardware_name,
                    run.start_time,
                    run.end_time,
                    run.status,
                    data_path,
                    time.time(),
                ),
            )
            
            # Save tags
            for tag in run.metadata.get("tags", []):
                cursor.execute(
                    """
                    INSERT OR REPLACE INTO tags
                    (run_id, tag, created_at)
                    VALUES (?, ?, ?)
                    """,
                    (run.run_id, tag, time.time()),
                )
            
            self.connection.commit()
            logger.info(f"Saved run record: {run.run_id}")
            return True
        
        except Exception as e:
            logger.error(f"Failed to save run record: {e}")
            return False
    
    def load_run(self, run_id: str) -> Optional[RunRecord]:
        """
        Load a run record from storage.
        
        Args:
            run_id: ID of the run to load
        
        Returns:
            RunRecord instance or None if not found
        """
        try:
            cursor = self.connection.cursor()
            
            # Get run metadata from database
            cursor.execute(
                """
                SELECT data_path FROM runs
                WHERE run_id = ?
                """,
                (run_id,),
            )
            
            result = cursor.fetchone()
            if not result:
                logger.warning(f"Run record not found: {run_id}")
                return None
            
            data_path = result[0]
            
            # Load run data from file
            with open(data_path, "rb") as f:
                data = pickle.load(f)
            
            # Create RunRecord instance
            run = RunRecord.from_dict(data)
            
            # Load tags
            cursor.execute(
                """
                SELECT tag FROM tags
                WHERE run_id = ?
                """,
                (run_id,),
            )
            
            tags = [row[0] for row in cursor.fetchall()]
            if tags:
                if "tags" not in run.metadata:
                    run.metadata["tags"] = []
                run.metadata["tags"].extend(tags)
            
            return run
        
        except Exception as e:
            logger.error(f"Failed to load run record: {e}")
            return None
    
    def delete_run(self, run_id: str) -> bool:
        """
        Delete a run record from storage.
        
        Args:
            run_id: ID of the run to delete
        
        Returns:
            True if successful, False otherwise
        """
        try:
            cursor = self.connection.cursor()
            
            # Get run metadata from database
            cursor.execute(
                """
                SELECT data_path FROM runs
                WHERE run_id = ?
                """,
                (run_id,),
            )
            
            result = cursor.fetchone()
            if not result:
                logger.warning(f"Run record not found: {run_id}")
                return False
            
            data_path = result[0]
            
            # Delete run data file
            if os.path.exists(data_path):
                os.remove(data_path)
            
            # Delete run metadata from database
            cursor.execute(
                """
                DELETE FROM runs
                WHERE run_id = ?
                """,
                (run_id,),
            )
            
            # Delete tags
            cursor.execute(
                """
                DELETE FROM tags
                WHERE run_id = ?
                """,
                (run_id,),
            )
            
            self.connection.commit()
            logger.info(f"Deleted run record: {run_id}")
            return True
        
        except Exception as e:
            logger.error(f"Failed to delete run record: {e}")
            return False
    
    def list_runs(
        self,
        model_name: Optional[str] = None,
        dataset_name: Optional[str] = None,
        hardware_name: Optional[str] = None,
        status: Optional[str] = None,
        tags: Optional[List[str]] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> List[Dict[str, Any]]:
        """
        List run records matching the given criteria.
        
        Args:
            model_name: Filter by model name
            dataset_name: Filter by dataset name
            hardware_name: Filter by hardware name
            status: Filter by status
            tags: Filter by tags (all tags must match)
            limit: Maximum number of records to return
            offset: Offset for pagination
        
        Returns:
            List of run record metadata
        """
        try:
            cursor = self.connection.cursor()
            
            # Build query
            query = """
            SELECT r.run_id, r.model_name, r.dataset_name, r.hardware_name, r.start_time, r.end_time, r.status
            FROM runs r
            """
            
            # Add tag join if needed
            if tags:
                query += f"""
                INNER JOIN (
                    SELECT run_id
                    FROM tags
                    WHERE tag IN ({','.join(['?'] * len(tags))})
                    GROUP BY run_id
                    HAVING COUNT(DISTINCT tag) = {len(tags)}
                ) t ON r.run_id = t.run_id
                """
            
            # Add filters
            conditions = []
            params = []
            
            if model_name:
                conditions.append("r.model_name = ?")
                params.append(model_name)
            
            if dataset_name:
                conditions.append("r.dataset_name = ?")
                params.append(dataset_name)
            
            if hardware_name:
                conditions.append("r.hardware_name = ?")
                params.append(hardware_name)
            
            if status:
                conditions.append("r.status = ?")
                params.append(status)
            
            if conditions:
                query += " WHERE " + " AND ".join(conditions)
            
            # Add tag parameters
            if tags:
                params.extend(tags)
            
            # Add order by, limit, and offset
            query += """
            ORDER BY r.start_time DESC
            LIMIT ? OFFSET ?
            """
            
            params.extend([limit, offset])
            
            # Execute query
            cursor.execute(query, params)
            
            # Fetch results
            results = []
            for row in cursor.fetchall():
                run_id, model_name, dataset_name, hardware_name, start_time, end_time, status = row
                
                # Get tags for this run
                cursor.execute(
                    """
                    SELECT tag FROM tags
                    WHERE run_id = ?
                    """,
                    (run_id,),
                )
                
                run_tags = [row[0] for row in cursor.fetchall()]
                
                results.append({
                    "run_id": run_id,
                    "model_name": model_name,
                    "dataset_name": dataset_name,
                    "hardware_name": hardware_name,
                    "start_time": start_time,
                    "end_time": end_time,
                    "status": status,
                    "tags": run_tags,
                })
            
            return results
        
        except Exception as e:
            logger.error(f"Failed to list run records: {e}")
            return []
    
    def add_tag(self, run_id: str, tag: str) -> bool:
        """
        Add a tag to a run record.
        
        Args:
            run_id: ID of the run to tag
            tag: Tag to add
        
        Returns:
            True if successful, False otherwise
        """
        try:
            cursor = self.connection.cursor()
            
            # Check if run exists
            cursor.execute(
                """
                SELECT run_id FROM runs
                WHERE run_id = ?
                """,
                (run_id,),
            )
            
            if not cursor.fetchone():
                logger.warning(f"Run record not found: {run_id}")
                return False
            
            # Add tag
            cursor.execute(
                """
                INSERT OR REPLACE INTO tags
                (run_id, tag, created_at)
                VALUES (?, ?, ?)
                """,
                (run_id, tag, time.time()),
            )
            
            self.connection.commit()
            logger.info(f"Added tag '{tag}' to run record: {run_id}")
            return True
        
        except Exception as e:
            logger.error(f"Failed to add tag: {e}")
            return False
    
    def remove_tag(self, run_id: str, tag: str) -> bool:
        """
        Remove a tag from a run record.
        
        Args:
            run_id: ID of the run to untag
            tag: Tag to remove
        
        Returns:
            True if successful, False otherwise
        """
        try:
            cursor = self.connection.cursor()
            
            # Remove tag
            cursor.execute(
                """
                DELETE FROM tags
                WHERE run_id = ? AND tag = ?
                """,
                (run_id, tag),
            )
            
            self.connection.commit()
            logger.info(f"Removed tag '{tag}' from run record: {run_id}")
            return True
        
        except Exception as e:
            logger.error(f"Failed to remove tag: {e}")
            return False
    
    def get_tags(self, run_id: str) -> List[str]:
        """
        Get tags for a run record.
        
        Args:
            run_id: ID of the run
        
        Returns:
            List of tags
        """
        try:
            cursor = self.connection.cursor()
            
            # Get tags
            cursor.execute(
                """
                SELECT tag FROM tags
                WHERE run_id = ?
                """,
                (run_id,),
            )
            
            return [row[0] for row in cursor.fetchall()]
        
        except Exception as e:
            logger.error(f"Failed to get tags: {e}")
            return []
    
    def export_runs(
        self,
        output_dir: str,
        run_ids: Optional[List[str]] = None,
    ) -> bool:
        """
        Export run records to a directory.
        
        Args:
            output_dir: Directory to export to
            run_ids: List of run IDs to export (all if None)
        
        Returns:
            True if successful, False otherwise
        """
        try:
            os.makedirs(output_dir, exist_ok=True)
            
            cursor = self.connection.cursor()
            
            # Get run IDs to export
            if run_ids is None:
                cursor.execute("SELECT run_id FROM runs")
                run_ids = [row[0] for row in cursor.fetchall()]
            
            # Export each run
            for run_id in run_ids:
                run = self.load_run(run_id)
                if run:
                    output_path = os.path.join(output_dir, f"{run_id}.json")
                    with open(output_path, "w") as f:
                        json.dump(run.to_dict(), f, indent=2)
            
            logger.info(f"Exported {len(run_ids)} run records to {output_dir}")
            return True
        
        except Exception as e:
            logger.error(f"Failed to export run records: {e}")
            return False
    
    def import_runs(self, input_dir: str) -> int:
        """
        Import run records from a directory.
        
        Args:
            input_dir: Directory to import from
        
        Returns:
            Number of imported run records
        """
        try:
            if not os.path.isdir(input_dir):
                logger.error(f"Input directory not found: {input_dir}")
                return 0
            
            # Find JSON files
            json_files = [f for f in os.listdir(input_dir) if f.endswith(".json")]
            
            # Import each run
            imported_count = 0
            for json_file in json_files:
                try:
                    input_path = os.path.join(input_dir, json_file)
                    with open(input_path, "r") as f:
                        data = json.load(f)
                    
                    run = RunRecord.from_dict(data)
                    if self.save_run(run):
                        imported_count += 1
                
                except Exception as e:
                    logger.error(f"Failed to import run record from {json_file}: {e}")
            
            logger.info(f"Imported {imported_count} run records from {input_dir}")
            return imported_count
        
        except Exception as e:
            logger.error(f"Failed to import run records: {e}")
            return 0
    
    def close(self):
        """Close the database connection."""
        if self.connection:
            self.connection.close()
            logger.info("Closed memory storage database connection")
    
    def __del__(self):
        """Destructor to ensure the database connection is closed."""
        self.close()


class MemoryAnalyzer:
    """
    Analyzer for historical run records.
    
    This class provides functionality to analyze historical run records
    and extract insights and patterns.
    
    Attributes:
        storage: Memory storage backend
    """
    
    def __init__(self, storage: Optional[MemoryStorage] = None):
        """
        Initialize the memory analyzer.
        
        Args:
            storage: Memory storage backend
        """
        self.storage = storage or MemoryStorage()
        logger.info("Memory analyzer initialized")
    
    def find_similar_runs(
        self,
        run_id: str,
        max_results: int = 5,
        similarity_threshold: float = 0.7,
    ) -> List[Dict[str, Any]]:
        """
        Find runs similar to the given run.
        
        Args:
            run_id: ID of the reference run
            max_results: Maximum number of similar runs to return
            similarity_threshold: Minimum similarity score (0-1)
        
        Returns:
            List of similar run records with similarity scores
        """
        try:
            # Load reference run
            reference_run = self.storage.load_run(run_id)
            if not reference_run:
                logger.warning(f"Reference run not found: {run_id}")
                return []
            
            # Get model and dataset info
            model_name = reference_run.model_info.get("name", "unknown_model")
            dataset_name = reference_run.dataset_info.get("name", "unknown_dataset")
            
            # Find candidate runs with the same model and dataset
            candidates = self.storage.list_runs(
                model_name=model_name,
                dataset_name=dataset_name,
                limit=100,
            )
            
            # Remove the reference run from candidates
            candidates = [c for c in candidates if c["run_id"] != run_id]
            
            if not candidates:
                logger.info(f"No similar runs found for {run_id}")
                return []
            
            # Load candidate runs
            candidate_runs = []
            for candidate in candidates:
                run = self.storage.load_run(candidate["run_id"])
                if run:
                    candidate_runs.append(run)
            
            # Calculate similarity scores
            similar_runs = []
            for candidate in candidate_runs:
                similarity = self._calculate_similarity(reference_run, candidate)
                if similarity >= similarity_threshold:
                    similar_runs.append({
                        "run_id": candidate.run_id,
                        "similarity": similarity,
                        "model_name": candidate.model_info.get("name", "unknown_model"),
                        "dataset_name": candidate.dataset_info.get("name", "unknown_dataset"),
                        "status": candidate.status,
                        "start_time": candidate.start_time,
                        "end_time": candidate.end_time,
                    })
            
            # Sort by similarity (descending)
            similar_runs.sort(key=lambda x: x["similarity"], reverse=True)
            
            # Limit results
            return similar_runs[:max_results]
        
        except Exception as e:
            logger.error(f"Failed to find similar runs: {e}")
            return []
    
    def _calculate_similarity(self, run1: RunRecord, run2: RunRecord) -> float:
        """
        Calculate similarity between two runs.
        
        Args:
            run1: First run
            run2: Second run
        
        Returns:
            Similarity score (0-1)
        """
        # Calculate similarity based on various factors
        similarities = []
        
        # Model similarity
        model_similarity = self._calculate_model_similarity(run1.model_info, run2.model_info)
        similarities.append(model_similarity)
        
        # Dataset similarity
        dataset_similarity = self._calculate_dataset_similarity(run1.dataset_info, run2.dataset_info)
        similarities.append(dataset_similarity)
        
        # Hardware similarity
        hardware_similarity = self._calculate_hardware_similarity(run1.hardware_info, run2.hardware_info)
        similarities.append(hardware_similarity)
        
        # Metrics similarity
        metrics_similarity = self._calculate_metrics_similarity(run1.metrics, run2.metrics)
        similarities.append(metrics_similarity)
        
        # Warnings similarity
        warnings_similarity = self._calculate_warnings_similarity(run1.warnings, run2.warnings)
        similarities.append(warnings_similarity)
        
        # Optimizations similarity
        optimizations_similarity = self._calculate_optimizations_similarity(run1.optimizations, run2.optimizations)
        similarities.append(optimizations_similarity)
        
        # Calculate weighted average
        weights = [0.25, 0.25, 0.1, 0.2, 0.1, 0.1]
        weighted_sum = sum(s * w for s, w in zip(similarities, weights))
        total_weight = sum(weights)
        
        return weighted_sum / total_weight
    
    def _calculate_model_similarity(self, model1: Dict[str, Any], model2: Dict[str, Any]) -> float:
        """
        Calculate similarity between two models.
        
        Args:
            model1: First model info
            model2: Second model info
        
        Returns:
            Similarity score (0-1)
        """
        # Check if models are identical
        if model1.get("name") == model2.get("name") and model1.get("architecture") == model2.get("architecture"):
            return 1.0
        
        # Check if architectures are the same
        if model1.get("architecture") == model2.get("architecture"):
            return 0.8
        
        # Check if model sizes are similar
        params1 = model1.get("num_parameters", 0)
        params2 = model2.get("num_parameters", 0)
        
        if params1 > 0 and params2 > 0:
            # Calculate size similarity
            ratio = min(params1, params2) / max(params1, params2)
            return 0.5 * ratio
        
        return 0.1
    
    def _calculate_dataset_similarity(self, dataset1: Dict[str, Any], dataset2: Dict[str, Any]) -> float:
        """
        Calculate similarity between two datasets.
        
        Args:
            dataset1: First dataset info
            dataset2: Second dataset info
        
        Returns:
            Similarity score (0-1)
        """
        # Check if datasets are identical
        if dataset1.get("name") == dataset2.get("name"):
            return 1.0
        
        # Check if dataset sizes are similar
        samples1 = dataset1.get("num_samples", 0)
        samples2 = dataset2.get("num_samples", 0)
        
        classes1 = dataset1.get("num_classes", 0)
        classes2 = dataset2.get("num_classes", 0)
        
        similarities = []
        
        # Sample size similarity
        if samples1 > 0 and samples2 > 0:
            ratio = min(samples1, samples2) / max(samples1, samples2)
            similarities.append(ratio)
        
        # Class count similarity
        if classes1 > 0 and classes2 > 0:
            if classes1 == classes2:
                similarities.append(1.0)
            else:
                ratio = min(classes1, classes2) / max(classes1, classes2)
                similarities.append(ratio)
        
        if not similarities:
            return 0.1
        
        return sum(similarities) / len(similarities)
    
    def _calculate_hardware_similarity(self, hardware1: Dict[str, Any], hardware2: Dict[str, Any]) -> float:
        """
        Calculate similarity between two hardware configurations.
        
        Args:
            hardware1: First hardware info
            hardware2: Second hardware info
        
        Returns:
            Similarity score (0-1)
        """
        # Check if hardware is identical
        if hardware1.get("name") == hardware2.get("name"):
            return 1.0
        
        # Check if GPU is the same
        if hardware1.get("gpu_name") == hardware2.get("gpu_name") and hardware1.get("gpu_name") is not None:
            return 0.9
        
        # Check if CPU is the same
        if hardware1.get("cpu_name") == hardware2.get("cpu_name") and hardware1.get("cpu_name") is not None:
            return 0.7
        
        return 0.3
    
    def _calculate_metrics_similarity(self, metrics1: Dict[str, List[Dict[str, Any]]], metrics2: Dict[str, List[Dict[str, Any]]]) -> float:
        """
        Calculate similarity between two sets of metrics.
        
        Args:
            metrics1: First metrics
            metrics2: Second metrics
        
        Returns:
            Similarity score (0-1)
        """
        # Check if both metrics are empty
        if not metrics1 and not metrics2:
            return 1.0
        
        # Check if one is empty
        if not metrics1 or not metrics2:
            return 0.0
        
        # Find common categories
        common_categories = set(metrics1.keys()) & set(metrics2.keys())
        if not common_categories:
            return 0.1
        
        # Calculate similarity for each common category
        category_similarities = []
        for category in common_categories:
            # Get the last metrics for each run
            if metrics1[category] and metrics2[category]:
                last_metrics1 = metrics1[category][-1]
                last_metrics2 = metrics2[category][-1]
                
                # Find common metric keys
                common_keys = set(last_metrics1.keys()) & set(last_metrics2.keys()) - {"timestamp"}
                if common_keys:
                    # Calculate similarity for each common key
                    key_similarities = []
                    for key in common_keys:
                        value1 = last_metrics1[key]
                        value2 = last_metrics2[key]
                        
                        # Skip non-numeric values
                        if not isinstance(value1, (int, float)) or not isinstance(value2, (int, float)):
                            continue
                        
                        # Calculate value similarity
                        if value1 == value2:
                            key_similarities.append(1.0)
                        else:
                            # Normalize values
                            max_val = max(abs(value1), abs(value2))
                            if max_val > 0:
                                diff = abs(value1 - value2) / max_val
                                key_similarities.append(max(0, 1.0 - diff))
                    
                    if key_similarities:
                        category_similarities.append(sum(key_similarities) / len(key_similarities))
        
        if not category_similarities:
            return 0.1
        
        return sum(category_similarities) / len(category_similarities)
    
    def _calculate_warnings_similarity(self, warnings1: List[Dict[str, Any]], warnings2: List[Dict[str, Any]]) -> float:
        """
        Calculate similarity between two sets of warnings.
        
        Args:
            warnings1: First warnings
            warnings2: Second warnings
        
        Returns:
            Similarity score (0-1)
        """
        # Check if both warnings are empty
        if not warnings1 and not warnings2:
            return 1.0
        
        # Check if one is empty
        if not warnings1 or not warnings2:
            return 0.0
        
        # Extract warning types
        types1 = {w.get("type") for w in warnings1 if "type" in w}
        types2 = {w.get("type") for w in warnings2 if "type" in w}
        
        # Calculate Jaccard similarity
        intersection = len(types1 & types2)
        union = len(types1 | types2)
        
        if union == 0:
            return 0.0
        
        return intersection / union
    
    def _calculate_optimizations_similarity(self, optimizations1: List[Dict[str, Any]], optimizations2: List[Dict[str, Any]]) -> float:
        """
        Calculate similarity between two sets of optimizations.
        
        Args:
            optimizations1: First optimizations
            optimizations2: Second optimizations
        
        Returns:
            Similarity score (0-1)
        """
        # Check if both optimizations are empty
        if not optimizations1 and not optimizations2:
            return 1.0
        
        # Check if one is empty
        if not optimizations1 or not optimizations2:
            return 0.0
        
        # Extract optimization types
        types1 = {o.get("type") for o in optimizations1 if "type" in o}
        types2 = {o.get("type") for o in optimizations2 if "type" in o}
        
        # Calculate Jaccard similarity
        intersection = len(types1 & types2)
        union = len(types1 | types2)
        
        if union == 0:
            return 0.0
        
        return intersection / union
    
    def analyze_run(self, run_id: str) -> Dict[str, Any]:
        """
        Analyze a run and extract insights.
        
        Args:
            run_id: ID of the run to analyze
        
        Returns:
            Dictionary of insights
        """
        try:
            # Load run
            run = self.storage.load_run(run_id)
            if not run:
                logger.warning(f"Run not found: {run_id}")
                return {}
            
            # Initialize insights
            insights = {
                "run_id": run_id,
                "model_name": run.model_info.get("name", "unknown_model"),
                "dataset_name": run.dataset_info.get("name", "unknown_dataset"),
                "status": run.status,
                "duration": (run.end_time or time.time()) - run.start_time,
                "metrics_summary": {},
                "warnings_summary": {},
                "optimizations_summary": {},
                "similar_runs": [],
                "recommendations": [],
            }
            
            # Analyze metrics
            insights["metrics_summary"] = self._analyze_metrics(run.metrics)
            
            # Analyze warnings
            insights["warnings_summary"] = self._analyze_warnings(run.warnings)
            
            # Analyze optimizations
            insights["optimizations_summary"] = self._analyze_optimizations(run.optimizations)
            
            # Find similar runs
            similar_runs = self.find_similar_runs(run_id)
            insights["similar_runs"] = similar_runs
            
            # Generate recommendations
            insights["recommendations"] = self._generate_recommendations(run, similar_runs)
            
            return insights
        
        except Exception as e:
            logger.error(f"Failed to analyze run: {e}")
            return {}
    
    def _analyze_metrics(self, metrics: Dict[str, List[Dict[str, Any]]]) -> Dict[str, Any]:
        """
        Analyze metrics and extract summary statistics.
        
        Args:
            metrics: Dictionary of metrics
        
        Returns:
            Dictionary of metric summaries
        """
        summary = {}
        
        for category, category_metrics in metrics.items():
            if not category_metrics:
                continue
            
            # Convert to DataFrame for easier analysis
            df = pd.DataFrame(category_metrics)
            
            # Get numeric columns
            numeric_cols = [col for col in df.columns if col != "timestamp" and pd.api.types.is_numeric_dtype(df[col])]
            
            if not numeric_cols:
                continue
            
            # Calculate summary statistics
            category_summary = {}
            for col in numeric_cols:
                col_summary = {
                    "mean": float(df[col].mean()),
                    "min": float(df[col].min()),
                    "max": float(df[col].max()),
                    "last": float(df[col].iloc[-1]),
                }
                
                # Calculate trend
                if len(df) > 1:
                    x = np.arange(len(df))
                    y = df[col].values
                    
                    # Linear regression
                    A = np.vstack([x, np.ones(len(x))]).T
                    m, c = np.linalg.lstsq(A, y, rcond=None)[0]
                    
                    col_summary["trend"] = float(m)
                    col_summary["trend_direction"] = "increasing" if m > 0 else "decreasing" if m < 0 else "stable"
                
                category_summary[col] = col_summary
            
            summary[category] = category_summary
        
        return summary
    
    def _analyze_warnings(self, warnings: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze warnings and extract summary statistics.
        
        Args:
            warnings: List of warnings
        
        Returns:
            Dictionary of warning summaries
        """
        if not warnings:
            return {"count": 0}
        
        # Count warnings by type
        warning_types = {}
        for warning in warnings:
            warning_type = warning.get("type", "unknown")
            if warning_type not in warning_types:
                warning_types[warning_type] = 0
            warning_types[warning_type] += 1
        
        # Count warnings by severity
        severity_counts = {}
        for warning in warnings:
            severity = warning.get("severity", "medium")
            if severity not in severity_counts:
                severity_counts[severity] = 0
            severity_counts[severity] += 1
        
        return {
            "count": len(warnings),
            "types": warning_types,
            "severity": severity_counts,
        }
    
    def _analyze_optimizations(self, optimizations: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze optimizations and extract summary statistics.
        
        Args:
            optimizations: List of optimizations
        
        Returns:
            Dictionary of optimization summaries
        """
        if not optimizations:
            return {"count": 0}
        
        # Count optimizations by type
        optimization_types = {}
        for optimization in optimizations:
            optimization_type = optimization.get("type", "unknown")
            if optimization_type not in optimization_types:
                optimization_types[optimization_type] = 0
            optimization_types[optimization_type] += 1
        
        # Count optimizations by category
        category_counts = {}
        for optimization in optimizations:
            category = optimization.get("category", "unknown")
            if isinstance(category, dict) and "name" in category:
                category = category["name"]
            if category not in category_counts:
                category_counts[category] = 0
            category_counts[category] += 1
        
        return {
            "count": len(optimizations),
            "types": optimization_types,
            "categories": category_counts,
        }
    
    def _generate_recommendations(self, run: RunRecord, similar_runs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Generate recommendations based on run analysis and similar runs.
        
        Args:
            run: Run record
            similar_runs: List of similar runs
        
        Returns:
            List of recommendations
        """
        recommendations = []
        
        # Check if run was successful
        if run.status != "completed":
            recommendations.append({
                "type": "status",
                "message": f"Run did not complete successfully (status: {run.status})",
                "priority": "high",
            })
        
        # Analyze metrics
        for category, metrics in run.metrics.items():
            if not metrics:
                continue
            
            # Memory recommendations
            if category == "memory":
                memory_recs = self._generate_memory_recommendations(metrics)
                recommendations.extend(memory_recs)
            
            # Timing recommendations
            elif category == "timing":
                timing_recs = self._generate_timing_recommendations(metrics)
                recommendations.extend(timing_recs)
            
            # Gradient recommendations
            elif category == "gradient":
                gradient_recs = self._generate_gradient_recommendations(metrics)
                recommendations.extend(gradient_recs)
            
            # Dataloader recommendations
            elif category == "dataloader":
                dataloader_recs = self._generate_dataloader_recommendations(metrics)
                recommendations.extend(dataloader_recs)
        
        # Analyze similar runs
        if similar_runs:
            similar_recs = self._generate_similar_run_recommendations(run, similar_runs)
            recommendations.extend(similar_recs)
        
        return recommendations
    
    def _generate_memory_recommendations(self, metrics: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Generate recommendations based on memory metrics.
        
        Args:
            metrics: List of memory metrics
        
        Returns:
            List of recommendations
        """
        recommendations = []
        
        # Get the last metrics
        last_metrics = metrics[-1]
        
        # Check for high memory usage
        if "allocated_memory" in last_metrics and "total_memory" in last_metrics:
            allocated = last_metrics["allocated_memory"]
            total = last_metrics["total_memory"]
            
            if total > 0:
                usage_pct = allocated / total
                
                if usage_pct > 0.9:
                    recommendations.append({
                        "type": "memory_usage",
                        "message": f"Memory usage is very high ({usage_pct:.1%})",
                        "details": "Consider reducing batch size or using gradient checkpointing",
                        "priority": "high",
                    })
                elif usage_pct > 0.7:
                    recommendations.append({
                        "type": "memory_usage",
                        "message": f"Memory usage is high ({usage_pct:.1%})",
                        "details": "Monitor memory usage closely",
                        "priority": "medium",
                    })
        
        # Check for memory fragmentation
        if "memory_fragmentation" in last_metrics:
            fragmentation = last_metrics["memory_fragmentation"]
            
            if fragmentation > 0.3:
                recommendations.append({
                    "type": "memory_fragmentation",
                    "message": f"Memory fragmentation is high ({fragmentation:.1%})",
                    "details": "Call torch.cuda.empty_cache() periodically",
                    "priority": "medium",
                })
        
        # Check for memory growth
        if len(metrics) > 1 and "allocated_memory" in metrics[0] and "allocated_memory" in metrics[-1]:
            first_allocated = metrics[0]["allocated_memory"]
            last_allocated = metrics[-1]["allocated_memory"]
            
            if first_allocated > 0:
                growth_pct = (last_allocated - first_allocated) / first_allocated
                
                if growth_pct > 0.5:
                    recommendations.append({
                        "type": "memory_growth",
                        "message": f"Memory usage is growing significantly ({growth_pct:.1%})",
                        "details": "Check for memory leaks or accumulating tensors",
                        "priority": "high",
                    })
        
        return recommendations
    
    def _generate_timing_recommendations(self, metrics: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Generate recommendations based on timing metrics.
        
        Args:
            metrics: List of timing metrics
        
        Returns:
            List of recommendations
        """
        recommendations = []
        
        # Get the last metrics
        last_metrics = metrics[-1]
        
        # Check for slow iterations
        if "iterations_per_second" in last_metrics:
            ips = last_metrics["iterations_per_second"]
            
            if ips < 1:
                recommendations.append({
                    "type": "slow_training",
                    "message": f"Training is very slow ({ips:.2f} iterations/second)",
                    "details": "Consider using a smaller model, mixed precision training, or more efficient hardware",
                    "priority": "high",
                })
            elif ips < 5:
                recommendations.append({
                    "type": "slow_training",
                    "message": f"Training is somewhat slow ({ips:.2f} iterations/second)",
                    "details": "Consider optimizations like mixed precision training",
                    "priority": "medium",
                })
        
        # Check for bottlenecks
        timing_keys = ["forward_time", "backward_time", "optimizer_time", "dataloader_time"]
        timing_values = {k: last_metrics.get(k, 0) for k in timing_keys if k in last_metrics}
        
        if timing_values:
            total_time = sum(timing_values.values())
            
            if total_time > 0:
                bottleneck = max(timing_values.items(), key=lambda x: x[1])
                bottleneck_pct = bottleneck[1] / total_time
                
                if bottleneck_pct > 0.5:
                    bottleneck_name = bottleneck[0].replace("_time", "")
                    
                    recommendations.append({
                        "type": f"{bottleneck_name}_bottleneck",
                        "message": f"{bottleneck_name.capitalize()} is a significant bottleneck ({bottleneck_pct:.1%} of total time)",
                        "details": self._get_bottleneck_details(bottleneck_name),
                        "priority": "medium",
                    })
        
        return recommendations
    
    def _get_bottleneck_details(self, bottleneck_name: str) -> str:
        """
        Get details for a specific bottleneck.
        
        Args:
            bottleneck_name: Name of the bottleneck
        
        Returns:
            Details string
        """
        if bottleneck_name == "forward":
            return "Consider using torch.compile() or a more efficient model architecture"
        elif bottleneck_name == "backward":
            return "Consider using gradient checkpointing or a more efficient model architecture"
        elif bottleneck_name == "optimizer":
            return "Consider using a different optimizer or gradient accumulation"
        elif bottleneck_name == "dataloader":
            return "Increase num_workers or use faster storage"
        else:
            return f"Optimize {bottleneck_name} phase"
    
    def _generate_gradient_recommendations(self, metrics: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Generate recommendations based on gradient metrics.
        
        Args:
            metrics: List of gradient metrics
        
        Returns:
            List of recommendations
        """
        recommendations = []
        
        # Get the last metrics
        last_metrics = metrics[-1]
        
        # Check for vanishing gradients
        if "avg_grad_norm" in last_metrics:
            avg_norm = last_metrics["avg_grad_norm"]
            
            if avg_norm < 0.001:
                recommendations.append({
                    "type": "vanishing_gradients",
                    "message": f"Gradients may be vanishing (avg norm: {avg_norm:.6f})",
                    "details": "Consider using batch normalization, residual connections, or different activation functions",
                    "priority": "high",
                })
        
        # Check for exploding gradients
        if "avg_grad_norm" in last_metrics:
            avg_norm = last_metrics["avg_grad_norm"]
            
            if avg_norm > 10.0:
                recommendations.append({
                    "type": "exploding_gradients",
                    "message": f"Gradients may be exploding (avg norm: {avg_norm:.4f})",
                    "details": "Consider using gradient clipping or reducing the learning rate",
                    "priority": "high",
                })
        
        # Check for dead gradients
        if "dead_gradients_pct" in last_metrics:
            dead_pct = last_metrics["dead_gradients_pct"]
            
            if dead_pct > 20:
                recommendations.append({
                    "type": "dead_gradients",
                    "message": f"Many parameters have near-zero gradients ({dead_pct:.1f}%)",
                    "details": "This may indicate dead neurons or vanishing gradients",
                    "priority": "medium",
                })
        
        return recommendations
    
    def _generate_dataloader_recommendations(self, metrics: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Generate recommendations based on dataloader metrics.
        
        Args:
            metrics: List of dataloader metrics
        
        Returns:
            List of recommendations
        """
        recommendations = []
        
        # Get the last metrics
        last_metrics = metrics[-1]
        
        # Check for dataloader efficiency
        if "worker_utilization" in last_metrics:
            utilization = last_metrics["worker_utilization"]
            
            if utilization < 0.5:
                recommendations.append({
                    "type": "dataloader_underutilization",
                    "message": f"Dataloader workers are underutilized ({utilization:.1%})",
                    "details": "Consider reducing the number of workers",
                    "priority": "low",
                })
            elif utilization > 0.9:
                recommendations.append({
                    "type": "dataloader_bottleneck",
                    "message": f"Dataloader workers are fully utilized ({utilization:.1%})",
                    "details": "Consider increasing the number of workers or using faster storage",
                    "priority": "medium",
                })
        
        # Check for optimal workers
        if "num_workers" in last_metrics and "estimated_optimal_workers" in last_metrics:
            num_workers = last_metrics["num_workers"]
            optimal_workers = last_metrics["estimated_optimal_workers"]
            
            if optimal_workers > num_workers * 1.5:
                recommendations.append({
                    "type": "dataloader_workers",
                    "message": f"Dataloader could use more workers (current: {num_workers}, optimal: {optimal_workers})",
                    "details": "Increase num_workers for better performance",
                    "priority": "medium",
                })
            elif num_workers > optimal_workers * 1.5:
                recommendations.append({
                    "type": "dataloader_workers",
                    "message": f"Dataloader has too many workers (current: {num_workers}, optimal: {optimal_workers})",
                    "details": "Reduce num_workers to free up resources",
                    "priority": "low",
                })
        
        return recommendations
    
    def _generate_similar_run_recommendations(self, run: RunRecord, similar_runs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Generate recommendations based on similar runs.
        
        Args:
            run: Current run
            similar_runs: List of similar runs
        
        Returns:
            List of recommendations
        """
        recommendations = []
        
        # Find successful similar runs
        successful_runs = [r for r in similar_runs if r["status"] == "completed"]
        
        if not successful_runs:
            return recommendations
        
        # Load the most similar successful run
        most_similar = successful_runs[0]
        similar_run = self.storage.load_run(most_similar["run_id"])
        
        if not similar_run:
            return recommendations
        
        # Compare optimizations
        current_optimizations = {o.get("type") for o in run.optimizations if "type" in o}
        similar_optimizations = {o.get("type") for o in similar_run.optimizations if "type" in o}
        
        # Find optimizations in the similar run that are not in the current run
        missing_optimizations = similar_optimizations - current_optimizations
        
        for opt_type in missing_optimizations:
            # Find the optimization details in the similar run
            opt_details = next((o for o in similar_run.optimizations if o.get("type") == opt_type), None)
            
            if opt_details:
                recommendations.append({
                    "type": "similar_run_optimization",
                    "message": f"A similar run used the '{opt_type}' optimization",
                    "details": opt_details.get("message", f"Consider applying the {opt_type} optimization"),
                    "priority": "medium",
                    "similar_run_id": most_similar["run_id"],
                })
        
        # Compare durations
        if run.end_time and similar_run.end_time:
            current_duration = run.end_time - run.start_time
            similar_duration = similar_run.end_time - similar_run.start_time
            
            if current_duration > similar_duration * 1.5:
                recommendations.append({
                    "type": "similar_run_performance",
                    "message": f"A similar run completed {current_duration/similar_duration:.1f}x faster",
                    "details": f"Run {most_similar['run_id']} took {similar_duration:.1f}s vs. {current_duration:.1f}s for the current run",
                    "priority": "high",
                    "similar_run_id": most_similar["run_id"],
                })
        
        return recommendations
    
    def cluster_runs(
        self,
        model_name: Optional[str] = None,
        dataset_name: Optional[str] = None,
        n_clusters: int = 3,
    ) -> Dict[str, Any]:
        """
        Cluster runs based on their metrics.
        
        Args:
            model_name: Filter by model name
            dataset_name: Filter by dataset name
            n_clusters: Number of clusters to create
        
        Returns:
            Dictionary with clustering results
        """
        try:
            # Get runs
            runs_metadata = self.storage.list_runs(
                model_name=model_name,
                dataset_name=dataset_name,
                limit=1000,
            )
            
            if not runs_metadata:
                logger.warning("No runs found for clustering")
                return {"clusters": []}
            
            # Load runs
            runs = []
            for metadata in runs_metadata:
                run = self.storage.load_run(metadata["run_id"])
                if run and run.status == "completed":
                    runs.append(run)
            
            if len(runs) < n_clusters:
                logger.warning(f"Not enough runs for clustering: {len(runs)} < {n_clusters}")
                return {"clusters": []}
            
            # Extract features
            features = []
            for run in runs:
                run_features = self._extract_clustering_features(run)
                if run_features:
                    features.append(run_features)
            
            if not features:
                logger.warning("No features extracted for clustering")
                return {"clusters": []}
            
            # Convert to DataFrame
            feature_df = pd.DataFrame(features)
            
            # Fill missing values
            feature_df = feature_df.fillna(0)
            
            # Standardize features
            scaler = StandardScaler()
            scaled_features = scaler.fit_transform(feature_df)
            
            # Apply PCA if there are many features
            if scaled_features.shape[1] > 10:
                pca = PCA(n_components=min(10, scaled_features.shape[0]))
                scaled_features = pca.fit_transform(scaled_features)
            
            # Apply K-means clustering
            kmeans = KMeans(n_clusters=min(n_clusters, len(scaled_features)), random_state=42)
            clusters = kmeans.fit_predict(scaled_features)
            
            # Organize results
            cluster_results = {}
            for i, cluster_id in enumerate(clusters):
                if cluster_id not in cluster_results:
                    cluster_results[cluster_id] = []
                
                cluster_results[cluster_id].append({
                    "run_id": runs[i].run_id,
                    "model_name": runs[i].model_info.get("name", "unknown_model"),
                    "dataset_name": runs[i].dataset_info.get("name", "unknown_dataset"),
                    "status": runs[i].status,
                    "duration": (runs[i].end_time or time.time()) - runs[i].start_time,
                })
            
            # Calculate cluster statistics
            cluster_stats = []
            for cluster_id, cluster_runs in cluster_results.items():
                # Calculate average duration
                durations = [r["duration"] for r in cluster_runs]
                avg_duration = sum(durations) / len(durations) if durations else 0
                
                cluster_stats.append({
                    "cluster_id": int(cluster_id),
                    "size": len(cluster_runs),
                    "avg_duration": avg_duration,
                    "runs": cluster_runs,
                })
            
            # Sort clusters by size (descending)
            cluster_stats.sort(key=lambda x: x["size"], reverse=True)
            
            return {"clusters": cluster_stats}
        
        except Exception as e:
            logger.error(f"Failed to cluster runs: {e}")
            return {"clusters": []}
    
    def _extract_clustering_features(self, run: RunRecord) -> Optional[Dict[str, float]]:
        """
        Extract features for clustering from a run.
        
        Args:
            run: Run record
        
        Returns:
            Dictionary of features or None if not enough data
        """
        features = {}
        
        # Extract duration
        if run.end_time:
            features["duration"] = run.end_time - run.start_time
        
        # Extract memory metrics
        if "memory" in run.metrics and run.metrics["memory"]:
            last_memory = run.metrics["memory"][-1]
            
            for key, value in last_memory.items():
                if key != "timestamp" and isinstance(value, (int, float)):
                    features[f"memory_{key}"] = value
        
        # Extract timing metrics
        if "timing" in run.metrics and run.metrics["timing"]:
            last_timing = run.metrics["timing"][-1]
            
            for key, value in last_timing.items():
                if key != "timestamp" and isinstance(value, (int, float)):
                    features[f"timing_{key}"] = value
        
        # Extract gradient metrics
        if "gradient" in run.metrics and run.metrics["gradient"]:
            last_gradient = run.metrics["gradient"][-1]
            
            for key, value in last_gradient.items():
                if key != "timestamp" and isinstance(value, (int, float)):
                    features[f"gradient_{key}"] = value
        
        # Extract dataloader metrics
        if "dataloader" in run.metrics and run.metrics["dataloader"]:
            last_dataloader = run.metrics["dataloader"][-1]
            
            for key, value in last_dataloader.items():
                if key != "timestamp" and isinstance(value, (int, float)):
                    features[f"dataloader_{key}"] = value
        
        # Count warnings by type
        warning_types = {}
        for warning in run.warnings:
            warning_type = warning.get("type", "unknown")
            if warning_type not in warning_types:
                warning_types[warning_type] = 0
            warning_types[warning_type] += 1
        
        for warning_type, count in warning_types.items():
            features[f"warning_{warning_type}"] = count
        
        # Count optimizations by type
        optimization_types = {}
        for optimization in run.optimizations:
            optimization_type = optimization.get("type", "unknown")
            if optimization_type not in optimization_types:
                optimization_types[optimization_type] = 0
            optimization_types[optimization_type] += 1
        
        for optimization_type, count in optimization_types.items():
            features[f"optimization_{optimization_type}"] = count
        
        # Return features if we have enough
        if len(features) > 3:
            return features
        else:
            return None
    
    def get_run_statistics(
        self,
        model_name: Optional[str] = None,
        dataset_name: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Get statistics for runs matching the given criteria.
        
        Args:
            model_name: Filter by model name
            dataset_name: Filter by dataset name
        
        Returns:
            Dictionary of statistics
        """
        try:
            # Get runs
            runs_metadata = self.storage.list_runs(
                model_name=model_name,
                dataset_name=dataset_name,
                limit=1000,
            )
            
            if not runs_metadata:
                logger.warning("No runs found for statistics")
                return {}
            
            # Initialize statistics
            stats = {
                "total_runs": len(runs_metadata),
                "completed_runs": 0,
                "failed_runs": 0,
                "avg_duration": 0,
                "min_duration": float("inf"),
                "max_duration": 0,
                "common_warnings": {},
                "common_optimizations": {},
                "model_distribution": {},
                "dataset_distribution": {},
            }
            
            # Calculate basic statistics
            durations = []
            for metadata in runs_metadata:
                # Count by status
                if metadata["status"] == "completed":
                    stats["completed_runs"] += 1
                elif metadata["status"] == "failed":
                    stats["failed_runs"] += 1
                
                # Calculate duration
                if metadata["end_time"]:
                    duration = metadata["end_time"] - metadata["start_time"]
                    durations.append(duration)
                    
                    stats["min_duration"] = min(stats["min_duration"], duration)
                    stats["max_duration"] = max(stats["max_duration"], duration)
                
                # Count by model
                model_name = metadata["model_name"]
                if model_name not in stats["model_distribution"]:
                    stats["model_distribution"][model_name] = 0
                stats["model_distribution"][model_name] += 1
                
                # Count by dataset
                dataset_name = metadata["dataset_name"]
                if dataset_name not in stats["dataset_distribution"]:
                    stats["dataset_distribution"][dataset_name] = 0
                stats["dataset_distribution"][dataset_name] += 1
            
            # Calculate average duration
            if durations:
                stats["avg_duration"] = sum(durations) / len(durations)
            
            if stats["min_duration"] == float("inf"):
                stats["min_duration"] = 0
            
            # Load a sample of runs for detailed analysis
            sample_size = min(20, len(runs_metadata))
            sample_metadata = runs_metadata[:sample_size]
            
            warning_counts = {}
            optimization_counts = {}
            
            for metadata in sample_metadata:
                run = self.storage.load_run(metadata["run_id"])
                if not run:
                    continue
                
                # Count warnings
                for warning in run.warnings:
                    warning_type = warning.get("type", "unknown")
                    if warning_type not in warning_counts:
                        warning_counts[warning_type] = 0
                    warning_counts[warning_type] += 1
                
                # Count optimizations
                for optimization in run.optimizations:
                    optimization_type = optimization.get("type", "unknown")
                    if optimization_type not in optimization_counts:
                        optimization_counts[optimization_type] = 0
                    optimization_counts[optimization_type] += 1
            
            # Sort and limit
            stats["common_warnings"] = dict(sorted(warning_counts.items(), key=lambda x: x[1], reverse=True)[:10])
            stats["common_optimizations"] = dict(sorted(optimization_counts.items(), key=lambda x: x[1], reverse=True)[:10])
            
            return stats
        
        except Exception as e:
            logger.error(f"Failed to get run statistics: {e}")
            return {}
    
    def __repr__(self) -> str:
        """String representation of the memory analyzer."""
        return "MemoryAnalyzer()"


class ExperienceBrain:
    """
    Experience brain for AutoPipelineDoctor.
    
    This class provides functionality to learn from past runs and make
    predictions and recommendations based on historical data.
    
    Attributes:
        storage: Memory storage backend
        analyzer: Memory analyzer
        current_run: Current run record
        is_active: Whether the experience brain is active
    """
    
    def __init__(
        self,
        storage_dir: Optional[str] = None,
        doctor: Optional[Any] = None,
    ):
        """
        Initialize the experience brain.
        
        Args:
            storage_dir: Directory to store run records
            doctor: Reference to the Doctor instance
        """
        self.storage = MemoryStorage(storage_dir)
        self.analyzer = MemoryAnalyzer(self.storage)
        self.doctor = doctor
        self.current_run = None
        self.is_active = False
        
        logger.info("Experience brain initialized")
    
    def start(
        self,
        model_info: Optional[Dict[str, Any]] = None,
        dataset_info: Optional[Dict[str, Any]] = None,
        hardware_info: Optional[Dict[str, Any]] = None,
    ) -> str:
        """
        Start a new run.
        
        Args:
            model_info: Information about the model
            dataset_info: Information about the dataset
            hardware_info: Information about the hardware
        
        Returns:
            Run ID
        """
        # Create a new run record
        self.current_run = RunRecord(
            model_info=model_info,
            dataset_info=dataset_info,
            hardware_info=hardware_info,
        )
        
        # Save the run
        self.storage.save_run(self.current_run)
        
        self.is_active = True
        logger.info(f"Started new run: {self.current_run.run_id}")
        
        return self.current_run.run_id
    
    def stop(self, status: str = "completed") -> bool:
        """
        Stop the current run.
        
        Args:
            status: Status of the run (e.g., "completed", "failed")
        
        Returns:
            True if successful, False otherwise
        """
        if not self.current_run:
            logger.warning("No current run to stop")
            return False
        
        # Mark the run as completed
        self.current_run.complete(status)
        
        # Save the run
        result = self.storage.save_run(self.current_run)
        
        self.is_active = False
        logger.info(f"Stopped run: {self.current_run.run_id} with status: {status}")
        
        return result
    
    def update_metrics(self, metrics: Dict[str, Any], category: str = "general"):
        """
        Update metrics for the current run.
        
        Args:
            metrics: Dictionary of metrics to update
            category: Category of metrics
        """
        if not self.is_active or not self.current_run:
            logger.warning("No active run to update metrics")
            return
        
        # Update metrics in the current run
        self.current_run.update_metrics(metrics, category)
        
        # Save the run
        self.storage.save_run(self.current_run)
    
    def add_warning(self, warning: Dict[str, Any]):
        """
        Add a warning to the current run.
        
        Args:
            warning: Warning dictionary
        """
        if not self.is_active or not self.current_run:
            logger.warning("No active run to add warning")
            return
        
        # Add warning to the current run
        self.current_run.add_warning(warning)
        
        # Save the run
        self.storage.save_run(self.current_run)
    
    def add_optimization(self, optimization: Dict[str, Any]):
        """
        Add an optimization to the current run.
        
        Args:
            optimization: Optimization dictionary
        """
        if not self.is_active or not self.current_run:
            logger.warning("No active run to add optimization")
            return
        
        # Add optimization to the current run
        self.current_run.add_optimization(optimization)
        
        # Save the run
        self.storage.save_run(self.current_run)
    
    def get_similar_runs(self, max_results: int = 5) -> List[Dict[str, Any]]:
        """
        Get runs similar to the current run.
        
        Args:
            max_results: Maximum number of similar runs to return
        
        Returns:
            List of similar run records with similarity scores
        """
        if not self.current_run:
            logger.warning("No current run to find similar runs")
            return []
        
        # Save the current run to ensure it's up to date
        self.storage.save_run(self.current_run)
        
        # Find similar runs
        return self.analyzer.find_similar_runs(
            self.current_run.run_id,
            max_results=max_results,
        )
    
    def get_recommendations(self) -> List[Dict[str, Any]]:
        """
        Get recommendations based on the current run and historical data.
        
        Returns:
            List of recommendations
        """
        if not self.current_run:
            logger.warning("No current run to generate recommendations")
            return []
        
        # Save the current run to ensure it's up to date
        self.storage.save_run(self.current_run)
        
        # Analyze the current run
        insights = self.analyzer.analyze_run(self.current_run.run_id)
        
        return insights.get("recommendations", [])
    
    def predict_failures(self) -> List[Dict[str, Any]]:
        """
        Predict potential failures based on the current run and historical data.
        
        Returns:
            List of potential failures
        """
        if not self.current_run:
            logger.warning("No current run to predict failures")
            return []
        
        # Get similar runs
        similar_runs = self.get_similar_runs(max_results=10)
        
        # Filter for failed runs
        failed_runs = [r for r in similar_runs if r["status"] == "failed"]
        
        if not failed_runs:
            return []
        
        # Load failed runs
        failure_predictions = []
        for run_meta in failed_runs:
            run = self.storage.load_run(run_meta["run_id"])
            if not run:
                continue
            
            # Extract failure information
            failure_info = {
                "run_id": run.run_id,
                "similarity": run_meta["similarity"],
                "status": run.status,
                "warnings": [w for w in run.warnings if w.get("severity") in ["high", "critical"]],
            }
            
            if failure_info["warnings"]:
                failure_predictions.append(failure_info)
        
        return failure_predictions
    
    def get_optimization_history(self, optimization_type: str) -> List[Dict[str, Any]]:
        """
        Get history of a specific optimization type.
        
        Args:
            optimization_type: Type of optimization
        
        Returns:
            List of runs where the optimization was applied
        """
        # Get all runs
        runs_metadata = self.storage.list_runs(limit=100)
        
        optimization_history = []
        for metadata in runs_metadata:
            run = self.storage.load_run(metadata["run_id"])
            if not run:
                continue
            
            # Check if the optimization was applied
            matching_optimizations = [o for o in run.optimizations if o.get("type") == optimization_type]
            
            if matching_optimizations:
                # Extract relevant information
                history_entry = {
                    "run_id": run.run_id,
                    "model_name": run.model_info.get("name", "unknown_model"),
                    "dataset_name": run.dataset_info.get("name", "unknown_dataset"),
                    "status": run.status,
                    "optimizations": matching_optimizations,
                }
                
                optimization_history.append(history_entry)
        
        return optimization_history
    
    def get_run_history(
        self,
        model_name: Optional[str] = None,
        dataset_name: Optional[str] = None,
        limit: int = 10,
    ) -> List[Dict[str, Any]]:
        """
        Get history of runs matching the given criteria.
        
        Args:
            model_name: Filter by model name
            dataset_name: Filter by dataset name
            limit: Maximum number of runs to return
        
        Returns:
            List of run records
        """
        # Get runs matching the criteria
        runs_metadata = self.storage.list_runs(
            model_name=model_name,
            dataset_name=dataset_name,
            limit=limit,
        )
        
        run_history = []
        for metadata in runs_metadata:
            run = self.storage.load_run(metadata["run_id"])
            if not run:
                continue
            
            # Extract relevant information
            history_entry = {
                "run_id": run.run_id,
                "model_name": run.model_info.get("name", "unknown_model"),
                "dataset_name": run.dataset_info.get("name", "unknown_dataset"),
                "status": run.status,
                "start_time": run.start_time,
                "end_time": run.end_time,
                "duration": (run.end_time or time.time()) - run.start_time,
                "warnings_count": len(run.warnings),
                "optimizations_count": len(run.optimizations),
            }
            
            run_history.append(history_entry)
        
        return run_history
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get statistics about all runs.
        
        Returns:
            Dictionary of statistics
        """
        return self.analyzer.get_run_statistics()
    
    def export_runs(self, output_dir: str) -> bool:
        """
        Export all runs to a directory.
        
        Args:
            output_dir: Directory to export to
        
        Returns:
            True if successful, False otherwise
        """
        return self.storage.export_runs(output_dir)
    
    def import_runs(self, input_dir: str) -> int:
        """
        Import runs from a directory.
        
        Args:
            input_dir: Directory to import from
        
        Returns:
            Number of imported runs
        """
        return self.storage.import_runs(input_dir)
    
    def close(self):
        """Close the experience brain."""
        if self.storage:
            self.storage.close()
        
        self.is_active = False
        logger.info("Experience brain closed")
    
    def __del__(self):
        """Destructor to ensure resources are properly released."""
        self.close()
    
    def __repr__(self) -> str:
        """String representation of the experience brain."""
        status = "active" if self.is_active else "inactive"
        current_run_id = self.current_run.run_id if self.current_run else "none"
        return f"ExperienceBrain(status={status}, current_run={current_run_id})"
