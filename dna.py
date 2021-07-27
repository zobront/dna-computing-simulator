# HOW CAN DNA DO COMPUTATIONS? DNA COMPUTING 101 - CODE ALONG: CREATE A DNA COMPUTER SIMULATOR

# WHAT IS DNA COMPUTING USEFUL FOR?
# - storage is obvious, but let's talk computation
# - benefits: small, energy efficient, parallel (helps with np complete)
# - it's come a long way since then (playing tic tac toe) but best place to start is original paper
# - https://courses.cs.duke.edu/cps296.4/spring04/papers/Adleman94.pdf
# - what are np complete problems?
# - example of what's a hamiltonian graph?

vertex_names = ['I', 'L', 'O', 'V', 'E', 'D', 'N', 'A']
V = len(vertex_names)
edges = [(0, 1), (0, 2), (0, 5), (1, 2), (1, 7), (2, 3), (3, 2), (3, 5), (3, 4), (4, 5), (5, 1), (5, 6), (6, 7)]

# STEP 0: PREP
# - create DNA kmers representing each edge in the graph
# - if a vertex is 20 digits, the edge is the last 10 of the out and the first 10 of the in 
# (except first and last, in which case it was 10 of the pairing and all 20 of the end
# - quick lesson: how does dna pair?
# - why 20? binding of 10 pairs is stable at room temp, and strands that long are unlikely to
# have issues like subsequences that bind, hairpin loops, etc.
# - they also created pairing kmers, that were complementary to the vertex digits


pairings = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'}
K = 10

import random
vertex_strands = [ ''.join([ random.choice(list(pairings.keys())) for _ in range(K)]) for _ in range(V) ]
print(f"Vertex Strands Generated: {vertex_strands}")

def find_edge_strands(vertices, edges):
	edge_strands_tmp = [ vertices[v1][(K//2):] + vertices[v2][:(K//2)] for (v1, v2) in edges ]
	return [ strand.replace(vertices[0][-(K//2):], vertices[0]).replace(vertices[-1][:(K//2)], vertices[-1]) for strand in edge_strands_tmp ]

edge_strands = find_edge_strands(vertex_strands, edges)
print(f"\nEdge Strands Created: {edge_strands}")

def find_complement(strand):
	# We'd technically want to reverse the strand here for 5' to 3', but for this video we'll keep it left to right
	output = ""
	for nuc in strand: output += pairings[nuc]
	return output

complements = [ find_complement(v) for v in vertex_strands ]
print(f"\nComplements Created: {complements}")

print('\nSTEP 1: CREATE RANDOM PATHS')
# - they mixed the pairing kmers and the edge kmers together
# - the result was a mix of overlapping pieces so that vertices would pair with edges that come off them, which would pair with the next vertex

all_edges = edge_strands * 100000
import random
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

	if growing_strand[-10:] == vertex_strands[-1]:
		path_strands.append(growing_strand)
		growing_strand = ""

print(f"Strands Created: {len(path_strands)}")

print("\nSTEP 2: REMOVE PATHS WITHOUT CORRECT START & END")
# - when dna is replicated using PCR, you need a "primer" to allow it to start
# - they replicated using the ends as primers, drowning out the rest

in_to_out_strands = [ path for path in path_strands if path[:10] == vertex_strands[0] and path[-10:] == vertex_strands[-1] ]
print(f"Strands Starting at {vertex_names[0]} and Ending at {vertex_names[V-1]}: {len(in_to_out_strands)}")

print("\nSTEP 3: KEEP PATHS WITH N VERTICES")
# - run on agarose gel, which allows us to see length
# - only 140bp were extracted, and then amplified again so we have lots of them

six_step_paths = [ path for path in path_strands if len(path) == V * 10 ]
print(f"Strands with {V} Steps: {len(six_step_paths)}")

print("\nSTEP 4: KEEP ONLY PATHS THAT TOUCH EACH VERTEX ONCE")
# - how do we check for specific segments? we can "fish them out" with inverse
# - turn the dsDNA into ssDNA
# - then we take the complementary strand of vertex 1 (attached to magnetic beads) and fish around
# - take the successful ones, and repeat for vertex 2, etc until we confirm all vertices are included

# we get to skip include_zero and include_five because we already checked for start and end
included = six_step_paths
for i in range(len(vertex_strands)):
	included = [ path for path in included if vertex_strands[i] in path ] 
	if i == 0 or i == len(vertex_strands) - 1:
		print(f"- Already Checked for {vertex_names[i]}")
	else:
		print(f"- Eliminating Paths Not Including {vertex_names[i]}: {len(included)} Remaining")
print(f"Strands Including All Vertices >= Once: {len(included)}")

print("\nSTEP 5: EXTRACT ANY PATHS THAT REMAIN")
# - amplify with PCR again, so we have pure, excessive of the "answer"

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


# OPPORTUNITIES
# - work should grow linearly (with this algorithm, at least)
# - number of oligos should grow linearly with number of edges, so it's manageable
# - the problem is that many np complete problems have countless edges, so need to be reformulated as fewer edge problsms
# - this is absurdly energy efficient compared to computers (1J could do 2 x 10^19 operations, even though most aren't used)





