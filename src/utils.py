import os
import sys 
import dill
import pickle
from sklearn.metrics import r2_score
from sklearn.model_selection import GridSearchCV

from src.exception import CustomException
from src.logger import logging
# from src.components.model_trainer import ModelTrainer


# utility function to save object in pickle file
# get file path for directory  , create directory , dump it.
def save_object(file_path, obj):
    try:
        dir_path = os.path.dirname(file_path)

        os.makedirs(dir_path, exist_ok=True)

        with open(file_path, "wb") as file_obj:
            pickle.dump(obj, file_obj)

    except Exception as e:
        raise CustomException(e, sys)
    
    # function to evaluate model.
def evaluate_model(X_train , y_train , X_test , y_test , models):
    try:
        report = {}
        for i in range(len(list(models))):
            model = list(models.values())[i]
            model.fit(X_train,y_train)
            y_train_pred = model.predict(X_train)
            y_test_pred = model.predict(X_test)
            train_model_score = r2_score(y_train , y_train_pred)
            test_model_score = r2_score(y_test , y_test_pred)
            report[list(models.keys())[i]] = test_model_score 
            
        return report
    
    except Exception as e:
        raise CustomException(e,sys)
  
# get root path  
def get_project_root():
     return os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
 
# get the relative path.
def get_full_path(relative_path):
    return os.path.join(get_project_root() , relative_path)


def prepare_directory(file_path):
    """
    Extracts the directory from a file path and creates 
    it if it doesn't already exist.
    """
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
    except Exception as e:
        raise CustomException(e,sys)


    