# AutoPipelineDoctor Documentation

## Overview

AutoPipelineDoctor (autopd) is a sophisticated Python library that automatically watches, diagnoses, predicts, optimizes, and explains model training behavior across all major deep learning stacks. It serves as an essential companion to every model training session, providing real-time insights and optimizations without requiring significant code changes.

## Installation

```bash
pip install autopd
```

## Quick Start

```python
import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from autopd import Doctor

# Create your model, optimizer, and dataloader
model = nn.Sequential(nn.Linear(784, 128), nn.ReLU(), nn.Linear(128, 10))
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
dataloader = DataLoader(dataset, batch_size=32)

# Initialize AutoPipelineDoctor
doctor = Doctor(model, optimizer, dataloader)

# Option 1: Watch your training loop
@doctor.watch
def train_loop(model, optimizer, dataloader, epochs=10):
    for epoch in range(epochs):
        for batch in dataloader:
            inputs, targets = batch
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = nn.functional.cross_entropy(outputs, targets)
            loss.backward()
            optimizer.step()

train_loop(model, optimizer, dataloader)

# Option 2: Auto-patch your training components
doctor.auto_patch()

# Your regular training loop
for epoch in range(10):
    for batch in dataloader:
        inputs, targets = batch
        optimizer.zero_grad()
        outputs = model(inputs)
        loss = nn.functional.cross_entropy(outputs, targets)
        loss.backward()
        optimizer.step()

# Get insights and recommendations
doctor.visualize()
recommendations = doctor.get_recommendations()
```

## Core Features

### 1. Always-Watching Pipeline AI

AutoPipelineDoctor continuously monitors your training in real-time, tracking:

- Batch latency
- GPU/CPU load
- Forward/backward/optimizer timings
- Memory usage and fragmentation
- Dataloader bottlenecks

### 2. Predictive Failure Forecasting

The library learns pipeline patterns to predict:

- OOM errors before they happen
- Overfitting/underfitting trajectories
- Dead gradient zones
- Imbalanced compute/data scaling

### 3. Intelligent Optimization Advisor

AutoPipelineDoctor suggests or auto-applies:

- AMP / bfloat16
- Dataloader worker tuning
- Batch size balancing
- Gradient checkpointing
- RAM/GPU swapoff
- Scheduler reconfiguration

### 4. Visual Feedback

The library provides:

- Real-time dashboards
- Memory usage graphs
- Bottleneck visualizations
- Gradient flow diagrams
- Optimization impact charts

### 5. LLM Assistant Interface

You can interact with AutoPipelineDoctor using natural language:

- Ask questions about performance
- Request explanations of bottlenecks
- Get optimization suggestions
- Generate reports

### 6. Memory of Past Runs

AutoPipelineDoctor retains historical run logs, graphs, and bottleneck maps, learning over time which models fail where.

### 7. Framework Support

The library works with:

- PyTorch / Lightning / HuggingFace
- Deepspeed
- Torch.compile / TorchDynamo

## Detailed API Reference

### Doctor Class

The central controller class that orchestrates all monitoring and optimization.

```python
class Doctor:
    def __init__(self, model=None, optimizer=None, dataloader=None, config=None):
        """
        Initialize the Doctor.
        
        Args:
            model: PyTorch model to monitor
            optimizer: PyTorch optimizer to monitor
            dataloader: PyTorch dataloader to monitor
            config: Configuration dictionary or path to configuration file
        """
        
    def watch(self, train_loop):
        """
        Decorator to watch a training loop.
        
        Args:
            train_loop: Training loop function to watch
            
        Returns:
            Wrapped training loop function
        """
        
    def auto_patch(self):
        """
        Automatically discover and patch PyTorch components in the caller's frame.
        """
        
    def visualize(self, output_path=None):
        """
        Generate visualizations of the monitored metrics.
        
        Args:
            output_path: Path to save visualizations
            
        Returns:
            Path to the generated visualizations
        """
        
    def get_recommendations(self):
        """
        Get optimization recommendations.
        
        Returns:
            List of recommendations
        """
        
    def apply_recommendations(self, recommendations=None):
        """
        Apply optimization recommendations.
        
        Args:
            recommendations: List of recommendations to apply
            
        Returns:
            Applied recommendations
        """
        
    def ask(self, query):
        """
        Ask a natural language question about the training.
        
        Args:
            query: Natural language query
            
        Returns:
            Natural language response
        """
        
    def save_report(self, output_path=None):
        """
        Save a comprehensive report of the training.
        
        Args:
            output_path: Path to save the report
            
        Returns:
            Path to the saved report
        """
```

