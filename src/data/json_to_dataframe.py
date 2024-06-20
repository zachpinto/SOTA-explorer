import os
import json
import pandas as pd

DATA_DIR = '../../data/raw'
PROCESSED_DIR = '../../data/processed'


def load_json(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)


def extract_tasks_by_area():
    tasks_data = []

    for file in os.listdir(DATA_DIR):
        if file.startswith('tasks_') and file.endswith('.json'):
            area = file[len('tasks_'):-len('.json')]
            tasks = load_json(os.path.join(DATA_DIR, file))
            for task in tasks:
                tasks_data.append({
                    'area': area,
                    'id': task['id'],
                    'name': task['name'],
                    'description': task['description'],
                    'children': '',
                    'parents': '',
                    'num_evals': 0
                })

    return pd.DataFrame(tasks_data)


def load_children(tasks_df):
    for file in os.listdir(DATA_DIR):
        if file.startswith('task_') and file.endswith('_children.json'):
            task_id = file[len('task_'):-len('_children.json')]
            children = load_json(os.path.join(DATA_DIR, file))
            children_ids = [child['id'] for child in children]
            children_str = ','.join(children_ids)
            tasks_df.loc[tasks_df['id'] == task_id, 'children'] = children_str


def load_parents(tasks_df):
    for file in os.listdir(DATA_DIR):
        if file.startswith('task_') and file.endswith('_parents.json'):
            task_id = file[len('task_'):-len('_parents.json')]
            parents = load_json(os.path.join(DATA_DIR, file))
            parents_ids = [parent['id'] for parent in parents]
            parents_str = ','.join(parents_ids)
            tasks_df.loc[tasks_df['id'] == task_id, 'parents'] = parents_str


def load_evaluations(tasks_df):
    for file in os.listdir(DATA_DIR):
        if file.startswith('task_') and file.endswith('_evaluations.json'):
            task_id = file[len('task_'):-len('_evaluations.json')]
            evaluations = load_json(os.path.join(DATA_DIR, file))
            num_evals = len(evaluations)
            tasks_df.loc[tasks_df['id'] == task_id, 'num_evals'] = num_evals


def save_tasks_by_area(tasks_df):
    os.makedirs(PROCESSED_DIR, exist_ok=True)
    tasks_df.to_csv(os.path.join(PROCESSED_DIR, 'tasks_by_area.csv'), index=False)


def extract_all_dataset_names(tasks_df):
    dataset_names = {}

    for task_id in tasks_df['id']:
        evaluations_file = os.path.join(DATA_DIR, f'task_{task_id}_evaluations.json')
        if os.path.exists(evaluations_file):
            evaluations = load_json(evaluations_file)
            for eval in evaluations:
                eval_id = eval['id']
                dataset_name = eval['dataset']
                dataset_names[eval_id] = dataset_name

    return dataset_names


def find_evaluations(task_id):
    evaluations = []
    eval_prefix = f"evaluation_{task_id}-on"
    eval_suffix = "_results.json"

    for file in os.listdir(DATA_DIR):
        if file.startswith(eval_prefix) and file.endswith(eval_suffix):
            eval_file = os.path.join(DATA_DIR, file)
            evaluations.append(eval_file)

    return evaluations


def extract_evaluation_results(evaluation_file):
    evaluation_results = load_json(evaluation_file)
    results = []

    for eval in evaluation_results:
        metrics = eval['metrics']
        model = eval['methodology']
        paper = eval['paper']
        date = eval['evaluated_on']

        for metric_name, metric_value in metrics.items():
            results.append({
                'metric': metric_name,
                'value': metric_value,
                'model': model,
                'paper': paper,
                'date': date
            })

    return results


def extract_evaluations_by_task(tasks_df, all_dataset_names):
    evaluation_data = []

    for task_id in tasks_df['id']:
        evaluation_files = find_evaluations(task_id)

        for eval_file in evaluation_files:
            eval_id = eval_file[len(DATA_DIR) + 1 + len('evaluation_'):-len('_results.json')]

            dataset_name = all_dataset_names.get(eval_id, 'Unknown')

            evaluation_results = extract_evaluation_results(eval_file)

            for result in evaluation_results:
                evaluation_data.append({
                    'Task': task_id,
                    'Dataset': dataset_name,
                    'Metric': result['metric'],
                    'Value': result['value'],
                    'Model': result['model'],
                    'Paper': result['paper'],
                    'Date': result['date']
                })

    return pd.DataFrame(evaluation_data)


def save_evaluations_by_task(evaluations_df):
    evaluations_df.dropna(subset=['Value'], inplace=True)
    evaluations_df.to_csv(os.path.join(PROCESSED_DIR, 'evaluations_by_task.csv'), index=False)


def main():
    # Dataframe 1: Tasks by Area
    tasks_df = extract_tasks_by_area()
    load_children(tasks_df)
    load_parents(tasks_df)
    load_evaluations(tasks_df)
    save_tasks_by_area(tasks_df)

    # Dataframe 2: Evaluations by Task
    all_dataset_names = extract_all_dataset_names(tasks_df)
    evaluations_df = extract_evaluations_by_task(tasks_df, all_dataset_names)
    save_evaluations_by_task(evaluations_df)


if __name__ == '__main__':
    main()
