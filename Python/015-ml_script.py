"""
This script does all the Machine Learning steps and outputs the results to the user. The only requirement is that the user input a valid PATH to the dataset.
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.linear_model import LinearRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier

# You can add supported models here. Make sure they are imported
SUPPORTED_MODELS= ["LinearRegression()"]

from sklearn.preprocessing import LabelEncoder

from sklearn.model_selection import train_test_split

# Metrics for KNeighbors Classifier
from sklearn.metrics import accuracy_score, classification_report 

# Metrics for LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score


import random 

# Options. Change as needed.
HIST_SIZE = (20,13)
HEATMAP_SETTINGS = {"annot": True, "cmap": "Blues"}
FIG_SIZE = (15,8)

# Do not change
BIGGEST_SEED = 2**32- 1

NO_SEED_INPUT= -1

FIRST_RESULT = "Classification Result"

CLASSIFICATION_RESULT_TEMPLATE = "Accuracy score: {accuracy_sc}\nClassification Report: {classification_re}"
R_SQ_TEMPLATE = "Mean Squared Error: {mean_sq_err}\nMean Absolute Error: {mean_abs_err}\nR Squared Score: {rsq_sc}"

def args_match_dtype(*args,dtype):
    try:
        for arg in args:
            eval("type(arg)==dtype")
    except Exception as e:
        raise e(f"Incorrect data. '{arg}' does not match intended type: {dtype}.")
    else:
        return True

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

def all_inputs_valid(**kwargs) -> bool:    
    check_1 = args_are_str(kwargs["dataset"],kwargs["dependent_var"])
    check_2 = args_are_int(kwargs["random_state"])
    check_3 = args_are_float(kwargs["test_size"])
    check_4 = args_are_list(kwargs["str_columns"])
    check_5 = args_are_bool(kwargs["str_data_present"])

    checks = (check_1,check_2,check_3,check_4,check_5)
    return all(checks)    

# Model function
def model_predict(dataset:str,
                  dependent_var:str, 
                  str_data_present:bool,
                  str_columns:list,
                  random_state:int,
                  test_size:float,
                  model_used: str,
                 ) -> tuple:  

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
        print("Dataset loading complete.")

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
        model = model_training(model_used=model_used,X_train=X_train,y_train=y_train)

        print("Model training complete.\n")

        # 5. Model testing.

        y_pred = model_testing(model=model,X_test=X_test)
        print("Model testing complete.")

        # 6. Model evaluation.
        
        output = model_evalution(y_test=y_test,y_pred=y_pred)
        return output
    
def load_dataset(dataset:str) -> pd.DataFrame:
    """
    Step 1 of the Machine Learning steps. This functions returns a DataFrame object, which can be used in the next step.
    """
    return pd.read_csv(dataset)

def visualize_data(df:pd.DataFrame) -> None:
    """
    Visualizes data. sns.heatmap, pd.DataFrame.hist, and plt.Figure methods are used.
    """
    heatmap_settings = HEATMAP_SETTINGS
    hist_settings = HIST_SIZE
    figure_settings = FIG_SIZE

    print(sns.heatmap(df.corr(), **heatmap_settings))

    df.hist(figsize=hist_settings)
        
    plt.figure(figsize=figure_settings)

    return None

def data_preprocessing(df:pd.DataFrame,dependent_var:str,str_data_present:bool) -> tuple[pd.DataFrame, pd.Series]:
    """
    Step 2 of the Machine Learning steps. Converts textual columns to numerical data, and returns 2 objects: The independent variables (X) and the dependent variable (y).
    """
    if str_data_present:
        df = convert_text_col_to_num(df=df)
    X = df.drop(dependent_var, axis=1)
    y = df[dependent_var]

    return X, y

def convert_text_col_to_num(df:pd.DataFrame) -> pd.DataFrame:
    """
    Converts the DataFrame's (dependent variable y's) texts into numerical data. Uses LabelEncoder.
    """
    for column in df.columns():
        le = LabelEncoder()
        df[column]= le.fit_transform(df[column])

    return df

def data_splitting(X:pd.DataFrame,y:pd.Series,test_size:float,random_state:int) -> tuple[pd.DataFrame, pd.Series, pd.DataFrame, pd.Series]:
    """
    Step 3 of the Machine Learning steps. Splits the independent and dependent variables into 2 categories: Training, and Testing.
    """
    X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=test_size,random_state=random_state)

    return X_train, X_test, y_train, y_test


def model_training(model_used: str, X_train: pd.DataFrame, y_train: pd.Series):
    """
    Step 4 of the Machine Learning steps. Trains the model with the given training dataset. Returns the trained Model.
    """
    model = model_used

    model.fit(X_train,y_train)
    return model

def model_testing(model,X_test: pd.DataFrame) -> np.ndarray:
    """
    Step 5 of the Machine Learning steps. Tests the model with the given training dataset. Returns the prediction.
    """
    y_pred = model.predict(X_test)
    return y_pred

def model_evalution(y_test: pd.Series, y_pred: pd.Series) -> tuple:
    """
    Step 6 of the Machine Learning steps. Evaluates the model by comparing the Model's prediction with the actual dataset's values. Returns the result in a string. 
    """ 
    results = {FIRST_RESULT: None, "Regression Result": None}
    
    for result in results.keys():
        try:
            if result == FIRST_RESULT:
                results[result] = CLASSIFICATION_RESULT_TEMPLATE.format(
                    accuracy_sc = accuracy_score(y_test,y_pred), 
                    classification_re = classification_report(y_test,y_pred)
                    )
            else: # Regression
                results[result] = R_SQ_TEMPLATE.format(
                    mean_sq_err = mean_squared_error(y_test, y_pred), 
                    mean_abs_err = mean_absolute_error(y_test, y_pred), 
                    rsq_sc = r2_score(y_test, y_pred)
                    )
        except Exception:
            results[result] = f"{result}: N/A"
    
    return tuple(results.values())  


if __name__ == "__main__":
    dataset = input("Enter dataset path including the dataset file itself. Path must be in your computer directory:\n").strip('"').strip("'")

    dependent_var = input("Enter dependent variable (i.e. the column name of the variable you want to predict values of, case-sensitive):\n")

    str_in_data = input("Are there textual data in the dataset (y/n)?\n")
    str_data_present = True if str_in_data.lower().startswith("y") else False

    str_columns = 'input("Enter column names (case-sensitive) that have textual values, separated by a comma:\n").split(",")'
    if str_data_present:
        eval(str_columns)

    seed = int(input(f"Enter seed (Enter {NO_SEED_INPUT} to auto generate seed):\n"))
    random_state = seed if seed!=NO_SEED_INPUT else random.randrange(BIGGEST_SEED)

    test_size = int(input("Enter the test/train split for test size (E.g. 70 if 70/30):\n"))/100
    

    for model in SUPPORTED_MODELS:
        print(f"Model used: {model}.")
        model_used = eval(model)

        output = model_predict(dataset=dataset,dependent_var=dependent_var,str_data_present=str_data_present,str_columns=str_columns,random_state=random_state,test_size=test_size,model_used=model_used)

        for result in output:
            print(result)

    
