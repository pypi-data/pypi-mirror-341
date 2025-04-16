"""
Causal Fault Tree Analysis (CFTA) module for AutoPipelineDoctor.

This advanced module traces backward through pipeline and config to identify root causes
of failures or inefficiencies, visualizing causal chains and providing actionable diagnostics.
"""

import torch
import logging
import time
import threading
import inspect
import traceback
import os
import json
import networkx as nx
import matplotlib.pyplot as plt
from typing import Dict, List, Tuple, Optional, Union, Any, Callable, Set
from enum import Enum
import numpy as np
from collections import defaultdict, deque
import re
import copy
import weakref

logger = logging.getLogger(__name__)


class FaultType(Enum):
    """Types of faults that can be detected."""
    MEMORY = "memory_issue"
    PERFORMANCE = "performance_issue"
    CONVERGENCE = "convergence_issue"
    DATALOADER = "dataloader_issue"
    HARDWARE = "hardware_issue"
    CONFIGURATION = "configuration_issue"
    NUMERICAL = "numerical_issue"
    IMPLEMENTATION = "implementation_issue"
    UNKNOWN = "unknown_issue"


class FaultSeverity(Enum):
    """Severity levels for faults."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class CausalNode:
    """
    Node in a causal fault tree.
    
    Attributes:
        id: Unique identifier for the node
        name: Human-readable name
        description: Detailed description
        type: Type of fault
        severity: Severity level
        metrics: Associated metrics
        timestamp: When the node was created
        parent: Parent node
        children: Child nodes
        evidence: Evidence supporting this node
        solutions: Potential solutions
    """
    
    def __init__(
        self,
        id: str,
        name: str,
        description: str,
        type: FaultType,
        severity: FaultSeverity,
        metrics: Optional[Dict[str, Any]] = None,
        timestamp: Optional[float] = None,
        parent: Optional['CausalNode'] = None,
        evidence: Optional[List[str]] = None,
        solutions: Optional[List[str]] = None,
    ):
        """
        Initialize a causal node.
        
        Args:
            id: Unique identifier for the node
            name: Human-readable name
            description: Detailed description
            type: Type of fault
            severity: Severity level
            metrics: Associated metrics
            timestamp: When the node was created
            parent: Parent node
            evidence: Evidence supporting this node
            solutions: Potential solutions
        """
        self.id = id
        self.name = name
        self.description = description
        self.type = type
        self.severity = severity
        self.metrics = metrics or {}
        self.timestamp = timestamp or time.time()
        self.parent = parent
        self.children = []
        self.evidence = evidence or []
        self.solutions = solutions or []
        
        # Add this node as a child of the parent
        if parent is not None:
            parent.add_child(self)
    
    def add_child(self, child: 'CausalNode') -> None:
        """
        Add a child node.
        
        Args:
            child: Child node to add
        """
        if child not in self.children:
            self.children.append(child)
            child.parent = self
    
    def add_evidence(self, evidence: str) -> None:
        """
        Add evidence to the node.
        
        Args:
            evidence: Evidence to add
        """
        if evidence not in self.evidence:
            self.evidence.append(evidence)
    
    def add_solution(self, solution: str) -> None:
        """
        Add a potential solution.
        
        Args:
            solution: Solution to add
        """
        if solution not in self.solutions:
            self.solutions.append(solution)
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the node to a dictionary.
        
        Returns:
            Dictionary representation of the node
        """
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "type": self.type.value,
            "severity": self.severity.value,
            "metrics": self.metrics,
            "timestamp": self.timestamp,
            "evidence": self.evidence,
            "solutions": self.solutions,
            "children": [child.id for child in self.children],
            "parent": self.parent.id if self.parent else None,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any], nodes_map: Dict[str, 'CausalNode'] = None) -> 'CausalNode':
        """
        Create a node from a dictionary.
        
        Args:
            data: Dictionary representation of the node
            nodes_map: Map of node IDs to nodes
            
        Returns:
            CausalNode instance
        """
        nodes_map = nodes_map or {}
        
        # Create the node
        node = cls(
            id=data["id"],
            name=data["name"],
            description=data["description"],
            type=FaultType(data["type"]),
            severity=FaultSeverity(data["severity"]),
            metrics=data["metrics"],
            timestamp=data["timestamp"],
            evidence=data["evidence"],
            solutions=data["solutions"],
        )
        
        # Add to nodes map
        nodes_map[node.id] = node
        
        return node


