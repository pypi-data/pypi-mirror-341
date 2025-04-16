# AutoPipelineDoctor Usage Guide

## Introduction

AutoPipelineDoctor (autopd) is a sophisticated Python library designed to automatically monitor, diagnose, predict, optimize, and explain model training behavior across all major deep learning frameworks. This guide will walk you through the basic and advanced usage of the library.

## Basic Usage

### Installation

```bash
pip install autopd
```

### Quick Start with PyTorch

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

# Get insights and recommendations
doctor.visualize()
recommendations = doctor.get_recommendations()
```

### Option 2: Auto-Patch

```python
# Initialize AutoPipelineDoctor
doctor = Doctor()

# Auto-patch your training components
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
```

## Core Features

### Real-Time Monitoring

AutoPipelineDoctor continuously monitors your training process, collecting metrics on:

- Hardware utilization (CPU/GPU)
- Memory usage and fragmentation
- Execution timing (forward/backward/optimizer)
- Gradient statistics
- Dataloader performance

```python
# Get current metrics
metrics = doctor.get_metrics()
print(metrics)

# Monitor specific categories
memory_metrics = doctor.memory_profiler.get_metrics()
timing_metrics = doctor.timing_profiler.get_metrics()
```

### Predictive Failure Forecasting

The library can predict potential failures before they happen:

```python
# Get active warnings
warnings = doctor.get_warnings()
for warning in warnings:
    print(f"{warning['severity']}: {warning['message']}")
    print(f"Details: {warning['details']}")
    
# Check for specific issues
oom_prediction = doctor.memory_profiler.predict_oom()
if oom_prediction['risk_level'] > 0.7:
    print(f"OOM risk detected: {oom_prediction['details']}")
```

### Optimization Recommendations

AutoPipelineDoctor provides intelligent optimization suggestions:

```python
# Get recommendations
recommendations = doctor.get_recommendations()
for rec in recommendations:
    print(f"{rec['category']}: {rec['message']}")
    
# Apply all recommendations
doctor.apply_recommendations()

# Apply specific recommendations
doctor.apply_recommendations([recommendations[0], recommendations[2]])

# Set optimization level
doctor.optimization_advisor.set_optimization_level("aggressive")  # Options: conservative, balanced, aggressive
```

### Visualization

Generate visual insights into your training process:

```python
# Create a dashboard
dashboard_path = doctor.visualize(output_path="./dashboard")

# Create specific visualizations
doctor.visualizer.plot_memory_usage(output_path="./memory_usage.png")
doctor.visualizer.plot_timing_breakdown(output_path="./timing.png")
doctor.visualizer.plot_gradient_statistics(output_path="./gradients.png")

# Create a custom visualization
metrics_to_plot = {
    "train_loss": doctor.get_metrics_history("train_loss"),
    "val_loss": doctor.get_metrics_history("val_loss"),
    "learning_rate": doctor.get_metrics_history("learning_rate")
}
doctor.visualizer.plot_custom(metrics_to_plot, output_path="./training_progress.png")
```

### Natural Language Interface

Interact with AutoPipelineDoctor using natural language:

```python
# Ask questions about your training
response = doctor.ask("Why is my training so slow?")
print(response)

response = doctor.ask("How can I reduce memory usage?")
print(response)

response = doctor.ask("What's causing the spikes in my loss?")
print(response)

# Generate a natural language report
report = doctor.llm_assistant.generate_report()
print(report)
```

### Historical Run Memory

AutoPipelineDoctor learns from past training runs:

```python
# Start a new run with metadata
doctor.experience_brain.start(
    model_info={"name": "ResNet50", "dataset": "CIFAR10"},
    hardware_info={"gpu": "RTX 3090", "memory": "24GB"}
)

# Get similar past runs
similar_runs = doctor.experience_brain.get_similar_runs(limit=3)
for run in similar_runs:
    print(f"Run ID: {run.id}")
    print(f"Model: {run.model_info['name']}")
    print(f"Status: {run.status}")
    print(f"Warnings: {len(run.warnings)}")

# Make predictions based on history
predictions = doctor.experience_brain.predict_from_history()
print(f"Predicted training time: {predictions['estimated_time']} hours")
print(f"Potential issues: {predictions['potential_issues']}")
```

## Framework Integrations

### PyTorch Lightning

```python
import pytorch_lightning as pl
from autopd import Doctor
from autopd.integrations import LightningIntegration

