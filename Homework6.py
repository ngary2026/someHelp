
# DIJKSTRA (CORRECT)
def dijkstra(matrix, start_node, max_iterations, target_node):
    num_nodes = len(matrix)
    nodes = [chr(ord('a') + i) for i in range(num_nodes)]  # Node IDs (a, b, c, ...)
    start_index = nodes.index(start_node)

    # Initialize data structures
    costs = {node: float('inf') for node in nodes}
    costs[start_node] = 0
    predecessors = {node: "none" for node in nodes}
    predecessors[start_node] = start_node  # Correctly set the starting node's predecessor to itself
    visited = set()

    for _ in range(max_iterations):
        # Find the unvisited node with the smallest cost
        current_node = min(
            (node for node in nodes if node not in visited),
            key=lambda n: costs[n],
            default=None
        )
        if current_node is None:
            break
        visited.add(current_node)

        # Update neighbors
        current_index = nodes.index(current_node)
        for neighbor_index, cost in enumerate(matrix[current_index]):
            if cost != float('inf'):  # Check for a valid connection
                neighbor_node = nodes[neighbor_index]
                if neighbor_node not in visited:
                    new_cost = costs[current_node] + cost
                    if new_cost < costs[neighbor_node]:
                        costs[neighbor_node] = new_cost
                        predecessors[neighbor_node] = current_node

    # Build the least-cost path from start_node to target_node
    path = []
    current_node = target_node
    while current_node != "none" and current_node != start_node:
        path.append(current_node)
        current_node = predecessors[current_node]
    if current_node == start_node:
        path.append(start_node)
    path.reverse()  # Reverse to show the path from start_node to target_node

    # Format output
    output_costs = [
        f"{predecessors[node]},{'inf' if costs[node] == float('inf') else int(costs[node])}"
        for node in nodes
    ]
    formatted_output = ",".join(output_costs)
    formatted_path = ",".join(path)
    return f"{formatted_output};{formatted_path}"

# DISTANCE VECTOR (CORRECT)
def distance_vector(matrix, target_node, max_iterations):
    num_nodes = len(matrix)
    nodes = [chr(ord('a') + i) for i in range(num_nodes)]  # Node IDs (a, b, c, ...)
    target_index = nodes.index(target_node)

    # Initialize distance vectors for each node
    distance_vectors = {node: [float('inf')] * num_nodes for node in nodes}
    for i in range(num_nodes):
        distance_vectors[nodes[i]][i] = 0  # Distance to itself is 0

    # Initialize distances with direct connections
    for i, node in enumerate(nodes):
        for j in range(num_nodes):
            if matrix[i][j] != float('inf'):
                distance_vectors[node][j] = matrix[i][j]

    # Debug: Initial state
    print("Initial Distance Vectors:")
    for node, vector in distance_vectors.items():
        print(f"{node}: {vector}")
    print()

    # Refined iterative updates
    for iteration in range(max_iterations):
        print(f"Iteration {iteration + 1}:")
        updated = False  # Track if any updates occur
        for i, node in enumerate(nodes):  # Process each node sequentially
            for j in range(num_nodes):  # Update distance to each destination
                for k in range(num_nodes):  # Consider neighbors
                    new_distance = distance_vectors[node][k] + distance_vectors[nodes[k]][j]
                    if new_distance < distance_vectors[node][j]:
                        distance_vectors[node][j] = new_distance
                        updated = True
                        # Debug: Log the update
                        print(f"Updated distance from {node} to {nodes[j]} via {nodes[k]}: {new_distance}")

        # Debug: State after iteration
        print("Distance Vectors After Update:")
        for node, vector in distance_vectors.items():
            print(f"{node}: {vector}")
        print()

        # If no updates occurred, break early (stabilized network)
        if not updated:
            print("No updates occurred, network stabilized.")
            break

    # Format the distance vector of the target node
    target_vector = distance_vectors[target_node]
    formatted_vector = ",".join(["inf" if x == float('inf') else str(int(x)) for x in target_vector])
    return formatted_vector


    
question = int(input("Which question?\n 1 = Dijjstra\n 2 = Distance Vector\n"))
if question == 1:
    print("Enter the adjacency matrix row by row.")
    print("Use 'inf' or leave blank for no direct connection. Separate values by commas.")
    print("Example row: 0,13,inf,12,15")
    print()

    num_nodes = int(input("Enter the number of nodes (e.g., 15 for a 15-node network): "))
    matrix = []
    for i in range(num_nodes):
        row = input(f"Enter row {chr(ord('a') + i)}: ").split(',')
        row = [float('inf') if x.strip() == "inf" or x.strip() == "" else int(x.strip()) for x in row]
        matrix.append(row)

    start_node = input("Enter the start node (e.g., 'h'): ").strip().lower()
    max_iterations = int(input("Enter the number of iterations: "))
    target_node = input("Enter the target node to find the shortest path to (e.g., 'j'): ").strip().lower()

    # Run Dijkstra's algorithm
    result = dijkstra(matrix, start_node, max_iterations, target_node)

    # Output the results
    print("\nResults after", max_iterations, "iterations:")
    print(result)

elif question == 2:
    print("Enter the adjacency matrix row by row.")
    print("Use 'inf' or leave blank for no direct connection. Separate values by commas.")
    print("Example row: 0,1,6,inf,inf,3")
    print()

    num_nodes = int(input("Enter the number of nodes (e.g., 12 for a 12-node network): "))
    matrix = []
    for i in range(num_nodes):
        row = input(f"Enter row {chr(ord('a') + i)}: ").split(',')
        row = [float('inf') if x.strip() == "inf" or x.strip() == "" else int(x.strip()) for x in row]
        matrix.append(row)

    target_node = input("Enter the target node to find the distance vector for (e.g., 'i'): ").strip().lower()
    max_iterations = int(input("Enter the number of iterations: "))

    # Run the Distance Vector Algorithm
    result = distance_vector(matrix, target_node, max_iterations)

    # Output the results
    print(f"\nDistance vector of Node [{target_node}] after {max_iterations} iterations:")
    print(result)