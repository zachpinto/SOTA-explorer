import os
import pandas as pd

INPUT_DIR = '../../data/interim'
OUTPUT_DIR = '../../data/processed'

OUTPUT_FILE = os.path.join(OUTPUT_DIR, 'tasks.csv')

# Load the input files
tasks_by_area_file = os.path.join(INPUT_DIR, 'tasks_by_area.csv')
tasks_layman_descriptions_file = os.path.join(INPUT_DIR, 'tasks_layman_descriptions.csv')

tasks_by_area_df = pd.read_csv(tasks_by_area_file)
tasks_layman_descriptions_df = pd.read_csv(tasks_layman_descriptions_file)

# Rename columns in tasks_layman_descriptions_df
tasks_layman_descriptions_df.rename(columns={'Task': 'task', 'Layman': 'layman'}, inplace=True)

# Rename 'id' to 'task' in tasks_by_area_df
tasks_by_area_df.rename(columns={'id': 'task'}, inplace=True)

# Merge the dataframes on 'task' column
merged_df = pd.merge(tasks_by_area_df, tasks_layman_descriptions_df, on='task', how='left')

# Select and reorder the columns
final_df = merged_df[['area', 'task', 'name', 'children', 'parents', 'num_evals', 'layman']]

# Save the output to CSV
final_df.to_csv(OUTPUT_FILE, index=False)

print(f"Tasks saved to {OUTPUT_FILE}")
