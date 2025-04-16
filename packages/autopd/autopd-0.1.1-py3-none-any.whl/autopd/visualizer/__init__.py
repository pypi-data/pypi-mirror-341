"""
Visualizer module for AutoPipelineDoctor.
"""

from typing import Dict, List, Optional, Any, Union
import logging
import os
import time
import json
import matplotlib.pyplot as plt
import numpy as np
import torch
import torch.nn as nn

logger = logging.getLogger(__name__)

class Visualizer:
    """
    Creates visualizations of training metrics and performance data.
    
    This class generates interactive dashboards, static plots, and visual reports
    to help understand model training behavior.
    """
    
    def __init__(self, output_dir: Optional[str] = None):
        """
        Initialize the visualizer.
        
        Args:
            output_dir: Directory to save visualizations
        """
        if output_dir is None:
            self.output_dir = os.path.join(os.getcwd(), 'autopd_visualizations')
        else:
            self.output_dir = output_dir
        
        # Create output directory if it doesn't exist
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Set default plot style
        plt.style.use('seaborn-v0_8-darkgrid')
    
    def plot_metrics(self, metrics: Dict[str, List[Dict[str, Any]]], metric_name: str, 
                    output_file: Optional[str] = None, title: Optional[str] = None,
                    x_key: str = 'timestamp', category: Optional[str] = None) -> str:
        """
        Plot a specific metric over time.
        
        Args:
            metrics: Dictionary of metrics
            metric_name: Name of the metric to plot
            output_file: Path to save the plot
            title: Plot title
            x_key: Key to use for x-axis
            category: Category of metrics to use
            
        Returns:
            Path to the saved plot
        """
        plt.figure(figsize=(10, 6))
        
        if category is None:
            # Try to find the metric in any category
            for cat, cat_metrics in metrics.items():
                if cat_metrics and metric_name in cat_metrics[0]:
                    category = cat
                    break
        
        if category is None or category not in metrics or not metrics[category]:
            logger.warning(f"Metric {metric_name} not found in any category")
            plt.close()
            return ""
        
        # Extract data
        x_values = []
        y_values = []
        
        for m in metrics[category]:
            if metric_name in m and x_key in m:
                x_values.append(m[x_key])
                y_values.append(m[metric_name])
        
        if not x_values:
            logger.warning(f"No data found for metric {metric_name} in category {category}")
            plt.close()
            return ""
        
        # Convert timestamps to relative time if needed
        if x_key == 'timestamp':
            start_time = min(x_values)
            x_values = [(x - start_time) / 60 for x in x_values]  # Convert to minutes
            plt.xlabel('Time (minutes)')
        else:
            plt.xlabel(x_key.replace('_', ' ').title())
        
        # Plot data
        plt.plot(x_values, y_values, marker='o', linestyle='-', markersize=4)
        
        # Set labels and title
        plt.ylabel(metric_name.replace('_', ' ').title())
        if title:
            plt.title(title)
        else:
            plt.title(f"{metric_name.replace('_', ' ').title()} over {x_key.replace('_', ' ').title()}")
        
        plt.grid(True)
        plt.tight_layout()
        
        # Save plot
        if output_file:
            if not output_file.endswith('.png'):
                output_file += '.png'
            
            output_path = os.path.join(self.output_dir, output_file)
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            logger.info(f"Plot saved to {output_path}")
            
            plt.close()
            return output_path
        else:
            # Generate a default filename
            timestamp = int(time.time())
            output_file = f"{metric_name}_{timestamp}.png"
            output_path = os.path.join(self.output_dir, output_file)
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            logger.info(f"Plot saved to {output_path}")
            
            plt.close()
            return output_path
    
    def plot_loss_curve(self, metrics: Dict[str, List[Dict[str, Any]]], 
                       output_file: Optional[str] = None) -> str:
        """
        Plot training loss curve.
        
        Args:
            metrics: Dictionary of metrics
            output_file: Path to save the plot
            
        Returns:
            Path to the saved plot
        """
        # Extract loss values from batch metrics
        if 'batch' not in metrics or not metrics['batch']:
            logger.warning("No batch metrics found for loss curve")
            return ""
        
        iterations = []
        losses = []
        
        for m in metrics['batch']:
            if 'iteration' in m and 'loss' in m:
                iterations.append(m['iteration'])
                losses.append(m['loss'])
        
        if not iterations:
            logger.warning("No loss data found in batch metrics")
            return ""
        
        # Create plot
        plt.figure(figsize=(10, 6))
        plt.plot(iterations, losses, marker='o', linestyle='-', markersize=4, alpha=0.7)
        
        # Add smoothed line
        if len(losses) > 10:
            window_size = min(10, len(losses) // 5)
            smoothed_losses = np.convolve(losses, np.ones(window_size) / window_size, mode='valid')
            smoothed_iterations = iterations[window_size-1:]
            plt.plot(smoothed_iterations, smoothed_losses, 'r-', linewidth=2, label='Smoothed Loss')
            plt.legend()
        
        plt.xlabel('Iteration')
        plt.ylabel('Loss')
        plt.title('Training Loss Curve')
        plt.grid(True)
        plt.tight_layout()
        
        # Save plot
        if output_file:
            if not output_file.endswith('.png'):
                output_file += '.png'
        else:
            output_file = f"loss_curve_{int(time.time())}.png"
        
        output_path = os.path.join(self.output_dir, output_file)
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        logger.info(f"Loss curve saved to {output_path}")
        
        plt.close()
        return output_path
    
    def plot_memory_usage(self, metrics: Dict[str, List[Dict[str, Any]]], 
                         output_file: Optional[str] = None) -> str:
        """
        Plot memory usage over time.
        
        Args:
            metrics: Dictionary of metrics
            output_file: Path to save the plot
            
        Returns:
            Path to the saved plot
        """
        if 'memory' not in metrics or not metrics['memory']:
            logger.warning("No memory metrics found")
            return ""
        
        # Extract memory data
        timestamps = []
        allocated = []
        reserved = []
        
        for m in metrics['memory']:
            if 'timestamp' in m:
                timestamps.append(m['timestamp'])
                allocated.append(m.get('allocated', 0) / (1024 * 1024))  # Convert to MB
                reserved.append(m.get('reserved', 0) / (1024 * 1024))  # Convert to MB
        
        if not timestamps:
            logger.warning("No timestamp data found in memory metrics")
            return ""
        
        # Convert timestamps to relative time
        start_time = min(timestamps)
        rel_times = [(t - start_time) / 60 for t in timestamps]  # Convert to minutes
        
        # Create plot
        plt.figure(figsize=(10, 6))
        
        if allocated:
            plt.plot(rel_times, allocated, 'b-', label='Allocated Memory (MB)')
        
        if reserved:
            plt.plot(rel_times, reserved, 'r-', label='Reserved Memory (MB)')
        
        plt.xlabel('Time (minutes)')
        plt.ylabel('Memory (MB)')
        plt.title('GPU Memory Usage Over Time')
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        
        # Save plot
        if output_file:
            if not output_file.endswith('.png'):
                output_file += '.png'
        else:
            output_file = f"memory_usage_{int(time.time())}.png"
        
        output_path = os.path.join(self.output_dir, output_file)
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        logger.info(f"Memory usage plot saved to {output_path}")
        
        plt.close()
        return output_path
    
    def plot_timing_breakdown(self, metrics: Dict[str, List[Dict[str, Any]]], 
                             output_file: Optional[str] = None) -> str:
        """
        Plot timing breakdown of training operations.
        
        Args:
            metrics: Dictionary of metrics
            output_file: Path to save the plot
            
        Returns:
            Path to the saved plot
        """
        if 'timing' not in metrics or not metrics['timing']:
            logger.warning("No timing metrics found")
            return ""
        
        # Find all timing keys
        timing_keys = []
        for m in metrics['timing']:
            for key in m.keys():
                if key.endswith('_time') and key not in ['timestamp', 'iteration']:
                    if key not in timing_keys:
                        timing_keys.append(key)
        
        if not timing_keys:
            logger.warning("No timing data found in timing metrics")
            return ""
        
        # Calculate average times
        avg_times = {}
        for key in timing_keys:
            values = [m[key] for m in metrics['timing'] if key in m]
            if values:
                avg_times[key] = sum(values) / len(values)
        
        if not avg_times:
            logger.warning("Could not calculate average times")
            return ""
        
        # Create bar plot
        plt.figure(figsize=(10, 6))
        
        # Sort by time
        sorted_items = sorted(avg_times.items(), key=lambda x: x[1], reverse=True)
        labels = [k.replace('_time', '').replace('_', ' ').title() for k, v in sorted_items]
        values = [v for k, v in sorted_items]
        
        bars = plt.bar(labels, values, color='skyblue')
        
        # Add values on top of bars
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height + 0.001,
                    f'{height:.3f}s',
                    ha='center', va='bottom', rotation=0)
        
        plt.xlabel('Operation')
        plt.ylabel('Average Time (seconds)')
        plt.title('Timing Breakdown of Training Operations')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        
        # Save plot
        if output_file:
            if not output_file.endswith('.png'):
                output_file += '.png'
        else:
            output_file = f"timing_breakdown_{int(time.time())}.png"
        
        output_path = os.path.join(self.output_dir, output_file)
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        logger.info(f"Timing breakdown plot saved to {output_path}")
        
        plt.close()
        return output_path
    
    def plot_gradient_statistics(self, metrics: Dict[str, List[Dict[str, Any]]], 
                               output_file: Optional[str] = None) -> str:
        """
        Plot gradient statistics over time.
        
        Args:
            metrics: Dictionary of metrics
            output_file: Path to save the plot
            
        Returns:
            Path to the saved plot
        """
        if 'gradients' not in metrics or not metrics['gradients']:
            logger.warning("No gradient metrics found")
            return ""
        
        # Extract gradient data
        timestamps = []
        avg_norms = []
        max_values = []
        zero_percents = []
        
        for m in metrics['gradients']:
            if 'timestamp' in m and 'avg_grad_norm' in m:
                timestamps.append(m['timestamp'])
                avg_norms.append(m['avg_grad_norm'])
                max_values.append(m.get('max_grad_value', 0))
                zero_percents.append(m.get('zero_grad_percent', 0) * 100)  # Convert to percentage
        
        if not timestamps:
            logger.warning("No timestamp data found in gradient metrics")
            return ""
        
        # Convert timestamps to relative time
        start_time = min(timestamps)
        rel_times = [(t - start_time) / 60 for t in timestamps]  # Convert to minutes
        
        # Create plot with two y-axes
        fig, ax1 = plt.subplots(figsize=(10, 6))
        
        # Plot gradient norms
        color = 'tab:blue'
        ax1.set_xlabel('Time (minutes)')
        ax1.set_ylabel('Gradient Norm', color=color)
        ax1.plot(rel_times, avg_norms, color=color, marker='o', linestyle='-', markersize=4, label='Avg Gradient Norm')
        ax1.tick_params(axis='y', labelcolor=color)
        
        # Create second y-axis
        ax2 = ax1.twinx()
        color = 'tab:red'
        ax2.set_ylabel('Zero Gradients (%)', color=color)
        ax2.plot(rel_times, zero_percents, color=color, marker='s', linestyle='-', markersize=4, label='Zero Gradients (%)')
        ax2.tick_params(axis='y', labelcolor=color)
        
        # Add legend
        lines1, labels1 = ax1.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left')
        
        plt.title('Gradient Statistics Over Time')
        plt.grid(True)
        fig.tight_layout()
        
        # Save plot
        if output_file:
            if not output_file.endswith('.png'):
                output_file += '.png'
        else:
            output_file = f"gradient_stats_{int(time.time())}.png"
        
        output_path = os.path.join(self.output_dir, output_file)
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        logger.info(f"Gradient statistics plot saved to {output_path}")
        
        plt.close()
        return output_path
    
    def create_dashboard(self, metrics: Dict[str, List[Dict[str, Any]]], 
                        output_file: Optional[str] = None) -> str:
        """
        Create a comprehensive dashboard with multiple plots.
        
        Args:
            metrics: Dictionary of metrics
            output_file: Path to save the dashboard
            
        Returns:
            Path to the saved dashboard
        """
        # Create individual plots
        plots = []
        
        # Loss curve
        loss_plot = self.plot_loss_curve(metrics, 'loss_curve.png')
        if loss_plot:
            plots.append(('Loss Curve', loss_plot))
        
        # Memory usage
        memory_plot = self.plot_memory_usage(metrics, 'memory_usage.png')
        if memory_plot:
            plots.append(('Memory Usage', memory_plot))
        
        # Timing breakdown
        timing_plot = self.plot_timing_breakdown(metrics, 'timing_breakdown.png')
        if timing_plot:
            plots.append(('Timing Breakdown', timing_plot))
        
        # Gradient statistics
        gradient_plot = self.plot_gradient_statistics(metrics, 'gradient_stats.png')
        if gradient_plot:
            plots.append(('Gradient Statistics', gradient_plot))
        
        if not plots:
            logger.warning("No plots created for dashboard")
            return ""
        
        # Create HTML dashboard
        if output_file:
            if not output_file.endswith('.html'):
                output_file += '.html'
        else:
            output_file = f"dashboard_{int(time.time())}.html"
        
        output_path = os.path.join(self.output_dir, output_file)
        
        with open(output_path, 'w') as f:
            f.write("""
            <!DOCTYPE html>
            <html>
            <head>
                <title>AutoPipelineDoctor Dashboard</title>
                <style>
                    body {
                        font-family: Arial, sans-serif;
                        margin: 0;
                        padding: 20px;
                        background-color: #f5f5f5;
                    }
                    .container {
                        max-width: 1200px;
                        margin: 0 auto;
                    }
                    .header {
                        background-color: #4CAF50;
                        color: white;
                        padding: 20px;
                        text-align: center;
                        margin-bottom: 20px;
                        border-radius: 5px;
                    }
                    .plot-container {
                        background-color: white;
                        padding: 20px;
                        margin-bottom: 20px;
                        border-radius: 5px;
                        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                    }
                    .plot-title {
                        font-size: 18px;
                        font-weight: bold;
                        margin-bottom: 10px;
                        color: #333;
                    }
                    .plot-image {
                        width: 100%;
                        height: auto;
                        border: 1px solid #ddd;
                    }
                    .footer {
                        text-align: center;
                        margin-top: 20px;
                        color: #666;
                        font-size: 14px;
                    }
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>AutoPipelineDoctor Dashboard</h1>
                        <p>Generated on """ + time.strftime("%Y-%m-%d %H:%M:%S") + """</p>
                    </div>
            """)
            
            for title, plot_path in plots:
                # Get relative path
                rel_path = os.path.basename(plot_path)
                
                f.write(f"""
                    <div class="plot-container">
                        <div class="plot-title">{title}</div>
                        <img class="plot-image" src="{rel_path}" alt="{title}">
                    </div>
                """)
            
            f.write("""
                    <div class="footer">
                        <p>Powered by AutoPipelineDoctor</p>
                    </div>
                </div>
            </body>
            </html>
            """)
        
        logger.info(f"Dashboard saved to {output_path}")
        return output_path
    
    def export_metrics_to_json(self, metrics: Dict[str, List[Dict[str, Any]]], 
                              output_file: Optional[str] = None) -> str:
        """
        Export metrics to JSON file.
        
        Args:
            metrics: Dictionary of metrics
            output_file: Path to save the JSON file
            
        Returns:
            Path to the saved JSON file
        """
        if output_file:
            if not output_file.endswith('.json'):
                output_file += '.json'
        else:
            output_file = f"metrics_{int(time.time())}.json"
        
        output_path = os.path.join(self.output_dir, output_file)
        
        # Convert any non-serializable objects to strings
        serializable_metrics = {}
        for category, category_metrics in metrics.items():
            serializable_metrics[category] = []
            for m in category_metrics:
                serializable_m = {}
                for k, v in m.items():
                    if isinstance(v, (int, float, str, bool, type(None))):
                        serializable_m[k] = v
                    else:
                        serializable_m[k] = str(v)
                serializable_metrics[category].append(serializable_m)
        
        with open(output_path, 'w') as f:
            json.dump(serializable_metrics, f, indent=2)
        
        logger.info(f"Metrics exported to {output_path}")
        return output_path

