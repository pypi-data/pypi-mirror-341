import sys
from pathlib import Path
file = Path(__file__).resolve()
parent, root = file.parent, file.parents[1]
sys.path.append(str(root))

from sklearn.pipeline import Pipeline
from feature_engine.imputation import ArbitraryNumberImputer, CategoricalImputer, MeanMedianImputer
from feature_engine.encoding import RareLabelEncoder, OrdinalEncoder
from feature_engine.selection import DropFeatures
from housing_prediction.processing.features import TemporalVariableTransformer
from xgboost import XGBRegressor


from housing_prediction.config.core import config


housing_prediction_pipe=Pipeline([
  
          # ===== IMPUTATION =====
    # impute numerical variables with the ArbitraryNumberImputer
    ('ArbitraryNumber_imputation', ArbitraryNumberImputer( arbitrary_number=-1, 
                                                          variables=config.model_config_.arbitrary_variable )),

     # impute numerical variables with the median value
    ('frequentNumber_imputation', MeanMedianImputer(imputation_method='median', 
                                                     variables=config.model_config_.numerical_features
                                                     )),

    # impute categorical variables with string missing
    ('missing_imputation', CategoricalImputer(imputation_method='missing', 
                                              variables=config.model_config_.categorical_features)),

    # == TEMPORAL VARIABLES ====
    ('elapsed_time', TemporalVariableTransformer(
        variables=config.model_config_.temporal_features, 
        reference_variable=config.model_config_.reference_variable)),

    ('drop_features', DropFeatures(features_to_drop=config.model_config_.drop_features)),

      # == CATEGORICAL ENCODING
    ('rare_label_encoder', RareLabelEncoder(tol=0.01, n_categories=5, 
                                            variables=config.model_config_.categorical_features)),

    # encode categorical and discrete variables using the target mean
    ('categorical_encoder', OrdinalEncoder(encoding_method='ordered', 
                                           variables=config.model_config_.categorical_features)), 

    ('XGB Boost Model', XGBRegressor(n_estimators=config.model_config_.n_estimators, 
                                     max_depth=config.model_config_.max_depth, 
                                     eta=config.model_config_.eta, 
                                     subsample=config.model_config_.subsample, 
                                     colsample_bytree=config.model_config_.colsample_bytree, 
                                     objective='reg:squarederror',
                                     random_state=config.model_config_.random_state))

     ])
