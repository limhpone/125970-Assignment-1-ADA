import pandas as pd
import numpy as np

# Analyze exhaustive results
df_ex = pd.read_csv('results/exhaustive_results.csv')

print("=" * 60)
print("EXHAUSTIVE RESULTS ANALYSIS")
print("=" * 60)

for alpha in sorted(df_ex['alpha'].unique()):
    subset = df_ex[df_ex['alpha'] == alpha]
    print(f"\n\nAlpha = {alpha} (n={sorted(subset['n'].unique())})")
    print("-" * 40)
    
    eft_ratio = (subset['greedy_EFT_count'] / subset['opt_count']).mean()
    est_ratio = (subset['greedy_EST_count'] / subset['opt_count']).mean()
    sd_ratio = (subset['greedy_SD_count'] / subset['opt_count']).mean()
    
    print(f"  EFT approximation ratio: {eft_ratio:.4f} (perfect={eft_ratio==1.0})")
    print(f"  EST approximation ratio: {est_ratio:.4f}")
    print(f"  SD  approximation ratio: {sd_ratio:.4f}")
    
    # Check EFT optimality
    eft_optimal = (subset['greedy_EFT_count'] == subset['opt_count']).all()
    print(f"\n  EFT always optimal: {eft_optimal}")
    print(f"  EST matches optimal: {(subset['greedy_EST_count'] == subset['opt_count']).sum()}/{len(subset)} cases")
    print(f"  SD matches optimal:  {(subset['greedy_SD_count'] == subset['opt_count']).sum()}/{len(subset)} cases")

# Analyze greedy results - runtime scaling
print("\n\n" + "=" * 60)
print("GREEDY RUNTIME ANALYSIS")
print("=" * 60)

df_gr = pd.read_csv('results/greedy_results.csv')

for alpha in sorted(df_gr['alpha'].unique()):
    subset = df_gr[df_gr['alpha'] == alpha]
    grouped = subset.groupby('n').agg({
        't_EFT': 'mean',
        't_EST': 'mean',
        't_SD': 'mean'
    })
    
    print(f"\n\nAlpha = {alpha}")
    print("-" * 40)
    print(f"{'n':<10} {'EFT (s)':<12} {'EST (s)':<12} {'SD (s)':<12}")
    print("-" * 40)
    for n in sorted(grouped.index):
        print(f"{n:<10} {grouped.loc[n, 't_EFT']:.6f}    {grouped.loc[n, 't_EST']:.6f}    {grouped.loc[n, 't_SD']:.6f}")

# Exhaustive runtime scaling
print("\n\n" + "=" * 60)
print("EXHAUSTIVE RUNTIME SCALING")
print("=" * 60)

for alpha in sorted(df_ex['alpha'].unique()):
    subset = df_ex[df_ex['alpha'] == alpha]
    grouped = subset.groupby('n')['t_exhaustive'].mean()
    
    print(f"\nAlpha = {alpha}")
    print("-" * 40)
    for n in sorted(grouped.index):
        print(f"  n={n:2d}: {grouped[n]:.6f} seconds")
