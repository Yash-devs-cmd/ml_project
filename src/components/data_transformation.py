import sys
import os 
from dataclasses import dataclass
import numpy as np
import pandas as pd 
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder , StandardScaler

from src.exception import CustomException
from src.logger import logging
from src.utils import save_object


@dataclass 
class DataTransformationConfig:
    preprocessor_obj_file_path = os.path.join('artifacts' , 'preprocessor.pkl')
    
class Datatransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()
        # Do Scaling and Encoding of Numerical and Categorical Features of the dataset.
    def get_data_transformer_object(self):
        # this function is responsible for scaling and encoding 
        try:
        # get numerical and catgorical features 
            num_features = ['writing_score' , 'reading_score']
            cat_features = [
            'gender' ,
            'race_ethnicity' ,
            'parental_level_of_education' , 
            'lunch' , 
            'test_preparation_course'
            ]
            logging.info('Categorical Columns Encoding Completed')
            logging.info('Numerical Columns Scaling Completed')
            
            # handle missing values and do scaling
            num_pipeline = Pipeline(
                steps = [
                    
                    ('imputer' , SimpleImputer(strategy='median')),
                    ('scaler' , StandardScaler())
                ]
            )
            # handle missing values and do encoding
            cat_pipeline = Pipeline(
                steps  = [
                    ('imputer' ,SimpleImputer(strategy='most_frequent')),
                    ('one_hot_encoder' , OneHotEncoder()),
                    ('scaler' , StandardScaler(with_mean=False))
                ]
            )
           
            # combine num_pipeline and cat_pipeline in preprocessor
            preprocessor = ColumnTransformer(
                [
                    ('num_pipeline' ,num_pipeline , num_features),
                    ('cat_pipeline' ,cat_pipeline , cat_features),
                ]
            )
            
            return preprocessor

        except Exception as e:
            raise CustomException(e,sys)
    
   
    
    def initiate_data_transformation(self , train_path , test_path):    
        try:
            # read training and test data paths 
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)
            
            # print('train_df',train_df)
            # print('test_df',test_df)
            
            logging.info('Read train and test data completed')
            logging.info('Obtaining preprocessing object')
            # intialize the preprocessor object
            preprocessing_obj = self.get_data_transformer_object()
            # print('preprocessing object' , preprocessing_obj)
            # get the target column 
            target_column_name = 'math_score'
            
            # create input and target features for train and test-sets 
            input_feature_train_df = train_df.drop(columns=[target_column_name] , axis=1)
            target_feature_train_df = train_df[target_column_name]
            
            input_feature_test_df = test_df.drop(columns=[target_column_name] , axis=1)
            target_feature_test_df = test_df[target_column_name]
            
            logging.info('Applying preprocessing object on training dataframe and testing dataframe')
            # do model training for preprocessor object on training and test sets.
            
            input_feature_train_arr = preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr =  preprocessing_obj.transform(input_feature_test_df)
            
            # print('input_feature_train_arr' , input_feature_train_arr)
            # print('input_feature_test_arr' , input_feature_test_arr)
            
            # basically column stack the array . [ transformed_features | target ]
                                               #  like x1, x2, x3, ..., xN,| y

            train_arr = np.c_[ input_feature_train_arr , np.array(target_feature_train_df)]
            test_arr = np.c_[input_feature_test_arr , np.array(target_feature_test_df)]
            # print('stacked train array' , train_arr)
            
            logging.info('Saved preprocessing object')
            
            # save the pickle file in memory.
            save_object(
                        file_path=self.data_transformation_config.preprocessor_obj_file_path,
                        obj=preprocessing_obj
                        )
            return (
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_file_path,
            )
            
            

        except Exception as e:
            raise CustomException(e,sys)
        
        

    
            