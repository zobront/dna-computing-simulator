import random

# STEP 0: PREP
# - The experimenters want to create DNA strands that encode for the nodes and edges of a graph
# - We will create a graph with 8 vertices (they used 7), and encode the edges between them with a list of tuples
# - We will encode each node with a random string of bases 10 bases long (to ensure randomness and to make molecules stable at room temp)
# - We'll encode edges with the last 5 bases of the vertex at the start of the edge, and the first 5 of the end of the edge
# - Finally, we'll make strands complementary to the vertex strands
# - The result is that edges and complementary strands can connect to form random paths through the graph

vertex_names = ['I', 'L', 'O', 'V', 'E', 'D', 'N', 'A']
V = len(vertex_names)
edges = [(0, 1), (0, 2), (0, 5), (1, 2), (1, 7), (2, 3), (3, 2), (3, 5), (3, 4), (4, 5), (5, 1), (5, 6), (6, 7)]

pairings = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'}
K = 10

vertex_strands = [ ''.join([ random.choice(list(pairings.keys())) for _ in range(K) ]) for _ in range(V) ]
print(f"Vertex Strands Generated: {vertex_strands}")

def find_edge_strands(vertices, edges):
    edge_strands = [ vertices[v1][(K//2):] + vertices[v2][:(K//2)] for (v1, v2) in edges ]
    return [ strand.replace(vertices[0][-(K//2):], vertices[0]).replace(vertices[-1][:(K//2)], vertices[-1]) for strand in edge_strands]

edge_strands = find_edge_strands(vertex_strands, edges)
print(f"\nEdge Strands Created: {edge_strands}")

def find_complement(strand):
    output = ""
    for nuc in strand: output += pairings[nuc]
    return output

complements = [ find_complement(v) for v in vertex_strands ]
print(f"\nComplements Created: {complements}")


###

# STEP 1: CREATE RANDOM PATHS
# - With all the DNA prep work done, the experimenters simply had to mix the DNA together to form random paths
# - In our case, we will multiply the list of edges by 10k and then allow them to grow when a complement exists to bridge them

all_edges = edge_strands * 10000
random.shuffle(all_edges)

path_strands = []
growing_strand = ""

for idx, s in enumerate(all_edges):
    if len(growing_strand) == 0:
        growing_strand += s
    else:
        target_comp = find_complement(growing_strand[-(K//2):]) + find_complement(s[:(K//2)])
        if target_comp in complements:
            growing_strand += s

    if growing_strand[-K:] == vertex_strands[-1]:
        path_strands.append(growing_strand)
        growing_strand = ""

print(f"\nStrands Created: {len(path_strands)} ")

###

# STEP 2: REMOVE PATHS WITHOUT CORRECT START & END
# - When dna is replicated using PCR, you need a primer to allow it to start
# - Rather than filtering the bad paths, they replicated it using the correct ends as primers, drowning out the rest

in_and_out_strands = [ path for path in path_strands if path[:K] == vertex_strands[0] and path[-K:] == vertex_strands[-1] ]
print(f"\nStrands Starting at {vertex_names[0]} and Ending at {vertex_names[V-1]}: {len(in_and_out_strands)}")

###

# STEP 3: KEEP ONLY PATHS WITH N VERTICES
# - Gel Electrophoresis is a process that lets us filter DNA by length
# - We know that for a path to have touched every vertex once, it should have 8 steps, and therefore 10 * 8 nucleotides

n_step_paths = [ path for path in in_and_out_strands if len(path) == V * 10 ]
print(f"\nStrands with {V} Steps: {len(n_step_paths)}")

###

# STEP 4: KEEP ONLY PATHS WITH THAT TOUCH EACH VERTEX AT LEAST ONCE
# - How can we check for specific vertices without individually sequencing each of the strands?
# - We can "fish them out" with the inverse.
# - We split the double stranded DNA into single stranded DNA.
# - We cover a magnetic bead with the complementary strand to the first vertex we want to check.
# - Then we pour the DNA over the bead, and only the strands with that vertex will stick to the complement.
# - We take those that stuck, and then repeat the process for the next vertex, until we've done them all.

included = n_step_paths
for i in range(len(vertex_strands)):
    included = [ path for path in included if vertex_strands[i] in path ]
    if i == 0 or i == len(vertex_strands) - 1:
        print(f"- Already Checked for {vertex_names[i]}")
    else:
        print(f"- Eliminating Paths Not Including {vertex_names[i]}: {len(included)} Remaining")
print(f"Strands Including All Vertices >= Once: {len(included)}")

# STEP 5: EXTRACT ANY PATHS THAT REMAIN
# - Amplify the remaining DNA with PCR to ensure you have lots of it.
# - Decode the sequence of any remaining strand and you will find a path through the graph.

solution = included[0]

def decode_solution(strand):
	path = []
	for i in range(0, len(strand), 10):
		vertex_strand = strand[i:i+10]
		vertex_num = vertex_strands.index(vertex_strand)
		decoded_letters = vertex_names[vertex_num]
		path.append(decoded_letters)
	return path

path = decode_solution(solution)
print(f"Solution: {str(path)}")