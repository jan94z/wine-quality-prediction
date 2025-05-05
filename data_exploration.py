import pandas as pd 

if __name__ == "__main__":
    white_path = './winequality-white.csv'
    red_path = './winequality-red.csv'
    
    # WHITE
    print("White Wine Quality Dataset")
    print("-----------------------------------")
    winequality_white = pd.read_csv(white_path, sep=';')
    print('Head:\n', winequality_white.head())
    print("-----------------------------------")
    print('Columns:', len(winequality_white.columns))
    print('Rows:', len(winequality_white))
    print("-----------------------------------")
    # summary
    describe_white = winequality_white.describe().round(2)
    print('Summary:\n', describe_white)
    print("-----------------------------------")
    # check for missing values
    print("Missing Values:\n", winequality_white.isnull().sum())
    
    print("-----------------------------------")

    # RED
    print("Red Wine Quality Dataset")
    print("-----------------------------------")
    winequality_red = pd.read_csv(red_path , sep=';')
    print('Head:\n', winequality_red.head())
    print("-----------------------------------")
    print('Columns:', len(winequality_red.columns))
    print('Rows:', len(winequality_red))
    print("-----------------------------------")
    # summary
    describe_red = winequality_red.describe().round(2)
    print('Summary:\n', describe_red)
    print("-----------------------------------")
    # check for missing values
    print("Missing Values:\n", winequality_red.isnull().sum())
    print("-----------------------------------")
