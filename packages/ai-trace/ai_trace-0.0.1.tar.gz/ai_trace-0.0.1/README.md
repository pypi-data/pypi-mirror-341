# AI Trace

AI Trace is a visualization tool for CrewAI workflows. It allows you to visualize your CrewAI agents, tasks, and tools in an interactive diagram.

![AI Trace Visualization](https://github.com/aitrace-dev/ai-trace-cli/blob/main/screenshot.png)
## Installation

```bash
pip install ai-trace
```

## Usage

There are 2 main functions: `view_crew` and `save_view`.

```python
from ai_trace.trace_crewai import view_crew, save_view
...
view_crew(crew)  # Opens the visualization in your default browser

# Or save the visualization to a file
save_view(crew, "my_crew_visualization.html")

```

Full example


```python
from crewai import Crew, Agent, Task
from ai_trace.trace_crewai import view_crew, save_view

# Create your CrewAI agents, tasks, and crew as usual
agent = Agent(
    role="Data Scientist",
    goal="Analyze data and provide insights",
    backstory="You are an experienced data scientist with expertise in data analysis."
)

task = Task(
    description="Analyze the dataset and provide insights",
    expected_output="A detailed analysis report",
    agent=agent
)

crew = Crew(
    agents=[agent],
    tasks=[task]
)

# Visualize your crew
view_crew(crew)  # Opens the visualization in your default browser

# Or save the visualization to a file
save_view(crew, "my_crew_visualization.html")
```

## Features

- Visualize CrewAI agents, tasks, and tools
- Interactive diagram with agent and task details
- Automatic layout of workflow components
- Save visualizations as HTML files for sharing

## License

This project is licensed under a modified Commons Clause License. See the [LICENSE](LICENSE) file for details.
