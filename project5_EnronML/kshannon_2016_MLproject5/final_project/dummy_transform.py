
from sklearn.base import BaseEstimator


class DummyTransform(BaseEstimator):
	'''
	This class provides
		1. def fit
		2. def transform
		3. def fit_transform 
	Allowing you to bypass chained steps of an SkLearn Pipeline if you do not
	want to use a select, scaler or pca estimator.
	'''

	def __init__(self):
		pass


	def fit(self, X, y=None, **fit_params):
		return self



	def transform(self, X):
		return X


	def fit_transform(self, X, y=None, **fit_params):
		return X

		