### Profiler Modules

#### HardwareProfiler

Monitors CPU/GPU usage, memory, and temperature.

```python
class HardwareProfiler:
    def __init__(self, doctor, config=None):
        """
        Initialize the hardware profiler.
        
        Args:
            doctor: Reference to the Doctor instance
            config: Configuration dictionary
        """
        
    def start(self):
        """
        Start monitoring hardware.
        """
        
    def stop(self):
        """
        Stop monitoring hardware.
        """
        
    def update_metrics(self, metrics):
        """
        Update hardware metrics.
        
        Args:
            metrics: Dictionary of metrics
        """
        
    def get_metrics(self):
        """
        Get hardware metrics.
        
        Returns:
            Dictionary of metrics
        """
```

#### MemoryProfiler

Tracks memory consumption, fragmentation, and model size.

```python
class MemoryProfiler:
    def __init__(self, doctor, config=None):
        """
        Initialize the memory profiler.
        
        Args:
            doctor: Reference to the Doctor instance
            config: Configuration dictionary
        """
        
    def start(self):
        """
        Start monitoring memory.
        """
        
    def stop(self):
        """
        Stop monitoring memory.
        """
        
    def update_metrics(self, metrics):
        """
        Update memory metrics.
        
        Args:
            metrics: Dictionary of metrics
        """
        
    def get_metrics(self):
        """
        Get memory metrics.
        
        Returns:
            Dictionary of metrics
        """
        
    def predict_oom(self):
        """
        Predict out-of-memory errors.
        
        Returns:
            OOM prediction details
        """
```

#### TimingProfiler

Measures execution times for forward/backward passes and identifies bottlenecks.

```python
class TimingProfiler:
    def __init__(self, doctor, config=None):
        """
        Initialize the timing profiler.
        
        Args:
            doctor: Reference to the Doctor instance
            config: Configuration dictionary
        """
        
    def start(self):
        """
        Start monitoring timing.
        """
        
    def stop(self):
        """
        Stop monitoring timing.
        """
        
    def update_metrics(self, metrics):
        """
        Update timing metrics.
        
        Args:
            metrics: Dictionary of metrics
        """
        
    def get_metrics(self):
        """
        Get timing metrics.
        
        Returns:
            Dictionary of metrics
        """
        
    def identify_bottlenecks(self):
        """
        Identify timing bottlenecks.
        
        Returns:
            List of bottlenecks
        """
```

#### DataloaderProfiler

Analyzes dataloader performance and worker utilization.

```python
class DataloaderProfiler:
    def __init__(self, doctor, config=None):
        """
        Initialize the dataloader profiler.
        
        Args:
            doctor: Reference to the Doctor instance
            config: Configuration dictionary
        """
        
    def start(self):
        """
        Start monitoring dataloader.
        """
        
    def stop(self):
        """
        Stop monitoring dataloader.
        """
        
    def update_metrics(self, metrics):
        """
        Update dataloader metrics.
        
        Args:
            metrics: Dictionary of metrics
        """
        
    def get_metrics(self):
        """
        Get dataloader metrics.
        
        Returns:
            Dictionary of metrics
        """
        
    def optimize_workers(self):
        """
        Optimize dataloader workers.
        
        Returns:
            Optimal worker count
        """
```

