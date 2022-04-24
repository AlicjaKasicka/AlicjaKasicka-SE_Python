from flask import Flask, app
import numpy as np
import pandas as pd

app = Flask(__name__)

def before_request():
    app.jinja_env.cache = {}

app.before_request(before_request)
data = []

print("Give a path to a csv file: ")
FILE_PATH = input()

class ColumnInfo():
    def __init__(self, name, minimum, maximum, mean, tenth_percentile, ninetieth_percentile, per_miss_values):
        self.name = name
        self.minimum = minimum
        self.maximum = maximum
        self.mean = mean
        self.tenth_percentile = tenth_percentile
        self.ninetieth_percentile = ninetieth_percentile
        self.per_miss_values = per_miss_values

    def getInfo(self):
        return (f"Name: {self.name}, Minimum: {self.minimum}, Maximum: {self.maximum}, Mean: {self.mean}, Tenth_percentile: {self.tenth_percentile}, Ninetieth_percentile: {self.ninetieth_percentile}, Per_miss_values: {self.per_miss_values}")

class File():
    def __init__(self, id, rows, columns, column_info):
        self.id = id
        self.rows = rows
        self.columns = columns
        self.column_info = column_info

    #def get_dict(self):
        #return (f"id: {self.id}, rows: {self.rows}, columns: {self.columns}, column info: {self.column_info}")

def readCSV(file_path = FILE_PATH):
    df = pd.read_csv(file_path, on_bad_lines="skip")
    columns = []
    for col in df:
        column = df[col]
        percentage_missing = (column.isnull().sum() * 100 / len(column)).round(0)
        if (column.dtype == np.float64 or column.dtype == np.int64):
            median = column.median()
            column.fillna(median, inplace=True)
            new_col = ColumnInfo(name= col, minimum= column.min(), maximum= column.max(),
            mean= column.mean(skipna=True), tenth_percentile= column.quantile(0.1),
            ninetieth_percentile= column.quantile(0.9), per_miss_values= percentage_missing)
        else:
            new_col = ColumnInfo(name= col, minimum= "non numeric values", maximum= "non numeric values", mean= "non numeric values", 
            tenth_percentile= "non numeric values", ninetieth_percentile= "non numeric values", per_miss_values= percentage_missing)
        columns.append(new_col.getInfo())
    new_file = File(id= 1, rows= len(df), columns= len(df.columns), column_info= columns)
    data.append(new_file)

readCSV()

@app.route('/')
def index():
    return "Possible endpoints are: /files, /id, /rows, /columns, /columnInfo."

@app.route('/files', methods= ['GET'])
def get_files():
    output = []
    for file in data:
        file_data = (f"id: {file.id}, number of rows: {file.rows}, number of columns: {file.columns}, columns info: {file.column_info}")
        output.append(file_data)
    return {"files": output}

@app.route('/id', methods=['GET'])
def get_id():
    file = data[0]
    return {"id": file.id}

@app.route('/rows', methods=['GET'])
def get_rows():
    file = data[0]
    return {'number of rows': file.rows}

@app.route('/columns', methods = ['GET'])
def get_columns():
    file = data[0]
    return {'number of columns': file.columns}

@app.route('/columnInfo', methods = ['GET'])
def get_columnInfo():
    file = data[0]
    return {'information about the statistics of each column': file.column_info}