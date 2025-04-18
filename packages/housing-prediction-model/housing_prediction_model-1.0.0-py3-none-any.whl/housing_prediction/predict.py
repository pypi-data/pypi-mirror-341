import sys
from pathlib import Path
file = Path(__file__).resolve()
parent, root = file.parent, file.parents[1]
sys.path.append(str(root))

from typing import Union
import pandas as pd
import numpy as np


from housing_prediction import __version__ as _version
from housing_prediction.config.core import config
from housing_prediction.pipeline import housing_prediction_pipe
from housing_prediction.processing.data_manager import load_pipeline
from housing_prediction.processing.data_manager import pre_pipeline_preparation
from housing_prediction.processing.validation import validate_inputs


pipeline_file_name = f"{config.app_config_.pipeline_save_file}{_version}.pkl"
housing_prediction_pipe = load_pipeline(file_name=pipeline_file_name)


def make_prediction(*,input_data:Union[pd.DataFrame, dict]) -> dict:
    """Make a prediction using a saved model """

    validated_data, errors = validate_inputs(input_df=pd.DataFrame(input_data))
    
    validated_data=validated_data.reindex(columns=config.model_config_.features)
    results = {"predictions": None, "version": _version, "errors": errors}
    
    predictions = housing_prediction_pipe.predict(validated_data)

    results = {"predictions": int(predictions[0]),"version": _version, "errors": errors}
    print(results)
    if not errors:

        predictions = housing_prediction_pipe.predict(validated_data)
        results = {"predictions": predictions,"version": _version, "errors": errors}

    return results

if __name__ == "__main__":

    data_in = {
    "Id": [1461],
    "MSSubClass": [60],
    "MSZoning": ["RL"],
    "LotFrontage": [65.0],
    "LotArea": [8450],
    "Street": ["Pave"],
    "Alley": [None],
    "LotShape": ["Reg"],
    "LandContour": ["Lvl"],
    "Utilities": ["AllPub"],
    "LotConfig": ["Inside"],
    "LandSlope": ["Gtl"],
    "Neighborhood": ["CollgCr"],
    "Condition1": ["Norm"],
    "Condition2": ["Norm"],
    "BldgType": ["1Fam"],
    "HouseStyle": ["2Story"],
    "OverallQual": [7],
    "OverallCond": [5],
    "YearBuilt": [2003],
    "YearRemodAdd": [2003],
    "RoofStyle": ["Gable"],
    "RoofMatl": ["CompShg"],
    "Exterior1st": ["VinylSd"],
    "Exterior2nd": ["VinylSd"],
    "MasVnrType": ["BrkFace"],
    "MasVnrArea": [196.0],
    "ExterQual": ["Gd"],
    "ExterCond": ["TA"],
    "Foundation": ["PConc"],
    "BsmtQual": ["Gd"],
    "BsmtCond": ["TA"],
    "BsmtExposure": ["No"],
    "BsmtFinType1": ["GLQ"],
    "BsmtFinSF1": [706],
    "BsmtFinType2": ["Unf"],
    "BsmtFinSF2": [0],
    "BsmtUnfSF": [150],
    "TotalBsmtSF": [856],
    "Heating": ["GasA"],
    "HeatingQC": ["Ex"],
    "CentralAir": ["Y"],
    "Electrical": ["SBrkr"],
    "1stFlrSF": [856],
    "2ndFlrSF": [854],
    "LowQualFinSF": [0],
    "GrLivArea": [1710],
    "BsmtFullBath": [1],
    "BsmtHalfBath": [0],
    "FullBath": [2],
    "HalfBath": [1],
    "BedroomAbvGr": [3],
    "KitchenAbvGr": [1],
    "KitchenQual": ["Gd"],
    "TotRmsAbvGrd": [8],
    "Functional": ["Typ"],
    "Fireplaces": [1],
    "FireplaceQu": ["TA"],
    "GarageType": ["Attchd"],
    "GarageYrBlt": [2003],
    "GarageFinish": ["RFn"],
    "GarageCars": [2],
    "GarageArea": [548],
    "GarageQual": ["TA"],
    "GarageCond": ["TA"],
    "PavedDrive": ["Y"],
    "WoodDeckSF": [0],
    "OpenPorchSF": [61],
    "EnclosedPorch": [0],
    "3SsnPorch": [0],
    "ScreenPorch": [0],
    "PoolArea": [0],
    "PoolQC": [None],
    "Fence": [None],
    "MiscFeature": [None],
    "MiscVal": [0],
    "MoSold": [2],
    "YrSold": [2010],
    "SaleType": ["WD"],
    "SaleCondition": ["Normal"]
    }

    input_df = pd.DataFrame(data_in)
    
    make_prediction(input_data=input_df)
     
