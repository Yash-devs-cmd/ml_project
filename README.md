## End to End ML 


## Notes 


Data Ingestion 

Data ingestion is the process of retrieving or fetching data from a data source


# create Data Ingestion config class and define the path 
# create Data Ingestion class for intiating data ingestion 

# create project root 
# read data from dataset  as dataframe 
# get path of artifact folder 
# save the dataframe in artifact folder 
# create train test split 
# save train and test sets in artifact folder
# return train and test paths .

Data Transformation is the process of transforming data .
Flow:-->
# read train and test datasets
# initialize the processor object to get encoded numerical and categorical columns
# define target columns
# make input and target columns for train and test-sets
# model-train the input features for both train and test sets
# column stack the array so we get a combined array
# save the object
# return train,test and file_path of processor and to save in artifacts folder.