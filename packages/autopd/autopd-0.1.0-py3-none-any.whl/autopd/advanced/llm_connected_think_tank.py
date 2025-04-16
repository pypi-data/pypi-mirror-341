"""
LLM-Connected Think Tank Mode module for AutoPipelineDoctor.

This advanced module creates a multi-agent reasoning system that analyzes pipeline state,
debates optimization strategies, cites relevant research or bug reports, and outputs
a ranked list of best actions.
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
import requests
import uuid
import hashlib
import asyncio
from typing import Dict, List, Tuple, Optional, Union, Any, Callable, Set, Type
from enum import Enum
from dataclasses import dataclass, field
from collections import defaultdict, deque
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

logger = logging.getLogger(__name__)


class AgentRole(Enum):
    """Roles for agents in the think tank."""
    COORDINATOR = "coordinator"
    PERFORMANCE_ANALYST = "performance_analyst"
    MEMORY_OPTIMIZER = "memory_optimizer"
    NUMERICAL_STABILITY_EXPERT = "numerical_stability_expert"
    ARCHITECTURE_SPECIALIST = "architecture_specialist"
    RESEARCH_SCIENTIST = "research_scientist"
    HARDWARE_ENGINEER = "hardware_engineer"
    DATALOADER_SPECIALIST = "dataloader_specialist"
    TRAINING_DYNAMICS_EXPERT = "training_dynamics_expert"
    DEVIL_ADVOCATE = "devil_advocate"
    CUSTOM = "custom"


class DebateStage(Enum):
    """Stages of the think tank debate."""
    PROBLEM_DEFINITION = "problem_definition"
    ANALYSIS = "analysis"
    SOLUTION_GENERATION = "solution_generation"
    CRITIQUE = "critique"
    REFINEMENT = "refinement"
    CONSENSUS = "consensus"
    RECOMMENDATION = "recommendation"


class RecommendationCategory(Enum):
    """Categories for recommendations."""
    MEMORY_OPTIMIZATION = "memory_optimization"
    PERFORMANCE_OPTIMIZATION = "performance_optimization"
    NUMERICAL_STABILITY = "numerical_stability"
    ARCHITECTURE_MODIFICATION = "architecture_modification"
    DATALOADER_OPTIMIZATION = "dataloader_optimization"
    TRAINING_STRATEGY = "training_strategy"
    HARDWARE_UTILIZATION = "hardware_utilization"
    DEBUGGING = "debugging"
    RESEARCH_DIRECTION = "research_direction"
    CUSTOM = "custom"


class RecommendationPriority(Enum):
    """Priority levels for recommendations."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    EXPERIMENTAL = "experimental"


class RecommendationRisk(Enum):
    """Risk levels for recommendations."""
    SAFE = "safe"
    LOW_RISK = "low_risk"
    MEDIUM_RISK = "medium_risk"
    HIGH_RISK = "high_risk"
    EXPERIMENTAL = "experimental"


class LLMProvider(Enum):
    """Supported LLM providers."""
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    HUGGINGFACE = "huggingface"
    AZURE_OPENAI = "azure_openai"
    LOCAL = "local"
    CUSTOM = "custom"


@dataclass
class LLMConfig:
    """Configuration for LLM providers."""
    provider: LLMProvider = LLMProvider.OPENAI
    model_name: str = "gpt-4"
    api_key: str = ""
    api_base: str = ""
    api_version: str = ""
    max_tokens: int = 1000
    temperature: float = 0.7
    top_p: float = 1.0
    frequency_penalty: float = 0.0
    presence_penalty: float = 0.0
    timeout: float = 60.0
    custom_parameters: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AgentConfig:
    """Configuration for an agent."""
    role: AgentRole
    llm_config: LLMConfig
    system_prompt: str
    expertise_areas: List[str] = field(default_factory=list)
    citation_sources: List[str] = field(default_factory=list)
    custom_parameters: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ThinkTankConfig:
    """Configuration for the think tank."""
    agents: List[AgentConfig] = field(default_factory=list)
    max_debate_rounds: int = 5
    max_tokens_per_message: int = 1000
    debate_timeout: float = 300.0
    include_citations: bool = True
    include_code_examples: bool = True
    include_research_references: bool = True
    save_debate_history: bool = True
    debate_history_dir: str = "./debate_history"
    custom_parameters: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Message:
    """Message in the think tank debate."""
    agent_role: AgentRole
    content: str
    stage: DebateStage
    timestamp: float = field(default_factory=time.time)
    references: List[Dict[str, str]] = field(default_factory=list)
    code_snippets: List[Dict[str, str]] = field(default_factory=list)
    metrics: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Recommendation:
    """Recommendation from the think tank."""
    title: str
    description: str
    category: RecommendationCategory
    priority: RecommendationPriority
    risk: RecommendationRisk
    implementation_steps: List[str] = field(default_factory=list)
    code_snippet: Optional[str] = None
    references: List[Dict[str, str]] = field(default_factory=list)
    metrics_impact: Dict[str, float] = field(default_factory=dict)
    confidence: float = 0.0
    votes: int = 0
    agent_roles: List[AgentRole] = field(default_factory=list)


@dataclass
class DebateResult:
    """Result of a think tank debate."""
    recommendations: List[Recommendation]
    debate_history: List[Message]
    metrics_analyzed: Dict[str, Any]
    consensus_reached: bool
    debate_duration: float
    timestamp: float = field(default_factory=time.time)
    debate_id: str = field(default_factory=lambda: str(uuid.uuid4()))


