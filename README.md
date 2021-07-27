# DNA Computing Simulator

This is a simple Python simulator to emulate the logic of Leonard Adleman's 1994 paper that launched the field of DNA Computing. 

### Process

The simulator goes through the five steps he laid out in his experiment to solve a Hamiltonian Path problem:

1) Create DNA strands that encode for the nodes and edges in a graph, and mix them to create all possible paths.
2) Filter for only those strands that run from the beginning node to the ending node.
3) Filter for only those strands that have a length of 10N bases, where N is the number of nodes in the graph.
4) Filter for onlly those strands that touch each node in the graph at least once.
5) For any strands that remain, decode them back to solve the graph problem.

### Resources

**Video Walkthrough**: [Here is a link to a YouTube video I created, walking through the code and explaining the experiment in more detail.](https://youtu.be/YBhWrHeIqDs)

**Original Paper**: [Here is a link to Leonard Adleman's original paper.](https://courses.cs.duke.edu/cps296.4/spring04/papers/Adleman94.pdf)