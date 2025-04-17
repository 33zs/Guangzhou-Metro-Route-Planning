import timeit
import pandas as pd
from collections import defaultdict
import heapq
def calculate_path(start_station, end_station):
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

    def calculate_total_distance(path, metro_data):
        total_distance = 0
        for i in range(1, len(path)):
            prev_station = path[i - 1]
            current_station = path[i]

            # 在 DataFrame 中查找匹配的行
            matching_rows = metro_data[((metro_data['Chinese Station'] == current_station) &
                                        (metro_data['Chinese Station.1'] == prev_station)) |
                                       ((metro_data['Chinese Station'] == prev_station) &
                                        (metro_data['Chinese Station.1'] == current_station))]

            if not matching_rows.empty:
                # 从第一个匹配的行中获取距离
                distance = matching_rows['Distance to last (km)'].values[0]
                total_distance += distance
            else:
                # 处理没有找到匹配行的情况
                print(f"没有找到匹配的行，站点：{prev_station} -> {current_station}")

        return total_distance


    # Load the Guangzhou Metro data
    subway_data = pd.read_excel('../data/广州地铁1，2，3线路数据.xlsx')

    # Build the graph using distances as weights
    # Load the transfer station data
    transfer_data = pd.read_excel('../data/换乘站数据.xlsx')
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


    total_distance_chinese = calculate_total_distance(path_transfers_test, subway_data)

    return {
        "shortest_time": total_time_distance_test,
        "path": path_transfers_test,
        "transfer_stations": transfer_stations_distance_test,
        "number_of_transfers": number_of_transfers_distance_test,
        "total_distance": total_distance_chinese
    }
# 性能测试函数
def performance_test(start_station, end_station, iterations=10):
    # 内部函数执行 calculate_path
    def test_run():
        return calculate_path(start_station, end_station)

    # 使用 timeit 测量执行时间
    execution_time = timeit.timeit(test_run, number=iterations)
    average_time = execution_time / iterations

    # 执行一次函数获取结果
    result = test_run()

    return average_time, result

# 测试用例
test_cases = [
    ("公园前", "机场南"),
    ("东山口", "嘉禾望岗"),
    ("珠江新城", "广州塔")
]

# 对每个测试用例进行性能测试
test_results = {}
for start, end in test_cases:
    test_results[(start, end)] = performance_test(start, end, iterations=5)

# 打印测试结果
for case, result in test_results.items():
    print(f"从 {case[0]} 到 {case[1]} 的平均执行时间: {result[0]:.4f} 秒")
    print(f"路径详情: {result[1]}")
    print("\n")