#### GradientProfiler

Monitors gradient statistics and detects issues like vanishing/exploding gradients.

```python
class GradientProfiler:
    def __init__(self, doctor, config=None):
        """
        Initialize the gradient profiler.
        
        Args:
            doctor: Reference to the Doctor instance
            config: Configuration dictionary
        """
        
    def start(self):
        """
        Start monitoring gradients.
        """
        
    def stop(self):
        """
        Stop monitoring gradients.
        """
        
    def update_metrics(self, metrics):
        """
        Update gradient metrics.
        
        Args:
            metrics: Dictionary of metrics
        """
        
    def get_metrics(self):
        """
        Get gradient metrics.
        
        Returns:
            Dictionary of metrics
        """
        
    def detect_issues(self):
        """
        Detect gradient issues.
        
        Returns:
            List of issues
        """
```

### Bottleneck Detection

#### FailureForecaster

Predicts training failures before they happen.

```python
class FailureForecaster:
    def __init__(self, doctor, config=None):
        """
        Initialize the failure forecaster.
        
        Args:
            doctor: Reference to the Doctor instance
            config: Configuration dictionary
        """
        
    def update(self, metrics):
        """
        Update forecaster with new metrics.
        
        Args:
            metrics: Dictionary of metrics
        """
        
    def predict_failures(self):
        """
        Predict potential failures.
        
        Returns:
            List of potential failures
        """
        
    def get_warnings(self):
        """
        Get active warnings.
        
        Returns:
            List of warnings
        """
```

### Optimization

#### OptimizationAdvisor

Provides intelligent optimization suggestions.

```python
class OptimizationAdvisor:
    def __init__(self, doctor, config=None):
        """
        Initialize the optimization advisor.
        
        Args:
            doctor: Reference to the Doctor instance
            config: Configuration dictionary
        """
        
    def analyze(self):
        """
        Analyze current state and generate recommendations.
        
        Returns:
            List of recommendations
        """
        
    def apply(self, recommendations=None):
        """
        Apply optimization recommendations.
        
        Args:
            recommendations: List of recommendations to apply
            
        Returns:
            Applied recommendations
        """
        
    def get_optimization_level(self):
        """
        Get current optimization level.
        
        Returns:
            Optimization level
        """
        
    def set_optimization_level(self, level):
        """
        Set optimization level.
        
        Args:
            level: Optimization level (conservative, balanced, aggressive)
        """
```

### Visualization

#### Visualizer

Creates interactive dashboards and static plots.

```python
class Visualizer:
    def __init__(self, doctor, config=None):
        """
        Initialize the visualizer.
        
        Args:
            doctor: Reference to the Doctor instance
            config: Configuration dictionary
        """
        
    def create_dashboard(self, output_path=None):
        """
        Create an interactive dashboard.
        
        Args:
            output_path: Path to save the dashboard
            
        Returns:
            Path to the dashboard
        """
        
    def plot_memory_usage(self, output_path=None):
        """
        Plot memory usage.
        
        Args:
            output_path: Path to save the plot
            
        Returns:
            Path to the plot
        """
        
    def plot_timing_breakdown(self, output_path=None):
        """
        Plot timing breakdown.
        
        Args:
            output_path: Path to save the plot
            
        Returns:
            Path to the plot
        """
        
    def plot_gradient_statistics(self, output_path=None):
        """
        Plot gradient statistics.
        
        Args:
            output_path: Path to save the plot
            
        Returns:
            Path to the plot
        """
        
    def plot_custom(self, metrics, output_path=None):
        """
        Create a custom plot.
        
        Args:
            metrics: Dictionary of metrics to plot
            output_path: Path to save the plot
            
        Returns:
            Path to the plot
        """
```

### LLM Interface

#### LLMAssistant

Provides natural language interaction capabilities.

