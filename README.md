# SOTA Explorer

## Description
This project creates a streamlit app to allow users to quickly find and view detailed information about ML 
tasks and how various models have performed on popular benchmarks. The app is designed to be user-friendly and easy to navigate. 
One theoretical use case is for journalists to quickly find a layman description of a given ML task and, if necessary,
report on how specific capabilities related to that task (or its subtasks) have improved over time. 

## Features
- Search for SOTA models by task, dataset, or model name in a "nested" directory structure
- View detailed information about a task, including: 
  - A layman's description of the task
  - A list of subtasks (if applicable)
  - A list of datasets used to benchmark the task
  - A chart showing the performance of various models on selected task over time

## Data Sources
- [Papers with Code](https://paperswithcode.com/) for all ML tasks, datasets, and model evaluation metrics

## Installation

Clone the repository and navigate to the project directory:

```bash
git clone https://github.com/zachpinto/SOTA-explorer.git
cd SOTA-Explorer
```

Install the required packages:

```bash
pip install -r requirements.txt
```

## Usage

To run the application, execute the following command:

```bash
streamlit run HOME.py
```

## Contributing

Pull requests are welcome. I am not a professional web developer, so major changes to other front-end technologies are welcome. 


## License
MIT





