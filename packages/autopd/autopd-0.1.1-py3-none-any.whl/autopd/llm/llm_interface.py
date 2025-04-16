"""
LLM interface module for AutoPipelineDoctor.

This module provides a natural language interface for interacting with
AutoPipelineDoctor, allowing users to query and control the system using
natural language.
"""

import logging
import os
import json
import re
import time
from typing import Dict, Any, Optional, List, Tuple, Union, Callable
from datetime import datetime
import tempfile
from pathlib import Path
import textwrap
import threading
import queue

import torch
import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)


class LLMAssistant:
    """
    Natural language interface for AutoPipelineDoctor.
    
    This class provides a conversational interface for interacting with
    AutoPipelineDoctor, allowing users to query and control the system
    using natural language.
    
    Attributes:
        doctor: Reference to the Doctor instance
        model_provider: Provider for LLM capabilities (local or API-based)
        conversation_history: History of the conversation
        is_active: Whether the assistant is active
        max_history_length: Maximum number of conversation turns to keep
        default_system_prompt: Default system prompt for the LLM
    """
    
    def __init__(
        self,
        doctor: Optional[Any] = None,
        model_provider: str = "openai",
        api_key: Optional[str] = None,
        model_name: Optional[str] = None,
        max_history_length: int = 10,
        system_prompt: Optional[str] = None,
    ):
        """
        Initialize the LLM assistant.
        
        Args:
            doctor: Reference to the Doctor instance
            model_provider: Provider for LLM capabilities (openai, anthropic, huggingface, or local)
            api_key: API key for the model provider
            model_name: Name of the model to use
            max_history_length: Maximum number of conversation turns to keep
            system_prompt: System prompt for the LLM
        """
        self.doctor = doctor
        self.model_provider = model_provider
        self.api_key = api_key
        self.model_name = model_name
        self.max_history_length = max_history_length
        
        # Initialize conversation history
        self.conversation_history = []
        
        # Set default system prompt
        self.default_system_prompt = system_prompt or self._get_default_system_prompt()
        
        # Initialize LLM client
        self.llm_client = None
        self._initialize_llm_client()
        
        # Set active state
        self.is_active = False
        
        # Initialize command registry
        self.commands = self._initialize_commands()
        
        # Initialize response queue for async operations
        self.response_queue = queue.Queue()
        
        logger.info(f"LLM Assistant initialized with {model_provider} provider")
    
    def start(self):
        """Start the LLM assistant."""
        self.is_active = True
        logger.info("LLM Assistant started")
        return self
    
    def stop(self):
        """Stop the LLM assistant."""
        self.is_active = False
        logger.info("LLM Assistant stopped")
        return self
    
    def _initialize_llm_client(self):
        """Initialize the LLM client based on the provider."""
        try:
            if self.model_provider == "openai":
                self._initialize_openai_client()
            elif self.model_provider == "anthropic":
                self._initialize_anthropic_client()
            elif self.model_provider == "huggingface":
                self._initialize_huggingface_client()
            elif self.model_provider == "local":
                self._initialize_local_client()
            else:
                logger.warning(f"Unknown model provider: {self.model_provider}. Falling back to mock LLM.")
                self._initialize_mock_client()
        except Exception as e:
            logger.error(f"Failed to initialize LLM client: {e}")
            logger.warning("Falling back to mock LLM.")
            self._initialize_mock_client()
    
    def _initialize_openai_client(self):
        """Initialize the OpenAI client."""
        try:
            import openai
            
            # Set API key
            if self.api_key:
                openai.api_key = self.api_key
            elif os.environ.get("OPENAI_API_KEY"):
                openai.api_key = os.environ.get("OPENAI_API_KEY")
            else:
                raise ValueError("OpenAI API key not provided")
            
            # Set default model if not provided
            if not self.model_name:
                self.model_name = "gpt-4"
            
            self.llm_client = openai.OpenAI()
            logger.info(f"Initialized OpenAI client with model: {self.model_name}")
        except ImportError:
            logger.error("OpenAI package not installed. Install with: pip install openai")
            raise
        except Exception as e:
            logger.error(f"Failed to initialize OpenAI client: {e}")
            raise
    
    def _initialize_anthropic_client(self):
        """Initialize the Anthropic client."""
        try:
            import anthropic
            
            # Set API key
            if self.api_key:
                api_key = self.api_key
            elif os.environ.get("ANTHROPIC_API_KEY"):
                api_key = os.environ.get("ANTHROPIC_API_KEY")
            else:
                raise ValueError("Anthropic API key not provided")
            
            # Set default model if not provided
            if not self.model_name:
                self.model_name = "claude-3-opus-20240229"
            
            self.llm_client = anthropic.Anthropic(api_key=api_key)
            logger.info(f"Initialized Anthropic client with model: {self.model_name}")
        except ImportError:
            logger.error("Anthropic package not installed. Install with: pip install anthropic")
            raise
        except Exception as e:
            logger.error(f"Failed to initialize Anthropic client: {e}")
            raise
    
    def _initialize_huggingface_client(self):
        """Initialize the Hugging Face client."""
        try:
            from huggingface_hub import InferenceClient
            
            # Set API key
            if self.api_key:
                api_key = self.api_key
            elif os.environ.get("HF_API_KEY"):
                api_key = os.environ.get("HF_API_KEY")
            else:
                raise ValueError("Hugging Face API key not provided")
            
            # Set default model if not provided
            if not self.model_name:
                self.model_name = "mistralai/Mixtral-8x7B-Instruct-v0.1"
            
            self.llm_client = InferenceClient(token=api_key)
            logger.info(f"Initialized Hugging Face client with model: {self.model_name}")
        except ImportError:
            logger.error("Hugging Face Hub package not installed. Install with: pip install huggingface_hub")
            raise
        except Exception as e:
            logger.error(f"Failed to initialize Hugging Face client: {e}")
            raise
    
    def _initialize_local_client(self):
        """Initialize a local LLM client."""
        try:
            from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
            
            # Set default model if not provided
            if not self.model_name:
                self.model_name = "TheBloke/Llama-2-7B-Chat-GGUF"
            
            # Check if CUDA is available
            device = "cuda" if torch.cuda.is_available() else "cpu"
            
            # Load model and tokenizer
            tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            model = AutoModelForCausalLM.from_pretrained(
                self.model_name,
                device_map=device,
                torch_dtype=torch.float16 if device == "cuda" else torch.float32,
                low_cpu_mem_usage=True,
            )
            
            # Create pipeline
            self.llm_client = pipeline(
                "text-generation",
                model=model,
                tokenizer=tokenizer,
                max_length=2048,
                do_sample=True,
                temperature=0.7,
                top_p=0.95,
            )
            
            logger.info(f"Initialized local LLM client with model: {self.model_name}")
        except ImportError:
            logger.error("Transformers package not installed. Install with: pip install transformers")
            raise
        except Exception as e:
            logger.error(f"Failed to initialize local LLM client: {e}")
            raise
    
    def _initialize_mock_client(self):
        """Initialize a mock LLM client for testing."""
        self.model_provider = "mock"
        self.model_name = "mock-llm"
        self.llm_client = None
        logger.info("Initialized mock LLM client")
    
    def _get_default_system_prompt(self) -> str:
        """
        Get the default system prompt for the LLM.
        
        Returns:
            Default system prompt
        """
        return """
        You are AutoPipelineDoctor's AI Assistant, an expert in machine learning and deep learning training pipelines.
        Your role is to help users understand and optimize their ML/AI training processes.
        
        You have access to real-time metrics and analysis from AutoPipelineDoctor, which is monitoring the user's training pipeline.
        
        When responding to queries:
        1. Be concise but thorough in your explanations
        2. Provide specific, actionable advice based on the metrics you have access to
        3. Explain technical concepts in a way that's accessible but not oversimplified
        4. When suggesting optimizations, explain the reasoning and expected benefits
        5. If you don't have enough information, ask clarifying questions
        
        You can help with:
        - Explaining performance bottlenecks
        - Suggesting memory optimizations
        - Interpreting training metrics
        - Diagnosing issues like overfitting, underfitting, or gradient problems
        - Recommending hyperparameter adjustments
        - Explaining AutoPipelineDoctor's features and how to use them
        
        You have access to commands that can retrieve information or perform actions.
        Use these commands when needed to provide the most accurate and helpful responses.
        """
    
    def _initialize_commands(self) -> Dict[str, Callable]:
        """
        Initialize the command registry.
        
        Returns:
            Dictionary of command names to handler functions
        """
        return {
            "get_memory_metrics": self._handle_get_memory_metrics,
            "get_timing_metrics": self._handle_get_timing_metrics,
            "get_gradient_metrics": self._handle_get_gradient_metrics,
            "get_dataloader_metrics": self._handle_get_dataloader_metrics,
            "get_hardware_metrics": self._handle_get_hardware_metrics,
            "get_optimization_suggestions": self._handle_get_optimization_suggestions,
            "get_warnings": self._handle_get_warnings,
            "apply_optimization": self._handle_apply_optimization,
            "generate_report": self._handle_generate_report,
            "generate_dashboard": self._handle_generate_dashboard,
            "explain_metrics": self._handle_explain_metrics,
            "help": self._handle_help,
        }
    
    def ask(self, query: str) -> str:
        """
        Ask a question to the LLM assistant.
        
        Args:
            query: User query
        
        Returns:
            Assistant response
        """
        if not self.is_active:
            return "LLM Assistant is not active. Please start it first."
        
        try:
            # Add user query to conversation history
            self.conversation_history.append({"role": "user", "content": query})
            
            # Generate response
            response = self._generate_response(query)
            
            # Add assistant response to conversation history
            self.conversation_history.append({"role": "assistant", "content": response})
            
            # Trim conversation history if needed
            if len(self.conversation_history) > self.max_history_length * 2:
                # Keep the first message (system prompt) and the most recent messages
                self.conversation_history = self.conversation_history[:1] + self.conversation_history[-(self.max_history_length * 2):]
            
            return response
        
        except Exception as e:
            logger.error(f"Failed to generate response: {e}")
            return f"I encountered an error while processing your request: {str(e)}"
    
    def ask_async(self, query: str, callback: Optional[Callable[[str], None]] = None):
        """
        Ask a question to the LLM assistant asynchronously.
        
        Args:
            query: User query
            callback: Optional callback function to call with the response
        """
        if not self.is_active:
            if callback:
                callback("LLM Assistant is not active. Please start it first.")
            return
        
        def _async_ask():
            try:
                response = self.ask(query)
                if callback:
                    callback(response)
                else:
                    self.response_queue.put(response)
            except Exception as e:
                logger.error(f"Failed to generate async response: {e}")
                error_message = f"I encountered an error while processing your request: {str(e)}"
                if callback:
                    callback(error_message)
                else:
                    self.response_queue.put(error_message)
        
        # Start a new thread for the async request
        thread = threading.Thread(target=_async_ask)
        thread.daemon = True
        thread.start()
    
    def get_async_response(self, timeout: Optional[float] = None) -> Optional[str]:
        """
        Get the response from an asynchronous request.
        
        Args:
            timeout: Timeout in seconds
        
        Returns:
            Assistant response or None if timeout
        """
        try:
            return self.response_queue.get(timeout=timeout)
        except queue.Empty:
            return None
    
    def _generate_response(self, query: str) -> str:
        """
        Generate a response to the user query.
        
        Args:
            query: User query
        
        Returns:
            Assistant response
        """
        # Check for commands in the query
        command_match = re.search(r"/(\w+)(?:\s+(.+))?", query)
        if command_match:
            command = command_match.group(1)
            args = command_match.group(2) or ""
            
            # Handle command
            if command in self.commands:
                return self.commands[command](args)
            else:
                return f"Unknown command: /{command}. Type /help for a list of available commands."
        
        # Prepare messages for the LLM
        messages = self._prepare_messages_for_llm()
        
        # Generate response based on the provider
        if self.model_provider == "openai":
            return self._generate_openai_response(messages)
        elif self.model_provider == "anthropic":
            return self._generate_anthropic_response(messages)
        elif self.model_provider == "huggingface":
            return self._generate_huggingface_response(messages)
        elif self.model_provider == "local":
            return self._generate_local_response(messages)
        else:
            return self._generate_mock_response(query)
    
    def _prepare_messages_for_llm(self) -> List[Dict[str, str]]:
        """
        Prepare messages for the LLM.
        
        Returns:
            List of message dictionaries
        """
        # Start with system message
        messages = [{"role": "system", "content": self.default_system_prompt}]
        
        # Add conversation history
        messages.extend(self.conversation_history)
        
        # Add context about the current state if doctor is available
        if self.doctor:
            context = self._get_doctor_context()
            if context:
                messages.append({"role": "system", "content": f"Current context: {context}"})
        
        return messages
    
    def _get_doctor_context(self) -> str:
        """
        Get context about the current state of the Doctor.
        
        Returns:
            Context string
        """
        context_parts = []
        
        try:
            # Get memory metrics
            if hasattr(self.doctor, "memory_profiler") and self.doctor.memory_profiler:
                memory_metrics = self.doctor.memory_profiler.get_metrics()
                if memory_metrics:
                    context_parts.append("Memory metrics: " + json.dumps(memory_metrics))
            
            # Get timing metrics
            if hasattr(self.doctor, "timing_profiler") and self.doctor.timing_profiler:
                timing_metrics = self.doctor.timing_profiler.get_metrics()
                if timing_metrics:
                    context_parts.append("Timing metrics: " + json.dumps(timing_metrics))
            
            # Get warnings
            if hasattr(self.doctor, "failure_forecaster") and self.doctor.failure_forecaster:
                warnings = self.doctor.failure_forecaster.get_warnings()
                if warnings:
                    context_parts.append("Warnings: " + json.dumps(warnings))
            
            # Get optimization suggestions
            if hasattr(self.doctor, "optimization_advisor") and self.doctor.optimization_advisor:
                suggestions = self.doctor.optimization_advisor.get_suggestions()
                if suggestions:
                    context_parts.append("Optimization suggestions: " + json.dumps(suggestions))
        
        except Exception as e:
            logger.error(f"Failed to get doctor context: {e}")
        
        return "\n\n".join(context_parts)
    
    def _generate_openai_response(self, messages: List[Dict[str, str]]) -> str:
        """
        Generate a response using the OpenAI API.
        
        Args:
            messages: List of message dictionaries
        
        Returns:
            Assistant response
        """
        try:
            response = self.llm_client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                temperature=0.7,
                max_tokens=1024,
            )
            
            return response.choices[0].message.content
        
        except Exception as e:
            logger.error(f"Failed to generate OpenAI response: {e}")
            return f"I encountered an error while generating a response: {str(e)}"
    
    def _generate_anthropic_response(self, messages: List[Dict[str, str]]) -> str:
        """
        Generate a response using the Anthropic API.
        
        Args:
            messages: List of message dictionaries
        
        Returns:
            Assistant response
        """
        try:
            # Convert messages to Anthropic format
            system = next((m["content"] for m in messages if m["role"] == "system"), None)
            
            # Filter out system messages for the messages list
            user_assistant_messages = [m for m in messages if m["role"] != "system"]
            
            response = self.llm_client.messages.create(
                model=self.model_name,
                system=system,
                messages=user_assistant_messages,
                temperature=0.7,
                max_tokens=1024,
            )
            
            return response.content[0].text
        
        except Exception as e:
            logger.error(f"Failed to generate Anthropic response: {e}")
            return f"I encountered an error while generating a response: {str(e)}"
    
    def _generate_huggingface_response(self, messages: List[Dict[str, str]]) -> str:
        """
        Generate a response using the Hugging Face API.
        
        Args:
            messages: List of message dictionaries
        
        Returns:
            Assistant response
        """
        try:
            # Convert messages to a prompt format
            prompt = self._convert_messages_to_prompt(messages)
            
            response = self.llm_client.text_generation(
                prompt=prompt,
                model=self.model_name,
                max_new_tokens=1024,
                temperature=0.7,
                top_p=0.95,
            )
            
            # Extract the response from the generated text
            return self._extract_response_from_text(response, prompt)
        
        except Exception as e:
            logger.error(f"Failed to generate Hugging Face response: {e}")
            return f"I encountered an error while generating a response: {str(e)}"
    
    def _generate_local_response(self, messages: List[Dict[str, str]]) -> str:
        """
        Generate a response using a local LLM.
        
        Args:
            messages: List of message dictionaries
        
        Returns:
            Assistant response
        """
        try:
            # Convert messages to a prompt format
            prompt = self._convert_messages_to_prompt(messages)
            
            response = self.llm_client(
                prompt,
                max_length=len(prompt) + 1024,
                do_sample=True,
                temperature=0.7,
                top_p=0.95,
            )[0]["generated_text"]
            
            # Extract the response from the generated text
            return self._extract_response_from_text(response, prompt)
        
        except Exception as e:
            logger.error(f"Failed to generate local response: {e}")
            return f"I encountered an error while generating a response: {str(e)}"
    
    def _generate_mock_response(self, query: str) -> str:
        """
        Generate a mock response for testing.
        
        Args:
            query: User query
        
        Returns:
            Mock response
        """
        # Simple keyword-based responses
        if "memory" in query.lower():
            return "Based on the memory metrics, your model is using resources efficiently. The current memory usage is within normal parameters."
        
        elif "performance" in query.lower() or "slow" in query.lower():
            return "I've analyzed the performance metrics and found that the dataloader might be a bottleneck. Consider increasing the number of workers or using faster storage."
        
        elif "error" in query.lower() or "issue" in query.lower():
            return "I've detected potential issues in your training pipeline. There might be a risk of overfitting based on the validation loss trends. Consider adding regularization or early stopping."
        
        elif "optimize" in query.lower() or "improve" in query.lower():
            return "To optimize your training pipeline, I recommend:\n1. Using mixed precision training (AMP)\n2. Increasing the batch size\n3. Using a more efficient optimizer like AdamW\n4. Implementing gradient checkpointing for large models"
        
        elif "explain" in query.lower() or "what is" in query.lower() or "how does" in query.lower():
            return "AutoPipelineDoctor is monitoring your training pipeline in real-time, collecting metrics on memory usage, computation time, gradient behavior, and more. This allows me to provide insights and recommendations to improve your training process."
        
        else:
            return "I'm here to help you optimize your ML/AI training pipeline. I can provide insights on performance, memory usage, and suggest optimizations. What specific aspect would you like to know more about?"
    
    def _convert_messages_to_prompt(self, messages: List[Dict[str, str]]) -> str:
        """
        Convert messages to a prompt format for text generation models.
        
        Args:
            messages: List of message dictionaries
        
        Returns:
            Formatted prompt
        """
        prompt = ""
        
        # Add system message
        system_messages = [m for m in messages if m["role"] == "system"]
        if system_messages:
            prompt += "System: " + "\n".join([m["content"] for m in system_messages]) + "\n\n"
        
        # Add conversation history
        for message in [m for m in messages if m["role"] != "system"]:
            if message["role"] == "user":
                prompt += f"User: {message['content']}\n"
            elif message["role"] == "assistant":
                prompt += f"Assistant: {message['content']}\n"
        
        # Add final prompt for the assistant
        prompt += "Assistant: "
        
        return prompt
    
    def _extract_response_from_text(self, text: str, prompt: str) -> str:
        """
        Extract the assistant's response from the generated text.
        
        Args:
            text: Generated text
            prompt: Original prompt
        
        Returns:
            Extracted response
        """
        # Remove the prompt from the beginning
        if text.startswith(prompt):
            response = text[len(prompt):]
        else:
            response = text
        
        # Extract until the next "User:" or end of text
        if "User:" in response:
            response = response.split("User:")[0].strip()
        
        return response.strip()
    
    def _handle_get_memory_metrics(self, args: str) -> str:
        """
        Handle the get_memory_metrics command.
        
        Args:
            args: Command arguments
        
        Returns:
            Command response
        """
        if not self.doctor or not hasattr(self.doctor, "memory_profiler") or not self.doctor.memory_profiler:
            return "Memory profiler is not available."
        
        try:
            metrics = self.doctor.memory_profiler.get_metrics()
            return f"Memory Metrics:\n```json\n{json.dumps(metrics, indent=2)}\n```"
        
        except Exception as e:
            logger.error(f"Failed to get memory metrics: {e}")
            return f"Failed to get memory metrics: {str(e)}"
    
    def _handle_get_timing_metrics(self, args: str) -> str:
        """
        Handle the get_timing_metrics command.
        
        Args:
            args: Command arguments
        
        Returns:
            Command response
        """
        if not self.doctor or not hasattr(self.doctor, "timing_profiler") or not self.doctor.timing_profiler:
            return "Timing profiler is not available."
        
        try:
            metrics = self.doctor.timing_profiler.get_metrics()
            return f"Timing Metrics:\n```json\n{json.dumps(metrics, indent=2)}\n```"
        
        except Exception as e:
            logger.error(f"Failed to get timing metrics: {e}")
            return f"Failed to get timing metrics: {str(e)}"
    
    def _handle_get_gradient_metrics(self, args: str) -> str:
        """
        Handle the get_gradient_metrics command.
        
        Args:
            args: Command arguments
        
        Returns:
            Command response
        """
        if not self.doctor or not hasattr(self.doctor, "gradient_profiler") or not self.doctor.gradient_profiler:
            return "Gradient profiler is not available."
        
        try:
            metrics = self.doctor.gradient_profiler.get_metrics()
            return f"Gradient Metrics:\n```json\n{json.dumps(metrics, indent=2)}\n```"
        
        except Exception as e:
            logger.error(f"Failed to get gradient metrics: {e}")
            return f"Failed to get gradient metrics: {str(e)}"
    
    def _handle_get_dataloader_metrics(self, args: str) -> str:
        """
        Handle the get_dataloader_metrics command.
        
        Args:
            args: Command arguments
        
        Returns:
            Command response
        """
        if not self.doctor or not hasattr(self.doctor, "dataloader_profiler") or not self.doctor.dataloader_profiler:
            return "Dataloader profiler is not available."
        
        try:
            metrics = self.doctor.dataloader_profiler.get_metrics()
            return f"Dataloader Metrics:\n```json\n{json.dumps(metrics, indent=2)}\n```"
        
        except Exception as e:
            logger.error(f"Failed to get dataloader metrics: {e}")
            return f"Failed to get dataloader metrics: {str(e)}"
    
    def _handle_get_hardware_metrics(self, args: str) -> str:
        """
        Handle the get_hardware_metrics command.
        
        Args:
            args: Command arguments
        
        Returns:
            Command response
        """
        if not self.doctor or not hasattr(self.doctor, "hardware_profiler") or not self.doctor.hardware_profiler:
            return "Hardware profiler is not available."
        
        try:
            metrics = self.doctor.hardware_profiler.get_metrics()
            return f"Hardware Metrics:\n```json\n{json.dumps(metrics, indent=2)}\n```"
        
        except Exception as e:
            logger.error(f"Failed to get hardware metrics: {e}")
            return f"Failed to get hardware metrics: {str(e)}"
    
    def _handle_get_optimization_suggestions(self, args: str) -> str:
        """
        Handle the get_optimization_suggestions command.
        
        Args:
            args: Command arguments
        
        Returns:
            Command response
        """
        if not self.doctor or not hasattr(self.doctor, "optimization_advisor") or not self.doctor.optimization_advisor:
            return "Optimization advisor is not available."
        
        try:
            suggestions = self.doctor.optimization_advisor.get_suggestions()
            
            if not suggestions:
                return "No optimization suggestions available at this time."
            
            response = "Optimization Suggestions:\n\n"
            
            for i, suggestion in enumerate(suggestions, 1):
                response += f"{i}. **{suggestion.get('message', 'Unknown suggestion')}**\n"
                response += f"   - Type: {suggestion.get('type', 'unknown')}\n"
                response += f"   - Priority: {suggestion.get('priority', 0)}\n"
                response += f"   - Risk Level: {suggestion.get('risk_level', 'unknown')}\n"
                
                if "details" in suggestion:
                    response += f"   - Details: {suggestion['details']}\n"
                
                if "code" in suggestion:
                    response += f"   - Implementation:\n```python\n{suggestion['code']}\n```\n"
                
                response += "\n"
            
            return response
        
        except Exception as e:
            logger.error(f"Failed to get optimization suggestions: {e}")
            return f"Failed to get optimization suggestions: {str(e)}"
    
    def _handle_get_warnings(self, args: str) -> str:
        """
        Handle the get_warnings command.
        
        Args:
            args: Command arguments
        
        Returns:
            Command response
        """
        if not self.doctor or not hasattr(self.doctor, "failure_forecaster") or not self.doctor.failure_forecaster:
            return "Failure forecaster is not available."
        
        try:
            warnings = self.doctor.failure_forecaster.get_warnings()
            
            if not warnings:
                return "No warnings available at this time."
            
            response = "Warnings:\n\n"
            
            for i, warning in enumerate(warnings, 1):
                severity = warning.get("severity", "medium")
                
                if severity == "critical":
                    prefix = "🚨 CRITICAL"
                elif severity == "high":
                    prefix = "⚠️ HIGH"
                elif severity == "medium":
                    prefix = "⚠️ MEDIUM"
                else:
                    prefix = "ℹ️ LOW"
                
                response += f"{i}. **{prefix}: {warning.get('message', 'Unknown warning')}**\n"
                response += f"   - Type: {warning.get('type', 'unknown')}\n"
                
                if "details" in warning:
                    response += f"   - Details: {warning['details']}\n"
                
                if "suggestions" in warning and warning["suggestions"]:
                    response += "   - Suggestions:\n"
                    for j, suggestion in enumerate(warning["suggestions"], 1):
                        response += f"     {j}. {suggestion}\n"
                
                response += "\n"
            
            return response
        
        except Exception as e:
            logger.error(f"Failed to get warnings: {e}")
            return f"Failed to get warnings: {str(e)}"
    
    def _handle_apply_optimization(self, args: str) -> str:
        """
        Handle the apply_optimization command.
        
        Args:
            args: Command arguments
        
        Returns:
            Command response
        """
        if not self.doctor or not hasattr(self.doctor, "optimization_advisor") or not self.doctor.optimization_advisor:
            return "Optimization advisor is not available."
        
        if not args:
            return "Please specify an optimization type to apply. Use /get_optimization_suggestions to see available optimizations."
        
        try:
            # Parse optimization type from args
            opt_type = args.strip()
            
            # Get suggestions
            suggestions = self.doctor.optimization_advisor.get_suggestions()
            
            # Find matching suggestion
            matching_suggestions = [s for s in suggestions if s.get("type") == opt_type]
            
            if not matching_suggestions:
                return f"No optimization of type '{opt_type}' is available. Use /get_optimization_suggestions to see available optimizations."
            
            # Apply the optimization
            result = self.doctor.optimization_advisor.auto_optimize(
                categories=None,
                max_optimizations=1,
            )
            
            if not result:
                return f"Failed to apply optimization '{opt_type}'."
            
            applied = [r for r in result if r.get("type") == opt_type]
            
            if not applied:
                return f"Optimization '{opt_type}' was not applied. It may have failed or been skipped."
            
            return f"Successfully applied optimization '{opt_type}'."
        
        except Exception as e:
            logger.error(f"Failed to apply optimization: {e}")
            return f"Failed to apply optimization: {str(e)}"
    
    def _handle_generate_report(self, args: str) -> str:
        """
        Handle the generate_report command.
        
        Args:
            args: Command arguments
        
        Returns:
            Command response
        """
        if not self.doctor or not hasattr(self.doctor, "report_generator") or not self.doctor.report_generator:
            return "Report generator is not available."
        
        try:
            # Parse arguments
            include_plots = "no-plots" not in args.lower()
            include_dashboard = "no-dashboard" not in args.lower()
            
            # Generate report
            report_path = self.doctor.report_generator.generate_report(
                include_plots=include_plots,
                include_dashboard=include_dashboard,
            )
            
            if not report_path:
                return "Failed to generate report."
            
            return f"Report generated successfully at: {report_path}"
        
        except Exception as e:
            logger.error(f"Failed to generate report: {e}")
            return f"Failed to generate report: {str(e)}"
    
    def _handle_generate_dashboard(self, args: str) -> str:
        """
        Handle the generate_dashboard command.
        
        Args:
            args: Command arguments
        
        Returns:
            Command response
        """
        if not self.doctor or not hasattr(self.doctor, "visualizer") or not self.doctor.visualizer:
            return "Visualizer is not available."
        
        try:
            # Generate dashboard
            dashboard_path = self.doctor.visualizer.generate_dashboard()
            
            if not dashboard_path:
                return "Failed to generate dashboard."
            
            return f"Dashboard generated successfully at: {dashboard_path}"
        
        except Exception as e:
            logger.error(f"Failed to generate dashboard: {e}")
            return f"Failed to generate dashboard: {str(e)}"
    
    def _handle_explain_metrics(self, args: str) -> str:
        """
        Handle the explain_metrics command.
        
        Args:
            args: Command arguments
        
        Returns:
            Command response
        """
        if not self.doctor or not hasattr(self.doctor, "explainer") or not self.doctor.explainer:
            return "Natural language explainer is not available."
        
        if not args:
            return "Please specify a category of metrics to explain (memory, timing, gradient, dataloader, hardware)."
        
        try:
            # Parse category from args
            category = args.strip().lower()
            
            # Get metrics for the category
            metrics = None
            
            if category == "memory" and hasattr(self.doctor, "memory_profiler"):
                metrics = self.doctor.memory_profiler.get_metrics()
            elif category == "timing" and hasattr(self.doctor, "timing_profiler"):
                metrics = self.doctor.timing_profiler.get_metrics()
            elif category == "gradient" and hasattr(self.doctor, "gradient_profiler"):
                metrics = self.doctor.gradient_profiler.get_metrics()
            elif category == "dataloader" and hasattr(self.doctor, "dataloader_profiler"):
                metrics = self.doctor.dataloader_profiler.get_metrics()
            elif category == "hardware" and hasattr(self.doctor, "hardware_profiler"):
                metrics = self.doctor.hardware_profiler.get_metrics()
            
            if not metrics:
                return f"No metrics available for category '{category}'."
            
            # Generate explanation
            explanation = self.doctor.explainer.explain_metrics(metrics, category)
            
            if not explanation:
                return f"Failed to generate explanation for '{category}' metrics."
            
            return f"Explanation of {category} metrics:\n\n{explanation}"
        
        except Exception as e:
            logger.error(f"Failed to explain metrics: {e}")
            return f"Failed to explain metrics: {str(e)}"
    
    def _handle_help(self, args: str) -> str:
        """
        Handle the help command.
        
        Args:
            args: Command arguments
        
        Returns:
            Command response
        """
        help_text = """
        Available commands:
        
        /get_memory_metrics - Get memory usage metrics
        /get_timing_metrics - Get timing performance metrics
        /get_gradient_metrics - Get gradient statistics
        /get_dataloader_metrics - Get dataloader performance metrics
        /get_hardware_metrics - Get hardware utilization metrics
        /get_optimization_suggestions - Get optimization suggestions
        /get_warnings - Get warnings and issues
        /apply_optimization <type> - Apply a specific optimization
        /generate_report [no-plots] [no-dashboard] - Generate a comprehensive report
        /generate_dashboard - Generate an interactive dashboard
        /explain_metrics <category> - Get natural language explanation of metrics
        /help - Show this help message
        
        You can also ask questions in natural language about your training pipeline.
        """
        
        return textwrap.dedent(help_text).strip()
    
    def __repr__(self) -> str:
        """String representation of the LLM assistant."""
        status = "active" if self.is_active else "inactive"
        return f"LLMAssistant(provider={self.model_provider}, model={self.model_name}, status={status})"


