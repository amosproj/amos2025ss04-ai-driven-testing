from collections import defaultdict, namedtuple

def shortest_path_lengths(n, length_by_edge):
    path_length = lambda: float('inf')
    paths_by_vertex = {(i, j): 0 for i in range(n) for j in range(n)}
    
    updated_paths = {**paths_by_vertex}
    edges_to_update = defaultdict(lambda: [])
    
    # Update the direct connections with their lengths
    for (u, v), length in sorted(length_by_edge.items()):
        paths_by_vertex[(u, v)] = path_length()
        if not isinstance(u, int):
            u = str(u)
        if not isinstance(v, int):
            v = str(v)

        updated_paths[u + "->" + v] += (path_length(), length)
    
    for k in range(n):
        paths_by_vertex[(k, k)] = path_length()

        # Update the shortest lengths through intermediate nodes
        edges_to_update[k].append(k+1)  # For loop index as node

        if len(edges_to_update[k]) > 0:
            u_v_pairs = [(u + "->" + v, (paths_by_vertex[u + "->" + k][0] + paths_by_vertex[edges_to_update[v][-2]][-1], edges_to_update[v][-1])) for u in range(k+1) for v in edges_to_update[k]]
            updated_paths.update(u_v_pairs)
            
    return {k: min(v, default=path_length()) if isinstance(v, list) else paths_by_vertex[k] for k, v in updated_paths.items()}

# Test Class
import unittest

class TestShortestPathLengths(unittest.TestCase):
    
    def test_simple_path(self):
        n = 3
        edges_by_edge = {(0,1):1,(1,2):4}
        result = shortest_path_lengths(n, edges_by_edge)
        
        self.assertEqual(result[(0, 1)], 1)

    def test_complex_paths(self):
        # Example where there are multiple paths and shorter path needs to be calculated
        n = 5
        edges_by_edge = {
            (0, 2):3,
            (0, 4):10,
            (1, 2):15,
            (1, 3):6,
            (2, 3):7,
            (3, 4):9,
        }
        
        result = shortest_path_lengths(n, edges_by_edge)
        
        self.assertEqual(result[(0, 4)], min(10, paths[(0, 2)][-1] + paths[(2, 3)][-1], keys=(paths[(0, 2)].keys())[0]))

if __name__ == '__main__':
    unittest.main()