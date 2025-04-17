import pandas as pd
import random
import time
from collections import defaultdict
import heapq

# Function to build a graph model from the dataset
def build_graph_with_time(data):
    graph = defaultdict(dict)
    for _, row in data.iterrows():
        u, v = row['Chinese Station.1'], row['Chinese Station']
        if pd.notna(u):  # Exclude the first station as it has no previous station
            # Add edges with travel time as weight
            graph[u][v] = row['Travel Time to last (min)']
            graph[v][u] = row['Travel Time to last (min)']  # For an undirected graph
    return graph

# Implementation of Dijkstra's algorithm to find the shortest path
def dijkstra_with_time(graph, start, end):
    min_heap = [(0, start, [start])]
    visited = set()
    times = {vertex: float('infinity') for vertex in graph}
    times[start] = 0

    while min_heap:
        current_time, current_vertex, path = heapq.heappop(min_heap)
        if current_vertex == end:
            return current_time, path
        if current_vertex in visited:
            continue

        visited.add(current_vertex)
        for neighbor, weight in graph[current_vertex].items():
            time = current_time + weight
            if time < times[neighbor]:
                times[neighbor] = time
                heapq.heappush(min_heap, (time, neighbor, path + [neighbor]))

    return float('infinity'), []

# Function to calculate the shortest path using the graph
def calculate_path(graph, start_station, end_station):
    shortest_time, path = dijkstra_with_time(graph, start_station, end_station)
    return shortest_time, path

# Load the Guangzhou Metro data from an Excel file
file_path = '../data/广州地铁1，2，3线路数据.xlsx'  # Replace with your file path
subway_data = pd.read_excel(file_path)

# Build the graph using station names and travel times
subway_graph_time = build_graph_with_time(subway_data)

# Selecting test cases
random.seed(0)  # For reproducible results
all_stations = set(subway_data['Chinese Station'].dropna().tolist())
all_stations_list = list(all_stations)  # Convert set to list
test_cases = random.sample(all_stations_list, 10)  # Select 10 random stations
test_cases = [(test_cases[i], test_cases[i + 1]) for i in range(0, len(test_cases), 2)]  # Pair the stations

# Perform performance testing
execution_times = []

for start_station, end_station in test_cases:
    start_time = time.perf_counter()  # Start timer
    shortest_time, path = calculate_path(subway_graph_time, start_station, end_station)
    end_time = time.perf_counter()  # End timer
    execution_time = end_time - start_time
    execution_times.append(execution_time)

    # Print the results and execution time
    print(f"Shortest time from {start_station} to {end_station}: {shortest_time} minutes, Path: {path}")
    print(f"Execution time: {execution_time} seconds")

# Calculate average execution time
average_time = sum(execution_times) / len(execution_times)
print(f"Average execution time: {average_time} seconds")
