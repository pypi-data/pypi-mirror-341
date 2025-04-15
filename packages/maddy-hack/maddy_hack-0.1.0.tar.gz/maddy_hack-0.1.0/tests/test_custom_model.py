# custom_model/__init__.py

from collections import deque

def bfs(edge, source):
    """BFS function to calculate distances from source."""
    n = len(edge)
    dist = [float('inf')] * n
    dist[source] = 0
    q = deque([source])
    while q:
        u = q.popleft()
        if edge[u] != -1:
            v = edge[u]
            if dist[u] + 1 < dist[v]:
                dist[v] = dist[u] + 1
                q.append(v)
    return dist

def nearest_meeting_cell(edge, C1, C2):
    """Find the nearest meeting cell using BFS distances."""
    n = len(edge)
    dist_from_C1 = bfs(edge, C1)
    dist_from_C2 = bfs(edge, C2)
    
    meeting_cell = -1
    min_dist_sum = float('inf')
    for i in range(n):
        if dist_from_C1[i] != float('inf') and dist_from_C2[i] != float('inf'):
            total = dist_from_C1[i] + dist_from_C2[i]
            if total < min_dist_sum:
                min_dist_sum = total
                meeting_cell = i
    return meeting_cell

def largest_sum_cycle(edge):
    """Compute the largest sum of node values in a cycle if present."""
    n = len(edge)
    indegree = [0] * n
    for i in range(n):
        if edge[i] != -1:
            indegree[edge[i]] += 1

    visited = [False] * n
    q = deque()
    for i in range(n):
        if indegree[i] == 0:
            visited[i] = True
            q.append(i)
    while q:
        node = q.popleft()
        if edge[node] == -1:
            continue
        next_node = edge[node]
        indegree[next_node] -= 1
        if indegree[next_node] == 0 and not visited[next_node]:
            visited[next_node] = True
            q.append(next_node)

    ans = -1
    for i in range(n):
        if visited[i]:
            continue
        sum_cycle = 0
        cur = i
        while not visited[cur]:
            visited[cur] = True
            sum_cycle += cur
            cur = edge[cur]
        ans = max(ans, sum_cycle)
    return ans

def max_weight_node(edge):
    """Find the node with the maximum accumulated weight."""
    n = len(edge)
    weight = [0] * n
    for i in range(n):
        if edge[i] != -1:
            weight[edge[i]] += i

    ans = -1
    maxi = float('-inf')
    for i in range(n):
        if weight[i] >= maxi:
            maxi = weight[i]
            ans = i
    return ans

# Optional: Command-line interface entry point for testing
def main():
    import argparse
    parser = argparse.ArgumentParser(
        description="Run methods from the custom_model package."
    )
    parser.add_argument(
        '--method',
        choices=['meeting', 'cycle', 'weight'],
        required=True,
        help="Method to run: 'meeting' for nearest_meeting_cell, 'cycle' for largest_sum_cycle, 'weight' for max_weight_node."
    )
    parser.add_argument('--edge', nargs='+', type=int, required=True,
                        help="List of integers representing the edge array")
    parser.add_argument('--C1', type=int, help="Starting cell for meeting cell (required for 'meeting')")
    parser.add_argument('--C2', type=int, help="Second cell for meeting cell (required for 'meeting')")

    args = parser.parse_args()
    if args.method == 'meeting':
        if args.C1 is None or args.C2 is None:
            parser.error("For the 'meeting' method, you must provide both --C1 and --C2.")
        result = nearest_meeting_cell(args.edge, args.C1, args.C2)
        print("Nearest Meeting Cell:", result)
    elif args.method == 'cycle':
        result = largest_sum_cycle(args.edge)
        print("Largest Sum Cycle:", result)
    elif args.method == 'weight':
        result = max_weight_node(args.edge)
        print("Maximum Weight Node:", result)

if __name__ == "__main__":
    main()
