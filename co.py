import pandas as pd
import numpy as np

df = pd.read_csv('cleaned_dataset2.csv')
np.random.seed(42)

df['Unit_Price'] = pd.to_numeric(df['Unit_Price'].astype(str).str.replace('$', ''), errors='coerce')

# Profit (rho): Price * 30% Profit Margin
df['rho'] = df['Unit_Price'] * 0.03

# Demand (delta) = Product Sales / Total Store Sales
df['delta'] = df['Sales_Volume'] / df['Sales_Volume'].sum()

high_impulse_products = ['Butter Biscuit', 'Chocolate Biscuit', 'Icecream', 'Vanilla Biscuit', 
                'Soda', 'Pretzels', 'Popcorn', 'Potato Chips'] 

# Create a mask for high impulse products
is_high_impulse = df['Product_Name'].isin(high_impulse_products)

# Use np.where to assign values (Vectorized approach)
df['iota'] = np.where(is_high_impulse, 1.25 * df['delta'], 0.25 * df['delta'])

# Slotting Fees (omega, omega_prime) --> 1) Create Base Slotting Fee, 2) omega = base fee * shelf attractiveness 3) omega_prime = omega * traffic attractivness
num_shelves = 5
shelves = range(1, num_shelves + 1)
shelf_quality = {1: 0.6, 2: 0.9, 3: 1.5, 4: 1.1, 5: 0.8} 
traffic_multiplier = 1.30

omega = {}       
omega_prime = {} 

for shelf in shelves:
    base_fees = np.random.uniform(100, 200, size=len(df))
    w_values = np.round(base_fees * shelf_quality[shelf], 2)
    w_prime_values = np.round(w_values * traffic_multiplier, 2)

    df[f'omega_level_{shelf}'] = np.where(df['Supplier_Name'] == 'No_Name', 0, w_values)
    df[f'omega_prime_level_{shelf}'] = np.where(df['Supplier_Name'] == 'No_Name', 0, w_prime_values)

# Units per Display (mu), Min (l_p) & Max (v_p) Displays per Product
df['mu'] = np.where(df['Sales_Volume'] > df['Sales_Volume'].median(), 12, 6) #going by logic that if product is high selling, gets more units in a display
df['min_l'] = np.random.choice(
    [1, 2, 3],    #to keep the minimum to be more realistic, keep it to a range of 1-3
    size=len(df),   
    p=[0.6, 0.3, 0.1]) # more skewed to having a min of 1 display per product 
target_inventory = df['Reorder_Level'] + df['Reorder_Quantity'] #this is the assumed max inventory we would carry, hence target
df['max_v'] = np.floor(target_inventory / df['mu']).astype(int)

df['min_l'] = np.where(df['min_l'] > df['max_v'], df['max_v'], df['min_l'])
# Space per Display (zeta): avg width of product in each category (rather than define every product's width) * number of facings in display based
#                                                                                                                                       on # units in display
#                                                                                                        (i.e. if mu = 12 units, then 2 facings if display 
#                                                                                                                                                  has depth of 6)
width_map_cm = {
    'Dairy': 10,   
    'Seafood': 20,
    'Fruits & Vegetables': 7,
    'Grains & Pulses': 9,
    'Bakery': 15,
    'Snacks': 12,
    'Beverages': 8,
    'Oils & Fats': 9
}
df['unit_width_cm'] = df['Category'].map(width_map_cm)

#Calculate Zeta (Space per Display)
df['facings_per_display'] = np.where(df['mu'] == 12, 2, 1)

df['zeta'] = df['unit_width_cm'] * df['facings_per_display']

# producing the final output for product-related parameter csv file:
output_cols = ['Product_Name', 'Supplier_Name', 'Category', 'rho', 'delta', 'iota', 'zeta', 'mu', 'min_l', 'max_v']

N = 5 
for i in range(1, N+1):
    output_cols.extend([f'omega_level_{i}', f'omega_prime_level_{i}'])

final_data = df[output_cols]
final_data.to_csv('product_parameter.csv', index=False)

print(final_data.head()) #just to see preview in terminal 