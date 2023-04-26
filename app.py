from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import pandas as pd
import json
import numpy as np

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": ["http://127.0.0.1:5500"]}})

dataset = "C:/Users/ripatil/Desktop/dashboard-main/dashboard-main/heart_disease_cleaned.csv"
df_global = pd.read_csv(dataset)


@app.route("/barchart") 
def getBarChartData():
    varx = request.args['varX']
    vary = request.args['varY']
    
    df = pd.concat([df_global[varx], df_global[vary]], axis=1)
    df = df.reset_index()
    df_global.reset_index()

    dict = {}
    for i in df.index:
        if df[varx][i] in dict:
            dict[df[varx][i]] += df[vary][i]
        else:
            dict[df[varx][i]] = df[vary][i]
    
    values_json = {"x_axis": varx, "y_axis": vary, "data":[]}
    for key, value in dict.items():
        values_json['data'].append({"x_axis": key, "y_axis": value})
    json_data = json.dumps(values_json, default=np_encoder)
    return json_data
   
def np_encoder(object):
    if isinstance(object, np.generic):
        return object.item()
    
def binningAge(age):
    return int(age/5) - 5

def binningBMI(BMI):
    return int(BMI/5) - 2

@app.route("/heatmap") 
def getHeatMapData():
    varx = request.args['varX']
    vary = request.args['varY']
    varz = request.args['varZ']

    df = df_global    
    dict = {}
    
    for i in df.index:
        key_str = str(binningBMI(df[varx][i])) + ":" + str(binningAge(df[vary][i]))
        if key_str in dict:
            dict[key_str] += df[varz][i]
        else:
            dict[key_str] = df[varz][i]
        
    values_json = {"x_axis": varx, "y_axis": vary, "data":[]}
    for key, value in dict.items():
        keys = key.split(':')
        values_json['data'].append({"group": keys[0], "variable": keys[1], "value": value})
    
    json_data = json.dumps(values_json, default=np_encoder)
    return json_data


@app.route("/piechart") 
def getPieChartData():
    varx = request.args['varX']
    vary = request.args['varY']
    df_global.reset_index()
    df = pd.concat([df_global[varx], df_global[vary]], axis=1)
    df = df.reset_index()
    df_global.reset_index()

    dict = {}
    for i in df.index:
        if df[varx][i] in dict:
            dict[df[varx][i]] += df[vary][i]
        else:
            dict[df[varx][i]] = df[vary][i]
    
    values_json = {"x_axis": varx, "y_axis": vary, "data":[]}
    for key, value in dict.items():
        values_json['data'].append({key :value})
    json_data = json.dumps(values_json, default=np_encoder)
    return json_data

@app.route("/pcp") 
def getPCPData():

    cols = ["Age","CigsPerDay","Total Cholestrol","Systolic BP","Diastolic BP","BMI","Heart Rate","Glucose", "Education"]
    df_global.reset_index()
    df = df_global
    
    values_json = {"cols": cols, "data":[]}
    for i in df.index:
        dict = {}
        for attribute in cols:
            dict[attribute] = df[attribute][i]
        values_json['data'].append(dict)
    json_data = json.dumps(values_json, default=np_encoder)
    return json_data


@app.route("/radarchart") 
def getRadarChartData():
    cols = ["Age","CigsPerDay","Total Cholestrol","Systolic BP","Diastolic BP","BMI","Heart Rate","Glucose"]
    df_global.reset_index()
    df = df_global
    values_json = []
    for i in range(10):
        value = []
        for attribute in cols:
            # dict.append({"axis": attribute, "value":df[attribute][i]})
            dict = {}
            dict['axis'] = attribute
            dict['value'] = df[attribute][i]
            value.append(dict)
        values_json.append(value)
    json_data = json.dumps(values_json, default=np_encoder)
    return json_data


@app.route("/scatterplot") 
def getScatterPlotData():
    varx = request.args['varX']
    vary = request.args['varY']
    varz = request.args['varZ']
    df_global.reset_index()
    df = df_global    
    dict = {}
    
    for i in df.index:
        key_str = df[varx][i].astype(str) + ":" + df[vary][i].astype(str)
        if key_str in dict:
            dict[key_str] += df[varz][i]
        else:
            dict[key_str] = df[varz][i]
        
    values_json = {"x_axis": varx, "y_axis": vary, "data":[]}
    for key, value in dict.items():
        keys = key.split(':')
        values_json['data'].append({"x_axis": keys[0], "y_axis": keys[1], "Heart Stroke": value})

    json_data = json.dumps(values_json, default=np_encoder)
    return json_data