class CausalFaultTree:
    """
    Tree structure for causal fault analysis.
    
    Attributes:
        root: Root node of the tree
        nodes: Map of node IDs to nodes
        current_node: Currently active node
    """
    
    def __init__(self, root: Optional[CausalNode] = None):
        """
        Initialize a causal fault tree.
        
        Args:
            root: Root node of the tree
        """
        self.root = root
        self.nodes = {}
        self.current_node = root
        
        if root is not None:
            self.nodes[root.id] = root
    
    def add_node(
        self,
        id: str,
        name: str,
        description: str,
        type: FaultType,
        severity: FaultSeverity,
        metrics: Optional[Dict[str, Any]] = None,
        parent: Optional[Union[CausalNode, str]] = None,
        evidence: Optional[List[str]] = None,
        solutions: Optional[List[str]] = None,
    ) -> CausalNode:
        """
        Add a node to the tree.
        
        Args:
            id: Unique identifier for the node
            name: Human-readable name
            description: Detailed description
            type: Type of fault
            severity: Severity level
            metrics: Associated metrics
            parent: Parent node or ID
            evidence: Evidence supporting this node
            solutions: Potential solutions
            
        Returns:
            The created node
        """
        # Resolve parent
        parent_node = None
        if parent is not None:
            if isinstance(parent, str):
                parent_node = self.nodes.get(parent)
                if parent_node is None:
                    raise ValueError(f"Parent node with ID {parent} not found")
            else:
                parent_node = parent
        
        # Create node
        node = CausalNode(
            id=id,
            name=name,
            description=description,
            type=type,
            severity=severity,
            metrics=metrics,
            parent=parent_node,
            evidence=evidence,
            solutions=solutions,
        )
        
        # Add to nodes map
        self.nodes[id] = node
        
        # Set as root if no root exists
        if self.root is None:
            self.root = node
            self.current_node = node
        
        return node
    
    def get_node(self, id: str) -> Optional[CausalNode]:
        """
        Get a node by ID.
        
        Args:
            id: Node ID
            
        Returns:
            Node or None if not found
        """
        return self.nodes.get(id)
    
    def set_current_node(self, node: Union[CausalNode, str]) -> None:
        """
        Set the current active node.
        
        Args:
            node: Node or node ID
        """
        if isinstance(node, str):
            node = self.nodes.get(node)
            if node is None:
                raise ValueError(f"Node with ID {node} not found")
        
        self.current_node = node
    
    def add_child_to_current(
        self,
        id: str,
        name: str,
        description: str,
        type: FaultType,
        severity: FaultSeverity,
        metrics: Optional[Dict[str, Any]] = None,
        evidence: Optional[List[str]] = None,
        solutions: Optional[List[str]] = None,
    ) -> CausalNode:
        """
        Add a child to the current node.
        
        Args:
            id: Unique identifier for the node
            name: Human-readable name
            description: Detailed description
            type: Type of fault
            severity: Severity level
            metrics: Associated metrics
            evidence: Evidence supporting this node
            solutions: Potential solutions
            
        Returns:
            The created node
        """
        if self.current_node is None:
            raise ValueError("No current node set")
        
        return self.add_node(
            id=id,
            name=name,
            description=description,
            type=type,
            severity=severity,
            metrics=metrics,
            parent=self.current_node,
            evidence=evidence,
            solutions=solutions,
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the tree to a dictionary.
        
        Returns:
            Dictionary representation of the tree
        """
        return {
            "root": self.root.id if self.root else None,
            "current": self.current_node.id if self.current_node else None,
            "nodes": {node_id: node.to_dict() for node_id, node in self.nodes.items()},
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'CausalFaultTree':
        """
        Create a tree from a dictionary.
        
        Args:
            data: Dictionary representation of the tree
            
        Returns:
            CausalFaultTree instance
        """
        tree = cls()
        nodes_map = {}
        
        # Create all nodes first
        for node_id, node_data in data["nodes"].items():
            node = CausalNode.from_dict(node_data, nodes_map)
            tree.nodes[node_id] = node
        
        # Set up parent-child relationships
        for node_id, node_data in data["nodes"].items():
            node = tree.nodes[node_id]
            
            # Set parent
            if node_data["parent"] is not None:
                parent = tree.nodes.get(node_data["parent"])
                if parent is not None:
                    node.parent = parent
            
            # Set children
            for child_id in node_data["children"]:
                child = tree.nodes.get(child_id)
                if child is not None:
                    node.children.append(child)
        
        # Set root and current node
        if data["root"] is not None:
            tree.root = tree.nodes.get(data["root"])
        
        if data["current"] is not None:
            tree.current_node = tree.nodes.get(data["current"])
        else:
            tree.current_node = tree.root
        
        return tree
    
    def save(self, path: str) -> None:
        """
        Save the tree to a file.
        
        Args:
            path: Path to save the tree
        """
        with open(path, 'w') as f:
            json.dump(self.to_dict(), f, indent=2)
    
    @classmethod
    def load(cls, path: str) -> 'CausalFaultTree':
        """
        Load a tree from a file.
        
        Args:
            path: Path to load the tree from
            
        Returns:
            CausalFaultTree instance
        """
        with open(path, 'r') as f:
            data = json.load(f)
        
        return cls.from_dict(data)
    
    def visualize(self, output_path: str = None, show: bool = False) -> str:
        """
        Visualize the fault tree.
        
        Args:
            output_path: Path to save the visualization
            show: Whether to show the visualization
            
        Returns:
            Path to the saved visualization
        """
        if not self.root:
            raise ValueError("Tree has no root node")
        
        # Create a directed graph
        G = nx.DiGraph()
        
        # Add nodes and edges
        for node_id, node in self.nodes.items():
            # Node attributes
            G.add_node(
                node_id,
                label=node.name,
                description=node.description,
                type=node.type.value,
                severity=node.severity.value,
            )
            
            # Add edges from parent to children
            for child in node.children:
                G.add_edge(node_id, child.id)
        
        # Set up the plot
        plt.figure(figsize=(12, 8))
        
        # Node positions using hierarchical layout
        pos = nx.nx_agraph.graphviz_layout(G, prog="dot")
        
        # Node colors based on severity
        severity_colors = {
            FaultSeverity.CRITICAL.value: "red",
            FaultSeverity.HIGH.value: "orange",
            FaultSeverity.MEDIUM.value: "yellow",
            FaultSeverity.LOW.value: "green",
            FaultSeverity.INFO.value: "blue",
        }
        
        node_colors = [severity_colors[G.nodes[n]["severity"]] for n in G.nodes]
        
        # Draw the graph
        nx.draw(
            G,
            pos,
            with_labels=True,
            node_color=node_colors,
            node_size=2000,
            font_size=10,
            font_weight="bold",
            arrows=True,
        )
        
        # Add a title
        plt.title("Causal Fault Tree Analysis")
        
        # Save or show
        if output_path:
            plt.savefig(output_path, bbox_inches="tight")
            logger.info(f"Saved fault tree visualization to {output_path}")
        
        if show:
            plt.show()
        
        plt.close()
        
        return output_path


class CausalFaultTreeAnalysis:
    """
    Causal Fault Tree Analysis (CFTA) for identifying root causes of failures or inefficiencies.
    
    This module traces backward through pipeline and config to identify root causes,
    visualizes causal chains, and provides actionable diagnostics.
    
    Attributes:
        model: The PyTorch model being analyzed
        optimizer: The optimizer being used
        dataloader: The dataloader being used
        config: Configuration parameters
        metrics_history: History of collected metrics
        fault_trees: Collection of fault trees
        active_tree: Currently active fault tree
        rules: Analysis rules
        hooks: Registered hooks
        tracing_active: Whether tracing is active
    """
    
    def __init__(
        self,
        model: Optional[torch.nn.Module] = None,
        optimizer: Optional[torch.optim.Optimizer] = None,
        dataloader: Optional[Any] = None,
        config: Optional[Dict[str, Any]] = None,
    ):
        """
        Initialize the CausalFaultTreeAnalysis module.
        
        Args:
            model: The PyTorch model being analyzed
            optimizer: The optimizer being used
            dataloader: The dataloader being used
            config: Configuration parameters
        """
        self.model = model
        self.optimizer = optimizer
        self.dataloader = dataloader
        self.config = config or {}
        
        # Initialize metrics history
        self.metrics_history = defaultdict(list)
        self.metrics_timestamps = []
        
        # Initialize fault trees
        self.fault_trees = {}
        self.active_tree = None
        
        # Initialize rules
        self.rules = self._initialize_rules()
        
        # Initialize hooks
        self.hooks = []
        
        # Initialize tracing
        self.tracing_active = False
        self.trace_history = []
        self.stack_traces = []
        
        # Initialize event log
        self.event_log = []
        
        # Initialize component registry
        self.component_registry = {}
        
        logger.info("Initialized CausalFaultTreeAnalysis")
    
    def register(
        self,
        model: Optional[torch.nn.Module] = None,
        optimizer: Optional[torch.optim.Optimizer] = None,
        dataloader: Optional[Any] = None,
        config: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Register components with the module.
        
        Args:
            model: The PyTorch model being analyzed
            optimizer: The optimizer being used
            dataloader: The dataloader being used
            config: Configuration parameters
        """
        if model is not None:
            self.model = model
            self._register_component("model", model)
        
        if optimizer is not None:
            self.optimizer = optimizer
            self._register_component("optimizer", optimizer)
        
        if dataloader is not None:
            self.dataloader = dataloader
            self._register_component("dataloader", dataloader)
        
        if config is not None:
            self.config = config
            self._register_component("config", config)
        
        logger.info("Registered components with CFTA")
    
    def _register_component(self, name: str, component: Any) -> None:
        """
        Register a component for analysis.
        
        Args:
            name: Component name
            component: Component object
        """
        self.component_registry[name] = {
            "object": component,
            "type": type(component).__name__,
            "registered_at": time.time(),
            "metadata": self._extract_component_metadata(component),
        }
    
    def _extract_component_metadata(self, component: Any) -> Dict[str, Any]:
        """
        Extract metadata from a component.
        
        Args:
            component: Component to extract metadata from
            
        Returns:
            Dictionary of metadata
        """
        metadata = {}
        
        try:
            # Extract model metadata
            if isinstance(component, torch.nn.Module):
                metadata["num_parameters"] = sum(p.numel() for p in component.parameters())
                metadata["trainable_parameters"] = sum(p.numel() for p in component.parameters() if p.requires_grad)
                metadata["layers"] = len(list(component.modules()))
                
                # Get model architecture summary
                metadata["architecture"] = str(component)
                
                # Get parameter statistics
                param_stats = {}
                for name, param in component.named_parameters():
                    if param.requires_grad:
                        param_stats[name] = {
                            "shape": list(param.shape),
                            "size": param.numel(),
                            "dtype": str(param.dtype),
                            "device": str(param.device),
                        }
                
                metadata["parameter_stats"] = param_stats
            
            # Extract optimizer metadata
            elif isinstance(component, torch.optim.Optimizer):
                metadata["type"] = component.__class__.__name__
                metadata["param_groups"] = len(component.param_groups)
                
                # Get optimizer parameters
                optim_params = {}
                for i, group in enumerate(component.param_groups):
                    group_params = {}
                    for k, v in group.items():
                        if k != "params":
                            group_params[k] = v
                    
                    optim_params[f"group_{i}"] = group_params
                
                metadata["parameters"] = optim_params
            
            # Extract dataloader metadata
            elif hasattr(component, "__iter__") and hasattr(component, "__len__"):
                metadata["length"] = len(component)
                metadata["batch_size"] = getattr(component, "batch_size", None)
                metadata["num_workers"] = getattr(component, "num_workers", None)
                metadata["pin_memory"] = getattr(component, "pin_memory", None)
                metadata["shuffle"] = getattr(component, "shuffle", None)
                
                # Try to get dataset info
                if hasattr(component, "dataset"):
                    dataset = component.dataset
                    metadata["dataset_length"] = len(dataset)
                    metadata["dataset_type"] = type(dataset).__name__
            
            # Extract config metadata
            elif isinstance(component, dict):
                # Just use the dict directly
                metadata = component
        
        except Exception as e:
            logger.warning(f"Error extracting metadata: {e}")
        
        return metadata
    
    def update_metrics(self, metrics: Dict[str, Any]) -> None:
        """
        Update metrics history.
        
        Args:
            metrics: Current metrics
        """
        timestamp = time.time()
        self.metrics_timestamps.append(timestamp)
        
        for key, value in metrics.items():
            # Convert torch tensors to Python values
            if isinstance(value, torch.Tensor):
                value = value.item() if value.numel() == 1 else value.mean().item()
            
            self.metrics_history[key].append(value)
        
        # Analyze metrics for potential issues
        self._analyze_metrics(metrics, timestamp)
    
    def _analyze_metrics(self, metrics: Dict[str, Any], timestamp: float) -> None:
        """
        Analyze metrics for potential issues.
        
        Args:
            metrics: Current metrics
            timestamp: Timestamp of the metrics
        """
        # Apply rules to detect issues
        for rule in self.rules:
            try:
                if rule["condition"](metrics, self.metrics_history):
                    # Rule triggered, create an event
                    event = {
                        "timestamp": timestamp,
                        "type": rule["type"],
                        "name": rule["name"],
                        "description": rule["description"],
                        "severity": rule["severity"],
                        "metrics": {k: metrics.get(k) for k in rule["relevant_metrics"]},
                    }
                    
                    self.event_log.append(event)
                    
                    # Create a fault tree if this is a new issue
                    if rule["create_tree"]:
                        self._create_fault_tree_from_event(event)
                    
                    logger.info(f"Detected issue: {rule['name']}")
            except Exception as e:
                logger.warning(f"Error applying rule {rule['name']}: {e}")
    
    def _create_fault_tree_from_event(self, event: Dict[str, Any]) -> None:
        """
        Create a fault tree from an event.
        
        Args:
            event: Event that triggered the fault tree
        """
        # Create a unique ID for the tree
        tree_id = f"{event['type']}_{int(event['timestamp'])}"
        
        # Check if a tree with this ID already exists
        if tree_id in self.fault_trees:
            return
        
        # Create a new tree
        tree = CausalFaultTree()
        
        # Create the root node
        root = tree.add_node(
            id=f"{tree_id}_root",
            name=event["name"],
            description=event["description"],
            type=FaultType(event["type"]),
            severity=FaultSeverity(event["severity"]),
            metrics=event["metrics"],
        )
        
        # Set as active tree
        self.fault_trees[tree_id] = tree
        self.active_tree = tree
        
        # Start tracing to find the cause
        self._trace_fault_cause(root)
    
    def _trace_fault_cause(self, node: CausalNode) -> None:
        """
        Trace the cause of a fault.
        
        Args:
            node: Node representing the fault
        """
        # Get the fault type
        fault_type = node.type
        
        # Apply causal analysis based on fault type
        if fault_type == FaultType.MEMORY:
            self._analyze_memory_fault(node)
        elif fault_type == FaultType.PERFORMANCE:
            self._analyze_performance_fault(node)
        elif fault_type == FaultType.CONVERGENCE:
            self._analyze_convergence_fault(node)
        elif fault_type == FaultType.DATALOADER:
            self._analyze_dataloader_fault(node)
        elif fault_type == FaultType.HARDWARE:
            self._analyze_hardware_fault(node)
        elif fault_type == FaultType.CONFIGURATION:
            self._analyze_configuration_fault(node)
        elif fault_type == FaultType.NUMERICAL:
            self._analyze_numerical_fault(node)
        elif fault_type == FaultType.IMPLEMENTATION:
            self._analyze_implementation_fault(node)
        else:
            logger.warning(f"No analysis available for fault type: {fault_type}")
    
    def _analyze_memory_fault(self, node: CausalNode) -> None:
        """
        Analyze a memory-related fault.
        
        Args:
            node: Node representing the fault
        """
        # Check model size
        if self.model is not None:
            model_size = sum(p.numel() * p.element_size() for p in self.model.parameters()) / (1024 * 1024)
            
            if model_size > 1000:  # More than 1GB
                child = self.active_tree.add_node(
                    id=f"{node.id}_large_model",
                    name="Large Model Size",
                    description=f"Model size is {model_size:.2f} MB, which may cause memory issues",
                    type=FaultType.MEMORY,
                    severity=FaultSeverity.MEDIUM,
                    parent=node,
                    metrics={"model_size_mb": model_size},
                    solutions=[
                        "Use a smaller model architecture",
                        "Apply model pruning or quantization",
                        "Enable gradient checkpointing",
                        "Use mixed precision training",
                    ],
                )
        
        # Check batch size
        if self.dataloader is not None and hasattr(self.dataloader, "batch_size"):
            batch_size = self.dataloader.batch_size
            
            # Check if batch size is too large relative to available memory
            if "cuda_memory_allocated" in node.metrics and "cuda_memory_total" in node.metrics:
                memory_usage = node.metrics["cuda_memory_allocated"] / node.metrics["cuda_memory_total"]
                
                if memory_usage > 0.8 and batch_size > 1:
                    child = self.active_tree.add_node(
                        id=f"{node.id}_large_batch",
                        name="Large Batch Size",
                        description=f"Batch size is {batch_size}, which may be too large for available memory",
                        type=FaultType.MEMORY,
                        severity=FaultSeverity.HIGH,
                        parent=node,
                        metrics={"batch_size": batch_size, "memory_usage": memory_usage},
                        solutions=[
                            "Reduce batch size",
                            "Use gradient accumulation with smaller batches",
                            "Enable mixed precision training",
                        ],
                    )
        
        # Check for memory fragmentation
        if "cuda_memory_allocated" in node.metrics and "cuda_memory_reserved" in node.metrics:
            allocated = node.metrics["cuda_memory_allocated"]
            reserved = node.metrics["cuda_memory_reserved"]
            
            if reserved > 0:
                fragmentation = 1.0 - (allocated / reserved)
                
                if fragmentation > 0.3:  # More than 30% fragmentation
                    child = self.active_tree.add_node(
                        id=f"{node.id}_fragmentation",
                        name="Memory Fragmentation",
                        description=f"Memory fragmentation is {fragmentation:.2%}, which may cause OOM errors",
                        type=FaultType.MEMORY,
                        severity=FaultSeverity.MEDIUM,
                        parent=node,
                        metrics={"fragmentation": fragmentation},
                        solutions=[
                            "Call torch.cuda.empty_cache() periodically",
                            "Reduce variable scope to free memory earlier",
                            "Avoid creating many small tensors",
                        ],
                    )
        
        # Check for activation memory
        if self.model is not None and hasattr(self.model, "forward"):
            # This is a simplified check - in a real implementation, you would
            # need to trace the forward pass to estimate activation memory
            has_many_activations = False
            
            for module in self.model.modules():
                if isinstance(module, (torch.nn.ReLU, torch.nn.GELU, torch.nn.SiLU)):
                    has_many_activations = True
                    break
            
            if has_many_activations:
                child = self.active_tree.add_node(
                    id=f"{node.id}_activations",
                    name="High Activation Memory",
                    description="Model has many activation functions, which may cause high memory usage",
                    type=FaultType.MEMORY,
                    severity=FaultSeverity.MEDIUM,
                    parent=node,
                    solutions=[
                        "Enable activation checkpointing",
                        "Use more memory-efficient activation functions",
                        "Reduce model depth",
                    ],
                )
    
    def _analyze_performance_fault(self, node: CausalNode) -> None:
        """
        Analyze a performance-related fault.
        
        Args:
            node: Node representing the fault
        """
        # Check dataloader performance
        if "dataloader_time" in node.metrics and "batch_time" in node.metrics:
            dataloader_time = node.metrics["dataloader_time"]
            batch_time = node.metrics["batch_time"]
            
            if dataloader_time > 0.3 * batch_time:  # Dataloader takes more than 30% of batch time
                child = self.active_tree.add_node(
                    id=f"{node.id}_dataloader_bottleneck",
                    name="Dataloader Bottleneck",
                    description="Dataloader is taking a significant portion of batch processing time",
                    type=FaultType.DATALOADER,
                    severity=FaultSeverity.MEDIUM,
                    parent=node,
                    metrics={"dataloader_time": dataloader_time, "batch_time": batch_time},
                    solutions=[
                        "Increase number of dataloader workers",
                        "Use faster data loading methods (e.g., memory mapping)",
                        "Optimize data preprocessing",
                        "Use pin_memory=True for GPU training",
                    ],
                )
                
                # Further analyze dataloader bottleneck
                self._analyze_dataloader_fault(child)
        
        # Check GPU utilization
        if "gpu_utilization" in node.metrics:
            gpu_util = node.metrics["gpu_utilization"]
            
            if gpu_util < 0.5:  # Less than 50% GPU utilization
                child = self.active_tree.add_node(
                    id=f"{node.id}_low_gpu_util",
                    name="Low GPU Utilization",
                    description=f"GPU utilization is only {gpu_util:.2%}, indicating inefficient computation",
                    type=FaultType.PERFORMANCE,
                    severity=FaultSeverity.MEDIUM,
                    parent=node,
                    metrics={"gpu_utilization": gpu_util},
                    solutions=[
                        "Increase batch size",
                        "Use mixed precision training",
                        "Optimize model architecture for better parallelism",
                        "Check for CPU bottlenecks in preprocessing",
                    ],
                )
        
        # Check CPU utilization for dataloader workers
        if "cpu_utilization" in node.metrics and self.dataloader is not None:
            cpu_util = node.metrics["cpu_utilization"]
            num_workers = getattr(self.dataloader, "num_workers", 0)
            
            if cpu_util < 0.5 and num_workers > 0:  # Low CPU utilization with workers
                child = self.active_tree.add_node(
                    id=f"{node.id}_inefficient_workers",
                    name="Inefficient Dataloader Workers",
                    description=f"Using {num_workers} workers but CPU utilization is only {cpu_util:.2%}",
                    type=FaultType.DATALOADER,
                    severity=FaultSeverity.LOW,
                    parent=node,
                    metrics={"cpu_utilization": cpu_util, "num_workers": num_workers},
                    solutions=[
                        "Reduce number of dataloader workers",
                        "Optimize data preprocessing to be more CPU-intensive",
                    ],
                )
        
        # Check optimizer overhead
        if "optimizer_time" in node.metrics and "backward_time" in node.metrics:
            optimizer_time = node.metrics["optimizer_time"]
            backward_time = node.metrics["backward_time"]
            
            if optimizer_time > 0.5 * backward_time:  # Optimizer takes more than 50% of backward time
                child = self.active_tree.add_node(
                    id=f"{node.id}_optimizer_overhead",
                    name="High Optimizer Overhead",
                    description="Optimizer is taking a significant portion of backward pass time",
                    type=FaultType.PERFORMANCE,
                    severity=FaultSeverity.MEDIUM,
                    parent=node,
                    metrics={"optimizer_time": optimizer_time, "backward_time": backward_time},
                    solutions=[
                        "Use a simpler optimizer (e.g., SGD instead of Adam)",
                        "Reduce model complexity",
                        "Use parameter groups with different settings",
                    ],
                )
    
    def _analyze_convergence_fault(self, node: CausalNode) -> None:
        """
        Analyze a convergence-related fault.
        
        Args:
            node: Node representing the fault
        """
        # Check for exploding gradients
        if "grad_norm" in node.metrics:
            grad_norm = node.metrics["grad_norm"]
            
            if grad_norm > 10.0:  # Arbitrary threshold for high gradient norm
                child = self.active_tree.add_node(
                    id=f"{node.id}_exploding_gradients",
                    name="Exploding Gradients",
                    description=f"Gradient norm is {grad_norm:.2f}, which may cause training instability",
                    type=FaultType.NUMERICAL,
                    severity=FaultSeverity.HIGH,
                    parent=node,
                    metrics={"grad_norm": grad_norm},
                    solutions=[
                        "Apply gradient clipping",
                        "Reduce learning rate",
                        "Use weight normalization or layer normalization",
                        "Check for issues in loss function",
                    ],
                )
        
        # Check for vanishing gradients
        if "grad_norm" in node.metrics:
            grad_norm = node.metrics["grad_norm"]
            
            if grad_norm < 0.0001:  # Arbitrary threshold for low gradient norm
                child = self.active_tree.add_node(
                    id=f"{node.id}_vanishing_gradients",
                    name="Vanishing Gradients",
                    description=f"Gradient norm is {grad_norm:.6f}, which may cause slow or stalled training",
                    type=FaultType.NUMERICAL,
                    severity=FaultSeverity.HIGH,
                    parent=node,
                    metrics={"grad_norm": grad_norm},
                    solutions=[
                        "Use architectures that mitigate vanishing gradients (e.g., ResNet)",
                        "Use activation functions that don't saturate (e.g., ReLU, LeakyReLU)",
                        "Initialize weights properly",
                        "Use batch normalization",
                    ],
                )
        
        # Check for plateauing loss
        if len(self.metrics_history.get("loss", [])) > 10:
            recent_losses = self.metrics_history["loss"][-10:]
            loss_change = abs(recent_losses[-1] - recent_losses[0]) / max(abs(recent_losses[0]), 1e-10)
            
            if loss_change < 0.01:  # Less than 1% change in loss
                child = self.active_tree.add_node(
                    id=f"{node.id}_plateauing_loss",
                    name="Plateauing Loss",
                    description="Loss has changed very little over recent iterations",
                    type=FaultType.CONVERGENCE,
                    severity=FaultSeverity.MEDIUM,
                    parent=node,
                    metrics={"loss_change": loss_change},
                    solutions=[
                        "Increase learning rate",
                        "Use a learning rate scheduler",
                        "Try a different optimizer",
                        "Check if model has enough capacity",
                    ],
                )
        
        # Check for oscillating loss
        if len(self.metrics_history.get("loss", [])) > 10:
            recent_losses = self.metrics_history["loss"][-10:]
            
            # Calculate oscillation metric (simplified)
            oscillations = sum(1 for i in range(1, len(recent_losses) - 1)
                              if (recent_losses[i] - recent_losses[i-1]) * 
                                 (recent_losses[i+1] - recent_losses[i]) < 0)
            
            oscillation_ratio = oscillations / (len(recent_losses) - 2)
            
            if oscillation_ratio > 0.5:  # More than 50% of points show oscillation
                child = self.active_tree.add_node(
                    id=f"{node.id}_oscillating_loss",
                    name="Oscillating Loss",
                    description="Loss is oscillating significantly between iterations",
                    type=FaultType.CONVERGENCE,
                    severity=FaultSeverity.MEDIUM,
                    parent=node,
                    metrics={"oscillation_ratio": oscillation_ratio},
                    solutions=[
                        "Reduce learning rate",
                        "Use a smoother optimizer (e.g., Adam)",
                        "Add gradient clipping",
                        "Use a learning rate scheduler with warm-up",
                    ],
                )
    
    def _analyze_dataloader_fault(self, node: CausalNode) -> None:
        """
        Analyze a dataloader-related fault.
        
        Args:
            node: Node representing the fault
        """
        if self.dataloader is None:
            return
        
        # Check number of workers
        num_workers = getattr(self.dataloader, "num_workers", 0)
        
        if num_workers == 0:
            child = self.active_tree.add_node(
                id=f"{node.id}_no_workers",
                name="No Dataloader Workers",
                description="Dataloader is running in the main process, which may cause I/O bottlenecks",
                type=FaultType.DATALOADER,
                severity=FaultSeverity.MEDIUM,
                parent=node,
                metrics={"num_workers": num_workers},
                solutions=[
                    "Set num_workers to a positive value (typically 4-8)",
                    "Use pin_memory=True for GPU training",
                ],
            )
        
        # Check pin_memory
        pin_memory = getattr(self.dataloader, "pin_memory", False)
        
        if not pin_memory and torch.cuda.is_available():
            child = self.active_tree.add_node(
                id=f"{node.id}_no_pin_memory",
                name="Pin Memory Not Enabled",
                description="Dataloader is not using pinned memory, which may slow down CPU to GPU transfers",
                type=FaultType.DATALOADER,
                severity=FaultSeverity.LOW,
                parent=node,
                metrics={"pin_memory": pin_memory},
                solutions=[
                    "Set pin_memory=True in DataLoader constructor",
                ],
            )
        
        # Check prefetch factor
        prefetch_factor = getattr(self.dataloader, "prefetch_factor", 2)
        
        if prefetch_factor < 2 and num_workers > 0:
            child = self.active_tree.add_node(
                id=f"{node.id}_low_prefetch",
                name="Low Prefetch Factor",
                description="Dataloader has a low prefetch factor, which may cause workers to be underutilized",
                type=FaultType.DATALOADER,
                severity=FaultSeverity.LOW,
                parent=node,
                metrics={"prefetch_factor": prefetch_factor},
                solutions=[
                    "Increase prefetch_factor to 2-4",
                ],
            )
        
        # Check for complex transforms
        if hasattr(self.dataloader, "dataset") and hasattr(self.dataloader.dataset, "transform"):
            transform = self.dataloader.dataset.transform
            transform_str = str(transform)
            
            # Check for CPU-intensive transforms
            cpu_intensive_transforms = ["Resize", "RandomResizedCrop", "RandomRotation"]
            has_cpu_intensive = any(t in transform_str for t in cpu_intensive_transforms)
            
            if has_cpu_intensive:
                child = self.active_tree.add_node(
                    id=f"{node.id}_complex_transforms",
                    name="Complex Data Transforms",
                    description="Dataset is using CPU-intensive transforms, which may slow down data loading",
                    type=FaultType.DATALOADER,
                    severity=FaultSeverity.MEDIUM,
                    parent=node,
                    solutions=[
                        "Pre-process data offline if possible",
                        "Optimize transform operations",
                        "Increase number of workers",
                    ],
                )
    
    def _analyze_hardware_fault(self, node: CausalNode) -> None:
        """
        Analyze a hardware-related fault.
        
        Args:
            node: Node representing the fault
        """
        # Check for thermal throttling
        if "gpu_temperature" in node.metrics:
            temp = node.metrics["gpu_temperature"]
            
            if temp > 80:  # Arbitrary threshold for high temperature
                child = self.active_tree.add_node(
                    id=f"{node.id}_thermal_throttling",
                    name="GPU Thermal Throttling",
                    description=f"GPU temperature is {temp}°C, which may cause thermal throttling",
                    type=FaultType.HARDWARE,
                    severity=FaultSeverity.HIGH,
                    parent=node,
                    metrics={"gpu_temperature": temp},
                    solutions=[
                        "Improve cooling",
                        "Reduce batch size or model complexity",
                        "Check for other processes using the GPU",
                    ],
                )
        
        # Check for power throttling
        if "gpu_power_usage" in node.metrics and "gpu_power_limit" in node.metrics:
            power_usage = node.metrics["gpu_power_usage"]
            power_limit = node.metrics["gpu_power_limit"]
            
            if power_usage > 0.95 * power_limit:  # Near power limit
                child = self.active_tree.add_node(
                    id=f"{node.id}_power_throttling",
                    name="GPU Power Throttling",
                    description=f"GPU power usage is {power_usage:.2f}W, close to the limit of {power_limit:.2f}W",
                    type=FaultType.HARDWARE,
                    severity=FaultSeverity.MEDIUM,
                    parent=node,
                    metrics={"gpu_power_usage": power_usage, "gpu_power_limit": power_limit},
                    solutions=[
                        "Reduce batch size or model complexity",
                        "Use mixed precision training",
                        "Check for other processes using the GPU",
                    ],
                )
        
        # Check for CPU bottleneck
        if "cpu_utilization" in node.metrics and "gpu_utilization" in node.metrics:
            cpu_util = node.metrics["cpu_utilization"]
            gpu_util = node.metrics["gpu_utilization"]
            
            if cpu_util > 0.9 and gpu_util < 0.5:  # High CPU, low GPU
                child = self.active_tree.add_node(
                    id=f"{node.id}_cpu_bottleneck",
                    name="CPU Bottleneck",
                    description="CPU utilization is high while GPU utilization is low, indicating a CPU bottleneck",
                    type=FaultType.HARDWARE,
                    severity=FaultSeverity.MEDIUM,
                    parent=node,
                    metrics={"cpu_utilization": cpu_util, "gpu_utilization": gpu_util},
                    solutions=[
                        "Optimize data preprocessing",
                        "Increase number of dataloader workers",
                        "Move more computation to the GPU",
                        "Use a faster CPU or more cores",
                    ],
                )
        
        # Check for slow disk I/O
        if "dataloader_time" in node.metrics and "batch_time" in node.metrics:
            dataloader_time = node.metrics["dataloader_time"]
            batch_time = node.metrics["batch_time"]
            
            if dataloader_time > 0.5 * batch_time:  # Dataloader takes more than 50% of batch time
                # Check if this is likely due to disk I/O
                if self.dataloader is not None and getattr(self.dataloader, "num_workers", 0) > 0:
                    child = self.active_tree.add_node(
                        id=f"{node.id}_slow_disk",
                        name="Slow Disk I/O",
                        description="Data loading is slow despite using multiple workers, indicating slow disk I/O",
                        type=FaultType.HARDWARE,
                        severity=FaultSeverity.MEDIUM,
                        parent=node,
                        metrics={"dataloader_time": dataloader_time, "batch_time": batch_time},
                        solutions=[
                            "Use a faster storage device (SSD or NVMe)",
                            "Cache data in memory if possible",
                            "Use memory mapping for large datasets",
                            "Reduce data preprocessing complexity",
                        ],
                    )
    
    def _analyze_configuration_fault(self, node: CausalNode) -> None:
        """
        Analyze a configuration-related fault.
        
        Args:
            node: Node representing the fault
        """
        # Check learning rate
        if self.optimizer is not None and hasattr(self.optimizer, "param_groups"):
            lr = self.optimizer.param_groups[0].get("lr", 0)
            
            # Check for very high learning rate
            if lr > 0.1:
                child = self.active_tree.add_node(
                    id=f"{node.id}_high_lr",
                    name="High Learning Rate",
                    description=f"Learning rate is {lr}, which may cause training instability",
                    type=FaultType.CONFIGURATION,
                    severity=FaultSeverity.MEDIUM,
                    parent=node,
                    metrics={"learning_rate": lr},
                    solutions=[
                        "Reduce learning rate",
                        "Use a learning rate scheduler",
                        "Use gradient clipping",
                    ],
                )
            
            # Check for very low learning rate
            if lr < 1e-5:
                child = self.active_tree.add_node(
                    id=f"{node.id}_low_lr",
                    name="Low Learning Rate",
                    description=f"Learning rate is {lr}, which may cause slow convergence",
                    type=FaultType.CONFIGURATION,
                    severity=FaultSeverity.MEDIUM,
                    parent=node,
                    metrics={"learning_rate": lr},
                    solutions=[
                        "Increase learning rate",
                        "Use a learning rate scheduler with warm-up",
                        "Try a different optimizer",
                    ],
                )
        
        # Check batch size
        if self.dataloader is not None and hasattr(self.dataloader, "batch_size"):
            batch_size = self.dataloader.batch_size
            
            # Check for very small batch size
            if batch_size < 4:
                child = self.active_tree.add_node(
                    id=f"{node.id}_small_batch",
                    name="Small Batch Size",
                    description=f"Batch size is {batch_size}, which may cause noisy gradients and slow training",
                    type=FaultType.CONFIGURATION,
                    severity=FaultSeverity.LOW,
                    parent=node,
                    metrics={"batch_size": batch_size},
                    solutions=[
                        "Increase batch size if memory allows",
                        "Use gradient accumulation to simulate larger batches",
                        "Use a different optimizer (e.g., Adam) that handles noisy gradients better",
                    ],
                )
        
        # Check for mixed precision
        if torch.cuda.is_available():
            using_amp = False
            
            # Check if torch.cuda.amp is being used
            if "using_amp" in node.metrics:
                using_amp = node.metrics["using_amp"]
            
            if not using_amp:
                child = self.active_tree.add_node(
                    id=f"{node.id}_no_amp",
                    name="Mixed Precision Not Enabled",
                    description="Mixed precision training is not enabled, which may reduce performance and increase memory usage",
                    type=FaultType.CONFIGURATION,
                    severity=FaultSeverity.LOW,
                    parent=node,
                    solutions=[
                        "Enable mixed precision training with torch.cuda.amp",
                        "Use torch.cuda.amp.autocast and GradScaler",
                    ],
                )
        
        # Check for gradient checkpointing
        if self.model is not None and "memory_usage" in node.metrics:
            memory_usage = node.metrics["memory_usage"]
            
            using_checkpointing = False
            
            # Check if gradient checkpointing is being used
            if "using_checkpointing" in node.metrics:
                using_checkpointing = node.metrics["using_checkpointing"]
            
            if not using_checkpointing and memory_usage > 0.8:
                child = self.active_tree.add_node(
                    id=f"{node.id}_no_checkpointing",
                    name="Gradient Checkpointing Not Enabled",
                    description="Gradient checkpointing is not enabled despite high memory usage",
                    type=FaultType.CONFIGURATION,
                    severity=FaultSeverity.MEDIUM,
                    parent=node,
                    metrics={"memory_usage": memory_usage},
                    solutions=[
                        "Enable gradient checkpointing",
                        "Use torch.utils.checkpoint.checkpoint for specific modules",
                    ],
                )
    
    def _analyze_numerical_fault(self, node: CausalNode) -> None:
        """
        Analyze a numerical-related fault.
        
        Args:
            node: Node representing the fault
        """
        # Check for NaN or Inf values
        if "has_nan" in node.metrics or "has_inf" in node.metrics:
            has_nan = node.metrics.get("has_nan", False)
            has_inf = node.metrics.get("has_inf", False)
            
            if has_nan or has_inf:
                child = self.active_tree.add_node(
                    id=f"{node.id}_nan_inf",
                    name="NaN or Inf Values",
                    description="Model contains NaN or Inf values, which will cause training to fail",
                    type=FaultType.NUMERICAL,
                    severity=FaultSeverity.CRITICAL,
                    parent=node,
                    metrics={"has_nan": has_nan, "has_inf": has_inf},
                    solutions=[
                        "Check for division by zero or log of zero",
                        "Add epsilon to denominators",
                        "Use gradient clipping",
                        "Check for numerical instability in loss function",
                    ],
                )
        
        # Check for very large or small values
        if "max_value" in node.metrics or "min_value" in node.metrics:
            max_value = node.metrics.get("max_value", 0)
            min_value = node.metrics.get("min_value", 0)
            
            if abs(max_value) > 1e6 or (min_value != 0 and abs(min_value) < 1e-6):
                child = self.active_tree.add_node(
                    id=f"{node.id}_extreme_values",
                    name="Extreme Values",
                    description="Model contains very large or small values, which may cause numerical instability",
                    type=FaultType.NUMERICAL,
                    severity=FaultSeverity.HIGH,
                    parent=node,
                    metrics={"max_value": max_value, "min_value": min_value},
                    solutions=[
                        "Use weight normalization or layer normalization",
                        "Check for proper initialization",
                        "Use gradient clipping",
                        "Check for numerical instability in loss function",
                    ],
                )
        
        # Check for dead neurons (ReLU units that are always negative)
        if "dead_neurons_pct" in node.metrics:
            dead_neurons_pct = node.metrics["dead_neurons_pct"]
            
            if dead_neurons_pct > 10:  # More than 10% dead neurons
                child = self.active_tree.add_node(
                    id=f"{node.id}_dead_neurons",
                    name="Dead Neurons",
                    description=f"{dead_neurons_pct:.2f}% of neurons are dead (always output zero)",
                    type=FaultType.NUMERICAL,
                    severity=FaultSeverity.MEDIUM,
                    parent=node,
                    metrics={"dead_neurons_pct": dead_neurons_pct},
                    solutions=[
                        "Use LeakyReLU instead of ReLU",
                        "Reduce learning rate",
                        "Check for proper initialization",
                        "Use batch normalization",
                    ],
                )
        
        # Check for saturated neurons (sigmoid/tanh units that are always near extremes)
        if "saturated_neurons_pct" in node.metrics:
            saturated_neurons_pct = node.metrics["saturated_neurons_pct"]
            
            if saturated_neurons_pct > 10:  # More than 10% saturated neurons
                child = self.active_tree.add_node(
                    id=f"{node.id}_saturated_neurons",
                    name="Saturated Neurons",
                    description=f"{saturated_neurons_pct:.2f}% of neurons are saturated (always near extremes)",
                    type=FaultType.NUMERICAL,
                    severity=FaultSeverity.MEDIUM,
                    parent=node,
                    metrics={"saturated_neurons_pct": saturated_neurons_pct},
                    solutions=[
                        "Use ReLU or other non-saturating activations",
                        "Reduce learning rate",
                        "Check for proper initialization",
                        "Use batch normalization",
                    ],
                )
    
    def _analyze_implementation_fault(self, node: CausalNode) -> None:
        """
        Analyze an implementation-related fault.
        
        Args:
            node: Node representing the fault
        """
        # This would require more sophisticated analysis of the code
        # Here we just provide a placeholder implementation
        
        # Check for common implementation issues
        if self.model is not None:
            # Check for model in training mode during evaluation
            if "is_eval" in node.metrics and "model_training" in node.metrics:
                is_eval = node.metrics["is_eval"]
                model_training = node.metrics["model_training"]
                
                if is_eval and model_training:
                    child = self.active_tree.add_node(
                        id=f"{node.id}_train_mode_in_eval",
                        name="Training Mode During Evaluation",
                        description="Model is in training mode during evaluation, which may affect results",
                        type=FaultType.IMPLEMENTATION,
                        severity=FaultSeverity.MEDIUM,
                        parent=node,
                        solutions=[
                            "Call model.eval() before evaluation",
                            "Use torch.no_grad() during evaluation",
                        ],
                    )
            
            # Check for missing zero_grad
            if "missing_zero_grad" in node.metrics:
                missing_zero_grad = node.metrics["missing_zero_grad"]
                
                if missing_zero_grad:
                    child = self.active_tree.add_node(
                        id=f"{node.id}_missing_zero_grad",
                        name="Missing Zero Grad",
                        description="Gradients are not zeroed before backward pass, which may cause incorrect updates",
                        type=FaultType.IMPLEMENTATION,
                        severity=FaultSeverity.HIGH,
                        parent=node,
                        solutions=[
                            "Call optimizer.zero_grad() before loss.backward()",
                            "Use set_to_none=True for better performance",
                        ],
                    )
            
            # Check for detached tensors
            if "detached_tensors" in node.metrics:
                detached_tensors = node.metrics["detached_tensors"]
                
                if detached_tensors:
                    child = self.active_tree.add_node(
                        id=f"{node.id}_detached_tensors",
                        name="Detached Tensors",
                        description="Tensors are detached from the computation graph, which may prevent gradient flow",
                        type=FaultType.IMPLEMENTATION,
                        severity=FaultSeverity.HIGH,
                        parent=node,
                        solutions=[
                            "Remove .detach() calls from tensors that need gradients",
                            "Check for accidental use of .item(), .cpu(), or .numpy()",
                            "Ensure tensors are created with requires_grad=True when needed",
                        ],
                    )
    
    def _initialize_rules(self) -> List[Dict[str, Any]]:
        """
        Initialize analysis rules.
        
        Returns:
            List of rules
        """
        rules = []
        
        # Memory-related rules
        rules.append({
            "name": "High Memory Usage",
            "description": "Memory usage is approaching device limits",
            "type": FaultType.MEMORY.value,
            "severity": FaultSeverity.HIGH.value,
            "condition": lambda metrics, history: metrics.get("memory_usage", 0) > 0.9,
            "relevant_metrics": ["memory_usage", "cuda_memory_allocated", "cuda_memory_reserved", "cuda_memory_total"],
            "create_tree": True,
        })
        
        # Performance-related rules
        rules.append({
            "name": "Slow Iteration Time",
            "description": "Batch processing time is unusually high",
            "type": FaultType.PERFORMANCE.value,
            "severity": FaultSeverity.MEDIUM.value,
            "condition": lambda metrics, history: (
                len(history.get("batch_time", [])) > 5 and
                metrics.get("batch_time", 0) > 1.5 * sum(history["batch_time"][-5:]) / 5
            ),
            "relevant_metrics": ["batch_time", "forward_time", "backward_time", "optimizer_time", "dataloader_time"],
            "create_tree": True,
        })
        
        # Dataloader-related rules
        rules.append({
            "name": "Dataloader Bottleneck",
            "description": "Data loading is taking a significant portion of iteration time",
            "type": FaultType.DATALOADER.value,
            "severity": FaultSeverity.MEDIUM.value,
            "condition": lambda metrics, history: (
                metrics.get("dataloader_time", 0) > 0.3 * metrics.get("batch_time", 1)
            ),
            "relevant_metrics": ["dataloader_time", "batch_time", "num_workers", "pin_memory"],
            "create_tree": True,
        })
        
        # Convergence-related rules
        rules.append({
            "name": "Training Not Converging",
            "description": "Loss is not decreasing over time",
            "type": FaultType.CONVERGENCE.value,
            "severity": FaultSeverity.HIGH.value,
            "condition": lambda metrics, history: (
                len(history.get("loss", [])) > 20 and
                abs(history["loss"][-1] - history["loss"][-20]) / max(abs(history["loss"][-20]), 1e-10) < 0.01
            ),
            "relevant_metrics": ["loss", "learning_rate", "grad_norm"],
            "create_tree": True,
        })
        
        # Numerical stability rules
        rules.append({
            "name": "Numerical Instability",
            "description": "Model contains NaN or Inf values",
            "type": FaultType.NUMERICAL.value,
            "severity": FaultSeverity.CRITICAL.value,
            "condition": lambda metrics, history: (
                metrics.get("has_nan", False) or metrics.get("has_inf", False)
            ),
            "relevant_metrics": ["has_nan", "has_inf", "max_value", "min_value", "grad_norm"],
            "create_tree": True,
        })
        
        return rules
    
    def start_tracing(self) -> None:
        """Start tracing for fault analysis."""
        if self.tracing_active:
            logger.warning("Tracing is already active")
            return
        
        self.tracing_active = True
        self.trace_history = []
        self.stack_traces = []
        
        # Register hooks
        if self.model is not None:
            self._register_model_hooks()
        
        if self.optimizer is not None:
            self._register_optimizer_hooks()
        
        logger.info("Started tracing for fault analysis")
    
    def stop_tracing(self) -> None:
        """Stop tracing for fault analysis."""
        if not self.tracing_active:
            logger.warning("Tracing is not active")
            return
        
        self.tracing_active = False
        
        # Remove hooks
        for hook in self.hooks:
            hook.remove()
        
        self.hooks = []
        
        logger.info("Stopped tracing for fault analysis")
    
    def _register_model_hooks(self) -> None:
        """Register hooks for model tracing."""
        # Forward pre-hook
        def forward_pre_hook(module, input):
            if self.tracing_active:
                self.trace_history.append({
                    "type": "forward_pre",
                    "module": type(module).__name__,
                    "timestamp": time.time(),
                    "stack_trace": traceback.extract_stack(),
                })
            return None
        
        # Forward hook
        def forward_hook(module, input, output):
            if self.tracing_active:
                self.trace_history.append({
                    "type": "forward",
                    "module": type(module).__name__,
                    "timestamp": time.time(),
                    "stack_trace": traceback.extract_stack(),
                })
            return None
        
        # Backward hook
        def backward_hook(module, grad_input, grad_output):
            if self.tracing_active:
                self.trace_history.append({
                    "type": "backward",
                    "module": type(module).__name__,
                    "timestamp": time.time(),
                    "stack_trace": traceback.extract_stack(),
                })
            return None
        
        # Register hooks
        for name, module in self.model.named_modules():
            # Skip the root module
            if name == "":
                continue
            
            # Register hooks
            self.hooks.append(module.register_forward_pre_hook(forward_pre_hook))
            self.hooks.append(module.register_forward_hook(forward_hook))
            
            if hasattr(module, "register_backward_hook"):
                self.hooks.append(module.register_backward_hook(backward_hook))
    
    def _register_optimizer_hooks(self) -> None:
        """Register hooks for optimizer tracing."""
        # Patch optimizer step method
        original_step = self.optimizer.step
        
        @functools.wraps(original_step)
        def patched_step(*args, **kwargs):
            if self.tracing_active:
                self.trace_history.append({
                    "type": "optimizer_step",
                    "optimizer": type(self.optimizer).__name__,
                    "timestamp": time.time(),
                    "stack_trace": traceback.extract_stack(),
                })
            
            return original_step(*args, **kwargs)
        
        self.optimizer.step = patched_step
        
        # Store the original method for cleanup
        self.original_optimizer_step = original_step
        
        # Patch optimizer zero_grad method
        original_zero_grad = self.optimizer.zero_grad
        
        @functools.wraps(original_zero_grad)
        def patched_zero_grad(*args, **kwargs):
            if self.tracing_active:
                self.trace_history.append({
                    "type": "optimizer_zero_grad",
                    "optimizer": type(self.optimizer).__name__,
                    "timestamp": time.time(),
                    "stack_trace": traceback.extract_stack(),
                })
            
            return original_zero_grad(*args, **kwargs)
        
        self.optimizer.zero_grad = patched_zero_grad
        
        # Store the original method for cleanup
        self.original_optimizer_zero_grad = original_zero_grad
    
    def analyze_trace(self) -> Dict[str, Any]:
        """
        Analyze the collected trace data.
        
        Returns:
            Analysis results
        """
        if not self.trace_history:
            return {"error": "No trace data available"}
        
        results = {
            "trace_count": len(self.trace_history),
            "forward_count": sum(1 for t in self.trace_history if t["type"] == "forward"),
            "backward_count": sum(1 for t in self.trace_history if t["type"] == "backward"),
            "optimizer_step_count": sum(1 for t in self.trace_history if t["type"] == "optimizer_step"),
            "optimizer_zero_grad_count": sum(1 for t in self.trace_history if t["type"] == "optimizer_zero_grad"),
            "issues": [],
        }
        
        # Check for missing zero_grad
        if results["optimizer_step_count"] > results["optimizer_zero_grad_count"]:
            results["issues"].append({
                "type": "missing_zero_grad",
                "description": "Some optimizer steps are performed without zeroing gradients",
                "severity": "high",
            })
        
        # Check for backward without optimizer step
        if results["backward_count"] > results["optimizer_step_count"]:
            results["issues"].append({
                "type": "missing_optimizer_step",
                "description": "Some backward passes are not followed by optimizer steps",
                "severity": "medium",
            })
        
        # Analyze timing
        if len(self.trace_history) > 1:
            # Calculate time spent in different phases
            forward_times = []
            backward_times = []
            optimizer_times = []
            
            for i in range(1, len(self.trace_history)):
                curr = self.trace_history[i]
                prev = self.trace_history[i-1]
                
                time_diff = curr["timestamp"] - prev["timestamp"]
                
                if prev["type"] == "forward_pre" and curr["type"] == "forward":
                    forward_times.append(time_diff)
                elif prev["type"] == "forward" and curr["type"] == "backward":
                    backward_times.append(time_diff)
                elif prev["type"] == "backward" and curr["type"] == "optimizer_step":
                    optimizer_times.append(time_diff)
            
            # Add timing results
            if forward_times:
                results["avg_forward_time"] = sum(forward_times) / len(forward_times)
            
            if backward_times:
                results["avg_backward_time"] = sum(backward_times) / len(backward_times)
            
            if optimizer_times:
                results["avg_optimizer_time"] = sum(optimizer_times) / len(optimizer_times)
            
            # Check for bottlenecks
            if "avg_forward_time" in results and "avg_backward_time" in results and "avg_optimizer_time" in results:
                total_time = results["avg_forward_time"] + results["avg_backward_time"] + results["avg_optimizer_time"]
                
                if results["avg_forward_time"] > 0.5 * total_time:
                    results["issues"].append({
                        "type": "forward_bottleneck",
                        "description": "Forward pass is taking a significant portion of iteration time",
                        "severity": "medium",
                        "metrics": {
                            "forward_time_pct": results["avg_forward_time"] / total_time * 100,
                        },
                    })
                
                if results["avg_backward_time"] > 0.5 * total_time:
                    results["issues"].append({
                        "type": "backward_bottleneck",
                        "description": "Backward pass is taking a significant portion of iteration time",
                        "severity": "medium",
                        "metrics": {
                            "backward_time_pct": results["avg_backward_time"] / total_time * 100,
                        },
                    })
                
                if results["avg_optimizer_time"] > 0.3 * total_time:
                    results["issues"].append({
                        "type": "optimizer_bottleneck",
                        "description": "Optimizer is taking a significant portion of iteration time",
                        "severity": "medium",
                        "metrics": {
                            "optimizer_time_pct": results["avg_optimizer_time"] / total_time * 100,
                        },
                    })
        
        return results
    
    def get_fault_trees(self) -> Dict[str, CausalFaultTree]:
        """
        Get all fault trees.
        
        Returns:
            Dictionary of fault trees
        """
        return self.fault_trees
    
    def get_active_tree(self) -> Optional[CausalFaultTree]:
        """
        Get the active fault tree.
        
        Returns:
            Active fault tree or None
        """
        return self.active_tree
    
    def set_active_tree(self, tree_id: str) -> None:
        """
        Set the active fault tree.
        
        Args:
            tree_id: ID of the tree to set as active
        """
        if tree_id in self.fault_trees:
            self.active_tree = self.fault_trees[tree_id]
        else:
            raise ValueError(f"Tree with ID {tree_id} not found")
    
    def visualize_tree(self, tree_id: Optional[str] = None, output_path: Optional[str] = None, show: bool = False) -> Optional[str]:
        """
        Visualize a fault tree.
        
        Args:
            tree_id: ID of the tree to visualize (uses active tree if None)
            output_path: Path to save the visualization
            show: Whether to show the visualization
            
        Returns:
            Path to the saved visualization or None
        """
        tree = None
        
        if tree_id is not None:
            tree = self.fault_trees.get(tree_id)
        else:
            tree = self.active_tree
        
        if tree is None:
            logger.warning("No tree to visualize")
            return None
        
        # Generate output path if not provided
        if output_path is None:
            output_dir = "/tmp/autopd_cfta"
            os.makedirs(output_dir, exist_ok=True)
            output_path = f"{output_dir}/fault_tree_{int(time.time())}.png"
        
        return tree.visualize(output_path=output_path, show=show)
    
    def get_event_log(self) -> List[Dict[str, Any]]:
        """
        Get the event log.
        
        Returns:
            List of events
        """
        return self.event_log
    
    def clear_event_log(self) -> None:
        """Clear the event log."""
        self.event_log = []
    
    def save_state(self, path: str) -> None:
        """
        Save the module state to a file.
        
        Args:
            path: Path to save the state
        """
        state = {
            "fault_trees": {tree_id: tree.to_dict() for tree_id, tree in self.fault_trees.items()},
            "active_tree": self.active_tree.to_dict() if self.active_tree else None,
            "event_log": self.event_log,
        }
        
        try:
            with open(path, 'w') as f:
                json.dump(state, f, indent=2)
            
            logger.info(f"Saved CausalFaultTreeAnalysis state to {path}")
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
            with open(path, 'r') as f:
                state = json.load(f)
            
            # Load fault trees
            self.fault_trees = {}
            for tree_id, tree_data in state["fault_trees"].items():
                self.fault_trees[tree_id] = CausalFaultTree.from_dict(tree_data)
            
            # Load active tree
            if state["active_tree"] is not None:
                active_tree_id = state["active_tree"]["root"]
                if active_tree_id in self.fault_trees:
                    self.active_tree = self.fault_trees[active_tree_id]
            
            # Load event log
            self.event_log = state["event_log"]
            
            logger.info(f"Loaded CausalFaultTreeAnalysis state from {path}")
            return True
        except Exception as e:
            logger.error(f"Failed to load state: {e}")
            return False
    
    def reset(self) -> None:
        """Reset the module state."""
        # Stop tracing if active
        if self.tracing_active:
            self.stop_tracing()
        
        # Clear data
        self.metrics_history = defaultdict(list)
        self.metrics_timestamps = []
        self.fault_trees = {}
        self.active_tree = None
        self.trace_history = []
        self.stack_traces = []
        self.event_log = []
        
        logger.info("Reset CausalFaultTreeAnalysis state")
