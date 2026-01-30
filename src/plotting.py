"""
Plotting Utilities for Interval Scheduling Analysis
Generates publication-quality plots for the report.
"""

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, List
import os


# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (10, 6)
plt.rcParams['font.size'] = 11


def plot_greedy_runtime_loglog(results: Dict, output_dir: str = "results"):
    """
    Plot greedy algorithm runtime on log-log scale.
    Expected: linear trend indicating O(n log n).
    
    Args:
        results: Benchmark results from benchmark_greedy_algorithms
        output_dir: Directory to save plots
    """
    os.makedirs(output_dir, exist_ok=True)
    
    algorithms = ['EFT', 'EST', 'SD']
    colors = ['blue', 'green', 'red']
    
    for alpha in results.keys():
        fig, ax = plt.subplots(figsize=(10, 6))
        
        for alg, color in zip(algorithms, colors):
            n_values = []
            mean_times = []
            std_times = []
            
            for n in sorted(results[alpha].keys()):
                if alg in results[alpha][n]:
                    n_values.append(n)
                    mean_times.append(results[alpha][n][alg]['mean'])
                    std_times.append(results[alpha][n][alg]['std'])
            
            n_values = np.array(n_values)
            mean_times = np.array(mean_times)
            std_times = np.array(std_times)
            
            ax.loglog(n_values, mean_times, 'o-', color=color, label=alg, linewidth=2, markersize=6)
            ax.fill_between(n_values, 
                          mean_times - std_times, 
                          mean_times + std_times, 
                          alpha=0.2, color=color)
        
        ax.set_xlabel('Input Size (n)', fontsize=12, fontweight='bold')
        ax.set_ylabel('Runtime (seconds)', fontsize=12, fontweight='bold')
        ax.set_title(f'Greedy Algorithms Runtime (α = {alpha})', fontsize=14, fontweight='bold')
        ax.legend(fontsize=11)
        ax.grid(True, alpha=0.3)
        
        filename = f"greedy_runtime_loglog_alpha_{alpha}.png"
        plt.savefig(os.path.join(output_dir, filename), dpi=300, bbox_inches='tight')

        plt.close()


def plot_greedy_normalized_runtime(results: Dict, output_dir: str = "results"):
    """
    Plot normalized runtime: t(n) / (n log n).
    Should approach a constant for O(n log n) algorithms.
    
    Args:
        results: Benchmark results
        output_dir: Directory to save plots
    """
    os.makedirs(output_dir, exist_ok=True)
    
    algorithms = ['EFT', 'EST', 'SD']
    colors = ['blue', 'green', 'red']
    
    for alpha in results.keys():
        fig, ax = plt.subplots(figsize=(10, 6))
        
        for alg, color in zip(algorithms, colors):
            n_values = []
            normalized_times = []
            
            for n in sorted(results[alpha].keys()):
                if alg in results[alpha][n]:
                    mean_time = results[alpha][n][alg]['mean']
                    normalized = mean_time / (n * np.log2(n))
                    n_values.append(n)
                    normalized_times.append(normalized)
            
            ax.plot(n_values, normalized_times, 'o-', color=color, label=alg, linewidth=2, markersize=6)
        
        ax.set_xlabel('Input Size (n)', fontsize=12, fontweight='bold')
        ax.set_ylabel('t(n) / (n log n)', fontsize=12, fontweight='bold')
        ax.set_title(f'Normalized Greedy Runtime (α = {alpha})', fontsize=14, fontweight='bold')
        ax.legend(fontsize=11)
        ax.grid(True, alpha=0.3)
        ax.set_xscale('log')
        
        filename = f"greedy_normalized_alpha_{alpha}.png"
        plt.savefig(os.path.join(output_dir, filename), dpi=300, bbox_inches='tight')

        plt.close()


