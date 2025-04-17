# 🚇 Guangzhou Metro Route Planning System

A route planning system for **Guangzhou Metro Lines 1, 2, and 3**, designed to compute the **shortest route**, **minimum travel time**, and **least number of transfers** between stations. It features a user-friendly web interface and map visualization, powered by Flask, Pandas, Plotly, and classic graph algorithms.

## 🛠 Features

- 🔍 Query routes between any two stations on Lines 1–3.
- 🕒 Find shortest time paths (Dijkstra's algorithm based on travel time).
- 📏 Find shortest distance paths (Dijkstra's algorithm based on physical distance).
- 🔁 Find routes with the **fewest transfers**.
- 🌐 Interactive **HTML map visualization** with Plotly.
- 🖥️ Web interface built using Flask and HTML/CSS.

## 📂 Project Structure

```
.
├── algorithm1.py       # Shortest time path
├── algorithm2.py       # Shortest distance path
├── algorithm3.py       # Least transfer path
├── runWebsite.py       # Main Flask server
├── initial_map.py      # Initialize geographic data
├── regenerate_map.py   # Visualize map using Plotly
├── index.html          # Frontend interface
└── /data               # Raw station & route data (CSV/Excel)
```

## 🚀 Getting Started

1. **Install dependencies**:
   ```bash
   pip install pandas flask plotly numpy
   ```

2. **Run the server**:
   ```bash
   python runWebsite.py
   ```

3. **Access the app**:  
   Open [http://localhost:5000](http://localhost:5000) in your browser.

## 🧪 Algorithms Used

- **Dijkstra's Algorithm** for shortest path calculation.
- **Min-heap (priority queue)** optimization using `heapq`.
- **Graph representation** via adjacency list (`defaultdict(dict)`).
- **Pandas DataFrame** for station data parsing and manipulation.



## 📊 Example Query

**Input**:  
Start: `Nongjiangsuo`  
End: `Baiyun Dadao Bei`  
Algorithm: `Shortest Time`

**Output**:  
Route with total time = 42 mins, 1 transfer at `Jichang Nan`.
