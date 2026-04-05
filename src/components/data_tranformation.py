import sys
import os
from dataclasses import dataclass

import numpy as np
import pandas as pd

from src.utils import save_object
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from src.exception import CustomException
from src.logger import logging


# ---------------- CONFIG CLASS ----------------
class DataTranformationsConfig:
    preprocessor_obj_file_path = os.path.join('artifacts', 'preprocessor.pkl')


# ---------------- MAIN TRANSFORMATION CLASS ----------------
class DataTranformations:
    def __init__(self):
        self.data_tranformation_config = DataTranformationsConfig()

    # -------- CREATE PREPROCESSOR PIPELINE --------
    def get_data_transformer_object(self):
        '''
        This function creates the preprocessing pipelines
        '''

        try:
            numerical_columns = ["writing score", "reading score"]

            categorical_columns = [
                "gender",
                "race/ethnicity",
                "parental level of education",
                "lunch",
                "test preparation course",
            ]

            # Numerical pipeline
            num_pipeline = Pipeline(
                steps=[
                    ('imputer', SimpleImputer(strategy='median')),
                    ('scaler', StandardScaler(with_mean=False))
                ]
            )

            # Categorical pipeline
            cat_pipeline = Pipeline(
                steps=[
                    ("imputer", SimpleImputer(strategy='most_frequent')),
                    ("one_hot_encoder", OneHotEncoder()),
                    ('scaler', StandardScaler(with_mean=False))
                ]
            )

            logging.info(f"Numerical Columns: {numerical_columns}")
            logging.info(f"Categorical Columns: {categorical_columns}")

            # Column Transformer
            preprocessor = ColumnTransformer(
                [
                    ("num_pipeline", num_pipeline, numerical_columns),
                    ("cat_pipeline", cat_pipeline, categorical_columns)
                ]
            )

            return preprocessor

        except Exception as e:
            raise CustomException(e, sys)

    # -------- APPLY TRANSFORMATION ON TRAIN & TEST --------
    def initiate_data_tranformations(self, train_path, test_path):
        try:
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)

            logging.info("Read Train and Test Data Successfully")

            preprocessing_obj = self.get_data_transformer_object()

            target_column_name = 'math score'

            # Split input and target for TRAIN
            #input_feature_train_df = train_df.drop(columns=[target_column_name], axis=1)
            input_feature_train_df = train_df.drop(columns=[target_column_name])

            target_feature_train_df = train_df[target_column_name]

            # Split input and target for TEST
            #input_feature_test_df = test_df.drop(columns=[target_column_name], axis=1)
            input_feature_test_df = test_df.drop(columns=[target_column_name])
            target_feature_test_df = test_df[target_column_name]

            logging.info("Applying preprocessing on training and testing data")

            # fit on train, transform on test
            input_feature_train_arr = preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr = preprocessing_obj.transform(input_feature_test_df)

            # Combine features and target
            train_arr = np.c_[input_feature_train_arr, np.array(target_feature_train_df)]
            test_arr = np.c_[input_feature_test_arr, np.array(target_feature_test_df)]

            logging.info("Saving preprocessing object")

            save_object(
                file_path=self.data_tranformation_config.preprocessor_obj_file_path,
                obj=preprocessing_obj
            )

            return (
                train_arr,
                test_arr,
                self.data_tranformation_config.preprocessor_obj_file_path,
            )

        except Exception as e:
            raise CustomException(e, sys)


# import sys
# import os
# from dataclasses import dataclass

# import numpy as np
# import pandas as pd


# from sklearn.compose import ColumnTransformer
# from sklearn.impute import SimpleImputer # Missing values
# from sklearn.pipeline import Pipeline
# from sklearn.preprocessing import OneHotEncoder, StandardScaler

# from src.exception import CustomException
# from src.logger import logging

# class DataTranformationsConfig:
#     preprocessor_obj_file_path = os.path.join('artifacts', 'preprocessor.pkl')

# class DataTranformations:
#     def __init__(self):
#         self.data_tranformation_config = DataTranformationsConfig()
#     def get_data_transformer_object(self):

#         '''
#         This Function is responcible for data transformation

#         '''
#         try:
#             numerical_columns = ["writing_score", "reading_score"]
#             categorical_columns = [
#                 "gender",
#                 "race_ethnicity",
#                 "parental_level_of_education",
#                 "lunch",
#                 "test_preparation_course",
#             ]

#             num_pipeline = Pipeline(
#                 steps=[
#                     ('imputer', SimpleImputer(strategy='median')), # Hadling Missing Values
#                     ('scalaer', StandardScaler())
#                 ]
#             )
#             cat_pipeline = Pipeline(
#                 steps=[
#                     ("imputer", SimpleImputer(strategy='most_frequent')),
#                     ("one_hot_encoder", OneHotEncoder()),
#                     ('scalar', StandardScaler())
#                 ]
#             )
#             logging.info(f"Numerical Columns: {numerical_columns}")
#             logging.info(f"Catagorical Columns: {categorical_columns}")

#             preprocessor = ColumnTransformer(
#                 [
#                     ("num_pipeline", num_pipeline, numerical_columns),
#                     ("cat_pipeline", cat_pipeline, categorical_columns)
#                 ]
#             )

#             return preprocessor
#         except Exception as e:
#             return CustomException(e, sys)
            