class Agent:
    """
    Agent in the think tank.
    
    Attributes:
        config: Agent configuration
        llm_client: LLM client for generating responses
        message_history: History of messages from this agent
        knowledge_base: Knowledge base for this agent
    """
    
    def __init__(self, config: AgentConfig):
        """
        Initialize the agent.
        
        Args:
            config: Agent configuration
        """
        self.config = config
        self.llm_client = self._create_llm_client()
        self.message_history: List[Message] = []
        self.knowledge_base: Dict[str, Any] = {}
        
        logger.info(f"Initialized agent with role: {config.role.value}")
    
    def _create_llm_client(self) -> Any:
        """
        Create LLM client based on provider.
        
        Returns:
            LLM client
        """
        llm_config = self.config.llm_config
        
        if llm_config.provider == LLMProvider.OPENAI:
            try:
                import openai
                
                client = openai.OpenAI(
                    api_key=llm_config.api_key or os.environ.get("OPENAI_API_KEY"),
                    base_url=llm_config.api_base or openai.base_url,
                    timeout=llm_config.timeout,
                )
                
                return client
            except ImportError:
                logger.warning("OpenAI package not installed, using mock client")
                return MockLLMClient()
        
        elif llm_config.provider == LLMProvider.ANTHROPIC:
            try:
                import anthropic
                
                client = anthropic.Anthropic(
                    api_key=llm_config.api_key or os.environ.get("ANTHROPIC_API_KEY"),
                )
                
                return client
            except ImportError:
                logger.warning("Anthropic package not installed, using mock client")
                return MockLLMClient()
        
        elif llm_config.provider == LLMProvider.AZURE_OPENAI:
            try:
                import openai
                
                client = openai.AzureOpenAI(
                    api_key=llm_config.api_key or os.environ.get("AZURE_OPENAI_API_KEY"),
                    api_version=llm_config.api_version or "2023-05-15",
                    azure_endpoint=llm_config.api_base or os.environ.get("AZURE_OPENAI_ENDPOINT"),
                    timeout=llm_config.timeout,
                )
                
                return client
            except ImportError:
                logger.warning("OpenAI package not installed, using mock client")
                return MockLLMClient()
        
        elif llm_config.provider == LLMProvider.HUGGINGFACE:
            try:
                from huggingface_hub import InferenceClient
                
                client = InferenceClient(
                    token=llm_config.api_key or os.environ.get("HF_API_TOKEN"),
                    timeout=llm_config.timeout,
                )
                
                return client
            except ImportError:
                logger.warning("Hugging Face package not installed, using mock client")
                return MockLLMClient()
        
        elif llm_config.provider == LLMProvider.LOCAL:
            try:
                from transformers import AutoModelForCausalLM, AutoTokenizer
                
                model_name = llm_config.model_name or "TheBloke/Llama-2-7B-Chat-GGUF"
                
                tokenizer = AutoTokenizer.from_pretrained(model_name)
                model = AutoModelForCausalLM.from_pretrained(model_name)
                
                return {"model": model, "tokenizer": tokenizer}
            except ImportError:
                logger.warning("Transformers package not installed, using mock client")
                return MockLLMClient()
        
        else:
            logger.warning(f"Unsupported LLM provider: {llm_config.provider}, using mock client")
            return MockLLMClient()
    
    async def generate_response(
        self,
        prompt: str,
        debate_history: List[Message],
        metrics: Dict[str, Any],
        stage: DebateStage,
    ) -> Message:
        """
        Generate a response from the agent.
        
        Args:
            prompt: Prompt for the agent
            debate_history: History of the debate
            metrics: Current metrics
            stage: Current debate stage
            
        Returns:
            Agent's response message
        """
        llm_config = self.config.llm_config
        
        # Format debate history for context
        formatted_history = self._format_debate_history(debate_history)
        
        # Format metrics for context
        formatted_metrics = self._format_metrics(metrics)
        
        # Create full prompt
        full_prompt = f"{self.config.system_prompt}\n\n"
        full_prompt += f"Current debate stage: {stage.value}\n\n"
        full_prompt += f"Debate history:\n{formatted_history}\n\n"
        full_prompt += f"Current metrics:\n{formatted_metrics}\n\n"
        full_prompt += f"Prompt: {prompt}\n\n"
        full_prompt += f"As the {self.config.role.value}, provide your analysis and recommendations."
        
        try:
            # Generate response based on provider
            if llm_config.provider == LLMProvider.OPENAI:
                response_text = await self._generate_openai_response(full_prompt)
            elif llm_config.provider == LLMProvider.ANTHROPIC:
                response_text = await self._generate_anthropic_response(full_prompt)
            elif llm_config.provider == LLMProvider.AZURE_OPENAI:
                response_text = await self._generate_azure_openai_response(full_prompt)
            elif llm_config.provider == LLMProvider.HUGGINGFACE:
                response_text = await self._generate_huggingface_response(full_prompt)
            elif llm_config.provider == LLMProvider.LOCAL:
                response_text = await self._generate_local_response(full_prompt)
            else:
                response_text = await self._generate_mock_response(full_prompt)
            
            # Extract references and code snippets
            references = self._extract_references(response_text)
            code_snippets = self._extract_code_snippets(response_text)
            
            # Create message
            message = Message(
                agent_role=self.config.role,
                content=response_text,
                stage=stage,
                references=references,
                code_snippets=code_snippets,
                metrics=metrics,
            )
            
            # Add to message history
            self.message_history.append(message)
            
            return message
        
        except Exception as e:
            logger.error(f"Error generating response from {self.config.role.value}: {e}")
            logger.error(traceback.format_exc())
            
            # Create error message
            error_message = Message(
                agent_role=self.config.role,
                content=f"Error generating response: {str(e)}",
                stage=stage,
                metrics=metrics,
            )
            
            return error_message
    
    async def _generate_openai_response(self, prompt: str) -> str:
        """
        Generate response using OpenAI.
        
        Args:
            prompt: Full prompt
            
        Returns:
            Generated response
        """
        llm_config = self.config.llm_config
        client = self.llm_client
        
        try:
            response = await asyncio.to_thread(
                client.chat.completions.create,
                model=llm_config.model_name,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=llm_config.max_tokens,
                temperature=llm_config.temperature,
                top_p=llm_config.top_p,
                frequency_penalty=llm_config.frequency_penalty,
                presence_penalty=llm_config.presence_penalty,
            )
            
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            raise
    
    async def _generate_anthropic_response(self, prompt: str) -> str:
        """
        Generate response using Anthropic.
        
        Args:
            prompt: Full prompt
            
        Returns:
            Generated response
        """
        llm_config = self.config.llm_config
        client = self.llm_client
        
        try:
            response = await asyncio.to_thread(
                client.messages.create,
                model=llm_config.model_name,
                max_tokens=llm_config.max_tokens,
                temperature=llm_config.temperature,
                messages=[{"role": "user", "content": prompt}],
            )
            
            return response.content[0].text
        except Exception as e:
            logger.error(f"Anthropic API error: {e}")
            raise
    
    async def _generate_azure_openai_response(self, prompt: str) -> str:
        """
        Generate response using Azure OpenAI.
        
        Args:
            prompt: Full prompt
            
        Returns:
            Generated response
        """
        llm_config = self.config.llm_config
        client = self.llm_client
        
        try:
            response = await asyncio.to_thread(
                client.chat.completions.create,
                model=llm_config.model_name,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=llm_config.max_tokens,
                temperature=llm_config.temperature,
                top_p=llm_config.top_p,
                frequency_penalty=llm_config.frequency_penalty,
                presence_penalty=llm_config.presence_penalty,
            )
            
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Azure OpenAI API error: {e}")
            raise
    
    async def _generate_huggingface_response(self, prompt: str) -> str:
        """
        Generate response using Hugging Face.
        
        Args:
            prompt: Full prompt
            
        Returns:
            Generated response
        """
        llm_config = self.config.llm_config
        client = self.llm_client
        
        try:
            response = await asyncio.to_thread(
                client.text_generation,
                prompt=prompt,
                model=llm_config.model_name,
                max_new_tokens=llm_config.max_tokens,
                temperature=llm_config.temperature,
                top_p=llm_config.top_p,
            )
            
            return response
        except Exception as e:
            logger.error(f"Hugging Face API error: {e}")
            raise
    
    async def _generate_local_response(self, prompt: str) -> str:
        """
        Generate response using local model.
        
        Args:
            prompt: Full prompt
            
        Returns:
            Generated response
        """
        llm_config = self.config.llm_config
        model_data = self.llm_client
        
        try:
            model = model_data["model"]
            tokenizer = model_data["tokenizer"]
            
            inputs = tokenizer(prompt, return_tensors="pt")
            outputs = await asyncio.to_thread(
                model.generate,
                inputs["input_ids"],
                max_new_tokens=llm_config.max_tokens,
                temperature=llm_config.temperature,
                top_p=llm_config.top_p,
            )
            
            response = tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            # Remove the prompt from the response
            response = response[len(prompt):].strip()
            
            return response
        except Exception as e:
            logger.error(f"Local model error: {e}")
            raise
    
    async def _generate_mock_response(self, prompt: str) -> str:
        """
        Generate mock response for testing.
        
        Args:
            prompt: Full prompt
            
        Returns:
            Generated response
        """
        role = self.config.role.value
        
        # Generate a deterministic but varied response based on role and prompt
        prompt_hash = hashlib.md5(prompt.encode()).hexdigest()[:8]
        
        responses = {
            AgentRole.COORDINATOR.value: f"As the coordinator, I've analyzed the situation and suggest we focus on optimizing the batch size and memory usage. Let's hear from the memory and performance experts.\n\nReferences:\n[1] Smith et al., 'Efficient Training Strategies', 2023\n\n```python\n# Example coordination code\ndef coordinate_optimization(model, optimizer):\n    # Monitor metrics and delegate to specialists\n    pass\n```",
            
            AgentRole.PERFORMANCE_ANALYST.value: f"Looking at the performance metrics, I notice several bottlenecks in the forward pass. The batch size could be increased by 30% with proper memory optimization.\n\nReferences:\n[1] Johnson et al., 'Performance Analysis of Deep Learning Models', 2022\n\n```python\n# Performance optimization\ndef optimize_forward_pass(model):\n    # Use torch.compile for speedup\n    return torch.compile(model)\n```",
            
            AgentRole.MEMORY_OPTIMIZER.value: f"The memory usage pattern shows fragmentation and inefficient tensor allocation. I recommend implementing gradient checkpointing and using torch.cuda.amp for mixed precision training.\n\nReferences:\n[1] Chen et al., 'Memory Optimization Techniques', 2023\n\n```python\n# Memory optimization\ndef apply_gradient_checkpointing(model):\n    model.gradient_checkpointing_enable()\n    return model\n```",
            
            AgentRole.NUMERICAL_STABILITY_EXPERT.value: f"I'm seeing potential numerical instability in the loss calculation. The gradient norms are fluctuating significantly. Consider gradient clipping and a more robust loss function.\n\nReferences:\n[1] Wang et al., 'Numerical Stability in Deep Learning', 2021\n\n```python\n# Numerical stability\ndef apply_gradient_clipping(optimizer, max_norm=1.0):\n    torch.nn.utils.clip_grad_norm_(optimizer.parameters(), max_norm)\n```",
            
            AgentRole.ARCHITECTURE_SPECIALIST.value: f"The model architecture could be optimized by replacing some of the dense layers with more efficient attention mechanisms. This would reduce parameter count while maintaining model capacity.\n\nReferences:\n[1] Li et al., 'Efficient Transformer Architectures', 2023\n\n```python\n# Architecture optimization\nclass EfficientAttention(nn.Module):\n    def __init__(self, dim, heads=8):\n        super().__init__()\n        # Efficient attention implementation\n        pass\n```",
            
            AgentRole.RESEARCH_SCIENTIST.value: f"Recent research suggests that {prompt_hash}-based regularization techniques can improve generalization for this type of model. I recommend experimenting with this approach.\n\nReferences:\n[1] Zhang et al., 'Advanced Regularization Techniques', 2023\n[2] Brown et al., 'Generalization in Deep Learning', 2022\n\n```python\n# Implementation of recent research\ndef apply_advanced_regularization(model, strength=0.1):\n    # Apply {prompt_hash}-based regularization\n    pass\n```",
            
            AgentRole.HARDWARE_ENGINEER.value: f"The GPU utilization is suboptimal. We're seeing memory bandwidth limitations and compute underutilization. Restructuring the operations to improve parallelism would help.\n\nReferences:\n[1] Nvidia, 'GPU Performance Optimization Guide', 2023\n\n```python\n# Hardware optimization\ndef optimize_for_gpu(model):\n    # Use channels_last memory format\n    model = model.to(memory_format=torch.channels_last)\n    return model\n```",
            
            AgentRole.DATALOADER_SPECIALIST.value: f"The dataloader is creating a bottleneck. Increasing num_workers and implementing prefetching would improve throughput. Also consider using faster data formats like WebDataset.\n\nReferences:\n[1] PyTorch, 'DataLoader Best Practices', 2023\n\n```python\n# Dataloader optimization\ndef create_optimized_dataloader(dataset, batch_size=32):\n    return DataLoader(\n        dataset,\n        batch_size=batch_size,\n        num_workers=4,\n        pin_memory=True,\n        prefetch_factor=2\n    )\n```",
            
            AgentRole.TRAINING_DYNAMICS_EXPERT.value: f"The learning rate schedule could be improved. I'm seeing signs of the model getting stuck in local minima. Consider using a cyclical learning rate or a more sophisticated scheduler.\n\nReferences:\n[1] Smith, 'Cyclical Learning Rates for Training Neural Networks', 2017\n\n```python\n# Learning rate scheduling\ndef create_cyclical_lr_scheduler(optimizer, base_lr=1e-4, max_lr=1e-3):\n    return torch.optim.lr_scheduler.CyclicLR(\n        optimizer,\n        base_lr=base_lr,\n        max_lr=max_lr,\n        step_size_up=2000,\n        mode='triangular2'\n    )\n```",
            
            AgentRole.DEVIL_ADVOCATE.value: f"I disagree with some of the proposed optimizations. The memory savings from gradient checkpointing might be offset by the recomputation cost. We should benchmark this carefully before implementation.\n\nReferences:\n[1] Critical Analysis of Optimization Techniques, 2023\n\n```python\n# Benchmarking code\ndef benchmark_gradient_checkpointing(model, inputs):\n    # Measure performance with and without checkpointing\n    times = []\n    memory = []\n    # Implementation details\n    return {'times': times, 'memory': memory}\n```",
        }
        
        # Default response for custom roles
        default_response = f"As a {role} specialist, I've analyzed the situation and have the following recommendations based on the metrics and debate history.\n\nReferences:\n[1] Expert Analysis, 2023\n\n```python\n# Example code\ndef optimize_for_{role}(model, optimizer):\n    # Specialized optimization\n    pass\n```"
        
        # Get response for this role or use default
        response = responses.get(role, default_response)
        
        # Add some variation based on the prompt hash
        variations = [
            f"\n\nAdditionally, the {prompt_hash} pattern in the metrics suggests we should consider adjusting the learning rate.",
            f"\n\nI also noticed that the {prompt_hash} component could be further optimized.",
            f"\n\nBased on my analysis of similar cases, the {prompt_hash} approach has shown promising results.",
            f"\n\nWe should be cautious about the {prompt_hash} effect, which could lead to instability.",
            f"\n\nThe {prompt_hash} technique mentioned in recent literature could be applicable here.",
        ]
        
        # Add a variation based on the hash
        variation_index = int(prompt_hash, 16) % len(variations)
        response += variations[variation_index]
        
        # Simulate async behavior
        await asyncio.sleep(0.5)
        
        return response
    
    def _format_debate_history(self, debate_history: List[Message]) -> str:
        """
        Format debate history for the prompt.
        
        Args:
            debate_history: History of the debate
            
        Returns:
            Formatted debate history
        """
        if not debate_history:
            return "No previous messages."
        
        formatted_history = ""
        
        for i, message in enumerate(debate_history[-10:]):  # Limit to last 10 messages
            timestamp = datetime.datetime.fromtimestamp(message.timestamp).strftime("%H:%M:%S")
            formatted_history += f"[{timestamp}] {message.agent_role.value} ({message.stage.value}):\n{message.content}\n\n"
        
        return formatted_history
    
    def _format_metrics(self, metrics: Dict[str, Any]) -> str:
        """
        Format metrics for the prompt.
        
        Args:
            metrics: Current metrics
            
        Returns:
            Formatted metrics
        """
        if not metrics:
            return "No metrics available."
        
        formatted_metrics = ""
        
        for key, value in metrics.items():
            if isinstance(value, (int, float)):
                formatted_metrics += f"{key}: {value}\n"
            elif isinstance(value, (list, tuple)) and len(value) > 0:
                if len(value) > 5:
                    # For long lists, show first 3 and last 2 elements
                    formatted_values = [str(v) for v in value[:3]] + ["..."] + [str(v) for v in value[-2:]]
                    formatted_metrics += f"{key}: [{', '.join(formatted_values)}]\n"
                else:
                    formatted_metrics += f"{key}: [{', '.join(str(v) for v in value)}]\n"
            else:
                formatted_metrics += f"{key}: {str(value)}\n"
        
        return formatted_metrics
    
    def _extract_references(self, text: str) -> List[Dict[str, str]]:
        """
        Extract references from the response.
        
        Args:
            text: Response text
            
        Returns:
            List of references
        """
        references = []
        
        # Look for references in the format [1] Author, 'Title', Year
        reference_pattern = r'\[(\d+)\]\s+([^,]+),\s+[\'"]([^\'"]*)[\'"]\s*,\s*(\d{4})'
        matches = re.findall(reference_pattern, text)
        
        for match in matches:
            reference_number, author, title, year = match
            references.append({
                "number": reference_number,
                "author": author.strip(),
                "title": title.strip(),
                "year": year.strip(),
                "full_citation": f"[{reference_number}] {author}, '{title}', {year}",
            })
        
        return references
    
    def _extract_code_snippets(self, text: str) -> List[Dict[str, str]]:
        """
        Extract code snippets from the response.
        
        Args:
            text: Response text
            
        Returns:
            List of code snippets
        """
        code_snippets = []
        
        # Look for code snippets in the format ```python ... ```
        code_pattern = r'```(?:python)?\s*(.*?)\s*```'
        matches = re.findall(code_pattern, text, re.DOTALL)
        
        for i, match in enumerate(matches):
            code_snippets.append({
                "index": i,
                "language": "python",
                "code": match.strip(),
            })
        
        return code_snippets