```python
class LLMAssistant:
    def __init__(self, doctor, config=None):
        """
        Initialize the LLM assistant.
        
        Args:
            doctor: Reference to the Doctor instance
            config: Configuration dictionary
        """
        
    def ask(self, query):
        """
        Ask a natural language question.
        
        Args:
            query: Natural language query
            
        Returns:
            Natural language response
        """
        
    def explain(self, metric):
        """
        Explain a specific metric.
        
        Args:
            metric: Metric to explain
            
        Returns:
            Natural language explanation
        """
        
    def suggest_optimizations(self):
        """
        Suggest optimizations in natural language.
        
        Returns:
            Natural language suggestions
        """
        
    def generate_report(self):
        """
        Generate a natural language report.
        
        Returns:
            Natural language report
        """
```

### Historical Memory

#### ExperienceBrain

Stores and analyzes past training runs.

```python
class ExperienceBrain:
    def __init__(self, doctor, config=None):
        """
        Initialize the experience brain.
        
        Args:
            doctor: Reference to the Doctor instance
            config: Configuration dictionary
        """
        
    def start(self, model_info=None, dataset_info=None, hardware_info=None):
        """
        Start a new training run.
        
        Args:
            model_info: Information about the model
            dataset_info: Information about the dataset
            hardware_info: Information about the hardware
        """
        
    def stop(self, status="completed"):
        """
        Stop the current training run.
        
        Args:
            status: Status of the run
        """
        
    def update_metrics(self, metrics, category=None):
        """
        Update metrics for the current run.
        
        Args:
            metrics: Dictionary of metrics
            category: Metric category
        """
        
    def add_warning(self, warning):
        """
        Add a warning to the current run.
        
        Args:
            warning: Warning details
        """
        
    def add_optimization(self, optimization):
        """
        Add an optimization to the current run.
        
        Args:
            optimization: Optimization details
        """
        
    def get_similar_runs(self, limit=5):
        """
        Get similar runs to the current run.
        
        Args:
            limit: Maximum number of runs to return
            
        Returns:
            List of similar runs
        """
        
    def predict_from_history(self):
        """
        Make predictions based on historical runs.
        
        Returns:
            Predictions
        """
```

### Framework Integrations

#### PyTorchIntegration

Integration with PyTorch models, optimizers, and dataloaders.

```python
class PyTorchIntegration:
    def __init__(self, doctor, model=None, optimizer=None, dataloader=None):
        """
        Initialize the PyTorch integration.
        
        Args:
            doctor: Reference to the Doctor instance
            model: PyTorch model to monitor
            optimizer: PyTorch optimizer to monitor
            dataloader: PyTorch dataloader to monitor
        """
        
    def register(self, model=None, optimizer=None, dataloader=None):
        """
        Register PyTorch components for monitoring.
        
        Args:
            model: PyTorch model to monitor
            optimizer: PyTorch optimizer to monitor
            dataloader: PyTorch dataloader to monitor
        """
        
    def attach(self):
        """
        Attach hooks and patches to the registered PyTorch components.
        """
        
    def detach(self):
        """
        Detach hooks and restore original methods.
        """
        
    def auto_patch(self):
        """
        Automatically discover and patch PyTorch components in the caller's frame.
        """
        
    def watch(self, train_loop):
        """
        Watch a training loop.
        
        Args:
            train_loop: Training loop function to watch
            
        Returns:
            Wrapped training loop function
        """
```

#### LightningIntegration

Integration with PyTorch Lightning.

```python
class LightningIntegration:
    def __init__(self, doctor):
        """
        Initialize the Lightning integration.
        
        Args:
            doctor: Reference to the Doctor instance
        """
        
    def get_callback(self):
        """
        Get the Lightning callback.
        
        Returns:
            Lightning callback
        """
        
    @staticmethod
    def patch_trainer(trainer, doctor):
        """
        Patch a Lightning trainer to enable monitoring.
        
        Args:
            trainer: Lightning trainer to patch
            doctor: Reference to the Doctor instance
            
        Returns:
            Patched trainer
        """
        
    @staticmethod
    def create_trainer_with_monitoring(doctor, **trainer_kwargs):
        """
        Create a Lightning trainer with monitoring.
        
        Args:
            doctor: Reference to the Doctor instance
            **trainer_kwargs: Keyword arguments for the trainer
            
        Returns:
            Lightning trainer with monitoring
        """
```

