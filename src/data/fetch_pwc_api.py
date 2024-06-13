import os
import json
import logging
import time
from paperswithcode import PapersWithCodeClient
from tea_client.errors import HttpClientError

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Constants
# Note: These constants can be modified as needed
DATA_DIR = '../../data/raw'
RETRY_LIMIT = 5
RETRY_DELAY = 5  # seconds

# Initialize the PapersWithCode client
client = PapersWithCodeClient()

# Save data to a JSON file
def save_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)
    logging.info(f"Saved data to {filename}")

# Ensure the data/raw directory exists
os.makedirs(DATA_DIR, exist_ok=True)

# Fetch areas
def fetch_areas():
    logging.info("Fetching areas...")
    try:
        areas = client.area_list()
        if areas:
            save_json([area_to_dict(area) for area in areas.results], os.path.join(DATA_DIR, 'areas.json'))
        return areas
    except Exception as e:
        logging.error(f"Error fetching areas: {e}")
        return None

# Convert area to dictionary
def area_to_dict(area):
    return {
        'id': area.id,
        'name': area.name,
    }

# Fetch tasks for an area
def fetch_tasks(area_id):
    logging.info(f"Fetching tasks for area {area_id}...")
    tasks = []
    page = 1
    while True:
        try:
            area_tasks = client.area_task_list(area_id=area_id, page=page)
            if not area_tasks:
                break
            tasks.extend(area_tasks.results)
            if len(area_tasks.results) < 50:  # Assuming 50 is the default page size
                break
            page += 1
        except HttpClientError as e:
            logging.error(f"HTTP error fetching tasks for area {area_id} on page {page}: {e}")
            break
        except Exception as e:
            logging.error(f"Error fetching tasks for area {area_id} on page {page}: {e}")
            break
    save_json([task_to_dict(task) for task in tasks], os.path.join(DATA_DIR, f'tasks_{area_id}.json'))
    return tasks

# Convert task to dictionary
def task_to_dict(task):
    return {
        'id': task.id,
        'name': task.name,
        'description': task.description,
    }

# Fetch details for a task
def fetch_task_details(task_id):
    logging.info(f"Fetching details for task {task_id}...")
    try:
        task_details = client.task_get(task_id)
        if task_details:
            save_json(task_to_dict(task_details), os.path.join(DATA_DIR, f'task_{task_id}.json'))
        return task_details
    except HttpClientError as e:
        logging.error(f"HTTP error fetching details for task {task_id}: {e}")
        return None
    except Exception as e:
        logging.error(f"Error fetching details for task {task_id}: {e}")
        return None

# Fetch evaluations for a task
def fetch_evaluations(task_id):
    logging.info(f"Fetching evaluations for task {task_id}...")
    evaluations = []
    page = 1
    while True:
        try:
            task_evaluations = client.task_evaluation_list(task_id=task_id, page=page)
            if not task_evaluations:
                break
            evaluations.extend(task_evaluations.results)
            if len(task_evaluations.results) < 50:  # Assuming 50 is the default page size
                break
            page += 1
        except HttpClientError as e:
            logging.error(f"HTTP error fetching evaluations for task {task_id} on page {page}: {e}")
            break
        except Exception as e:
            logging.error(f"Error fetching evaluations for task {task_id} on page {page}: {e}")
            break
    save_json([evaluation_to_dict(evaluation) for evaluation in evaluations], os.path.join(DATA_DIR, f'task_{task_id}_evaluations.json'))
    return evaluations

# Convert evaluation to dictionary
def evaluation_to_dict(evaluation):
    return {
        'id': evaluation.id,
        'task': evaluation.task,
        'dataset': evaluation.dataset,
        'description': evaluation.description,
    }

# Fetch evaluation results
def fetch_evaluation_results(evaluation_id):
    logging.info(f"Fetching results for evaluation {evaluation_id}...")
    results = []
    page = 1
    while True:
        try:
            evaluation_results = client.evaluation_result_list(evaluation_id=evaluation_id, page=page)
            if not evaluation_results:
                break
            results.extend(evaluation_results.results)
            if len(evaluation_results.results) < 50:  # Assuming 50 is the default page size
                break
            page += 1
        except HttpClientError as e:
            logging.error(f"HTTP error fetching results for evaluation {evaluation_id} on page {page}: {e}")
            break
        except Exception as e:
            logging.error(f"Error fetching results for evaluation {evaluation_id} on page {page}: {e}")
            break
    save_json([result_to_dict(result) for result in results], os.path.join(DATA_DIR, f'evaluation_{evaluation_id}_results.json'))
    return results

# Convert evaluation result to dictionary
def result_to_dict(result):
    return {
        'id': result.id,
        'metrics': result.metrics,
        'methodology': result.methodology,
        'paper': result.paper,
        'uses_additional_data': result.uses_additional_data,
        'evaluated_on': result.evaluated_on,
    }

# Fetch parents of a task
def fetch_parents(task_id):
    logging.info(f"Fetching parents for task {task_id}...")
    parents = []
    page = 1
    while True:
        try:
            task_parents = client.task_parent_list(task_id=task_id, page=page)
            if not task_parents:
                break
            parents.extend(task_parents.results)
            if len(task_parents.results) < 50:  # Assuming 50 is the default page size
                break
            page += 1
        except HttpClientError as e:
            logging.error(f"HTTP error fetching parents for task {task_id} on page {page}: {e}")
            break
        except Exception as e:
            logging.error(f"Error fetching parents for task {task_id} on page {page}: {e}")
            break
    save_json([task_to_dict(parent) for parent in parents], os.path.join(DATA_DIR, f'task_{task_id}_parents.json'))
    return parents

# Fetch children of a task
def fetch_children(task_id):
    logging.info(f"Fetching children for task {task_id}...")
    children = []
    page = 1
    while True:
        try:
            task_children = client.task_child_list(task_id=task_id, page=page)
            if not task_children:
                break
            children.extend(task_children.results)
            if len(task_children.results) < 50:  # Assuming 50 is the default page size
                break
            page += 1
        except HttpClientError as e:
            logging.error(f"HTTP error fetching children for task {task_id} on page {page}: {e}")
            break
        except Exception as e:
            logging.error(f"Error fetching children for task {task_id} on page {page}: {e}")
            break
    save_json([task_to_dict(child) for child in children], os.path.join(DATA_DIR, f'task_{task_id}_children.json'))
    return children

# Main function to fetch all relevant data
def main():
    areas = fetch_areas()
    if not areas:
        logging.error("Failed to fetch areas.")
        return

    all_tasks = []
    all_evaluations = []

    for area in areas.results:
        area_tasks = fetch_tasks(area.id)
        if area_tasks:
            all_tasks.extend(area_tasks)

    for task in all_tasks:
        fetch_task_details(task.id)
        fetch_parents(task.id)
        fetch_children(task.id)
        task_evaluations = fetch_evaluations(task.id)
        if task_evaluations:
            all_evaluations.extend(task_evaluations)

    for evaluation in all_evaluations:
        fetch_evaluation_results(evaluation.id)

    logging.info("Relevant data fetched and saved successfully.")


if __name__ == "__main__":
    main()
