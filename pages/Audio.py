import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import timedelta

# Load the tasks.csv file
tasks_file = 'app_data/tasks.csv'
tasks_df = pd.read_csv(tasks_file)

# Load the evals.csv file
evals_file = 'app_data/evals.csv'
evals_df = pd.read_csv(evals_file)
evals_df['Value'] = pd.to_numeric(evals_df['Value'], errors='coerce')  # Ensure numeric values
evals_df['Date'] = pd.to_datetime(evals_df['Date'])  # Convert Date to datetime format

# Filter tasks that have associated evaluations
tasks_with_evals = evals_df['Task'].unique()
tasks_df = tasks_df[tasks_df['task'].isin(tasks_with_evals)]

def display_task_info(task_id, depth=0, col1=None, col2=None):
    task = tasks_df[tasks_df['task'] == task_id].iloc[0]
    children = tasks_df[(tasks_df['parents'].apply(lambda x: task_id in str(x).split(','))) & (tasks_df['task'] != task_id) & (tasks_df['task'].isin(tasks_with_evals))]
    if not children.empty:
        child_task_id = col1.selectbox('Select a child task:', [''] + sorted(children['name'].to_list()), key=f"child_{depth}")
        if child_task_id:
            child_task_id = tasks_df[tasks_df['name'] == child_task_id].iloc[0]['task']
            display_task_info(child_task_id, depth + 1, col1, col2)
        else:
            display_task_details(task, col1, col2)
    else:
        display_task_details(task, col1, col2)

def display_task_details(task, col1, col2):
    col1.subheader(f"Task: {task['name']}")
    col1.write(f"**Layman's Description:** {task['layman']}")
    col1.write(f"**Number of Evaluations:** {task['num_evals']}")
    display_benchmark_data(task['task'], col1, col2)

def display_benchmark_data(task_name, col1, col2):
    relevant_evals = evals_df[evals_df['Task'].str.lower() == task_name.lower()]
    benchmarks = sorted(relevant_evals['Dataset'].unique())
    selected_benchmark = col1.selectbox("Please choose a benchmark:", [''] + benchmarks)
    if selected_benchmark:
        benchmark_data = relevant_evals[relevant_evals['Dataset'] == selected_benchmark]
        if not benchmark_data.empty:
            fig, best_performances = plot_performance_graph(benchmark_data, task_name, selected_benchmark)
            col2.plotly_chart(fig, use_container_width=True)
            for metric, details in best_performances.items():
                col2.write(f"The benchmark **{selected_benchmark}** uses the metric, **{metric}** for evaluating model performance. Here, you can see that the model **{details['model']}** achieved the best performance, and achieved this on **{details['date']}**.")

def plot_performance_graph(data, task_name, dataset_name):
    data = data.sort_values('Date')
    fig = go.Figure()
    best_performances = {}

    for metric, group in data.groupby('Metric'):
        best_value = group.loc[group['Value'].idxmin() if metric.lower() in ['mr', 'minade', 'minfde', 'brier-minfde'] else group['Value'].idxmax()]
        group['Color'] = ['red' if idx == best_value.name else 'blue' for idx in group.index]
        fig.add_trace(go.Scatter(
            x=group['Date'],
            y=group['Value'],
            mode='lines+markers',
            name=metric,
            marker=dict(color=group['Color']),
            text=group['Model'],
        ))
        best_performances[metric] = {
            'model': best_value['Model'],
            'date': best_value['Date'].strftime('%Y-%m-%d'),
            'value': best_value['Value']
        }

    start_date = data['Date'].min() - timedelta(days=90)
    end_date = data['Date'].max() + timedelta(days=90)
    y_max = data['Value'].max()
    y_axis_range = [0, 1] if y_max <= 1 else [0, 100]

    fig.update_layout(
        title=f'Performance of ML Models for {task_name} on the {dataset_name} Benchmark over Time',
        xaxis=dict(title='Date', range=[start_date, end_date]),
        yaxis=dict(title='Metric Score', range=y_axis_range),
        legend_title='Metric',
        hovermode='x unified'
    )
    return fig, best_performances

def main(area='audio'):
    st.title('Audio')
    st.write('This page contains information about Audio-related ML tasks.')
    col1, col2 = st.columns([2, 3])  # Create two columns for different content
    area_tasks = tasks_df[tasks_df['area'].str.lower() == area.lower()]
    initial_tasks = area_tasks[area_tasks['parents'] == area_tasks['task']]
    selected_task = col1.selectbox('Select a task:', [''] + sorted(initial_tasks['name'].to_list()))
    if selected_task:
        selected_task_id = area_tasks[area_tasks['name'] == selected_task]['task'].iloc[0]
        display_task_info(selected_task_id, col1=col1, col2=col2)

if __name__ == "__main__":
    main()
