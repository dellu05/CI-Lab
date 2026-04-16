
graph = {}
edge_cost = {}
heuristic = {}
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

def input_heuristic():
    heuristic.clear()
    print("\nEnter heuristic values (h(n)):")
    for node in graph:
        h = int(input(f"Heuristic of {node}: "))
        heuristic[node] = h
def input_edge_costs():
    edge_cost.clear()
    print("\nEnter edge costs (for UCS):")
    for u in graph:
        for v in graph[u]:
            if (v, u) not in edge_cost:
                w = int(input(f"Cost from {u} to {v}: "))
                edge_cost[(u, v)] = w
                edge_cost[(v, u)] = w

def astar_search():
    start = input("Enter start node: ")
    goal = input("Enter goal node: ")

    if start not in graph or goal not in graph:
        print("Start or goal node not present.")
        return


    frontier = [(heuristic[start], 0, start, [start])]
    explored = []
    step = 1

    print("\nStarting A* Search...")

    while frontier:
        frontier.sort()
        f, g, node, path = frontier.pop(0)

        if node in explored:
            continue

        print(f"\nStep {step}: Expanding node '{node}'")
        print(f"  Current Path: {' -> '.join(path)}")
        print(f"  g(n) = {g}, h(n) = {heuristic[node]}, f(n) = {f}")

        if node == goal:
            print("\n--- Goal Reached! ---")
            print("Final Path:", " -> ".join(path))
            print("Total Path Cost:", g)
            return

        explored.append(node)

        print("  Children:")
        has_children = False

        for neighbour in graph[node]:
            if neighbour not in explored:
                has_children = True
                cost = edge_cost[(node, neighbour)]
                new_g = g + cost
                new_f = new_g + heuristic[neighbour]
                new_path = path + [neighbour]

                print(
                    f"    -> {neighbour} "
                    f"(g={new_g}, h={heuristic[neighbour]}, f={new_f}) | "
                    f"Path: {' -> '.join(new_path)}"
                )

                frontier.append((new_f, new_g, neighbour, new_path))

        if not has_children:
            print("    (No unvisited children)")

        print("  Frontier now:")
        for item in frontier:
            print(f"    {item[2]} : f={item[0]}, g={item[1]}")

        step += 1

    print("\nGoal not reachable.")


while True:
    print("\n******* MENU *******")
    print("1. Add Node")
    print("2. Delete Node")
    print("3. Add Edge")
    print("4. Remove Edge")
    print("5. Display Graph")
    print("6. A* Search")
    print("7. Exit")

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
        input_edge_costs()
        input_heuristic()
        astar_search()
    elif choice == 7:
        print("Exiting program.")
        break
    else:
        print("Invalid choice.")
