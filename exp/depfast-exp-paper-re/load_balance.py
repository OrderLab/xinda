import os
from datetime import datetime, timedelta
import argparse
import math

def balance_tasks_simple(tasks, nodes):
    # Calculate total number of tasks and tasks per node using ceiling division
    total_tasks = tasks['depfast']['count']
    tasks_per_node = math.ceil(total_tasks / nodes)
    
    # Initialize nodes
    node_times = [0] * nodes
    node_assignments = [{} for _ in range(nodes)]
    
    # Assign tasks to nodes
    count_remaining = total_tasks
    for i in range(nodes):
        if count_remaining >= tasks_per_node:
            node_assignments[i]['depfast'] = tasks_per_node
        else:
            node_assignments[i]['depfast'] = count_remaining
        node_times[i] = node_assignments[i]['depfast'] * tasks['depfast']['time']
        count_remaining -= node_assignments[i]['depfast']
    
    # Format the assignment for output
    final_assignments = []
    for i, node_assignment in enumerate(node_assignments):
        final_assignments.append((i + 1, node_assignment, round(node_times[i], 2)))
    
    return final_assignments

def create_dir_if_not_exist(path_):
    is_exsit = os.path.exists(path_)
    if not is_exsit:
        os.makedirs(path_)

def process_and_update_file(input_file_path, new_file_path, num_lines):
    # Read the entire content of the input file
    with open(input_file_path, 'r') as file:
        lines = file.readlines()

    # Separate the first 100 lines and the rest
    first_100_lines = lines[:num_lines]
    remaining_lines = lines[num_lines:]

    # Append the first 100 lines to the new file
    with open(new_file_path, 'a') as new_file:
        new_file.writelines(first_100_lines)

    # Overwrite the original file with the remaining lines
    with open(input_file_path, 'w') as file:
        file.writelines(remaining_lines)

parser = argparse.ArgumentParser(description="Load balance tasks for distributed systems.")
parser.add_argument('--generate', action='store_true',
                    help='generate job files')
args = parser.parse_args()

tasks = {
    'depfast': {'time': 3, 'count': 960},
}
num_nodes = 8
# Reassign tasks using the simple division method with ceiling
balanced_assignments_simple = balance_tasks_simple(tasks, num_nodes)

current_datetime = datetime.now()
assignment_lines = []
for assignment in balanced_assignments_simple:
    node_id = assignment[0]
    tasks = assignment[1]
    total_time_minutes = assignment[2]
    total_time_hours = total_time_minutes / 60
    
    # Format start time
    start_time_str = current_datetime.strftime("%m-%d %H:%M")
    
    # Calculate and format finish time
    finish_time = current_datetime + timedelta(minutes=total_time_minutes)
    finish_time_str = finish_time.strftime("%m-%d %H:%M")
    
    # Construct the assignment line
    assignment_line = f"Node {node_id}: {tasks}, Total time: {total_time_minutes}min / {total_time_hours:.2f}hr / {start_time_str} -> {finish_time_str}"
    
    # Add the formatted line to the list
    assignment_lines.append(assignment_line)

# Join all lines into a single string separated by newlines
assignment_str = "\n".join(assignment_lines)
print(assignment_str)

if args.generate:
    # Create directories for each node and generate job files
    for node in balanced_assignments_simple:
        node_id = node[0]
        create_dir_if_not_exist('./exp')
        new_file_path = f"./exp/node{node_id}.job"
        for sys in node[1]:
            input_file_path = f"./scripts/{sys}.sh"
            process_and_update_file(input_file_path, new_file_path, 5*node[1][sys])
