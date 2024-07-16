import streamlit as st
import networkx as nx
import dimod
from dwave.system import LeapHybridSampler 
from dwave_networkx.algorithms import traveling_salesperson_qubo

def get_qubo(G, lagrange, n):
    """Returns a dictionary representing a QUBO"""
    Q = traveling_salesperson_qubo(G, lagrange=lagrange, weight=n, missing_edge_weight=None)
    offset = 2 * n * lagrange
    return Q, offset

def get_sampler():
    """Returns a sampler"""
    sampler = LeapHybridSampler()
    return sampler

def solve_tsp(num_cities, edges, lagrange=4000):
    G = nx.Graph()
    G.add_weighted_edges_from(edges)
    Q, offset = get_qubo(G, lagrange, num_cities)
    sampler = get_sampler()
    bqm = dimod.BinaryQuadraticModel.from_qubo(Q, offset=offset)
    response = sampler.sample(bqm, label="Training - TSP")

    sample = response.first.sample
    cost = response.first.energy
    route = [None] * num_cities

    for (city, time), val in sample.items():
        if val:
            route[time] = city

    if None not in route:
        return route, cost
    else:
        return None, None

def main():
    st.title("Traveling Salesperson Problem Solver")

    st.header("Input Parameters")
    num_cities = st.number_input("Number of cities", min_value=3, max_value=20, value=7)
    num_edges = st.number_input("Number of edges", min_value=num_cities, max_value=num_cities*(num_cities-1)//2, value=10)

    st.header("Edges")
    edges = []
    for i in range(num_edges):
        edge = st.text_input(f"Edge {i+1} (format: city1,city2,weight)", value=f"{i%num_cities},{(i+1)%num_cities},{100*(i+1)}")
        city1, city2, weight = map(int, edge.split(','))
        edges.append((city1, city2, weight))

    if st.button("Solve TSP"):
        with st.spinner("Solving..."):
            route, cost = solve_tsp(num_cities, edges)
        if route:
            st.success(f"Optimal route: {route}")
            st.success(f"Cost: {cost}")
        else:
            st.error("Failed to find a valid route.")

if __name__ == "__main__":
    main()
