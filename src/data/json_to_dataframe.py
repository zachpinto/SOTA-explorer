import os
import json
import pandas as pd

DATA_DIR = '../../data/raw'

def load_json_files(data_dir, file_prefix):
    data = []
    for file in os.listdir(data_dir):
        if file.startswith(file_prefix) and file.endswith('.json'):
            with open(os.path.join(data_dir, file), 'r') as f:
                data.extend(json.load(f))
    return pd.DataFrame(data)

# Load data into DataFrames
areas_df = load_json_files(DATA_DIR, 'areas')
tasks_df = load_json_files(DATA_DIR, 'task_')
evaluations_df = load_json_files(DATA_DIR, 'task_')
evaluation_results_df = load_json_files(DATA_DIR, 'evaluation_')
parents_df = load_json_files(DATA_DIR, 'task_')
children_df = load_json_files(DATA_DIR, 'task_')

# Display the first few rows of each DataFrame
print("Areas DataFrame:")
print(areas_df.head())

print("\nTasks DataFrame:")
print(tasks_df.head())

print("\nEvaluations DataFrame:")
print(evaluations_df.head())

print("\nEvaluation Results DataFrame:")
print(evaluation_results_df.head())

print("\nParents DataFrame:")
print(parents_df.head())

print("\nChildren DataFrame:")
print(children_df.head())
