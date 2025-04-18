from datetime import datetime
import sys
from pathlib import Path
file = Path(__file__).resolve()
parent, root = file.parent, file.parents[1]
sys.path.append(str(root))

from typing import List, Optional, Tuple, Union

import numpy as np
import pandas as pd
from pydantic import BaseModel, ValidationError, Field

from housing_prediction.config.core import config
from housing_prediction.processing.data_manager import pre_pipeline_preparation


def validate_inputs(*, input_df: pd.DataFrame) -> Tuple[pd.DataFrame, Optional[dict]]:
    """Check model inputs for unprocessable values."""

    pre_processed = pre_pipeline_preparation(df=input_df)
    validated_data = pre_processed[config.model_config_.features].copy()
    errors = None

    try:
        # replace numpy nans so that pydantic can validate
        MultipleDataInputs(
            inputs=validated_data.replace({np.nan: None}).to_dict(orient="records")
        )
    except ValidationError as error:
        errors = error.json()

    return validated_data, errors

class DataInputSchema(BaseModel):
    Id: int
    MSSubClass: int
    MSZoning: str
    LotFrontage: Optional[float]
    LotArea: int
    Street: str
    Alley: Optional[str]
    LotShape: str
    LandContour: str
    Utilities: str
    LotConfig: str
    LandSlope: str
    Neighborhood: str
    Condition1: str
    Condition2: str
    BldgType: str
    HouseStyle: str
    OverallQual: int
    OverallCond: int
    YearBuilt: int
    YearRemodAdd: int
    RoofStyle: str
    RoofMatl: str
    Exterior1st: str
    Exterior2nd: str
    MasVnrType: Optional[str]
    MasVnrArea: Optional[float]
    ExterQual: str
    ExterCond: str
    Foundation: str
    BsmtQual: Optional[str]
    BsmtCond: Optional[str]
    BsmtExposure: Optional[str]
    BsmtFinType1: Optional[str]
    BsmtFinSF1: int
    BsmtFinType2: Optional[str]
    BsmtFinSF2: int
    BsmtUnfSF: int
    TotalBsmtSF: int
    Heating: str
    HeatingQC: str
    CentralAir: str
    Electrical: Optional[str]
    FirstFlrSF: int = Field(..., alias='1stFlrSF')
    SecondFlrSF: int = Field(..., alias='2ndFlrSF')
    LowQualFinSF: int
    GrLivArea: int
    BsmtFullBath: int
    BsmtHalfBath: int
    FullBath: int
    HalfBath: int
    BedroomAbvGr: int
    KitchenAbvGr: int
    KitchenQual: str
    TotRmsAbvGrd: int
    Functional: str
    Fireplaces: int
    FireplaceQu: Optional[str]
    GarageType: Optional[str]
    GarageYrBlt: Optional[int]
    GarageFinish: Optional[str]
    GarageCars: int
    GarageArea: int
    GarageQual: Optional[str]
    GarageCond: Optional[str]
    PavedDrive: str
    WoodDeckSF: int
    OpenPorchSF: int
    EnclosedPorch: int
    ThreeSsnPorch: int = Field(..., alias='3SsnPorch')
    ScreenPorch: int
    PoolArea: int
    PoolQC: Optional[str]
    Fence: Optional[str]
    MiscFeature: Optional[str]
    MiscVal: int
    MoSold: int
    YrSold: int
    SaleType: str
    SaleCondition: str

    class Config:
        populate_by_name = True

class MultipleDataInputs(BaseModel):
    inputs: List[DataInputSchema]


