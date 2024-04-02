# Define the file path
file_path = 'NBA.json'

# Read the first 2041 lines into memory
with open(file_path, 'r') as file:
    lines = [next(file) for _ in range(2041)]

# Now, reopen the file in write mode and write back those lines
with open(file_path, 'w') as file:
    file.writelines(lines)