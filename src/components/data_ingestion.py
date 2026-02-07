import os
import sys
from src.exception import CustomException
from src.logger import logging
import pandas as pd
from sklearn.model_selection import train_test_split
from dataclasses import dataclass
from src.components.data_transformation import Datatransformation
from src.components.data_transformation import DataTransformationConfig
from src.components.model_trainer import ModelTrainerConfig
from src.components.model_trainer import ModelTrainer
from src.utils import get_full_path
from src.utils import prepare_directory



@dataclass
class DataIngestionConfig:
    # create train data path , and the train data will be available in artifacts,same for test-data 
    train_data_path: str = get_full_path('artifacts/train.csv')
    test_data_path: str = get_full_path('artifacts/test.csv')
    raw_data_path: str = get_full_path('artifacts/data.csv')

class DataIngestion:
    def __init__(self):
        # train, test,raw will be saved in ingestion_config
        self.ingestion_config = DataIngestionConfig()
        # print(self.ingestion_config.train_data_path)
        # self.ingestion_config.train_data_path  contrains training data path.
        
    def initiate_data_ingestion(self):
        logging.info("Entered the data ingestion method or component")
        try:
            # read the data
           source_path = get_full_path('notebook/data/stud.csv')
           df = pd.read_csv(source_path)
           # join the path and read the dataset as well.
           logging.info('Read The Dataset as Dataframe')
            
            # get the path of artifact folder and create a new folder.
           prepare_directory(self.ingestion_config.train_data_path)
        #    print('path of train data:' , (self.ingestion_config.train_data_path))
        #    print('self ingestion config path:' , (self.ingestion_config))
            
            # save the dataframe in artifact folder.
           df.to_csv(self.ingestion_config.raw_data_path , index=False , header=True)
           
           
           logging.info("Train Test Split Initiated")
           
           # create train test split 
           train_set , test_set = train_test_split(df , test_size=0.2 , random_state=42)
           # save train and test sets in artifacts.
           train_set.to_csv(self.ingestion_config.train_data_path , index=False , header=True)
           
           test_set.to_csv(self.ingestion_config.test_data_path , index=False , header=True)
           
           logging.info("Ingestion of Data is Completed")
           
           return (
               self.ingestion_config.train_data_path,
               self.ingestion_config.test_data_path,
           )

        except Exception as e:
            logging.error("Error occurred in data ingestion")
            raise CustomException(e, sys) 
        
        
        
if __name__ =="__main__":
    # testing it.
    obj = DataIngestion()
    train_data,test_data =  obj.initiate_data_ingestion()
    data_transformation = Datatransformation()
    train_arr,test_arr =  data_transformation.initiate_data_transformation(train_data , test_data)
    modeltrainer = ModelTrainer()
    print(modeltrainer.initiate_model_training(train_arr,test_arr))
    
    
    

    