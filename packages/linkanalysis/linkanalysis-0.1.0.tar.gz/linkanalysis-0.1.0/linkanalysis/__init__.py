def addition(numbers: list) -> float:
    return sum(numbers)
def show_code():
    code = '''
import numpy as np
def pagerank(adj_matrix, damping_factor=0.85, max_iterations=100, epsilon=1.0e-6):
    n = len(adj_matrix)
    teleport_prob = (1 - damping_factor) / n
    scores = np.ones(n) / n
    for _ in range(max_iterations):
        prev_scores = np.copy(scores)
        scores = teleport_prob + damping_factor * np.dot(adj_matrix.T, scores)
        while np.linalg.norm(scores - prev_scores) < epsilon:
            break
    return scores

adj_matrix = np.array([
[0, 1, 1, 0],
[1, 0, 1, 1],
[1, 1, 0, 1],
[0, 1, 1, 0]
])

pagerank_scores = pagerank(adj_matrix)
print("PageRank Scores:", pagerank_scores)

    '''
    print(code)