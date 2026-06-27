from collections import deque

#detects cycles in a DAG using Kahn's algorithm (topological sort).

def has_cycle(tasks: list[str], edges: list[list[str]]) -> bool:
    
    graph = {}
    for task in tasks:
        graph[task] = []
        
    in_degree = {}
    for task in tasks:
        in_degree[task] = 0

    for u, v in edges:
        if u not in graph or v not in graph:
            raise ValueError(f"Unknown task in edge: {u} -> {v}")
        graph[u].append(v)
        in_degree[v] += 1

    queue = deque([task for task in tasks if in_degree[task] == 0])
    visited_count = 0

    while queue:
        node = queue.popleft()
        visited_count += 1  
        
        for nbr in graph[node]:
            in_degree[nbr] -= 1
            if in_degree[nbr] == 0:
                queue.append(nbr)

    return visited_count != len(tasks)