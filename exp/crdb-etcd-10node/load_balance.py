import os
from datetime import datetime, timedelta
import argparse
import copy

def balance_tasks_single_system_preferred(tasks, nodes):
    # Calculate total time for each task
    for task in tasks:
        tasks[task]['total_time'] = tasks[task]['time'] * tasks[task]['count']
    
    # Sort tasks by their total time in descending order
    sorted_tasks = sorted(tasks.items(), key=lambda x: x[1]['total_time'], reverse=True)
    
    # Initialize nodes
    node_times = [0] * nodes
    init_dict = {}
    for k, v in tasks.items():
        init_dict[k] = 0
    node_assignments = [copy.deepcopy(init_dict) for _ in range(nodes)]
    
    # Assign tasks to nodes
    for task, info in sorted_tasks:
        count_remaining = info['count']
        while count_remaining > 0:
            # Find the node with the minimum total time currently
            min_node = node_times.index(min(node_times))
            # Fill one node with as many of the same task as possible, but not exceeding twice the average
            avg_count = info['count'] // nodes
            # max_count = min(count_remaining, avg_count)
            max_count = min(1, avg_count)
            node_assignments[min_node][task] += max_count
            node_times[min_node] += max_count * info['time']
            count_remaining -= max_count
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
parser.add_argument('--sanity', action='store_true',
                    help='generate job files')
args = parser.parse_args()

tasks = {
    # 'cass': {'time': 7, 'count': 500},
    'crdb': {'time': 3.5, 'count': 2280},
    'etcd': {'time': 3, 'count': 1140},
    # 'hbase': {'time': 4.5, 'count': 500},
    # 'kafka': {'time': 3.3, 'count': 500}
}
num_nodes = 18
# Reassign tasks with a preference for keeping each node's tasks from the same system
balanced_assignments_preferred = balance_tasks_single_system_preferred(tasks, num_nodes)

current_datetime = datetime.now()
assignment_lines = []
for assignment in balanced_assignments_preferred:
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
    for node in balanced_assignments_preferred:
        node_id = node[0]
        create_dir_if_not_exist('./exp')
        new_file_path = f"./exp/node{node_id}.job"
        for sys, count in node[1].items():
            if count == 0:
                continue
            input_file_path = f"./scripts/{sys}.sh"
            process_and_update_file(input_file_path, new_file_path, 5*node[1][sys])
    with open('assignments.txt', 'w') as f:
        f.write(assignment_str)

if args.sanity:
    line_counts = {}
    summ = 0
    for node in balanced_assignments_preferred:
        node_id = node[0]
        new_file_path = f"./exp/node{node_id}.job"
        with open(new_file_path, 'r') as file:
            line_count = sum(1 for line in file)
            line_counts[f'node{node_id}'] = line_count /5
            summ += line_count /5
    line_counts['total'] = summ
    print(line_counts)