import sys
from pathlib import Path

file = Path(__file__).resolve()
parent, root = file.parent, file.parents[1]
sys.path.append(str(root))

import pandas as pd
from sklearn.model_selection import train_test_split

from housing_prediction.config.core import config
from housing_prediction.pipeline import housing_prediction_pipe
from housing_prediction.processing.data_manager import load_dataset, save_pipeline
from sklearn.metrics import mean_squared_error, r2_score

def run_training() -> None:
    
    """
    Train the model.
    """

    # read training data
    data = load_dataset(file_name=config.app_config_.training_data_file)

    # divide train and test
    X_train, X_test, y_train, y_test = train_test_split(
        data[config.model_config_.features],
        data[config.model_config_.target],
        test_size=config.model_config_.test_size,
        random_state=config.model_config_.random_state,
    )

    # Pipeline fitting
    housing_prediction_pipe.fit(X_train,y_train)
    y_pred = housing_prediction_pipe.predict(X_test)

    # persist trained model
    save_pipeline(pipeline_to_persist= housing_prediction_pipe)

    # printing the score
    print("R2 Score (in %):", r2_score(y_test, y_pred)*100)

    with open("metrics.txt", "w") as f:
      f.write(f"### 📈 Model Performance Metrics\n")
      f.write(f"- R² Score: {r2_score(y_test, y_pred)*100:.4f}\n")
      f.write(f"- Sample Predictions: {y_pred[:5]}\n")
    
if __name__ == "__main__":
    print("Running")
    run_training()
