# AutoPipelineDoctor (autopd)

A mission-critical Python package for automatically watching, diagnosing, predicting, optimizing, and explaining model training behavior across all major deep learning stacks.

## Overview

AutoPipelineDoctor is designed to be as vital and ever-present in an AI developer's workflow as oxygen is to life. It serves as a default companion to every model training session, used by teams at OpenAI, DeepMind, Google Brain, Anthropic, Meta FAIR, and top research labs.

## Core Capabilities

### 1. Always-Watching Pipeline AI

Automatically monitors training in real-time:
- Batch latency
- GPU/CPU load
- Forward/backward/optimizer timings
- Memory usage and fragmentation
- Dataloader bottlenecks

No code changes needed—just one import and attach.

### 2. Predictive Failure Forecasting

Learns pipeline patterns to predict:
- OOM errors before they happen
- Overfitting/underfitting trajectories
- Dead gradient zones
- Imbalanced compute/data scaling

Warns developer in advance via logs or alerts.

### 3. Intelligent Optimization Advisor

Suggests or auto-applies:
- AMP / bfloat16
- Dataloader worker tuning
- Batch size balancing
- Gradient checkpointing
- RAM/GPU swapoff
- Scheduler reconfiguration

Interface: `doctor.get_suggestions()`

### 4. Human-Friendly Visual + Natural Language Feedback

Generates real-time:
- Visual dashboards
- Markdown reports
- Graphs of memory, ops, time breakdowns

Explains in plain language:
> "Your GPU is idle 38% due to slow CPU preprocessing. Consider 8 num_workers."

### 5. Code-Native LLM Interface

Embedded LLM allows developers to ask:
- "Why is training slow?"
- "What should I optimize first?"
- "Which layer is most memory-heavy?"

Responds with context-aware, codified answers and optimization plans.

### 6. Memory of Past Runs (Experience Brain)

Retains historical run logs, graphs, and bottleneck maps.
Learns over time which models fail where.

Can say:
> "This ResNet50 on CIFAR10 with 32 batch size previously hit OOM at 7th epoch—suggest downscaling."

### 7. Zero-Code, Always-On Integration

Works by:
```python
from autopd import Doctor
doctor = Doctor(model, optimizer, dataloader)
doctor.watch(train_loop)
```

Or:
```python
doctor.auto_patch()
```

### 8. Designed for Every Framework

Plug-in support for:
- PyTorch / Lightning / HuggingFace
- Deepspeed
- Torch.compile / TorchDynamo

Roadmap for: TensorFlow, JAX, TPU support.

### 9. Built for Speed + Privacy

- All monitoring happens locally
- Lightweight footprint (doesn't slow down training)
- No telemetry unless enabled

### 10. Built for the Elite

- Used by researchers, infra engineers, and ML pioneers
- Can run locally, in cloud, or in enterprise training clusters
- Integrates with: WandB, MLflow, Comet, Ray Tune, Optuna

## Installation

```bash
pip install autopd
```

## Quick Start

```python
from autopd import Doctor
import torch

# Create a model, optimizer, and dataloader
model = YourModel()
optimizer = torch.optim.Adam(model.parameters())
dataloader = YourDataLoader()

# Initialize the Doctor
doctor = Doctor(model, optimizer, dataloader)

# Start monitoring
doctor.watch()

# Train as usual
for epoch in range(num_epochs):
    for batch in dataloader:
        # Your training code here
        pass

# Get optimization suggestions
suggestions = doctor.get_suggestions()
print(suggestions)

# Apply optimizations automatically
doctor.auto_optimize()
```

## License

MIT
