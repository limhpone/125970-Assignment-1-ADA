# Run experiments individually
# More flexible and safer than running all at once

import os
import sys

def show_menu():
    print("\n" + "="*50)
    print("Interval Scheduling Experiments")
    print("="*50)
    print("\n1. Run Greedy Algorithms (~10-15 min)")
    print("2. Run Exhaustive Algorithm (~5-10 min)")
    print("3. Run Quality Analysis (~10-15 min)")
    print("4. Generate All Plots")
    print("5. Run Everything (Full Experiment)")
    print("6. Check Results Status")
    print("0. Exit")
    print("\n" + "="*50)

def check_results():
    print("\nChecking results folder...")
    
    if not os.path.exists('results'):
        print("❌ No results folder found")
        return
    
    files = {
        'greedy_results.json': 'Greedy results',
        'exhaustive_results.json': 'Exhaustive results',
        'quality_results.json': 'Quality analysis results'
    }
    
    plots = [
        'greedy_runtime_loglog_alpha_0.1.png',
        'greedy_runtime_loglog_alpha_1.png',
        'greedy_runtime_loglog_alpha_5.png',
        'greedy_normalized_alpha_0.1.png',
        'greedy_normalized_alpha_1.png',
        'greedy_normalized_alpha_5.png',
        'exhaustive_runtime.png',
        'exhaustive_normalized.png',
        'solution_quality_alpha_0.1.png',
        'solution_quality_alpha_1.png',
        'solution_quality_alpha_5.png'
    ]
    
    print("\nData Files:")
    for file, desc in files.items():
        path = os.path.join('results', file)
        if os.path.exists(path):
            size = os.path.getsize(path)
            print(f"  ✓ {desc}: {size/1024:.1f} KB")
        else:
            print(f"  ✗ {desc}: Not found")
    
    print("\nPlot Files:")
    plot_count = 0
    for plot in plots:
        path = os.path.join('results', plot)
        if os.path.exists(path):
            plot_count += 1
    print(f"  {plot_count}/11 plots generated")
    
    if plot_count == 11:
        print("\n✓ All experiments complete! Ready for report.")
    elif plot_count > 0:
        print("\n⚠ Partial results. Run missing experiments.")
    else:
        print("\n✗ No plots found. Run experiments first.")

def run_stage(stage):
    if stage == 1:
        from main import run_greedy_experiments
        print("\nRunning Greedy Experiments...")
        run_greedy_experiments()
        print("✓ Greedy experiments complete\n")
    
    elif stage == 2:
        from main import run_exhaustive_experiments
        print("\nRunning Exhaustive Algorithm...")
        run_exhaustive_experiments()
        print("✓ Exhaustive experiments complete\n")
    
    elif stage == 3:
        from main import run_solution_quality_analysis
        print("\nRunning Quality Analysis...")
        run_solution_quality_analysis()
        print("✓ Quality analysis complete\n")
    
    elif stage == 4:
        print("\nGenerating plots from existing data...")
        import json
        from src.plotting import (
            plot_greedy_runtime_loglog,
            plot_greedy_normalized_runtime,
            plot_exhaustive_runtime,
            plot_exhaustive_normalized_runtime,
            plot_solution_quality
        )
        
        # Load data
        try:
            with open('results/greedy_results.json') as f:
                greedy = json.load(f)
                # Convert string keys back to numbers
                greedy = {float(k): {int(n): v for n, v in vals.items()} 
                         for k, vals in greedy.items()}
            plot_greedy_runtime_loglog(greedy)
            plot_greedy_normalized_runtime(greedy)
            print("✓ Greedy plots generated")
        except FileNotFoundError:
            print("✗ Greedy results not found")
        
        try:
            with open('results/exhaustive_results.json') as f:
                exhaustive = json.load(f)
                exhaustive = {float(k): {int(n): v for n, v in vals.items()} 
                             for k, vals in exhaustive.items()}
            plot_exhaustive_runtime(exhaustive)
            plot_exhaustive_normalized_runtime(exhaustive)
            print("✓ Exhaustive plots generated")
        except FileNotFoundError:
            print("✗ Exhaustive results not found")
        
        try:
            with open('results/quality_results.json') as f:
                quality = json.load(f)
                quality = {float(k): {int(n): v for n, v in vals.items()} 
                          for k, vals in quality.items()}
            plot_solution_quality(quality)
            print("✓ Quality plots generated")
        except FileNotFoundError:
            print("✗ Quality results not found")
    
    elif stage == 5:
        from main import main
        main()

def main_menu():
    while True:
        show_menu()
        try:
            choice = input("\nEnter choice (0-6): ").strip()
            
            if choice == '0':
                print("\nExiting...")
                break
            
            elif choice == '6':
                check_results()
                input("\nPress Enter to continue...")
            
            elif choice in ['1', '2', '3', '4', '5']:
                run_stage(int(choice))
                input("\nPress Enter to continue...")
            
            else:
                print("Invalid choice. Try again.")
        
        except KeyboardInterrupt:
            print("\n\nExperiment cancelled by user.")
            sys.exit(0)
        except Exception as e:
            print(f"\nError: {e}")
            input("\nPress Enter to continue...")

if __name__ == "__main__":
    main_menu()
