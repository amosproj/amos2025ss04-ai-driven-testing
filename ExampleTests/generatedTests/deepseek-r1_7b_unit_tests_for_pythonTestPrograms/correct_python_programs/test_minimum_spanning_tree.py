def main():
    import sys

    def find(u, parent):
        while parent[u] != u:
            parent[u] = parent[parent[u]]  # Path compression
            u = parent[u]
        return u

    def union(u, v, parent, size):
        root_u = find(u, parent)
        root_v = find(v, parent)

        if root_u == root_v:
            return False
        
        # Union by size
        if size[root_u] < size[root_v]:
            parent[root_u] = root_v
            size[root_v] += size[root_u]
        else:
            parent[root_v] = root_u
            size[root_u] += size[root_v]
        return True

    input = sys.stdin.read().split()
    ptr = 0
    T = int(input[ptr])
    ptr += 1
    
    for _ in range(T):
        N = int(input[ptr])
        ptr +=1
        
        edges = []
        nodes = set()
        
        # Read all edges and collect unique nodes
        while len(edges) < N-1:
            w = int(input[ptr])
            u = int(input[ptr+1])
            v = int(input[ptr+2])
            ptr +=3
            edges.append( (w, u, v) )
            if u not in nodes:
                nodes.add(u)
            if v not in nodes:
                nodes.add(v)
        
        sorted_edges = sorted(edges, key=lambda x: x[0])
        sum_w = 0
        
        parent = {}
        size = {}
        for node in nodes:
            parent[node] = node
            size[node] = 1
        
        count = 0
        for w, u, v in sorted_edges:
            if find(u, parent) != find(v, parent):
                union(u, v, parent, size)
                sum_w += w
                count +=1
                if count == len(nodes)-1:
                    break
        
        print(sum_w)

if __name__ == '__main__':
    main()