#### HuggingFaceIntegration

Integration with HuggingFace Transformers.

```python
class HuggingFaceIntegration:
    def __init__(self, doctor):
        """
        Initialize the HuggingFace integration.
        
        Args:
            doctor: Reference to the Doctor instance
        """
        
    def get_callback(self):
        """
        Get the HuggingFace callback.
        
        Returns:
            HuggingFace callback
        """
        
    @staticmethod
    def patch_trainer(trainer, doctor):
        """
        Patch a HuggingFace trainer to enable monitoring.
        
        Args:
            trainer: HuggingFace trainer to patch
            doctor: Reference to the Doctor instance
            
        Returns:
            Patched trainer
        """
        
    @staticmethod
    def create_trainer_with_monitoring(doctor, model, args, **trainer_kwargs):
        """
        Create a HuggingFace trainer with monitoring.
        
        Args:
            doctor: Reference to the Doctor instance
            model: HuggingFace model
            args: Training arguments
            **trainer_kwargs: Keyword arguments for the trainer
            
        Returns:
            HuggingFace trainer with monitoring
        """
```

#### DeepSpeedIntegration

Integration with DeepSpeed.

```python
class DeepSpeedIntegration:
    def __init__(self, doctor, engine=None):
        """
        Initialize the DeepSpeed integration.
        
        Args:
            doctor: Reference to the Doctor instance
            engine: DeepSpeed engine to monitor
        """
        
    def register(self, engine):
        """
        Register a DeepSpeed engine for monitoring.
        
        Args:
            engine: DeepSpeed engine to monitor
        """
        
    def attach(self):
        """
        Attach hooks and patches to the registered DeepSpeed engine.
        """
        
    def detach(self):
        """
        Detach hooks and restore original methods.
        """
        
    def watch(self, train_func):
        """
        Watch a training function.
        
        Args:
            train_func: Training function to watch
            
        Returns:
            Wrapped training function
        """
        
    @staticmethod
    def patch_engine(engine, doctor):
        """
        Patch a DeepSpeed engine to enable monitoring.
        
        Args:
            engine: DeepSpeed engine to patch
            doctor: Reference to the Doctor instance
            
        Returns:
            Patched engine
        """
        
    @staticmethod
    def initialize_with_monitoring(model, optimizer=None, config=None, doctor=None, **kwargs):
        """
        Initialize a DeepSpeed engine with monitoring.
        
        Args:
            model: PyTorch model
            optimizer: PyTorch optimizer
            config: DeepSpeed configuration
            doctor: Reference to the Doctor instance
            **kwargs: Additional keyword arguments for DeepSpeed initialization
            
        Returns:
            DeepSpeed engine with monitoring
        """
```

#### TorchDynamoIntegration

Integration with TorchDynamo and torch.compile.

```python
class TorchDynamoIntegration:
    def __init__(self, doctor):
        """
        Initialize the TorchDynamo integration.
        
        Args:
            doctor: Reference to the Doctor instance
        """
        
    def attach(self):
        """
        Attach hooks and patches to TorchDynamo and torch.compile.
        """
        
    def detach(self):
        """
        Detach hooks and restore original methods.
        """
        
    @staticmethod
    def enable_monitoring(doctor):
        """
        Enable monitoring for TorchDynamo and torch.compile.
        
        Args:
            doctor: Reference to the Doctor instance
            
        Returns:
            TorchDynamo integration
        """
```

## Advanced Usage Examples

