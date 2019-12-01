import unittest
import subprocess
import random
import os
import time
import pandas as pd
from sqlalchemy import create_engine
import pymysql
from horse_ai.cfg import *
from horse_ai.speed_model import HorseState, calculate_linreg_features

class TestMain(unittest.TestCase):


	def setUp(self):
		self.db_connection_str = 'mysql+pymysql://nec:H0rse@dmin@localhost:3300/ml'
		self.db_connection = create_engine(self.db_connection_str)
		self.nullHorse = pd.DataFrame(dict(zip(FEATURES_COL_LIST, [[0.]]*len(FEATURES_COL_LIST))))
		self.nullHorse[PLACE_FEATURE_NAME] = 3.
		self.nullHorse[PLACE_FEATURE_NAME+'_1'] = 2.
		self.nullHorse[PLACE_FEATURE_NAME+'_2'] = 1.



	def test_get_target_and_past(self):
		horseState = HorseState(self.nullHorse)
		target, past = horseState.get_target_and_past(0, STEPS)
		print(target)
		print(past)
		self.assertEqual(target['target_' + PLACE_FEATURE_NAME].values[0], 3.)
		self.assertEqual(past['past_' + PLACE_FEATURE_NAME + '_1'].values[0], 2.)
		self.assertEqual(past['past_' + PLACE_FEATURE_NAME + '_2'].values[0], 1.)
		target, past = horseState.get_target_and_past(-1, STEPS)
		self.assertEqual(target['target_' + PLACE_FEATURE_NAME].values[0], None)
		self.assertEqual(past['past_' + PLACE_FEATURE_NAME + '_1'].values[0], 3.)

	def test_linear_regression(self):
		STEPS = 3
		LINREG_COLUMNS = [PLACE_FEATURE_NAME, HORSE_SPEED_FEATURE_NAME]
		horseState = HorseState(self.nullHorse)
		target, past = horseState.get_target_and_past(0, STEPS)
		linreg = calculate_linreg_features(past, LINREG_COLUMNS, STEPS)
		self.assertAlmostEqual(linreg[PLACE_FEATURE_NAME+'_slope'].values[0], 1.)
		self.assertAlmostEqual(linreg[PLACE_FEATURE_NAME+'_linear_model_prediction'].values[0], 3.)
		self.assertAlmostEqual(linreg[PLACE_FEATURE_NAME+'_intercept'].values[0], 0.)
		self.assertAlmostEqual(linreg[HORSE_SPEED_FEATURE_NAME+'_slope'].values[0], 0.)

	def test_linear_regression_with_time_index(self):
		STEPS = 3
		LINREG_COLUMNS = [PLACE_FEATURE_NAME]
		self.nullHorse[RESULT_DATE_FEATURE_NAME] = pd.to_datetime('today')
		self.nullHorse[RESULT_DATE_FEATURE_NAME+'_1'] = pd.to_datetime('today') - pd.DateOffset(1)
		self.nullHorse[RESULT_DATE_FEATURE_NAME+'_2'] = pd.to_datetime('today') - pd.DateOffset(2)
		self.nullHorse[RESULT_DATE_FEATURE_NAME+'_3'] = pd.to_datetime('today') - pd.DateOffset(10)
		horseState = HorseState(self.nullHorse)
		target, past = horseState.get_target_and_past(0, STEPS)
		linreg = calculate_linreg_features(past, LINREG_COLUMNS, STEPS, True)
		print(linreg)
		self.assertLessEqual(linreg[PLACE_FEATURE_NAME+'_slope'].values[0], 0.2)
		self.assertLessEqual(linreg[PLACE_FEATURE_NAME+'_linear_model_prediction'].values[0], 2.2)


	# def test_mysql_connection(self):
	# 	df = pd.read_sql('SELECT * FROM ml_export_dataset LIMIT 10', con=self.db_connection)
	# 	print(df.head())
	# 	self.assertEqual(len(df), 10)

	# def test_ml_results(self):
	# 	df = pd.read_sql('SELECT * FROM ml_results LIMIT 10', con=self.db_connection)
	# 	print(df.head())
	# 	self.assertEqual(len(df), 10)
	# 	print('STD VALUE EXAMPLE: ' + str(df['std'].values[0]))
	# 	self.assertTrue(isinstance(df['std'].values[0], float))

if __name__ == '__main__':
	unittest.main()