"""
LLM interface module for AutoPipelineDoctor.
"""

from typing import Dict, List, Optional, Any, Union, Callable
import logging
import os
import json
import time
import threading
import queue
import re

logger = logging.getLogger(__name__)

class LLMAssistant:
    """
    Natural language interface for AutoPipelineDoctor.
    
    This class provides a natural language interface for interacting with
    AutoPipelineDoctor, allowing users to ask questions about their training
    process and receive detailed explanations and recommendations.
    """
    
    def __init__(self, api_key: Optional[str] = None, provider: str = 'openai', 
                model: str = 'gpt-4', temperature: float = 0.2):
        """
        Initialize the LLM assistant.
        
        Args:
            api_key: API key for the LLM provider (optional, uses env var if not provided)
            provider: LLM provider ('openai', 'anthropic', 'huggingface', 'local')
            model: Model name to use
            temperature: Temperature for generation (0.0-1.0)
        """
        self.provider = provider
        self.model = model
        self.temperature = temperature
        
        # Set API key
        if api_key:
            self.api_key = api_key
        else:
            # Try to get from environment variables
            if provider == 'openai':
                self.api_key = os.environ.get('OPENAI_API_KEY')
            elif provider == 'anthropic':
                self.api_key = os.environ.get('ANTHROPIC_API_KEY')
            elif provider == 'huggingface':
                self.api_key = os.environ.get('HUGGINGFACE_API_KEY')
            else:
                self.api_key = None
        
        # Initialize client
        self.client = None
        self._initialize_client()
        
        # Conversation history
        self.conversation_history = []
        
        # System prompt template
        self.system_prompt = """
        You are an AI assistant specialized in analyzing and explaining machine learning training processes.
        You have access to detailed metrics and insights from AutoPipelineDoctor, a tool that monitors ML/AI training pipelines.
        
        When responding to questions:
        1. Be concise but thorough
        2. Explain technical concepts clearly
        3. Provide specific, actionable recommendations when appropriate
        4. Reference specific metrics and data points to support your explanations
        5. Use markdown formatting for better readability
        
        The following metrics and analysis are available to you:
        {metrics_summary}
        """
        
        # Response queue for async processing
        self.response_queue = queue.Queue()
    
    def _initialize_client(self):
        """Initialize the LLM client based on the provider."""
        try:
            if self.provider == 'openai':
                try:
                    import openai
                    if self.api_key:
                        openai.api_key = self.api_key
                    self.client = openai.OpenAI()
                    logger.info(f"Initialized OpenAI client with model {self.model}")
                except ImportError:
                    logger.error("OpenAI package not installed. Run 'pip install openai'")
                    self.client = None
            
            elif self.provider == 'anthropic':
                try:
                    import anthropic
                    if self.api_key:
                        self.client = anthropic.Anthropic(api_key=self.api_key)
                    else:
                        self.client = anthropic.Anthropic()
                    logger.info(f"Initialized Anthropic client with model {self.model}")
                except ImportError:
                    logger.error("Anthropic package not installed. Run 'pip install anthropic'")
                    self.client = None
            
            elif self.provider == 'huggingface':
                try:
                    from huggingface_hub import InferenceClient
                    if self.api_key:
                        self.client = InferenceClient(token=self.api_key)
                    else:
                        self.client = InferenceClient()
                    logger.info(f"Initialized HuggingFace client with model {self.model}")
                except ImportError:
                    logger.error("HuggingFace Hub package not installed. Run 'pip install huggingface_hub'")
                    self.client = None
            
            elif self.provider == 'local':
                try:
                    from transformers import pipeline
                    self.client = pipeline("text-generation", model=self.model)
                    logger.info(f"Initialized local model {self.model}")
                except ImportError:
                    logger.error("Transformers package not installed. Run 'pip install transformers'")
                    self.client = None
            
            else:
                logger.error(f"Unknown provider: {self.provider}")
                self.client = None
        
        except Exception as e:
            logger.error(f"Error initializing LLM client: {e}")
            self.client = None
    
    def _prepare_metrics_summary(self, metrics: Dict[str, List[Dict[str, Any]]], 
                               bottlenecks: List[Dict[str, Any]], 
                               recommendations: List[Dict[str, Any]]) -> str:
        """
        Prepare a summary of metrics for the system prompt.
        
        Args:
            metrics: Dictionary of metrics
            bottlenecks: List of detected bottlenecks
            recommendations: List of optimization recommendations
            
        Returns:
            Summary string
        """
        summary = []
        
        # Add metrics summary
        summary.append("## Metrics Summary")
        
        for category, category_metrics in metrics.items():
            if not category_metrics:
                continue
            
            summary.append(f"\n### {category.title()} Metrics")
            
            # Get the latest metrics
            latest = category_metrics[-1]
            
            # Add key metrics
            for key, value in latest.items():
                if key not in ['timestamp', 'iteration']:
                    if isinstance(value, float):
                        summary.append(f"- {key}: {value:.6g}")
                    else:
                        summary.append(f"- {key}: {value}")
        
        # Add bottlenecks
        if bottlenecks:
            summary.append("\n## Detected Bottlenecks")
            
            for bottleneck in bottlenecks:
                bottleneck_type = bottleneck.get('type', 'unknown')
                severity = bottleneck.get('severity', 'medium')
                message = bottleneck.get('message', 'No details available')
                
                summary.append(f"- {message} ({severity} severity, type: {bottleneck_type})")
        
        # Add recommendations
        if recommendations:
            summary.append("\n## Optimization Recommendations")
            
            for rec in recommendations:
                category = rec.get('category', 'general')
                priority = rec.get('priority', 'medium')
                message = rec.get('message', 'No details available')
                
                summary.append(f"- {message} ({priority} priority, category: {category})")
        
        return "\n".join(summary)
    
    def ask(self, query: str, metrics: Dict[str, List[Dict[str, Any]]], 
           bottlenecks: List[Dict[str, Any]], recommendations: List[Dict[str, Any]]) -> str:
        """
        Ask a question about the training process.
        
        Args:
            query: User query
            metrics: Dictionary of metrics
            bottlenecks: List of detected bottlenecks
            recommendations: List of optimization recommendations
            
        Returns:
            Response from the LLM
        """
        if not self.client:
            return "LLM client not initialized. Please check your API key and provider settings."
        
        # Prepare metrics summary
        metrics_summary = self._prepare_metrics_summary(metrics, bottlenecks, recommendations)
        
        # Prepare system prompt
        system_prompt = self.system_prompt.format(metrics_summary=metrics_summary)
        
        # Add query to conversation history
        self.conversation_history.append({"role": "user", "content": query})
        
        try:
            if self.provider == 'openai':
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        *self.conversation_history
                    ],
                    temperature=self.temperature
                )
                answer = response.choices[0].message.content
            
            elif self.provider == 'anthropic':
                messages = [{"role": "user" if msg["role"] == "user" else "assistant", 
                           "content": msg["content"]} for msg in self.conversation_history]
                
                response = self.client.messages.create(
                    model=self.model,
                    system=system_prompt,
                    messages=messages,
                    temperature=self.temperature
                )
                answer = response.content[0].text
            
            elif self.provider == 'huggingface':
                # Format conversation for HuggingFace
                conversation = f"System: {system_prompt}\n\n"
                
                for msg in self.conversation_history:
                    role = "User" if msg["role"] == "user" else "Assistant"
                    conversation += f"{role}: {msg['content']}\n\n"
                
                conversation += "Assistant: "
                
                response = self.client.text_generation(
                    prompt=conversation,
                    model=self.model,
                    temperature=self.temperature,
                    max_new_tokens=1024
                )
                answer = response
            
            elif self.provider == 'local':
                # Format conversation for local model
                conversation = f"System: {system_prompt}\n\n"
                
                for msg in self.conversation_history:
                    role = "User" if msg["role"] == "user" else "Assistant"
                    conversation += f"{role}: {msg['content']}\n\n"
                
                conversation += "Assistant: "
                
                response = self.client(
                    conversation,
                    max_new_tokens=1024,
                    temperature=self.temperature
                )
                answer = response[0]['generated_text'].split("Assistant: ")[-1]
            
            else:
                answer = "Unknown provider. Please use 'openai', 'anthropic', 'huggingface', or 'local'."
        
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            answer = f"Error generating response: {str(e)}"
        
        # Add response to conversation history
        self.conversation_history.append({"role": "assistant", "content": answer})
        
        return answer
    
    def ask_async(self, query: str, metrics: Dict[str, List[Dict[str, Any]]], 
                 bottlenecks: List[Dict[str, Any]], recommendations: List[Dict[str, Any]],
                 callback: Optional[Callable[[str], None]] = None):
        """
        Ask a question asynchronously.
        
        Args:
            query: User query
            metrics: Dictionary of metrics
            bottlenecks: List of detected bottlenecks
            recommendations: List of optimization recommendations
            callback: Optional callback function to call with the response
        """
        def _async_ask():
            response = self.ask(query, metrics, bottlenecks, recommendations)
            if callback:
                callback(response)
            self.response_queue.put(response)
        
        thread = threading.Thread(target=_async_ask)
        thread.daemon = True
        thread.start()
    
    def get_async_response(self, timeout: Optional[float] = None) -> Optional[str]:
        """
        Get the response from an asynchronous query.
        
        Args:
            timeout: Timeout in seconds (None for no timeout)
            
        Returns:
            Response or None if timeout
        """
        try:
            return self.response_queue.get(timeout=timeout)
        except queue.Empty:
            return None
    
    def clear_conversation(self):
        """Clear the conversation history."""
        self.conversation_history = []
        logger.info("Conversation history cleared")
    
    def save_conversation(self, file_path: str):
        """
        Save the conversation history to a file.
        
        Args:
            file_path: Path to save the conversation
        """
        with open(file_path, 'w') as f:
            json.dump(self.conversation_history, f, indent=2)
        
        logger.info(f"Conversation saved to {file_path}")
    
    def load_conversation(self, file_path: str):
        """
        Load conversation history from a file.
        
        Args:
            file_path: Path to load the conversation from
        """
        with open(file_path, 'r') as f:
            self.conversation_history = json.load(f)
        
        logger.info(f"Conversation loaded from {file_path}")

