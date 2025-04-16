#initiator

#PAGE RANK-WEBGRAPH-LINK ANALYSIS
def pagerank(graph, damping_factor=0.85, epsilon=1.0e-8, max_iterations=100):
    num_nodes = len(graph)
    pagerank_scores = {node: 1.0 / num_nodes for node in graph}
    nodes = list(graph.keys())

    for _ in range(max_iterations):
        new_scores = {}
        max_change = 0

        for node in nodes:
            rank = (1 - damping_factor) / num_nodes
            for other_node in nodes:
                links = graph[other_node]
                if node in links:
                    if len(links) > 0:
                        rank += damping_factor * (pagerank_scores[other_node] / len(links))
                    else:
                        rank += damping_factor * (pagerank_scores[other_node] / num_nodes)
            new_scores[node] = rank
            max_change = max(max_change, abs(rank - pagerank_scores[node]))

        pagerank_scores = new_scores
        if max_change < epsilon:
            break

    return pagerank_scores

# Define the web graph
web_graph = {
    'A': ['B', 'C', 'D'],
    'B': ['C', 'E'],
    'C': ['A', 'D'],
    'D': [],
    'E': []
}

# Calculate PageRank
scores = pagerank(web_graph)

# Display sorted PageRank scores
print("PageRank Scores:")
for node, score in sorted(scores.items(), key=lambda x: x[1], reverse=True):
    print(f"{node}: {score:.6f}")