### PyTorch Example

```python
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
import numpy as np
from autopd import Doctor

# Create a synthetic dataset
x = torch.randn(1000, 20)
y = torch.randint(0, 2, (1000,))
dataset = TensorDataset(x, y)
dataloader = DataLoader(dataset, batch_size=32, shuffle=True)

# Create a model
model = nn.Sequential(
    nn.Linear(20, 64),
    nn.ReLU(),
    nn.Dropout(0.2),
    nn.Linear(64, 32),
    nn.ReLU(),
    nn.Linear(32, 2)
)

# Create an optimizer
optimizer = optim.Adam(model.parameters(), lr=0.001)

# Initialize AutoPipelineDoctor
doctor = Doctor(model, optimizer, dataloader)

# Define a training loop
def train(epochs=10):
    for epoch in range(epochs):
        for batch_idx, (data, target) in enumerate(dataloader):
            optimizer.zero_grad()
            output = model(data)
            loss = nn.functional.cross_entropy(output, target)
            loss.backward()
            optimizer.step()
            
            if batch_idx % 10 == 0:
                print(f"Epoch: {epoch}, Batch: {batch_idx}, Loss: {loss.item():.4f}")

# Watch the training loop
watched_train = doctor.watch(train)
watched_train(epochs=5)

# Get recommendations
recommendations = doctor.get_recommendations()
print("Recommendations:")
for rec in recommendations:
    print(f"- {rec['message']}")

# Apply recommendations
doctor.apply_recommendations()

# Continue training with optimizations
watched_train(epochs=5)

# Visualize results
doctor.visualize()

# Ask questions
response = doctor.ask("What was the main bottleneck in my training?")
print(response)

# Save a report
report_path = doctor.save_report()
print(f"Report saved to: {report_path}")
```

### PyTorch Lightning Example

```python
import torch
import torch.nn as nn
import torch.nn.functional as F
import pytorch_lightning as pl
from torch.utils.data import DataLoader, TensorDataset
import numpy as np
from autopd import Doctor
from autopd.integrations import LightningIntegration

# Create a synthetic dataset
x = torch.randn(1000, 20)
y = torch.randint(0, 2, (1000,))
dataset = TensorDataset(x, y)
train_loader = DataLoader(dataset, batch_size=32, shuffle=True)

# Define a Lightning module
class LitModel(pl.LightningModule):
    def __init__(self):
        super().__init__()
        self.layer1 = nn.Linear(20, 64)
        self.layer2 = nn.Linear(64, 32)
        self.layer3 = nn.Linear(32, 2)
        
    def forward(self, x):
        x = F.relu(self.layer1(x))
        x = F.dropout(x, 0.2)
        x = F.relu(self.layer2(x))
        x = self.layer3(x)
        return x
    
    def training_step(self, batch, batch_idx):
        x, y = batch
        logits = self(x)
        loss = F.cross_entropy(logits, y)
        self.log('train_loss', loss)
        return loss
    
    def configure_optimizers(self):
        return torch.optim.Adam(self.parameters(), lr=0.001)

# Initialize model
model = LitModel()

# Initialize AutoPipelineDoctor
doctor = Doctor()

# Get Lightning integration
lightning_integration = LightningIntegration(doctor)

# Create a trainer with monitoring
trainer = lightning_integration.create_trainer_with_monitoring(
    doctor,
    max_epochs=10,
    enable_progress_bar=True
)

# Train the model
trainer.fit(model, train_loader)

# Get recommendations
recommendations = doctor.get_recommendations()
print("Recommendations:")
for rec in recommendations:
    print(f"- {rec['message']}")

# Visualize results
doctor.visualize()

# Ask questions
response = doctor.ask("How can I improve my training efficiency?")
print(response)
```

### HuggingFace Transformers Example

