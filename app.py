from flask import Flask, app
from flask_restful import Api
import numpy as np
import pandas as pd

app = Flask(__name__)
api = Api(app)

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
        return (f"Name: {str(self.name)}, Minimum: {str(self.minimum)}, Maximum: {str(self.maximum)}, Mean: {str(self.mean)}, Tenth_percentile: {str(self.tenth_percentile)}, Ninetieth_percentile: {str(self.ninetieth_percentile)}, Per_miss_values: {str(self.per_miss_values)}")

class File():
    def __init__(self, id, rows, columns, column_info, column_list):
        self.id = id
        self.rows = rows
        self.columns = columns
        self.column_info = column_info
        self.column_list = column_list


def readCSV(file_path = FILE_PATH):
    df = pd.read_csv(file_path, on_bad_lines="skip")
    columns = []
    columns_list = []
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
        columns_list.append(new_col)
    new_file = File(id= 1, rows= len(df), columns= len(df.columns), column_info= columns, column_list = columns_list)
    data.append(new_file)

readCSV()

@app.route('/')
def index():
    return {"Getting all information about a file": '/files',
            "Getting id of a file": '/id',
            "Getting information about the number of columns": '/columns',
            "Getting information about the number of rows": '/rows',
            "Getting information about all of the columns": '/columnInfo',
            "Getting information about the column with a certain ID": '/columnInfo/{ID}'}

@app.route('/files', methods= ['GET'])
def get_files():
    file = data[0]
    return {"id": file.id, "number of rows": file.rows, "number of columns": file.columns, "columns info": file.column_info}

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

@app.route('/columnInfo/<ID>', methods = ['GET'])
def get_columnInfoID(ID):
    if int(ID) > data[0].columns or int(ID)==0:
        return {f'Information about the statistics of the {ID}. column' : 'No such column.'}
    else:
        id = int(ID) -1
        return {f'information about the statistics of the {ID}. column': data[0].column_info[id]}

@app.route('/columnInfo/<ID>/<statistics>', methods = ['GET'])
def get_statistics(ID, statistics):
    if int(ID) > data[0].columns or int(ID)==0:
        return {f'Information about the {statistics} of the {ID}. column' : 'No such column.'}
    elif statistics not in ["minimum", "maximum", "mean", "10th", "90th", "%missing"]:
        return {f'Information about the {statistics} of the {ID}. column' : 'No such statistics.'}
    else:
        id = int(ID) -1
        if statistics == "mean":
            return {f'information about the {statistics} of the {ID}. column': data[0].column_list[id].mean}
        if statistics == "minimum":
            return {f'information about the {statistics} of the {ID}. column': str(data[0].column_list[id].minimum)}
        if statistics == "maximum":
            return {f'information about the {statistics} of the {ID}. column': str(data[0].column_list[id].maximum)}
        if statistics == "10th":
            return {f'information about the {statistics} of the {ID}. column': data[0].column_list[id].tenth_percentile}
        if statistics == "90th":
            return {f'information about the {statistics} of the {ID}. column': data[0].column_list[id].ninetieth_percentile}
        if statistics == "%missing":
            return {f'information about the {statistics} of the {ID}. column': data[0].column_list[id].per_miss_values}

if __name__ == "__main__":
    app.run(debug=True)