
graph = {}
edge_cost = {}

MAX_STATES = 15


def add_node():
    if len(graph) >= MAX_STATES:
        print("Maximum state space (15) reached!")
        return
    n = int(input("Enter total nodes to add: "))
    for i in range(n):
        node = input("Enter node name: ")
        if node not in graph:
            graph[node] = []
            print("Node added successfully.")
        else:
            print("Node already exists.")

def delete_node():
    node = input("Enter node to delete: ")
    if node in graph:
        del graph[node]
        for n in graph:
            graph[n] = [x for x in graph[n] if x != node]
        print("Node deleted successfully.")
    else:
        print("Node not found.")

def add_edge():
    n = int(input("Enter total edges to add: "))
    for i in range(n):
        print("Edge", i + 1)
        u = input("Enter first node: ")
        v = input("Enter second node: ")
        if u in graph and v in graph:
            graph[u].append(v)
            graph[v].append(u)
            print("Edge added successfully.")
        else:
            print("Add both nodes first.")

def remove_edge():
    u = input("Enter first node: ")
    v = input("Enter second node: ")
    if u in graph and v in graph:
        if v in graph[u]:
            graph[u].remove(v)
            graph[v].remove(u)
            print("Edge removed successfully.")
        else:
            print("Edge does not exist.")
    else:
        print("Node not found.")

def display_graph():
    print("\nAdjacency List:")
    for node in graph:
        print(node, "->", graph[node])


def bfs_search():
    start = input("Enter start node: ")
    goal = input("Enter goal node: ")

    if start not in graph or goal not in graph:
        print("Start or goal node not present.")
        return

    visited = []
    queue = [start]
    parent = {start: None}
    step = 1

    while queue:
        print("\nStep", step)
        print("Queue:", queue)
        print("Visited:", visited)

        node = queue.pop(0)

        if node not in visited:
            visited.append(node)

            if node == goal:
                path = []
                cur = goal
                while cur is not None:
                    path.append(cur)
                    cur = parent[cur]
                path.reverse()

                print("\nFinal Output:")
                print("BFS Traversal Order:")
                print(" -> ".join(visited))
                print("Path:")
                print(" -> ".join(path))
                print("Path Cost:", len(path) - 1)
                return

            for neighbour in graph[node]:
                if neighbour not in visited and neighbour not in queue:
                    queue.append(neighbour)
                    parent[neighbour] = node
        step += 1

    print("No path found.")


def dfs_search():
    start = input("Enter start node: ")
    goal = input("Enter goal node: ")

    if start not in graph or goal not in graph:
        print("Start or goal node not present.")
        return

    visited = []
    stack = [start]
    parent = {start: None}
    step = 1

    while stack:
        print("\nStep", step)
        print("Stack:", stack)
        print("Visited:", visited)

        node = stack.pop()

        if node not in visited:
            visited.append(node)

            if node == goal:
                path = []
                cur = goal
                while cur is not None:
                    path.append(cur)
                    cur = parent[cur]
                path.reverse()

                print("\nFinal Output:")
                print("DFS Traversal Order:")
                print(" -> ".join(visited))
                print("Path:")
                print(" -> ".join(path))
                print("Path Cost:", len(path) - 1)
                return

            for neighbour in reversed(graph[node]):
                if neighbour not in visited:
                    stack.append(neighbour)
                    parent[neighbour] = node
        step += 1

    print("No path found.")


def input_edge_costs():
    edge_cost.clear()
    print("\nEnter edge costs (for UCS):")
    for u in graph:
        for v in graph[u]:
            if (v, u) not in edge_cost:
                w = int(input(f"Cost from {u} to {v}: "))
                edge_cost[(u, v)] = w
                edge_cost[(v, u)] = w

def ucs_search():
    start = input("Enter start node: ")
    goal = input("Enter goal node: ")

    if start not in graph or goal not in graph:
        print("Start or goal node not present.")
        return


    frontier = [(0, start, [start])]
    explored = []
    step = 1

    print("\nStarting UCS Search...")

    while frontier:

        frontier.sort()
        cost, node, path = frontier.pop(0)

        if node in explored:
            continue


        print(f"\nStep {step}: Expanding node '{node}'")
        print(f"  Current Path: {' -> '.join(path)}")
        print(f"  Current Cost: {cost}")

        if node == goal:
            print("\n--- Goal Reached! ---")
            print("Final Path:", " -> ".join(path))
            print("Total Path Cost:", cost)
            return

        explored.append(node)


        print("  Children:")
        has_children = False
        for neighbour in graph[node]:
            if neighbour not in explored:
                has_children = True
                w = edge_cost[(node, neighbour)]
                new_cost = cost + w
                new_path = path + [neighbour]

                print(f"    -> {neighbour} (Total Cost: {new_cost}, Path: {' -> '.join(new_path)})")
                frontier.append((new_cost, neighbour, new_path))

        if not has_children:
            print("    (No unvisited children)")

        step += 1

    print("\nGoal not reachable.")


while True:
    print("\n******* MENU *******")
    print("1. Add Node")
    print("2. Delete Node")
    print("3. Add Edge")
    print("4. Remove Edge")
    print("5. Display Graph")
    print("6. BFS Search")
    print("7. DFS Search")
    print("8. UCS Search")
    print("9. Exit")

    choice = int(input("Enter your choice: "))

    if choice == 1:
        add_node()
    elif choice == 2:
        delete_node()
    elif choice == 3:
        add_edge()
    elif choice == 4:
        remove_edge()
    elif choice == 5:
        display_graph()
    elif choice == 6:
        bfs_search()
    elif choice == 7:
        dfs_search()
    elif choice == 8:
        input_edge_costs()
        ucs_search()
    elif choice == 9:
        print("Exiting program.")
        break
    else:
        print("Invalid choice.")
