import pandas as pd
from collections import defaultdict
import heapq
def calculate_path(start_station, end_station):
    # Function to build a graph using travel time as weights
    def build_graph_with_time(data):
        graph = defaultdict(dict)
        for _, row in data.iterrows():
            u, v = row['Chinese Station.1'], row['Chinese Station']
            if pd.notna(u):  # Exclude the first station as it has no previous station
                time = row['Travel Time to last (min)']
                graph[u][v] = time
                graph[v][u] = time  # Undirected graph, add edges in both directions
        return graph

    # Dijkstra algorithm implementation to calculate the shortest path in terms of time
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

    def calculate_total_distance(path, metro_data):
        total_distance = 0
        for i in range(1, len(path)):
            prev_station = path[i - 1]
            current_station = path[i]

            # Find matching rows in the DataFrame
            matching_rows = metro_data[((metro_data['Chinese Station'] == current_station) &
                                        (metro_data['Chinese Station.1'] == prev_station)) |
                                       ((metro_data['Chinese Station'] == prev_station) &
                                        (metro_data['Chinese Station.1'] == current_station))]

            if not matching_rows.empty:
                # Get the distance from the first matching row
                distance = matching_rows['Distance to last (km)'].values[0]
                total_distance += distance
            else:
                # Handle case where no matching rows are found
                print(f"没有找到匹配的行，站点：{prev_station} -> {current_station}")

        return total_distance

    # Load the Guangzhou Metro data
    metro_file_path = 'data/广州地铁1，2，3线路数据.xlsx' # Replace with the path to your file
    subway_data = pd.read_excel(metro_file_path)

    # Build the graph using Chinese station names and travel times
    subway_graph_time = build_graph_with_time(subway_data)

    # Calculate the shortest travel time and path from one station to another
    start_station_chinese = start_station
    end_station_chinese = end_station
    shortest_time_chinese, path_chinese = dijkstra_with_time(subway_graph_time, start_station_chinese, end_station_chinese)

    # Load the transfer station data
    transfer_file_path = 'data/换乘站数据.xlsx' # Replace with the path to your file
    transfer_data = pd.read_excel(transfer_file_path)

    # Identify and count transfer stations for the calculated path
    transfer_stations = identify_and_count_transfers_with_chinese_names(path_chinese, transfer_data, subway_data)
    number_of_transfers = len(transfer_stations)

    # Calculate the total distance for the path
    total_distance_chinese = calculate_total_distance(path_chinese, subway_data)
    return {
        "shortest_time": shortest_time_chinese,
        "path": path_chinese,
        "transfer_stations": transfer_stations,
        "number_of_transfers": number_of_transfers,
        "total_distance": total_distance_chinese
    }

# Output the results
# print(f"Shortest travel time from {start_station_chinese} to {end_station_chinese} is: {shortest_time_chinese} minutes")
# print(f"Path: {' -> '.join(path_chinese)}")
# print(f"Transfer stations: {transfer_stations}")
# print(f"Number of transfers: {number_of_transfers}")
# print(f"Total distance: {total_distance_chinese} km")
# print(calculate_path('黄沙',"体育西路"))
