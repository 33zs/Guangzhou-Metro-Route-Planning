import pandas as pd
from collections import defaultdict
import heapq
def calculate_path(start_station, end_station):
    # Function to build a graph using distances as weights
    def build_graph_with_distance(data):
        graph = defaultdict(dict)
        for _, row in data.iterrows():
            u, v = row['Chinese Station.1'], row['Chinese Station']
            if pd.notna(u):  # Exclude the first station as it has no previous station
                distance = row['Distance to last (km)']
                graph[u][v] = distance
                graph[v][u] = distance  # Undirected graph, add edges in both directions
        return graph

    # Dijkstra algorithm implementation for shortest distance
    def dijkstra_with_distance(graph, start, end):
        min_heap = [(0, start, [start])]
        visited = set()
        distances = {vertex: float('infinity') for vertex in graph}
        distances[start] = 0

        while min_heap:
            current_distance, current_vertex, path = heapq.heappop(min_heap)
            if current_vertex == end:
                return current_distance, path
            if current_vertex in visited:
                continue

            visited.add(current_vertex)
            for neighbor, weight in graph[current_vertex].items():
                distance = current_distance + weight
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    heapq.heappush(min_heap, (distance, neighbor, path + [neighbor]))

        return float('infinity'), []

    # Function to identify and count transfer stations
    def identify_and_count_transfers_with_chinese_names(path, transfer_data, metro_data):
        transfer_stations = []
        for i in range(1, len(path) - 1):
            station_chinese = metro_data[metro_data['Chinese Station'] == path[i]]['Chinese Station'].values[0]
            prev_station_line = metro_data[metro_data['Chinese Station'] == path[i - 1]]['线路'].values[0]
            next_station_line = metro_data[metro_data['Chinese Station'] == path[i + 1]]['线路'].values[0]
            if prev_station_line != next_station_line and station_chinese in transfer_data['换乘点'].values:
                transfer_stations.append(station_chinese)
        return transfer_stations

    # Load the Guangzhou Metro data
    metro_file_path = 'data/广州地铁1，2，3线路数据.xlsx' # Replace with your file path
    subway_data = pd.read_excel(metro_file_path)

    # Build the graph using distances as weights
    subway_graph_distance = build_graph_with_distance(subway_data)

    # Load the transfer station data
    transfer_file_path = 'data/换乘站数据.xlsx'# Replace with your file path
    transfer_data = pd.read_excel(transfer_file_path)

    # Test case: Shortest distance path from '公园前' to '机场南'
    start_station_test = start_station
    end_station_test = end_station
    shortest_distance_test, path_distance_test = dijkstra_with_distance(subway_graph_distance, start_station_test, end_station_test)
    total_time_distance_test = sum(subway_data.loc[(subway_data['Chinese Station'].isin(path_distance_test)) &
                                                   (subway_data['Chinese Station.1'].isin(path_distance_test)),
                                                   'Travel Time to last (min)'])
    transfer_stations_distance_test = identify_and_count_transfers_with_chinese_names(path_distance_test, transfer_data, subway_data)
    number_of_transfers_distance_test = len(transfer_stations_distance_test)
    #  Finally, return the calculated results
    return {
        "shortest_time": total_time_distance_test,
        "path": path_distance_test,
        "transfer_stations": transfer_stations_distance_test,
        "number_of_transfers": number_of_transfers_distance_test,
        "total_distance": shortest_distance_test
    }
# # Output the results
# print(f"Shortest distance from {start_station_test} to {end_station_test} is: {shortest_distance_test} km")
# print(f"Path: {' -> '.join(path_distance_test)}")
# print(f"Total travel time: {total_time_distance_test} minutes")
# print(f"Transfer stations: {transfer_stations_distance_test}")
# print(f"Number of transfers: {number_of_transfers_distance_test}")