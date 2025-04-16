"""
Visualization and reporting module for AutoPipelineDoctor.

This module provides functionality to generate visual dashboards, markdown reports,
and natural language explanations of model training performance.
"""

import logging
import os
import time
from typing import Dict, Any, Optional, List, Tuple, Union, Callable
import json
from datetime import datetime
import tempfile
from pathlib import Path

import torch
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.figure import Figure
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

logger = logging.getLogger(__name__)


class Visualizer:
    """
    Visualizer for ML/AI training pipeline metrics.
    
    This class generates visual dashboards, plots, and reports based on
    metrics collected during model training.
    
    Attributes:
        output_dir: Directory to save visualizations and reports
        metrics_history: Dictionary of historical metrics
        is_active: Whether the visualizer is active
        plot_style: Style for matplotlib plots
        color_palette: Color palette for plots
        interactive: Whether to generate interactive plots
    """
    
    def __init__(
        self,
        output_dir: Optional[str] = None,
        interactive: bool = True,
        plot_style: str = "whitegrid",
        color_palette: str = "viridis",
    ):
        """
        Initialize the visualizer.
        
        Args:
            output_dir: Directory to save visualizations and reports
            interactive: Whether to generate interactive plots
            plot_style: Style for matplotlib plots
            color_palette: Color palette for plots
        """
        self.output_dir = output_dir or os.path.join(os.getcwd(), "autopd_reports")
        os.makedirs(self.output_dir, exist_ok=True)
        
        self.metrics_history = {}
        self.is_active = False
        self.plot_style = plot_style
        self.color_palette = color_palette
        self.interactive = interactive
        
        # Set up plotting style
        sns.set_style(plot_style)
        sns.set_palette(color_palette)
        
        # Initialize timestamp for report naming
        self.start_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        logger.info(f"Visualizer initialized with output directory: {self.output_dir}")
    
    def start(self):
        """Start the visualizer."""
        self.is_active = True
        logger.info("Visualizer started")
        return self
    
    def stop(self):
        """Stop the visualizer."""
        self.is_active = False
        logger.info("Visualizer stopped")
        return self
    
    def update_metrics(self, metrics: Dict[str, Any], category: str = "general"):
        """
        Update metrics history with new metrics.
        
        Args:
            metrics: Dictionary of metrics to update
            category: Category of metrics (e.g., "memory", "timing", "gradient")
        """
        if not self.is_active:
            return
        
        # Initialize category if it doesn't exist
        if category not in self.metrics_history:
            self.metrics_history[category] = []
        
        # Add timestamp to metrics
        metrics_with_time = metrics.copy()
        metrics_with_time["timestamp"] = time.time()
        
        # Append to history
        self.metrics_history[category].append(metrics_with_time)
        
        logger.debug(f"Updated {category} metrics history")
    
    def generate_dashboard(self, output_path: Optional[str] = None) -> str:
        """
        Generate an interactive dashboard of training metrics.
        
        Args:
            output_path: Path to save the dashboard HTML file
        
        Returns:
            Path to the generated dashboard HTML file
        """
        if not self.metrics_history:
            logger.warning("No metrics history available for dashboard generation")
            return ""
        
        if output_path is None:
            output_path = os.path.join(
                self.output_dir, f"dashboard_{self.start_time}.html"
            )
        
        try:
            # Create a plotly dashboard
            fig = make_subplots(
                rows=len(self.metrics_history),
                cols=1,
                subplot_titles=list(self.metrics_history.keys()),
                vertical_spacing=0.1,
            )
            
            row = 1
            for category, metrics_list in self.metrics_history.items():
                if not metrics_list:
                    continue
                
                # Convert metrics list to DataFrame
                df = pd.DataFrame(metrics_list)
                
                # Get timestamps
                timestamps = df["timestamp"].values
                timestamps = [datetime.fromtimestamp(ts) for ts in timestamps]
                
                # Plot numeric metrics
                for col in df.columns:
                    if col == "timestamp":
                        continue
                    
                    # Check if column is numeric
                    if pd.api.types.is_numeric_dtype(df[col]):
                        fig.add_trace(
                            go.Scatter(
                                x=timestamps,
                                y=df[col].values,
                                mode="lines+markers",
                                name=f"{category}_{col}",
                            ),
                            row=row,
                            col=1,
                        )
                
                row += 1
            
            # Update layout
            fig.update_layout(
                title="AutoPipelineDoctor Training Metrics Dashboard",
                height=300 * len(self.metrics_history),
                width=1000,
                showlegend=True,
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            )
            
            # Save to HTML file
            fig.write_html(output_path)
            
            logger.info(f"Generated dashboard at {output_path}")
            return output_path
        
        except Exception as e:
            logger.error(f"Failed to generate dashboard: {e}")
            return ""
    
    def generate_report(self, output_path: Optional[str] = None) -> str:
        """
        Generate a comprehensive markdown report of training metrics.
        
        Args:
            output_path: Path to save the markdown report
        
        Returns:
            Path to the generated markdown report
        """
        if not self.metrics_history:
            logger.warning("No metrics history available for report generation")
            return ""
        
        if output_path is None:
            output_path = os.path.join(
                self.output_dir, f"report_{self.start_time}.md"
            )
        
        try:
            # Generate report content
            report = self._generate_report_content()
            
            # Save to file
            with open(output_path, "w") as f:
                f.write(report)
            
            logger.info(f"Generated report at {output_path}")
            return output_path
        
        except Exception as e:
            logger.error(f"Failed to generate report: {e}")
            return ""
    
    def _generate_report_content(self) -> str:
        """
        Generate the content of the markdown report.
        
        Returns:
            Markdown formatted report content
        """
        report = "# AutoPipelineDoctor Training Report\n\n"
        report += f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        
        # Add summary section
        report += "## Summary\n\n"
        report += self._generate_summary_section()
        
        # Add sections for each metric category
        for category, metrics_list in self.metrics_history.items():
            if not metrics_list:
                continue
            
            report += f"## {category.capitalize()} Metrics\n\n"
            
            # Convert metrics list to DataFrame
            df = pd.DataFrame(metrics_list)
            
            # Generate statistics for numeric columns
            numeric_cols = [col for col in df.columns if col != "timestamp" and pd.api.types.is_numeric_dtype(df[col])]
            
            if numeric_cols:
                report += "### Statistics\n\n"
                report += "| Metric | Mean | Min | Max | Last |\n"
                report += "|--------|------|-----|-----|------|\n"
                
                for col in numeric_cols:
                    mean_val = df[col].mean()
                    min_val = df[col].min()
                    max_val = df[col].max()
                    last_val = df[col].iloc[-1]
                    
                    report += f"| {col} | {mean_val:.4f} | {min_val:.4f} | {max_val:.4f} | {last_val:.4f} |\n"
                
                report += "\n"
            
            # Generate plots for this category
            plot_path = self._generate_category_plots(category, df)
            if plot_path:
                report += f"### Plots\n\n"
                report += f"![{category} Metrics]({os.path.relpath(plot_path, os.path.dirname(os.path.join(self.output_dir, 'report.md')))})\n\n"
            
            # Add natural language explanation
            report += "### Analysis\n\n"
            report += self._generate_explanation(category, df)
            report += "\n\n"
        
        # Add recommendations section
        report += "## Recommendations\n\n"
        report += self._generate_recommendations()
        
        return report
    
    def _generate_summary_section(self) -> str:
        """
        Generate the summary section of the report.
        
        Returns:
            Markdown formatted summary section
        """
        summary = ""
        
        # Count total metrics
        total_metrics = sum(len(metrics_list) for metrics_list in self.metrics_history.values())
        summary += f"- Total metrics collected: {total_metrics}\n"
        
        # Count categories
        summary += f"- Metric categories: {', '.join(self.metrics_history.keys())}\n"
        
        # Calculate monitoring duration
        if any(self.metrics_history.values()):
            # Find earliest and latest timestamps
            earliest = min(
                metrics_list[0]["timestamp"]
                for metrics_list in self.metrics_history.values()
                if metrics_list
            )
            latest = max(
                metrics_list[-1]["timestamp"]
                for metrics_list in self.metrics_history.values()
                if metrics_list
            )
            
            duration_seconds = latest - earliest
            hours, remainder = divmod(duration_seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            
            summary += f"- Monitoring duration: {int(hours)}h {int(minutes)}m {int(seconds)}s\n"
        
        return summary
    
    def _generate_category_plots(self, category: str, df: pd.DataFrame) -> str:
        """
        Generate plots for a specific metric category.
        
        Args:
            category: Category of metrics
            df: DataFrame of metrics
        
        Returns:
            Path to the generated plot image
        """
        # Skip if no numeric columns
        numeric_cols = [col for col in df.columns if col != "timestamp" and pd.api.types.is_numeric_dtype(df[col])]
        if not numeric_cols:
            return ""
        
        try:
            # Create plot directory
            plots_dir = os.path.join(self.output_dir, "plots")
            os.makedirs(plots_dir, exist_ok=True)
            
            # Generate plot file path
            plot_path = os.path.join(plots_dir, f"{category}_{self.start_time}.png")
            
            # Create figure
            n_cols = min(3, len(numeric_cols))
            n_rows = (len(numeric_cols) + n_cols - 1) // n_cols
            
            fig, axes = plt.subplots(n_rows, n_cols, figsize=(5 * n_cols, 4 * n_rows))
            
            # Flatten axes for easier indexing
            if n_rows == 1 and n_cols == 1:
                axes = np.array([axes])
            elif n_rows == 1 or n_cols == 1:
                axes = axes.flatten()
            
            # Convert timestamps to datetime
            timestamps = df["timestamp"].apply(lambda x: datetime.fromtimestamp(x))
            
            # Plot each metric
            for i, col in enumerate(numeric_cols):
                row, col_idx = divmod(i, n_cols)
                
                if n_rows > 1 and n_cols > 1:
                    ax = axes[row, col_idx]
                else:
                    ax = axes[i]
                
                ax.plot(timestamps, df[col], marker="o", linestyle="-", markersize=4)
                ax.set_title(col)
                ax.set_xlabel("Time")
                ax.set_ylabel(col)
                ax.grid(True, alpha=0.3)
                
                # Rotate x-axis labels for better readability
                plt.setp(ax.get_xticklabels(), rotation=45, ha="right")
            
            # Hide empty subplots
            for i in range(len(numeric_cols), n_rows * n_cols):
                row, col_idx = divmod(i, n_cols)
                if n_rows > 1 and n_cols > 1:
                    axes[row, col_idx].axis("off")
                elif i < len(axes):
                    axes[i].axis("off")
            
            # Adjust layout
            plt.tight_layout()
            
            # Save figure
            plt.savefig(plot_path, dpi=100, bbox_inches="tight")
            plt.close(fig)
            
            return plot_path
        
        except Exception as e:
            logger.error(f"Failed to generate plots for {category}: {e}")
            return ""
    
    def _generate_explanation(self, category: str, df: pd.DataFrame) -> str:
        """
        Generate natural language explanation of metrics.
        
        Args:
            category: Category of metrics
            df: DataFrame of metrics
        
        Returns:
            Markdown formatted explanation
        """
        explanation = ""
        
        # Skip if no numeric columns
        numeric_cols = [col for col in df.columns if col != "timestamp" and pd.api.types.is_numeric_dtype(df[col])]
        if not numeric_cols:
            return "No numeric metrics available for analysis."
        
        try:
            # Generate explanations based on category
            if category == "memory":
                explanation += self._explain_memory_metrics(df)
            elif category == "timing":
                explanation += self._explain_timing_metrics(df)
            elif category == "gradient":
                explanation += self._explain_gradient_metrics(df)
            elif category == "dataloader":
                explanation += self._explain_dataloader_metrics(df)
            elif category == "hardware":
                explanation += self._explain_hardware_metrics(df)
            else:
                # Generic explanation for other categories
                explanation += self._explain_generic_metrics(category, df)
            
            return explanation
        
        except Exception as e:
            logger.error(f"Failed to generate explanation for {category}: {e}")
            return f"Error generating explanation: {str(e)}"
    
    def _explain_memory_metrics(self, df: pd.DataFrame) -> str:
        """
        Generate explanation for memory metrics.
        
        Args:
            df: DataFrame of memory metrics
        
        Returns:
            Markdown formatted explanation
        """
        explanation = ""
        
        # Check for memory usage trends
        if "allocated_memory" in df.columns:
            # Calculate trend
            x = np.arange(len(df))
            y = df["allocated_memory"].values
            
            if len(x) > 1:
                A = np.vstack([x, np.ones(len(x))]).T
                m, c = np.linalg.lstsq(A, y, rcond=None)[0]
                
                if m > 0:
                    explanation += f"Memory usage is **increasing** at a rate of approximately {m:.2f} MB per iteration. "
                    
                    # Estimate time to OOM
                    if "total_memory" in df.columns:
                        total_memory = df["total_memory"].iloc[-1]
                        current_memory = df["allocated_memory"].iloc[-1]
                        available_memory = total_memory - current_memory
                        
                        if m > 0:
                            iterations_to_oom = available_memory / m
                            explanation += f"At this rate, you may run out of memory in approximately {int(iterations_to_oom)} iterations. "
                elif m < 0:
                    explanation += f"Memory usage is **decreasing** at a rate of approximately {-m:.2f} MB per iteration. "
                else:
                    explanation += "Memory usage is **stable** throughout training. "
            
            # Check for memory fragmentation
            if "memory_fragmentation" in df.columns:
                avg_fragmentation = df["memory_fragmentation"].mean()
                if avg_fragmentation > 0.3:
                    explanation += f"Memory fragmentation is **high** ({avg_fragmentation:.2%}), which may lead to inefficient memory usage. "
                else:
                    explanation += f"Memory fragmentation is at an acceptable level ({avg_fragmentation:.2%}). "
        
        # Check for model size
        if "model_size" in df.columns:
            model_size = df["model_size"].iloc[-1]
            explanation += f"The model size is approximately {model_size:.2f} MB. "
        
        # Check for largest layer
        if "largest_layer_memory" in df.columns and "largest_layer_name" in df.columns:
            largest_layer_memory = df["largest_layer_memory"].iloc[-1]
            largest_layer_name = df["largest_layer_name"].iloc[-1]
            explanation += f"The largest layer is **{largest_layer_name}**, consuming {largest_layer_memory:.2f} MB. "
        
        return explanation
    
    def _explain_timing_metrics(self, df: pd.DataFrame) -> str:
        """
        Generate explanation for timing metrics.
        
        Args:
            df: DataFrame of timing metrics
        
        Returns:
            Markdown formatted explanation
        """
        explanation = ""
        
        # Check for timing bottlenecks
        timing_cols = [
            col for col in ["forward_time", "backward_time", "optimizer_time", "dataloader_time"]
            if col in df.columns
        ]
        
        if timing_cols:
            # Calculate average times
            avg_times = {col: df[col].mean() for col in timing_cols}
            
            # Find the bottleneck
            bottleneck = max(avg_times.items(), key=lambda x: x[1])
            total_time = sum(avg_times.values())
            
            if total_time > 0:
                bottleneck_pct = bottleneck[1] / total_time * 100
                explanation += f"The main timing bottleneck is the **{bottleneck[0].replace('_time', '')}** phase, "
                explanation += f"which takes {bottleneck[1]:.4f}s on average ({bottleneck_pct:.1f}% of total time). "
            
            # Check for iterations per second
            if "iterations_per_second" in df.columns:
                ips = df["iterations_per_second"].iloc[-1]
                explanation += f"The training speed is {ips:.2f} iterations per second. "
        
        return explanation
    
    def _explain_gradient_metrics(self, df: pd.DataFrame) -> str:
        """
        Generate explanation for gradient metrics.
        
        Args:
            df: DataFrame of gradient metrics
        
        Returns:
            Markdown formatted explanation
        """
        explanation = ""
        
        # Check for gradient issues
        if "avg_grad_norm" in df.columns:
            avg_grad_norm = df["avg_grad_norm"].iloc[-1]
            explanation += f"The average gradient norm is {avg_grad_norm:.4f}. "
            
            if avg_grad_norm < 0.001:
                explanation += "This is **very small**, which may indicate vanishing gradients. "
            elif avg_grad_norm > 10.0:
                explanation += "This is **very large**, which may indicate exploding gradients. "
            else:
                explanation += "This is within a normal range. "
        
        # Check for dead gradients
        if "dead_gradients_pct" in df.columns:
            dead_gradients_pct = df["dead_gradients_pct"].iloc[-1]
            if dead_gradients_pct > 20:
                explanation += f"**{dead_gradients_pct:.1f}%** of parameters have near-zero gradients, "
                explanation += "which may indicate dead neurons or vanishing gradients. "
            elif dead_gradients_pct > 5:
                explanation += f"{dead_gradients_pct:.1f}% of parameters have near-zero gradients. "
        
        # Check for exploding gradients
        if "exploding_gradients_pct" in df.columns:
            exploding_gradients_pct = df["exploding_gradients_pct"].iloc[-1]
            if exploding_gradients_pct > 10:
                explanation += f"**{exploding_gradients_pct:.1f}%** of parameters have very large gradients, "
                explanation += "which may indicate exploding gradients. "
            elif exploding_gradients_pct > 2:
                explanation += f"{exploding_gradients_pct:.1f}% of parameters have large gradients. "
        
        return explanation
    
    def _explain_dataloader_metrics(self, df: pd.DataFrame) -> str:
        """
        Generate explanation for dataloader metrics.
        
        Args:
            df: DataFrame of dataloader metrics
        
        Returns:
            Markdown formatted explanation
        """
        explanation = ""
        
        # Check for dataloader efficiency
        if "avg_batch_time" in df.columns:
            avg_batch_time = df["avg_batch_time"].iloc[-1]
            explanation += f"The average batch loading time is {avg_batch_time:.4f}s. "
            
            if "num_workers" in df.columns and "estimated_optimal_workers" in df.columns:
                num_workers = df["num_workers"].iloc[-1]
                optimal_workers = df["estimated_optimal_workers"].iloc[-1]
                
                if optimal_workers > num_workers * 1.5:
                    explanation += f"The dataloader is using **{int(num_workers)}** workers, but **{int(optimal_workers)}** "
                    explanation += "would be more efficient. "
                elif num_workers > optimal_workers * 1.5:
                    explanation += f"The dataloader is using **{int(num_workers)}** workers, but **{int(optimal_workers)}** "
                    explanation += "would be sufficient. "
                else:
                    explanation += f"The dataloader is using an appropriate number of workers ({int(num_workers)}). "
        
        # Check for worker utilization
        if "worker_utilization" in df.columns:
            worker_utilization = df["worker_utilization"].iloc[-1]
            if worker_utilization < 0.5:
                explanation += f"Worker utilization is low ({worker_utilization:.2%}), indicating potential inefficiency. "
            elif worker_utilization > 0.9:
                explanation += f"Worker utilization is high ({worker_utilization:.2%}), indicating potential bottleneck. "
        
        return explanation
    
    def _explain_hardware_metrics(self, df: pd.DataFrame) -> str:
        """
        Generate explanation for hardware metrics.
        
        Args:
            df: DataFrame of hardware metrics
        
        Returns:
            Markdown formatted explanation
        """
        explanation = ""
        
        # Check for GPU utilization
        if "gpu_percent" in df.columns:
            avg_gpu = df["gpu_percent"].mean()
            explanation += f"Average GPU utilization is {avg_gpu:.1f}%. "
            
            if avg_gpu < 30:
                explanation += "This is **very low**, indicating potential CPU bottlenecks or inefficient GPU usage. "
            elif avg_gpu < 70:
                explanation += "This is **moderate**, suggesting room for optimization. "
            else:
                explanation += "This is **high**, indicating good GPU utilization. "
        
        # Check for CPU utilization
        if "cpu_percent" in df.columns:
            avg_cpu = df["cpu_percent"].mean()
            explanation += f"Average CPU utilization is {avg_cpu:.1f}%. "
            
            if "gpu_percent" in df.columns and avg_cpu > 80 and df["gpu_percent"].mean() < 50:
                explanation += "CPU is heavily utilized while GPU is underutilized, suggesting a CPU bottleneck. "
        
        # Check for GPU memory
        if "gpu_memory_percent" in df.columns:
            avg_gpu_mem = df["gpu_memory_percent"].mean()
            explanation += f"Average GPU memory utilization is {avg_gpu_mem:.1f}%. "
            
            if avg_gpu_mem > 90:
                explanation += "This is **very high**, risking out-of-memory errors. "
            elif avg_gpu_mem < 30:
                explanation += "This is **low**, suggesting room for larger batch sizes. "
        
        # Check for GPU temperature
        if "gpu_temperature" in df.columns:
            avg_temp = df["gpu_temperature"].mean()
            max_temp = df["gpu_temperature"].max()
            
            explanation += f"Average GPU temperature is {avg_temp:.1f}°C (max: {max_temp:.1f}°C). "
            
            if max_temp > 85:
                explanation += "This is **very high** and may lead to thermal throttling. "
            elif max_temp > 75:
                explanation += "This is **high** but within normal operating range. "
        
        return explanation
    
    def _explain_generic_metrics(self, category: str, df: pd.DataFrame) -> str:
        """
        Generate generic explanation for metrics.
        
        Args:
            category: Category of metrics
            df: DataFrame of metrics
        
        Returns:
            Markdown formatted explanation
        """
        explanation = ""
        
        # Get numeric columns
        numeric_cols = [col for col in df.columns if col != "timestamp" and pd.api.types.is_numeric_dtype(df[col])]
        
        if not numeric_cols:
            return "No numeric metrics available for analysis."
        
        # Analyze trends for each metric
        for col in numeric_cols:
            # Calculate trend
            x = np.arange(len(df))
            y = df[col].values
            
            if len(x) > 1:
                A = np.vstack([x, np.ones(len(x))]).T
                m, c = np.linalg.lstsq(A, y, rcond=None)[0]
                
                # Get last value
                last_val = df[col].iloc[-1]
                
                explanation += f"**{col}**: Current value is {last_val:.4f}. "
                
                if abs(m) < 0.001:
                    explanation += "This metric is **stable** throughout training. "
                elif m > 0:
                    explanation += f"This metric is **increasing** at a rate of approximately {m:.4f} per iteration. "
                else:
                    explanation += f"This metric is **decreasing** at a rate of approximately {-m:.4f} per iteration. "
            
            # Check for outliers
            q1 = df[col].quantile(0.25)
            q3 = df[col].quantile(0.75)
            iqr = q3 - q1
            lower_bound = q1 - 1.5 * iqr
            upper_bound = q3 + 1.5 * iqr
            
            outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)][col]
            if len(outliers) > 0:
                explanation += f"There are {len(outliers)} outliers in this metric. "
            
            explanation += "\n\n"
        
        return explanation
    
    def _generate_recommendations(self) -> str:
        """
        Generate recommendations based on metrics.
        
        Returns:
            Markdown formatted recommendations
        """
        recommendations = ""
        
        # Check if we have enough data
        if not self.metrics_history:
            return "Not enough data to generate recommendations."
        
        # Memory recommendations
        if "memory" in self.metrics_history and self.metrics_history["memory"]:
            memory_df = pd.DataFrame(self.metrics_history["memory"])
            
            # Check for high memory usage
            if "allocated_memory" in memory_df.columns and "total_memory" in memory_df.columns:
                memory_usage_pct = memory_df["allocated_memory"].iloc[-1] / memory_df["total_memory"].iloc[-1]
                
                if memory_usage_pct > 0.9:
                    recommendations += "- **Critical**: Memory usage is very high (>90%). Consider reducing batch size or using gradient checkpointing.\n"
                elif memory_usage_pct > 0.7:
                    recommendations += "- **Warning**: Memory usage is high (>70%). Monitor closely and consider memory optimizations.\n"
            
            # Check for memory fragmentation
            if "memory_fragmentation" in memory_df.columns:
                fragmentation = memory_df["memory_fragmentation"].iloc[-1]
                
                if fragmentation > 0.3:
                    recommendations += "- **Optimization**: High memory fragmentation detected. Call `torch.cuda.empty_cache()` periodically.\n"
        
        # Timing recommendations
        if "timing" in self.metrics_history and self.metrics_history["timing"]:
            timing_df = pd.DataFrame(self.metrics_history["timing"])
            
            # Check for dataloader bottleneck
            if "dataloader_time" in timing_df.columns and "total_time" in timing_df.columns:
                dataloader_pct = timing_df["dataloader_time"].mean() / timing_df["total_time"].mean()
                
                if dataloader_pct > 0.3:
                    recommendations += "- **Performance**: Dataloader is a significant bottleneck. Increase num_workers or use faster storage.\n"
            
            # Check for optimizer bottleneck
            if "optimizer_time" in timing_df.columns and "total_time" in timing_df.columns:
                optimizer_pct = timing_df["optimizer_time"].mean() / timing_df["total_time"].mean()
                
                if optimizer_pct > 0.3:
                    recommendations += "- **Performance**: Optimizer step is taking significant time. Consider using a different optimizer or gradient accumulation.\n"
        
        # Gradient recommendations
        if "gradient" in self.metrics_history and self.metrics_history["gradient"]:
            gradient_df = pd.DataFrame(self.metrics_history["gradient"])
            
            # Check for vanishing gradients
            if "dead_gradients_pct" in gradient_df.columns:
                dead_pct = gradient_df["dead_gradients_pct"].iloc[-1]
                
                if dead_pct > 20:
                    recommendations += "- **Training**: Vanishing gradients detected. Consider using batch normalization, residual connections, or different activation functions.\n"
            
            # Check for exploding gradients
            if "exploding_gradients_pct" in gradient_df.columns:
                exploding_pct = gradient_df["exploding_gradients_pct"].iloc[-1]
                
                if exploding_pct > 10:
                    recommendations += "- **Training**: Exploding gradients detected. Use gradient clipping or reduce learning rate.\n"
        
        # Hardware recommendations
        if "hardware" in self.metrics_history and self.metrics_history["hardware"]:
            hardware_df = pd.DataFrame(self.metrics_history["hardware"])
            
            # Check for GPU underutilization
            if "gpu_percent" in hardware_df.columns:
                gpu_util = hardware_df["gpu_percent"].mean()
                
                if gpu_util < 30:
                    recommendations += "- **Performance**: GPU utilization is very low. Check for CPU bottlenecks or consider using a smaller model.\n"
            
            # Check for high temperature
            if "gpu_temperature" in hardware_df.columns:
                max_temp = hardware_df["gpu_temperature"].max()
                
                if max_temp > 85:
                    recommendations += "- **Hardware**: GPU temperature is very high. Ensure proper cooling or reduce workload.\n"
        
        # If no specific recommendations, add general ones
        if not recommendations:
            recommendations += "- No specific issues detected. Continue monitoring training performance.\n"
            recommendations += "- Consider experimenting with different learning rates and batch sizes for optimal performance.\n"
            recommendations += "- Regularly check for new versions of libraries and frameworks for performance improvements.\n"
        
        return recommendations
    
    def generate_plots(
        self,
        metrics: Dict[str, Any],
        category: str = "general",
        output_dir: Optional[str] = None,
    ) -> List[str]:
        """
        Generate plots for specific metrics.
        
        Args:
            metrics: Dictionary of metrics to plot
            category: Category of metrics
            output_dir: Directory to save plots
        
        Returns:
            List of paths to generated plot files
        """
        if not self.is_active:
            return []
        
        if output_dir is None:
            output_dir = os.path.join(self.output_dir, "plots")
        
        os.makedirs(output_dir, exist_ok=True)
        
        plot_paths = []
        
        try:
            # Convert metrics to DataFrame if it's a list of metrics
            if isinstance(metrics, list):
                df = pd.DataFrame(metrics)
            else:
                # If it's a single metrics dict, convert to DataFrame with one row
                df = pd.DataFrame([metrics])
            
            # Generate plots based on category
            if category == "memory":
                plot_paths.extend(self._generate_memory_plots(df, output_dir))
            elif category == "timing":
                plot_paths.extend(self._generate_timing_plots(df, output_dir))
            elif category == "gradient":
                plot_paths.extend(self._generate_gradient_plots(df, output_dir))
            elif category == "hardware":
                plot_paths.extend(self._generate_hardware_plots(df, output_dir))
            else:
                # Generic plots for other categories
                plot_paths.extend(self._generate_generic_plots(df, category, output_dir))
            
            return plot_paths
        
        except Exception as e:
            logger.error(f"Failed to generate plots: {e}")
            return []
    
    def _generate_memory_plots(self, df: pd.DataFrame, output_dir: str) -> List[str]:
        """
        Generate memory-specific plots.
        
        Args:
            df: DataFrame of memory metrics
            output_dir: Directory to save plots
        
        Returns:
            List of paths to generated plot files
        """
        plot_paths = []
        
        # Memory usage plot
        if "allocated_memory" in df.columns and "reserved_memory" in df.columns:
            try:
                fig, ax = plt.subplots(figsize=(10, 6))
                
                if "timestamp" in df.columns:
                    x = df["timestamp"].apply(lambda x: datetime.fromtimestamp(x))
                else:
                    x = np.arange(len(df))
                
                ax.plot(x, df["allocated_memory"], marker="o", label="Allocated Memory (MB)")
                ax.plot(x, df["reserved_memory"], marker="s", label="Reserved Memory (MB)")
                
                if "total_memory" in df.columns:
                    ax.axhline(y=df["total_memory"].iloc[0], color="r", linestyle="--", label="Total Memory")
                
                ax.set_title("Memory Usage Over Time")
                ax.set_xlabel("Time" if "timestamp" in df.columns else "Iteration")
                ax.set_ylabel("Memory (MB)")
                ax.grid(True, alpha=0.3)
                ax.legend()
                
                # Save plot
                plot_path = os.path.join(output_dir, f"memory_usage_{self.start_time}.png")
                plt.savefig(plot_path, dpi=100, bbox_inches="tight")
                plt.close(fig)
                
                plot_paths.append(plot_path)
            except Exception as e:
                logger.error(f"Failed to generate memory usage plot: {e}")
        
        # Memory fragmentation plot
        if "memory_fragmentation" in df.columns:
            try:
                fig, ax = plt.subplots(figsize=(10, 6))
                
                if "timestamp" in df.columns:
                    x = df["timestamp"].apply(lambda x: datetime.fromtimestamp(x))
                else:
                    x = np.arange(len(df))
                
                ax.plot(x, df["memory_fragmentation"] * 100, marker="o", label="Fragmentation (%)")
                
                ax.set_title("Memory Fragmentation Over Time")
                ax.set_xlabel("Time" if "timestamp" in df.columns else "Iteration")
                ax.set_ylabel("Fragmentation (%)")
                ax.grid(True, alpha=0.3)
                
                # Add warning threshold
                ax.axhline(y=30, color="r", linestyle="--", label="Warning Threshold (30%)")
                
                ax.legend()
                
                # Save plot
                plot_path = os.path.join(output_dir, f"memory_fragmentation_{self.start_time}.png")
                plt.savefig(plot_path, dpi=100, bbox_inches="tight")
                plt.close(fig)
                
                plot_paths.append(plot_path)
            except Exception as e:
                logger.error(f"Failed to generate memory fragmentation plot: {e}")
        
        return plot_paths
    
    def _generate_timing_plots(self, df: pd.DataFrame, output_dir: str) -> List[str]:
        """
        Generate timing-specific plots.
        
        Args:
            df: DataFrame of timing metrics
            output_dir: Directory to save plots
        
        Returns:
            List of paths to generated plot files
        """
        plot_paths = []
        
        # Timing breakdown plot
        timing_cols = [
            col for col in ["forward_time", "backward_time", "optimizer_time", "dataloader_time"]
            if col in df.columns
        ]
        
        if timing_cols:
            try:
                fig, ax = plt.subplots(figsize=(10, 6))
                
                if "timestamp" in df.columns:
                    x = df["timestamp"].apply(lambda x: datetime.fromtimestamp(x))
                else:
                    x = np.arange(len(df))
                
                for col in timing_cols:
                    ax.plot(x, df[col], marker="o", label=col.replace("_time", "").capitalize())
                
                ax.set_title("Timing Breakdown Over Time")
                ax.set_xlabel("Time" if "timestamp" in df.columns else "Iteration")
                ax.set_ylabel("Time (seconds)")
                ax.grid(True, alpha=0.3)
                ax.legend()
                
                # Save plot
                plot_path = os.path.join(output_dir, f"timing_breakdown_{self.start_time}.png")
                plt.savefig(plot_path, dpi=100, bbox_inches="tight")
                plt.close(fig)
                
                plot_paths.append(plot_path)
            except Exception as e:
                logger.error(f"Failed to generate timing breakdown plot: {e}")
        
        # Iterations per second plot
        if "iterations_per_second" in df.columns:
            try:
                fig, ax = plt.subplots(figsize=(10, 6))
                
                if "timestamp" in df.columns:
                    x = df["timestamp"].apply(lambda x: datetime.fromtimestamp(x))
                else:
                    x = np.arange(len(df))
                
                ax.plot(x, df["iterations_per_second"], marker="o", label="Iterations per Second")
                
                ax.set_title("Training Speed Over Time")
                ax.set_xlabel("Time" if "timestamp" in df.columns else "Iteration")
                ax.set_ylabel("Iterations per Second")
                ax.grid(True, alpha=0.3)
                
                # Save plot
                plot_path = os.path.join(output_dir, f"training_speed_{self.start_time}.png")
                plt.savefig(plot_path, dpi=100, bbox_inches="tight")
                plt.close(fig)
                
                plot_paths.append(plot_path)
            except Exception as e:
                logger.error(f"Failed to generate training speed plot: {e}")
        
        # Timing pie chart
        if len(timing_cols) >= 2:
            try:
                # Calculate average times
                avg_times = {col.replace("_time", ""): df[col].mean() for col in timing_cols}
                
                # Create pie chart
                fig, ax = plt.subplots(figsize=(8, 8))
                
                labels = list(avg_times.keys())
                sizes = list(avg_times.values())
                
                ax.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=90)
                ax.axis("equal")  # Equal aspect ratio ensures that pie is drawn as a circle
                
                ax.set_title("Average Time Distribution")
                
                # Save plot
                plot_path = os.path.join(output_dir, f"timing_distribution_{self.start_time}.png")
                plt.savefig(plot_path, dpi=100, bbox_inches="tight")
                plt.close(fig)
                
                plot_paths.append(plot_path)
            except Exception as e:
                logger.error(f"Failed to generate timing distribution plot: {e}")
        
        return plot_paths
    
    def _generate_gradient_plots(self, df: pd.DataFrame, output_dir: str) -> List[str]:
        """
        Generate gradient-specific plots.
        
        Args:
            df: DataFrame of gradient metrics
            output_dir: Directory to save plots
        
        Returns:
            List of paths to generated plot files
        """
        plot_paths = []
        
        # Gradient norm plot
        if "avg_grad_norm" in df.columns:
            try:
                fig, ax = plt.subplots(figsize=(10, 6))
                
                if "timestamp" in df.columns:
                    x = df["timestamp"].apply(lambda x: datetime.fromtimestamp(x))
                else:
                    x = np.arange(len(df))
                
                ax.plot(x, df["avg_grad_norm"], marker="o", label="Average Gradient Norm")
                
                if "max_grad_norm" in df.columns:
                    ax.plot(x, df["max_grad_norm"], marker="s", label="Max Gradient Norm")
                
                if "min_grad_norm" in df.columns:
                    ax.plot(x, df["min_grad_norm"], marker="^", label="Min Gradient Norm")
                
                ax.set_title("Gradient Norms Over Time")
                ax.set_xlabel("Time" if "timestamp" in df.columns else "Iteration")
                ax.set_ylabel("Gradient Norm")
                ax.grid(True, alpha=0.3)
                ax.legend()
                
                # Use log scale for better visualization
                ax.set_yscale("log")
                
                # Save plot
                plot_path = os.path.join(output_dir, f"gradient_norms_{self.start_time}.png")
                plt.savefig(plot_path, dpi=100, bbox_inches="tight")
                plt.close(fig)
                
                plot_paths.append(plot_path)
            except Exception as e:
                logger.error(f"Failed to generate gradient norm plot: {e}")
        
        # Gradient issues plot
        if "dead_gradients_pct" in df.columns or "exploding_gradients_pct" in df.columns:
            try:
                fig, ax = plt.subplots(figsize=(10, 6))
                
                if "timestamp" in df.columns:
                    x = df["timestamp"].apply(lambda x: datetime.fromtimestamp(x))
                else:
                    x = np.arange(len(df))
                
                if "dead_gradients_pct" in df.columns:
                    ax.plot(x, df["dead_gradients_pct"], marker="o", label="Dead Gradients (%)")
                
                if "exploding_gradients_pct" in df.columns:
                    ax.plot(x, df["exploding_gradients_pct"], marker="s", label="Exploding Gradients (%)")
                
                ax.set_title("Gradient Issues Over Time")
                ax.set_xlabel("Time" if "timestamp" in df.columns else "Iteration")
                ax.set_ylabel("Percentage (%)")
                ax.grid(True, alpha=0.3)
                
                # Add warning thresholds
                ax.axhline(y=20, color="r", linestyle="--", label="Dead Gradient Warning (20%)")
                ax.axhline(y=10, color="orange", linestyle="--", label="Exploding Gradient Warning (10%)")
                
                ax.legend()
                
                # Save plot
                plot_path = os.path.join(output_dir, f"gradient_issues_{self.start_time}.png")
                plt.savefig(plot_path, dpi=100, bbox_inches="tight")
                plt.close(fig)
                
                plot_paths.append(plot_path)
            except Exception as e:
                logger.error(f"Failed to generate gradient issues plot: {e}")
        
        return plot_paths
    
    def _generate_hardware_plots(self, df: pd.DataFrame, output_dir: str) -> List[str]:
        """
        Generate hardware-specific plots.
        
        Args:
            df: DataFrame of hardware metrics
            output_dir: Directory to save plots
        
        Returns:
            List of paths to generated plot files
        """
        plot_paths = []
        
        # GPU/CPU utilization plot
        if "gpu_percent" in df.columns or "cpu_percent" in df.columns:
            try:
                fig, ax = plt.subplots(figsize=(10, 6))
                
                if "timestamp" in df.columns:
                    x = df["timestamp"].apply(lambda x: datetime.fromtimestamp(x))
                else:
                    x = np.arange(len(df))
                
                if "gpu_percent" in df.columns:
                    ax.plot(x, df["gpu_percent"], marker="o", label="GPU Utilization (%)")
                
                if "cpu_percent" in df.columns:
                    ax.plot(x, df["cpu_percent"], marker="s", label="CPU Utilization (%)")
                
                ax.set_title("Hardware Utilization Over Time")
                ax.set_xlabel("Time" if "timestamp" in df.columns else "Iteration")
                ax.set_ylabel("Utilization (%)")
                ax.grid(True, alpha=0.3)
                ax.legend()
                
                # Save plot
                plot_path = os.path.join(output_dir, f"hardware_utilization_{self.start_time}.png")
                plt.savefig(plot_path, dpi=100, bbox_inches="tight")
                plt.close(fig)
                
                plot_paths.append(plot_path)
            except Exception as e:
                logger.error(f"Failed to generate hardware utilization plot: {e}")
        
        # Memory utilization plot
        if "gpu_memory_percent" in df.columns or "memory_percent" in df.columns:
            try:
                fig, ax = plt.subplots(figsize=(10, 6))
                
                if "timestamp" in df.columns:
                    x = df["timestamp"].apply(lambda x: datetime.fromtimestamp(x))
                else:
                    x = np.arange(len(df))
                
                if "gpu_memory_percent" in df.columns:
                    ax.plot(x, df["gpu_memory_percent"], marker="o", label="GPU Memory (%)")
                
                if "memory_percent" in df.columns:
                    ax.plot(x, df["memory_percent"], marker="s", label="System Memory (%)")
                
                ax.set_title("Memory Utilization Over Time")
                ax.set_xlabel("Time" if "timestamp" in df.columns else "Iteration")
                ax.set_ylabel("Utilization (%)")
                ax.grid(True, alpha=0.3)
                ax.legend()
                
                # Save plot
                plot_path = os.path.join(output_dir, f"memory_utilization_{self.start_time}.png")
                plt.savefig(plot_path, dpi=100, bbox_inches="tight")
                plt.close(fig)
                
                plot_paths.append(plot_path)
            except Exception as e:
                logger.error(f"Failed to generate memory utilization plot: {e}")
        
        # Temperature plot
        if "gpu_temperature" in df.columns:
            try:
                fig, ax = plt.subplots(figsize=(10, 6))
                
                if "timestamp" in df.columns:
                    x = df["timestamp"].apply(lambda x: datetime.fromtimestamp(x))
                else:
                    x = np.arange(len(df))
                
                ax.plot(x, df["gpu_temperature"], marker="o", label="GPU Temperature (°C)")
                
                ax.set_title("GPU Temperature Over Time")
                ax.set_xlabel("Time" if "timestamp" in df.columns else "Iteration")
                ax.set_ylabel("Temperature (°C)")
                ax.grid(True, alpha=0.3)
                
                # Add warning thresholds
                ax.axhline(y=85, color="r", linestyle="--", label="Critical Temperature (85°C)")
                ax.axhline(y=75, color="orange", linestyle="--", label="Warning Temperature (75°C)")
                
                ax.legend()
                
                # Save plot
                plot_path = os.path.join(output_dir, f"gpu_temperature_{self.start_time}.png")
                plt.savefig(plot_path, dpi=100, bbox_inches="tight")
                plt.close(fig)
                
                plot_paths.append(plot_path)
            except Exception as e:
                logger.error(f"Failed to generate temperature plot: {e}")
        
        return plot_paths
    
    def _generate_generic_plots(self, df: pd.DataFrame, category: str, output_dir: str) -> List[str]:
        """
        Generate generic plots for any metrics.
        
        Args:
            df: DataFrame of metrics
            category: Category of metrics
            output_dir: Directory to save plots
        
        Returns:
            List of paths to generated plot files
        """
        plot_paths = []
        
        # Get numeric columns
        numeric_cols = [col for col in df.columns if col != "timestamp" and pd.api.types.is_numeric_dtype(df[col])]
        
        if not numeric_cols:
            return plot_paths
        
        try:
            # Create multi-line plot for all metrics
            fig, ax = plt.subplots(figsize=(12, 8))
            
            if "timestamp" in df.columns:
                x = df["timestamp"].apply(lambda x: datetime.fromtimestamp(x))
            else:
                x = np.arange(len(df))
            
            for col in numeric_cols:
                ax.plot(x, df[col], marker="o", label=col)
            
            ax.set_title(f"{category.capitalize()} Metrics Over Time")
            ax.set_xlabel("Time" if "timestamp" in df.columns else "Iteration")
            ax.set_ylabel("Value")
            ax.grid(True, alpha=0.3)
            ax.legend()
            
            # Save plot
            plot_path = os.path.join(output_dir, f"{category}_metrics_{self.start_time}.png")
            plt.savefig(plot_path, dpi=100, bbox_inches="tight")
            plt.close(fig)
            
            plot_paths.append(plot_path)
        except Exception as e:
            logger.error(f"Failed to generate generic metrics plot: {e}")
        
        # Create individual plots for each metric
        for col in numeric_cols:
            try:
                fig, ax = plt.subplots(figsize=(10, 6))
                
                if "timestamp" in df.columns:
                    x = df["timestamp"].apply(lambda x: datetime.fromtimestamp(x))
                else:
                    x = np.arange(len(df))
                
                ax.plot(x, df[col], marker="o", label=col)
                
                ax.set_title(f"{col} Over Time")
                ax.set_xlabel("Time" if "timestamp" in df.columns else "Iteration")
                ax.set_ylabel(col)
                ax.grid(True, alpha=0.3)
                
                # Save plot
                plot_path = os.path.join(output_dir, f"{category}_{col}_{self.start_time}.png")
                plt.savefig(plot_path, dpi=100, bbox_inches="tight")
                plt.close(fig)
                
                plot_paths.append(plot_path)
            except Exception as e:
                logger.error(f"Failed to generate plot for {col}: {e}")
        
        return plot_paths
    
    def __repr__(self) -> str:
        """String representation of the visualizer."""
        status = "active" if self.is_active else "inactive"
        categories = list(self.metrics_history.keys())
        return f"Visualizer(status={status}, categories={categories})"


