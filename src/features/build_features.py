import os
import pandas as pd
import openai
import time
from dotenv import load_dotenv
from tenacity import retry, stop_after_attempt, wait_exponential, wait_random

# Load environment variables from .env file
load_dotenv()

# Set OpenAI API key
api_key = os.getenv('OPENAI_API_KEY')
if api_key is None:
    raise ValueError("API key not found. Please set the OPENAI_API_KEY environment variable.")

client = openai.OpenAI(api_key=api_key)

DATA_DIR = '../../data/processed'
OUTPUT_FILE = '../../data/interim/tasks_layman_descriptions.csv'
MODEL = 'gpt-3.5-turbo'


# Function to read tasks from CSV
def read_tasks(file_path):
    tasks_df = pd.read_csv(file_path)
    return tasks_df


# Retry logic with exponential backoff
@retry(stop=stop_after_attempt(5), wait=wait_exponential() + wait_random(min=1, max=60))
def generate_layman_description(task, description, area):
    prompt = f"""
    Task Name: {task}
    Area: {area}
    Description: {description}

    Write a layman's summary of the above task, focusing on potential applications and explaining it in simple terms. 
    The summary should be 1-2 small paragraphs. It should be written so that it's in layman terms, ie. so the general 
    public or journalists can understand it and would be interested in learning more about it.
    It should focus heavily on mentioning potential real-life applications of this task, 
    but these applications don't need to be generic or broad; they can be quite specific if possible! 
    For example, it might read like something you might read in a general audience newsletter about AI 
    (but it should not be super cheesy or gimmicky - it should still be professional-sounding!) 
    """
    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system",
                 "content": "You are an AI assistant that provides clear and concise explanations in layman's terms."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=200
        )
        layman_summary = response.choices[0].message.content.strip()
    except openai.error.RateLimitError as e:
        print(f"Rate limit exceeded for task {task}. Waiting for quota reset...")
        raise e
    except Exception as e:
        print(f"Error generating description for task {task}: {e}")
        layman_summary = "Sorry, there is no description available for this task!"

    return layman_summary


# Generate descriptions for tasks
def generate_descriptions_for_tasks(tasks_df, existing_tasks_set):
    descriptions = []

    for index, row in tasks_df.iterrows():
        task = row['id']
        description = row['description']
        area = row['area']

        if task in existing_tasks_set:
            continue

        print(f"Generating description for task: {task}")
        try:
            layman_description = generate_layman_description(task, description, area)
        except openai.error.RateLimitError:
            # Save progress and wait for the quota to reset
            save_descriptions(descriptions, OUTPUT_FILE)
            print(f"Quota exceeded. Progress saved. Resuming after waiting for quota reset...")
            time.sleep(60 * 60)  # Wait for an hour before retrying
            layman_description = generate_layman_description(task, description, area)

        descriptions.append({'task': task, 'layman': layman_description})

        # Save progress incrementally
        save_descriptions(descriptions, OUTPUT_FILE)

        # Add a delay to avoid hitting API rate limits
        time.sleep(1)

    return descriptions


# Save descriptions to CSV
def save_descriptions(descriptions, output_file):
    if os.path.exists(output_file):
        try:
            existing_df = pd.read_csv(output_file)
            new_df = pd.DataFrame(descriptions)
            combined_df = pd.concat([existing_df, new_df]).drop_duplicates(subset='task').reset_index(drop=True)
            combined_df.to_csv(output_file, index=False)
        except pd.errors.EmptyDataError:
            new_df = pd.DataFrame(descriptions)
            new_df.to_csv(output_file, index=False)
    else:
        descriptions_df = pd.DataFrame(descriptions)
        descriptions_df.to_csv(output_file, index=False)


# Main function
def main():
    tasks_file_path = os.path.join(DATA_DIR, 'tasks_by_area.csv')
    tasks_df = read_tasks(tasks_file_path)

    # Check if the output file already exists and determine the starting index
    if os.path.exists(OUTPUT_FILE):
        try:
            existing_df = pd.read_csv(OUTPUT_FILE)
            existing_tasks_set = set(existing_df['task'].tolist())
        except pd.errors.EmptyDataError:
            existing_tasks_set = set()
    else:
        existing_tasks_set = set()

    # Generate descriptions starting from the last processed index
    descriptions = generate_descriptions_for_tasks(tasks_df, existing_tasks_set)

    save_descriptions(descriptions, OUTPUT_FILE)
    print(f"Descriptions saved to {OUTPUT_FILE}")


if __name__ == '__main__':
    main()
