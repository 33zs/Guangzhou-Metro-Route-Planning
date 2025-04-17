import pandas as pd
from collections import defaultdict
import heapq
def calculate_path(start_station, end_station):
    # Function to build a graph where edges represent transfer requirements
    def build_graph_with_transfers(data, transfer_data):
        graph = defaultdict(dict)
        for _, row in data.iterrows():
            u, v = row['Chinese Station.1'], row['Chinese Station']
            if pd.notna(u):
            # Check if the edge is a transfer by looking at the transfer data
                needs_transfer = u in transfer_data['换乘点'].values and v in transfer_data['换乘点'].values
                graph[u][v] = 1 if needs_transfer else 0
                graph[v][u] = 1 if needs_transfer else 0
        return graph

    # Dijkstra algorithm implementation for shortest distance
    def dijkstra_with_transfers(graph, start, end):
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

    # Function to calculate the total distance of the path
    def calculate_total_distance(path, metro_data):
        total_distance = 0
        for i in range(1, len(path)):
            prev_station = path[i - 1]
            current_station = path[i]

            # Look for matching rows in the DataFrame
            matching_rows = metro_data[((metro_data['Chinese Station'] == current_station) &
                                        (metro_data['Chinese Station.1'] == prev_station)) |
                                       ((metro_data['Chinese Station'] == prev_station) &
                                        (metro_data['Chinese Station.1'] == current_station))]

            if not matching_rows.empty:
                # Get distance from the first matching row
                distance = matching_rows['Distance to last (km)'].values[0]
                total_distance += distance
            else:
                # Handle case where no matching rows are found
                print(f"No matching row found for stations:{prev_station} -> {current_station}")

        return total_distance


    # Load the Guangzhou Metro data
    subway_data = pd.read_excel('data/广州地铁1，2，3线路数据.xlsx')

    # Build the graph using distances as weights
    # Load the transfer station data
    transfer_data = pd.read_excel('data/换乘站数据.xlsx')
    subway_graph_distance = build_graph_with_transfers(subway_data,transfer_data)

    # Test case: Shortest distance path from '公园前' to '机场南'
    start_station_test = start_station
    end_station_test = end_station
    shortest_transfers_test, path_transfers_test = dijkstra_with_transfers(subway_graph_distance, start_station_test, end_station_test)
    total_time_distance_test = sum(subway_data.loc[(subway_data['Chinese Station'].isin(path_transfers_test)) &
                                                   (subway_data['Chinese Station.1'].isin(path_transfers_test)),
                                                   'Travel Time to last (min)'])
    transfer_stations_distance_test = identify_and_count_transfers_with_chinese_names(path_transfers_test, transfer_data, subway_data)
    number_of_transfers_distance_test = len(transfer_stations_distance_test)

    # Calculate the total distance of the path
    total_distance_chinese = calculate_total_distance(path_transfers_test, subway_data)
    # Return the calculated results
    return {
        "shortest_time": total_time_distance_test,
        "path": path_transfers_test,
        "transfer_stations": transfer_stations_distance_test,
        "number_of_transfers": number_of_transfers_distance_test,
        "total_distance": total_distance_chinese
    }