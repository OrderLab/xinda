num_nodes = 18
script = './scripts/finetune.sh'

# Read the script file
with open(script, 'r') as file:
    lines = file.readlines()

# Check if the number of lines matches num_nodes
if len(lines) != num_nodes:
    raise ValueError(f"The script should have exactly {num_nodes} lines, but it has {len(lines)} lines.")

# Iterate through the lines and write each to a corresponding job file
for i in range(1, num_nodes + 1):
    node_file = f'exp/node{i}.job'
    with open(node_file, 'w') as file:
        file.write(lines[i - 1])