def plot_exhaustive_runtime(results: Dict, output_dir: str = "results"):
    """
    Plot exhaustive algorithm runtime vs n.
    Expected: exponential growth.
    
    Args:
        results: Benchmark results from benchmark_exhaustive_algorithm
        output_dir: Directory to save plots
    """
    os.makedirs(output_dir, exist_ok=True)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    colors = {'0.1': 'blue', '1': 'green', '5': 'red'}
    
    for alpha in results.keys():
        n_values = []
        mean_times = []
        std_times = []
        
        for n in sorted(results[alpha].keys()):
            n_values.append(n)
            mean_times.append(results[alpha][n]['mean'])
            std_times.append(results[alpha][n]['std'])
        
        n_values = np.array(n_values)
        mean_times = np.array(mean_times)
        std_times = np.array(std_times)
        
        color = colors.get(str(alpha), 'black')
        ax.semilogy(n_values, mean_times, 'o-', color=color, label=f'α = {alpha}', 
                   linewidth=2, markersize=6)
        ax.fill_between(n_values, 
                       mean_times - std_times, 
                       mean_times + std_times, 
                       alpha=0.2, color=color)
    
    ax.set_xlabel('Input Size (n)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Runtime (seconds, log scale)', fontsize=12, fontweight='bold')
    ax.set_title('Exhaustive Algorithm Runtime', fontsize=14, fontweight='bold')
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3)
    
    filename = "exhaustive_runtime.png"
    plt.savefig(os.path.join(output_dir, filename), dpi=300, bbox_inches='tight')

    plt.close()


def plot_exhaustive_normalized_runtime(results: Dict, output_dir: str = "results"):
    """
    Plot normalized exhaustive runtime: t(n) / (n·2^n).
    
    Args:
        results: Benchmark results
        output_dir: Directory to save plots
    """
    os.makedirs(output_dir, exist_ok=True)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    colors = {'0.1': 'blue', '1': 'green', '5': 'red'}
    
    for alpha in results.keys():
        n_values = []
        normalized_times = []
        
        for n in sorted(results[alpha].keys()):
            mean_time = results[alpha][n]['mean']
            # Normalize by n * 2^n
            normalized = mean_time / (n * (2 ** n))
            n_values.append(n)
            normalized_times.append(normalized)
        
        color = colors.get(str(alpha), 'black')
        ax.plot(n_values, normalized_times, 'o-', color=color, label=f'α = {alpha}', 
               linewidth=2, markersize=6)
    
    ax.set_xlabel('Input Size (n)', fontsize=12, fontweight='bold')
    ax.set_ylabel('t(n) / (n · 2^n)', fontsize=12, fontweight='bold')
    ax.set_title('Normalized Exhaustive Runtime', fontsize=14, fontweight='bold')
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3)
    
    filename = "exhaustive_normalized.png"
    plt.savefig(os.path.join(output_dir, filename), dpi=300, bbox_inches='tight')

    plt.close()


def plot_solution_quality(quality_results: Dict, output_dir: str = "results"):
    """
    Plot solution quality comparison: greedy vs optimal.
    
    Args:
        quality_results: Dictionary with format {alpha: {n: {alg: ratio}}}
        output_dir: Directory to save plots
    """
    os.makedirs(output_dir, exist_ok=True)
    
    algorithms = ['EFT', 'EST', 'SD']
    colors = ['blue', 'green', 'red']
    
    for alpha in quality_results.keys():
        fig, ax = plt.subplots(figsize=(10, 6))
        
        for alg, color in zip(algorithms, colors):
            n_values = []
            quality_ratios = []
            
            for n in sorted(quality_results[alpha].keys()):
                if alg in quality_results[alpha][n]:
                    n_values.append(n)
                    quality_ratios.append(quality_results[alpha][n][alg])
            
            ax.plot(n_values, quality_ratios, 'o-', color=color, label=alg, 
                   linewidth=2, markersize=6)
        
        ax.set_xlabel('Input Size (n)', fontsize=12, fontweight='bold')
        ax.set_ylabel('Quality Ratio (greedy / optimal)', fontsize=12, fontweight='bold')
        ax.set_title(f'Solution Quality Comparison (α = {alpha})', fontsize=14, fontweight='bold')
        ax.legend(fontsize=11)
        ax.grid(True, alpha=0.3)
        ax.set_ylim([0, 1.1])
        ax.axhline(y=1.0, color='black', linestyle='--', alpha=0.5, label='Optimal')
        
        filename = f"solution_quality_alpha_{alpha}.png"
        plt.savefig(os.path.join(output_dir, filename), dpi=300, bbox_inches='tight')

        plt.close()


if __name__ == "__main__":
    print("Plotting module loaded. Use functions to generate plots from benchmark results.")
