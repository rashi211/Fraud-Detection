import os
import sys

# Add the root directory of the project to the sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.exception import CustomException
from src.logger import logging
import pandas as pd
from sklearn.model_selection import train_test_split
class DataIngestionConfig:
    def __init__ (self):
        # this will give the path where new train,test and raw data should be stored
        self.train_data_path = os.path.join('artifacts',"train.csv")
        self.test_data_path = os.path.join('artifacts',"test.csv")
        self.raw_data_path = os.path.join('artifacts',"data.csv")

class DataIngestion:
    # creating an instance of the other class from the below class
    def __init__ (self):
        self.ingestion_config = DataIngestionConfig()
    
    # method used for logging, train , test split and sving back file to the path
    def initiate_data_ingestion(self):
        logging.info("Entered the Data Ingestion Conponent")
        # this can fail as well so data ingestion is in try catch
        try:
            # r for black slashes
            df = pd.read_csv(r'notebook\data\stud.csv')
            logging.info("Read the dataset from dataframe")

            #Having the data,create a dir to save the files
            os.makedirs(os.path.dirname(self.ingestion_config.test_data_path),exist_ok=True)
            # save raw data file to the dir created above
            df.to_csv(self.ingestion_config.raw_data_path,index=False,header = True)
            #log starting of split
            logging.info("Train Test Split Initiated")
            train_set, test_set = train_test_split(df,test_size=0.2,random_state =43)
            
            train_set.to_csv(self.ingestion_config.train_data_path,index=False,header= True)
            test_set.to_csv(self.ingestion_config.test_data_path,index=False,header=True)

            #log end of split
            logging.info("Ingestion of Data is completed")

            # return path for test and train
            return(
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path
            )
        except Exception as e:
            raise CustomException(e,sys)

'''
config = DataIngestionConfig()
print(os.path.dirname(config.train_data_path)) # Output: artifacts/train.csv
print(os.path.dirname(config.test_data_path)) # Output: artifacts/train.csv
print(os.path.dirname(config.raw_data_path)) # Output: artifacts/train.csv
print(config.test_data_path)   # Output: artifacts/test.csv
print(config.raw_data_path)    # Output: artifacts/data.csv
 '''  
if __name__ == "__main__":
    obj = DataIngestion()
    train_data,test_data = obj.initiate_data_ingestion()
    print(train_data)
    print(test_data)
    print(obj.ingestion_config)

