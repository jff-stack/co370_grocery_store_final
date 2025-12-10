import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# --------------------------
# 1. Load Data
# --------------------------
try:
    df_shelves = pd.read_csv('env_shelves.csv')
    dist_matrix = np.loadtxt('env_distance_matrix.csv', delimiter=',')
    df_scalars = pd.read_csv('env_scalars.csv')
    print("Data loaded successfully.")
except FileNotFoundError:
    print("Error: CSV files not found. Please run your generation script first.")
    exit()

# --------------------------
# 2. Plotting the Store Layout
# --------------------------
def plot_store_layout(df):
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Define colors/markers for storage types
    type_colors = {'S': '#d95f02', 'R': '#1f77b4', 'F': '#17becf'} # Orange (Shelf), Blue (Fridge), Cyan (Freezer)
    type_labels = {'S': 'Standard Shelf', 'R': 'Fridge (Dairy/Meat)', 'F': 'Freezer (Seafood)'}
    
    # Plot Entrance
    ax.scatter(0, 0, c='gold', s=300, marker='*', edgecolors='black', label='Entrance (0,0)', zorder=10)
    
    # Plot Shelves by Type
    for stype, color in type_colors.items():
        subset = df[df['Type'] == stype]
        if not subset.empty:
            ax.scatter(subset['X'], subset['Y'], c=color, s=150, 
                       label=type_labels[stype], edgecolors='black', alpha=0.8)
            
            # Annotate Shelf IDs
            for _, row in subset.iterrows():
                ax.text(row['X'], row['Y'], str(int(row['Shelf_ID'])), 
                        fontsize=8, ha='center', va='center', color='white', fontweight='bold')

    # Highlight High Demand Zones (Red Halo)
    high_demand = df[df['is_high_demand'] == 1]
    ax.scatter(high_demand['X'], high_demand['Y'], s=300, facecolors='none', 
               edgecolors='red', linewidth=2, linestyle='--', label='High Demand Zone')

    # Formatting
    ax.set_title(f"Store Environment Map\n(Generated from {len(df)} shelves)", fontsize=16)
    ax.set_xlabel("Store Width (X Coordinates)")
    ax.set_ylabel("Store Depth (Y Coordinates)")
    ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    ax.grid(True, linestyle=':', alpha=0.6)
    ax.set_aspect('equal')
    
    plt.tight_layout()
    plt.show()

# --------------------------
# 3. Plotting Distance Matrix Heatmap
# --------------------------
def plot_distance_heatmap(matrix):
    plt.figure(figsize=(10, 8))
    sns.heatmap(matrix, cmap="viridis", square=True, cbar_kws={'label': 'Distance (Euclidean)'})
    plt.title("Shelf-to-Shelf Distance Matrix Heatmap")
    plt.xlabel("Shelf ID Index")
    plt.ylabel("Shelf ID Index")
    plt.show()

# --------------------------
# 4. Visualizing Parameters (Multipliers)
# --------------------------
def plot_parameters(df_scal):
    # Filter for Lambda (Level Multipliers)
    lambdas = df_scal[df_scal['Key'].str.contains('Lambda')]
    
    if not lambdas.empty:
        plt.figure(figsize=(8, 5))
        # Clean string to get level number
        levels = lambdas['Key'].str.replace('Lambda_', '')
        values = lambdas['Value']
        
        bars = plt.bar(levels, values, color='skyblue', edgecolor='black')
        plt.title("Impulse Multipliers by Shelf Level")
        plt.xlabel("Shelf Level")
        plt.ylabel("Multiplier Value")
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        
        # Add values on top of bars
        for bar in bars:
            yval = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2, yval + 0.02, round(yval, 2), ha='center', va='bottom')
            
        plt.show()

# --------------------------
# Run Visualizations
# --------------------------
plot_store_layout(df_shelves)
plot_distance_heatmap(dist_matrix)
plot_parameters(df_scalars)