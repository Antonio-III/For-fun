import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.linear_model import LinearRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier


from sklearn.preprocessing import LabelEncoder

from sklearn.model_selection import train_test_split

# Metrics for KNeighbors Classifier
from sklearn.metrics import accuracy_score, classification_report 

# Metrics for LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score


import random 

SUPPORTED_MODELS= {"KNeighborsClassifier": KNeighborsClassifier(),
                    "LinearRegression": LinearRegression(),
                    "DecisionTreeClassifier": DecisionTreeClassifier()}

MODEL_TYPES = {"KNeighborsClassifier": "Categorical",
                    "LinearRegression": "Continuous",
                    "DecisionTreeClassifier": "Categorical"}

def args_match_dtype(*args,dtype):
    try:
        for arg in args:
            val = eval("type(arg)==dtype")
    except Exception as e:
        raise e(f"Cannot convert '{arg}' to {dtype}.")
    else:
        if val ==False:
            raise Exception(f"Cannot convert {arg} to {dtype}.")

# Check functions
def args_are_str(*args):
    return args_match_dtype(args,dtype=str)
def args_are_int(*args):
    return args_match_dtype(args,dtype=int)
def args_are_float(*args):
    return args_match_dtype(args,dtype=float)
def args_are_list(*args):
    return args_match_dtype(args,dtype=list)
def args_are_bool(*args):
    return args_match_dtype(args,dtype=bool)    

def model_predict(dataset:str,
                  dependent_var:str, 
                  str_data_present:bool,
                  str_columns:list,
                  random_state:int,
                  test_size:float,
                  model_used: str,
                  supported_models = SUPPORTED_MODELS,
                  model_types = MODEL_TYPES
                 ) -> tuple: 
    
    def all_inputs_valid(**kwargs) -> bool:    
        check_1 = args_are_str(kwargs["dataset"],kwargs["dependent_var"],dtype=str)
        check_2 = args_are_int(kwargs["random_state"],dtype=int)
        check_3 = args_are_float(kwargs["test_size"],dtype=float)
        check_4 = args_are_list(kwargs["str_columns"],dtype=list)
        check_5 = args_are_bool(kwargs["str_data_present"],dtype=bool)

        return all(check_1,check_2,check_3,check_4,check_5)     

    if all_inputs_valid(dataset             =dataset,
                        dependent_var       =dependent_var, 
                        str_data_present    =str_data_present,
                        str_columns         =str_columns,
                        random_state        =random_state,
                        test_size           =test_size,
                        ):
        
        # 1.2 Loading dataset.
        df = load_dataset(dataset=dataset)

        print(f"Dataset head:\n{df.head()}")
        print("Dataset loading complete.\n")

        # Visualization
        visualize_data(df=df) if not str_data_present else None

        # 2. Data cleaning/preprocessing.
        X,y = data_preprocessing(df=df,dependent_var=dependent_var,str_data_present=str_data_present)

        print(f"Features (X):\n{X.head()}")
        print(f"Features (y):\n{y.head()}")
        print("Data cleaning complete.\n")

        # 3. Data splitting
        X_train, X_test, y_train, y_test = data_splitting(X,y,test_size=test_size,random_state=random_state)

        print(f"Training set size: {X_train.shape[0]}.")
        print(f"Test set size:{X_test.shape[0]}.")
        print("Data splitting complete.\n")

        # 4. Model training.
        model = model_training(supported_models=supported_models,model_used=model_used,X_train=X_train,y_train=y_train)

        print("Model training complete.\n")

        # 5. Model testing.

        y_pred = model_testing(model=model,X_test=X_test)

        print("Model testing complete.\n")

        # 6. Model evaluation.
        
        output = model_evalution(model_type=model_types[model_used],y_test=y_test,y_pred=y_pred)
        return output
    
def load_dataset(dataset:str):
    return pd.read_csv(dataset)

def visualize_data(df:pd.DataFrame):
    heatmap_settings ={"annot": True, "cmap":"Blues"}
    hist_settings = (20,13)
    figure_settings = (15,8)

    print(sns.heatmap(df.corr(), **heatmap_settings))

    df.hist(figsize=hist_settings)
        
    plt.figure(figsize=figure_settings)

    return None

def data_preprocessing(df:pd.DataFrame,dependent_var:str,str_data_present:bool):
    if str_data_present:
        df = convert_text_col_to_num(df=df)
    X = df.drop(dependent_var, axis=1)
    y = df[dependent_var]

    return X, y

def convert_text_col_to_num(df:pd.DataFrame):
    for column in df.columns():
        le = LabelEncoder()
        df[column]= le.fit_transform(df[column])

    return df

def data_splitting(X:pd.DataFrame,y:pd.Series,test_size:float,random_state:int):
    X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=test_size,random_state=random_state)
    return X_train, X_test, y_train, y_test


def model_training(supported_models:dict,model_used:str,X_train,y_train):
    model = supported_models[model_used]

    model.fit(X_train,y_train)
    return model

def model_testing(model,X_test):
    y_pred = model.predict(X_test)
    return y_pred
def model_evalution(model_type:str,y_test,y_pred):
    output = ()
    match model_type:
        case "Categorical":
            output = (accuracy_score(y_test,y_pred), classification_report(y_test,y_pred))
        case "Continuous":
            output = ( mean_squared_error(y_test,y_pred), mean_absolute_error(y_test,y_pred), r2_score(y_test,y_pred) )
        case _:
            raise Exception("Model neither predicts categorical or continuous values.")
    return output

if __name__ == "__main__":
    dataset = input("Enter dataset path including the dataset file itself. Path must be in your computer directory:\n")
    dependent_var = input("Enter dependent variable (i.e. the column name of the variable you want to predict):\n")
    str_in_data = input("Are there textual data in the dataset (y/n)?\n")
    str_data_present = True if str_in_data.lower().startswith("y")=="y" else False
    str_columns = input("Enter column names (must be exactly as they appear in the dataset) that have textual values, separated by a comma:\n").split(",")
    seed = int(input("Enter seed (Enter -1 to auto generate seed):\n"))
    random_state = seed if seed!=-1 else random.randrange(2**32-1)
    test_size = int(input("Enter the test/train split for test size (E.g. 70 if 70/30):\n"))/100
    model_used = input(f"Enter model used. Must match the name. Supported models:\n{list(MODEL_TYPES.keys())}")
    output = model_predict(dataset=dataset,dependent_var=dependent_var,str_data_present=str_data_present,str_columns=str_columns,random_state=random_state,test_size=test_size,model_used=model_used)
    for result in output:
        print(result)

    