class LLMInterface:
    """
    High-level interface for interacting with AutoPipelineDoctor using natural language.
    
    This class provides a user-friendly interface for interacting with
    AutoPipelineDoctor using natural language queries.
    """
    
    def __init__(self, doctor, api_key: Optional[str] = None, provider: str = 'openai'):
        """
        Initialize the LLM interface.
        
        Args:
            doctor: AutoPipelineDoctor instance
            api_key: API key for the LLM provider
            provider: LLM provider ('openai', 'anthropic', 'huggingface', 'local')
        """
        self.doctor = doctor
        self.assistant = LLMAssistant(api_key=api_key, provider=provider)
        
        # Command patterns
        self.command_patterns = {
            r'(?i)show\s+metrics(?:\s+for\s+(\w+))?': self._handle_show_metrics,
            r'(?i)show\s+bottlenecks': self._handle_show_bottlenecks,
            r'(?i)show\s+recommendations': self._handle_show_recommendations,
            r'(?i)visualize\s+(\w+)': self._handle_visualize,
            r'(?i)optimize\s+(\w+)': self._handle_optimize,
            r'(?i)explain\s+(\w+)': self._handle_explain,
            r'(?i)generate\s+report': self._handle_generate_report
        }
    
    def process_query(self, query: str) -> str:
        """
        Process a natural language query.
        
        Args:
            query: User query
            
        Returns:
            Response
        """
        # Check if query matches a command pattern
        for pattern, handler in self.command_patterns.items():
            match = re.match(pattern, query)
            if match:
                return handler(*match.groups())
        
        # If no command pattern matches, treat as a general question
        return self._handle_general_question(query)
    
    def _handle_general_question(self, query: str) -> str:
        """
        Handle a general question.
        
        Args:
            query: User query
            
        Returns:
            Response
        """
        # Get metrics, bottlenecks, and recommendations from doctor
        metrics = self.doctor.metrics
        bottlenecks = self.doctor.get_bottlenecks() if hasattr(self.doctor, 'get_bottlenecks') else []
        recommendations = self.doctor.get_recommendations()
        
        # Ask the LLM assistant
        return self.assistant.ask(query, metrics, bottlenecks, recommendations)
    
    def _handle_show_metrics(self, category: Optional[str] = None) -> str:
        """
        Handle show metrics command.
        
        Args:
            category: Optional category of metrics to show
            
        Returns:
            Response
        """
        metrics = self.doctor.metrics
        
        if category and category in metrics:
            if metrics[category]:
                return f"## {category.title()} Metrics\n\n" + json.dumps(metrics[category][-1], indent=2)
            else:
                return f"No metrics available for category: {category}"
        
        # Show summary of all metrics
        summary = []
        
        for cat, cat_metrics in metrics.items():
            if cat_metrics:
                summary.append(f"## {cat.title()} Metrics\n")
                latest = cat_metrics[-1]
                for key, value in latest.items():
                    if key not in ['timestamp', 'iteration']:
                        if isinstance(value, float):
                            summary.append(f"- {key}: {value:.6g}")
                        else:
                            summary.append(f"- {key}: {value}")
                summary.append("")
        
        if summary:
            return "\n".join(summary)
        else:
            return "No metrics available yet."
    
    def _handle_show_bottlenecks(self) -> str:
        """
        Handle show bottlenecks command.
        
        Returns:
            Response
        """
        if hasattr(self.doctor, 'get_bottlenecks'):
            bottlenecks = self.doctor.get_bottlenecks()
            
            if bottlenecks:
                response = f"## Detected Bottlenecks ({len(bottlenecks)})\n\n"
                
                for i, bottleneck in enumerate(bottlenecks, 1):
                    bottleneck_type = bottleneck.get('type', 'unknown')
                    severity = bottleneck.get('severity', 'medium')
                    message = bottleneck.get('message', 'No details available')
                    details = bottleneck.get('details', '')
                    
                    response += f"{i}. {message} ({severity} severity, type: {bottleneck_type})\n"
                    if details:
                        response += f"   {details}\n"
                    response += "\n"
                
                return response
            else:
                return "No bottlenecks detected."
        else:
            return "Bottleneck detection not available."
    
    def _handle_show_recommendations(self) -> str:
        """
        Handle show recommendations command.
        
        Returns:
            Response
        """
        recommendations = self.doctor.get_recommendations()
        
        if recommendations:
            response = f"## Optimization Recommendations ({len(recommendations)})\n\n"
            
            # Group by category
            categories = {}
            for rec in recommendations:
                category = rec.get('category', 'general')
                if category not in categories:
                    categories[category] = []
                categories[category].append(rec)
            
            for category, category_recs in categories.items():
                response += f"### {category.title()} Optimizations\n\n"
                
                for i, rec in enumerate(category_recs, 1):
                    priority = rec.get('priority', 'medium')
                    message = rec.get('message', 'No details available')
                    details = rec.get('details', '')
                    
                    response += f"{i}. {message} ({priority} priority)\n"
                    if details:
                        response += f"   {details}\n"
                    response += "\n"
            
            return response
        else:
            return "No optimization recommendations available."
    
    def _handle_visualize(self, metric: str) -> str:
        """
        Handle visualize command.
        
        Args:
            metric: Metric to visualize
            
        Returns:
            Response
        """
        if hasattr(self.doctor, 'visualize'):
            try:
                visualization = self.doctor.visualize(visualization_type=metric)
                return f"Visualization for {metric} created. Check the output directory for the visualization files."
            except Exception as e:
                return f"Error creating visualization: {str(e)}"
        else:
            return "Visualization not available."
    
    def _handle_optimize(self, optimization: str) -> str:
        """
        Handle optimize command.
        
        Args:
            optimization: Optimization to apply
            
        Returns:
            Response
        """
        if hasattr(self.doctor, 'apply_optimization'):
            try:
                result = self.doctor.apply_optimization(optimization)
                if result:
                    return f"Optimization '{optimization}' applied successfully."
                else:
                    return f"Failed to apply optimization '{optimization}'."
            except Exception as e:
                return f"Error applying optimization: {str(e)}"
        else:
            return "Optimization application not available."
    
    def _handle_explain(self, topic: str) -> str:
        """
        Handle explain command.
        
        Args:
            topic: Topic to explain
            
        Returns:
            Response
        """
        # Get metrics, bottlenecks, and recommendations from doctor
        metrics = self.doctor.metrics
        bottlenecks = self.doctor.get_bottlenecks() if hasattr(self.doctor, 'get_bottlenecks') else []
        recommendations = self.doctor.get_recommendations()
        
        # Formulate a specific question based on the topic
        if topic.lower() in ['memory', 'memory usage']:
            query = "Explain the memory usage patterns in the training process. Are there any concerns or optimizations needed?"
        elif topic.lower() in ['timing', 'performance']:
            query = "Explain the timing breakdown of the training process. Where are the bottlenecks and how can they be addressed?"
        elif topic.lower() in ['gradients', 'gradient']:
            query = "Explain the gradient statistics. Are there any issues like vanishing or exploding gradients?"
        elif topic.lower() in ['bottlenecks', 'bottleneck']:
            query = "Explain the detected bottlenecks in detail and how they affect training performance."
        elif topic.lower() in ['recommendations', 'optimizations']:
            query = "Explain the optimization recommendations in detail and how they would improve training."
        else:
            query = f"Explain {topic} in the context of the current training process."
        
        # Ask the LLM assistant
        return self.assistant.ask(query, metrics, bottlenecks, recommendations)
    
    def _handle_generate_report(self) -> str:
        """
        Handle generate report command.
        
        Returns:
            Response
        """
        if hasattr(self.doctor, 'generate_report'):
            try:
                report = self.doctor.generate_report()
                return f"Report generated. Check the output directory for the report file."
            except Exception as e:
                return f"Error generating report: {str(e)}"
        else:
            return "Report generation not available."
    
    def start_cli(self):
        """Start a command-line interface for interacting with the LLM interface."""
        print("AutoPipelineDoctor LLM Interface")
        print("Type 'exit' or 'quit' to exit")
        print()
        
        while True:
            try:
                query = input("> ")
                
                if query.lower() in ['exit', 'quit']:
                    break
                
                response = self.process_query(query)
                print("\n" + response + "\n")
            
            except KeyboardInterrupt:
                print("\nExiting...")
                break
            
            except Exception as e:
                print(f"Error: {str(e)}")
    
    def start_web_interface(self, host: str = '0.0.0.0', port: int = 8080):
        """
        Start a web interface for interacting with the LLM interface.
        
        Args:
            host: Host to bind to
            port: Port to bind to
        """
        try:
            from flask import Flask, request, jsonify, render_template_string
            
            app = Flask(__name__)
            
            @app.route('/')
            def home():
                html = """
                <!DOCTYPE html>
                <html>
                <head>
                    <title>AutoPipelineDoctor LLM Interface</title>
                    <style>
                        body {
                            font-family: Arial, sans-serif;
                            margin: 0;
                            padding: 20px;
                            background-color: #f5f5f5;
                        }
                        .container {
                            max-width: 800px;
                            margin: 0 auto;
                            background-color: white;
                            padding: 20px;
                            border-radius: 5px;
                            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                        }
                        .header {
                            text-align: center;
                            margin-bottom: 20px;
                        }
                        .chat-container {
                            height: 400px;
                            overflow-y: auto;
                            border: 1px solid #ddd;
                            padding: 10px;
                            margin-bottom: 10px;
                            border-radius: 5px;
                        }
                        .input-container {
                            display: flex;
                        }
                        .input-container input {
                            flex-grow: 1;
                            padding: 10px;
                            border: 1px solid #ddd;
                            border-radius: 5px;
                        }
                        .input-container button {
                            padding: 10px 20px;
                            background-color: #4CAF50;
                            color: white;
                            border: none;
                            border-radius: 5px;
                            margin-left: 10px;
                            cursor: pointer;
                        }
                        .message {
                            margin-bottom: 10px;
                            padding: 10px;
                            border-radius: 5px;
                        }
                        .user-message {
                            background-color: #e6f7ff;
                            text-align: right;
                        }
                        .assistant-message {
                            background-color: #f0f0f0;
                        }
                    </style>
                </head>
                <body>
                    <div class="container">
                        <div class="header">
                            <h1>AutoPipelineDoctor LLM Interface</h1>
                        </div>
                        <div class="chat-container" id="chat-container"></div>
                        <div class="input-container">
                            <input type="text" id="query-input" placeholder="Ask a question...">
                            <button id="send-button">Send</button>
                        </div>
                    </div>
                    
                    <script>
                        document.getElementById('send-button').addEventListener('click', sendQuery);
                        document.getElementById('query-input').addEventListener('keypress', function(e) {
                            if (e.key === 'Enter') {
                                sendQuery();
                            }
                        });
                        
                        function sendQuery() {
                            const queryInput = document.getElementById('query-input');
                            const query = queryInput.value.trim();
                            
                            if (query) {
                                // Add user message to chat
                                addMessage(query, 'user');
                                
                                // Clear input
                                queryInput.value = '';
                                
                                // Send query to server
                                fetch('/query', {
                                    method: 'POST',
                                    headers: {
                                        'Content-Type': 'application/json'
                                    },
                                    body: JSON.stringify({ query: query })
                                })
                                .then(response => response.json())
                                .then(data => {
                                    // Add assistant message to chat
                                    addMessage(data.response, 'assistant');
                                })
                                .catch(error => {
                                    console.error('Error:', error);
                                    addMessage('Error: ' + error, 'assistant');
                                });
                            }
                        }
                        
                        function addMessage(message, role) {
                            const chatContainer = document.getElementById('chat-container');
                            const messageElement = document.createElement('div');
                            messageElement.classList.add('message');
                            messageElement.classList.add(role + '-message');
                            
                            // Convert markdown to HTML
                            const converter = new showdown.Converter();
                            messageElement.innerHTML = converter.makeHtml(message);
                            
                            chatContainer.appendChild(messageElement);
                            chatContainer.scrollTop = chatContainer.scrollHeight;
                        }
                    </script>
                    
                    <!-- Add showdown.js for markdown support -->
                    <script src="https://cdnjs.cloudflare.com/ajax/libs/showdown/1.9.1/showdown.min.js"></script>
                </body>
                </html>
                """
                return render_template_string(html)
            
            @app.route('/query', methods=['POST'])
            def query():
                data = request.json
                query = data.get('query', '')
                
                response = self.process_query(query)
                
                return jsonify({'response': response})
            
            print(f"Starting web interface on http://{host}:{port}")
            app.run(host=host, port=port)
        
        except ImportError:
            print("Flask not installed. Run 'pip install flask' to use the web interface.")
