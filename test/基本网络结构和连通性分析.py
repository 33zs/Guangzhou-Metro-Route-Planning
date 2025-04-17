import pandas as pd
import networkx as nx
from collections import defaultdict

# Function to build a graph model
def build_graph(data):
    graph = nx.Graph()
    for _, row in data.iterrows():
        if pd.notna(row['Chinese Station.1']):
            graph.add_edge(row['Chinese Station.1'], row['Chinese Station'],
                           weight=row['Travel Time to last (min)'])
    return graph

# Load data from an Excel file
file_path = '../data/广州地铁1，2，3线路数据.xlsx'
subway_data = pd.read_excel(file_path)

# Build an undirected graph based on the subway data
G_undirected = build_graph(subway_data)

# Basic network analysis
num_nodes = G_undirected.number_of_nodes()
num_edges = G_undirected.number_of_edges()
is_connected = nx.is_connected(G_undirected)

# Print the results
print("基本网络结构：")
print(f"节点数量（地铁站）：{num_nodes}")
print(f"边的数量（直接连接）：{num_edges}")
print(f"整个网络是否连通：{'是' if is_connected else '否'}")
