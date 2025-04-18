

from sklearn.base import BaseEstimator, TransformerMixin

class TemporalVariableTransformer(BaseEstimator, TransformerMixin):
    # Transformer for calculating the elapsed time between a reference variable and specified temporal variables.

    def __init__(self, variables, reference_variable):
       
        if not isinstance(variables, list):
            raise ValueError('variables should be a list')

        self.variables = variables  
        self.reference_variable = reference_variable  

    def fit(self, X, y=None):
    
        return self

    def transform(self, X):

        X = X.copy()

        for feature in self.variables:
            X[feature] = X[self.reference_variable] - X[feature]  

        return X 