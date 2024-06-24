import pandas as pd
import re

# Load your DataFrame
tasks_df = pd.read_csv('../../app_data/tasks_copy.csv')

def trim_incomplete_sentences(layman_text):
    # Check if the last character is a punctuation mark
    if not re.match(r'.*[.!?]$', layman_text.strip()):
        # If not, find the last occurrence of punctuation and trim
        trimmed_text = re.sub(r' [^.!?]*$', '', layman_text)
        return trimmed_text
    return layman_text

# Apply the function to the 'layman' column of the entire DataFrame
tasks_df['layman'] = tasks_df['layman'].apply(trim_incomplete_sentences)

# Save the modified DataFrame back to CSV if needed
tasks_df.to_csv('../../app_data/tasks.csv', index=False)
