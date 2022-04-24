### FILE STATISTICS REST API

## Aim of the project
The aim of this project is to output statistics of an input file. 

Those statistics are:
* number of columns
* number of rows
* minimum, maximum, mean, 10th percentile, 90th percentile (of each column)
* % of missing values in each column

## Technologies
Project is using:
* Flask (flask, app)
* Pandas library
* Numpy library

## Setup
To run this project, save the "app.py" file and run it using command line (after creating virtual environment):
  $ flask run  
Then you will be asked to input a csv file, so input a filepath of a file you want the app to analyze.
  $ C:\Users\Alicja\Desktop\Nauka\deepsense\api\titanic.csv

## After running the project
The output of a setup is a web address, you can access each statistics by using different endpoints:
* '/files' - full information about the statistics of a file
* '/id' - id of a file
* '/columns' - number of columns
* '/rows' - number of rows
* '/columnInfo' - information about every column of a file (its name, minimum and maximum value, mean, 10th and 90th percentile and percentage of missing values)

## State of the project
Since it was my first time writing a REST API, it probably needs some improvements. I will work on them as my knowledge progresses.