class LLMInterface:
    """
    Interface for interacting with AutoPipelineDoctor using natural language.
    
    This class provides a high-level interface for interacting with
    AutoPipelineDoctor using natural language, including a command-line
    interface and a web interface.
    
    Attributes:
        assistant: LLM assistant for natural language interaction
        doctor: Reference to the Doctor instance
        is_active: Whether the interface is active
    """
    
    def __init__(
        self,
        doctor: Optional[Any] = None,
        model_provider: str = "openai",
        api_key: Optional[str] = None,
        model_name: Optional[str] = None,
    ):
        """
        Initialize the LLM interface.
        
        Args:
            doctor: Reference to the Doctor instance
            model_provider: Provider for LLM capabilities (openai, anthropic, huggingface, or local)
            api_key: API key for the model provider
            model_name: Name of the model to use
        """
        self.doctor = doctor
        self.assistant = LLMAssistant(
            doctor=doctor,
            model_provider=model_provider,
            api_key=api_key,
            model_name=model_name,
        )
        self.is_active = False
        
        logger.info("LLM Interface initialized")
    
    def start(self):
        """Start the LLM interface."""
        self.is_active = True
        self.assistant.start()
        logger.info("LLM Interface started")
        return self
    
    def stop(self):
        """Stop the LLM interface."""
        self.is_active = False
        self.assistant.stop()
        logger.info("LLM Interface stopped")
        return self
    
    def ask(self, query: str) -> str:
        """
        Ask a question to the LLM interface.
        
        Args:
            query: User query
        
        Returns:
            Assistant response
        """
        if not self.is_active:
            return "LLM Interface is not active. Please start it first."
        
        return self.assistant.ask(query)
    
    def start_cli(self):
        """Start a command-line interface for interacting with the LLM assistant."""
        if not self.is_active:
            print("LLM Interface is not active. Starting...")
            self.start()
        
        print("Welcome to AutoPipelineDoctor's LLM Interface!")
        print("Type 'exit' or 'quit' to exit.")
        print("Type '/help' for a list of available commands.")
        
        while True:
            try:
                query = input("\nYou: ")
                
                if query.lower() in ["exit", "quit"]:
                    break
                
                response = self.ask(query)
                print(f"\nAssistant: {response}")
            
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"Error: {str(e)}")
        
        print("Goodbye!")
    
    def start_web_interface(self, host: str = "0.0.0.0", port: int = 8080):
        """
        Start a web interface for interacting with the LLM assistant.
        
        Args:
            host: Host to bind to
            port: Port to bind to
        """
        if not self.is_active:
            logger.info("LLM Interface is not active. Starting...")
            self.start()
        
        try:
            import flask
            from flask import Flask, request, jsonify, render_template
            
            app = Flask(__name__)
            
            # Create a simple HTML template
            html_template = """
            <!DOCTYPE html>
            <html>
            <head>
                <title>AutoPipelineDoctor LLM Interface</title>
                <style>
                    body {
                        font-family: Arial, sans-serif;
                        max-width: 800px;
                        margin: 0 auto;
                        padding: 20px;
                    }
                    .chat-container {
                        border: 1px solid #ccc;
                        border-radius: 5px;
                        padding: 10px;
                        height: 400px;
                        overflow-y: auto;
                        margin-bottom: 10px;
                    }
                    .message {
                        margin-bottom: 10px;
                        padding: 8px;
                        border-radius: 5px;
                    }
                    .user {
                        background-color: #e6f7ff;
                        text-align: right;
                    }
                    .assistant {
                        background-color: #f2f2f2;
                    }
                    .input-container {
                        display: flex;
                    }
                    #user-input {
                        flex-grow: 1;
                        padding: 8px;
                        border: 1px solid #ccc;
                        border-radius: 5px;
                    }
                    button {
                        padding: 8px 16px;
                        background-color: #4CAF50;
                        color: white;
                        border: none;
                        border-radius: 5px;
                        margin-left: 10px;
                        cursor: pointer;
                    }
                    pre {
                        white-space: pre-wrap;
                        word-wrap: break-word;
                    }
                </style>
            </head>
            <body>
                <h1>AutoPipelineDoctor LLM Interface</h1>
                <div class="chat-container" id="chat-container"></div>
                <div class="input-container">
                    <input type="text" id="user-input" placeholder="Ask a question...">
                    <button onclick="sendMessage()">Send</button>
                </div>
                
                <script>
                    function addMessage(content, isUser) {
                        const chatContainer = document.getElementById('chat-container');
                        const messageDiv = document.createElement('div');
                        messageDiv.className = `message ${isUser ? 'user' : 'assistant'}`;
                        
                        // Check if content contains code blocks
                        if (!isUser && content.includes('```')) {
                            let formattedContent = '';
                            let inCodeBlock = false;
                            let codeContent = '';
                            
                            content.split('\\n').forEach(line => {
                                if (line.startsWith('```')) {
                                    if (inCodeBlock) {
                                        formattedContent += `<pre>${codeContent}</pre>`;
                                        codeContent = '';
                                    } else {
                                        codeContent = '';
                                    }
                                    inCodeBlock = !inCodeBlock;
                                } else if (inCodeBlock) {
                                    codeContent += line + '\\n';
                                } else {
                                    formattedContent += line + '<br>';
                                }
                            });
                            
                            if (codeContent) {
                                formattedContent += `<pre>${codeContent}</pre>`;
                            }
                            
                            messageDiv.innerHTML = formattedContent;
                        } else {
                            messageDiv.textContent = content;
                        }
                        
                        chatContainer.appendChild(messageDiv);
                        chatContainer.scrollTop = chatContainer.scrollHeight;
                    }
                    
                    function sendMessage() {
                        const userInput = document.getElementById('user-input');
                        const message = userInput.value.trim();
                        
                        if (message) {
                            addMessage(message, true);
                            userInput.value = '';
                            
                            fetch('/ask', {
                                method: 'POST',
                                headers: {
                                    'Content-Type': 'application/json',
                                },
                                body: JSON.stringify({ query: message }),
                            })
                            .then(response => response.json())
                            .then(data => {
                                addMessage(data.response, false);
                            })
                            .catch(error => {
                                console.error('Error:', error);
                                addMessage('Error: ' + error.message, false);
                            });
                        }
                    }
                    
                    // Allow pressing Enter to send message
                    document.getElementById('user-input').addEventListener('keypress', function(e) {
                        if (e.key === 'Enter') {
                            sendMessage();
                        }
                    });
                    
                    // Add welcome message
                    addMessage("Welcome to AutoPipelineDoctor's LLM Interface! How can I help you optimize your ML/AI training pipeline?", false);
                </script>
            </body>
            </html>
            """
            
            @app.route('/')
            def home():
                return html_template
            
            @app.route('/ask', methods=['POST'])
            def ask_endpoint():
                data = request.json
                query = data.get('query', '')
                
                if not query:
                    return jsonify({'response': 'Please provide a query.'})
                
                try:
                    response = self.ask(query)
                    return jsonify({'response': response})
                except Exception as e:
                    logger.error(f"Error in ask endpoint: {e}")
                    return jsonify({'response': f"Error: {str(e)}"})
            
            logger.info(f"Starting web interface on http://{host}:{port}")
            app.run(host=host, port=port)
        
        except ImportError:
            logger.error("Flask is required for the web interface. Install with: pip install flask")
            print("Flask is required for the web interface. Install with: pip install flask")
        except Exception as e:
            logger.error(f"Failed to start web interface: {e}")
            print(f"Failed to start web interface: {e}")
    
    def __repr__(self) -> str:
        """String representation of the LLM interface."""
        status = "active" if self.is_active else "inactive"
        return f"LLMInterface(status={status})"