# Initialize AutoPipelineDoctor
doctor = Doctor()

# Get Lightning integration
lightning_integration = LightningIntegration(doctor)

# Option 1: Create a trainer with monitoring
trainer = lightning_integration.create_trainer_with_monitoring(
    doctor,
    max_epochs=10,
    gpus=1
)

# Option 2: Patch an existing trainer
trainer = pl.Trainer(max_epochs=10, gpus=1)
trainer = lightning_integration.patch_trainer(trainer, doctor)

# Train as usual
trainer.fit(model, train_dataloader, val_dataloader)
```

### HuggingFace Transformers

```python
from transformers import Trainer, TrainingArguments
from autopd import Doctor
from autopd.integrations import HuggingFaceIntegration

# Initialize AutoPipelineDoctor
doctor = Doctor()

# Get HuggingFace integration
hf_integration = HuggingFaceIntegration(doctor)

# Option 1: Create a trainer with monitoring
training_args = TrainingArguments(output_dir="./results", num_train_epochs=3)
trainer = hf_integration.create_trainer_with_monitoring(
    doctor,
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=eval_dataset
)

# Option 2: Patch an existing trainer
trainer = Trainer(model=model, args=training_args, train_dataset=train_dataset)
trainer = hf_integration.patch_trainer(trainer, doctor)

# Train as usual
trainer.train()
```

### DeepSpeed

```python
import deepspeed
from autopd import Doctor
from autopd.integrations import DeepSpeedIntegration

# Initialize AutoPipelineDoctor
doctor = Doctor()

# Option 1: Initialize DeepSpeed with monitoring
ds_config = {
    "train_batch_size": 32,
    "fp16": {"enabled": True},
    "zero_optimization": {"stage": 1}
}
engine = DeepSpeedIntegration.initialize_with_monitoring(
    model=model,
    config=ds_config,
    doctor=doctor
)

# Option 2: Patch an existing engine
engine = deepspeed.initialize(model=model, config=ds_config)
engine = DeepSpeedIntegration.patch_engine(engine, doctor)

# Option 3: Watch a training function
ds_integration = DeepSpeedIntegration(doctor)
watched_train = ds_integration.watch(train_function)
watched_train(engine, dataloader)
```

### TorchDynamo and torch.compile

```python
import torch
from autopd import Doctor
from autopd.integrations import TorchDynamoIntegration

# Initialize AutoPipelineDoctor
doctor = Doctor(model, optimizer, dataloader)

# Enable TorchDynamo monitoring
TorchDynamoIntegration.enable_monitoring(doctor)

# Compile your model as usual
compiled_model = torch.compile(model, backend="inductor")

# Train with the compiled model
train_loop(compiled_model, optimizer, dataloader)
```

## Advanced Configuration

### Custom Configuration

```python
# Initialize with custom configuration
config = {
    "monitoring": {
        "interval": 0.5,  # Monitoring interval in seconds
        "metrics": ["memory", "timing", "gradients", "dataloader"],
        "log_level": "info"
    },
    "optimization": {
        "level": "balanced",  # conservative, balanced, aggressive
        "auto_apply": False,
        "categories": ["memory", "performance", "stability"]
    },
    "visualization": {
        "dashboard_type": "plotly",  # plotly, matplotlib
        "update_interval": 5.0,
        "max_history": 1000
    },
    "llm": {
        "provider": "openai",
        "model": "gpt-4",
        "api_key": "your_api_key"  # Optional, can also use environment variable
    },
    "memory": {
        "storage_path": "./autopd_runs",
        "max_runs": 100,
        "retention_days": 30
    }
}

doctor = Doctor(config=config)
```

### Custom Hooks

```python
# Register custom metric collectors
def custom_metric_collector():
    return {"my_custom_metric": calculate_something()}

doctor.register_metric_collector(custom_metric_collector)

# Register custom warning detector
def custom_warning_detector(metrics):
    if metrics.get("my_custom_metric", 0) > threshold:
        return {
            "type": "custom_warning",
            "message": "Custom threshold exceeded",
            "details": f"Value: {metrics['my_custom_metric']}",
            "severity": "medium"
        }
    return None

doctor.register_warning_detector(custom_warning_detector)

# Register custom optimization suggester
def custom_optimization_suggester(metrics):
    if condition_met(metrics):
        return {
            "type": "custom_optimization",
            "message": "Try this custom optimization",
            "details": "This will improve X by doing Y",
            "apply_func": lambda: apply_my_optimization()
        }
    return None