class NaturalLanguageExplainer:
    """
    Natural language explainer for ML/AI training metrics.
    
    This class generates human-friendly natural language explanations
    of model training performance and issues.
    
    Attributes:
        is_active: Whether the explainer is active
    """
    
    def __init__(self):
        """Initialize the natural language explainer."""
        self.is_active = False
        logger.info("Natural language explainer initialized")
    
    def start(self):
        """Start the natural language explainer."""
        self.is_active = True
        logger.info("Natural language explainer started")
        return self
    
    def stop(self):
        """Stop the natural language explainer."""
        self.is_active = False
        logger.info("Natural language explainer stopped")
        return self
    
    def explain_metrics(self, metrics: Dict[str, Any], category: str = "general") -> str:
        """
        Generate natural language explanation of metrics.
        
        Args:
            metrics: Dictionary of metrics to explain
            category: Category of metrics
        
        Returns:
            Natural language explanation
        """
        if not self.is_active:
            return ""
        
        try:
            # Convert metrics to DataFrame if it's a list of metrics
            if isinstance(metrics, list):
                df = pd.DataFrame(metrics)
            else:
                # If it's a single metrics dict, convert to DataFrame with one row
                df = pd.DataFrame([metrics])
            
            # Generate explanation based on category
            if category == "memory":
                explanation = self._explain_memory_metrics(df)
            elif category == "timing":
                explanation = self._explain_timing_metrics(df)
            elif category == "gradient":
                explanation = self._explain_gradient_metrics(df)
            elif category == "dataloader":
                explanation = self._explain_dataloader_metrics(df)
            elif category == "hardware":
                explanation = self._explain_hardware_metrics(df)
            else:
                # Generic explanation for other categories
                explanation = self._explain_generic_metrics(category, df)
            
            return explanation
        
        except Exception as e:
            logger.error(f"Failed to generate explanation: {e}")
            return f"Error generating explanation: {str(e)}"
    
    def explain_warning(self, warning: Dict[str, Any]) -> str:
        """
        Generate natural language explanation of a warning.
        
        Args:
            warning: Warning dictionary
        
        Returns:
            Natural language explanation
        """
        if not self.is_active:
            return ""
        
        try:
            warning_type = warning.get("type", "unknown")
            severity = warning.get("severity", "medium")
            message = warning.get("message", "")
            details = warning.get("details", "")
            suggestions = warning.get("suggestions", [])
            
            # Start with severity indicator
            if severity == "critical":
                explanation = "🚨 CRITICAL ISSUE: "
            elif severity == "high":
                explanation = "⚠️ HIGH SEVERITY: "
            elif severity == "medium":
                explanation = "⚠️ WARNING: "
            else:
                explanation = "ℹ️ NOTICE: "
            
            # Add message and details
            explanation += message
            
            if details:
                explanation += f"\n\n{details}"
            
            # Add suggestions
            if suggestions:
                explanation += "\n\nRecommended actions:\n"
                for i, suggestion in enumerate(suggestions, 1):
                    explanation += f"{i}. {suggestion}\n"
            
            return explanation
        
        except Exception as e:
            logger.error(f"Failed to generate warning explanation: {e}")
            return f"Error generating explanation: {str(e)}"
    
    def explain_optimization(self, optimization: Dict[str, Any]) -> str:
        """
        Generate natural language explanation of an optimization.
        
        Args:
            optimization: Optimization dictionary
        
        Returns:
            Natural language explanation
        """
        if not self.is_active:
            return ""
        
        try:
            opt_type = optimization.get("type", "unknown")
            message = optimization.get("message", "")
            details = optimization.get("details", "")
            code = optimization.get("code", "")
            
            # Start with optimization type
            explanation = f"📈 OPTIMIZATION ({opt_type}): "
            
            # Add message and details
            explanation += message
            
            if details:
                explanation += f"\n\n{details}"
            
            # Add code example
            if code:
                explanation += "\n\nImplementation example:\n```python\n"
                explanation += code
                explanation += "\n```"
            
            return explanation
        
        except Exception as e:
            logger.error(f"Failed to generate optimization explanation: {e}")
            return f"Error generating explanation: {str(e)}"
    
    def _explain_memory_metrics(self, df: pd.DataFrame) -> str:
        """
        Generate explanation for memory metrics.
        
        Args:
            df: DataFrame of memory metrics
        
        Returns:
            Natural language explanation
        """
        explanation = "Memory Analysis: "
        
        # Check for memory usage
        if "allocated_memory" in df.columns:
            allocated = df["allocated_memory"].iloc[-1]
            explanation += f"Your model is currently using {allocated:.2f} MB of memory. "
            
            if "total_memory" in df.columns:
                total = df["total_memory"].iloc[-1]
                usage_pct = (allocated / total) * 100
                
                if usage_pct > 90:
                    explanation += f"This is {usage_pct:.1f}% of available memory, which is very high. "
                    explanation += "You're at risk of running out of memory. Consider reducing batch size or using gradient checkpointing. "
                elif usage_pct > 70:
                    explanation += f"This is {usage_pct:.1f}% of available memory, which is moderately high. "
                    explanation += "You should monitor memory usage closely. "
                else:
                    explanation += f"This is {usage_pct:.1f}% of available memory, which is acceptable. "
        
        # Check for memory fragmentation
        if "memory_fragmentation" in df.columns:
            fragmentation = df["memory_fragmentation"].iloc[-1] * 100
            
            if fragmentation > 30:
                explanation += f"Memory fragmentation is high at {fragmentation:.1f}%. "
                explanation += "This means memory is being used inefficiently. Consider calling torch.cuda.empty_cache() periodically. "
            else:
                explanation += f"Memory fragmentation is at an acceptable level ({fragmentation:.1f}%). "
        
        # Check for model size
        if "model_size" in df.columns:
            model_size = df["model_size"].iloc[-1]
            explanation += f"Your model size is {model_size:.2f} MB. "
        
        # Check for largest layer
        if "largest_layer_memory" in df.columns and "largest_layer_name" in df.columns:
            largest_layer = df["largest_layer_name"].iloc[-1]
            largest_size = df["largest_layer_memory"].iloc[-1]
            explanation += f"The largest layer is '{largest_layer}', consuming {largest_size:.2f} MB. "
        
        return explanation
    
    def _explain_timing_metrics(self, df: pd.DataFrame) -> str:
        """
        Generate explanation for timing metrics.
        
        Args:
            df: DataFrame of timing metrics
        
        Returns:
            Natural language explanation
        """
        explanation = "Performance Analysis: "
        
        # Check for timing breakdown
        timing_cols = [
            col for col in ["forward_time", "backward_time", "optimizer_time", "dataloader_time"]
            if col in df.columns
        ]
        
        if timing_cols:
            # Calculate average times
            avg_times = {col: df[col].iloc[-1] for col in timing_cols}
            
            # Find the bottleneck
            bottleneck = max(avg_times.items(), key=lambda x: x[1])
            total_time = sum(avg_times.values())
            
            if total_time > 0:
                bottleneck_pct = (bottleneck[1] / total_time) * 100
                
                explanation += f"The main bottleneck in your training loop is the {bottleneck[0].replace('_time', '')} phase, "
                explanation += f"which takes {bottleneck[1]:.4f}s ({bottleneck_pct:.1f}% of total time). "
                
                # Add specific advice based on bottleneck
                if bottleneck[0] == "forward_time":
                    explanation += "To improve forward pass performance, consider using torch.compile() or a more efficient model architecture. "
                elif bottleneck[0] == "backward_time":
                    explanation += "To improve backward pass performance, consider using gradient checkpointing or a more efficient model architecture. "
                elif bottleneck[0] == "optimizer_time":
                    explanation += "To improve optimizer performance, consider using a different optimizer or gradient accumulation. "
                elif bottleneck[0] == "dataloader_time":
                    explanation += "To improve dataloader performance, increase num_workers or use faster storage. "
        
        # Check for iterations per second
        if "iterations_per_second" in df.columns:
            ips = df["iterations_per_second"].iloc[-1]
            explanation += f"Your training speed is {ips:.2f} iterations per second. "
            
            if "total_time" in df.columns and df["total_time"].iloc[-1] > 0:
                explanation += f"Each iteration takes approximately {1/ips:.4f}s. "
        
        return explanation
    
    def _explain_gradient_metrics(self, df: pd.DataFrame) -> str:
        """
        Generate explanation for gradient metrics.
        
        Args:
            df: DataFrame of gradient metrics
        
        Returns:
            Natural language explanation
        """
        explanation = "Gradient Analysis: "
        
        # Check for gradient norms
        if "avg_grad_norm" in df.columns:
            avg_norm = df["avg_grad_norm"].iloc[-1]
            
            if avg_norm < 0.001:
                explanation += f"Your average gradient norm is very small ({avg_norm:.6f}), which may indicate vanishing gradients. "
                explanation += "This can slow down or stall training. Consider using batch normalization, residual connections, or different activation functions. "
            elif avg_norm > 10.0:
                explanation += f"Your average gradient norm is very large ({avg_norm:.4f}), which may indicate exploding gradients. "
                explanation += "This can cause training instability. Consider using gradient clipping or reducing the learning rate. "
            else:
                explanation += f"Your average gradient norm is {avg_norm:.4f}, which is within a normal range. "
        
        # Check for dead gradients
        if "dead_gradients_pct" in df.columns:
            dead_pct = df["dead_gradients_pct"].iloc[-1]
            
            if dead_pct > 20:
                explanation += f"{dead_pct:.1f}% of parameters have near-zero gradients, which indicates potential vanishing gradients or dead neurons. "
                explanation += "This can slow down or stall training in affected parts of the network. "
            elif dead_pct > 5:
                explanation += f"{dead_pct:.1f}% of parameters have near-zero gradients, which is slightly elevated but may not be problematic. "
            else:
                explanation += f"Only {dead_pct:.1f}% of parameters have near-zero gradients, which is normal. "
        
        # Check for exploding gradients
        if "exploding_gradients_pct" in df.columns:
            exploding_pct = df["exploding_gradients_pct"].iloc[-1]
            
            if exploding_pct > 10:
                explanation += f"{exploding_pct:.1f}% of parameters have very large gradients, which indicates exploding gradients. "
                explanation += "This can cause training instability or divergence. Consider using gradient clipping or reducing the learning rate. "
            elif exploding_pct > 2:
                explanation += f"{exploding_pct:.1f}% of parameters have large gradients, which is slightly elevated but may not be problematic. "
            else:
                explanation += f"Only {exploding_pct:.1f}% of parameters have large gradients, which is normal. "
        
        return explanation
    
    def _explain_dataloader_metrics(self, df: pd.DataFrame) -> str:
        """
        Generate explanation for dataloader metrics.
        
        Args:
            df: DataFrame of dataloader metrics
        
        Returns:
            Natural language explanation
        """
        explanation = "Dataloader Analysis: "
        
        # Check for batch loading time
        if "avg_batch_time" in df.columns:
            avg_time = df["avg_batch_time"].iloc[-1]
            
            if "batch_size" in df.columns:
                batch_size = df["batch_size"].iloc[-1]
                time_per_sample = avg_time / batch_size
                
                explanation += f"Your dataloader takes {avg_time:.4f}s per batch ({time_per_sample*1000:.2f}ms per sample) with batch size {int(batch_size)}. "
            else:
                explanation += f"Your dataloader takes {avg_time:.4f}s per batch. "
            
            if avg_time > 0.1:
                explanation += "This is relatively slow and may be a bottleneck. "
            elif avg_time > 0.01:
                explanation += "This is moderately fast. "
            else:
                explanation += "This is very fast. "
        
        # Check for worker utilization
        if "worker_utilization" in df.columns and "num_workers" in df.columns:
            utilization = df["worker_utilization"].iloc[-1]
            num_workers = df["num_workers"].iloc[-1]
            
            if utilization < 0.5 and num_workers > 1:
                explanation += f"Your dataloader workers are underutilized ({utilization*100:.1f}%). "
                explanation += f"You're currently using {int(num_workers)} workers, but fewer might be sufficient. "
            elif utilization > 0.9:
                explanation += f"Your dataloader workers are fully utilized ({utilization*100:.1f}%). "
                
                if "estimated_optimal_workers" in df.columns:
                    optimal = df["estimated_optimal_workers"].iloc[-1]
                    if optimal > num_workers:
                        explanation += f"Consider increasing from {int(num_workers)} to {int(optimal)} workers for better performance. "
            else:
                explanation += f"Your dataloader worker utilization is {utilization*100:.1f}%, which is reasonable. "
        
        return explanation
    
    def _explain_hardware_metrics(self, df: pd.DataFrame) -> str:
        """
        Generate explanation for hardware metrics.
        
        Args:
            df: DataFrame of hardware metrics
        
        Returns:
            Natural language explanation
        """
        explanation = "Hardware Analysis: "
        
        # Check for GPU utilization
        if "gpu_percent" in df.columns:
            gpu_util = df["gpu_percent"].iloc[-1]
            
            if gpu_util < 30:
                explanation += f"Your GPU utilization is very low ({gpu_util:.1f}%). "
                explanation += "This suggests your training is bottlenecked elsewhere, possibly by CPU processing or data loading. "
            elif gpu_util < 70:
                explanation += f"Your GPU utilization is moderate ({gpu_util:.1f}%). "
                explanation += "There may be room for optimization to increase GPU usage. "
            else:
                explanation += f"Your GPU utilization is high ({gpu_util:.1f}%), indicating good GPU usage. "
        
        # Check for CPU utilization
        if "cpu_percent" in df.columns:
            cpu_util = df["cpu_percent"].iloc[-1]
            
            if "gpu_percent" in df.columns:
                gpu_util = df["gpu_percent"].iloc[-1]
                
                if cpu_util > 80 and gpu_util < 50:
                    explanation += f"Your CPU utilization is high ({cpu_util:.1f}%) while GPU utilization is moderate ({gpu_util:.1f}%). "
                    explanation += "This suggests a CPU bottleneck. Consider increasing dataloader workers or reducing CPU preprocessing. "
                else:
                    explanation += f"Your CPU utilization is {cpu_util:.1f}%. "
            else:
                explanation += f"Your CPU utilization is {cpu_util:.1f}%. "
        
        # Check for GPU memory
        if "gpu_memory_percent" in df.columns:
            gpu_mem = df["gpu_memory_percent"].iloc[-1]
            
            if gpu_mem > 90:
                explanation += f"Your GPU memory utilization is very high ({gpu_mem:.1f}%). "
                explanation += "You're at risk of running out of memory. Consider reducing batch size or using memory optimization techniques. "
            elif gpu_mem > 70:
                explanation += f"Your GPU memory utilization is high ({gpu_mem:.1f}%). "
                explanation += "Monitor memory usage closely. "
            elif gpu_mem < 30:
                explanation += f"Your GPU memory utilization is low ({gpu_mem:.1f}%). "
                explanation += "You may be able to increase batch size for better performance. "
            else:
                explanation += f"Your GPU memory utilization is {gpu_mem:.1f}%, which is reasonable. "
        
        # Check for GPU temperature
        if "gpu_temperature" in df.columns:
            temp = df["gpu_temperature"].iloc[-1]
            
            if temp > 85:
                explanation += f"Your GPU temperature is very high ({temp:.1f}°C). "
                explanation += "This may lead to thermal throttling and reduced performance. Ensure proper cooling. "
            elif temp > 75:
                explanation += f"Your GPU temperature is high ({temp:.1f}°C) but within normal operating range. "
            else:
                explanation += f"Your GPU temperature is {temp:.1f}°C, which is normal. "
        
        return explanation
    
    def _explain_generic_metrics(self, category: str, df: pd.DataFrame) -> str:
        """
        Generate generic explanation for metrics.
        
        Args:
            category: Category of metrics
            df: DataFrame of metrics
        
        Returns:
            Natural language explanation
        """
        explanation = f"{category.capitalize()} Analysis: "
        
        # Get numeric columns
        numeric_cols = [col for col in df.columns if col != "timestamp" and pd.api.types.is_numeric_dtype(df[col])]
        
        if not numeric_cols:
            return explanation + "No numeric metrics available for analysis."
        
        # Add summary of each metric
        for col in numeric_cols[:3]:  # Limit to first 3 metrics to avoid too long explanations
            value = df[col].iloc[-1]
            
            # Check if we have historical data to analyze trend
            if len(df) > 1:
                first_value = df[col].iloc[0]
                change = value - first_value
                pct_change = (change / first_value) * 100 if first_value != 0 else float('inf')
                
                if abs(pct_change) < 1:
                    explanation += f"{col} is stable at {value:.4f}. "
                elif pct_change > 0:
                    explanation += f"{col} has increased by {pct_change:.1f}% to {value:.4f}. "
                else:
                    explanation += f"{col} has decreased by {abs(pct_change):.1f}% to {value:.4f}. "
            else:
                explanation += f"{col} is currently {value:.4f}. "
        
        # If there are more metrics, mention them
        if len(numeric_cols) > 3:
            explanation += f"There are {len(numeric_cols) - 3} more metrics in this category. "
        
        return explanation
    
    def __repr__(self) -> str:
        """String representation of the natural language explainer."""
        status = "active" if self.is_active else "inactive"
        return f"NaturalLanguageExplainer(status={status})"