```python
import torch
from transformers import BertForSequenceClassification, BertTokenizer
from transformers import Trainer, TrainingArguments
from datasets import load_dataset
from autopd import Doctor
from autopd.integrations import HuggingFaceIntegration

# Load dataset
dataset = load_dataset("glue", "mrpc")
tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")

def tokenize_function(examples):
    return tokenizer(examples["sentence1"], examples["sentence2"], padding="max_length", truncation=True)

tokenized_datasets = dataset.map(tokenize_function, batched=True)
train_dataset = tokenized_datasets["train"]
eval_dataset = tokenized_datasets["validation"]

# Load model
model = BertForSequenceClassification.from_pretrained("bert-base-uncased")

# Initialize AutoPipelineDoctor
doctor = Doctor()

# Get HuggingFace integration
hf_integration = HuggingFaceIntegration(doctor)

# Define training arguments
training_args = TrainingArguments(
    output_dir="./results",
    num_train_epochs=3,
    per_device_train_batch_size=16,
    per_device_eval_batch_size=16,
    warmup_steps=500,
    weight_decay=0.01,
    logging_dir="./logs",
    logging_steps=10,
)

# Create a trainer with monitoring
trainer = hf_integration.create_trainer_with_monitoring(
    doctor,
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=eval_dataset,
)

# Train the model
trainer.train()

# Get recommendations
recommendations = doctor.get_recommendations()
print("Recommendations:")
for rec in recommendations:
    print(f"- {rec['message']}")

# Visualize results
doctor.visualize()

# Ask questions
response = doctor.ask("What are the main memory bottlenecks in my transformer model?")
print(response)
```

### DeepSpeed Example

```python
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import DataLoader, TensorDataset
import deepspeed
from autopd import Doctor
from autopd.integrations import DeepSpeedIntegration

# Create a synthetic dataset
x = torch.randn(1000, 20)
y = torch.randint(0, 2, (1000,))
dataset = TensorDataset(x, y)
dataloader = DataLoader(dataset, batch_size=32, shuffle=True)

# Define a model
class SimpleModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.layer1 = nn.Linear(20, 64)
        self.layer2 = nn.Linear(64, 32)
        self.layer3 = nn.Linear(32, 2)
        
    def forward(self, x):
        x = F.relu(self.layer1(x))
        x = F.dropout(x, 0.2)
        x = F.relu(self.layer2(x))
        x = self.layer3(x)
        return x

# Initialize model
model = SimpleModel()

# Initialize AutoPipelineDoctor
doctor = Doctor()

# DeepSpeed configuration
ds_config = {
    "train_batch_size": 32,
    "steps_per_print": 10,
    "optimizer": {
        "type": "Adam",
        "params": {
            "lr": 0.001
        }
    },
    "zero_optimization": {
        "stage": 1
    }
}

# Initialize DeepSpeed with monitoring
engine = DeepSpeedIntegration.initialize_with_monitoring(
    model=model,
    config=ds_config,
    doctor=doctor
)

# Training loop
def train(engine, dataloader, epochs=10):
    for epoch in range(epochs):
        for batch_idx, (data, target) in enumerate(dataloader):
            outputs = engine(data)
            loss = F.cross_entropy(outputs, target)
            engine.backward(loss)
            engine.step()
            
            if batch_idx % 10 == 0:
                print(f"Epoch: {epoch}, Batch: {batch_idx}, Loss: {loss.item():.4f}")

# Watch the training loop
ds_integration = DeepSpeedIntegration(doctor)
watched_train = ds_integration.watch(train)
watched_train(engine, dataloader, epochs=5)

# Get recommendations
recommendations = doctor.get_recommendations()
print("Recommendations:")
for rec in recommendations:
    print(f"- {rec['message']}")

# Visualize results
doctor.visualize()

# Ask questions
response = doctor.ask("How is ZeRO optimization affecting my training?")
print(response)
```

### TorchDynamo Example