doctor.register_optimization_suggester(custom_optimization_suggester)
```

### Distributed Training

```python
# Initialize with distributed training configuration
config = {
    "distributed": {
        "enabled": True,
        "rank": dist.get_rank(),
        "world_size": dist.get_world_size(),
        "master_only": ["visualization", "llm", "memory"],
        "sync_interval": 10.0
    }
}

doctor = Doctor(config=config)

# Use as usual in your distributed training script
```

## Best Practices

### Memory Optimization

1. Start with conservative memory settings and let AutoPipelineDoctor guide you:

```python
doctor.optimization_advisor.set_optimization_level("conservative")
recommendations = doctor.get_recommendations(category="memory")
doctor.apply_recommendations(recommendations)
```

2. For large models, enable gradient checkpointing early:

```python
from autopd.optimizations import enable_gradient_checkpointing
enable_gradient_checkpointing(model)
```

3. Use mixed precision training when possible:

```python
from autopd.optimizations import enable_amp
enable_amp(model, optimizer)
```

### Performance Optimization

1. Optimize dataloader workers:

```python
optimal_workers = doctor.dataloader_profiler.optimize_workers()
dataloader = DataLoader(dataset, batch_size=32, num_workers=optimal_workers)
```

2. Find the optimal batch size:

```python
optimal_batch_size = doctor.optimization_advisor.find_optimal_batch_size()
dataloader = DataLoader(dataset, batch_size=optimal_batch_size)
```

3. Use torch.compile with monitoring:

```python
TorchDynamoIntegration.enable_monitoring(doctor)
compiled_model = torch.compile(model, backend="inductor")
```

### Training Stability

1. Monitor gradient statistics:

```python
gradient_issues = doctor.gradient_profiler.detect_issues()
if gradient_issues:
    print(f"Gradient issues detected: {gradient_issues}")
```

2. Watch for overfitting:

```python
doctor.experience_brain.add_warning_detector("overfitting", threshold=0.2)
```

3. Use early stopping based on AutoPipelineDoctor's predictions:

```python
if doctor.get_warnings(type="overfitting"):
    print("Early stopping due to overfitting risk")
    break
```

## Troubleshooting

### Common Issues

1. **Out-of-memory errors**:

```python
# Check memory usage
memory_metrics = doctor.memory_profiler.get_metrics()
print(f"Model size: {memory_metrics['model_size_mb']} MB")
print(f"Peak memory: {memory_metrics['peak_memory_mb']} MB")
print(f"Available memory: {memory_metrics['available_memory_mb']} MB")

# Apply memory optimizations
doctor.apply_recommendations(category="memory")
```

2. **Slow training**:

```python
# Check timing breakdown
timing_metrics = doctor.timing_profiler.get_metrics()
print(f"Forward time: {timing_metrics['forward_time']} s")
print(f"Backward time: {timing_metrics['backward_time']} s")
print(f"Optimizer time: {timing_metrics['optimizer_time']} s")
print(f"Dataloader time: {timing_metrics['dataloader_time']} s")

# Identify bottlenecks
bottlenecks = doctor.timing_profiler.identify_bottlenecks()
for bottleneck in bottlenecks:
    print(f"Bottleneck: {bottleneck['component']}, Impact: {bottleneck['impact']}")
```

3. **Gradient issues**:

```python
# Check gradient statistics
gradient_metrics = doctor.gradient_profiler.get_metrics()
print(f"Gradient norm: {gradient_metrics['avg_grad_norm']}")
print(f"Zero gradients: {gradient_metrics['zero_gradients_pct']}%")

# Apply gradient clipping
from autopd.optimizations import apply_gradient_clipping
apply_gradient_clipping(optimizer, max_norm=1.0)
```

### Getting Help

When all else fails, ask AutoPipelineDoctor directly:

```python
response = doctor.ask("I'm having trouble with my training. It's slow and keeps running out of memory. What should I do?")
print(response)

# Generate a comprehensive report
report_path = doctor.save_report(output_path="./training_report.md")
print(f"Report saved to: {report_path}")
```

## Conclusion

AutoPipelineDoctor is designed to be an essential companion for AI developers, providing real-time insights, predictions, and optimizations for your training pipelines. By following this guide, you can leverage its full potential to make your training more efficient, stable, and successful.

For more detailed information, refer to the [API Reference](api_reference.md) and [Examples](examples.md) documentation.
