# Housing Prediction - ML Project

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![scikit-learn](https://img.shields.io/badge/scikit--learn-0.24%2B-orange)
![License](https://img.shields.io/badge/License-MIT-green)

## 🚴 Overview
This project builds a machine learning model to predict housing prices based on various features. 


## 🛠 Tech Stack
The following libraries and tools are used in this project:
- **requests** - To handle API requests.
- **numpy** - For numerical computations.
- **pandas** - For data manipulation and analysis.
- **seaborn** - For statistical data visualization.
- **matplotlib** - For plotting and data visualization.
- **scikit-learn** - For building machine learning models.
- **joblib** - For model serialization and deserialization.
- **pydantic** - For data validation and settings management.
- **strictyaml** - For YAML-based configuration management.
- **ruamel.yaml** - For YAML parsing and writing.
- **pytest** - For running unit and integration tests.
- **build** - For packaging the project.

## 📂 Project Structure
```bash
├── housing_prediction        # Main package
│   ├── config            # Configuration files
│   │   ├── core.py
│   │   ├── __init__.py
│   ├── datasets          # Dataset storage
│   │   ├── bike-sharing-dataset.csv
│   │   ├── __init__.py
│   ├── processing        # Data processing pipeline
│   │   ├── data_manager.py
│   │   ├── features.py
│   │   ├── validation.py
│   │   ├── __init__.py
│   ├── trained_models    # Stored trained models
│   │   ├── config.yml
│   │   ├── pipeline.py
│   │   ├── predict.py
│   │   ├── train_pipeline.py
│   │   ├── VERSION
│   │   ├── __init__.py
├── tests                  # Unit and integration tests
│   ├── __pycache__/       
│   ├── conftest.py        # Pytest configuration
│   ├── test_features.py   # Tests for feature engineering
│   ├── test_predictions.py # Tests for model predictions
│   ├── __init__.py       
├── requirements           # Dependency management
│   ├── requirements.txt
│   ├── test_requirements.txt  # Dependencies for testing
├── venv                   # Virtual environment
├── .gitignore             # Git ignore file
├── README.md              # Project documentation
├── setup.py               # Packaging setup
├── pyproject.toml         # Project metadata and dependencies
```

## ⚙️ Installation
```sh
git clone <repository_url>
cd housing_prediction
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
pip install -r requirements/requirements.txt
```

## 🛠 Running Tests
Install testing dependencies:

```sh
pip install -r requirements/test_requirements.txt
Run tests using pytest:
```

Run Test Using **pytest**
```sh
pytest tests/
```

## 🔨 How to Build the Package
First, install the build package:

```sh
pip install build
Then, build the package:
```

Then, build the package:
```sh
python -m build
```

This will generate a distributable package inside the dist/ folder.
To install the package locally:
```sh
pip install dist/*.whl
```

## 🚀 Usage
- **Preprocess the data**
  ```sh
  python bikeshare_model/processing/data_manager.py
  ```
- **Train the model**
  ```sh
  python bikeshare_model/trained_models/train_pipeline.py
  ```
- **Make predictions**
  ```sh
  python bikeshare_model/trained_models/predict.py --input sample_input.json
  ```

## ⚙️ Configuration
- Configurations are stored in **`config.yml`**.
- Strict YAML parsing is enforced using **strictyaml** and **ruamel.yaml**.

## 💾 Model Saving & Loading
- The trained model is saved using **joblib** and can be loaded for inference.

## 🤝 Contributions
Contributions are welcome! Feel free to submit pull requests or report issues.

## 📜 License
This project is licensed under the **MIT** License

---
**Author: Kaushik T D Roy**