class MockLLMClient:
    """Mock LLM client for testing."""
    
    def __init__(self):
        """Initialize the mock client."""
        pass


class LLMConnectedThinkTank:
    """
    LLM-Connected Think Tank Mode for AutoPipelineDoctor.
    
    This module creates a multi-agent reasoning system that analyzes pipeline state,
    debates optimization strategies, cites relevant research or bug reports, and outputs
    a ranked list of best actions.
    
    Attributes:
        config: Think tank configuration
        agents: Dictionary of agents by role
        debate_history: History of all debates
        current_debate: Current debate messages
        recommendations: List of recommendations
        metrics_history: History of metrics
        running: Whether the think tank is running
    """
    
    def __init__(self, config: Optional[ThinkTankConfig] = None):
        """
        Initialize the LLMConnectedThinkTank.
        
        Args:
            config: Think tank configuration
        """
        # Initialize configuration
        self.config = config or self._default_config()
        
        # Initialize agents
        self.agents: Dict[AgentRole, Agent] = {}
        self._initialize_agents()
        
        # Initialize debate history
        self.debate_history: List[DebateResult] = []
        self.current_debate: List[Message] = []
        
        # Initialize recommendations
        self.recommendations: List[Recommendation] = []
        
        # Initialize metrics history
        self.metrics_history: Dict[str, List[Any]] = defaultdict(list)
        
        # Initialize state
        self.running: bool = False
        self.debate_in_progress: bool = False
        
        # Initialize locks
        self.debate_lock = asyncio.Lock()
        
        # Initialize debate history directory
        if self.config.save_debate_history:
            os.makedirs(self.config.debate_history_dir, exist_ok=True)
        
        logger.info("Initialized LLMConnectedThinkTank")
    
    def _default_config(self) -> ThinkTankConfig:
        """
        Create default think tank configuration.
        
        Returns:
            Default configuration
        """
        # Default LLM configuration
        default_llm_config = LLMConfig(
            provider=LLMProvider.OPENAI,
            model_name="gpt-4",
            api_key="",
            max_tokens=1000,
            temperature=0.7,
        )
        
        # Create agent configurations
        agents = []
        
        # Coordinator
        agents.append(AgentConfig(
            role=AgentRole.COORDINATOR,
            llm_config=copy.deepcopy(default_llm_config),
            system_prompt=(
                "You are the Coordinator in a multi-agent think tank for optimizing ML/AI training pipelines. "
                "Your role is to guide the discussion, synthesize insights from other agents, and ensure the "
                "debate remains focused on finding practical solutions. You should identify the most promising "
                "recommendations and help build consensus."
            ),
            expertise_areas=["facilitation", "synthesis", "decision making"],
        ))
        
        # Performance Analyst
        agents.append(AgentConfig(
            role=AgentRole.PERFORMANCE_ANALYST,
            llm_config=copy.deepcopy(default_llm_config),
            system_prompt=(
                "You are the Performance Analyst in a multi-agent think tank for optimizing ML/AI training pipelines. "
                "Your role is to identify performance bottlenecks, analyze throughput metrics, and recommend "
                "optimizations to improve training speed. Focus on computational efficiency, parallelism, and "
                "identifying operations that could be optimized."
            ),
            expertise_areas=["performance profiling", "throughput optimization", "computational efficiency"],
            citation_sources=["PyTorch performance guides", "NVIDIA optimization documentation"],
        ))
        
        # Memory Optimizer
        agents.append(AgentConfig(
            role=AgentRole.MEMORY_OPTIMIZER,
            llm_config=copy.deepcopy(default_llm_config),
            system_prompt=(
                "You are the Memory Optimizer in a multi-agent think tank for optimizing ML/AI training pipelines. "
                "Your role is to analyze memory usage patterns, identify memory bottlenecks, and recommend "
                "techniques to reduce memory consumption. Focus on gradient checkpointing, mixed precision training, "
                "and efficient tensor operations."
            ),
            expertise_areas=["memory profiling", "memory optimization", "OOM prevention"],
            citation_sources=["PyTorch memory management guides", "Academic papers on memory optimization"],
        ))
        
        # Numerical Stability Expert
        agents.append(AgentConfig(
            role=AgentRole.NUMERICAL_STABILITY_EXPERT,
            llm_config=copy.deepcopy(default_llm_config),
            system_prompt=(
                "You are the Numerical Stability Expert in a multi-agent think tank for optimizing ML/AI training pipelines. "
                "Your role is to identify numerical issues like gradient vanishing/exploding, NaN/Inf values, and "
                "recommend techniques to improve stability. Focus on normalization, initialization, and loss function design."
            ),
            expertise_areas=["numerical analysis", "gradient issues", "loss function design"],
            citation_sources=["Academic papers on numerical stability", "Deep learning textbooks"],
        ))
        
        # Architecture Specialist
        agents.append(AgentConfig(
            role=AgentRole.ARCHITECTURE_SPECIALIST,
            llm_config=copy.deepcopy(default_llm_config),
            system_prompt=(
                "You are the Architecture Specialist in a multi-agent think tank for optimizing ML/AI training pipelines. "
                "Your role is to analyze model architectures and recommend structural improvements. Focus on layer design, "
                "activation functions, and architectural patterns that could improve performance or reduce complexity."
            ),
            expertise_areas=["neural architecture", "model design", "structural optimization"],
            citation_sources=["Academic papers on neural architectures", "Model architecture benchmarks"],
        ))
        
        # Research Scientist
        agents.append(AgentConfig(
            role=AgentRole.RESEARCH_SCIENTIST,
            llm_config=copy.deepcopy(default_llm_config),
            system_prompt=(
                "You are the Research Scientist in a multi-agent think tank for optimizing ML/AI training pipelines. "
                "Your role is to bring cutting-edge research insights to the discussion. Cite relevant papers, "
                "suggest novel techniques, and evaluate the theoretical soundness of proposed solutions."
            ),
            expertise_areas=["research literature", "theoretical analysis", "novel techniques"],
            citation_sources=["arXiv papers", "ML conference proceedings", "Research journals"],
        ))
        
        # Hardware Engineer
        agents.append(AgentConfig(
            role=AgentRole.HARDWARE_ENGINEER,
            llm_config=copy.deepcopy(default_llm_config),
            system_prompt=(
                "You are the Hardware Engineer in a multi-agent think tank for optimizing ML/AI training pipelines. "
                "Your role is to analyze hardware utilization and recommend optimizations specific to the underlying "
                "hardware. Focus on GPU/CPU/TPU-specific optimizations, memory bandwidth, and compute efficiency."
            ),
            expertise_areas=["hardware optimization", "GPU/CPU/TPU architecture", "hardware-software co-design"],
            citation_sources=["Hardware vendor documentation", "Hardware optimization guides"],
        ))
        
        # Dataloader Specialist
        agents.append(AgentConfig(
            role=AgentRole.DATALOADER_SPECIALIST,
            llm_config=copy.deepcopy(default_llm_config),
            system_prompt=(
                "You are the Dataloader Specialist in a multi-agent think tank for optimizing ML/AI training pipelines. "
                "Your role is to analyze data loading processes and recommend optimizations. Focus on I/O efficiency, "
                "preprocessing, caching, and parallelism in data loading."
            ),
            expertise_areas=["data loading", "I/O optimization", "preprocessing efficiency"],
            citation_sources=["PyTorch DataLoader documentation", "Data loading benchmarks"],
        ))
        
        # Training Dynamics Expert
        agents.append(AgentConfig(
            role=AgentRole.TRAINING_DYNAMICS_EXPERT,
            llm_config=copy.deepcopy(default_llm_config),
            system_prompt=(
                "You are the Training Dynamics Expert in a multi-agent think tank for optimizing ML/AI training pipelines. "
                "Your role is to analyze learning curves, convergence behavior, and recommend improvements to training "
                "dynamics. Focus on learning rate schedules, optimizers, and regularization techniques."
            ),
            expertise_areas=["optimization algorithms", "learning rate scheduling", "convergence analysis"],
            citation_sources=["Optimization algorithm papers", "Learning dynamics research"],
        ))
        
        # Devil's Advocate
        agents.append(AgentConfig(
            role=AgentRole.DEVIL_ADVOCATE,
            llm_config=copy.deepcopy(default_llm_config),
            system_prompt=(
                "You are the Devil's Advocate in a multi-agent think tank for optimizing ML/AI training pipelines. "
                "Your role is to critically evaluate proposed solutions, identify potential risks or downsides, "
                "and ensure the team considers alternative perspectives. Be constructively critical but not negative."
            ),
            expertise_areas=["critical analysis", "risk assessment", "alternative perspectives"],
        ))
        
        # Create think tank configuration
        return ThinkTankConfig(
            agents=agents,
            max_debate_rounds=5,
            max_tokens_per_message=1000,
            debate_timeout=300.0,
            include_citations=True,
            include_code_examples=True,
            include_research_references=True,
            save_debate_history=True,
            debate_history_dir="./debate_history",
        )
    
    def _initialize_agents(self) -> None:
        """Initialize agents from configuration."""
        for agent_config in self.config.agents:
            self.agents[agent_config.role] = Agent(agent_config)
        
        logger.info(f"Initialized {len(self.agents)} agents")
    
    async def start_debate(
        self,
        problem_statement: str,
        metrics: Dict[str, Any],
        model_info: Optional[Dict[str, Any]] = None,
        dataset_info: Optional[Dict[str, Any]] = None,
        hardware_info: Optional[Dict[str, Any]] = None,
        custom_context: Optional[Dict[str, Any]] = None,
    ) -> DebateResult:
        """
        Start a new think tank debate.
        
        Args:
            problem_statement: Description of the problem to solve
            metrics: Current metrics
            model_info: Information about the model
            dataset_info: Information about the dataset
            hardware_info: Information about the hardware
            custom_context: Additional custom context
            
        Returns:
            Result of the debate
        """
        # Check if debate is already in progress
        async with self.debate_lock:
            if self.debate_in_progress:
                logger.warning("Debate already in progress, cannot start a new one")
                raise RuntimeError("Debate already in progress")
            
            self.debate_in_progress = True
        
        try:
            # Record start time
            start_time = time.time()
            
            # Clear current debate
            self.current_debate = []
            
            # Update metrics history
            self._update_metrics_history(metrics)
            
            # Create context
            context = {
                "problem_statement": problem_statement,
                "metrics": metrics,
                "model_info": model_info or {},
                "dataset_info": dataset_info or {},
                "hardware_info": hardware_info or {},
                "custom_context": custom_context or {},
            }
            
            # Run debate
            logger.info("Starting think tank debate")
            
            # Problem definition stage
            await self._run_debate_stage(
                DebateStage.PROBLEM_DEFINITION,
                f"Define the problem based on the following statement: {problem_statement}",
                context,
            )
            
            # Analysis stage
            await self._run_debate_stage(
                DebateStage.ANALYSIS,
                "Analyze the metrics and identify potential issues or optimization opportunities.",
                context,
            )
            
            # Solution generation stage
            await self._run_debate_stage(
                DebateStage.SOLUTION_GENERATION,
                "Generate potential solutions to address the identified issues.",
                context,
            )
            
            # Critique stage
            await self._run_debate_stage(
                DebateStage.CRITIQUE,
                "Critique the proposed solutions, identifying potential risks or limitations.",
                context,
            )
            
            # Refinement stage
            await self._run_debate_stage(
                DebateStage.REFINEMENT,
                "Refine the solutions based on the critique and develop concrete implementation steps.",
                context,
            )
            
            # Consensus stage
            await self._run_debate_stage(
                DebateStage.CONSENSUS,
                "Build consensus on the most promising solutions and prioritize recommendations.",
                context,
            )
            
            # Recommendation stage
            await self._run_debate_stage(
                DebateStage.RECOMMENDATION,
                "Formulate final recommendations with implementation details and expected impact.",
                context,
            )
            
            # Extract recommendations
            recommendations = self._extract_recommendations()
            
            # Calculate debate duration
            debate_duration = time.time() - start_time
            
            # Create debate result
            result = DebateResult(
                recommendations=recommendations,
                debate_history=self.current_debate,
                metrics_analyzed=metrics,
                consensus_reached=True,  # Assume consensus was reached
                debate_duration=debate_duration,
            )
            
            # Save debate history
            if self.config.save_debate_history:
                self._save_debate_history(result)
            
            # Add to debate history
            self.debate_history.append(result)
            
            # Update recommendations
            self.recommendations = recommendations
            
            logger.info(f"Completed think tank debate in {debate_duration:.2f} seconds with {len(recommendations)} recommendations")
            
            return result
        
        finally:
            # Reset debate in progress flag
            async with self.debate_lock:
                self.debate_in_progress = False
    
    async def _run_debate_stage(
        self,
        stage: DebateStage,
        prompt: str,
        context: Dict[str, Any],
    ) -> None:
        """
        Run a stage of the debate.
        
        Args:
            stage: Debate stage
            prompt: Prompt for the stage
            context: Context information
        """
        logger.info(f"Running debate stage: {stage.value}")
        
        # Start with coordinator
        coordinator_role = AgentRole.COORDINATOR
        coordinator = self.agents.get(coordinator_role)
        
        if not coordinator:
            logger.warning(f"Coordinator agent not found, using first available agent")
            coordinator_role, coordinator = next(iter(self.agents.items()))
        
        # Generate coordinator message
        coordinator_message = await coordinator.generate_response(
            prompt=prompt,
            debate_history=self.current_debate,
            metrics=context["metrics"],
            stage=stage,
        )
        
        # Add to debate history
        self.current_debate.append(coordinator_message)
        
        # Determine which agents should participate in this stage
        participating_agents = self._select_agents_for_stage(stage)
        
        # Generate responses from participating agents
        tasks = []
        
        for role, agent in participating_agents.items():
            if role != coordinator_role:  # Skip coordinator as it already responded
                task = agent.generate_response(
                    prompt=f"Respond to the coordinator's message: {coordinator_message.content}",
                    debate_history=self.current_debate,
                    metrics=context["metrics"],
                    stage=stage,
                )
                tasks.append(task)
        
        # Wait for all responses
        agent_messages = await asyncio.gather(*tasks)
        
        # Add to debate history
        for message in agent_messages:
            self.current_debate.append(message)
        
        # Generate summary from coordinator
        summary_prompt = "Summarize the key points from this stage of the debate and identify next steps."
        
        summary_message = await coordinator.generate_response(
            prompt=summary_prompt,
            debate_history=self.current_debate,
            metrics=context["metrics"],
            stage=stage,
        )
        
        # Add to debate history
        self.current_debate.append(summary_message)
        
        logger.info(f"Completed debate stage: {stage.value}")
    
    def _select_agents_for_stage(self, stage: DebateStage) -> Dict[AgentRole, Agent]:
        """
        Select agents to participate in a debate stage.
        
        Args:
            stage: Debate stage
            
        Returns:
            Dictionary of selected agents
        """
        # Always include coordinator
        selected_agents = {
            AgentRole.COORDINATOR: self.agents.get(AgentRole.COORDINATOR)
        }
        
        # Remove None values (in case coordinator is not defined)
        selected_agents = {k: v for k, v in selected_agents.items() if v is not None}
        
        # Select other agents based on stage
        if stage == DebateStage.PROBLEM_DEFINITION:
            # Include all agents for problem definition
            selected_agents.update(self.agents)
        
        elif stage == DebateStage.ANALYSIS:
            # Include analysts and experts
            for role in [
                AgentRole.PERFORMANCE_ANALYST,
                AgentRole.MEMORY_OPTIMIZER,
                AgentRole.NUMERICAL_STABILITY_EXPERT,
                AgentRole.HARDWARE_ENGINEER,
                AgentRole.DATALOADER_SPECIALIST,
                AgentRole.TRAINING_DYNAMICS_EXPERT,
            ]:
                if role in self.agents:
                    selected_agents[role] = self.agents[role]
        
        elif stage == DebateStage.SOLUTION_GENERATION:
            # Include solution generators
            for role in [
                AgentRole.PERFORMANCE_ANALYST,
                AgentRole.MEMORY_OPTIMIZER,
                AgentRole.ARCHITECTURE_SPECIALIST,
                AgentRole.RESEARCH_SCIENTIST,
                AgentRole.HARDWARE_ENGINEER,
                AgentRole.DATALOADER_SPECIALIST,
                AgentRole.TRAINING_DYNAMICS_EXPERT,
            ]:
                if role in self.agents:
                    selected_agents[role] = self.agents[role]
        
        elif stage == DebateStage.CRITIQUE:
            # Include critics and devil's advocate
            for role in [
                AgentRole.DEVIL_ADVOCATE,
                AgentRole.NUMERICAL_STABILITY_EXPERT,
                AgentRole.RESEARCH_SCIENTIST,
            ]:
                if role in self.agents:
                    selected_agents[role] = self.agents[role]
        
        elif stage == DebateStage.REFINEMENT:
            # Include all agents for refinement
            selected_agents.update(self.agents)
        
        elif stage == DebateStage.CONSENSUS:
            # Include all agents for consensus
            selected_agents.update(self.agents)
        
        elif stage == DebateStage.RECOMMENDATION:
            # Include coordinator and key experts
            for role in [
                AgentRole.PERFORMANCE_ANALYST,
                AgentRole.MEMORY_OPTIMIZER,
                AgentRole.ARCHITECTURE_SPECIALIST,
                AgentRole.RESEARCH_SCIENTIST,
            ]:
                if role in self.agents:
                    selected_agents[role] = self.agents[role]
        
        return selected_agents
    
    def _extract_recommendations(self) -> List[Recommendation]:
        """
        Extract recommendations from the debate.
        
        Returns:
            List of recommendations
        """
        recommendations = []
        
        # Look for recommendation patterns in the messages
        for message in self.current_debate:
            if message.stage == DebateStage.RECOMMENDATION or message.stage == DebateStage.CONSENSUS:
                # Extract recommendations from the message content
                extracted = self._parse_recommendations_from_text(message.content, message.agent_role)
                recommendations.extend(extracted)
        
        # Deduplicate recommendations
        unique_recommendations = []
        seen_titles = set()
        
        for rec in recommendations:
            if rec.title not in seen_titles:
                seen_titles.add(rec.title)
                unique_recommendations.append(rec)
        
        # Sort by priority and votes
        priority_values = {
            RecommendationPriority.CRITICAL: 4,
            RecommendationPriority.HIGH: 3,
            RecommendationPriority.MEDIUM: 2,
            RecommendationPriority.LOW: 1,
            RecommendationPriority.EXPERIMENTAL: 0,
        }
        
        unique_recommendations.sort(
            key=lambda x: (priority_values.get(x.priority, 0), x.votes),
            reverse=True,
        )
        
        return unique_recommendations
    
    def _parse_recommendations_from_text(self, text: str, agent_role: AgentRole) -> List[Recommendation]:
        """
        Parse recommendations from text.
        
        Args:
            text: Text to parse
            agent_role: Role of the agent who generated the text
            
        Returns:
            List of parsed recommendations
        """
        recommendations = []
        
        # Look for recommendation patterns
        # Pattern 1: Recommendation: Title - Description
        pattern1 = r"Recommendation:?\s*([^-\n]+)-\s*(.*?)(?:\n\n|\Z)"
        matches1 = re.findall(pattern1, text, re.DOTALL)
        
        for match in matches1:
            title, description = match
            
            # Create recommendation
            rec = Recommendation(
                title=title.strip(),
                description=description.strip(),
                category=self._infer_category(title, description),
                priority=self._infer_priority(title, description),
                risk=self._infer_risk(title, description),
                implementation_steps=self._extract_steps(description),
                code_snippet=self._extract_code_snippet(description),
                references=self._extract_references_from_text(description),
                confidence=0.8,  # Default confidence
                votes=1,  # Single vote from this agent
                agent_roles=[agent_role],
            )
            
            recommendations.append(rec)
        
        # Pattern 2: 1. Title: Description
        pattern2 = r"(\d+)\.\s*([^:\n]+):\s*(.*?)(?:\n\n|\n\d+\.|\Z)"
        matches2 = re.findall(pattern2, text, re.DOTALL)
        
        for match in matches2:
            number, title, description = match
            
            # Create recommendation
            rec = Recommendation(
                title=title.strip(),
                description=description.strip(),
                category=self._infer_category(title, description),
                priority=self._infer_priority(title, description),
                risk=self._infer_risk(title, description),
                implementation_steps=self._extract_steps(description),
                code_snippet=self._extract_code_snippet(description),
                references=self._extract_references_from_text(description),
                confidence=0.7,  # Default confidence
                votes=1,  # Single vote from this agent
                agent_roles=[agent_role],
            )
            
            recommendations.append(rec)
        
        return recommendations
    
    def _infer_category(self, title: str, description: str) -> RecommendationCategory:
        """
        Infer recommendation category from title and description.
        
        Args:
            title: Recommendation title
            description: Recommendation description
            
        Returns:
            Inferred category
        """
        combined_text = (title + " " + description).lower()
        
        # Check for category keywords
        if any(kw in combined_text for kw in ["memory", "ram", "oom", "checkpoint", "offload"]):
            return RecommendationCategory.MEMORY_OPTIMIZATION
        
        elif any(kw in combined_text for kw in ["performance", "speed", "throughput", "latency", "faster"]):
            return RecommendationCategory.PERFORMANCE_OPTIMIZATION
        
        elif any(kw in combined_text for kw in ["stability", "nan", "inf", "overflow", "underflow", "precision"]):
            return RecommendationCategory.NUMERICAL_STABILITY
        
        elif any(kw in combined_text for kw in ["architecture", "layer", "model", "structure", "design"]):
            return RecommendationCategory.ARCHITECTURE_MODIFICATION
        
        elif any(kw in combined_text for kw in ["dataloader", "batch", "worker", "prefetch", "io", "disk"]):
            return RecommendationCategory.DATALOADER_OPTIMIZATION
        
        elif any(kw in combined_text for kw in ["training", "learning rate", "optimizer", "schedule", "epoch"]):
            return RecommendationCategory.TRAINING_STRATEGY
        
        elif any(kw in combined_text for kw in ["hardware", "gpu", "cpu", "tpu", "device", "cuda"]):
            return RecommendationCategory.HARDWARE_UTILIZATION
        
        elif any(kw in combined_text for kw in ["debug", "log", "print", "trace", "profile"]):
            return RecommendationCategory.DEBUGGING
        
        elif any(kw in combined_text for kw in ["research", "paper", "novel", "experiment", "study"]):
            return RecommendationCategory.RESEARCH_DIRECTION
        
        else:
            return RecommendationCategory.CUSTOM
    
    def _infer_priority(self, title: str, description: str) -> RecommendationPriority:
        """
        Infer recommendation priority from title and description.
        
        Args:
            title: Recommendation title
            description: Recommendation description
            
        Returns:
            Inferred priority
        """
        combined_text = (title + " " + description).lower()
        
        # Check for priority keywords
        if any(kw in combined_text for kw in ["critical", "urgent", "immediate", "severe", "crucial"]):
            return RecommendationPriority.CRITICAL
        
        elif any(kw in combined_text for kw in ["high", "important", "significant", "major"]):
            return RecommendationPriority.HIGH
        
        elif any(kw in combined_text for kw in ["medium", "moderate", "average"]):
            return RecommendationPriority.MEDIUM
        
        elif any(kw in combined_text for kw in ["low", "minor", "small", "slight"]):
            return RecommendationPriority.LOW
        
        elif any(kw in combined_text for kw in ["experimental", "research", "novel", "try"]):
            return RecommendationPriority.EXPERIMENTAL
        
        else:
            return RecommendationPriority.MEDIUM  # Default to medium priority
    
    def _infer_risk(self, title: str, description: str) -> RecommendationRisk:
        """
        Infer recommendation risk from title and description.
        
        Args:
            title: Recommendation title
            description: Recommendation description
            
        Returns:
            Inferred risk
        """
        combined_text = (title + " " + description).lower()
        
        # Check for risk keywords
        if any(kw in combined_text for kw in ["safe", "proven", "reliable", "stable", "guaranteed"]):
            return RecommendationRisk.SAFE
        
        elif any(kw in combined_text for kw in ["low risk", "minimal risk", "minor risk"]):
            return RecommendationRisk.LOW_RISK
        
        elif any(kw in combined_text for kw in ["medium risk", "moderate risk", "some risk"]):
            return RecommendationRisk.MEDIUM_RISK
        
        elif any(kw in combined_text for kw in ["high risk", "risky", "dangerous", "unstable"]):
            return RecommendationRisk.HIGH_RISK
        
        elif any(kw in combined_text for kw in ["experimental", "untested", "research", "novel"]):
            return RecommendationRisk.EXPERIMENTAL
        
        else:
            return RecommendationRisk.LOW_RISK  # Default to low risk
    
    def _extract_steps(self, text: str) -> List[str]:
        """
        Extract implementation steps from text.
        
        Args:
            text: Text to extract steps from
            
        Returns:
            List of implementation steps
        """
        steps = []
        
        # Look for numbered steps
        pattern1 = r"(\d+)\.\s*(.*?)(?:\n\d+\.|\n\n|\Z)"
        matches1 = re.findall(pattern1, text, re.DOTALL)
        
        if matches1:
            for match in matches1:
                number, step = match
                steps.append(step.strip())
            
            return steps
        
        # Look for bullet points
        pattern2 = r"[-*]\s*(.*?)(?:\n[-*]|\n\n|\Z)"
        matches2 = re.findall(pattern2, text, re.DOTALL)
        
        if matches2:
            for match in matches2:
                steps.append(match.strip())
            
            return steps
        
        # If no structured steps found, split by sentences and take up to 3
        sentences = re.split(r'(?<=[.!?])\s+', text)
        
        if sentences and len(sentences) > 1:
            return [s.strip() for s in sentences[:3] if len(s.strip()) > 10]
        
        # If all else fails, just return the text as a single step
        if text.strip():
            return [text.strip()]
        
        return steps
    
    def _extract_code_snippet(self, text: str) -> Optional[str]:
        """
        Extract code snippet from text.
        
        Args:
            text: Text to extract code from
            
        Returns:
            Extracted code snippet or None
        """
        # Look for code blocks
        pattern = r'```(?:python)?\s*(.*?)\s*```'
        matches = re.findall(pattern, text, re.DOTALL)
        
        if matches:
            return matches[0].strip()
        
        return None
    
    def _extract_references_from_text(self, text: str) -> List[Dict[str, str]]:
        """
        Extract references from text.
        
        Args:
            text: Text to extract references from
            
        Returns:
            List of references
        """
        references = []
        
        # Look for references in the format [1] Author, 'Title', Year
        reference_pattern = r'\[(\d+)\]\s+([^,]+),\s+[\'"]([^\'"]*)[\'"]\s*,\s*(\d{4})'
        matches = re.findall(reference_pattern, text)
        
        for match in matches:
            reference_number, author, title, year = match
            references.append({
                "number": reference_number,
                "author": author.strip(),
                "title": title.strip(),
                "year": year.strip(),
                "full_citation": f"[{reference_number}] {author}, '{title}', {year}",
            })
        
        return references
    
    def _update_metrics_history(self, metrics: Dict[str, Any]) -> None:
        """
        Update metrics history.
        
        Args:
            metrics: Current metrics
        """
        for key, value in metrics.items():
            self.metrics_history[key].append(value)
            
            # Limit history size
            if len(self.metrics_history[key]) > 100:
                self.metrics_history[key] = self.metrics_history[key][-100:]
    
    def _save_debate_history(self, result: DebateResult) -> None:
        """
        Save debate history to file.
        
        Args:
            result: Debate result
        """
        try:
            # Create filename
            timestamp = datetime.datetime.fromtimestamp(result.timestamp).strftime("%Y%m%d_%H%M%S")
            filename = f"debate_{timestamp}_{result.debate_id}.json"
            filepath = os.path.join(self.config.debate_history_dir, filename)
            
            # Convert to serializable format
            serializable_result = {
                "debate_id": result.debate_id,
                "timestamp": result.timestamp,
                "debate_duration": result.debate_duration,
                "consensus_reached": result.consensus_reached,
                "metrics_analyzed": result.metrics_analyzed,
                "debate_history": [
                    {
                        "agent_role": message.agent_role.value,
                        "content": message.content,
                        "stage": message.stage.value,
                        "timestamp": message.timestamp,
                        "references": message.references,
                        "code_snippets": message.code_snippets,
                    }
                    for message in result.debate_history
                ],
                "recommendations": [
                    {
                        "title": rec.title,
                        "description": rec.description,
                        "category": rec.category.value,
                        "priority": rec.priority.value,
                        "risk": rec.risk.value,
                        "implementation_steps": rec.implementation_steps,
                        "code_snippet": rec.code_snippet,
                        "references": rec.references,
                        "metrics_impact": rec.metrics_impact,
                        "confidence": rec.confidence,
                        "votes": rec.votes,
                        "agent_roles": [role.value for role in rec.agent_roles],
                    }
                    for rec in result.recommendations
                ],
            }
            
            # Save to file
            with open(filepath, "w") as f:
                json.dump(serializable_result, f, indent=2)
            
            logger.info(f"Saved debate history to {filepath}")
        
        except Exception as e:
            logger.error(f"Failed to save debate history: {e}")
            logger.error(traceback.format_exc())
    
    def load_debate_history(self, filepath: str) -> Optional[DebateResult]:
        """
        Load debate history from file.
        
        Args:
            filepath: Path to debate history file
            
        Returns:
            Loaded debate result or None
        """
        try:
            # Load from file
            with open(filepath, "r") as f:
                data = json.load(f)
            
            # Convert to DebateResult
            debate_history = [
                Message(
                    agent_role=AgentRole(msg["agent_role"]),
                    content=msg["content"],
                    stage=DebateStage(msg["stage"]),
                    timestamp=msg["timestamp"],
                    references=msg["references"],
                    code_snippets=msg["code_snippets"],
                    metrics={},  # Metrics not stored in serialized format
                )
                for msg in data["debate_history"]
            ]
            
            recommendations = [
                Recommendation(
                    title=rec["title"],
                    description=rec["description"],
                    category=RecommendationCategory(rec["category"]),
                    priority=RecommendationPriority(rec["priority"]),
                    risk=RecommendationRisk(rec["risk"]),
                    implementation_steps=rec["implementation_steps"],
                    code_snippet=rec["code_snippet"],
                    references=rec["references"],
                    metrics_impact=rec["metrics_impact"],
                    confidence=rec["confidence"],
                    votes=rec["votes"],
                    agent_roles=[AgentRole(role) for role in rec["agent_roles"]],
                )
                for rec in data["recommendations"]
            ]
            
            result = DebateResult(
                recommendations=recommendations,
                debate_history=debate_history,
                metrics_analyzed=data["metrics_analyzed"],
                consensus_reached=data["consensus_reached"],
                debate_duration=data["debate_duration"],
                timestamp=data["timestamp"],
                debate_id=data["debate_id"],
            )
            
            logger.info(f"Loaded debate history from {filepath}")
            
            return result
        
        except Exception as e:
            logger.error(f"Failed to load debate history: {e}")
            logger.error(traceback.format_exc())
            return None
    
    def get_recommendations(
        self,
        category: Optional[RecommendationCategory] = None,
        priority: Optional[RecommendationPriority] = None,
        max_count: Optional[int] = None,
    ) -> List[Recommendation]:
        """
        Get recommendations.
        
        Args:
            category: Filter by category
            priority: Filter by priority
            max_count: Maximum number of recommendations to return
            
        Returns:
            List of recommendations
        """
        filtered_recommendations = self.recommendations
        
        # Filter by category
        if category is not None:
            filtered_recommendations = [rec for rec in filtered_recommendations if rec.category == category]
        
        # Filter by priority
        if priority is not None:
            filtered_recommendations = [rec for rec in filtered_recommendations if rec.priority == priority]
        
        # Limit count
        if max_count is not None:
            filtered_recommendations = filtered_recommendations[:max_count]
        
        return filtered_recommendations
    
    def get_debate_history(self, max_count: Optional[int] = None) -> List[DebateResult]:
        """
        Get debate history.
        
        Args:
            max_count: Maximum number of debate results to return
            
        Returns:
            List of debate results
        """
        # Sort by timestamp (newest first)
        sorted_history = sorted(self.debate_history, key=lambda x: x.timestamp, reverse=True)
        
        # Limit count
        if max_count is not None:
            sorted_history = sorted_history[:max_count]
        
        return sorted_history
    
    def get_metrics_history(self, metric_name: str) -> List[Any]:
        """
        Get history of a metric.
        
        Args:
            metric_name: Name of the metric
            
        Returns:
            List of metric values
        """
        return list(self.metrics_history.get(metric_name, []))
    
    def visualize_debate(
        self,
        debate_result: DebateResult,
        output_path: Optional[str] = None,
    ) -> Optional[str]:
        """
        Visualize a debate.
        
        Args:
            debate_result: Debate result to visualize
            output_path: Path to save the visualization
            
        Returns:
            Path to the saved visualization or None
        """
        try:
            # Create figure
            plt.figure(figsize=(12, 8))
            
            # Count messages by agent and stage
            agent_counts = defaultdict(int)
            stage_counts = defaultdict(int)
            
            for message in debate_result.debate_history:
                agent_counts[message.agent_role.value] += 1
                stage_counts[message.stage.value] += 1
            
            # Create subplots
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
            
            # Plot agent participation
            agents = list(agent_counts.keys())
            counts = list(agent_counts.values())
            
            ax1.bar(agents, counts)
            ax1.set_title("Agent Participation")
            ax1.set_xlabel("Agent Role")
            ax1.set_ylabel("Number of Messages")
            ax1.set_xticklabels(agents, rotation=45, ha="right")
            
            # Plot stage distribution
            stages = list(stage_counts.keys())
            counts = list(stage_counts.values())
            
            ax2.bar(stages, counts)
            ax2.set_title("Debate Stages")
            ax2.set_xlabel("Stage")
            ax2.set_ylabel("Number of Messages")
            ax2.set_xticklabels(stages, rotation=45, ha="right")
            
            # Adjust layout
            plt.tight_layout()
            
            # Save or show plot
            if output_path:
                plt.savefig(output_path, bbox_inches="tight", dpi=300)
                logger.info(f"Saved debate visualization to {output_path}")
                plt.close(fig)
                return output_path
            else:
                plt.show()
                plt.close(fig)
                return None
        
        except Exception as e:
            logger.error(f"Failed to visualize debate: {e}")
            logger.error(traceback.format_exc())
            return None
    
    def visualize_recommendations(
        self,
        recommendations: List[Recommendation],
        output_path: Optional[str] = None,
    ) -> Optional[str]:
        """
        Visualize recommendations.
        
        Args:
            recommendations: Recommendations to visualize
            output_path: Path to save the visualization
            
        Returns:
            Path to the saved visualization or None
        """
        try:
            # Create figure
            plt.figure(figsize=(12, 8))
            
            # Count recommendations by category and priority
            category_counts = defaultdict(int)
            priority_counts = defaultdict(int)
            
            for rec in recommendations:
                category_counts[rec.category.value] += 1
                priority_counts[rec.priority.value] += 1
            
            # Create subplots
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
            
            # Plot category distribution
            categories = list(category_counts.keys())
            counts = list(category_counts.values())
            
            ax1.bar(categories, counts)
            ax1.set_title("Recommendation Categories")
            ax1.set_xlabel("Category")
            ax1.set_ylabel("Count")
            ax1.set_xticklabels(categories, rotation=45, ha="right")
            
            # Plot priority distribution
            priorities = list(priority_counts.keys())
            counts = list(priority_counts.values())
            
            # Sort priorities by severity
            priority_order = {
                RecommendationPriority.CRITICAL.value: 0,
                RecommendationPriority.HIGH.value: 1,
                RecommendationPriority.MEDIUM.value: 2,
                RecommendationPriority.LOW.value: 3,
                RecommendationPriority.EXPERIMENTAL.value: 4,
            }
            
            sorted_priorities = sorted(priorities, key=lambda x: priority_order.get(x, 999))
            sorted_counts = [priority_counts[p] for p in sorted_priorities]
            
            # Define colors for priorities
            colors = {
                RecommendationPriority.CRITICAL.value: "red",
                RecommendationPriority.HIGH.value: "orange",
                RecommendationPriority.MEDIUM.value: "yellow",
                RecommendationPriority.LOW.value: "blue",
                RecommendationPriority.EXPERIMENTAL.value: "purple",
            }
            
            bar_colors = [colors.get(p, "gray") for p in sorted_priorities]
            
            ax2.bar(sorted_priorities, sorted_counts, color=bar_colors)
            ax2.set_title("Recommendation Priorities")
            ax2.set_xlabel("Priority")
            ax2.set_ylabel("Count")
            
            # Adjust layout
            plt.tight_layout()
            
            # Save or show plot
            if output_path:
                plt.savefig(output_path, bbox_inches="tight", dpi=300)
                logger.info(f"Saved recommendations visualization to {output_path}")
                plt.close(fig)
                return output_path
            else:
                plt.show()
                plt.close(fig)
                return None
        
        except Exception as e:
            logger.error(f"Failed to visualize recommendations: {e}")
            logger.error(traceback.format_exc())
            return None
    
    def format_recommendations_markdown(self, recommendations: List[Recommendation]) -> str:
        """
        Format recommendations as markdown.
        
        Args:
            recommendations: Recommendations to format
            
        Returns:
            Markdown formatted recommendations
        """
        if not recommendations:
            return "No recommendations available."
        
        markdown = "# Optimization Recommendations\n\n"
        
        # Group by priority
        priority_groups = defaultdict(list)
        
        for rec in recommendations:
            priority_groups[rec.priority].append(rec)
        
        # Priority order
        priority_order = [
            RecommendationPriority.CRITICAL,
            RecommendationPriority.HIGH,
            RecommendationPriority.MEDIUM,
            RecommendationPriority.LOW,
            RecommendationPriority.EXPERIMENTAL,
        ]
        
        # Add recommendations by priority
        for priority in priority_order:
            if priority in priority_groups:
                markdown += f"## {priority.value.title()} Priority\n\n"
                
                for i, rec in enumerate(priority_groups[priority]):
                    markdown += f"### {i+1}. {rec.title}\n\n"
                    markdown += f"**Category:** {rec.category.value.replace('_', ' ').title()}  \n"
                    markdown += f"**Risk Level:** {rec.risk.value.replace('_', ' ').title()}  \n"
                    markdown += f"**Confidence:** {rec.confidence:.0%}  \n\n"
                    
                    markdown += f"{rec.description}\n\n"
                    
                    if rec.implementation_steps:
                        markdown += "#### Implementation Steps\n\n"
                        
                        for j, step in enumerate(rec.implementation_steps):
                            markdown += f"{j+1}. {step}\n"
                        
                        markdown += "\n"
                    
                    if rec.code_snippet:
                        markdown += "#### Code Example\n\n"
                        markdown += f"```python\n{rec.code_snippet}\n```\n\n"
                    
                    if rec.references:
                        markdown += "#### References\n\n"
                        
                        for ref in rec.references:
                            markdown += f"- {ref.get('full_citation', '')}\n"
                        
                        markdown += "\n"
                    
                    markdown += "---\n\n"
        
        return markdown
    
    def format_debate_markdown(self, debate_result: DebateResult) -> str:
        """
        Format debate as markdown.
        
        Args:
            debate_result: Debate result to format
            
        Returns:
            Markdown formatted debate
        """
        if not debate_result:
            return "No debate available."
        
        # Format timestamp
        timestamp = datetime.datetime.fromtimestamp(debate_result.timestamp).strftime("%Y-%m-%d %H:%M:%S")
        
        markdown = f"# Think Tank Debate - {timestamp}\n\n"
        markdown += f"**Debate ID:** {debate_result.debate_id}  \n"
        markdown += f"**Duration:** {debate_result.debate_duration:.2f} seconds  \n"
        markdown += f"**Consensus Reached:** {'Yes' if debate_result.consensus_reached else 'No'}  \n\n"
        
        # Add metrics
        markdown += "## Metrics Analyzed\n\n"
        markdown += "```\n"
        
        for key, value in debate_result.metrics_analyzed.items():
            if isinstance(value, (int, float)):
                markdown += f"{key}: {value}\n"
            elif isinstance(value, (list, tuple)) and len(value) > 0:
                if len(value) > 5:
                    # For long lists, show first 3 and last 2 elements
                    formatted_values = [str(v) for v in value[:3]] + ["..."] + [str(v) for v in value[-2:]]
                    markdown += f"{key}: [{', '.join(formatted_values)}]\n"
                else:
                    markdown += f"{key}: [{', '.join(str(v) for v in value)}]\n"
            else:
                markdown += f"{key}: {str(value)}\n"
        
        markdown += "```\n\n"
        
        # Add debate history
        markdown += "## Debate History\n\n"
        
        current_stage = None
        
        for message in debate_result.debate_history:
            # Add stage header if stage changed
            if message.stage != current_stage:
                current_stage = message.stage
                markdown += f"### Stage: {current_stage.value.replace('_', ' ').title()}\n\n"
            
            # Format timestamp
            msg_timestamp = datetime.datetime.fromtimestamp(message.timestamp).strftime("%H:%M:%S")
            
            # Add message
            markdown += f"#### {message.agent_role.value.replace('_', ' ').title()} ({msg_timestamp})\n\n"
            markdown += f"{message.content}\n\n"
            
            # Add references if any
            if message.references:
                markdown += "**References:**\n\n"
                
                for ref in message.references:
                    markdown += f"- {ref.get('full_citation', '')}\n"
                
                markdown += "\n"
            
            # Add code snippets if any
            if message.code_snippets:
                for snippet in message.code_snippets:
                    markdown += f"```{snippet.get('language', 'python')}\n{snippet.get('code', '')}\n```\n\n"
            
            markdown += "---\n\n"
        
        # Add recommendations
        markdown += "## Recommendations\n\n"
        markdown += self.format_recommendations_markdown(debate_result.recommendations)
        
        return markdown
    
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
                "max_debate_rounds": self.config.max_debate_rounds,
                "max_tokens_per_message": self.config.max_tokens_per_message,
                "debate_timeout": self.config.debate_timeout,
                "include_citations": self.config.include_citations,
                "include_code_examples": self.config.include_code_examples,
                "include_research_references": self.config.include_research_references,
                "save_debate_history": self.config.save_debate_history,
                "debate_history_dir": self.config.debate_history_dir,
                "custom_parameters": self.config.custom_parameters,
                "agents": [],
            }
            
            # Add agent configurations
            for agent_config in self.config.agents:
                agent_dict = {
                    "role": agent_config.role.value,
                    "system_prompt": agent_config.system_prompt,
                    "expertise_areas": agent_config.expertise_areas,
                    "citation_sources": agent_config.citation_sources,
                    "custom_parameters": agent_config.custom_parameters,
                    "llm_config": {
                        "provider": agent_config.llm_config.provider.value,
                        "model_name": agent_config.llm_config.model_name,
                        "api_base": agent_config.llm_config.api_base,
                        "api_version": agent_config.llm_config.api_version,
                        "max_tokens": agent_config.llm_config.max_tokens,
                        "temperature": agent_config.llm_config.temperature,
                        "top_p": agent_config.llm_config.top_p,
                        "frequency_penalty": agent_config.llm_config.frequency_penalty,
                        "presence_penalty": agent_config.llm_config.presence_penalty,
                        "timeout": agent_config.llm_config.timeout,
                        "custom_parameters": agent_config.llm_config.custom_parameters,
                    },
                }
                
                config["agents"].append(agent_dict)
            
            # Save to file
            with open(path, "w") as f:
                json.dump(config, f, indent=2)
            
            logger.info(f"Saved configuration to {path}")
            return True
        
        except Exception as e:
            logger.error(f"Failed to save configuration: {e}")
            logger.error(traceback.format_exc())
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
                config_dict = json.load(f)
            
            # Create agent configurations
            agents = []
            
            for agent_dict in config_dict.get("agents", []):
                # Create LLM config
                llm_dict = agent_dict.get("llm_config", {})
                
                llm_config = LLMConfig(
                    provider=LLMProvider(llm_dict.get("provider", LLMProvider.OPENAI.value)),
                    model_name=llm_dict.get("model_name", "gpt-4"),
                    api_key=llm_dict.get("api_key", ""),
                    api_base=llm_dict.get("api_base", ""),
                    api_version=llm_dict.get("api_version", ""),
                    max_tokens=llm_dict.get("max_tokens", 1000),
                    temperature=llm_dict.get("temperature", 0.7),
                    top_p=llm_dict.get("top_p", 1.0),
                    frequency_penalty=llm_dict.get("frequency_penalty", 0.0),
                    presence_penalty=llm_dict.get("presence_penalty", 0.0),
                    timeout=llm_dict.get("timeout", 60.0),
                    custom_parameters=llm_dict.get("custom_parameters", {}),
                )
                
                # Create agent config
                agent_config = AgentConfig(
                    role=AgentRole(agent_dict.get("role", AgentRole.COORDINATOR.value)),
                    llm_config=llm_config,
                    system_prompt=agent_dict.get("system_prompt", ""),
                    expertise_areas=agent_dict.get("expertise_areas", []),
                    citation_sources=agent_dict.get("citation_sources", []),
                    custom_parameters=agent_dict.get("custom_parameters", {}),
                )
                
                agents.append(agent_config)
            
            # Create think tank config
            self.config = ThinkTankConfig(
                agents=agents,
                max_debate_rounds=config_dict.get("max_debate_rounds", 5),
                max_tokens_per_message=config_dict.get("max_tokens_per_message", 1000),
                debate_timeout=config_dict.get("debate_timeout", 300.0),
                include_citations=config_dict.get("include_citations", True),
                include_code_examples=config_dict.get("include_code_examples", True),
                include_research_references=config_dict.get("include_research_references", True),
                save_debate_history=config_dict.get("save_debate_history", True),
                debate_history_dir=config_dict.get("debate_history_dir", "./debate_history"),
                custom_parameters=config_dict.get("custom_parameters", {}),
            )
            
            # Reinitialize agents
            self._initialize_agents()
            
            logger.info(f"Loaded configuration from {path}")
            return True
        
        except Exception as e:
            logger.error(f"Failed to load configuration: {e}")
            logger.error(traceback.format_exc())
            return False
    
    def clear_debate_history(self) -> None:
        """Clear debate history."""
        self.debate_history = []
        self.current_debate = []
        
        logger.info("Cleared debate history")
    
    def clear_recommendations(self) -> None:
        """Clear recommendations."""
        self.recommendations = []
        
        logger.info("Cleared recommendations")
    
    def clear_metrics_history(self) -> None:
        """Clear metrics history."""
        self.metrics_history.clear()
        
        logger.info("Cleared metrics history")
    
    def clear_all(self) -> None:
        """Clear all data."""
        self.clear_debate_history()
        self.clear_recommendations()
        self.clear_metrics_history()
        
        logger.info("Cleared all data")
    
    def get_status(self) -> Dict[str, Any]:
        """
        Get system status.
        
        Returns:
            System status
        """
        return {
            "debate_in_progress": self.debate_in_progress,
            "debate_history_count": len(self.debate_history),
            "recommendations_count": len(self.recommendations),
            "agents_count": len(self.agents),
            "metrics_count": len(self.metrics_history),
        }
