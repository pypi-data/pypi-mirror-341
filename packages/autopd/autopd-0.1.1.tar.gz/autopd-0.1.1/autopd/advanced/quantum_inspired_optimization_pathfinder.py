"""
Quantum-Inspired Optimization Pathfinder for AutoPipelineDoctor.

This module provides quantum-inspired optimization techniques for finding optimal
hyperparameters and training configurations in deep learning pipelines.
"""

import os
import time
import math
import random
import logging
import threading
import numpy as np
from typing import Dict, List, Optional, Union, Any, Tuple, Callable, Set
from collections import defaultdict, deque

import torch
import torch.nn as nn
from torch.optim import Optimizer

logger = logging.getLogger(__name__)


class QuantumInspiredOptimizationPathfinder:
    """
    Quantum-Inspired Optimization Pathfinder for deep learning pipelines.
    
    This class implements quantum-inspired optimization techniques to find optimal
    hyperparameters and training configurations for deep learning models. It uses
    quantum computing concepts like superposition, entanglement, and quantum annealing
    to efficiently explore the hyperparameter space and find optimal configurations.
    
    Attributes:
        model: The PyTorch model to optimize
        optimizer: The optimizer used for training
        search_space: The hyperparameter search space
        quantum_iterations: Number of quantum-inspired iterations
        population_size: Size of the quantum population
        interference_strength: Strength of quantum interference effects
        entanglement_factor: Factor controlling entanglement between parameters
        output_dir: Directory to save results
        running: Whether the pathfinder is currently running
        best_configs: List of best configurations found
        quantum_states: Current quantum states
        observation_history: History of observations
    """
    
    def __init__(
        self,
        model: nn.Module,
        optimizer: Optional[Optimizer] = None,
        search_space: Optional[Dict[str, Any]] = None,
        quantum_iterations: int = 100,
        population_size: int = 20,
        interference_strength: float = 0.3,
        entanglement_factor: float = 0.5,
        output_dir: Optional[str] = None,
    ):
        """
        Initialize the QuantumInspiredOptimizationPathfinder.
        
        Args:
            model: PyTorch model to optimize
            optimizer: Optimizer used for training (optional)
            search_space: Hyperparameter search space (optional)
            quantum_iterations: Number of quantum-inspired iterations
            population_size: Size of the quantum population
            interference_strength: Strength of quantum interference effects
            entanglement_factor: Factor controlling entanglement between parameters
            output_dir: Directory to save results (optional)
        """
        self.model = model
        self.optimizer = optimizer
        self.search_space = search_space or self._default_search_space()
        self.quantum_iterations = quantum_iterations
        self.population_size = population_size
        self.interference_strength = interference_strength
        self.entanglement_factor = entanglement_factor
        self.output_dir = output_dir or os.path.join(os.getcwd(), "quantum_pathfinder_output")
        
        # Create output directory if it doesn't exist
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Initialize quantum states and tracking variables
        self.running = False
        self.best_configs = []
        self.quantum_states = self._initialize_quantum_states()
        self.observation_history = []
        self.optimization_thread = None
        self.lock = threading.Lock()
        
        logger.info(f"Initialized QuantumInspiredOptimizationPathfinder with {population_size} quantum states")
    
    def _default_search_space(self) -> Dict[str, Any]:
        """
        Create default search space based on model and optimizer.
        
        Returns:
            Default hyperparameter search space
        """
        search_space = {
            "learning_rate": {
                "type": "continuous",
                "range": [1e-5, 1e-1],
                "log_scale": True
            },
            "batch_size": {
                "type": "discrete",
                "values": [8, 16, 32, 64, 128, 256]
            },
            "optimizer_type": {
                "type": "categorical",
                "values": ["SGD", "Adam", "AdamW", "RMSprop"]
            },
            "weight_decay": {
                "type": "continuous",
                "range": [1e-6, 1e-2],
                "log_scale": True
            },
            "dropout_rate": {
                "type": "continuous",
                "range": [0.0, 0.5],
                "log_scale": False
            },
            "activation_function": {
                "type": "categorical",
                "values": ["ReLU", "LeakyReLU", "GELU", "SiLU"]
            }
        }
        
        # Add model-specific parameters if possible
        if hasattr(self.model, "num_layers") and isinstance(getattr(self.model, "num_layers"), int):
            search_space["num_layers"] = {
                "type": "discrete",
                "values": list(range(1, getattr(self.model, "num_layers") * 2 + 1))
            }
        
        # Add optimizer-specific parameters
        if self.optimizer is not None:
            if isinstance(self.optimizer, torch.optim.Adam) or isinstance(self.optimizer, torch.optim.AdamW):
                search_space["beta1"] = {
                    "type": "continuous",
                    "range": [0.8, 0.999],
                    "log_scale": False
                }
                search_space["beta2"] = {
                    "type": "continuous",
                    "range": [0.9, 0.9999],
                    "log_scale": False
                }
            elif isinstance(self.optimizer, torch.optim.SGD):
                search_space["momentum"] = {
                    "type": "continuous",
                    "range": [0.0, 0.99],
                    "log_scale": False
                }
        
        return search_space
    
    def _initialize_quantum_states(self) -> List[Dict[str, Any]]:
        """
        Initialize quantum states for optimization.
        
        Returns:
            List of quantum states (hyperparameter configurations)
        """
        quantum_states = []
        
        for _ in range(self.population_size):
            state = {}
            
            # Sample random values for each parameter in the search space
            for param_name, param_config in self.search_space.items():
                if param_config["type"] == "continuous":
                    if param_config.get("log_scale", False):
                        log_min = math.log(param_config["range"][0])
                        log_max = math.log(param_config["range"][1])
                        value = math.exp(random.uniform(log_min, log_max))
                    else:
                        value = random.uniform(param_config["range"][0], param_config["range"][1])
                elif param_config["type"] == "discrete":
                    value = random.choice(param_config["values"])
                elif param_config["type"] == "categorical":
                    value = random.choice(param_config["values"])
                else:
                    raise ValueError(f"Unknown parameter type: {param_config['type']}")
                
                state[param_name] = value
            
            # Add quantum properties
            state["amplitude"] = complex(random.uniform(0, 1), random.uniform(0, 1))
            state["phase"] = random.uniform(0, 2 * math.pi)
            state["entanglement"] = {}
            
            quantum_states.append(state)
        
        # Initialize entanglement between parameters
        self._initialize_entanglement(quantum_states)
        
        return quantum_states
    
    def _initialize_entanglement(self, quantum_states: List[Dict[str, Any]]) -> None:
        """
        Initialize entanglement between parameters in quantum states.
        
        Args:
            quantum_states: List of quantum states to initialize entanglement for
        """
        param_names = list(self.search_space.keys())
        
        for state in quantum_states:
            # Create entanglement between random pairs of parameters
            num_entangled_pairs = int(len(param_names) * self.entanglement_factor)
            
            for _ in range(num_entangled_pairs):
                param1, param2 = random.sample(param_names, 2)
                
                if param1 not in state["entanglement"]:
                    state["entanglement"][param1] = []
                
                state["entanglement"][param1].append({
                    "param": param2,
                    "strength": random.uniform(0.1, 0.9),
                    "phase": random.uniform(0, 2 * math.pi)
                })
    
    def start(self) -> None:
        """Start the quantum-inspired optimization process in a separate thread."""
        if self.running:
            logger.warning("Quantum-Inspired Optimization Pathfinder is already running")
            return
        
        self.running = True
        self.optimization_thread = threading.Thread(target=self._optimization_loop)
        self.optimization_thread.daemon = True
        self.optimization_thread.start()
        
        logger.info("Started Quantum-Inspired Optimization Pathfinder")
    
    def stop(self) -> None:
        """Stop the quantum-inspired optimization process."""
        if not self.running:
            logger.warning("Quantum-Inspired Optimization Pathfinder is not running")
            return
        
        self.running = False
        if self.optimization_thread is not None:
            self.optimization_thread.join(timeout=5.0)
        
        logger.info("Stopped Quantum-Inspired Optimization Pathfinder")
    
    def _optimization_loop(self) -> None:
        """Main optimization loop implementing quantum-inspired algorithms."""
        iteration = 0
        
        while self.running and iteration < self.quantum_iterations:
            logger.info(f"Quantum optimization iteration {iteration + 1}/{self.quantum_iterations}")
            
            # Apply quantum operations
            self._apply_quantum_superposition()
            self._apply_quantum_interference()
            self._apply_quantum_entanglement()
            
            # Measure quantum states to get classical configurations
            configurations = self._measure_quantum_states()
            
            # Evaluate configurations
            evaluations = self._evaluate_configurations(configurations)
            
            # Update quantum states based on evaluations
            self._update_quantum_states(evaluations)
            
            # Record best configurations
            self._record_best_configurations(evaluations)
            
            iteration += 1
            
            # Sleep to avoid consuming too many resources
            time.sleep(0.1)
        
        logger.info(f"Completed {iteration} quantum optimization iterations")
        
        # Final measurement to get best configurations
        if self.running:
            self._finalize_optimization()
    
    def _apply_quantum_superposition(self) -> None:
        """Apply quantum superposition operation to quantum states."""
        with self.lock:
            for state in self.quantum_states:
                # Update amplitudes with random fluctuations
                amplitude = state["amplitude"]
                phase = state["phase"]
                
                # Apply Hadamard-like transformation
                new_real = (amplitude.real + amplitude.imag) / math.sqrt(2)
                new_imag = (amplitude.real - amplitude.imag) / math.sqrt(2)
                
                # Add quantum fluctuations
                new_real += random.gauss(0, 0.1)
                new_imag += random.gauss(0, 0.1)
                
                # Normalize
                norm = math.sqrt(new_real**2 + new_imag**2)
                if norm > 0:
                    new_real /= norm
                    new_imag /= norm
                
                state["amplitude"] = complex(new_real, new_imag)
                state["phase"] = (phase + random.uniform(0, math.pi/4)) % (2 * math.pi)
    
    def _apply_quantum_interference(self) -> None:
        """Apply quantum interference operation to quantum states."""
        with self.lock:
            # Create interference between quantum states
            for i in range(len(self.quantum_states)):
                for j in range(i + 1, len(self.quantum_states)):
                    state_i = self.quantum_states[i]
                    state_j = self.quantum_states[j]
                    
                    # Calculate interference strength based on similarity
                    similarity = self._calculate_state_similarity(state_i, state_j)
                    interference = similarity * self.interference_strength
                    
                    # Apply interference effect
                    phase_diff = (state_i["phase"] - state_j["phase"]) % (2 * math.pi)
                    
                    # Update amplitudes based on interference
                    amp_i = state_i["amplitude"]
                    amp_j = state_j["amplitude"]
                    
                    # Constructive/destructive interference based on phase difference
                    interference_factor = math.cos(phase_diff)
                    
                    new_amp_i = amp_i + interference * interference_factor * amp_j
                    new_amp_j = amp_j + interference * interference_factor * amp_i
                    
                    # Normalize
                    norm_i = abs(new_amp_i)
                    norm_j = abs(new_amp_j)
                    
                    if norm_i > 0:
                        new_amp_i /= norm_i
                    if norm_j > 0:
                        new_amp_j /= norm_j
                    
                    state_i["amplitude"] = new_amp_i
                    state_j["amplitude"] = new_amp_j
    
    def _apply_quantum_entanglement(self) -> None:
        """Apply quantum entanglement operation to quantum states."""
        with self.lock:
            for state in self.quantum_states:
                # Apply entanglement effects
                for param1, entanglements in state["entanglement"].items():
                    for entanglement in entanglements:
                        param2 = entanglement["param"]
                        strength = entanglement["strength"]
                        phase = entanglement["phase"]
                        
                        # Skip if either parameter is not in search space
                        if param1 not in self.search_space or param2 not in self.search_space:
                            continue
                        
                        # Apply entanglement effect based on parameter types
                        param1_config = self.search_space[param1]
                        param2_config = self.search_space[param2]
                        
                        if param1_config["type"] == "continuous" and param2_config["type"] == "continuous":
                            # Continuous parameters: apply correlated changes
                            range1 = param1_config["range"]
                            range2 = param2_config["range"]
                            
                            # Calculate normalized positions in ranges
                            norm_pos1 = (state[param1] - range1[0]) / (range1[1] - range1[0])
                            norm_pos2 = (state[param2] - range2[0]) / (range2[1] - range2[0])
                            
                            # Apply entanglement effect
                            entanglement_effect = strength * math.sin(phase) * (norm_pos1 - 0.5)
                            new_norm_pos2 = norm_pos2 + entanglement_effect
                            new_norm_pos2 = max(0, min(1, new_norm_pos2))
                            
                            # Convert back to actual parameter value
                            state[param2] = range2[0] + new_norm_pos2 * (range2[1] - range2[0])
                            
                            # Apply log scaling if needed
                            if param2_config.get("log_scale", False):
                                log_min = math.log(range2[0])
                                log_max = math.log(range2[1])
                                log_value = log_min + new_norm_pos2 * (log_max - log_min)
                                state[param2] = math.exp(log_value)
    
    def _calculate_state_similarity(self, state1: Dict[str, Any], state2: Dict[str, Any]) -> float:
        """
        Calculate similarity between two quantum states.
        
        Args:
            state1: First quantum state
            state2: Second quantum state
            
        Returns:
            Similarity score between 0 and 1
        """
        similarities = []
        
        for param_name, param_config in self.search_space.items():
            if param_name not in state1 or param_name not in state2:
                continue
            
            if param_config["type"] == "continuous":
                # For continuous parameters, calculate normalized distance
                range_min, range_max = param_config["range"]
                range_size = range_max - range_min
                
                if range_size > 0:
                    if param_config.get("log_scale", False):
                        # Log scale: calculate distance in log space
                        log_min = math.log(range_min)
                        log_max = math.log(range_max)
                        log_range = log_max - log_min
                        
                        log_val1 = math.log(max(state1[param_name], range_min))
                        log_val2 = math.log(max(state2[param_name], range_min))
                        
                        distance = abs(log_val1 - log_val2) / log_range
                    else:
                        # Linear scale
                        distance = abs(state1[param_name] - state2[param_name]) / range_size
                    
                    similarity = 1.0 - min(1.0, distance)
                    similarities.append(similarity)
            
            elif param_config["type"] == "discrete":
                # For discrete parameters, calculate normalized distance
                values = param_config["values"]
                if len(values) > 1:
                    idx1 = values.index(state1[param_name]) if state1[param_name] in values else 0
                    idx2 = values.index(state2[param_name]) if state2[param_name] in values else 0
                    
                    distance = abs(idx1 - idx2) / (len(values) - 1)
                    similarity = 1.0 - min(1.0, distance)
                    similarities.append(similarity)
            
            elif param_config["type"] == "categorical":
                # For categorical parameters, binary similarity
                similarity = 1.0 if state1[param_name] == state2[param_name] else 0.0
                similarities.append(similarity)
        
        # Return average similarity across all parameters
        return sum(similarities) / len(similarities) if similarities else 0.0
    
    def _measure_quantum_states(self) -> List[Dict[str, Any]]:
        """
        Measure quantum states to get classical configurations.
        
        Returns:
            List of classical configurations
        """
        configurations = []
        
        with self.lock:
            for state in self.quantum_states:
                # Create a classical configuration from the quantum state
                config = {}
                
                for param_name, param_config in self.search_space.items():
                    if param_name not in state:
                        continue
                    
                    # Apply quantum collapse based on amplitude and phase
                    amplitude = abs(state["amplitude"])
                    phase = state["phase"]
                    
                    if param_config["type"] == "continuous":
                        range_min, range_max = param_config["range"]
                        
                        # Apply quantum fluctuation based on amplitude and phase
                        fluctuation = amplitude * math.sin(phase) * 0.2
                        
                        # Get base value and apply fluctuation
                        base_value = state[param_name]
                        value = base_value * (1.0 + fluctuation)
                        
                        # Ensure value is within range
                        value = max(range_min, min(range_max, value))
                        
                        config[param_name] = value
                    
                    elif param_config["type"] == "discrete":
                        values = param_config["values"]
                        current_idx = values.index(state[param_name]) if state[param_name] in values else 0
                        
                        # Apply quantum fluctuation to index
                        fluctuation = int(amplitude * math.sin(phase) * len(values) * 0.2)
                        new_idx = (current_idx + fluctuation) % len(values)
                        
                        config[param_name] = values[new_idx]
                    
                    elif param_config["type"] == "categorical":
                        # For categorical, we either keep the current value or randomly select another
                        if random.random() < amplitude:
                            config[param_name] = state[param_name]
                        else:
                            values = [v for v in param_config["values"] if v != state[param_name]]
                            if values:
                                config[param_name] = random.choice(values)
                            else:
                                config[param_name] = state[param_name]
                
                configurations.append(config)
        
        return configurations
    
    def _evaluate_configurations(self, configurations: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Evaluate configurations using a surrogate model or heuristics.
        
        Args:
            configurations: List of hyperparameter configurations to evaluate
            
        Returns:
            List of configurations with evaluation scores
        """
        evaluations = []
        
        for config in configurations:
            # Create a copy of the configuration for evaluation
            evaluation = config.copy()
            
            # Calculate a heuristic score based on known best practices
            score = self._calculate_heuristic_score(config)
            
            # Add evaluation metrics
            evaluation["score"] = score
            evaluation["evaluated"] = True
            
            evaluations.append(evaluation)
        
        return evaluations
    
    def _calculate_heuristic_score(self, config: Dict[str, Any]) -> float:
        """
        Calculate a heuristic score for a configuration based on best practices.
        
        Args:
            config: Hyperparameter configuration to evaluate
            
        Returns:
            Heuristic score between 0 and 1
        """
        score_components = []
        
        # Learning rate heuristics
        if "learning_rate" in config:
            lr = config["learning_rate"]
            
            # Penalize extremely small or large learning rates
            if lr < 1e-6:
                lr_score = 0.2
            elif lr < 1e-4:
                lr_score = 0.6
            elif lr < 1e-2:
                lr_score = 0.9
            elif lr < 5e-2:
                lr_score = 0.7
            else:
                lr_score = 0.3
            
            score_components.append(lr_score)
        
        # Batch size heuristics
        if "batch_size" in config:
            batch_size = config["batch_size"]
            
            # Prefer moderate batch sizes
            if batch_size < 8:
                batch_score = 0.3
            elif batch_size < 32:
                batch_score = 0.7
            elif batch_size < 128:
                batch_score = 0.9
            elif batch_size < 256:
                batch_score = 0.7
            else:
                batch_score = 0.5
            
            score_components.append(batch_score)
        
        # Optimizer heuristics
        if "optimizer_type" in config:
            optimizer_type = config["optimizer_type"]
            
            # Prefer adaptive optimizers
            if optimizer_type == "Adam" or optimizer_type == "AdamW":
                optimizer_score = 0.9
            elif optimizer_type == "RMSprop":
                optimizer_score = 0.8
            elif optimizer_type == "SGD":
                optimizer_score = 0.6
            else:
                optimizer_score = 0.5
            
            score_components.append(optimizer_score)
        
        # Weight decay heuristics
        if "weight_decay" in config:
            weight_decay = config["weight_decay"]
            
            # Prefer moderate weight decay
            if weight_decay < 1e-5:
                wd_score = 0.4
            elif weight_decay < 1e-4:
                wd_score = 0.7
            elif weight_decay < 1e-3:
                wd_score = 0.9
            elif weight_decay < 1e-2:
                wd_score = 0.6
            else:
                wd_score = 0.3
            
            score_components.append(wd_score)
        
        # Dropout rate heuristics
        if "dropout_rate" in config:
            dropout_rate = config["dropout_rate"]
            
            # Prefer moderate dropout rates
            if dropout_rate < 0.1:
                dropout_score = 0.5
            elif dropout_rate < 0.3:
                dropout_score = 0.9
            elif dropout_rate < 0.5:
                dropout_score = 0.7
            else:
                dropout_score = 0.4
            
            score_components.append(dropout_score)
        
        # Activation function heuristics
        if "activation_function" in config:
            activation = config["activation_function"]
            
            # Prefer modern activation functions
            if activation == "GELU" or activation == "SiLU":
                activation_score = 0.9
            elif activation == "LeakyReLU":
                activation_score = 0.8
            elif activation == "ReLU":
                activation_score = 0.7
            else:
                activation_score = 0.5
            
            score_components.append(activation_score)
        
        # Calculate overall score as weighted average
        if score_components:
            # Add some randomness to avoid getting stuck in local optima
            randomness = random.uniform(0.9, 1.1)
            score = sum(score_components) / len(score_components) * randomness
            
            # Ensure score is between 0 and 1
            score = max(0.0, min(1.0, score))
            return score
        else:
            return random.uniform(0.3, 0.7)  # Return random score if no components
    
    def _update_quantum_states(self, evaluations: List[Dict[str, Any]]) -> None:
        """
        Update quantum states based on evaluation results.
        
        Args:
            evaluations: List of evaluated configurations
        """
        with self.lock:
            # Sort evaluations by score
            sorted_evaluations = sorted(evaluations, key=lambda x: x.get("score", 0), reverse=True)
            
            # Update quantum states based on evaluations
            for i, (state, evaluation) in enumerate(zip(self.quantum_states, sorted_evaluations)):
                # Update parameter values
                for param_name in self.search_space.keys():
                    if param_name in evaluation:
                        state[param_name] = evaluation[param_name]
                
                # Update quantum properties based on score
                score = evaluation.get("score", 0)
                
                # Higher scores get higher amplitudes
                amplitude = math.sqrt(score) * (1.0 - i / len(self.quantum_states) * 0.5)
                state["amplitude"] = complex(amplitude, amplitude * 0.5)
                
                # Update phase based on score
                state["phase"] = score * math.pi
                
                # Update entanglement based on score
                if score > 0.7:
                    # Increase entanglement for promising states
                    self._strengthen_entanglement(state)
                elif score < 0.3:
                    # Decrease entanglement for poor states
                    self._weaken_entanglement(state)
    
    def _strengthen_entanglement(self, state: Dict[str, Any]) -> None:
        """
        Strengthen entanglement in a quantum state.
        
        Args:
            state: Quantum state to strengthen entanglement for
        """
        param_names = list(self.search_space.keys())
        
        # Add new entangled pairs
        for _ in range(2):
            if len(param_names) >= 2:
                param1, param2 = random.sample(param_names, 2)
                
                if param1 not in state["entanglement"]:
                    state["entanglement"][param1] = []
                
                # Check if this pair already exists
                exists = False
                for e in state["entanglement"][param1]:
                    if e["param"] == param2:
                        # Increase strength
                        e["strength"] = min(0.95, e["strength"] * 1.2)
                        exists = True
                        break
                
                # Add new entanglement if it doesn't exist
                if not exists:
                    state["entanglement"][param1].append({
                        "param": param2,
                        "strength": random.uniform(0.5, 0.8),
                        "phase": random.uniform(0, 2 * math.pi)
                    })
    
    def _weaken_entanglement(self, state: Dict[str, Any]) -> None:
        """
        Weaken entanglement in a quantum state.
        
        Args:
            state: Quantum state to weaken entanglement for
        """
        # Reduce strength of existing entanglements
        for param1 in list(state["entanglement"].keys()):
            entanglements = state["entanglement"][param1]
            
            for i, e in enumerate(entanglements):
                # Reduce strength
                e["strength"] *= 0.8
                
                # Remove if too weak
                if e["strength"] < 0.1:
                    entanglements.pop(i)
            
            # Remove empty lists
            if not entanglements:
                del state["entanglement"][param1]
    
    def _record_best_configurations(self, evaluations: List[Dict[str, Any]]) -> None:
        """
        Record best configurations from evaluations.
        
        Args:
            evaluations: List of evaluated configurations
        """
        # Sort evaluations by score
        sorted_evaluations = sorted(evaluations, key=lambda x: x.get("score", 0), reverse=True)
        
        # Take top configurations
        top_configs = sorted_evaluations[:3]
        
        with self.lock:
            # Add to best configurations if they're good enough
            for config in top_configs:
                score = config.get("score", 0)
                
                if score > 0.7:  # Only record good configurations
                    # Create a clean copy without quantum properties
                    clean_config = {k: v for k, v in config.items() if k in self.search_space}
                    clean_config["score"] = score
                    clean_config["timestamp"] = time.time()
                    
                    # Add to best configurations if not already present
                    if not any(self._config_similarity(clean_config, bc) > 0.9 for bc in self.best_configs):
                        self.best_configs.append(clean_config)
            
            # Keep only top configurations
            self.best_configs = sorted(self.best_configs, key=lambda x: x.get("score", 0), reverse=True)[:10]
    
    def _config_similarity(self, config1: Dict[str, Any], config2: Dict[str, Any]) -> float:
        """
        Calculate similarity between two configurations.
        
        Args:
            config1: First configuration
            config2: Second configuration
            
        Returns:
            Similarity score between 0 and 1
        """
        # Use the same similarity calculation as for quantum states
        param_keys = set(config1.keys()).intersection(set(config2.keys())).intersection(set(self.search_space.keys()))
        
        if not param_keys:
            return 0.0
        
        similarities = []
        
        for param_name in param_keys:
            param_config = self.search_space[param_name]
            
            if param_config["type"] == "continuous":
                # For continuous parameters, calculate normalized distance
                range_min, range_max = param_config["range"]
                range_size = range_max - range_min
                
                if range_size > 0:
                    if param_config.get("log_scale", False):
                        # Log scale: calculate distance in log space
                        log_min = math.log(range_min)
                        log_max = math.log(range_max)
                        log_range = log_max - log_min
                        
                        log_val1 = math.log(max(config1[param_name], range_min))
                        log_val2 = math.log(max(config2[param_name], range_min))
                        
                        distance = abs(log_val1 - log_val2) / log_range
                    else:
                        # Linear scale
                        distance = abs(config1[param_name] - config2[param_name]) / range_size
                    
                    similarity = 1.0 - min(1.0, distance)
                    similarities.append(similarity)
            
            elif param_config["type"] == "discrete" or param_config["type"] == "categorical":
                # For discrete and categorical parameters, binary similarity
                similarity = 1.0 if config1[param_name] == config2[param_name] else 0.0
                similarities.append(similarity)
        
        # Return average similarity across all parameters
        return sum(similarities) / len(similarities) if similarities else 0.0
    
    def _finalize_optimization(self) -> None:
        """Finalize optimization and save results."""
        logger.info("Finalizing quantum optimization")
        
        # Save best configurations to file
        self._save_best_configurations()
        
        # Generate optimization report
        self._generate_optimization_report()
        
        logger.info(f"Optimization completed, found {len(self.best_configs)} promising configurations")
    
    def _save_best_configurations(self) -> None:
        """Save best configurations to file."""
        if not self.best_configs:
            logger.warning("No best configurations to save")
            return
        
        # Create output file
        output_file = os.path.join(self.output_dir, "best_configurations.txt")
        
        with open(output_file, "w") as f:
            f.write("# Quantum-Inspired Optimization Pathfinder: Best Configurations\n\n")
            
            for i, config in enumerate(self.best_configs):
                f.write(f"## Configuration {i+1} (Score: {config.get('score', 0):.4f})\n\n")
                
                for param_name, value in sorted(config.items()):
                    if param_name in self.search_space:
                        f.write(f"- {param_name}: {value}\n")
                
                f.write("\n")
        
        logger.info(f"Saved best configurations to {output_file}")
    
    def _generate_optimization_report(self) -> None:
        """Generate optimization report."""
        # Create output file
        output_file = os.path.join(self.output_dir, "optimization_report.txt")
        
        with open(output_file, "w") as f:
            f.write("# Quantum-Inspired Optimization Pathfinder: Report\n\n")
            
            f.write("## Optimization Settings\n\n")
            f.write(f"- Quantum Iterations: {self.quantum_iterations}\n")
            f.write(f"- Population Size: {self.population_size}\n")
            f.write(f"- Interference Strength: {self.interference_strength}\n")
            f.write(f"- Entanglement Factor: {self.entanglement_factor}\n\n")
            
            f.write("## Search Space\n\n")
            for param_name, param_config in self.search_space.items():
                f.write(f"### {param_name}\n")
                f.write(f"- Type: {param_config['type']}\n")
                
                if param_config["type"] == "continuous":
                    f.write(f"- Range: [{param_config['range'][0]}, {param_config['range'][1]}]\n")
                    f.write(f"- Log Scale: {param_config.get('log_scale', False)}\n")
                else:
                    f.write(f"- Values: {param_config['values']}\n")
                
                f.write("\n")
            
            f.write("## Best Configurations\n\n")
            
            if self.best_configs:
                for i, config in enumerate(self.best_configs[:5]):  # Show top 5
                    f.write(f"### Configuration {i+1} (Score: {config.get('score', 0):.4f})\n\n")
                    
                    for param_name, value in sorted(config.items()):
                        if param_name in self.search_space:
                            f.write(f"- {param_name}: {value}\n")
                    
                    f.write("\n")
            else:
                f.write("No best configurations found.\n\n")
            
            f.write("## Optimization Insights\n\n")
            f.write(self._generate_optimization_insights())
        
        logger.info(f"Generated optimization report at {output_file}")
    
    def _generate_optimization_insights(self) -> str:
        """
        Generate insights from the optimization process.
        
        Returns:
            String containing optimization insights
        """
        insights = []
        
        # Only generate insights if we have best configurations
        if not self.best_configs:
            return "Insufficient data to generate insights."
        
        # Analyze parameter distributions in best configurations
        param_distributions = {}
        
        for param_name in self.search_space.keys():
            values = [config[param_name] for config in self.best_configs if param_name in config]
            
            if not values:
                continue
            
            param_config = self.search_space[param_name]
            
            if param_config["type"] == "continuous":
                # For continuous parameters, calculate statistics
                mean_value = sum(values) / len(values)
                min_value = min(values)
                max_value = max(values)
                
                param_distributions[param_name] = {
                    "mean": mean_value,
                    "min": min_value,
                    "max": max_value
                }
                
                # Generate insight
                insights.append(f"- {param_name}: Optimal values appear to be around {mean_value:.6f} (range: {min_value:.6f} to {max_value:.6f})")
            
            elif param_config["type"] == "discrete" or param_config["type"] == "categorical":
                # For discrete and categorical parameters, count occurrences
                value_counts = {}
                for value in values:
                    value_counts[value] = value_counts.get(value, 0) + 1
                
                # Find most common value
                most_common = max(value_counts.items(), key=lambda x: x[1])
                
                param_distributions[param_name] = {
                    "most_common": most_common[0],
                    "count": most_common[1],
                    "total": len(values)
                }
                
                # Generate insight
                percentage = most_common[1] / len(values) * 100
                insights.append(f"- {param_name}: {most_common[0]} appears in {percentage:.1f}% of top configurations")
        
        # Generate overall insights
        if insights:
            overall_insights = "Based on the quantum optimization process, the following insights were identified:\n\n"
            overall_insights += "\n".join(insights)
            
            # Add recommendations
            overall_insights += "\n\nRecommendations:\n\n"
            
            if self.best_configs:
                best_config = self.best_configs[0]
                overall_insights += "1. Try the top configuration:\n"
                
                for param_name, value in sorted(best_config.items()):
                    if param_name in self.search_space:
                        overall_insights += f"   - {param_name}: {value}\n"
                
                overall_insights += "\n2. Consider exploring these parameter ranges:\n"
                
                for param_name, dist in param_distributions.items():
                    param_config = self.search_space[param_name]
                    
                    if param_config["type"] == "continuous":
                        overall_insights += f"   - {param_name}: {dist['min']:.6f} to {dist['max']:.6f}\n"
            
            return overall_insights
        else:
            return "Insufficient data to generate meaningful insights."
    
    def get_best_configurations(self, top_n: int = 5) -> List[Dict[str, Any]]:
        """
        Get the best configurations found by the optimizer.
        
        Args:
            top_n: Number of top configurations to return
            
        Returns:
            List of best configurations
        """
        with self.lock:
            # Return top N configurations
            return self.best_configs[:top_n]
    
    def get_optimization_status(self) -> Dict[str, Any]:
        """
        Get the current status of the optimization process.
        
        Returns:
            Dictionary containing optimization status
        """
        with self.lock:
            return {
                "running": self.running,
                "num_best_configs": len(self.best_configs),
                "top_score": self.best_configs[0].get("score", 0) if self.best_configs else 0,
                "quantum_states": len(self.quantum_states),
                "output_dir": self.output_dir
            }
    
    def apply_best_configuration(self, model: Optional[nn.Module] = None, optimizer: Optional[Optimizer] = None) -> Dict[str, Any]:
        """
        Apply the best configuration to the model and optimizer.
        
        Args:
            model: PyTorch model to apply configuration to (optional)
            optimizer: Optimizer to apply configuration to (optional)
            
        Returns:
            Dictionary containing applied configuration and results
        """
        if not self.best_configs:
            logger.warning("No best configurations available to apply")
            return {"success": False, "reason": "No best configurations available"}
        
        # Get best configuration
        best_config = self.best_configs[0]
        
        # Use provided model and optimizer or fall back to initialized ones
        model = model or self.model
        optimizer = optimizer or self.optimizer
        
        if model is None:
            logger.warning("No model provided to apply configuration to")
            return {"success": False, "reason": "No model provided"}
        
        applied_changes = {}
        
        # Apply configuration to model if possible
        if "activation_function" in best_config:
            activation = best_config["activation_function"]
            applied_changes["activation_function"] = self._apply_activation_function(model, activation)
        
        if "dropout_rate" in best_config:
            dropout_rate = best_config["dropout_rate"]
            applied_changes["dropout_rate"] = self._apply_dropout_rate(model, dropout_rate)
        
        # Apply configuration to optimizer if possible
        if optimizer is not None and "learning_rate" in best_config:
            lr = best_config["learning_rate"]
            applied_changes["learning_rate"] = self._apply_learning_rate(optimizer, lr)
        
        if optimizer is not None and "weight_decay" in best_config:
            weight_decay = best_config["weight_decay"]
            applied_changes["weight_decay"] = self._apply_weight_decay(optimizer, weight_decay)
        
        # Return results
        return {
            "success": True,
            "applied_config": best_config,
            "applied_changes": applied_changes
        }
    
    def _apply_activation_function(self, model: nn.Module, activation: str) -> Dict[str, Any]:
        """
        Apply activation function to model.
        
        Args:
            model: PyTorch model to apply activation function to
            activation: Activation function name
            
        Returns:
            Dictionary containing results
        """
        activation_map = {
            "ReLU": nn.ReLU,
            "LeakyReLU": nn.LeakyReLU,
            "GELU": nn.GELU,
            "SiLU": nn.SiLU
        }
        
        if activation not in activation_map:
            return {"success": False, "reason": f"Unknown activation function: {activation}"}
        
        activation_class = activation_map[activation]
        count = 0
        
        # Replace activation functions in model
        for name, module in list(model.named_children()):
            if isinstance(module, nn.ReLU) or isinstance(module, nn.LeakyReLU) or \
               isinstance(module, nn.GELU) or isinstance(module, nn.SiLU):
                setattr(model, name, activation_class())
                count += 1
            else:
                # Recursively apply to child modules
                child_result = self._apply_activation_function(module, activation)
                count += child_result.get("count", 0)
        
        return {"success": True, "count": count}
    
    def _apply_dropout_rate(self, model: nn.Module, dropout_rate: float) -> Dict[str, Any]:
        """
        Apply dropout rate to model.
        
        Args:
            model: PyTorch model to apply dropout rate to
            dropout_rate: Dropout rate
            
        Returns:
            Dictionary containing results
        """
        count = 0
        
        # Replace dropout layers in model
        for name, module in list(model.named_children()):
            if isinstance(module, nn.Dropout):
                setattr(model, name, nn.Dropout(p=dropout_rate))
                count += 1
            else:
                # Recursively apply to child modules
                child_result = self._apply_dropout_rate(module, dropout_rate)
                count += child_result.get("count", 0)
        
        return {"success": True, "count": count}
    
    def _apply_learning_rate(self, optimizer: Optimizer, lr: float) -> Dict[str, Any]:
        """
        Apply learning rate to optimizer.
        
        Args:
            optimizer: PyTorch optimizer to apply learning rate to
            lr: Learning rate
            
        Returns:
            Dictionary containing results
        """
        count = 0
        
        # Update learning rate for all parameter groups
        for param_group in optimizer.param_groups:
            param_group["lr"] = lr
            count += 1
        
        return {"success": True, "count": count}
    
    def _apply_weight_decay(self, optimizer: Optimizer, weight_decay: float) -> Dict[str, Any]:
        """
        Apply weight decay to optimizer.
        
        Args:
            optimizer: PyTorch optimizer to apply weight decay to
            weight_decay: Weight decay
            
        Returns:
            Dictionary containing results
        """
        count = 0
        
        # Update weight decay for all parameter groups
        for param_group in optimizer.param_groups:
            if "weight_decay" in param_group:
                param_group["weight_decay"] = weight_decay
                count += 1
        
        return {"success": True, "count": count}
    
    def visualize_optimization_landscape(self) -> Dict[str, Any]:
        """
        Visualize the optimization landscape.
        
        Returns:
            Dictionary containing visualization data
        """
        if not self.best_configs:
            logger.warning("No configurations available for visualization")
            return {"success": False, "reason": "No configurations available"}
        
        # Select two most important parameters for visualization
        param_importance = self._calculate_parameter_importance()
        
        if len(param_importance) < 2:
            logger.warning("Not enough parameters for visualization")
            return {"success": False, "reason": "Not enough parameters"}
        
        # Get top two parameters
        top_params = sorted(param_importance.items(), key=lambda x: x[1], reverse=True)[:2]
        param1, param2 = top_params[0][0], top_params[1][0]
        
        # Create grid for visualization
        grid_size = 20
        param1_config = self.search_space[param1]
        param2_config = self.search_space[param2]
        
        # Generate grid points
        grid_points = []
        
        if param1_config["type"] == "continuous" and param2_config["type"] == "continuous":
            # For continuous parameters, create a grid of values
            param1_range = param1_config["range"]
            param2_range = param2_config["range"]
            
            if param1_config.get("log_scale", False):
                param1_values = np.logspace(np.log10(param1_range[0]), np.log10(param1_range[1]), grid_size)
            else:
                param1_values = np.linspace(param1_range[0], param1_range[1], grid_size)
            
            if param2_config.get("log_scale", False):
                param2_values = np.logspace(np.log10(param2_range[0]), np.log10(param2_range[1]), grid_size)
            else:
                param2_values = np.linspace(param2_range[0], param2_range[1], grid_size)
            
            for p1 in param1_values:
                for p2 in param2_values:
                    grid_points.append({param1: p1, param2: p2})
        else:
            # For discrete or categorical parameters, use all combinations
            if param1_config["type"] == "continuous":
                param1_range = param1_config["range"]
                if param1_config.get("log_scale", False):
                    param1_values = np.logspace(np.log10(param1_range[0]), np.log10(param1_range[1]), grid_size)
                else:
                    param1_values = np.linspace(param1_range[0], param1_range[1], grid_size)
            else:
                param1_values = param1_config["values"]
            
            if param2_config["type"] == "continuous":
                param2_range = param2_config["range"]
                if param2_config.get("log_scale", False):
                    param2_values = np.logspace(np.log10(param2_range[0]), np.log10(param2_range[1]), grid_size)
                else:
                    param2_values = np.linspace(param2_range[0], param2_range[1], grid_size)
            else:
                param2_values = param2_config["values"]
            
            for p1 in param1_values:
                for p2 in param2_values:
                    grid_points.append({param1: p1, param2: p2})
        
        # Evaluate grid points
        grid_scores = []
        
        for point in grid_points:
            # Create a complete configuration by using best values for other parameters
            config = self.best_configs[0].copy() if self.best_configs else {}
            config.update(point)
            
            # Calculate score
            score = self._calculate_heuristic_score(config)
            grid_scores.append(score)
        
        # Create visualization data
        visualization = {
            "success": True,
            "param1": param1,
            "param2": param2,
            "param1_values": param1_values.tolist() if isinstance(param1_values, np.ndarray) else param1_values,
            "param2_values": param2_values.tolist() if isinstance(param2_values, np.ndarray) else param2_values,
            "scores": grid_scores,
            "best_points": [
                {param1: config[param1], param2: config[param2], "score": config.get("score", 0)}
                for config in self.best_configs[:5]
                if param1 in config and param2 in config
            ]
        }
        
        return visualization
    
    def _calculate_parameter_importance(self) -> Dict[str, float]:
        """
        Calculate importance of each parameter based on best configurations.
        
        Returns:
            Dictionary mapping parameter names to importance scores
        """
        if not self.best_configs:
            return {}
        
        # Calculate variance of each parameter in best configurations
        param_variances = {}
        
        for param_name in self.search_space.keys():
            values = [config[param_name] for config in self.best_configs if param_name in config]
            
            if not values:
                continue
            
            param_config = self.search_space[param_name]
            
            if param_config["type"] == "continuous":
                # For continuous parameters, calculate normalized variance
                mean = sum(values) / len(values)
                variance = sum((v - mean) ** 2 for v in values) / len(values)
                
                # Normalize by parameter range
                range_min, range_max = param_config["range"]
                range_size = range_max - range_min
                
                if range_size > 0:
                    normalized_variance = variance / (range_size ** 2)
                    
                    # Invert variance to get importance (lower variance = higher importance)
                    importance = 1.0 / (1.0 + normalized_variance)
                    param_variances[param_name] = importance
            
            elif param_config["type"] == "discrete" or param_config["type"] == "categorical":
                # For discrete and categorical parameters, calculate entropy
                value_counts = {}
                for value in values:
                    value_counts[value] = value_counts.get(value, 0) + 1
                
                # Calculate entropy
                entropy = 0
                for count in value_counts.values():
                    p = count / len(values)
                    entropy -= p * math.log2(p)
                
                # Normalize entropy by maximum possible entropy
                max_entropy = math.log2(len(set(values)))
                
                if max_entropy > 0:
                    normalized_entropy = entropy / max_entropy
                    
                    # Invert entropy to get importance (lower entropy = higher importance)
                    importance = 1.0 - normalized_entropy
                    param_variances[param_name] = importance
        
        return param_variances
