import pandas as pd
import matplotlib.pyplot as plt
import io
import matplotlib.patches as patches

data_string = """Shelf_ID,Type,X,Y,Width_W,Levels_N,DIST_b,is_high_demand
1,S,25,10,400,5,26.93,1
2,S,28,10,400,5,29.73,1
3,S,25,20,400,5,32.02,0
4,S,28,20,400,5,34.41,0
5,S,25,30,400,5,39.05,0
6,S,28,30,400,5,41.04,0
7,S,25,40,400,5,47.17,1
8,S,28,40,400,5,48.83,1
9,S,50,10,400,5,50.99,1
10,S,53,10,400,5,53.94,1
11,S,50,20,400,5,53.85,0
12,S,53,20,400,5,56.65,0
13,S,50,30,400,5,58.31,0
14,S,53,30,400,5,60.9,0
15,S,50,40,400,5,64.03,1
16,S,53,40,400,5,66.4,1
17,S,75,10,400,5,75.66,1
18,S,78,10,400,5,78.64,1
19,S,75,20,400,5,77.62,0
20,S,78,20,400,5,80.52,0
21,S,75,30,400,5,80.78,0
22,S,78,30,400,5,83.57,0
23,S,75,40,400,5,85.0,1
24,S,78,40,400,5,87.66,1
25,R,10,60,400,5,60.83,0
26,R,20,60,400,5,63.25,0
27,R,30,60,400,5,67.08,0
28,R,40,60,400,5,72.11,1
29,R,50,60,400,5,78.1,1
30,R,60,60,400,5,84.85,1
31,R,70,60,400,5,92.2,0
32,R,80,60,400,5,100.0,0
33,R,90,60,400,5,108.17,0
34,F,100,10,400,5,100.5,1
35,F,100,20,400,5,101.98,0

"""
df = pd.read_csv(io.StringIO(data_string))

color_map = {'S': 'lightblue', 'R': "#D2A3E2", 'F': 'orange'}
df['Color'] = df['Type'].map(color_map)

# grid setup
plt.figure(figsize=(10, 6)) 
plt.title("Store Shelf Layout", fontsize=14)
plt.xlabel("X Coordinate", fontsize=10)
plt.ylabel("Y Coordinate", fontsize=10)
plt.grid(True, linestyle=':', alpha=0.5)

plt.xlim(-2, 102) 
plt.ylim(-2, 62)  

# plot shelves 
plt.scatter(
    df['X'], 
    df['Y'], 
    c=df['Color'], 
    s=250,  
    marker='s', 
    edgecolors='gray', 
    label=None
)

# high-demand shelves 
high_demand = df[df['is_high_demand'] == 1]
plt.scatter(
    high_demand['X'], 
    high_demand['Y'], 
    s=200,          
    marker='*',      
    color='red',      
    label=None)

# entrance 
plt.scatter(
    0, 
    0, 
    s=700,
    marker='o',
    color="#7CCE6C", # Light Blue
    edgecolors='darkgreen',
    linewidth=0.5,
    label=None 
)

# checkout 
y_min_norm = (0 - (-2)) / (62 - (-2))  # 2/64
y_max_norm = (5 - (-2)) / (62 - (-2))  # 7/64

plt.axvspan(
    xmin=85,
    xmax=95,
    ymin=y_min_norm, 
    ymax=y_max_norm, 
    color='darkgreen', 
    alpha=0.7, 
    label=None 
)

# shelf IDs
for i in range(len(df)):
    plt.text(
        df['X'].iloc[i], 
        df['Y'].iloc[i] - 1.5,  
        str(df['Shelf_ID'].iloc[i]), 
        color='black', 
        ha='center', 
        va='top',           
        fontsize=9,         
        fontweight='bold'
    )

# legend 
plt.plot([], [], 's', color='lightblue', label='Standard (S)')
plt.plot([], [], 's', color="#D2A3E2", label='Refrigerated (R)')
plt.plot([], [], 's', color='orange', label='Freezer (F)')
plt.plot([], [], '*', color='red', markersize=10, 
         label='High Traffic Area')
plt.plot([], [], 'o', color="#7CCE6C", markersize=10, label='Entrance') 
plt.plot([], [], 's', color='darkgreen', markersize=10, label='Checkout') 

plt.legend(
    loc='upper center',         
    bbox_to_anchor=(0.5, -0.15), 
    ncol=3,                     
    fontsize=9
)

plt.tight_layout(rect=[0, 0.1, 1, 1]) 
plt.savefig('store_layout_visual_map.png')