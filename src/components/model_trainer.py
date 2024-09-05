import os 
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from dataclasses import dataclass
from src.logger import logging
from src.exception import CustomException
from sklearn.metrics import r2_score
from sklearn.ensemble import (RandomForestRegressor,
                              GradientBoostingRegressor,
                              AdaBoostRegressor)
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.neighbors import KNeighborsRegressor
from xgboost import (XGBRFRegressor,
                     XGBRegressor)
from src.utils import evaluate_models,save_object
from src.components.data_ingestion import DataIngestion
from src.components.data_transformation import DataTransformation

# file path to save the best model
class ModelTrainingConfig:
    trained_model_file_path = os.path.join("artifacts","model_training.pkl")

class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = ModelTrainingConfig()
    
    def initiate_model_trainer(self,train_arr,test_arr):
        try:
            logging.info("Split train and test data")
            # splitting to test and train with X and Y
            X_train,X_test,y_train,y_test = (
                train_arr[:,:-1],
                test_arr[:,:-1],
                train_arr[:,-1],
                test_arr[:,-1]
            )
            # basic different models to try
            models = {
                "Random Forest": RandomForestRegressor(),
                "Decision Tree": DecisionTreeRegressor(),
                "Gradient Boosting": GradientBoostingRegressor(),
                "Linear Regression": LinearRegression(),
                "XGBRFRegressor": XGBRFRegressor(),
                "XGBRegressor": XGBRegressor(),
                "AdaBoost Regressor": AdaBoostRegressor(),
                "KNN": KNeighborsRegressor()
            }

            params={
                "Decision Tree": {
                    'criterion':['squared_error', 'friedman_mse', 'absolute_error', 'poisson'],
                    # 'splitter':['best','random'],
                    # 'max_features':['sqrt','log2'],
                },
                "Random Forest":{
                    # 'criterion':['squared_error', 'friedman_mse', 'absolute_error', 'poisson'],
                    # 'max_features':['sqrt','log2',None],
                    'n_estimators': [8,16,32,64,128,256]
                },
                "Gradient Boosting":{
                     'loss':['squared_error', 'huber', 'absolute_error', 'quantile'],
                    'learning_rate':[.1,.01,.05,.001],
                    'subsample':[0.6,0.7,0.75,0.8,0.85,0.9],
                     'criterion':['squared_error', 'friedman_mse'],
                     'max_features':['auto','sqrt','log2'],
                    'n_estimators': [8,16,32,64,128,256]
                },
                "Linear Regression":{},
                "XGBRegressor":{
                    'learning_rate':[.1,.01,.05,.001],
                    'n_estimators': [8,16,32,64,128,256]
                },
                "CatBoosting Regressor":{
                    'depth': [6,8,10],
                    'learning_rate': [0.01, 0.05, 0.1],
                    'iterations': [30, 50, 100]
                },
                "AdaBoost Regressor":{
                    'learning_rate':[.1,.01,0.5,.001],
                    'loss':['linear','square','exponential'],
                    'n_estimators': [8,16,32,64,128,256]
                }
                
            }
            
            # loop through all the above models to create a dictionary with r2 score of test and train
            model_report:dict = evaluate_models(X_train,y_train,X_test,y_test,models,params)
            #for i in range(len(list(model_report))):
                # print(list(model_report.keys())[i],list(model_report.values())[i])
            # save the model
            logging.info(model_report)
            
            # To get the best model score from dict
            best_model_score = max(sorted(pd.DataFrame(model_report.values())[0]))

            # To get best model name from dict
            best_model_name =list(model_report.keys())[list(pd.DataFrame(model_report.values())[0]).index(best_model_score)]
            best_model = models[best_model_name]

            # if the best model is not evn 60% accurate then we need to do feature engineering
            if best_model_score<0.6:
                raise CustomException("No best model found")
            logging.info(f"Best found model on both training and testing dataset")

            # odel_trainer_config is the object of ModelTrainingConfig.
            # trained_model_file_path - this will be the path where the model si supposed to be saved
            # best _del is the final model to be sured to use for pred
            save_object(
                file_path = self.model_trainer_config.trained_model_file_path,
                obj = best_model
            )

            pred = best_model.predict(X_test)
            r2_square = r2_score(y_test,pred)
            return r2_square

        except Exception as e:
            raise CustomException(e,sys)

if __name__ == "__main__":
    obj = DataIngestion()
    train_d,test_d = obj.initiate_data_ingestion()

    obj1 = DataTransformation()
    train_arr,test_arr,_ = obj1.start_data_transformation(train_d,test_d)

    obj2 = ModelTrainer()
    obj2.initiate_model_trainer(train_arr,test_arr)