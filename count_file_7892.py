# This Python program implements the following use case:
# Write code to count the number of files in current directory and all its nested sub_directories and print the total count

import os

def count_files(directory):
    try:
        return sum(len(os.listdir(path)) for path in os.walk(directory))
    except FileNotFoundError:
        print(f"Directory '{directory}' not found.")
        return None

def main():
    current_dir = os.getcwd()
    file_count = count_files(current_dir)
    if file_count is not None:
        print(f"Total files in '{current_dir}': {file_count}")

if __name__ == "__main__":
    main()