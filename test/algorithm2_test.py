import pandas as pd
import random
import time
from collections import defaultdict
import heapq
# 加载广州地铁数据

subway_data = pd.read_excel('../data/广州地铁1，2，3线路数据.xlsx')

# 构建图模型，使用距离作为权重
def build_graph_with_distance(data):
    graph = defaultdict(dict)
    for _, row in data.iterrows():
        u, v = row['Chinese Station.1'], row['Chinese Station']
        if pd.notna(u):  # 排除没有前一站的起始站
            distance = row['Distance to last (km)']
            graph[u][v] = distance
            graph[v][u] = distance  # 无向图，双向添加边
    return graph


# Dijkstra算法实现，寻找最短距离
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


# 计算路径
def calculate_path(start_station, end_station):


    # 构建基于距离的图
    subway_graph_distance = build_graph_with_distance(subway_data)

    # 执行 Dijkstra 算法
    shortest_distance, path = dijkstra_with_distance(subway_graph_distance, start_station, end_station)

    # 返回结果
    return {
        "shortest_distance": shortest_distance,
        "path": path
    }


# 性能测试
def performance_test():
    # 选择测试案例
    random.seed(0)  # 确保可重复性
    all_stations = list(set(subway_data['Chinese Station'].dropna().tolist()))
    test_cases = random.sample(all_stations, 10)  # 选择10个站点
    test_cases = [(test_cases[i], test_cases[i + 1]) for i in range(0, len(test_cases), 2)]  # 创建站点对

    # 进行性能测试
    execution_times = []
    for start_station, end_station in test_cases:
        start_time = time.time()
        # 执行路径计算函数
        result = calculate_path(start_station, end_station)
        end_time = time.time()
        execution_time = end_time - start_time
        execution_times.append(execution_time)

        # 改进的打印结果
        print(f"测试案例：从 '{start_station}' 到 '{end_station}'")
        print(f"最短距离：{result['shortest_distance']} 公里")
        print(f"路径：{' -> '.join(result['path'])}")
        print(f"计算用时：{execution_time:.4f} 秒")
    # 计算平均运行时间
    average_time = sum(execution_times) / len(execution_times)
    print(f"平均运行时间：{average_time:.4f} 秒")


# 运行性能测试
performance_test()
