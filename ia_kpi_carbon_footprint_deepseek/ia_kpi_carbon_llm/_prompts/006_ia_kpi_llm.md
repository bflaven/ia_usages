
# 004_ia_kpi_llm.md


## PROMPT_1
As a python expert, write simple scripts that are use cases that leverage Eco2AI. Make several files to illustrate the usage of codecarbon

Please do code with best practices and comment each line. Do use Class, Functions, variables at the top of the script and make conventional description for Class and function.


## PERPLEXITY_1


Certainly! I'll create several Python scripts to illustrate the usage of Eco2AI, focusing on best practices, proper commenting, and conventional descriptions for classes and functions. These scripts will demonstrate various use cases of Eco2AI for tracking CO2 emissions in machine learning projects.

1. Basic Usage Script (basic_usage.py):

```python
import eco2AI
import time

# Constants
PROJECT_NAME = "Basic Eco2AI Demo"
EXPERIMENT_DESCRIPTION = "Demonstrating basic Eco2AI usage"

def simulate_computation():
    """Simulate a computation-intensive task."""
    time.sleep(5)  # Simulate 5 seconds of computation

def main():
    """Main function to demonstrate basic Eco2AI usage."""
    # Initialize the Eco2AI tracker
    tracker = eco2AI.Tracker(
        project_name=PROJECT_NAME,
        experiment_description=EXPERIMENT_DESCRIPTION
    )
    
    # Start tracking
    tracker.start()
    
    # Simulate some computation
    simulate_computation()
    
    # Stop tracking
    tracker.stop()
    
    print("Eco2AI tracking completed. Check the generated CSV file for results.")

if __name__ == "__main__":
    main()
```

2. Decorator Usage Script (decorator_usage.py):

```python
from eco2AI import track
import numpy as np

# Constants
ARRAY_SIZE = 10000
ITERATIONS = 1000

@track
def matrix_multiplication():
    """Perform matrix multiplication to simulate a compute-intensive task."""
    for _ in range(ITERATIONS):
        a = np.random.rand(ARRAY_SIZE, ARRAY_SIZE)
        b = np.random.rand(ARRAY_SIZE, ARRAY_SIZE)
        np.dot(a, b)

def main():
    """Main function to demonstrate Eco2AI decorator usage."""
    print("Starting matrix multiplication with Eco2AI tracking...")
    matrix_multiplication()
    print("Matrix multiplication completed. Check the generated CSV file for results.")

if __name__ == "__main__":
    main()
```

3. Machine Learning Example (ml_example.py):

```python
import eco2AI
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification
import numpy as np

# Constants
PROJECT_NAME = "ML Model Training"
EXPERIMENT_DESCRIPTION = "Training a Random Forest Classifier"
N_SAMPLES = 10000
N_FEATURES = 20
N_CLASSES = 2
TEST_SIZE = 0.2
RANDOM_STATE = 42

class MLExperiment:
    """Class to encapsulate a machine learning experiment with Eco2AI tracking."""

    def __init__(self):
        """Initialize the MLExperiment with Eco2AI tracker."""
        self.tracker = eco2AI.Tracker(
            project_name=PROJECT_NAME,
            experiment_description=EXPERIMENT_DESCRIPTION
        )
        self.X, self.y = None, None
        self.model = None

    def generate_data(self):
        """Generate synthetic data for classification."""
        self.X, self.y = make_classification(
            n_samples=N_SAMPLES,
            n_features=N_FEATURES,
            n_classes=N_CLASSES,
            random_state=RANDOM_STATE
        )

    def train_model(self):
        """Train a Random Forest Classifier."""
        X_train, X_test, y_train, y_test = train_test_split(
            self.X, self.y, test_size=TEST_SIZE, random_state=RANDOM_STATE
        )
        self.model = RandomForestClassifier(random_state=RANDOM_STATE)
        self.model.fit(X_train, y_train)
        score = self.model.score(X_test, y_test)
        print(f"Model accuracy: {score:.4f}")

    def run_experiment(self):
        """Run the full experiment with Eco2AI tracking."""
        self.tracker.start()
        self.generate_data()
        self.train_model()
        self.tracker.stop()
        print("Experiment completed. Check the generated CSV file for Eco2AI results.")

def main():
    """Main function to run the ML experiment with Eco2AI tracking."""
    experiment = MLExperiment()
    experiment.run_experiment()

if __name__ == "__main__":
    main()
```

These scripts demonstrate different ways to use Eco2AI in Python projects:

1. `basic_usage.py` shows the fundamental usage of Eco2AI with a simple simulated computation.
2. `decorator_usage.py` illustrates how to use the Eco2AI decorator for easy tracking of specific functions.
3. `ml_example.py` provides a more complex example, integrating Eco2AI into a machine learning workflow using scikit-learn.

Each script follows Python best practices, including proper commenting, use of constants, function and class definitions with docstrings, and a clear structure. They can be run independently to see how Eco2AI tracks CO2 emissions for different types of computations[1][5].

Citations:
[1] https://www.restack.io/p/educational-resources-for-sustainable-technology-answer-sustainable-ai-libraries-python
[2] https://codecarbon.io
[3] https://github.com/sb-ai-lab/Eco2AI/activity
[4] https://github.com/mlco2/codecarbon/actions
[5] https://github.com/sb-ai-lab/Eco2AI/blob/main/pyproject.toml
[6] https://dataforgood.fr/projects/codecarbon/
[7] https://www.restack.io/p/ai-for-climate-change-answer-python-ai-climate-modeling-cat-ai
[8] https://aclanthology.org/2024.tdle-1.pdf





