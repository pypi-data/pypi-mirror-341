"""
DNA Tracker for Experiment Lineage module for AutoPipelineDoctor.

This advanced module assigns a unique genetic fingerprint to every training run,
tracks the full ancestry of models including checkpoint sources, parameter deltas,
and code diffs, and visualizes the model evolution tree over time.
"""

import os
import json
import time
import uuid
import hashlib
import difflib
import pickle
import logging
import datetime
import re
import copy
import traceback
from typing import Dict, List, Tuple, Optional, Union, Any, Set, Type, Callable
from dataclasses import dataclass, field
from collections import defaultdict, deque
from enum import Enum
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import networkx as nx
import torch
import pandas as pd
import seaborn as sns
from matplotlib.lines import Line2D

logger = logging.getLogger(__name__)


class ModelSource(Enum):
    """Source of a model checkpoint."""
    SCRATCH = "scratch"
    CHECKPOINT = "checkpoint"
    PRETRAINED = "pretrained"
    FINETUNED = "finetuned"
    DISTILLED = "distilled"
    MERGED = "merged"
    PRUNED = "pruned"
    QUANTIZED = "quantized"
    CUSTOM = "custom"


class ModelRelationship(Enum):
    """Relationship between models."""
    PARENT = "parent"
    CHILD = "child"
    SIBLING = "sibling"
    FORK = "fork"
    MERGE_SOURCE = "merge_source"
    MERGE_TARGET = "merge_target"
    DISTILLATION_TEACHER = "distillation_teacher"
    DISTILLATION_STUDENT = "distillation_student"
    CONTINUATION = "continuation"
    CUSTOM = "custom"


class ChangeType(Enum):
    """Type of change between models."""
    ARCHITECTURE = "architecture"
    HYPERPARAMETERS = "hyperparameters"
    WEIGHTS = "weights"
    OPTIMIZER = "optimizer"
    DATASET = "dataset"
    TRAINING_CODE = "training_code"
    ENVIRONMENT = "environment"
    CUSTOM = "custom"


class ChangeSignificance(Enum):
    """Significance of a change."""
    MAJOR = "major"
    MINOR = "minor"
    PATCH = "patch"
    EXPERIMENTAL = "experimental"
    CUSTOM = "custom"


@dataclass
class ModelFingerprint:
    """
    Unique fingerprint for a model.
    
    Attributes:
        id: Unique identifier
        hash: Hash of model weights
        architecture_hash: Hash of model architecture
        hyperparameters_hash: Hash of hyperparameters
        dataset_hash: Hash of dataset
        code_hash: Hash of training code
        environment_hash: Hash of environment
        timestamp: Creation timestamp
        source: Source of the model
        parent_ids: List of parent model IDs
    """
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    hash: str = ""
    architecture_hash: str = ""
    hyperparameters_hash: str = ""
    dataset_hash: str = ""
    code_hash: str = ""
    environment_hash: str = ""
    timestamp: float = field(default_factory=time.time)
    source: ModelSource = ModelSource.SCRATCH
    parent_ids: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "id": self.id,
            "hash": self.hash,
            "architecture_hash": self.architecture_hash,
            "hyperparameters_hash": self.hyperparameters_hash,
            "dataset_hash": self.dataset_hash,
            "code_hash": self.code_hash,
            "environment_hash": self.environment_hash,
            "timestamp": self.timestamp,
            "source": self.source.value,
            "parent_ids": self.parent_ids,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ModelFingerprint':
        """Create from dictionary."""
        return cls(
            id=data.get("id", str(uuid.uuid4())),
            hash=data.get("hash", ""),
            architecture_hash=data.get("architecture_hash", ""),
            hyperparameters_hash=data.get("hyperparameters_hash", ""),
            dataset_hash=data.get("dataset_hash", ""),
            code_hash=data.get("code_hash", ""),
            environment_hash=data.get("environment_hash", ""),
            timestamp=data.get("timestamp", time.time()),
            source=ModelSource(data.get("source", ModelSource.SCRATCH.value)),
            parent_ids=data.get("parent_ids", []),
        )


@dataclass
class ModelChange:
    """
    Change between models.
    
    Attributes:
        from_id: Source model ID
        to_id: Target model ID
        type: Type of change
        significance: Significance of change
        description: Description of change
        details: Detailed information about the change
        timestamp: Change timestamp
    """
    from_id: str
    to_id: str
    type: ChangeType
    significance: ChangeSignificance
    description: str
    details: Dict[str, Any] = field(default_factory=dict)
    timestamp: float = field(default_factory=time.time)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "from_id": self.from_id,
            "to_id": self.to_id,
            "type": self.type.value,
            "significance": self.significance.value,
            "description": self.description,
            "details": self.details,
            "timestamp": self.timestamp,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ModelChange':
        """Create from dictionary."""
        return cls(
            from_id=data.get("from_id", ""),
            to_id=data.get("to_id", ""),
            type=ChangeType(data.get("type", ChangeType.CUSTOM.value)),
            significance=ChangeSignificance(data.get("significance", ChangeSignificance.CUSTOM.value)),
            description=data.get("description", ""),
            details=data.get("details", {}),
            timestamp=data.get("timestamp", time.time()),
        )


@dataclass
class ModelMetadata:
    """
    Metadata for a model.
    
    Attributes:
        name: Model name
        description: Model description
        version: Model version
        tags: List of tags
        metrics: Performance metrics
        custom_metadata: Custom metadata
    """
    name: str = ""
    description: str = ""
    version: str = "0.1.0"
    tags: List[str] = field(default_factory=list)
    metrics: Dict[str, Any] = field(default_factory=dict)
    custom_metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "name": self.name,
            "description": self.description,
            "version": self.version,
            "tags": self.tags,
            "metrics": self.metrics,
            "custom_metadata": self.custom_metadata,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ModelMetadata':
        """Create from dictionary."""
        return cls(
            name=data.get("name", ""),
            description=data.get("description", ""),
            version=data.get("version", "0.1.0"),
            tags=data.get("tags", []),
            metrics=data.get("metrics", {}),
            custom_metadata=data.get("custom_metadata", {}),
        )


@dataclass
class ModelRecord:
    """
    Record of a model.
    
    Attributes:
        fingerprint: Model fingerprint
        metadata: Model metadata
        checkpoint_path: Path to model checkpoint
        creation_time: Creation time
        last_modified: Last modified time
    """
    fingerprint: ModelFingerprint
    metadata: ModelMetadata = field(default_factory=ModelMetadata)
    checkpoint_path: Optional[str] = None
    creation_time: float = field(default_factory=time.time)
    last_modified: float = field(default_factory=time.time)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "fingerprint": self.fingerprint.to_dict(),
            "metadata": self.metadata.to_dict(),
            "checkpoint_path": self.checkpoint_path,
            "creation_time": self.creation_time,
            "last_modified": self.last_modified,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ModelRecord':
        """Create from dictionary."""
        return cls(
            fingerprint=ModelFingerprint.from_dict(data.get("fingerprint", {})),
            metadata=ModelMetadata.from_dict(data.get("metadata", {})),
            checkpoint_path=data.get("checkpoint_path"),
            creation_time=data.get("creation_time", time.time()),
            last_modified=data.get("last_modified", time.time()),
        )


