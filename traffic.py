import pandas as pd
import numpy as np
from scipy.spatial import distance_matrix

SHELF_WIDTH = 400         
NUM_LEVELS = 5            
DAILY_CUSTOMERS = 500
TRAFFIC_MULT = 1.30       

# level multipliers (Lambda_i) impulse
LEVEL_MULTS = {1: 0.6, 2: 0.9, 3: 1.5, 4: 1.1, 5: 0.8}

# storage mapping (Category -> Storage Type)
# R = Fridge, F = Freezer, S = Standard Shelf
STORAGE_MAP = {
    'Dairy': 'R', 'Seafood': 'F', 'Fruits & Vegetables': 'S', 'Bakery': 'S', 'Beverages': 'S', 'Grains & Pulses': 'S', 'Oils & Fats': 'S', 'Snacks': 'S'
}

# what drives people to high traffic routes (essential items - can edit this to just was a randomly generated list form search)
ESSENTIALS = ['Milk', 'Cheese', 'Eggs', 'Bread', 'Banana', 'Potato', 'Rice', 'Water', 'Soda', 'Fish']

# supplementary product data (sets S', R', F', T)
df_prods = pd.read_csv('processed_optimization_data.csv')

# map storage types with the different categories
df_prods['storage_type'] = df_prods['Category'].map(STORAGE_MAP).fillna('S')

# identify essentials
df_prods['is_essential'] = df_prods['Product_Name'].apply(
    lambda x: 1 if any(k.lower() in str(x).lower() for k in ESSENTIALS) else 0
)

# export supplement
df_prods[['Product_Name', 'storage_type', 'is_essential']].to_csv('env_product_supplement.csv', index=False)
print("created 'env_product_supplement.csv'") # storage type and whether the product is an essential driving traffic

# shelf layout generation (sets S, R, F & locations)
# simulating a store map in a (x,y) coordinate fashion and taking the store entrance (assuming one entrance) as (0,0)

shelves = []
sid = 1

# center aisles (type S) 
# 3 aisles, 4 sections deep = 24 standard shelf units
for a in range(1, 4):
    x_base = a * 25
    for s in range(1, 5):
        y_pos = s * 10
        shelves.append({'Shelf_ID': sid, 'Type': 'S', 'X': x_base, 'Y': y_pos}); sid += 1
        shelves.append({'Shelf_ID': sid, 'Type': 'S', 'X': x_base+3, 'Y': y_pos}); sid += 1

# perimeter fridges (type R) - top wall
# 9 fridge units for Dairy/Meat
for x in range(10, 100, 10):
    shelves.append({'Shelf_ID': sid, 'Type': 'R', 'X': x, 'Y': 60}); sid += 1

# perimeter freezers (type F) - right wall
# creating only 2 freezer units as seafood is our only freezer item
for y in range(10, 30, 10):
    shelves.append({'Shelf_ID': sid, 'Type': 'F', 'X': 100, 'Y': y}); sid += 1

df_shelves = pd.DataFrame(shelves)

# shelf constraints & distance from entrance
df_shelves['Width_W'] = SHELF_WIDTH
df_shelves['Levels_N'] = NUM_LEVELS
df_shelves['DIST_b'] = np.sqrt(df_shelves['X']**2 + df_shelves['Y']**2).round(2)

df_shelves.to_csv('env_shelves.csv', index=False)
print("created 'env_shelves.csv'")

# distance matrix (delta parameter)
coords = df_shelves[['X', 'Y']].values
dist_matrix = distance_matrix(coords, coords)

np.savetxt("env_distance_matrix.csv", dist_matrix, delimiter=",")
print("created 'env_distance_matrix.csv'")

# global scalars making it easier in the gurobi (can just edit these values here and re-run the script for a change in data)
scalars = {
    'Key': ['Theta', 'Tau'] + [f'Lambda_{k}' for k in LEVEL_MULTS.keys()],
    'Value': [DAILY_CUSTOMERS, TRAFFIC_MULT] + list(LEVEL_MULTS.values())
}
pd.DataFrame(scalars).to_csv('env_scalars.csv', index=False)
print("create 'env_scalars.csv'")