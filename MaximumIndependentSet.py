#MaximumIndependetSet
import streamlit as st
import networkx as nx
import dwave_networkx as dnx
import matplotlib.pyplot as plt
from dwave.samplers import SimulatedAnnealingSampler

def set_sampler():
    '''Returns a simulated annealing sampler'''
    sampler = SimulatedAnnealingSampler()
    return sampler

def create_graph(num_nodes, edge_list):
    # Create empty graph
    G = nx.Graph()
    # Add nodes
    G.add_nodes_from(range(1, num_nodes + 1))
    # Add edges
    G.add_edges_from(edge_list)
    return G

def solve_problem(G, sampler):
    '''Returns a solution to the maximum independent set problem on graph G 
    using the simulated annealing sampler.

    Args:
        G(networkx.Graph): a graph representing a problem
        sampler(dimod.Sampler): sampler used to find solutions

    Returns:
        A list of nodes
    '''
    # Find the maximum independent set, S
    S = dnx.maximum_independent_set(G, sampler=sampler, num_reads=10)
    return S

# Streamlit code
st.title("Maximum Independent Set Problem Solver")

# User inputs for graph configuration
num_nodes = st.number_input("Enter the number of nodes:", min_value=1, step=1)
edge_input = st.text_area("Enter the edges as tuples (e.g., (1,2),(3,5),(6,7)):", value="(1,2),(3,5),(6,7)")

# Convert edge_input to a list of tuples
try:
    edges = eval(edge_input)
    if not all(isinstance(edge, tuple) and len(edge) == 2 for edge in edges):
        raise ValueError("Edges must be a list of tuples.")
except Exception as e:
    st.error(f"Invalid input for edges: {e}")
    edges = []

# Create the graph
if st.button("Create Graph"):
    G = create_graph(num_nodes, edges)
    sampler = set_sampler()
    S = solve_problem(G, sampler)

    # Display the solution
    st.write(f'Maximum independent set size found is {len(S)}')
    st.write(f'The maximum independent set is: {S}')

    # Visualize the original graph
    subset_1 = G.subgraph(S)
    notS = list(set(G.nodes()) - set(S))
    subset_0 = G.subgraph(notS)
    pos = nx.spring_layout(G)

    fig, ax = plt.subplots()
    nx.draw_networkx(G, pos=pos, with_labels=True, ax=ax)
    st.write(f'The Original Graph')
    st.pyplot(fig)

    # Visualize the solution
    fig, ax = plt.subplots()
    nx.draw_networkx(subset_1, pos=pos, with_labels=True, node_color='r', font_color='k', ax=ax)
    nx.draw_networkx(subset_0, pos=pos, with_labels=True, node_color='b', font_color='w', ax=ax)
    st.write(f'The Solution Graph')
    st.pyplot(fig)