class NaturalLanguageExplainer:
    """
    Provides human-friendly explanations of metrics and performance data.
    
    This class generates natural language explanations of training behavior,
    bottlenecks, and optimization suggestions.
    """
    
    def __init__(self):
        """Initialize the natural language explainer."""
        pass
    
    def explain_memory_usage(self, metrics: Dict[str, List[Dict[str, Any]]]) -> str:
        """
        Generate explanation of memory usage.
        
        Args:
            metrics: Dictionary of metrics
            
        Returns:
            Natural language explanation
        """
        if 'memory' not in metrics or not metrics['memory']:
            return "No memory metrics available for analysis."
        
        memory_metrics = metrics['memory']
        
        # Calculate statistics
        if 'allocated' in memory_metrics[0]:
            allocated_values = [m['allocated'] for m in memory_metrics if 'allocated' in m]
            max_allocated = max(allocated_values)
            avg_allocated = sum(allocated_values) / len(allocated_values)
            
            # Get total memory if available
            if 'total' in memory_metrics[0]:
                total_memory = memory_metrics[0]['total']
                max_usage_percent = max_allocated / total_memory * 100
                
                explanation = f"Memory usage peaked at {max_allocated / (1024 * 1024):.2f} MB, "
                explanation += f"which is {max_usage_percent:.1f}% of the available {total_memory / (1024 * 1024 * 1024):.2f} GB. "
                
                if max_usage_percent > 90:
                    explanation += "This is very high memory usage, indicating potential risk of out-of-memory errors. "
                    explanation += "Consider using gradient checkpointing, mixed precision training, or reducing batch size."
                elif max_usage_percent > 70:
                    explanation += "This is moderately high memory usage. "
                    explanation += "For more efficient training, consider using mixed precision training."
                else:
                    explanation += "Memory usage is at a reasonable level."
            else:
                explanation = f"Memory usage peaked at {max_allocated / (1024 * 1024):.2f} MB, "
                explanation += f"with an average usage of {avg_allocated / (1024 * 1024):.2f} MB."
        else:
            explanation = "Memory metrics are available but don't contain allocation information."
        
        return explanation
    
    def explain_timing_breakdown(self, metrics: Dict[str, List[Dict[str, Any]]]) -> str:
        """
        Generate explanation of timing breakdown.
        
        Args:
            metrics: Dictionary of metrics
            
        Returns:
            Natural language explanation
        """
        if 'timing' not in metrics or not metrics['timing']:
            return "No timing metrics available for analysis."
        
        timing_metrics = metrics['timing']
        
        # Find all timing keys
        timing_keys = []
        for m in timing_metrics:
            for key in m.keys():
                if key.endswith('_time') and key not in ['timestamp', 'iteration']:
                    if key not in timing_keys:
                        timing_keys.append(key)
        
        if not timing_keys:
            return "Timing metrics are available but don't contain detailed timing information."
        
        # Calculate average times
        avg_times = {}
        for key in timing_keys:
            values = [m[key] for m in timing_metrics if key in m]
            if values:
                avg_times[key] = sum(values) / len(values)
        
        if not avg_times:
            return "Could not calculate average times from timing metrics."
        
        # Sort by time
        sorted_items = sorted(avg_times.items(), key=lambda x: x[1], reverse=True)
        
        # Calculate total time
        total_time = sum(avg_times.values())
        
        # Generate explanation
        explanation = "Timing breakdown analysis:\n\n"
        
        for key, value in sorted_items:
            operation = key.replace('_time', '').replace('_', ' ').title()
            percentage = value / total_time * 100
            explanation += f"- {operation}: {value:.3f} seconds ({percentage:.1f}% of total time)\n"
        
        # Identify bottlenecks
        if sorted_items:
            slowest_op = sorted_items[0]
            slowest_name = slowest_op[0].replace('_time', '').replace('_', ' ').title()
            slowest_percentage = slowest_op[1] / total_time * 100
            
            explanation += f"\nThe slowest operation is {slowest_name}, taking {slowest_percentage:.1f}% of the total time. "
            
            if 'forward' in slowest_op[0].lower():
                explanation += "To optimize forward pass performance, consider using torch.compile or channels_last memory format for CNN models."
            elif 'backward' in slowest_op[0].lower():
                explanation += "To optimize backward pass performance, consider using gradient checkpointing or mixed precision training."
            elif 'dataloader' in slowest_op[0].lower() or 'data' in slowest_op[0].lower():
                explanation += "To optimize data loading, consider increasing the number of dataloader workers or using pinned memory."
            elif 'optimizer' in slowest_op[0].lower():
                explanation += "To optimize optimizer performance, consider using a more efficient optimizer implementation or fused optimizers."
        
        return explanation
    
    def explain_gradient_statistics(self, metrics: Dict[str, List[Dict[str, Any]]]) -> str:
        """
        Generate explanation of gradient statistics.
        
        Args:
            metrics: Dictionary of metrics
            
        Returns:
            Natural language explanation
        """
        if 'gradients' not in metrics or not metrics['gradients']:
            return "No gradient metrics available for analysis."
        
        gradient_metrics = metrics['gradients']
        
        # Check for key metrics
        if 'avg_grad_norm' not in gradient_metrics[0]:
            return "Gradient metrics are available but don't contain norm information."
        
        # Extract data
        avg_norms = [m['avg_grad_norm'] for m in gradient_metrics if 'avg_grad_norm' in m]
        max_values = [m.get('max_grad_value', 0) for m in gradient_metrics if 'max_grad_value' in m]
        zero_percents = [m.get('zero_grad_percent', 0) * 100 for m in gradient_metrics if 'zero_grad_percent' in m]  # Convert to percentage
        
        if not avg_norms:
            return "Could not extract gradient norm data from metrics."
        
        # Calculate statistics
        avg_norm = sum(avg_norms) / len(avg_norms)
        max_norm = max(avg_norms)
        min_norm = min(avg_norms)
        
        # Generate explanation
        explanation = f"Gradient analysis shows an average gradient norm of {avg_norm:.2e}, "
        explanation += f"ranging from {min_norm:.2e} to {max_norm:.2e}. "
        
        # Check for potential issues
        if max_norm > 1e3:
            explanation += "There are signs of exploding gradients, which can destabilize training. "
            explanation += "Consider using gradient clipping or reducing the learning rate."
        elif max_norm < 1e-7:
            explanation += "There are signs of vanishing gradients, which can slow down or stall training. "
            explanation += "Consider using different activation functions (like LeakyReLU instead of ReLU) or a different initialization method."
        else:
            explanation += "Gradient magnitudes appear to be in a healthy range. "
        
        if zero_percents:
            avg_zero_percent = sum(zero_percents) / len(zero_percents)
            explanation += f"\n\nOn average, {avg_zero_percent:.1f}% of gradients are zero. "
            
            if avg_zero_percent > 50:
                explanation += "This high percentage of zero gradients suggests potential dead neurons or ReLU units. "
                explanation += "Consider using LeakyReLU instead of ReLU or checking for issues in your model architecture."
            elif avg_zero_percent > 20:
                explanation += "This moderate percentage of zero gradients is worth monitoring, but not necessarily problematic."
            else:
                explanation += "This is a normal amount of zero gradients."
        
        return explanation
    
    def explain_bottlenecks(self, bottlenecks: List[Dict[str, Any]]) -> str:
        """
        Generate explanation of detected bottlenecks.
        
        Args:
            bottlenecks: List of detected bottlenecks
            
        Returns:
            Natural language explanation
        """
        if not bottlenecks:
            return "No bottlenecks detected in the training process."
        
        explanation = f"Analysis detected {len(bottlenecks)} bottleneck(s) in your training process:\n\n"
        
        for i, bottleneck in enumerate(bottlenecks, 1):
            bottleneck_type = bottleneck.get('type', 'unknown')
            severity = bottleneck.get('severity', 'medium')
            message = bottleneck.get('message', 'No details available')
            details = bottleneck.get('details', '')
            
            explanation += f"{i}. {message} ({severity} severity)\n"
            if details:
                explanation += f"   {details}\n"
            
            # Add specific recommendations based on bottleneck type
            if bottleneck_type == 'memory':
                explanation += "   Recommendation: Consider using gradient checkpointing, mixed precision training, or reducing batch size.\n"
            elif bottleneck_type == 'timing' and 'forward pass' in message.lower():
                explanation += "   Recommendation: Consider using torch.compile or channels_last memory format for CNN models.\n"
            elif bottleneck_type == 'timing' and 'data loading' in message.lower():
                explanation += "   Recommendation: Increase number of dataloader workers, use pinned memory, or preprocess data.\n"
            elif bottleneck_type == 'dataloader':
                explanation += "   Recommendation: Optimize dataloader configuration and data preprocessing pipeline.\n"
            elif bottleneck_type in ['vanishing_gradients', 'exploding_gradients', 'dead_neurons']:
                explanation += "   Recommendation: Review model architecture, activation functions, and learning rate.\n"
            
            explanation += "\n"
        
        return explanation
    
    def explain_recommendations(self, recommendations: List[Dict[str, Any]]) -> str:
        """
        Generate explanation of optimization recommendations.
        
        Args:
            recommendations: List of optimization recommendations
            
        Returns:
            Natural language explanation
        """
        if not recommendations:
            return "No optimization recommendations available."
        
        explanation = f"Analysis generated {len(recommendations)} optimization recommendation(s):\n\n"
        
        # Group recommendations by category
        categories = {}
        for rec in recommendations:
            category = rec.get('category', 'general')
            if category not in categories:
                categories[category] = []
            categories[category].append(rec)
        
        for category, category_recs in categories.items():
            explanation += f"== {category.title()} Optimizations ==\n\n"
            
            for i, rec in enumerate(category_recs, 1):
                priority = rec.get('priority', 'medium')
                message = rec.get('message', 'No details available')
                details = rec.get('details', '')
                
                explanation += f"{i}. {message} ({priority} priority)\n"
                if details:
                    explanation += f"   {details}\n"
                
                # Add code snippet if available
                code = rec.get('code', '')
                if code:
                    explanation += "   Implementation:\n"
                    explanation += "   ```python\n"
                    for line in code.split('\n'):
                        explanation += f"   {line}\n"
                    explanation += "   ```\n"
                
                explanation += "\n"
        
        return explanation
    
    def generate_comprehensive_report(self, metrics: Dict[str, List[Dict[str, Any]]], 
                                     bottlenecks: List[Dict[str, Any]], 
                                     recommendations: List[Dict[str, Any]]) -> str:
        """
        Generate a comprehensive natural language report.
        
        Args:
            metrics: Dictionary of metrics
            bottlenecks: List of detected bottlenecks
            recommendations: List of optimization recommendations
            
        Returns:
            Comprehensive natural language report
        """
        report = "# AutoPipelineDoctor Training Analysis Report\n\n"
        report += f"Generated on {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        
        # Summary section
        report += "## Summary\n\n"
        
        # Count metrics
        metric_counts = {category: len(metrics[category]) for category in metrics if metrics[category]}
        total_metrics = sum(metric_counts.values())
        
        report += f"Analyzed {total_metrics} total metrics across {len(metric_counts)} categories. "
        report += f"Detected {len(bottlenecks)} bottlenecks and generated {len(recommendations)} optimization recommendations.\n\n"
        
        # Memory usage section
        report += "## Memory Usage Analysis\n\n"
        report += self.explain_memory_usage(metrics) + "\n\n"
        
        # Timing breakdown section
        report += "## Timing Breakdown Analysis\n\n"
        report += self.explain_timing_breakdown(metrics) + "\n\n"
        
        # Gradient statistics section
        report += "## Gradient Statistics Analysis\n\n"
        report += self.explain_gradient_statistics(metrics) + "\n\n"
        
        # Bottlenecks section
        report += "## Detected Bottlenecks\n\n"
        report += self.explain_bottlenecks(bottlenecks) + "\n\n"
        
        # Recommendations section
        report += "## Optimization Recommendations\n\n"
        report += self.explain_recommendations(recommendations) + "\n\n"
        
        # Conclusion
        report += "## Conclusion\n\n"
        
        if bottlenecks:
            report += "Your training process has some bottlenecks that could be addressed to improve performance. "
            report += "Review the recommendations above and consider implementing the high-priority ones first.\n\n"
        else:
            report += "Your training process appears to be running smoothly without major bottlenecks. "
            report += "You may still benefit from some of the optimization recommendations to further improve performance.\n\n"
        
        report += "For more detailed analysis, refer to the visualizations and metrics provided by AutoPipelineDoctor.\n"
        
        return report
