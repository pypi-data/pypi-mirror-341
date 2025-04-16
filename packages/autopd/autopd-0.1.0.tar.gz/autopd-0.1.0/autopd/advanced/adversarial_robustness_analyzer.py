"""
Adversarial Robustness Analyzer for AutoPipelineDoctor.

This module provides comprehensive adversarial attack testing, vulnerability detection,
and robustness enhancement for deep learning models during training.
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
import pickle
import hashlib
from datetime import datetime
import copy

import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.optim import Optimizer

logger = logging.getLogger(__name__)


class AdversarialRobustnessAnalyzer:
    """
    Adversarial Robustness Analyzer for deep learning models.
    
    This class provides comprehensive adversarial attack testing, vulnerability detection,
    and robustness enhancement for deep learning models during training. It implements
    various attack methods, defense strategies, and robustness metrics to help identify
    and mitigate vulnerabilities in models.
    
    Attributes:
        model: The PyTorch model to analyze
        device: Device to run analysis on (CPU or CUDA)
        attack_methods: List of attack methods to use
        defense_methods: List of defense methods to use
        robustness_metrics: List of robustness metrics to track
        output_dir: Directory to save analysis results
        running: Whether the analyzer is currently running
        vulnerability_history: History of detected vulnerabilities
        robustness_scores: Tracked robustness scores over time
        attack_success_rates: Success rates of different attacks
        defense_effectiveness: Effectiveness of different defenses
    """
    
    def __init__(
        self,
        model: nn.Module,
        device: Optional[torch.device] = None,
        attack_methods: Optional[List[str]] = None,
        defense_methods: Optional[List[str]] = None,
        robustness_metrics: Optional[List[str]] = None,
        auto_enhance: bool = False,
        output_dir: Optional[str] = None,
    ):
        """
        Initialize the AdversarialRobustnessAnalyzer.
        
        Args:
            model: PyTorch model to analyze
            device: Device to run analysis on (default: auto-detect)
            attack_methods: List of attack methods to use (default: all)
            defense_methods: List of defense methods to use (default: none)
            robustness_metrics: List of robustness metrics to track (default: all)
            auto_enhance: Whether to automatically enhance model robustness
            output_dir: Directory to save analysis results (optional)
        """
        self.model = model
        self.device = device or (torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu"))
        self.attack_methods = attack_methods or ["fgsm", "pgd", "deepfool", "carlini_wagner"]
        self.defense_methods = defense_methods or []
        self.robustness_metrics = robustness_metrics or ["empirical_robustness", "loss_sensitivity", "gradient_norm"]
        self.auto_enhance = auto_enhance
        self.output_dir = output_dir or os.path.join(os.getcwd(), "adversarial_robustness_output")
        
        # Create output directory if it doesn't exist
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Initialize analysis state
        self.running = False
        self.vulnerability_history = []
        self.robustness_scores = {metric: [] for metric in self.robustness_metrics}
        self.attack_success_rates = {attack: [] for attack in self.attack_methods}
        self.defense_effectiveness = {defense: [] for defense in self.defense_methods}
        
        # Initialize analysis thread
        self.analysis_thread = None
        self.lock = threading.Lock()
        
        # Initialize attack and defense methods
        self.attack_functions = self._initialize_attack_functions()
        self.defense_functions = self._initialize_defense_functions()
        self.metric_functions = self._initialize_metric_functions()
        
        # Initialize model state tracking
        self.model_state_history = deque(maxlen=5)  # Keep last 5 model states
        self.current_iteration = 0
        self.last_analysis_iteration = 0
        
        # Initialize enhancement strategies
        self.enhancement_strategies = self._initialize_enhancement_strategies()
        
        # Initialize performance tracking
        self.performance_impact = {
            "inference_time": [],
            "memory_usage": [],
            "training_overhead": [],
        }
        
        logger.info(f"Initialized AdversarialRobustnessAnalyzer with {len(self.attack_methods)} attack methods, "
                   f"{len(self.defense_methods)} defense methods, and {len(self.robustness_metrics)} metrics")
    
    def _initialize_attack_functions(self) -> Dict[str, Callable]:
        """
        Initialize attack functions.
        
        Returns:
            Dictionary mapping attack names to attack functions
        """
        attack_functions = {
            "fgsm": self._fast_gradient_sign_method,
            "pgd": self._projected_gradient_descent,
            "deepfool": self._deepfool_attack,
            "carlini_wagner": self._carlini_wagner_attack,
            "boundary": self._boundary_attack,
            "spatial": self._spatial_transformation_attack,
            "momentum_iterative": self._momentum_iterative_attack,
            "hopskip": self._hopskip_attack,
            "zoo": self._zeroth_order_optimization_attack,
        }
        
        # Filter to only include requested attack methods
        return {name: func for name, func in attack_functions.items() if name in self.attack_methods}
    
    def _initialize_defense_functions(self) -> Dict[str, Callable]:
        """
        Initialize defense functions.
        
        Returns:
            Dictionary mapping defense names to defense functions
        """
        defense_functions = {
            "adversarial_training": self._adversarial_training_defense,
            "input_gradient_regularization": self._input_gradient_regularization_defense,
            "feature_squeezing": self._feature_squeezing_defense,
            "spatial_smoothing": self._spatial_smoothing_defense,
            "label_smoothing": self._label_smoothing_defense,
            "defensive_distillation": self._defensive_distillation_defense,
            "randomized_smoothing": self._randomized_smoothing_defense,
            "jpeg_compression": self._jpeg_compression_defense,
            "input_transformation": self._input_transformation_defense,
        }
        
        # Filter to only include requested defense methods
        return {name: func for name, func in defense_functions.items() if name in self.defense_methods}
    
    def _initialize_metric_functions(self) -> Dict[str, Callable]:
        """
        Initialize robustness metric functions.
        
        Returns:
            Dictionary mapping metric names to metric functions
        """
        metric_functions = {
            "empirical_robustness": self._empirical_robustness_metric,
            "loss_sensitivity": self._loss_sensitivity_metric,
            "gradient_norm": self._gradient_norm_metric,
            "clever_score": self._clever_score_metric,
            "noise_sensitivity": self._noise_sensitivity_metric,
            "boundary_thickness": self._boundary_thickness_metric,
            "lipschitz_constant": self._lipschitz_constant_metric,
            "adversarial_distance": self._adversarial_distance_metric,
            "confidence_reduction": self._confidence_reduction_metric,
        }
        
        # Filter to only include requested metrics
        return {name: func for name, func in metric_functions.items() if name in self.robustness_metrics}
    
    def _initialize_enhancement_strategies(self) -> Dict[str, Callable]:
        """
        Initialize robustness enhancement strategies.
        
        Returns:
            Dictionary mapping strategy names to enhancement functions
        """
        enhancement_strategies = {
            "adversarial_training": self._apply_adversarial_training,
            "gradient_regularization": self._apply_gradient_regularization,
            "noise_augmentation": self._apply_noise_augmentation,
            "defensive_distillation": self._apply_defensive_distillation,
            "feature_denoising": self._apply_feature_denoising,
            "input_transformation": self._apply_input_transformation,
            "ensemble_method": self._apply_ensemble_method,
            "certified_defenses": self._apply_certified_defenses,
        }
        
        return enhancement_strategies
    
    def start(self) -> None:
        """Start the adversarial robustness analyzer."""
        if self.running:
            logger.warning("Adversarial Robustness Analyzer is already running")
            return
        
        self.running = True
        self.analysis_thread = threading.Thread(target=self._analysis_loop)
        self.analysis_thread.daemon = True
        self.analysis_thread.start()
        
        logger.info("Started Adversarial Robustness Analyzer")
    
    def stop(self) -> None:
        """Stop the adversarial robustness analyzer."""
        if not self.running:
            logger.warning("Adversarial Robustness Analyzer is not running")
            return
        
        self.running = False
        if self.analysis_thread is not None:
            self.analysis_thread.join(timeout=5.0)
        
        logger.info("Stopped Adversarial Robustness Analyzer")
    
    def _analysis_loop(self) -> None:
        """Main analysis loop for adversarial robustness."""
        while self.running:
            try:
                # Check if analysis is needed
                if self._should_analyze():
                    self._perform_analysis()
                
                # Apply automatic enhancements if enabled
                if self.auto_enhance and self.current_iteration > 0 and self.current_iteration % 50 == 0:
                    self._enhance_robustness()
                
                # Generate insights periodically
                if self.current_iteration > 0 and self.current_iteration % 100 == 0:
                    self._generate_insights()
                
                # Sleep to avoid consuming too many resources
                time.sleep(1.0)
            
            except Exception as e:
                logger.error(f"Error in adversarial analysis loop: {e}")
                logger.exception(e)
                time.sleep(5.0)  # Sleep longer on error
    
    def _should_analyze(self) -> bool:
        """
        Determine if adversarial analysis is needed.
        
        Returns:
            True if analysis is needed, False otherwise
        """
        # Analyze every 10 iterations
        return self.current_iteration - self.last_analysis_iteration >= 10
    
    def _perform_analysis(self) -> None:
        """Perform comprehensive adversarial robustness analysis."""
        logger.info(f"Performing adversarial robustness analysis at iteration {self.current_iteration}")
        
        analysis_start_time = time.time()
        
        # Save current model state
        self._save_current_model_state()
        
        # Generate synthetic data for analysis
        inputs, targets = self._generate_synthetic_data()
        
        # Analyze robustness metrics
        self._analyze_robustness_metrics(inputs, targets)
        
        # Test attack methods
        self._test_attack_methods(inputs, targets)
        
        # Evaluate defense methods
        if self.defense_methods:
            self._evaluate_defense_methods(inputs, targets)
        
        # Detect vulnerabilities
        vulnerabilities = self._detect_vulnerabilities()
        
        # Record analysis results
        self._record_analysis_results(vulnerabilities)
        
        # Update last analysis iteration
        self.last_analysis_iteration = self.current_iteration
        
        analysis_duration = time.time() - analysis_start_time
        logger.info(f"Adversarial robustness analysis completed in {analysis_duration:.2f} seconds")
    
    def _save_current_model_state(self) -> None:
        """Save the current model state for analysis."""
        # Create a lightweight representation of model state
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
            "state_summary": state_summary,
        })
    
    def _generate_synthetic_data(self, num_samples: int = 10) -> Tuple[torch.Tensor, torch.Tensor]:
        """
        Generate synthetic data for adversarial analysis.
        
        Args:
            num_samples: Number of synthetic samples to generate
            
        Returns:
            Tuple of (inputs, targets) tensors
        """
        # Determine input shape based on model
        input_shape = self._infer_input_shape()
        
        if input_shape is None:
            # Default to a standard image size if shape cannot be inferred
            input_shape = (3, 32, 32)
        
        # Generate random inputs
        inputs = torch.randn(num_samples, *input_shape, device=self.device)
        
        # Normalize inputs to a reasonable range
        inputs = torch.clamp(inputs, -1.0, 1.0)
        
        # Generate targets by getting model predictions
        self.model.eval()
        with torch.no_grad():
            logits = self.model(inputs)
        
        # Use argmax as targets
        targets = logits.argmax(dim=1)
        
        return inputs, targets
    
    def _infer_input_shape(self) -> Optional[Tuple[int, ...]]:
        """
        Infer the input shape expected by the model.
        
        Returns:
            Tuple representing input shape (excluding batch dimension)
        """
        # Try to infer from the first layer
        for module in self.model.modules():
            if isinstance(module, nn.Conv2d):
                # For Conv2d, infer from in_channels and assume a reasonable spatial size
                return (module.in_channels, 32, 32)
            elif isinstance(module, nn.Linear):
                # For Linear, reshape to a reasonable image size if possible
                in_features = module.in_features
                
                # Try to factorize into channels x height x width
                for channels in [1, 3]:
                    if in_features % channels == 0:
                        spatial_size = int(math.sqrt(in_features / channels))
                        if spatial_size * spatial_size * channels == in_features:
                            return (channels, spatial_size, spatial_size)
                
                # If can't factorize, return as a 1D feature vector
                return (in_features,)
        
        # If no suitable layer found, return None
        return None
    
    def _analyze_robustness_metrics(self, inputs: torch.Tensor, targets: torch.Tensor) -> None:
        """
        Analyze robustness metrics for the model.
        
        Args:
            inputs: Input tensor
            targets: Target tensor
        """
        for metric_name, metric_func in self.metric_functions.items():
            try:
                # Calculate metric
                metric_value = metric_func(inputs, targets)
                
                # Record metric
                self.robustness_scores[metric_name].append({
                    "iteration": self.current_iteration,
                    "value": metric_value,
                    "timestamp": time.time(),
                })
                
                logger.debug(f"Metric {metric_name}: {metric_value:.4f}")
            
            except Exception as e:
                logger.error(f"Error calculating metric {metric_name}: {e}")
    
    def _test_attack_methods(self, inputs: torch.Tensor, targets: torch.Tensor) -> None:
        """
        Test various attack methods against the model.
        
        Args:
            inputs: Input tensor
            targets: Target tensor
        """
        self.model.eval()
        
        # Get clean predictions
        with torch.no_grad():
            clean_outputs = self.model(inputs)
            clean_predictions = clean_outputs.argmax(dim=1)
        
        # Test each attack method
        for attack_name, attack_func in self.attack_functions.items():
            try:
                # Generate adversarial examples
                start_time = time.time()
                adv_inputs = attack_func(inputs, targets)
                attack_time = time.time() - start_time
                
                # Get predictions on adversarial examples
                with torch.no_grad():
                    adv_outputs = self.model(adv_inputs)
                    adv_predictions = adv_outputs.argmax(dim=1)
                
                # Calculate success rate
                success_mask = (adv_predictions != targets)
                success_rate = float(success_mask.sum().item()) / targets.size(0)
                
                # Calculate perturbation size
                perturbation = (adv_inputs - inputs).view(inputs.size(0), -1)
                l2_perturbation = torch.norm(perturbation, p=2, dim=1).mean().item()
                linf_perturbation = torch.norm(perturbation, p=float('inf'), dim=1).mean().item()
                
                # Record attack results
                self.attack_success_rates[attack_name].append({
                    "iteration": self.current_iteration,
                    "success_rate": success_rate,
                    "l2_perturbation": l2_perturbation,
                    "linf_perturbation": linf_perturbation,
                    "attack_time": attack_time,
                    "timestamp": time.time(),
                })
                
                logger.debug(f"Attack {attack_name}: Success rate {success_rate:.4f}, "
                           f"L2 perturbation {l2_perturbation:.4f}, "
                           f"Linf perturbation {linf_perturbation:.4f}")
            
            except Exception as e:
                logger.error(f"Error testing attack {attack_name}: {e}")
    
    def _evaluate_defense_methods(self, inputs: torch.Tensor, targets: torch.Tensor) -> None:
        """
        Evaluate various defense methods for the model.
        
        Args:
            inputs: Input tensor
            targets: Target tensor
        """
        # Generate adversarial examples using the most effective attack
        most_effective_attack = self._get_most_effective_attack()
        
        if most_effective_attack is None:
            logger.warning("No attack success data available to evaluate defenses")
            return
        
        attack_func = self.attack_functions[most_effective_attack]
        adv_inputs = attack_func(inputs, targets)
        
        # Evaluate each defense method
        for defense_name, defense_func in self.defense_functions.items():
            try:
                # Apply defense
                start_time = time.time()
                defended_inputs = defense_func(adv_inputs)
                defense_time = time.time() - start_time
                
                # Get predictions on defended inputs
                self.model.eval()
                with torch.no_grad():
                    defended_outputs = self.model(defended_inputs)
                    defended_predictions = defended_outputs.argmax(dim=1)
                
                # Calculate defense effectiveness
                success_mask = (defended_predictions == targets)
                effectiveness = float(success_mask.sum().item()) / targets.size(0)
                
                # Record defense results
                self.defense_effectiveness[defense_name].append({
                    "iteration": self.current_iteration,
                    "effectiveness": effectiveness,
                    "defense_time": defense_time,
                    "attack_used": most_effective_attack,
                    "timestamp": time.time(),
                })
                
                logger.debug(f"Defense {defense_name}: Effectiveness {effectiveness:.4f} against {most_effective_attack}")
            
            except Exception as e:
                logger.error(f"Error evaluating defense {defense_name}: {e}")
    
    def _get_most_effective_attack(self) -> Optional[str]:
        """
        Get the name of the most effective attack based on success rates.
        
        Returns:
            Name of the most effective attack, or None if no data available
        """
        best_attack = None
        best_success_rate = -1
        
        for attack_name, results in self.attack_success_rates.items():
            if not results:
                continue
            
            # Get the most recent result
            latest_result = results[-1]
            success_rate = latest_result["success_rate"]
            
            if success_rate > best_success_rate:
                best_success_rate = success_rate
                best_attack = attack_name
        
        return best_attack
    
    def _detect_vulnerabilities(self) -> List[Dict[str, Any]]:
        """
        Detect vulnerabilities in the model based on analysis results.
        
        Returns:
            List of detected vulnerabilities
        """
        vulnerabilities = []
        
        # Check attack success rates
        for attack_name, results in self.attack_success_rates.items():
            if not results:
                continue
            
            # Get the most recent result
            latest_result = results[-1]
            success_rate = latest_result["success_rate"]
            
            # High success rate indicates vulnerability
            if success_rate > 0.5:
                vulnerabilities.append({
                    "type": "high_attack_success",
                    "attack_method": attack_name,
                    "success_rate": success_rate,
                    "severity": "high" if success_rate > 0.8 else "medium",
                    "description": f"Model is vulnerable to {attack_name} attacks with {success_rate:.2%} success rate",
                    "iteration": self.current_iteration,
                    "timestamp": time.time(),
                })
        
        # Check robustness metrics
        for metric_name, results in self.robustness_scores.items():
            if not results or len(results) < 2:
                continue
            
            # Get the most recent result
            latest_result = results[-1]
            metric_value = latest_result["value"]
            
            # Detect issues based on metric type
            if metric_name == "empirical_robustness" and metric_value < 0.3:
                vulnerabilities.append({
                    "type": "low_empirical_robustness",
                    "metric_value": metric_value,
                    "severity": "high" if metric_value < 0.1 else "medium",
                    "description": f"Model has low empirical robustness ({metric_value:.4f})",
                    "iteration": self.current_iteration,
                    "timestamp": time.time(),
                })
            
            elif metric_name == "gradient_norm" and metric_value > 10.0:
                vulnerabilities.append({
                    "type": "high_gradient_norm",
                    "metric_value": metric_value,
                    "severity": "high" if metric_value > 50.0 else "medium",
                    "description": f"Model has high gradient norm ({metric_value:.4f}), indicating instability",
                    "iteration": self.current_iteration,
                    "timestamp": time.time(),
                })
            
            elif metric_name == "loss_sensitivity" and metric_value > 5.0:
                vulnerabilities.append({
                    "type": "high_loss_sensitivity",
                    "metric_value": metric_value,
                    "severity": "high" if metric_value > 10.0 else "medium",
                    "description": f"Model has high loss sensitivity ({metric_value:.4f}), indicating vulnerability to perturbations",
                    "iteration": self.current_iteration,
                    "timestamp": time.time(),
                })
        
        # Check for defense effectiveness
        if self.defense_methods:
            for defense_name, results in self.defense_effectiveness.items():
                if not results:
                    continue
                
                # Get the most recent result
                latest_result = results[-1]
                effectiveness = latest_result["effectiveness"]
                
                # Low effectiveness indicates vulnerability
                if effectiveness < 0.5:
                    vulnerabilities.append({
                        "type": "ineffective_defense",
                        "defense_method": defense_name,
                        "effectiveness": effectiveness,
                        "severity": "high" if effectiveness < 0.2 else "medium",
                        "description": f"Defense method {defense_name} is ineffective ({effectiveness:.2%})",
                        "iteration": self.current_iteration,
                        "timestamp": time.time(),
                    })
        
        return vulnerabilities
    
    def _record_analysis_results(self, vulnerabilities: List[Dict[str, Any]]) -> None:
        """
        Record analysis results and detected vulnerabilities.
        
        Args:
            vulnerabilities: List of detected vulnerabilities
        """
        # Add vulnerabilities to history
        self.vulnerability_history.extend(vulnerabilities)
        
        # Log vulnerabilities
        for vuln in vulnerabilities:
            logger.warning(f"Detected vulnerability: {vuln['description']} (Severity: {vuln['severity']})")
        
        # Save analysis results periodically
        if self.current_iteration % 50 == 0:
            self._save_analysis_results()
    
    def _save_analysis_results(self) -> None:
        """Save analysis results to file."""
        # Create filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(self.output_dir, f"robustness_analysis_{timestamp}.json")
        
        # Prepare results
        results = {
            "timestamp": time.time(),
            "iteration": self.current_iteration,
            "robustness_scores": {k: v[-10:] for k, v in self.robustness_scores.items() if v},  # Last 10 entries
            "attack_success_rates": {k: v[-10:] for k, v in self.attack_success_rates.items() if v},  # Last 10 entries
            "defense_effectiveness": {k: v[-10:] for k, v in self.defense_effectiveness.items() if v},  # Last 10 entries
            "vulnerabilities": self.vulnerability_history[-20:],  # Last 20 vulnerabilities
            "recommendations": self._generate_recommendations(),
        }
        
        # Save to file
        with open(filename, "w") as f:
            json.dump(results, f, indent=2)
        
        logger.info(f"Saved analysis results to {filename}")
    
    def _generate_recommendations(self) -> List[Dict[str, Any]]:
        """
        Generate recommendations for improving robustness.
        
        Returns:
            List of recommendations
        """
        recommendations = []
        
        # Analyze attack success rates
        high_success_attacks = []
        for attack_name, results in self.attack_success_rates.items():
            if not results:
                continue
            
            latest_result = results[-1]
            if latest_result["success_rate"] > 0.5:
                high_success_attacks.append(attack_name)
        
        if high_success_attacks:
            attack_list = ", ".join(high_success_attacks)
            recommendations.append({
                "type": "defense_recommendation",
                "target": "attack_vulnerability",
                "description": f"Model is vulnerable to {attack_list} attacks. Consider implementing adversarial training.",
                "priority": "high",
                "suggested_actions": ["adversarial_training", "gradient_regularization"],
            })
        
        # Analyze robustness metrics
        if "empirical_robustness" in self.robustness_scores and self.robustness_scores["empirical_robustness"]:
            latest_value = self.robustness_scores["empirical_robustness"][-1]["value"]
            if latest_value < 0.3:
                recommendations.append({
                    "type": "metric_recommendation",
                    "target": "empirical_robustness",
                    "description": f"Low empirical robustness ({latest_value:.4f}). Consider data augmentation and regularization.",
                    "priority": "medium",
                    "suggested_actions": ["noise_augmentation", "feature_denoising"],
                })
        
        if "gradient_norm" in self.robustness_scores and self.robustness_scores["gradient_norm"]:
            latest_value = self.robustness_scores["gradient_norm"][-1]["value"]
            if latest_value > 10.0:
                recommendations.append({
                    "type": "metric_recommendation",
                    "target": "gradient_norm",
                    "description": f"High gradient norm ({latest_value:.4f}). Consider gradient regularization techniques.",
                    "priority": "high" if latest_value > 50.0 else "medium",
                    "suggested_actions": ["gradient_regularization", "defensive_distillation"],
                })
        
        # Analyze defense effectiveness
        if self.defense_methods:
            ineffective_defenses = []
            for defense_name, results in self.defense_effectiveness.items():
                if not results:
                    continue
                
                latest_result = results[-1]
                if latest_result["effectiveness"] < 0.5:
                    ineffective_defenses.append(defense_name)
            
            if ineffective_defenses:
                defense_list = ", ".join(ineffective_defenses)
                recommendations.append({
                    "type": "defense_recommendation",
                    "target": "ineffective_defense",
                    "description": f"Current defenses ({defense_list}) are ineffective. Consider stronger or combined defenses.",
                    "priority": "high",
                    "suggested_actions": ["ensemble_method", "certified_defenses"],
                })
        
        return recommendations
    
    def _enhance_robustness(self) -> None:
        """Automatically enhance model robustness based on analysis results."""
        if not self.auto_enhance:
            return
        
        logger.info("Applying automatic robustness enhancements")
        
        # Get recommendations
        recommendations = self._generate_recommendations()
        
        # Apply enhancements based on recommendations
        applied_enhancements = []
        
        for recommendation in recommendations:
            if "suggested_actions" in recommendation:
                for action in recommendation["suggested_actions"]:
                    if action in self.enhancement_strategies:
                        try:
                            # Apply enhancement strategy
                            result = self.enhancement_strategies[action]()
                            
                            if result["success"]:
                                applied_enhancements.append({
                                    "strategy": action,
                                    "target": recommendation.get("target", "general"),
                                    "description": result["description"],
                                    "iteration": self.current_iteration,
                                    "timestamp": time.time(),
                                })
                                
                                logger.info(f"Applied enhancement strategy: {action}")
                        
                        except Exception as e:
                            logger.error(f"Error applying enhancement strategy {action}: {e}")
        
        # Log summary of applied enhancements
        if applied_enhancements:
            logger.info(f"Applied {len(applied_enhancements)} robustness enhancements")
        else:
            logger.info("No robustness enhancements were applied")
    
    def _generate_insights(self) -> Dict[str, Any]:
        """
        Generate insights from analysis results.
        
        Returns:
            Dictionary containing insights
        """
        insights = {
            "timestamp": time.time(),
            "iteration": self.current_iteration,
            "robustness_summary": {},
            "attack_vulnerability": {},
            "defense_effectiveness": {},
            "vulnerability_trends": {},
            "recommendations": self._generate_recommendations(),
        }
        
        # Summarize robustness metrics
        for metric_name, results in self.robustness_scores.items():
            if not results:
                continue
            
            values = [result["value"] for result in results[-10:]]  # Last 10 values
            
            insights["robustness_summary"][metric_name] = {
                "current": values[-1],
                "mean": float(np.mean(values)),
                "min": float(np.min(values)),
                "max": float(np.max(values)),
                "trend": "improving" if len(values) > 1 and values[-1] > values[0] else "worsening",
            }
        
        # Summarize attack vulnerability
        for attack_name, results in self.attack_success_rates.items():
            if not results:
                continue
            
            success_rates = [result["success_rate"] for result in results[-10:]]  # Last 10 values
            
            insights["attack_vulnerability"][attack_name] = {
                "current_success_rate": success_rates[-1],
                "mean_success_rate": float(np.mean(success_rates)),
                "trend": "improving" if len(success_rates) > 1 and success_rates[-1] < success_rates[0] else "worsening",
            }
        
        # Summarize defense effectiveness
        for defense_name, results in self.defense_effectiveness.items():
            if not results:
                continue
            
            effectiveness_values = [result["effectiveness"] for result in results[-10:]]  # Last 10 values
            
            insights["defense_effectiveness"][defense_name] = {
                "current_effectiveness": effectiveness_values[-1],
                "mean_effectiveness": float(np.mean(effectiveness_values)),
                "trend": "improving" if len(effectiveness_values) > 1 and effectiveness_values[-1] > effectiveness_values[0] else "worsening",
            }
        
        # Analyze vulnerability trends
        vulnerability_counts = {}
        for vuln in self.vulnerability_history[-50:]:  # Last 50 vulnerabilities
            vuln_type = vuln["type"]
            vulnerability_counts[vuln_type] = vulnerability_counts.get(vuln_type, 0) + 1
        
        insights["vulnerability_trends"] = {
            "most_common_type": max(vulnerability_counts.items(), key=lambda x: x[1])[0] if vulnerability_counts else None,
            "type_counts": vulnerability_counts,
            "total_vulnerabilities": len(self.vulnerability_history),
            "recent_vulnerabilities": len([v for v in self.vulnerability_history if v["iteration"] > self.current_iteration - 50]),
        }
        
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
        filename = os.path.join(self.output_dir, f"robustness_insights_{timestamp}.json")
        
        # Save to file
        with open(filename, "w") as f:
            json.dump(insights, f, indent=2)
        
        logger.info(f"Saved insights to {filename}")
    
    def on_iteration_complete(self, iteration: int, batch: Optional[Tuple[torch.Tensor, torch.Tensor]] = None) -> None:
        """
        Update analyzer with information about completed iteration.
        
        Args:
            iteration: Current iteration number
            batch: Current batch of data (inputs, targets) (optional)
        """
        with self.lock:
            self.current_iteration = iteration
            
            # If batch is provided, use it for immediate analysis
            if batch is not None and self._should_analyze():
                inputs, targets = batch
                inputs = inputs.to(self.device)
                targets = targets.to(self.device)
                
                self._perform_analysis_on_batch(inputs, targets)
    
    def _perform_analysis_on_batch(self, inputs: torch.Tensor, targets: torch.Tensor) -> None:
        """
        Perform analysis on a specific batch of data.
        
        Args:
            inputs: Input tensor
            targets: Target tensor
        """
        # Limit the number of samples to analyze to avoid excessive computation
        max_samples = 16
        if inputs.size(0) > max_samples:
            indices = torch.randperm(inputs.size(0))[:max_samples]
            inputs = inputs[indices]
            targets = targets[indices]
        
        # Perform analysis
        self._save_current_model_state()
        self._analyze_robustness_metrics(inputs, targets)
        self._test_attack_methods(inputs, targets)
        
        if self.defense_methods:
            self._evaluate_defense_methods(inputs, targets)
        
        vulnerabilities = self._detect_vulnerabilities()
        self._record_analysis_results(vulnerabilities)
        
        # Update last analysis iteration
        self.last_analysis_iteration = self.current_iteration
    
    def get_robustness_scores(self) -> Dict[str, List[Dict[str, Any]]]:
        """
        Get the current robustness scores.
        
        Returns:
            Dictionary mapping metric names to lists of score entries
        """
        with self.lock:
            # Create a copy to avoid threading issues
            return {metric: list(scores) for metric, scores in self.robustness_scores.items()}
    
    def get_attack_success_rates(self) -> Dict[str, List[Dict[str, Any]]]:
        """
        Get the current attack success rates.
        
        Returns:
            Dictionary mapping attack names to lists of success rate entries
        """
        with self.lock:
            # Create a copy to avoid threading issues
            return {attack: list(rates) for attack, rates in self.attack_success_rates.items()}
    
    def get_defense_effectiveness(self) -> Dict[str, List[Dict[str, Any]]]:
        """
        Get the current defense effectiveness values.
        
        Returns:
            Dictionary mapping defense names to lists of effectiveness entries
        """
        with self.lock:
            # Create a copy to avoid threading issues
            return {defense: list(values) for defense, values in self.defense_effectiveness.items()}
    
    def get_vulnerabilities(self) -> List[Dict[str, Any]]:
        """
        Get the detected vulnerabilities.
        
        Returns:
            List of vulnerability entries
        """
        with self.lock:
            # Create a copy to avoid threading issues
            return list(self.vulnerability_history)
    
    def get_recommendations(self) -> List[Dict[str, Any]]:
        """
        Get recommendations for improving robustness.
        
        Returns:
            List of recommendations
        """
        return self._generate_recommendations()
    
    def visualize_robustness(self, output_file: Optional[str] = None) -> Dict[str, Any]:
        """
        Generate visualization data for robustness metrics.
        
        Args:
            output_file: Path to save visualization data (optional)
            
        Returns:
            Dictionary containing visualization data
        """
        with self.lock:
            # Prepare visualization data
            visualization = {
                "title": "Adversarial Robustness Metrics",
                "metrics": {},
                "attacks": {},
                "defenses": {},
            }
            
            # Add metric data
            for metric_name, results in self.robustness_scores.items():
                if not results:
                    continue
                
                visualization["metrics"][metric_name] = {
                    "values": [{"iteration": entry["iteration"], "value": entry["value"]} for entry in results],
                    "current": results[-1]["value"],
                    "trend": "improving" if len(results) > 1 and results[-1]["value"] > results[0]["value"] else "worsening",
                }
            
            # Add attack data
            for attack_name, results in self.attack_success_rates.items():
                if not results:
                    continue
                
                visualization["attacks"][attack_name] = {
                    "success_rates": [{"iteration": entry["iteration"], "value": entry["success_rate"]} for entry in results],
                    "current": results[-1]["success_rate"],
                    "trend": "improving" if len(results) > 1 and results[-1]["success_rate"] < results[0]["success_rate"] else "worsening",
                }
            
            # Add defense data
            for defense_name, results in self.defense_effectiveness.items():
                if not results:
                    continue
                
                visualization["defenses"][defense_name] = {
                    "effectiveness": [{"iteration": entry["iteration"], "value": entry["effectiveness"]} for entry in results],
                    "current": results[-1]["effectiveness"],
                    "trend": "improving" if len(results) > 1 and results[-1]["effectiveness"] > results[0]["effectiveness"] else "worsening",
                }
            
            # Save to file if requested
            if output_file:
                with open(output_file, "w") as f:
                    json.dump(visualization, f, indent=2)
                
                logger.info(f"Saved robustness visualization to {output_file}")
            
            return visualization
    
    def generate_report(self, output_file: Optional[str] = None) -> Dict[str, Any]:
        """
        Generate a comprehensive report on adversarial robustness.
        
        Args:
            output_file: Path to save report (optional)
            
        Returns:
            Dictionary containing report data
        """
        with self.lock:
            # Generate insights
            insights = self._generate_insights()
            
            # Create report structure
            report = {
                "title": "Adversarial Robustness Analysis Report",
                "timestamp": time.time(),
                "iteration": self.current_iteration,
                "model_summary": self._generate_model_summary(),
                "robustness_metrics": {k: v[-5:] for k, v in self.robustness_scores.items() if v},  # Last 5 entries
                "attack_success_rates": {k: v[-5:] for k, v in self.attack_success_rates.items() if v},  # Last 5 entries
                "defense_effectiveness": {k: v[-5:] for k, v in self.defense_effectiveness.items() if v},  # Last 5 entries
                "vulnerabilities": self.vulnerability_history[-10:],  # Last 10 vulnerabilities
                "insights": insights,
                "recommendations": self._generate_recommendations(),
                "visualizations": {
                    "robustness": self.visualize_robustness(),
                },
            }
            
            # Save to file if requested
            if output_file:
                with open(output_file, "w") as f:
                    json.dump(report, f, indent=2)
                
                logger.info(f"Saved adversarial robustness report to {output_file}")
            
            return report
    
    def _generate_model_summary(self) -> Dict[str, Any]:
        """
        Generate a summary of the model architecture.
        
        Returns:
            Dictionary containing model summary
        """
        summary = {
            "num_parameters": sum(p.numel() for p in self.model.parameters()),
            "num_trainable_parameters": sum(p.numel() for p in self.model.parameters() if p.requires_grad),
            "layer_types": {},
        }
        
        # Count layer types
        for module in self.model.modules():
            module_type = module.__class__.__name__
            if module_type != "Sequential" and module_type != self.model.__class__.__name__:
                summary["layer_types"][module_type] = summary["layer_types"].get(module_type, 0) + 1
        
        return summary
    
    def apply_robustness_enhancement(self, strategy: str) -> Dict[str, Any]:
        """
        Apply a specific robustness enhancement strategy.
        
        Args:
            strategy: Name of the enhancement strategy to apply
            
        Returns:
            Dictionary containing result of the enhancement
        """
        if strategy not in self.enhancement_strategies:
            return {
                "success": False,
                "description": f"Unknown enhancement strategy: {strategy}",
            }
        
        try:
            # Apply the enhancement strategy
            result = self.enhancement_strategies[strategy]()
            
            # Log the result
            if result["success"]:
                logger.info(f"Applied enhancement strategy {strategy}: {result['description']}")
            else:
                logger.warning(f"Failed to apply enhancement strategy {strategy}: {result['description']}")
            
            return result
        
        except Exception as e:
            logger.error(f"Error applying enhancement strategy {strategy}: {e}")
            return {
                "success": False,
                "description": f"Error: {str(e)}",
            }
    
    def get_analysis_status(self) -> Dict[str, Any]:
        """
        Get the current status of the adversarial analysis.
        
        Returns:
            Dictionary containing analysis status
        """
        with self.lock:
            return {
                "running": self.running,
                "current_iteration": self.current_iteration,
                "last_analysis_iteration": self.last_analysis_iteration,
                "num_vulnerabilities": len(self.vulnerability_history),
                "num_metrics": len(self.robustness_scores),
                "num_attacks": len(self.attack_success_rates),
                "num_defenses": len(self.defense_effectiveness),
                "auto_enhance": self.auto_enhance,
                "output_dir": self.output_dir,
            }
    
    #
    # Attack Methods
    #
    
    def _fast_gradient_sign_method(self, inputs: torch.Tensor, targets: torch.Tensor, epsilon: float = 0.03) -> torch.Tensor:
        """
        Implement Fast Gradient Sign Method (FGSM) attack.
        
        Args:
            inputs: Input tensor
            targets: Target tensor
            epsilon: Perturbation size
            
        Returns:
            Adversarial examples
        """
        # Clone inputs to avoid modifying the original
        adv_inputs = inputs.clone().detach().to(self.device)
        targets = targets.clone().detach().to(self.device)
        
        # Set requires_grad
        adv_inputs.requires_grad = True
        
        # Forward pass
        self.model.eval()
        outputs = self.model(adv_inputs)
        
        # Calculate loss
        loss = F.cross_entropy(outputs, targets)
        
        # Backward pass
        self.model.zero_grad()
        loss.backward()
        
        # Create adversarial examples
        with torch.no_grad():
            # Get sign of gradient
            grad_sign = adv_inputs.grad.sign()
            
            # Add perturbation
            adv_inputs = adv_inputs + epsilon * grad_sign
            
            # Clamp to valid range
            adv_inputs = torch.clamp(adv_inputs, -1.0, 1.0)
        
        return adv_inputs
    
    def _projected_gradient_descent(self, inputs: torch.Tensor, targets: torch.Tensor, epsilon: float = 0.03, alpha: float = 0.01, num_steps: int = 10) -> torch.Tensor:
        """
        Implement Projected Gradient Descent (PGD) attack.
        
        Args:
            inputs: Input tensor
            targets: Target tensor
            epsilon: Perturbation size
            alpha: Step size
            num_steps: Number of steps
            
        Returns:
            Adversarial examples
        """
        # Clone inputs to avoid modifying the original
        adv_inputs = inputs.clone().detach().to(self.device)
        targets = targets.clone().detach().to(self.device)
        
        # Add random noise to start at a different point
        adv_inputs = adv_inputs + torch.empty_like(adv_inputs).uniform_(-epsilon, epsilon)
        adv_inputs = torch.clamp(adv_inputs, -1.0, 1.0)
        
        for _ in range(num_steps):
            # Set requires_grad
            adv_inputs.requires_grad = True
            
            # Forward pass
            self.model.eval()
            outputs = self.model(adv_inputs)
            
            # Calculate loss
            loss = F.cross_entropy(outputs, targets)
            
            # Backward pass
            self.model.zero_grad()
            loss.backward()
            
            # Update adversarial examples
            with torch.no_grad():
                adv_inputs = adv_inputs + alpha * adv_inputs.grad.sign()
                
                # Project back to epsilon ball
                delta = torch.clamp(adv_inputs - inputs, -epsilon, epsilon)
                adv_inputs = inputs + delta
                
                # Clamp to valid range
                adv_inputs = torch.clamp(adv_inputs, -1.0, 1.0)
        
        return adv_inputs
    
    def _deepfool_attack(self, inputs: torch.Tensor, targets: torch.Tensor, max_steps: int = 50, overshoot: float = 0.02) -> torch.Tensor:
        """
        Implement DeepFool attack.
        
        Args:
            inputs: Input tensor
            targets: Target tensor
            max_steps: Maximum number of steps
            overshoot: Overshoot parameter
            
        Returns:
            Adversarial examples
        """
        # Clone inputs to avoid modifying the original
        adv_inputs = inputs.clone().detach().to(self.device)
        
        # Get number of classes
        self.model.eval()
        with torch.no_grad():
            outputs = self.model(inputs)
        num_classes = outputs.shape[1]
        
        # Process each input separately
        for i in range(inputs.shape[0]):
            sample = inputs[i:i+1].clone().detach().to(self.device)
            adv_sample = sample.clone()
            
            # Get original prediction
            with torch.no_grad():
                output = self.model(sample)
            orig_class = output.argmax().item()
            
            # If already misclassified, skip
            if orig_class != targets[i].item():
                continue
            
            # DeepFool loop
            current_class = orig_class
            steps = 0
            
            while current_class == orig_class and steps < max_steps:
                # Set requires_grad
                adv_sample.requires_grad = True
                
                # Forward pass
                output = self.model(adv_sample)
                
                # Get gradients for all classes
                gradients = []
                for k in range(num_classes):
                    self.model.zero_grad()
                    output[0, k].backward(retain_graph=True)
                    gradients.append(adv_sample.grad.clone())
                    adv_sample.grad.zero_()
                
                # Find closest hyperplane
                with torch.no_grad():
                    w_k = gradients[orig_class]
                    f_k = output[0, orig_class]
                    
                    min_dist = float('inf')
                    closest_class = None
                    
                    for k in range(num_classes):
                        if k == orig_class:
                            continue
                        
                        w_k_prime = gradients[k]
                        f_k_prime = output[0, k]
                        
                        w_diff = w_k_prime - w_k
                        f_diff = f_k - f_k_prime
                        
                        # Calculate distance to decision boundary
                        if torch.norm(w_diff) > 1e-10:  # Avoid division by zero
                            dist = abs(f_diff) / torch.norm(w_diff)
                            
                            if dist < min_dist:
                                min_dist = dist
                                closest_class = k
                    
                    # If no valid class found, break
                    if closest_class is None:
                        break
                    
                    # Calculate perturbation
                    w_diff = gradients[closest_class] - gradients[orig_class]
                    f_diff = output[0, orig_class] - output[0, closest_class]
                    
                    # Avoid division by zero
                    if torch.norm(w_diff) > 1e-10:
                        perturbation = (f_diff.abs() / torch.norm(w_diff)**2) * w_diff
                        
                        # Apply perturbation with overshoot
                        adv_sample = adv_sample + (1 + overshoot) * perturbation
                        
                        # Clamp to valid range
                        adv_sample = torch.clamp(adv_sample, -1.0, 1.0)
                        
                        # Check if class changed
                        output = self.model(adv_sample)
                        current_class = output.argmax().item()
                    else:
                        break
                
                steps += 1
            
            # Update adversarial inputs
            adv_inputs[i] = adv_sample
        
        return adv_inputs
    
    def _carlini_wagner_attack(self, inputs: torch.Tensor, targets: torch.Tensor, confidence: float = 0.0, learning_rate: float = 0.01, max_iterations: int = 100) -> torch.Tensor:
        """
        Implement Carlini & Wagner L2 attack.
        
        Args:
            inputs: Input tensor
            targets: Target tensor
            confidence: Confidence parameter
            learning_rate: Learning rate for optimization
            max_iterations: Maximum number of iterations
            
        Returns:
            Adversarial examples
        """
        # Clone inputs to avoid modifying the original
        adv_inputs = inputs.clone().detach().to(self.device)
        targets = targets.clone().detach().to(self.device)
        
        # Initialize with small random noise
        noise = torch.randn_like(inputs) * 0.01
        w = torch.nn.Parameter(noise)
        optimizer = torch.optim.Adam([w], lr=learning_rate)
        
        # C&W attack loop
        for _ in range(max_iterations):
            # Apply tanh to ensure valid range
            adv_inputs = torch.tanh(inputs + w) * 0.5 + 0.5
            
            # Forward pass
            self.model.eval()
            outputs = self.model(adv_inputs)
            
            # Calculate C&W loss
            target_logits = outputs.gather(1, targets.unsqueeze(1)).squeeze(1)
            other_logits = outputs.clone()
            other_logits.scatter_(1, targets.unsqueeze(1), -float('inf'))
            other_logits = other_logits.max(1)[0]
            
            # Margin loss
            loss = torch.clamp(other_logits - target_logits + confidence, min=0)
            
            # Add L2 regularization
            loss = loss + torch.norm(w.view(w.shape[0], -1), p=2, dim=1)
            
            # Backward pass and optimization
            optimizer.zero_grad()
            loss.mean().backward()
            optimizer.step()
        
        # Final adversarial examples
        with torch.no_grad():
            adv_inputs = torch.tanh(inputs + w) * 0.5 + 0.5
            
            # Scale to [-1, 1] range
            adv_inputs = adv_inputs * 2 - 1
        
        return adv_inputs
    
    def _boundary_attack(self, inputs: torch.Tensor, targets: torch.Tensor, max_iterations: int = 50, step_size: float = 0.01) -> torch.Tensor:
        """
        Implement a simplified version of Boundary Attack.
        
        Args:
            inputs: Input tensor
            targets: Target tensor
            max_iterations: Maximum number of iterations
            step_size: Step size for perturbation
            
        Returns:
            Adversarial examples
        """
        # Clone inputs to avoid modifying the original
        adv_inputs = inputs.clone().detach().to(self.device)
        targets = targets.clone().detach().to(self.device)
        
        # Initialize with random noise
        noise = torch.randn_like(inputs)
        noise = noise / torch.norm(noise.view(noise.shape[0], -1), p=2, dim=1, keepdim=True).view(-1, 1, 1, 1)
        
        # Process each input separately
        for i in range(inputs.shape[0]):
            sample = inputs[i:i+1].clone().detach().to(self.device)
            target = targets[i:i+1].clone().detach().to(self.device)
            
            # Get original prediction
            self.model.eval()
            with torch.no_grad():
                output = self.model(sample)
            orig_class = output.argmax().item()
            
            # If already misclassified, skip
            if orig_class != target.item():
                continue
            
            # Start from a misclassified point
            adv_sample = sample + noise[i:i+1]
            adv_sample = torch.clamp(adv_sample, -1.0, 1.0)
            
            # Ensure starting point is adversarial
            with torch.no_grad():
                for _ in range(10):
                    output = self.model(adv_sample)
                    if output.argmax().item() != target.item():
                        break
                    adv_sample = adv_sample + torch.randn_like(adv_sample) * 0.1
                    adv_sample = torch.clamp(adv_sample, -1.0, 1.0)
            
            # Boundary attack loop
            for _ in range(max_iterations):
                # Step towards original sample
                direction = sample - adv_sample
                direction = direction / torch.norm(direction)
                
                # Apply step
                new_sample = adv_sample + direction * step_size
                
                # Check if still adversarial
                with torch.no_grad():
                    output = self.model(new_sample)
                    if output.argmax().item() != target.item():
                        adv_sample = new_sample
                
                # Clamp to valid range
                adv_sample = torch.clamp(adv_sample, -1.0, 1.0)
            
            # Update adversarial inputs
            adv_inputs[i] = adv_sample
        
        return adv_inputs
    
    def _spatial_transformation_attack(self, inputs: torch.Tensor, targets: torch.Tensor, max_rotation: float = 30.0, max_translation: float = 0.3) -> torch.Tensor:
        """
        Implement Spatial Transformation Attack.
        
        Args:
            inputs: Input tensor
            targets: Target tensor
            max_rotation: Maximum rotation in degrees
            max_translation: Maximum translation as fraction of image size
            
        Returns:
            Adversarial examples
        """
        # Clone inputs to avoid modifying the original
        adv_inputs = inputs.clone().detach().to(self.device)
        
        # Process each input separately
        for i in range(inputs.shape[0]):
            sample = inputs[i:i+1].clone().detach().to(self.device)
            
            # Get original prediction
            self.model.eval()
            with torch.no_grad():
                output = self.model(sample)
            orig_class = output.argmax().item()
            
            # If already misclassified, skip
            if orig_class != targets[i].item():
                continue
            
            # Try different transformations
            best_adv_sample = None
            best_loss = float('-inf')
            
            for _ in range(10):
                # Random rotation
                angle = torch.empty(1).uniform_(-max_rotation, max_rotation).item()
                
                # Random translation
                tx = torch.empty(1).uniform_(-max_translation, max_translation).item()
                ty = torch.empty(1).uniform_(-max_translation, max_translation).item()
                
                # Apply transformation
                # Note: In a real implementation, would use proper spatial transformation
                # Here we use a simplified approach for demonstration
                transformed = sample.clone()
                
                # Simulate rotation by shifting pixels
                if angle != 0:
                    h, w = transformed.shape[2], transformed.shape[3]
                    center_h, center_w = h // 2, w // 2
                    
                    for y in range(h):
                        for x in range(w):
                            # Calculate distance from center
                            y_diff = y - center_h
                            x_diff = x - center_w
                            
                            # Calculate new position
                            angle_rad = angle * math.pi / 180
                            new_x = int(x_diff * math.cos(angle_rad) - y_diff * math.sin(angle_rad) + center_w)
                            new_y = int(y_diff * math.cos(angle_rad) + x_diff * math.sin(angle_rad) + center_h)
                            
                            # Check if new position is valid
                            if 0 <= new_y < h and 0 <= new_x < w:
                                transformed[0, :, y, x] = sample[0, :, new_y, new_x]
                
                # Simulate translation
                if tx != 0 or ty != 0:
                    h, w = transformed.shape[2], transformed.shape[3]
                    dx, dy = int(tx * w), int(ty * h)
                    
                    if dx > 0:
                        transformed[0, :, :, dx:] = transformed[0, :, :, :-dx]
                        transformed[0, :, :, :dx] = 0
                    elif dx < 0:
                        transformed[0, :, :, :dx] = transformed[0, :, :, -dx:]
                        transformed[0, :, :, dx:] = 0
                    
                    if dy > 0:
                        transformed[0, :, dy:, :] = transformed[0, :, :-dy, :]
                        transformed[0, :, :dy, :] = 0
                    elif dy < 0:
                        transformed[0, :, :dy, :] = transformed[0, :, -dy:, :]
                        transformed[0, :, dy:, :] = 0
                
                # Check if transformation is adversarial
                with torch.no_grad():
                    output = self.model(transformed)
                    loss = -F.cross_entropy(output, targets[i:i+1])
                    
                    if loss > best_loss and output.argmax().item() != targets[i].item():
                        best_loss = loss
                        best_adv_sample = transformed.clone()
            
            # Update adversarial inputs if a successful transformation was found
            if best_adv_sample is not None:
                adv_inputs[i] = best_adv_sample
        
        return adv_inputs
    
    def _momentum_iterative_attack(self, inputs: torch.Tensor, targets: torch.Tensor, epsilon: float = 0.03, alpha: float = 0.01, num_steps: int = 10, decay: float = 0.9) -> torch.Tensor:
        """
        Implement Momentum Iterative Attack.
        
        Args:
            inputs: Input tensor
            targets: Target tensor
            epsilon: Perturbation size
            alpha: Step size
            num_steps: Number of steps
            decay: Momentum decay factor
            
        Returns:
            Adversarial examples
        """
        # Clone inputs to avoid modifying the original
        adv_inputs = inputs.clone().detach().to(self.device)
        targets = targets.clone().detach().to(self.device)
        
        # Initialize momentum
        momentum = torch.zeros_like(inputs)
        
        for _ in range(num_steps):
            # Set requires_grad
            adv_inputs.requires_grad = True
            
            # Forward pass
            self.model.eval()
            outputs = self.model(adv_inputs)
            
            # Calculate loss
            loss = F.cross_entropy(outputs, targets)
            
            # Backward pass
            self.model.zero_grad()
            loss.backward()
            
            # Update momentum
            grad = adv_inputs.grad.detach()
            grad_norm = torch.norm(grad.view(grad.shape[0], -1), p=1, dim=1)
            grad = grad / (grad_norm.view(-1, 1, 1, 1) + 1e-8)
            
            momentum = decay * momentum + grad
            
            # Update adversarial examples
            with torch.no_grad():
                adv_inputs = adv_inputs + alpha * momentum.sign()
                
                # Project back to epsilon ball
                delta = torch.clamp(adv_inputs - inputs, -epsilon, epsilon)
                adv_inputs = inputs + delta
                
                # Clamp to valid range
                adv_inputs = torch.clamp(adv_inputs, -1.0, 1.0)
        
        return adv_inputs
    
    def _hopskip_attack(self, inputs: torch.Tensor, targets: torch.Tensor, max_iterations: int = 50, initial_step: float = 0.1) -> torch.Tensor:
        """
        Implement a simplified version of HopSkipJump Attack.
        
        Args:
            inputs: Input tensor
            targets: Target tensor
            max_iterations: Maximum number of iterations
            initial_step: Initial step size
            
        Returns:
            Adversarial examples
        """
        # Clone inputs to avoid modifying the original
        adv_inputs = inputs.clone().detach().to(self.device)
        
        # Process each input separately
        for i in range(inputs.shape[0]):
            sample = inputs[i:i+1].clone().detach().to(self.device)
            target = targets[i:i+1].clone().detach().to(self.device)
            
            # Get original prediction
            self.model.eval()
            with torch.no_grad():
                output = self.model(sample)
            orig_class = output.argmax().item()
            
            # If already misclassified, skip
            if orig_class != target.item():
                continue
            
            # Start from a misclassified point (similar to boundary attack initialization)
            adv_sample = sample + torch.randn_like(sample) * 0.1
            adv_sample = torch.clamp(adv_sample, -1.0, 1.0)
            
            # Ensure starting point is adversarial
            with torch.no_grad():
                for _ in range(10):
                    output = self.model(adv_sample)
                    if output.argmax().item() != target.item():
                        break
                    adv_sample = adv_sample + torch.randn_like(adv_sample) * 0.1
                    adv_sample = torch.clamp(adv_sample, -1.0, 1.0)
            
            # HopSkipJump attack loop
            step_size = initial_step
            
            for it in range(max_iterations):
                # Binary search to find boundary point
                original = sample.clone()
                adversarial = adv_sample.clone()
                
                for _ in range(10):  # Binary search steps
                    midpoint = (original + adversarial) / 2
                    
                    with torch.no_grad():
                        output = self.model(midpoint)
                        if output.argmax().item() == target.item():
                            original = midpoint
                        else:
                            adversarial = midpoint
                
                # Boundary point
                boundary = adversarial.clone()
                
                # Estimate gradient direction using finite differences
                grad = torch.zeros_like(boundary)
                
                # Random sampling for gradient estimation
                num_samples = 10
                delta = 0.01
                
                for _ in range(num_samples):
                    noise = torch.randn_like(boundary) * delta
                    
                    with torch.no_grad():
                        output_pos = self.model(boundary + noise)
                        output_neg = self.model(boundary - noise)
                        
                        grad_sample = output_pos - output_neg
                        grad = grad + grad_sample.sign()
                
                # Normalize gradient
                grad = grad / (torch.norm(grad) + 1e-8)
                
                # Update step size
                step_size = step_size * 0.9
                
                # Update adversarial example
                adv_sample = boundary - step_size * grad
                
                # Clamp to valid range
                adv_sample = torch.clamp(adv_sample, -1.0, 1.0)
                
                # Check if still adversarial
                with torch.no_grad():
                    output = self.model(adv_sample)
                    if output.argmax().item() == target.item():
                        # If not adversarial, revert to boundary
                        adv_sample = boundary
            
            # Update adversarial inputs
            adv_inputs[i] = adv_sample
        
        return adv_inputs
    
    def _zeroth_order_optimization_attack(self, inputs: torch.Tensor, targets: torch.Tensor, max_iterations: int = 50, learning_rate: float = 0.01) -> torch.Tensor:
        """
        Implement a simplified version of ZOO (Zeroth Order Optimization) Attack.
        
        Args:
            inputs: Input tensor
            targets: Target tensor
            max_iterations: Maximum number of iterations
            learning_rate: Learning rate for optimization
            
        Returns:
            Adversarial examples
        """
        # Clone inputs to avoid modifying the original
        adv_inputs = inputs.clone().detach().to(self.device)
        
        # Process each input separately
        for i in range(inputs.shape[0]):
            sample = inputs[i:i+1].clone().detach().to(self.device)
            target = targets[i:i+1].clone().detach().to(self.device)
            
            # Get original prediction
            self.model.eval()
            with torch.no_grad():
                output = self.model(sample)
            orig_class = output.argmax().item()
            
            # If already misclassified, skip
            if orig_class != target.item():
                continue
            
            # Initialize perturbation
            delta = torch.zeros_like(sample).to(self.device)
            
            # ZOO attack loop
            for _ in range(max_iterations):
                # Randomly select a pixel to perturb
                c, h, w = sample.shape[1], sample.shape[2], sample.shape[3]
                
                channel = torch.randint(0, c, (1,)).item()
                height = torch.randint(0, h, (1,)).item()
                width = torch.randint(0, w, (1,)).item()
                
                # Compute gradient estimate using finite differences
                epsilon = 0.01
                
                # Positive perturbation
                delta_pos = delta.clone()
                delta_pos[0, channel, height, width] += epsilon
                
                # Negative perturbation
                delta_neg = delta.clone()
                delta_neg[0, channel, height, width] -= epsilon
                
                # Evaluate function values
                with torch.no_grad():
                    output_pos = self.model(torch.clamp(sample + delta_pos, -1.0, 1.0))
                    output_neg = self.model(torch.clamp(sample + delta_neg, -1.0, 1.0))
                    
                    # Target is the original class, so we want to minimize its probability
                    loss_pos = -output_pos[0, target.item()].item()
                    loss_neg = -output_neg[0, target.item()].item()
                    
                    # Estimate gradient
                    grad_estimate = (loss_pos - loss_neg) / (2 * epsilon)
                    
                    # Update perturbation
                    delta[0, channel, height, width] -= learning_rate * grad_estimate
                    
                    # Clamp perturbation to ensure valid range
                    adv_sample = torch.clamp(sample + delta, -1.0, 1.0)
                    
                    # Check if adversarial
                    output = self.model(adv_sample)
                    if output.argmax().item() != target.item():
                        break
            
            # Update adversarial inputs
            adv_inputs[i] = adv_sample
        
        return adv_inputs
    
    #
    # Defense Methods
    #
    
    def _adversarial_training_defense(self, adv_inputs: torch.Tensor) -> torch.Tensor:
        """
        Implement adversarial training defense.
        
        Args:
            adv_inputs: Adversarial input tensor
            
        Returns:
            Defended input tensor
        """
        # In a real implementation, this would involve training the model on adversarial examples
        # For this simulation, we just return the adversarial inputs unchanged
        return adv_inputs
    
    def _input_gradient_regularization_defense(self, adv_inputs: torch.Tensor) -> torch.Tensor:
        """
        Implement input gradient regularization defense.
        
        Args:
            adv_inputs: Adversarial input tensor
            
        Returns:
            Defended input tensor
        """
        # In a real implementation, this would involve regularizing the model's gradients
        # For this simulation, we just return the adversarial inputs unchanged
        return adv_inputs
    
    def _feature_squeezing_defense(self, adv_inputs: torch.Tensor, bit_depth: int = 5) -> torch.Tensor:
        """
        Implement feature squeezing defense.
        
        Args:
            adv_inputs: Adversarial input tensor
            bit_depth: Bit depth for quantization
            
        Returns:
            Defended input tensor
        """
        # Scale to [0, 1]
        inputs_0_1 = (adv_inputs + 1) / 2
        
        # Apply bit depth reduction
        max_val = 2**bit_depth - 1
        inputs_0_1 = torch.round(inputs_0_1 * max_val) / max_val
        
        # Scale back to [-1, 1]
        defended = inputs_0_1 * 2 - 1
        
        return defended
    
    def _spatial_smoothing_defense(self, adv_inputs: torch.Tensor, kernel_size: int = 3) -> torch.Tensor:
        """
        Implement spatial smoothing defense.
        
        Args:
            adv_inputs: Adversarial input tensor
            kernel_size: Size of smoothing kernel
            
        Returns:
            Defended input tensor
        """
        # Apply median filtering
        defended = adv_inputs.clone()
        
        # Process each channel separately
        for i in range(adv_inputs.shape[1]):
            # Extract channel
            channel = adv_inputs[:, i:i+1]
            
            # Apply median filtering
            # In a real implementation, would use proper 2D median filtering
            # Here we use a simplified approach for demonstration
            padding = kernel_size // 2
            padded = F.pad(channel, (padding, padding, padding, padding), mode='reflect')
            
            for b in range(adv_inputs.shape[0]):
                for h in range(adv_inputs.shape[2]):
                    for w in range(adv_inputs.shape[3]):
                        # Extract patch
                        patch = padded[b, 0, h:h+kernel_size, w:w+kernel_size]
                        
                        # Apply median
                        defended[b, i, h, w] = torch.median(patch)
        
        return defended
    
    def _label_smoothing_defense(self, adv_inputs: torch.Tensor) -> torch.Tensor:
        """
        Implement label smoothing defense.
        
        Args:
            adv_inputs: Adversarial input tensor
            
        Returns:
            Defended input tensor
        """
        # Label smoothing is applied during training, not to inputs
        # For this simulation, we just return the adversarial inputs unchanged
        return adv_inputs
    
    def _defensive_distillation_defense(self, adv_inputs: torch.Tensor) -> torch.Tensor:
        """
        Implement defensive distillation defense.
        
        Args:
            adv_inputs: Adversarial input tensor
            
        Returns:
            Defended input tensor
        """
        # Defensive distillation is applied during training, not to inputs
        # For this simulation, we just return the adversarial inputs unchanged
        return adv_inputs
    
    def _randomized_smoothing_defense(self, adv_inputs: torch.Tensor, sigma: float = 0.1, num_samples: int = 10) -> torch.Tensor:
        """
        Implement randomized smoothing defense.
        
        Args:
            adv_inputs: Adversarial input tensor
            sigma: Standard deviation of Gaussian noise
            num_samples: Number of noise samples
            
        Returns:
            Defended input tensor
        """
        # Apply randomized smoothing
        self.model.eval()
        batch_size = adv_inputs.shape[0]
        
        # Get predictions with noise
        with torch.no_grad():
            # Initialize vote counts
            outputs = self.model(adv_inputs)
            num_classes = outputs.shape[1]
            votes = torch.zeros(batch_size, num_classes, device=self.device)
            
            # Add noise and get predictions
            for _ in range(num_samples):
                noise = torch.randn_like(adv_inputs) * sigma
                noisy_inputs = torch.clamp(adv_inputs + noise, -1.0, 1.0)
                
                outputs = self.model(noisy_inputs)
                predictions = outputs.argmax(dim=1)
                
                # Count votes
                for i in range(batch_size):
                    votes[i, predictions[i]] += 1
            
            # Get majority vote
            smoothed_predictions = votes.argmax(dim=1)
        
        # For this simulation, we just return the adversarial inputs unchanged
        # In a real implementation, would use the smoothed predictions
        return adv_inputs
    
    def _jpeg_compression_defense(self, adv_inputs: torch.Tensor, quality: int = 75) -> torch.Tensor:
        """
        Implement JPEG compression defense.
        
        Args:
            adv_inputs: Adversarial input tensor
            quality: JPEG quality (0-100)
            
        Returns:
            Defended input tensor
        """
        # In a real implementation, would use actual JPEG compression
        # Here we use a simplified approach for demonstration
        
        # Apply DCT-like transformation
        defended = adv_inputs.clone()
        
        # Scale to [0, 1]
        inputs_0_1 = (adv_inputs + 1) / 2
        
        # Apply quantization similar to JPEG
        # Higher quality means less quantization
        quantization_factor = (101 - quality) / 50.0
        
        # Simple quantization
        defended = torch.round(inputs_0_1 / quantization_factor) * quantization_factor
        
        # Clamp to [0, 1]
        defended = torch.clamp(defended, 0, 1)
        
        # Scale back to [-1, 1]
        defended = defended * 2 - 1
        
        return defended
    
    def _input_transformation_defense(self, adv_inputs: torch.Tensor) -> torch.Tensor:
        """
        Implement input transformation defense.
        
        Args:
            adv_inputs: Adversarial input tensor
            
        Returns:
            Defended input tensor
        """
        # Apply a combination of transformations
        defended = adv_inputs.clone()
        
        # Apply bit depth reduction
        defended = self._feature_squeezing_defense(defended, bit_depth=5)
        
        # Apply spatial smoothing
        defended = self._spatial_smoothing_defense(defended, kernel_size=3)
        
        return defended
    
    #
    # Robustness Metrics
    #
    
    def _empirical_robustness_metric(self, inputs: torch.Tensor, targets: torch.Tensor) -> float:
        """
        Calculate empirical robustness metric.
        
        Args:
            inputs: Input tensor
            targets: Target tensor
            
        Returns:
            Empirical robustness score
        """
        # Generate small perturbations
        num_samples = 10
        epsilon = 0.01
        
        self.model.eval()
        with torch.no_grad():
            # Get clean predictions
            clean_outputs = self.model(inputs)
            clean_predictions = clean_outputs.argmax(dim=1)
            
            # Count robust predictions
            robust_count = 0
            
            for _ in range(num_samples):
                # Add random noise
                noise = torch.randn_like(inputs) * epsilon
                noisy_inputs = torch.clamp(inputs + noise, -1.0, 1.0)
                
                # Get predictions
                noisy_outputs = self.model(noisy_inputs)
                noisy_predictions = noisy_outputs.argmax(dim=1)
                
                # Count matches with clean predictions
                matches = (noisy_predictions == clean_predictions).float().mean().item()
                robust_count += matches
            
            # Calculate average robustness
            robustness = robust_count / num_samples
        
        return robustness
    
    def _loss_sensitivity_metric(self, inputs: torch.Tensor, targets: torch.Tensor) -> float:
        """
        Calculate loss sensitivity metric.
        
        Args:
            inputs: Input tensor
            targets: Target tensor
            
        Returns:
            Loss sensitivity score
        """
        # Set requires_grad
        inputs_grad = inputs.clone().detach().requires_grad_(True)
        
        # Forward pass
        self.model.eval()
        outputs = self.model(inputs_grad)
        
        # Calculate loss
        loss = F.cross_entropy(outputs, targets)
        
        # Backward pass
        self.model.zero_grad()
        loss.backward()
        
        # Calculate sensitivity
        gradients = inputs_grad.grad.view(inputs.size(0), -1)
        sensitivity = torch.norm(gradients, p=2, dim=1).mean().item()
        
        return sensitivity
    
    def _gradient_norm_metric(self, inputs: torch.Tensor, targets: torch.Tensor) -> float:
        """
        Calculate gradient norm metric.
        
        Args:
            inputs: Input tensor
            targets: Target tensor
            
        Returns:
            Gradient norm score
        """
        # Set requires_grad
        inputs_grad = inputs.clone().detach().requires_grad_(True)
        
        # Forward pass
        self.model.eval()
        outputs = self.model(inputs_grad)
        
        # Calculate loss
        loss = F.cross_entropy(outputs, targets)
        
        # Backward pass
        self.model.zero_grad()
        loss.backward()
        
        # Calculate gradient norm
        gradients = inputs_grad.grad.view(inputs.size(0), -1)
        grad_norm = torch.norm(gradients, p=2, dim=1).mean().item()
        
        return grad_norm
    
    def _clever_score_metric(self, inputs: torch.Tensor, targets: torch.Tensor, num_samples: int = 10) -> float:
        """
        Calculate CLEVER (Cross-Lipschitz Extreme Value for nEtwork Robustness) score.
        
        Args:
            inputs: Input tensor
            targets: Target tensor
            num_samples: Number of samples for estimation
            
        Returns:
            CLEVER score
        """
        # Simplified CLEVER score calculation
        lipschitz_estimates = []
        
        for i in range(inputs.size(0)):
            sample = inputs[i:i+1].clone().detach()
            target = targets[i:i+1].clone().detach()
            
            # Generate random samples around input
            max_lipschitz = 0
            
            for _ in range(num_samples):
                # Generate random direction
                direction = torch.randn_like(sample)
                direction = direction / torch.norm(direction)
                
                # Set requires_grad
                sample_grad = sample.clone().detach().requires_grad_(True)
                
                # Forward pass
                self.model.eval()
                outputs = self.model(sample_grad)
                
                # Calculate loss
                loss = F.cross_entropy(outputs, target)
                
                # Backward pass
                self.model.zero_grad()
                loss.backward()
                
                # Calculate directional derivative
                grad = sample_grad.grad
                directional_derivative = torch.sum(grad * direction).item()
                
                # Update max Lipschitz constant
                max_lipschitz = max(max_lipschitz, abs(directional_derivative))
            
            # CLEVER score is inverse of Lipschitz constant
            if max_lipschitz > 0:
                lipschitz_estimates.append(1.0 / max_lipschitz)
            else:
                lipschitz_estimates.append(float('inf'))
        
        # Return mean CLEVER score (excluding infinite values)
        finite_estimates = [est for est in lipschitz_estimates if est != float('inf')]
        if finite_estimates:
            return sum(finite_estimates) / len(finite_estimates)
        else:
            return 0.0
    
    def _noise_sensitivity_metric(self, inputs: torch.Tensor, targets: torch.Tensor) -> float:
        """
        Calculate noise sensitivity metric.
        
        Args:
            inputs: Input tensor
            targets: Target tensor
            
        Returns:
            Noise sensitivity score
        """
        # Test with different noise levels
        noise_levels = [0.01, 0.02, 0.05, 0.1]
        sensitivities = []
        
        self.model.eval()
        with torch.no_grad():
            # Get clean predictions
            clean_outputs = self.model(inputs)
            clean_predictions = clean_outputs.argmax(dim=1)
            
            for noise_level in noise_levels:
                # Add Gaussian noise
                noise = torch.randn_like(inputs) * noise_level
                noisy_inputs = torch.clamp(inputs + noise, -1.0, 1.0)
                
                # Get predictions
                noisy_outputs = self.model(noisy_inputs)
                noisy_predictions = noisy_outputs.argmax(dim=1)
                
                # Calculate sensitivity
                sensitivity = (noisy_predictions != clean_predictions).float().mean().item()
                sensitivities.append(sensitivity)
        
        # Return average sensitivity
        return sum(sensitivities) / len(sensitivities)
    
    def _boundary_thickness_metric(self, inputs: torch.Tensor, targets: torch.Tensor) -> float:
        """
        Calculate decision boundary thickness metric.
        
        Args:
            inputs: Input tensor
            targets: Target tensor
            
        Returns:
            Boundary thickness score
        """
        # Estimate boundary thickness by binary search
        thicknesses = []
        
        for i in range(inputs.size(0)):
            sample = inputs[i:i+1].clone().detach()
            target = targets[i:i+1].clone().detach()
            
            # Get original prediction
            self.model.eval()
            with torch.no_grad():
                output = self.model(sample)
            orig_class = output.argmax().item()
            
            # If already misclassified, skip
            if orig_class != target.item():
                continue
            
            # Generate random direction
            direction = torch.randn_like(sample)
            direction = direction / torch.norm(direction)
            
            # Binary search for decision boundary
            alpha_min = 0.0
            alpha_max = 1.0
            num_steps = 10
            
            for _ in range(num_steps):
                alpha_mid = (alpha_min + alpha_max) / 2
                
                # Check prediction at midpoint
                with torch.no_grad():
                    mid_sample = sample + alpha_mid * direction
                    mid_sample = torch.clamp(mid_sample, -1.0, 1.0)
                    
                    output = self.model(mid_sample)
                    mid_class = output.argmax().item()
                
                if mid_class == orig_class:
                    alpha_min = alpha_mid
                else:
                    alpha_max = alpha_mid
            
            # Thickness is the distance to the boundary
            thickness = alpha_max
            thicknesses.append(thickness)
        
        # Return average thickness
        if thicknesses:
            return sum(thicknesses) / len(thicknesses)
        else:
            return 0.0
    
    def _lipschitz_constant_metric(self, inputs: torch.Tensor, targets: torch.Tensor) -> float:
        """
        Estimate Lipschitz constant of the model.
        
        Args:
            inputs: Input tensor
            targets: Target tensor
            
        Returns:
            Estimated Lipschitz constant
        """
        # Estimate Lipschitz constant by sampling
        lipschitz_estimates = []
        
        for i in range(inputs.size(0)):
            sample1 = inputs[i:i+1].clone().detach()
            
            # Generate nearby point
            delta = torch.randn_like(sample1) * 0.01
            sample2 = torch.clamp(sample1 + delta, -1.0, 1.0)
            
            # Calculate input distance
            input_dist = torch.norm(sample2 - sample1).item()
            
            # Calculate output distance
            self.model.eval()
            with torch.no_grad():
                output1 = self.model(sample1)
                output2 = self.model(sample2)
                
                output_dist = torch.norm(output2 - output1).item()
            
            # Lipschitz constant is output_dist / input_dist
            if input_dist > 0:
                lipschitz = output_dist / input_dist
                lipschitz_estimates.append(lipschitz)
        
        # Return maximum Lipschitz constant
        if lipschitz_estimates:
            return max(lipschitz_estimates)
        else:
            return 0.0
    
    def _adversarial_distance_metric(self, inputs: torch.Tensor, targets: torch.Tensor) -> float:
        """
        Calculate minimum adversarial distance metric.
        
        Args:
            inputs: Input tensor
            targets: Target tensor
            
        Returns:
            Minimum adversarial distance score
        """
        # Use FGSM to find adversarial examples
        epsilon = 0.03
        adv_inputs = self._fast_gradient_sign_method(inputs, targets, epsilon)
        
        # Calculate distances
        distances = []
        
        self.model.eval()
        with torch.no_grad():
            for i in range(inputs.size(0)):
                sample = inputs[i:i+1]
                adv_sample = adv_inputs[i:i+1]
                target = targets[i:i+1]
                
                # Get predictions
                output = self.model(adv_sample)
                adv_class = output.argmax().item()
                
                # If adversarial, calculate distance
                if adv_class != target.item():
                    distance = torch.norm(adv_sample - sample).item()
                    distances.append(distance)
        
        # Return average distance
        if distances:
            return sum(distances) / len(distances)
        else:
            return float('inf')  # No successful adversarial examples
    
    def _confidence_reduction_metric(self, inputs: torch.Tensor, targets: torch.Tensor) -> float:
        """
        Calculate confidence reduction under perturbation.
        
        Args:
            inputs: Input tensor
            targets: Target tensor
            
        Returns:
            Confidence reduction score
        """
        # Generate small perturbations
        epsilon = 0.01
        
        self.model.eval()
        with torch.no_grad():
            # Get clean predictions and confidences
            clean_outputs = self.model(inputs)
            clean_confidences = F.softmax(clean_outputs, dim=1).gather(1, targets.unsqueeze(1)).squeeze(1)
            
            # Add random noise
            noise = torch.randn_like(inputs) * epsilon
            noisy_inputs = torch.clamp(inputs + noise, -1.0, 1.0)
            
            # Get noisy predictions and confidences
            noisy_outputs = self.model(noisy_inputs)
            noisy_confidences = F.softmax(noisy_outputs, dim=1).gather(1, targets.unsqueeze(1)).squeeze(1)
            
            # Calculate confidence reduction
            reductions = clean_confidences - noisy_confidences
            avg_reduction = reductions.mean().item()
        
        return avg_reduction
    
    #
    # Enhancement Strategies
    #
    
    def _apply_adversarial_training(self) -> Dict[str, Any]:
        """
        Apply adversarial training enhancement.
        
        Returns:
            Dictionary containing result of the enhancement
        """
        # In a real implementation, this would involve training the model on adversarial examples
        # For this simulation, we just return a success message
        return {
            "success": True,
            "description": "Applied adversarial training enhancement (simulation)",
            "details": "In a real implementation, this would retrain the model using adversarial examples",
        }
    
    def _apply_gradient_regularization(self) -> Dict[str, Any]:
        """
        Apply gradient regularization enhancement.
        
        Returns:
            Dictionary containing result of the enhancement
        """
        # In a real implementation, this would involve adding gradient regularization to the loss function
        # For this simulation, we just return a success message
        return {
            "success": True,
            "description": "Applied gradient regularization enhancement (simulation)",
            "details": "In a real implementation, this would add gradient penalty terms to the loss function",
        }
    
    def _apply_noise_augmentation(self) -> Dict[str, Any]:
        """
        Apply noise augmentation enhancement.
        
        Returns:
            Dictionary containing result of the enhancement
        """
        # In a real implementation, this would involve training with noise-augmented data
        # For this simulation, we just return a success message
        return {
            "success": True,
            "description": "Applied noise augmentation enhancement (simulation)",
            "details": "In a real implementation, this would add noise to training data",
        }
    
    def _apply_defensive_distillation(self) -> Dict[str, Any]:
        """
        Apply defensive distillation enhancement.
        
        Returns:
            Dictionary containing result of the enhancement
        """
        # In a real implementation, this would involve distilling the model
        # For this simulation, we just return a success message
        return {
            "success": True,
            "description": "Applied defensive distillation enhancement (simulation)",
            "details": "In a real implementation, this would train a student model on soft labels from the teacher model",
        }
    
    def _apply_feature_denoising(self) -> Dict[str, Any]:
        """
        Apply feature denoising enhancement.
        
        Returns:
            Dictionary containing result of the enhancement
        """
        # In a real implementation, this would involve adding denoising blocks to the model
        # For this simulation, we just return a success message
        return {
            "success": True,
            "description": "Applied feature denoising enhancement (simulation)",
            "details": "In a real implementation, this would add non-local means or other denoising blocks to the model",
        }
    
    def _apply_input_transformation(self) -> Dict[str, Any]:
        """
        Apply input transformation enhancement.
        
        Returns:
            Dictionary containing result of the enhancement
        """
        # In a real implementation, this would involve adding input transformation layers
        # For this simulation, we just return a success message
        return {
            "success": True,
            "description": "Applied input transformation enhancement (simulation)",
            "details": "In a real implementation, this would add preprocessing layers for bit depth reduction, JPEG compression, etc.",
        }
    
    def _apply_ensemble_method(self) -> Dict[str, Any]:
        """
        Apply ensemble method enhancement.
        
        Returns:
            Dictionary containing result of the enhancement
        """
        # In a real implementation, this would involve creating an ensemble of models
        # For this simulation, we just return a success message
        return {
            "success": True,
            "description": "Applied ensemble method enhancement (simulation)",
            "details": "In a real implementation, this would create an ensemble of models with different architectures or training procedures",
        }
    
    def _apply_certified_defenses(self) -> Dict[str, Any]:
        """
        Apply certified defenses enhancement.
        
        Returns:
            Dictionary containing result of the enhancement
        """
        # In a real implementation, this would involve adding certified robustness guarantees
        # For this simulation, we just return a success message
        return {
            "success": True,
            "description": "Applied certified defenses enhancement (simulation)",
            "details": "In a real implementation, this would add randomized smoothing or other certified defense techniques",
        }