class ReportGenerator:
    """
    Generator for comprehensive training reports.
    
    This class generates comprehensive reports of model training performance,
    including metrics, visualizations, and natural language explanations.
    
    Attributes:
        visualizer: Visualizer for generating plots
        explainer: Natural language explainer
        output_dir: Directory to save reports
        is_active: Whether the report generator is active
    """
    
    def __init__(
        self,
        visualizer: Optional[Visualizer] = None,
        explainer: Optional[NaturalLanguageExplainer] = None,
        output_dir: Optional[str] = None,
    ):
        """
        Initialize the report generator.
        
        Args:
            visualizer: Visualizer for generating plots
            explainer: Natural language explainer
            output_dir: Directory to save reports
        """
        self.visualizer = visualizer or Visualizer(output_dir)
        self.explainer = explainer or NaturalLanguageExplainer()
        self.output_dir = output_dir or os.path.join(os.getcwd(), "autopd_reports")
        os.makedirs(self.output_dir, exist_ok=True)
        
        self.is_active = False
        
        # Initialize timestamp for report naming
        self.start_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        logger.info(f"Report generator initialized with output directory: {self.output_dir}")
    
    def start(self):
        """Start the report generator."""
        self.is_active = True
        self.visualizer.start()
        self.explainer.start()
        logger.info("Report generator started")
        return self
    
    def stop(self):
        """Stop the report generator."""
        self.is_active = False
        self.visualizer.stop()
        self.explainer.stop()
        logger.info("Report generator stopped")
        return self
    
    def update_metrics(self, metrics: Dict[str, Any], category: str = "general"):
        """
        Update metrics for report generation.
        
        Args:
            metrics: Dictionary of metrics to update
            category: Category of metrics
        """
        if not self.is_active:
            return
        
        self.visualizer.update_metrics(metrics, category)
    
    def generate_report(
        self,
        include_plots: bool = True,
        include_dashboard: bool = True,
        output_path: Optional[str] = None,
    ) -> str:
        """
        Generate a comprehensive training report.
        
        Args:
            include_plots: Whether to include plots in the report
            include_dashboard: Whether to include an interactive dashboard
            output_path: Path to save the report
        
        Returns:
            Path to the generated report
        """
        if not self.is_active:
            return ""
        
        if output_path is None:
            output_path = os.path.join(
                self.output_dir, f"training_report_{self.start_time}.md"
            )
        
        try:
            # Generate report content
            report_content = self._generate_report_content(include_plots, include_dashboard)
            
            # Save to file
            with open(output_path, "w") as f:
                f.write(report_content)
            
            logger.info(f"Generated report at {output_path}")
            
            # Generate dashboard if requested
            if include_dashboard:
                dashboard_path = self.visualizer.generate_dashboard()
                logger.info(f"Generated dashboard at {dashboard_path}")
            
            return output_path
        
        except Exception as e:
            logger.error(f"Failed to generate report: {e}")
            return ""
    
    def _generate_report_content(self, include_plots: bool, include_dashboard: bool) -> str:
        """
        Generate the content of the training report.
        
        Args:
            include_plots: Whether to include plots in the report
            include_dashboard: Whether to include an interactive dashboard
        
        Returns:
            Markdown formatted report content
        """
        report = "# AutoPipelineDoctor Training Report\n\n"
        report += f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        
        # Add summary section
        report += "## Summary\n\n"
        report += self._generate_summary_section()
        
        # Add dashboard link if requested
        if include_dashboard:
            dashboard_path = self.visualizer.generate_dashboard()
            if dashboard_path:
                report += f"\n\n[View Interactive Dashboard]({os.path.relpath(dashboard_path, os.path.dirname(output_path))})\n\n"
        
        # Add sections for each metric category
        for category, metrics_list in self.visualizer.metrics_history.items():
            if not metrics_list:
                continue
            
            report += f"## {category.capitalize()} Metrics\n\n"
            
            # Add natural language explanation
            report += "### Analysis\n\n"
            explanation = self.explainer.explain_metrics(metrics_list[-1], category)
            report += explanation + "\n\n"
            
            # Convert metrics list to DataFrame
            df = pd.DataFrame(metrics_list)
            
            # Generate statistics for numeric columns
            numeric_cols = [col for col in df.columns if col != "timestamp" and pd.api.types.is_numeric_dtype(df[col])]
            
            if numeric_cols:
                report += "### Statistics\n\n"
                report += "| Metric | Mean | Min | Max | Last |\n"
                report += "|--------|------|-----|-----|------|\n"
                
                for col in numeric_cols:
                    mean_val = df[col].mean()
                    min_val = df[col].min()
                    max_val = df[col].max()
                    last_val = df[col].iloc[-1]
                    
                    report += f"| {col} | {mean_val:.4f} | {min_val:.4f} | {max_val:.4f} | {last_val:.4f} |\n"
                
                report += "\n"
            
            # Generate plots for this category if requested
            if include_plots:
                plot_paths = self.visualizer._generate_category_plots(category, df)
                if plot_paths:
                    report += f"### Plots\n\n"
                    for plot_path in plot_paths:
                        report += f"![{category} Metrics]({os.path.relpath(plot_path, os.path.dirname(output_path))})\n\n"
        
        # Add recommendations section
        report += "## Recommendations\n\n"
        report += self.visualizer._generate_recommendations()
        
        return report
    
    def _generate_summary_section(self) -> str:
        """
        Generate the summary section of the report.
        
        Returns:
            Markdown formatted summary section
        """
        return self.visualizer._generate_summary_section()
    
    def generate_alert(
        self,
        warning: Dict[str, Any],
        include_plots: bool = True,
        output_path: Optional[str] = None,
    ) -> str:
        """
        Generate an alert report for a warning.
        
        Args:
            warning: Warning dictionary
            include_plots: Whether to include plots in the alert
            output_path: Path to save the alert
        
        Returns:
            Path to the generated alert
        """
        if not self.is_active:
            return ""
        
        if output_path is None:
            warning_type = warning.get("type", "alert")
            output_path = os.path.join(
                self.output_dir, f"{warning_type}_alert_{self.start_time}.md"
            )
        
        try:
            # Generate alert content
            alert_content = self._generate_alert_content(warning, include_plots)
            
            # Save to file
            with open(output_path, "w") as f:
                f.write(alert_content)
            
            logger.info(f"Generated alert at {output_path}")
            return output_path
        
        except Exception as e:
            logger.error(f"Failed to generate alert: {e}")
            return ""
    
    def _generate_alert_content(self, warning: Dict[str, Any], include_plots: bool) -> str:
        """
        Generate the content of the alert report.
        
        Args:
            warning: Warning dictionary
            include_plots: Whether to include plots in the alert
        
        Returns:
            Markdown formatted alert content
        """
        warning_type = warning.get("type", "unknown")
        severity = warning.get("severity", "medium")
        
        # Set title based on severity
        if severity == "critical":
            alert = "# 🚨 CRITICAL ALERT: "
        elif severity == "high":
            alert = "# ⚠️ HIGH SEVERITY ALERT: "
        elif severity == "medium":
            alert = "# ⚠️ WARNING: "
        else:
            alert = "# ℹ️ NOTICE: "
        
        # Add warning message
        alert += warning.get("message", f"{warning_type} issue detected") + "\n\n"
        
        # Add timestamp
        alert += f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        
        # Add details
        alert += "## Details\n\n"
        alert += warning.get("details", "No additional details available.") + "\n\n"
        
        # Add natural language explanation
        alert += "## Analysis\n\n"
        explanation = self.explainer.explain_warning(warning)
        alert += explanation + "\n\n"
        
        # Add suggestions
        suggestions = warning.get("suggestions", [])
        if suggestions:
            alert += "## Recommended Actions\n\n"
            for i, suggestion in enumerate(suggestions, 1):
                alert += f"{i}. {suggestion}\n"
            alert += "\n"
        
        # Add plots if requested and available
        if include_plots:
            # Determine which category to use for plots based on warning type
            category_map = {
                "oom": "memory",
                "memory": "memory",
                "overfitting": "gradient",
                "underfitting": "gradient",
                "vanishing_gradients": "gradient",
                "exploding_gradients": "gradient",
                "dataloader": "dataloader",
                "scaling_inefficiency": "timing",
            }
            
            category = category_map.get(warning_type, "general")
            
            if category in self.visualizer.metrics_history and self.visualizer.metrics_history[category]:
                df = pd.DataFrame(self.visualizer.metrics_history[category])
                plot_paths = self.visualizer._generate_category_plots(category, df)
                
                if plot_paths:
                    alert += "## Diagnostic Plots\n\n"
                    for plot_path in plot_paths:
                        alert += f"![{category} Metrics]({os.path.relpath(plot_path, os.path.dirname(output_path))})\n\n"
        
        return alert
    
    def __repr__(self) -> str:
        """String representation of the report generator."""
        status = "active" if self.is_active else "inactive"
        return f"ReportGenerator(status={status})"