class DNATracker:
    """
    DNA Tracker for Experiment Lineage.
    
    This module assigns a unique genetic fingerprint to every training run,
    tracks the full ancestry of models including checkpoint sources, parameter deltas,
    and code diffs, and visualizes the model evolution tree over time.
    
    Attributes:
        storage_dir: Directory for storing DNA tracker data
        models: Dictionary of model records by ID
        changes: List of model changes
        relationships: Dictionary of model relationships
        current_model_id: ID of the current model being tracked
    """
    
    def __init__(self, storage_dir: str = "./dna_tracker"):
        """
        Initialize the DNA Tracker.
        
        Args:
            storage_dir: Directory for storing DNA tracker data
        """
        self.storage_dir = storage_dir
        self.models: Dict[str, ModelRecord] = {}
        self.changes: List[ModelChange] = []
        self.relationships: Dict[str, Dict[str, ModelRelationship]] = defaultdict(dict)
        self.current_model_id: Optional[str] = None
        
        # Create storage directory
        os.makedirs(storage_dir, exist_ok=True)
        os.makedirs(os.path.join(storage_dir, "models"), exist_ok=True)
        os.makedirs(os.path.join(storage_dir, "changes"), exist_ok=True)
        os.makedirs(os.path.join(storage_dir, "visualizations"), exist_ok=True)
        
        # Load existing data
        self._load_data()
        
        logger.info(f"Initialized DNA Tracker with {len(self.models)} models and {len(self.changes)} changes")
    
    def _load_data(self) -> None:
        """Load existing data from storage."""
        try:
            # Load models
            models_file = os.path.join(self.storage_dir, "models.json")
            if os.path.exists(models_file):
                with open(models_file, "r") as f:
                    models_data = json.load(f)
                
                for model_data in models_data:
                    model_record = ModelRecord.from_dict(model_data)
                    self.models[model_record.fingerprint.id] = model_record
            
            # Load changes
            changes_file = os.path.join(self.storage_dir, "changes.json")
            if os.path.exists(changes_file):
                with open(changes_file, "r") as f:
                    changes_data = json.load(f)
                
                for change_data in changes_data:
                    self.changes.append(ModelChange.from_dict(change_data))
            
            # Load relationships
            relationships_file = os.path.join(self.storage_dir, "relationships.json")
            if os.path.exists(relationships_file):
                with open(relationships_file, "r") as f:
                    relationships_data = json.load(f)
                
                for from_id, to_relationships in relationships_data.items():
                    for to_id, relationship_value in to_relationships.items():
                        self.relationships[from_id][to_id] = ModelRelationship(relationship_value)
            
            # Load current model ID
            current_model_file = os.path.join(self.storage_dir, "current_model.txt")
            if os.path.exists(current_model_file):
                with open(current_model_file, "r") as f:
                    self.current_model_id = f.read().strip()
            
            logger.info(f"Loaded {len(self.models)} models and {len(self.changes)} changes from {self.storage_dir}")
        
        except Exception as e:
            logger.error(f"Error loading DNA tracker data: {e}")
            logger.error(traceback.format_exc())
    
    def _save_data(self) -> None:
        """Save data to storage."""
        try:
            # Save models
            models_data = [model.to_dict() for model in self.models.values()]
            models_file = os.path.join(self.storage_dir, "models.json")
            with open(models_file, "w") as f:
                json.dump(models_data, f, indent=2)
            
            # Save changes
            changes_data = [change.to_dict() for change in self.changes]
            changes_file = os.path.join(self.storage_dir, "changes.json")
            with open(changes_file, "w") as f:
                json.dump(changes_data, f, indent=2)
            
            # Save relationships
            relationships_data = {}
            for from_id, to_relationships in self.relationships.items():
                relationships_data[from_id] = {to_id: relationship.value for to_id, relationship in to_relationships.items()}
            
            relationships_file = os.path.join(self.storage_dir, "relationships.json")
            with open(relationships_file, "w") as f:
                json.dump(relationships_data, f, indent=2)
            
            # Save current model ID
            if self.current_model_id:
                current_model_file = os.path.join(self.storage_dir, "current_model.txt")
                with open(current_model_file, "w") as f:
                    f.write(self.current_model_id)
            
            logger.info(f"Saved {len(self.models)} models and {len(self.changes)} changes to {self.storage_dir}")
        
        except Exception as e:
            logger.error(f"Error saving DNA tracker data: {e}")
            logger.error(traceback.format_exc())
    
    def register_model(
        self,
        model: torch.nn.Module,
        hyperparameters: Dict[str, Any],
        dataset_info: Dict[str, Any],
        code_files: Optional[List[str]] = None,
        environment_info: Optional[Dict[str, Any]] = None,
        source: ModelSource = ModelSource.SCRATCH,
        parent_ids: Optional[List[str]] = None,
        metadata: Optional[ModelMetadata] = None,
        checkpoint_path: Optional[str] = None,
    ) -> str:
        """
        Register a new model.
        
        Args:
            model: PyTorch model
            hyperparameters: Model hyperparameters
            dataset_info: Dataset information
            code_files: List of code files used for training
            environment_info: Environment information
            source: Source of the model
            parent_ids: List of parent model IDs
            metadata: Model metadata
            checkpoint_path: Path to model checkpoint
            
        Returns:
            Model ID
        """
        # Generate fingerprint
        fingerprint = self._generate_fingerprint(
            model=model,
            hyperparameters=hyperparameters,
            dataset_info=dataset_info,
            code_files=code_files,
            environment_info=environment_info,
            source=source,
            parent_ids=parent_ids or [],
        )
        
        # Create model record
        model_record = ModelRecord(
            fingerprint=fingerprint,
            metadata=metadata or ModelMetadata(),
            checkpoint_path=checkpoint_path,
        )
        
        # Add to models
        self.models[fingerprint.id] = model_record
        
        # Set as current model
        self.current_model_id = fingerprint.id
        
        # Create relationships
        if parent_ids:
            for parent_id in parent_ids:
                if parent_id in self.models:
                    # Add parent-child relationship
                    self.relationships[parent_id][fingerprint.id] = ModelRelationship.CHILD
                    self.relationships[fingerprint.id][parent_id] = ModelRelationship.PARENT
                    
                    # Add sibling relationships
                    for sibling_id in self.get_children(parent_id):
                        if sibling_id != fingerprint.id:
                            self.relationships[fingerprint.id][sibling_id] = ModelRelationship.SIBLING
                            self.relationships[sibling_id][fingerprint.id] = ModelRelationship.SIBLING
        
        # Save data
        self._save_data()
        
        # Save model-specific data
        self._save_model_data(fingerprint.id, model, hyperparameters, dataset_info, code_files, environment_info)
        
        logger.info(f"Registered model with ID: {fingerprint.id}")
        
        return fingerprint.id
    
    def _generate_fingerprint(
        self,
        model: torch.nn.Module,
        hyperparameters: Dict[str, Any],
        dataset_info: Dict[str, Any],
        code_files: Optional[List[str]] = None,
        environment_info: Optional[Dict[str, Any]] = None,
        source: ModelSource = ModelSource.SCRATCH,
        parent_ids: List[str] = None,
    ) -> ModelFingerprint:
        """
        Generate a fingerprint for a model.
        
        Args:
            model: PyTorch model
            hyperparameters: Model hyperparameters
            dataset_info: Dataset information
            code_files: List of code files used for training
            environment_info: Environment information
            source: Source of the model
            parent_ids: List of parent model IDs
            
        Returns:
            Model fingerprint
        """
        # Generate model hash
        model_hash = self._hash_model(model)
        
        # Generate architecture hash
        architecture_hash = self._hash_architecture(model)
        
        # Generate hyperparameters hash
        hyperparameters_hash = self._hash_dict(hyperparameters)
        
        # Generate dataset hash
        dataset_hash = self._hash_dict(dataset_info)
        
        # Generate code hash
        code_hash = self._hash_code_files(code_files) if code_files else ""
        
        # Generate environment hash
        environment_hash = self._hash_dict(environment_info) if environment_info else ""
        
        # Create fingerprint
        fingerprint = ModelFingerprint(
            hash=model_hash,
            architecture_hash=architecture_hash,
            hyperparameters_hash=hyperparameters_hash,
            dataset_hash=dataset_hash,
            code_hash=code_hash,
            environment_hash=environment_hash,
            source=source,
            parent_ids=parent_ids or [],
        )
        
        return fingerprint
    
    def _hash_model(self, model: torch.nn.Module) -> str:
        """
        Generate a hash of model weights.
        
        Args:
            model: PyTorch model
            
        Returns:
            Hash string
        """
        hasher = hashlib.sha256()
        
        # Hash model parameters
        for name, param in model.named_parameters():
            if param.requires_grad:
                param_data = param.detach().cpu().numpy().tobytes()
                hasher.update(param_data)
        
        return hasher.hexdigest()
    
    def _hash_architecture(self, model: torch.nn.Module) -> str:
        """
        Generate a hash of model architecture.
        
        Args:
            model: PyTorch model
            
        Returns:
            Hash string
        """
        hasher = hashlib.sha256()
        
        # Convert model to string representation
        model_str = str(model)
        hasher.update(model_str.encode())
        
        return hasher.hexdigest()
    
    def _hash_dict(self, data: Dict[str, Any]) -> str:
        """
        Generate a hash of a dictionary.
        
        Args:
            data: Dictionary to hash
            
        Returns:
            Hash string
        """
        if not data:
            return ""
        
        # Convert to JSON string
        json_str = json.dumps(data, sort_keys=True)
        
        # Generate hash
        hasher = hashlib.sha256()
        hasher.update(json_str.encode())
        
        return hasher.hexdigest()
    
    def _hash_code_files(self, file_paths: List[str]) -> str:
        """
        Generate a hash of code files.
        
        Args:
            file_paths: List of file paths
            
        Returns:
            Hash string
        """
        hasher = hashlib.sha256()
        
        for file_path in file_paths:
            if os.path.exists(file_path):
                try:
                    with open(file_path, "r") as f:
                        content = f.read()
                    
                    # Add file path and content to hash
                    hasher.update(file_path.encode())
                    hasher.update(content.encode())
                
                except Exception as e:
                    logger.warning(f"Error reading file {file_path}: {e}")
        
        return hasher.hexdigest()
    
    def _save_model_data(
        self,
        model_id: str,
        model: torch.nn.Module,
        hyperparameters: Dict[str, Any],
        dataset_info: Dict[str, Any],
        code_files: Optional[List[str]] = None,
        environment_info: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Save model-specific data.
        
        Args:
            model_id: Model ID
            model: PyTorch model
            hyperparameters: Model hyperparameters
            dataset_info: Dataset information
            code_files: List of code files used for training
            environment_info: Environment information
        """
        model_dir = os.path.join(self.storage_dir, "models", model_id)
        os.makedirs(model_dir, exist_ok=True)
        
        try:
            # Save model architecture
            architecture_file = os.path.join(model_dir, "architecture.txt")
            with open(architecture_file, "w") as f:
                f.write(str(model))
            
            # Save hyperparameters
            hyperparameters_file = os.path.join(model_dir, "hyperparameters.json")
            with open(hyperparameters_file, "w") as f:
                json.dump(hyperparameters, f, indent=2)
            
            # Save dataset info
            dataset_file = os.path.join(model_dir, "dataset_info.json")
            with open(dataset_file, "w") as f:
                json.dump(dataset_info, f, indent=2)
            
            # Save environment info
            if environment_info:
                environment_file = os.path.join(model_dir, "environment_info.json")
                with open(environment_file, "w") as f:
                    json.dump(environment_info, f, indent=2)
            
            # Save code files
            if code_files:
                code_dir = os.path.join(model_dir, "code")
                os.makedirs(code_dir, exist_ok=True)
                
                for file_path in code_files:
                    if os.path.exists(file_path):
                        try:
                            # Get relative path for saving
                            file_name = os.path.basename(file_path)
                            dest_path = os.path.join(code_dir, file_name)
                            
                            # Copy file
                            with open(file_path, "r") as src, open(dest_path, "w") as dest:
                                dest.write(src.read())
                        
                        except Exception as e:
                            logger.warning(f"Error copying file {file_path}: {e}")
        
        except Exception as e:
            logger.error(f"Error saving model data for {model_id}: {e}")
            logger.error(traceback.format_exc())
    
    def register_change(
        self,
        from_id: str,
        to_id: str,
        change_type: ChangeType,
        significance: ChangeSignificance,
        description: str,
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Register a change between models.
        
        Args:
            from_id: Source model ID
            to_id: Target model ID
            change_type: Type of change
            significance: Significance of change
            description: Description of change
            details: Detailed information about the change
        """
        # Check if models exist
        if from_id not in self.models:
            logger.warning(f"Source model {from_id} not found")
            return
        
        if to_id not in self.models:
            logger.warning(f"Target model {to_id} not found")
            return
        
        # Create change
        change = ModelChange(
            from_id=from_id,
            to_id=to_id,
            type=change_type,
            significance=significance,
            description=description,
            details=details or {},
        )
        
        # Add to changes
        self.changes.append(change)
        
        # Save data
        self._save_data()
        
        # Save change-specific data
        self._save_change_data(change)
        
        logger.info(f"Registered change from {from_id} to {to_id} of type {change_type.value}")
    
    def _save_change_data(self, change: ModelChange) -> None:
        """
        Save change-specific data.
        
        Args:
            change: Model change
        """
        change_dir = os.path.join(self.storage_dir, "changes", f"{change.from_id}_{change.to_id}")
        os.makedirs(change_dir, exist_ok=True)
        
        try:
            # Save change details
            change_file = os.path.join(change_dir, "change.json")
            with open(change_file, "w") as f:
                json.dump(change.to_dict(), f, indent=2)
            
            # Save additional details
            if change.details:
                details_file = os.path.join(change_dir, "details.json")
                with open(details_file, "w") as f:
                    json.dump(change.details, f, indent=2)
            
            # Generate diff if both models have code files
            from_model = self.models.get(change.from_id)
            to_model = self.models.get(change.to_id)
            
            if from_model and to_model:
                from_code_dir = os.path.join(self.storage_dir, "models", change.from_id, "code")
                to_code_dir = os.path.join(self.storage_dir, "models", change.to_id, "code")
                
                if os.path.exists(from_code_dir) and os.path.exists(to_code_dir):
                    diff_dir = os.path.join(change_dir, "diffs")
                    os.makedirs(diff_dir, exist_ok=True)
                    
                    # Get list of files in both directories
                    from_files = set(os.listdir(from_code_dir))
                    to_files = set(os.listdir(to_code_dir))
                    
                    # Generate diffs for common files
                    for file_name in from_files.intersection(to_files):
                        from_file = os.path.join(from_code_dir, file_name)
                        to_file = os.path.join(to_code_dir, file_name)
                        
                        try:
                            with open(from_file, "r") as f:
                                from_lines = f.readlines()
                            
                            with open(to_file, "r") as f:
                                to_lines = f.readlines()
                            
                            # Generate diff
                            diff = difflib.unified_diff(
                                from_lines,
                                to_lines,
                                fromfile=f"a/{file_name}",
                                tofile=f"b/{file_name}",
                                lineterm="",
                            )
                            
                            # Save diff
                            diff_file = os.path.join(diff_dir, f"{file_name}.diff")
                            with open(diff_file, "w") as f:
                                f.write("\n".join(diff))
                        
                        except Exception as e:
                            logger.warning(f"Error generating diff for {file_name}: {e}")
        
        except Exception as e:
            logger.error(f"Error saving change data for {change.from_id} to {change.to_id}: {e}")
            logger.error(traceback.format_exc())
    
    def detect_changes(
        self,
        from_id: str,
        to_id: str,
    ) -> List[ModelChange]:
        """
        Detect changes between models.
        
        Args:
            from_id: Source model ID
            to_id: Target model ID
            
        Returns:
            List of detected changes
        """
        # Check if models exist
        if from_id not in self.models:
            logger.warning(f"Source model {from_id} not found")
            return []
        
        if to_id not in self.models:
            logger.warning(f"Target model {to_id} not found")
            return []
        
        from_model = self.models[from_id]
        to_model = self.models[to_id]
        
        changes = []
        
        # Check architecture changes
        if from_model.fingerprint.architecture_hash != to_model.fingerprint.architecture_hash:
            changes.append(ModelChange(
                from_id=from_id,
                to_id=to_id,
                type=ChangeType.ARCHITECTURE,
                significance=ChangeSignificance.MAJOR,
                description="Model architecture changed",
                details={"from_hash": from_model.fingerprint.architecture_hash, "to_hash": to_model.fingerprint.architecture_hash},
            ))
        
        # Check hyperparameters changes
        if from_model.fingerprint.hyperparameters_hash != to_model.fingerprint.hyperparameters_hash:
            changes.append(ModelChange(
                from_id=from_id,
                to_id=to_id,
                type=ChangeType.HYPERPARAMETERS,
                significance=ChangeSignificance.MINOR,
                description="Hyperparameters changed",
                details={"from_hash": from_model.fingerprint.hyperparameters_hash, "to_hash": to_model.fingerprint.hyperparameters_hash},
            ))
        
        # Check weights changes
        if from_model.fingerprint.hash != to_model.fingerprint.hash:
            changes.append(ModelChange(
                from_id=from_id,
                to_id=to_id,
                type=ChangeType.WEIGHTS,
                significance=ChangeSignificance.PATCH,
                description="Model weights changed",
                details={"from_hash": from_model.fingerprint.hash, "to_hash": to_model.fingerprint.hash},
            ))
        
        # Check dataset changes
        if from_model.fingerprint.dataset_hash != to_model.fingerprint.dataset_hash:
            changes.append(ModelChange(
                from_id=from_id,
                to_id=to_id,
                type=ChangeType.DATASET,
                significance=ChangeSignificance.MINOR,
                description="Dataset changed",
                details={"from_hash": from_model.fingerprint.dataset_hash, "to_hash": to_model.fingerprint.dataset_hash},
            ))
        
        # Check code changes
        if from_model.fingerprint.code_hash and to_model.fingerprint.code_hash and from_model.fingerprint.code_hash != to_model.fingerprint.code_hash:
            changes.append(ModelChange(
                from_id=from_id,
                to_id=to_id,
                type=ChangeType.TRAINING_CODE,
                significance=ChangeSignificance.MINOR,
                description="Training code changed",
                details={"from_hash": from_model.fingerprint.code_hash, "to_hash": to_model.fingerprint.code_hash},
            ))
        
        # Check environment changes
        if from_model.fingerprint.environment_hash and to_model.fingerprint.environment_hash and from_model.fingerprint.environment_hash != to_model.fingerprint.environment_hash:
            changes.append(ModelChange(
                from_id=from_id,
                to_id=to_id,
                type=ChangeType.ENVIRONMENT,
                significance=ChangeSignificance.PATCH,
                description="Environment changed",
                details={"from_hash": from_model.fingerprint.environment_hash, "to_hash": to_model.fingerprint.environment_hash},
            ))
        
        return changes
    
    def get_model(self, model_id: str) -> Optional[ModelRecord]:
        """
        Get a model record.
        
        Args:
            model_id: Model ID
            
        Returns:
            Model record or None if not found
        """
        return self.models.get(model_id)
    
    def get_current_model(self) -> Optional[ModelRecord]:
        """
        Get the current model record.
        
        Returns:
            Current model record or None if not set
        """
        if self.current_model_id:
            return self.models.get(self.current_model_id)
        return None
    
    def set_current_model(self, model_id: str) -> bool:
        """
        Set the current model.
        
        Args:
            model_id: Model ID
            
        Returns:
            True if successful, False otherwise
        """
        if model_id in self.models:
            self.current_model_id = model_id
            self._save_data()
            logger.info(f"Set current model to {model_id}")
            return True
        
        logger.warning(f"Model {model_id} not found")
        return False
    
    def get_parents(self, model_id: str) -> List[str]:
        """
        Get parent models.
        
        Args:
            model_id: Model ID
            
        Returns:
            List of parent model IDs
        """
        if model_id not in self.models:
            return []
        
        parents = []
        
        # Check relationships
        for other_id, relationship in self.relationships.get(model_id, {}).items():
            if relationship == ModelRelationship.PARENT:
                parents.append(other_id)
        
        # Check fingerprint
        model = self.models[model_id]
        for parent_id in model.fingerprint.parent_ids:
            if parent_id not in parents and parent_id in self.models:
                parents.append(parent_id)
        
        return parents
    
    def get_children(self, model_id: str) -> List[str]:
        """
        Get child models.
        
        Args:
            model_id: Model ID
            
        Returns:
            List of child model IDs
        """
        if model_id not in self.models:
            return []
        
        children = []
        
        # Check relationships
        for other_id, relationship in self.relationships.get(model_id, {}).items():
            if relationship == ModelRelationship.CHILD:
                children.append(other_id)
        
        # Check fingerprints
        for other_id, model in self.models.items():
            if model_id in model.fingerprint.parent_ids and other_id not in children:
                children.append(other_id)
        
        return children
    
    def get_siblings(self, model_id: str) -> List[str]:
        """
        Get sibling models.
        
        Args:
            model_id: Model ID
            
        Returns:
            List of sibling model IDs
        """
        if model_id not in self.models:
            return []
        
        siblings = []
        
        # Check relationships
        for other_id, relationship in self.relationships.get(model_id, {}).items():
            if relationship == ModelRelationship.SIBLING:
                siblings.append(other_id)
        
        # Check parents
        parents = self.get_parents(model_id)
        for parent_id in parents:
            for child_id in self.get_children(parent_id):
                if child_id != model_id and child_id not in siblings:
                    siblings.append(child_id)
        
        return siblings
    
    def get_ancestors(self, model_id: str, max_depth: int = 10) -> List[str]:
        """
        Get ancestor models.
        
        Args:
            model_id: Model ID
            max_depth: Maximum depth to search
            
        Returns:
            List of ancestor model IDs
        """
        if model_id not in self.models or max_depth <= 0:
            return []
        
        ancestors = []
        visited = set()
        queue = deque([(model_id, 0)])
        
        while queue:
            current_id, depth = queue.popleft()
            
            if current_id in visited:
                continue
            
            visited.add(current_id)
            
            if depth > 0:  # Don't include the starting model
                ancestors.append(current_id)
            
            if depth < max_depth:
                parents = self.get_parents(current_id)
                for parent_id in parents:
                    if parent_id not in visited:
                        queue.append((parent_id, depth + 1))
        
        return ancestors
    
    def get_descendants(self, model_id: str, max_depth: int = 10) -> List[str]:
        """
        Get descendant models.
        
        Args:
            model_id: Model ID
            max_depth: Maximum depth to search
            
        Returns:
            List of descendant model IDs
        """
        if model_id not in self.models or max_depth <= 0:
            return []
        
        descendants = []
        visited = set()
        queue = deque([(model_id, 0)])
        
        while queue:
            current_id, depth = queue.popleft()
            
            if current_id in visited:
                continue
            
            visited.add(current_id)
            
            if depth > 0:  # Don't include the starting model
                descendants.append(current_id)
            
            if depth < max_depth:
                children = self.get_children(current_id)
                for child_id in children:
                    if child_id not in visited:
                        queue.append((child_id, depth + 1))
        
        return descendants
    
    def get_changes(
        self,
        model_id: Optional[str] = None,
        change_type: Optional[ChangeType] = None,
        significance: Optional[ChangeSignificance] = None,
    ) -> List[ModelChange]:
        """
        Get changes.
        
        Args:
            model_id: Filter by model ID (source or target)
            change_type: Filter by change type
            significance: Filter by significance
            
        Returns:
            List of changes
        """
        filtered_changes = self.changes
        
        # Filter by model ID
        if model_id:
            filtered_changes = [
                change for change in filtered_changes
                if change.from_id == model_id or change.to_id == model_id
            ]
        
        # Filter by change type
        if change_type:
            filtered_changes = [
                change for change in filtered_changes
                if change.type == change_type
            ]
        
        # Filter by significance
        if significance:
            filtered_changes = [
                change for change in filtered_changes
                if change.significance == significance
            ]
        
        return filtered_changes
    
    def get_lineage(self, model_id: str, max_depth: int = 10) -> Dict[str, Any]:
        """
        Get model lineage.
        
        Args:
            model_id: Model ID
            max_depth: Maximum depth to search
            
        Returns:
            Lineage information
        """
        if model_id not in self.models:
            return {}
        
        # Get ancestors and descendants
        ancestors = self.get_ancestors(model_id, max_depth)
        descendants = self.get_descendants(model_id, max_depth)
        
        # Get siblings
        siblings = self.get_siblings(model_id)
        
        # Get changes
        changes = self.get_changes(model_id)
        
        # Build lineage graph
        graph = {
            "model_id": model_id,
            "ancestors": ancestors,
            "descendants": descendants,
            "siblings": siblings,
            "changes": [change.to_dict() for change in changes],
            "graph": self._build_lineage_graph(model_id, ancestors, descendants, siblings),
        }
        
        return graph
    
    def _build_lineage_graph(
        self,
        model_id: str,
        ancestors: List[str],
        descendants: List[str],
        siblings: List[str],
    ) -> Dict[str, Any]:
        """
        Build lineage graph.
        
        Args:
            model_id: Model ID
            ancestors: List of ancestor model IDs
            descendants: List of descendant model IDs
            siblings: List of sibling model IDs
            
        Returns:
            Graph data
        """
        # Create graph
        graph = {
            "nodes": [],
            "edges": [],
        }
        
        # Add nodes
        all_models = set([model_id] + ancestors + descendants + siblings)
        
        for node_id in all_models:
            if node_id in self.models:
                model = self.models[node_id]
                
                # Determine node type
                node_type = "current" if node_id == model_id else (
                    "ancestor" if node_id in ancestors else (
                        "descendant" if node_id in descendants else (
                            "sibling" if node_id in siblings else "other"
                        )
                    )
                )
                
                # Add node
                graph["nodes"].append({
                    "id": node_id,
                    "type": node_type,
                    "name": model.metadata.name or f"Model {node_id[:8]}",
                    "source": model.fingerprint.source.value,
                    "timestamp": model.fingerprint.timestamp,
                })
        
        # Add edges
        for node_id in all_models:
            # Add parent-child edges
            parents = self.get_parents(node_id)
            for parent_id in parents:
                if parent_id in all_models:
                    # Get changes
                    changes = [
                        change for change in self.changes
                        if change.from_id == parent_id and change.to_id == node_id
                    ]
                    
                    # Add edge
                    graph["edges"].append({
                        "source": parent_id,
                        "target": node_id,
                        "type": "parent-child",
                        "changes": [change.to_dict() for change in changes],
                    })
        
        return graph
    
    def visualize_lineage(
        self,
        model_id: Optional[str] = None,
        max_depth: int = 3,
        output_path: Optional[str] = None,
        show_changes: bool = True,
        show_timestamps: bool = True,
    ) -> Optional[str]:
        """
        Visualize model lineage.
        
        Args:
            model_id: Model ID (uses current model if None)
            max_depth: Maximum depth to visualize
            output_path: Path to save the visualization
            show_changes: Whether to show changes on edges
            show_timestamps: Whether to show timestamps on nodes
            
        Returns:
            Path to the saved visualization or None
        """
        # Use current model if not specified
        if model_id is None:
            model_id = self.current_model_id
        
        if not model_id or model_id not in self.models:
            logger.warning(f"Model {model_id} not found")
            return None
        
        try:
            # Get lineage
            lineage = self.get_lineage(model_id, max_depth)
            
            # Create graph
            G = nx.DiGraph()
            
            # Add nodes
            for node in lineage["graph"]["nodes"]:
                G.add_node(
                    node["id"],
                    type=node["type"],
                    name=node["name"],
                    source=node["source"],
                    timestamp=node["timestamp"],
                )
            
            # Add edges
            for edge in lineage["graph"]["edges"]:
                G.add_edge(
                    edge["source"],
                    edge["target"],
                    type=edge["type"],
                    changes=edge["changes"],
                )
            
            # Create figure
            plt.figure(figsize=(12, 8))
            
            # Define node colors
            node_colors = {
                "current": "red",
                "ancestor": "blue",
                "descendant": "green",
                "sibling": "orange",
                "other": "gray",
            }
            
            # Define node positions
            pos = nx.spring_layout(G, seed=42)
            
            # Draw nodes
            for node_type, color in node_colors.items():
                nodes = [n for n, data in G.nodes(data=True) if data["type"] == node_type]
                if nodes:
                    nx.draw_networkx_nodes(
                        G,
                        pos,
                        nodelist=nodes,
                        node_color=color,
                        node_size=500,
                        alpha=0.8,
                    )
            
            # Draw edges
            nx.draw_networkx_edges(
                G,
                pos,
                width=1.0,
                alpha=0.5,
                arrowsize=20,
                arrowstyle="-|>",
            )
            
            # Draw labels
            labels = {}
            for node, data in G.nodes(data=True):
                label = data["name"]
                if show_timestamps:
                    timestamp = datetime.datetime.fromtimestamp(data["timestamp"]).strftime("%Y-%m-%d")
                    label += f"\n({timestamp})"
                labels[node] = label
            
            nx.draw_networkx_labels(
                G,
                pos,
                labels=labels,
                font_size=8,
                font_family="sans-serif",
            )
            
            # Draw edge labels if showing changes
            if show_changes:
                edge_labels = {}
                for u, v, data in G.edges(data=True):
                    if "changes" in data and data["changes"]:
                        # Get most significant change
                        changes = data["changes"]
                        if changes:
                            change = changes[0]  # Just use the first change for simplicity
                            edge_labels[(u, v)] = f"{change['type']}\n{change['significance']}"
                
                nx.draw_networkx_edge_labels(
                    G,
                    pos,
                    edge_labels=edge_labels,
                    font_size=6,
                )
            
            # Add legend
            legend_elements = [
                Line2D([0], [0], marker='o', color='w', markerfacecolor=color, markersize=10, label=node_type)
                for node_type, color in node_colors.items()
            ]
            
            plt.legend(handles=legend_elements, loc="upper right")
            
            # Remove axis
            plt.axis("off")
            
            # Add title
            model = self.models[model_id]
            title = f"Model Lineage: {model.metadata.name or model_id[:8]}"
            plt.title(title)
            
            # Save or show
            if output_path:
                plt.savefig(output_path, bbox_inches="tight", dpi=300)
                logger.info(f"Saved lineage visualization to {output_path}")
                plt.close()
                return output_path
            else:
                plt.tight_layout()
                plt.show()
                plt.close()
                return None
        
        except Exception as e:
            logger.error(f"Error visualizing lineage: {e}")
            logger.error(traceback.format_exc())
            return None
    
    def visualize_evolution(
        self,
        metric_name: str,
        output_path: Optional[str] = None,
        max_models: int = 20,
        show_changes: bool = True,
    ) -> Optional[str]:
        """
        Visualize model evolution based on a metric.
        
        Args:
            metric_name: Name of the metric to visualize
            output_path: Path to save the visualization
            max_models: Maximum number of models to include
            show_changes: Whether to show changes between models
            
        Returns:
            Path to the saved visualization or None
        """
        try:
            # Get models with the metric
            models_with_metric = []
            
            for model_id, model in self.models.items():
                if metric_name in model.metadata.metrics:
                    models_with_metric.append((model_id, model))
            
            if not models_with_metric:
                logger.warning(f"No models found with metric {metric_name}")
                return None
            
            # Sort by timestamp
            models_with_metric.sort(key=lambda x: x[1].fingerprint.timestamp)
            
            # Limit to max_models
            if len(models_with_metric) > max_models:
                # Keep first, last, and evenly spaced models in between
                first = models_with_metric[0]
                last = models_with_metric[-1]
                
                if max_models > 2:
                    step = (len(models_with_metric) - 2) // (max_models - 2)
                    middle = models_with_metric[1:-1:step][:max_models - 2]
                    models_with_metric = [first] + middle + [last]
                else:
                    models_with_metric = [first, last]
            
            # Extract data
            model_ids = [model_id for model_id, _ in models_with_metric]
            model_names = [model.metadata.name or model_id[:8] for model_id, model in models_with_metric]
            metric_values = [model.metadata.metrics[metric_name] for _, model in models_with_metric]
            timestamps = [model.fingerprint.timestamp for _, model in models_with_metric]
            
            # Convert timestamps to datetime
            dates = [datetime.datetime.fromtimestamp(ts) for ts in timestamps]
            
            # Create figure
            plt.figure(figsize=(12, 6))
            
            # Plot metric values
            plt.plot(dates, metric_values, marker='o', linestyle='-', linewidth=2, markersize=8)
            
            # Add labels
            plt.xlabel("Date")
            plt.ylabel(metric_name)
            plt.title(f"Model Evolution: {metric_name}")
            
            # Format x-axis
            plt.gcf().autofmt_xdate()
            
            # Add grid
            plt.grid(True, linestyle='--', alpha=0.7)
            
            # Add model names as annotations
            for i, (date, value, name) in enumerate(zip(dates, metric_values, model_names)):
                plt.annotate(
                    name,
                    (date, value),
                    textcoords="offset points",
                    xytext=(0, 10),
                    ha='center',
                    fontsize=8,
                )
            
            # Add changes if requested
            if show_changes and len(model_ids) > 1:
                # Get changes between consecutive models
                for i in range(len(model_ids) - 1):
                    from_id = model_ids[i]
                    to_id = model_ids[i + 1]
                    
                    changes = self.get_changes(from_id)
                    changes = [change for change in changes if change.to_id == to_id]
                    
                    if changes:
                        # Add change annotations
                        change_text = "\n".join([f"{change.type.value}" for change in changes[:3]])
                        if len(changes) > 3:
                            change_text += f"\n+{len(changes) - 3} more"
                        
                        plt.annotate(
                            change_text,
                            ((dates[i] + dates[i + 1]) / 2, (metric_values[i] + metric_values[i + 1]) / 2),
                            textcoords="offset points",
                            xytext=(0, -30),
                            ha='center',
                            fontsize=7,
                            bbox=dict(boxstyle="round,pad=0.3", fc="yellow", alpha=0.3),
                        )
            
            # Save or show
            if output_path:
                plt.savefig(output_path, bbox_inches="tight", dpi=300)
                logger.info(f"Saved evolution visualization to {output_path}")
                plt.close()
                return output_path
            else:
                plt.tight_layout()
                plt.show()
                plt.close()
                return None
        
        except Exception as e:
            logger.error(f"Error visualizing evolution: {e}")
            logger.error(traceback.format_exc())
            return None
    
    def visualize_parameter_changes(
        self,
        from_id: str,
        to_id: str,
        output_path: Optional[str] = None,
    ) -> Optional[str]:
        """
        Visualize parameter changes between models.
        
        Args:
            from_id: Source model ID
            to_id: Target model ID
            output_path: Path to save the visualization
            
        Returns:
            Path to the saved visualization or None
        """
        try:
            # Check if models exist
            if from_id not in self.models:
                logger.warning(f"Source model {from_id} not found")
                return None
            
            if to_id not in self.models:
                logger.warning(f"Target model {to_id} not found")
                return None
            
            # Get hyperparameters
            from_model = self.models[from_id]
            to_model = self.models[to_id]
            
            from_hyperparams_file = os.path.join(self.storage_dir, "models", from_id, "hyperparameters.json")
            to_hyperparams_file = os.path.join(self.storage_dir, "models", to_id, "hyperparameters.json")
            
            if not os.path.exists(from_hyperparams_file) or not os.path.exists(to_hyperparams_file):
                logger.warning("Hyperparameters files not found")
                return None
            
            with open(from_hyperparams_file, "r") as f:
                from_hyperparams = json.load(f)
            
            with open(to_hyperparams_file, "r") as f:
                to_hyperparams = json.load(f)
            
            # Find common parameters
            common_params = set(from_hyperparams.keys()).intersection(set(to_hyperparams.keys()))
            
            # Find changed parameters
            changed_params = []
            
            for param in common_params:
                if from_hyperparams[param] != to_hyperparams[param]:
                    changed_params.append(param)
            
            # Find added and removed parameters
            added_params = set(to_hyperparams.keys()) - set(from_hyperparams.keys())
            removed_params = set(from_hyperparams.keys()) - set(to_hyperparams.keys())
            
            # Create figure
            plt.figure(figsize=(12, 8))
            
            # Create subplots
            fig, axs = plt.subplots(2, 2, figsize=(15, 10))
            
            # Plot changed parameters
            if changed_params:
                ax = axs[0, 0]
                
                # Convert parameters to numeric if possible
                numeric_params = []
                for param in changed_params:
                    try:
                        from_value = float(from_hyperparams[param])
                        to_value = float(to_hyperparams[param])
                        numeric_params.append((param, from_value, to_value))
                    except (ValueError, TypeError):
                        pass
                
                if numeric_params:
                    params = [p[0] for p in numeric_params]
                    from_values = [p[1] for p in numeric_params]
                    to_values = [p[2] for p in numeric_params]
                    
                    x = np.arange(len(params))
                    width = 0.35
                    
                    ax.bar(x - width/2, from_values, width, label=f'From: {from_model.metadata.name or from_id[:8]}')
                    ax.bar(x + width/2, to_values, width, label=f'To: {to_model.metadata.name or to_id[:8]}')
                    
                    ax.set_ylabel('Value')
                    ax.set_title('Changed Numeric Parameters')
                    ax.set_xticks(x)
                    ax.set_xticklabels(params, rotation=45, ha='right')
                    ax.legend()
                else:
                    ax.text(0.5, 0.5, "No numeric parameters changed", ha='center', va='center')
                    ax.axis('off')
            else:
                axs[0, 0].text(0.5, 0.5, "No parameters changed", ha='center', va='center')
                axs[0, 0].axis('off')
            
            # Plot parameter change percentages
            if numeric_params:
                ax = axs[0, 1]
                
                params = [p[0] for p in numeric_params]
                from_values = np.array([p[1] for p in numeric_params])
                to_values = np.array([p[2] for p in numeric_params])
                
                # Calculate percentage changes
                pct_changes = []
                for i, (param, from_value, to_value) in enumerate(numeric_params):
                    if from_value != 0:
                        pct_change = (to_value - from_value) / abs(from_value) * 100
                    else:
                        pct_change = float('inf') if to_value > 0 else float('-inf') if to_value < 0 else 0
                    
                    # Cap extreme values for visualization
                    if pct_change > 1000:
                        pct_change = 1000
                    elif pct_change < -1000:
                        pct_change = -1000
                    
                    pct_changes.append(pct_change)
                
                x = np.arange(len(params))
                
                colors = ['green' if pct > 0 else 'red' for pct in pct_changes]
                
                ax.bar(x, pct_changes, color=colors)
                
                ax.set_ylabel('Percentage Change (%)')
                ax.set_title('Parameter Change Percentages')
                ax.set_xticks(x)
                ax.set_xticklabels(params, rotation=45, ha='right')
                ax.axhline(y=0, color='k', linestyle='-', alpha=0.3)
                ax.grid(axis='y', linestyle='--', alpha=0.3)
            else:
                axs[0, 1].text(0.5, 0.5, "No numeric parameters to compare", ha='center', va='center')
                axs[0, 1].axis('off')
            
            # Plot added parameters
            ax = axs[1, 0]
            if added_params:
                ax.text(0.5, 0.9, "Added Parameters:", ha='center', va='center', fontweight='bold')
                
                for i, param in enumerate(sorted(added_params)):
                    value = to_hyperparams[param]
                    value_str = str(value)
                    if len(value_str) > 50:
                        value_str = value_str[:47] + "..."
                    
                    ax.text(0.1, 0.8 - i * 0.1, f"{param}: {value_str}", ha='left', va='center', fontsize=9)
                    
                    if i >= 7:  # Limit to 8 parameters
                        ax.text(0.1, 0.8 - 8 * 0.1, f"... and {len(added_params) - 8} more", ha='left', va='center', fontsize=9)
                        break
            else:
                ax.text(0.5, 0.5, "No parameters added", ha='center', va='center')
            
            ax.axis('off')
            ax.set_title('Added Parameters')
            
            # Plot removed parameters
            ax = axs[1, 1]
            if removed_params:
                ax.text(0.5, 0.9, "Removed Parameters:", ha='center', va='center', fontweight='bold')
                
                for i, param in enumerate(sorted(removed_params)):
                    value = from_hyperparams[param]
                    value_str = str(value)
                    if len(value_str) > 50:
                        value_str = value_str[:47] + "..."
                    
                    ax.text(0.1, 0.8 - i * 0.1, f"{param}: {value_str}", ha='left', va='center', fontsize=9)
                    
                    if i >= 7:  # Limit to 8 parameters
                        ax.text(0.1, 0.8 - 8 * 0.1, f"... and {len(removed_params) - 8} more", ha='left', va='center', fontsize=9)
                        break
            else:
                ax.text(0.5, 0.5, "No parameters removed", ha='center', va='center')
            
            ax.axis('off')
            ax.set_title('Removed Parameters')
            
            # Add title
            from_name = from_model.metadata.name or from_id[:8]
            to_name = to_model.metadata.name or to_id[:8]
            fig.suptitle(f'Parameter Changes: {from_name} → {to_name}', fontsize=16)
            
            # Adjust layout
            plt.tight_layout(rect=[0, 0, 1, 0.95])
            
            # Save or show
            if output_path:
                plt.savefig(output_path, bbox_inches="tight", dpi=300)
                logger.info(f"Saved parameter changes visualization to {output_path}")
                plt.close(fig)
                return output_path
            else:
                plt.show()
                plt.close(fig)
                return None
        
        except Exception as e:
            logger.error(f"Error visualizing parameter changes: {e}")
            logger.error(traceback.format_exc())
            return None
    
    def export_lineage(self, model_id: str, output_path: str, max_depth: int = 10) -> bool:
        """
        Export model lineage to a file.
        
        Args:
            model_id: Model ID
            output_path: Path to save the lineage
            max_depth: Maximum depth to export
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Get lineage
            lineage = self.get_lineage(model_id, max_depth)
            
            # Save to file
            with open(output_path, "w") as f:
                json.dump(lineage, f, indent=2)
            
            logger.info(f"Exported lineage for model {model_id} to {output_path}")
            return True
        
        except Exception as e:
            logger.error(f"Error exporting lineage: {e}")
            logger.error(traceback.format_exc())
            return False
    
    def import_lineage(self, input_path: str) -> Optional[str]:
        """
        Import model lineage from a file.
        
        Args:
            input_path: Path to the lineage file
            
        Returns:
            Imported model ID or None if failed
        """
        try:
            # Load from file
            with open(input_path, "r") as f:
                lineage = json.load(f)
            
            # Get model ID
            model_id = lineage.get("model_id")
            
            if not model_id:
                logger.warning("No model ID found in lineage file")
                return None
            
            # Import models
            for node in lineage["graph"]["nodes"]:
                node_id = node["id"]
                
                # Skip if model already exists
                if node_id in self.models:
                    continue
                
                # Create model fingerprint
                fingerprint = ModelFingerprint(
                    id=node_id,
                    timestamp=node["timestamp"],
                    source=ModelSource(node["source"]),
                )
                
                # Create model metadata
                metadata = ModelMetadata(
                    name=node["name"],
                )
                
                # Create model record
                model_record = ModelRecord(
                    fingerprint=fingerprint,
                    metadata=metadata,
                )
                
                # Add to models
                self.models[node_id] = model_record
            
            # Import relationships
            for edge in lineage["graph"]["edges"]:
                from_id = edge["source"]
                to_id = edge["target"]
                
                # Add relationship
                self.relationships[from_id][to_id] = ModelRelationship.CHILD
                self.relationships[to_id][from_id] = ModelRelationship.PARENT
                
                # Import changes
                for change_data in edge.get("changes", []):
                    change = ModelChange.from_dict(change_data)
                    self.changes.append(change)
            
            # Save data
            self._save_data()
            
            logger.info(f"Imported lineage with model {model_id} from {input_path}")
            return model_id
        
        except Exception as e:
            logger.error(f"Error importing lineage: {e}")
            logger.error(traceback.format_exc())
            return None
    
    def generate_lineage_report(self, model_id: str, output_path: str, max_depth: int = 3) -> bool:
        """
        Generate a detailed lineage report.
        
        Args:
            model_id: Model ID
            output_path: Path to save the report
            max_depth: Maximum depth to include
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Check if model exists
            if model_id not in self.models:
                logger.warning(f"Model {model_id} not found")
                return False
            
            # Get model
            model = self.models[model_id]
            
            # Get lineage
            lineage = self.get_lineage(model_id, max_depth)
            
            # Generate report
            report = []
            
            # Add header
            report.append("# Model Lineage Report")
            report.append("")
            
            # Add model information
            report.append(f"## Model: {model.metadata.name or model_id}")
            report.append("")
            report.append(f"- **ID:** {model_id}")
            report.append(f"- **Source:** {model.fingerprint.source.value}")
            report.append(f"- **Created:** {datetime.datetime.fromtimestamp(model.fingerprint.timestamp).strftime('%Y-%m-%d %H:%M:%S')}")
            
            if model.metadata.description:
                report.append(f"- **Description:** {model.metadata.description}")
            
            if model.metadata.version:
                report.append(f"- **Version:** {model.metadata.version}")
            
            if model.metadata.tags:
                report.append(f"- **Tags:** {', '.join(model.metadata.tags)}")
            
            report.append("")
            
            # Add metrics
            if model.metadata.metrics:
                report.append("### Metrics")
                report.append("")
                
                for metric, value in model.metadata.metrics.items():
                    report.append(f"- **{metric}:** {value}")
                
                report.append("")
            
            # Add parents
            parents = self.get_parents(model_id)
            if parents:
                report.append("### Parents")
                report.append("")
                
                for parent_id in parents:
                    parent = self.models.get(parent_id)
                    if parent:
                        report.append(f"- **{parent.metadata.name or parent_id}** ({parent_id})")
                        
                        # Add changes from parent
                        changes = [
                            change for change in self.changes
                            if change.from_id == parent_id and change.to_id == model_id
                        ]
                        
                        if changes:
                            report.append("  - Changes:")
                            for change in changes:
                                report.append(f"    - {change.type.value} ({change.significance.value}): {change.description}")
                
                report.append("")
            
            # Add children
            children = self.get_children(model_id)
            if children:
                report.append("### Children")
                report.append("")
                
                for child_id in children:
                    child = self.models.get(child_id)
                    if child:
                        report.append(f"- **{child.metadata.name or child_id}** ({child_id})")
                        
                        # Add changes to child
                        changes = [
                            change for change in self.changes
                            if change.from_id == model_id and change.to_id == child_id
                        ]
                        
                        if changes:
                            report.append("  - Changes:")
                            for change in changes:
                                report.append(f"    - {change.type.value} ({change.significance.value}): {change.description}")
                
                report.append("")
            
            # Add siblings
            siblings = self.get_siblings(model_id)
            if siblings:
                report.append("### Siblings")
                report.append("")
                
                for sibling_id in siblings:
                    sibling = self.models.get(sibling_id)
                    if sibling:
                        report.append(f"- **{sibling.metadata.name or sibling_id}** ({sibling_id})")
                
                report.append("")
            
            # Add ancestors
            ancestors = self.get_ancestors(model_id, max_depth)
            if ancestors:
                report.append("### Ancestors")
                report.append("")
                
                for ancestor_id in ancestors:
                    ancestor = self.models.get(ancestor_id)
                    if ancestor:
                        report.append(f"- **{ancestor.metadata.name or ancestor_id}** ({ancestor_id})")
                
                report.append("")
            
            # Add descendants
            descendants = self.get_descendants(model_id, max_depth)
            if descendants:
                report.append("### Descendants")
                report.append("")
                
                for descendant_id in descendants:
                    descendant = self.models.get(descendant_id)
                    if descendant:
                        report.append(f"- **{descendant.metadata.name or descendant_id}** ({descendant_id})")
                
                report.append("")
            
            # Add lineage visualization
            vis_path = os.path.join(self.storage_dir, "visualizations", f"lineage_{model_id}.png")
            self.visualize_lineage(model_id, max_depth, vis_path)
            
            if os.path.exists(vis_path):
                report.append("### Lineage Visualization")
                report.append("")
                report.append(f"![Lineage Visualization]({vis_path})")
                report.append("")
            
            # Write report
            with open(output_path, "w") as f:
                f.write("\n".join(report))
            
            logger.info(f"Generated lineage report for model {model_id} at {output_path}")
            return True
        
        except Exception as e:
            logger.error(f"Error generating lineage report: {e}")
            logger.error(traceback.format_exc())
            return False
    
    def clear(self) -> None:
        """Clear all data."""
        self.models = {}
        self.changes = []
        self.relationships = defaultdict(dict)
        self.current_model_id = None
        
        # Save empty data
        self._save_data()
        
        logger.info("Cleared all DNA tracker data")
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get statistics about the tracked models.
        
        Returns:
            Statistics dictionary
        """
        stats = {
            "total_models": len(self.models),
            "total_changes": len(self.changes),
            "models_by_source": defaultdict(int),
            "changes_by_type": defaultdict(int),
            "changes_by_significance": defaultdict(int),
            "avg_children_per_model": 0,
            "max_children": 0,
            "max_children_model": None,
            "avg_parents_per_model": 0,
            "max_parents": 0,
            "max_parents_model": None,
            "max_depth": 0,
            "oldest_model": None,
            "newest_model": None,
        }
        
        # Count models by source
        for model_id, model in self.models.items():
            stats["models_by_source"][model.fingerprint.source.value] += 1
        
        # Count changes by type and significance
        for change in self.changes:
            stats["changes_by_type"][change.type.value] += 1
            stats["changes_by_significance"][change.significance.value] += 1
        
        # Calculate children and parents statistics
        total_children = 0
        total_parents = 0
        
        for model_id in self.models:
            children = self.get_children(model_id)
            parents = self.get_parents(model_id)
            
            total_children += len(children)
            total_parents += len(parents)
            
            if len(children) > stats["max_children"]:
                stats["max_children"] = len(children)
                stats["max_children_model"] = model_id
            
            if len(parents) > stats["max_parents"]:
                stats["max_parents"] = len(parents)
                stats["max_parents_model"] = model_id
        
        if self.models:
            stats["avg_children_per_model"] = total_children / len(self.models)
            stats["avg_parents_per_model"] = total_parents / len(self.models)
        
        # Find oldest and newest models
        if self.models:
            oldest_id = min(self.models.items(), key=lambda x: x[1].fingerprint.timestamp)[0]
            newest_id = max(self.models.items(), key=lambda x: x[1].fingerprint.timestamp)[0]
            
            stats["oldest_model"] = {
                "id": oldest_id,
                "name": self.models[oldest_id].metadata.name or oldest_id,
                "timestamp": self.models[oldest_id].fingerprint.timestamp,
            }
            
            stats["newest_model"] = {
                "id": newest_id,
                "name": self.models[newest_id].metadata.name or newest_id,
                "timestamp": self.models[newest_id].fingerprint.timestamp,
            }
        
        # Calculate maximum depth
        if self.models:
            for model_id in self.models:
                ancestors = self.get_ancestors(model_id, max_depth=100)
                descendants = self.get_descendants(model_id, max_depth=100)
                
                depth = len(ancestors) + len(descendants)
                stats["max_depth"] = max(stats["max_depth"], depth)
        
        return stats
    
    def visualize_statistics(self, output_path: Optional[str] = None) -> Optional[str]:
        """
        Visualize statistics about the tracked models.
        
        Args:
            output_path: Path to save the visualization
            
        Returns:
            Path to the saved visualization or None
        """
        try:
            # Get statistics
            stats = self.get_statistics()
            
            if stats["total_models"] == 0:
                logger.warning("No models to visualize statistics")
                return None
            
            # Create figure
            plt.figure(figsize=(15, 10))
            
            # Create subplots
            fig, axs = plt.subplots(2, 2, figsize=(15, 10))
            
            # Plot models by source
            ax = axs[0, 0]
            if stats["models_by_source"]:
                sources = list(stats["models_by_source"].keys())
                counts = list(stats["models_by_source"].values())
                
                ax.bar(sources, counts)
                ax.set_title("Models by Source")
                ax.set_xlabel("Source")
                ax.set_ylabel("Count")
                ax.set_xticklabels(sources, rotation=45, ha='right')
            else:
                ax.text(0.5, 0.5, "No data", ha='center', va='center')
                ax.axis('off')
            
            # Plot changes by type
            ax = axs[0, 1]
            if stats["changes_by_type"]:
                types = list(stats["changes_by_type"].keys())
                counts = list(stats["changes_by_type"].values())
                
                ax.bar(types, counts)
                ax.set_title("Changes by Type")
                ax.set_xlabel("Type")
                ax.set_ylabel("Count")
                ax.set_xticklabels(types, rotation=45, ha='right')
            else:
                ax.text(0.5, 0.5, "No data", ha='center', va='center')
                ax.axis('off')
            
            # Plot changes by significance
            ax = axs[1, 0]
            if stats["changes_by_significance"]:
                significances = list(stats["changes_by_significance"].keys())
                counts = list(stats["changes_by_significance"].values())
                
                # Sort by significance level
                significance_order = {
                    ChangeSignificance.MAJOR.value: 0,
                    ChangeSignificance.MINOR.value: 1,
                    ChangeSignificance.PATCH.value: 2,
                    ChangeSignificance.EXPERIMENTAL.value: 3,
                    ChangeSignificance.CUSTOM.value: 4,
                }
                
                sorted_indices = sorted(range(len(significances)), key=lambda i: significance_order.get(significances[i], 999))
                sorted_significances = [significances[i] for i in sorted_indices]
                sorted_counts = [counts[i] for i in sorted_indices]
                
                ax.bar(sorted_significances, sorted_counts)
                ax.set_title("Changes by Significance")
                ax.set_xlabel("Significance")
                ax.set_ylabel("Count")
                ax.set_xticklabels(sorted_significances, rotation=45, ha='right')
            else:
                ax.text(0.5, 0.5, "No data", ha='center', va='center')
                ax.axis('off')
            
            # Plot model timeline
            ax = axs[1, 1]
            if stats["oldest_model"] and stats["newest_model"]:
                # Get all models sorted by timestamp
                models = sorted(self.models.items(), key=lambda x: x[1].fingerprint.timestamp)
                timestamps = [model.fingerprint.timestamp for _, model in models]
                names = [model.metadata.name or model_id[:8] for model_id, model in models]
                
                # Convert timestamps to datetime
                dates = [datetime.datetime.fromtimestamp(ts) for ts in timestamps]
                
                # Create timeline
                ax.plot(dates, range(len(dates)), marker='o', linestyle='-', markersize=8)
                
                # Add model names
                for i, (date, name) in enumerate(zip(dates, names)):
                    ax.annotate(
                        name,
                        (date, i),
                        textcoords="offset points",
                        xytext=(10, 0),
                        ha='left',
                        fontsize=8,
                    )
                
                ax.set_title("Model Timeline")
                ax.set_xlabel("Date")
                ax.set_yticks([])
                ax.grid(axis='x', linestyle='--', alpha=0.3)
            else:
                ax.text(0.5, 0.5, "No data", ha='center', va='center')
                ax.axis('off')
            
            # Add title with summary statistics
            title = f"DNA Tracker Statistics\n"
            title += f"Total Models: {stats['total_models']} | "
            title += f"Total Changes: {stats['total_changes']} | "
            title += f"Max Depth: {stats['max_depth']}"
            
            fig.suptitle(title, fontsize=16)
            
            # Adjust layout
            plt.tight_layout(rect=[0, 0, 1, 0.95])
            
            # Save or show
            if output_path:
                plt.savefig(output_path, bbox_inches="tight", dpi=300)
                logger.info(f"Saved statistics visualization to {output_path}")
                plt.close(fig)
                return output_path
            else:
                plt.show()
                plt.close(fig)
                return None
        
        except Exception as e:
            logger.error(f"Error visualizing statistics: {e}")
            logger.error(traceback.format_exc())
            return None
