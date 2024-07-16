import streamlit as st
from dimod import Binary, CQM, quicksum
from dwave.system import LeapHybridCQMSampler

# Function to solve the knapsack problem
def solve_knapsack(values, weights, W):
    n = len(values)

    # Create the binary variables
    x = [Binary(i) for i in range(n)]

    # Construct the CQM
    cqm = CQM()

    # Add the objective
    cqm.set_objective(quicksum(-values[i] * x[i] for i in range(n)))

    # Add the two constraints
    cqm.add_constraint(quicksum(weights[i] * x[i] for i in range(n)) <= W, label='max weight')
    cqm.add_constraint(quicksum(x[i] for i in range(n)) <= 2, label='max items')

    # Submit to the CQH sampler
    sampler = LeapHybridCQMSampler()
    sampleset = sampler.sample_cqm(cqm)

    # Initialize variables to store the best feasible solution
    best_value = float('-inf')
    best_solution = None

    # Iterate over each solution in the sampleset to find the best feasible solution
    for sample, energy in zip(sampleset.samples(), sampleset.data_vectors['energy']):
        total_weight = sum(weights[i] * sample[i] for i in range(n))
        if total_weight <= W:
            total_value = sum(values[i] * sample[i] for i in range(n))
            if total_value > best_value:
                best_value = total_value
                best_solution = sample

    # Identify which items are included in the knapsack
    if best_solution is not None:
        included_items = [i for i in range(n) if best_solution[i] == 1]
        total_value = sum(values[i] for i in included_items)
        total_weight = sum(weights[i] for i in included_items)
        return included_items, total_value, total_weight
    else:
        return [], 0, 0

# Streamlit interface
st.title('Knapsack Problem Solver')

# User input for values
values_input = st.text_input('Enter the values (comma-separated):', '34, 25, 78, 21, 64')
values = [int(x.strip()) for x in values_input.split(',')]

# User input for weights
weights_input = st.text_input('Enter the weights (comma-separated):', '3, 5, 9, 4, 2')
weights = [int(x.strip()) for x in weights_input.split(',')]

# User input for maximum weight
W = st.number_input('Enter the maximum weight the knapsack can hold:', value=10)

# Button to solve the knapsack problem
if st.button('Solve'):
    included_items, total_value, total_weight = solve_knapsack(values, weights, W)

    # Display the results
    st.write('Included items:', included_items)
    st.write('Total value:', total_value)
    st.write('Total weight:', total_weight)