```python
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import DataLoader, TensorDataset
from autopd import Doctor
from autopd.integrations import TorchDynamoIntegration

# Create a synthetic dataset
x = torch.randn(1000, 20)
y = torch.randint(0, 2, (1000,))
dataset = TensorDataset(x, y)
dataloader = DataLoader(dataset, batch_size=32, shuffle=True)

# Define a model
class SimpleModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.layer1 = nn.Linear(20, 64)
        self.layer2 = nn.Linear(64, 32)
        self.layer3 = nn.Linear(32, 2)
        
    def forward(self, x):
        x = F.relu(self.layer1(x))
        x = F.dropout(x, 0.2)
        x = F.relu(self.layer2(x))
        x = self.layer3(x)
        return x

# Initialize model
model = SimpleModel()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

# Initialize AutoPipelineDoctor
doctor = Doctor(model, optimizer, dataloader)

# Enable TorchDynamo monitoring
TorchDynamoIntegration.enable_monitoring(doctor)

# Compile the model
compiled_model = torch.compile(model, backend="inductor")

# Training loop
def train(model, optimizer, dataloader, epochs=10):
    for epoch in range(epochs):
        for batch_idx, (data, target) in enumerate(dataloader):
            optimizer.zero_grad()
            output = model(data)
            loss = F.cross_entropy(output, target)
            loss.backward()
            optimizer.step()
            
            if batch_idx % 10 == 0:
                print(f"Epoch: {epoch}, Batch: {batch_idx}, Loss: {loss.item():.4f}")

# Watch the training loop
watched_train = doctor.watch(train)
watched_train(compiled_model, optimizer, dataloader, epochs=5)

# Get recommendations
recommendations = doctor.get_recommendations()
print("Recommendations:")
for rec in recommendations:
    print(f"- {rec['message']}")

# Visualize results
doctor.visualize()

# Ask questions
response = doctor.ask("How did compilation affect my model's performance?")
print(response)
```

## Best Practices

### Memory Optimization

1. **Start with a smaller batch size** and let AutoPipelineDoctor suggest optimal increases.
2. **Enable gradient checkpointing** for large models to trade computation for memory.
3. **Use mixed precision training** (AMP) for significant memory savings with minimal accuracy impact.
4. **Monitor memory fragmentation** and periodically empty the cache for long training runs.

### Performance Optimization

1. **Optimize dataloader workers** based on AutoPipelineDoctor's suggestions.
2. **Use torch.compile** with AutoPipelineDoctor monitoring to find the best backend.
3. **Balance batch size and gradient accumulation** for optimal throughput.
4. **Consider DeepSpeed integration** for distributed training with ZeRO optimization.

### Training Stability

1. **Watch gradient statistics** to detect vanishing or exploding gradients early.
2. **Monitor loss curves** for signs of overfitting or underfitting.
3. **Use AutoPipelineDoctor's failure forecasting** to prevent OOM errors before they happen.
4. **Leverage historical run data** to avoid repeating past mistakes.

## Troubleshooting

### Common Issues

1. **Out-of-memory errors**: Follow AutoPipelineDoctor's recommendations for memory optimization.
2. **Slow training**: Check the timing breakdown to identify bottlenecks.
3. **Vanishing/exploding gradients**: Use gradient clipping and proper initialization.
4. **Dataloader bottlenecks**: Optimize worker count and prefetching.

### Debugging Tips

1. **Use doctor.ask()** for natural language explanations of issues.
2. **Check doctor.visualize()** for visual insights into performance bottlenecks.
3. **Review doctor.get_recommendations()** for actionable suggestions.
4. **Examine doctor.save_report()** for comprehensive analysis.

## Contributing

Contributions to AutoPipelineDoctor are welcome! Please see our [contributing guidelines](https://github.com/your-username/autopd/blob/main/CONTRIBUTING.md) for more information.

## License

AutoPipelineDoctor is licensed under the MIT License. See the [LICENSE](https://github.com/your-username/autopd/blob/main/LICENSE) file for more information.
