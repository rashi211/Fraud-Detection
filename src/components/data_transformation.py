from sklearn.preprocessing import StandardScaler,OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

import os
import sys
import pandas as pd
import numpy as np
from dataclasses import dataclass
# Add the root directory of the project to the sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from src.utils import save_object
from src.exception import CustomException
from src.logger import logging
from src.components.data_ingestion import DataIngestion

@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path = os.path.join('artifacts',"preprocessor.pkl")

class DataTransformation:
    def __init__(self):
        self.data_transformation_config =  DataTransformationConfig()
    
    def get_data_transformer_object(self):
        ''' This is responsible for data transformation
        '''
        logging.info("Entered Transformation Component ")
        try :
            num_col = ["writing_score","reading_score"]
            cat_col = ["gender","race_ethnicity",
                       "parental_level_of_education",
                       "lunch","test_preparation_course"]

            # Impute numerical data with median and scaling using standard scaler
            num_pipeline = Pipeline(
                [
                    ("imputer",SimpleImputer(strategy="median")),
                    ("scaler",StandardScaler())
                ]
            )
            # Impute categorical data with mode and one hot encoding and scaling
            cat_pipeline = Pipeline(
                [
                    ("imputer",SimpleImputer(strategy="most_frequent")),
                    ("ohe",OneHotEncoder()),
                    ("scaler",StandardScaler(with_mean=False))
                ]
            )
            # Log categorical and numerical column
            logging.info("Categorical columns:{}".format(cat_col))
            logging.info("Numerical columns:{}".format(num_col))

            # convert it into transformer
            preprocessor  = ColumnTransformer(
                [
                    ("num_pipeline",num_pipeline,num_col),
                    ("cat_pipeline",cat_pipeline,cat_col)
                ]
            )

            return preprocessor
        
        except Exception as e:
            raise CustomException(e,sys)
    
    def start_data_transformation(self,train,test):
        
        try:
            train_df = pd.read_csv(train)
            test_df = pd.read_csv(test)

            logging.info("Read train and test data complrted") 
            logging.info("Calling preprocessing object")
            
            preprocessing_obj = self.get_data_transformer_object()

            target_col_name = "math_score"
            num_cat_Col = ["writing_score","reading_score"]

            input_feature_train_df=train_df.drop(columns=[target_col_name],axis=1)
            target_feature_train_df=train_df[target_col_name]

            input_feature_test_df=test_df.drop(columns=[target_col_name],axis=1)
            target_feature_test_df=test_df[target_col_name]
            
            logging.info(f"Apply preprocessor object")

            input_feature_train_arr = preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr = preprocessing_obj.transform(input_feature_test_df)

            train_arr = np.c_[
                input_feature_train_arr, np.array(target_feature_train_df)
            ]
            test_arr = np.c_[input_feature_test_arr, np.array(target_feature_test_df)]

            logging.info(f"Saved preprocessing object.")

            save_object(
                file_path = self.data_transformation_config.preprocessor_obj_file_path,
                obj = preprocessing_obj
            )

            return (
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_file_path
            )
        except Exception as e:
            raise CustomException(e,sys)

if __name__ == "__main__":
    obj = DataIngestion()
    train_d,test_d = obj.initiate_data_ingestion()

    obj1 = DataTransformation()
    obj1.start_data_transformation(train_d,test_d)