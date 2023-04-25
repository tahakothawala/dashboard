from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import pandas as pd
import json
import numpy as np

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": ["http://127.0.0.1:5500"]}})

dataset = "C:/Users/tkothawala/Documents/FinalProject/heart_disease_cleaned.csv"
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

@app.route("/heatmap") 
def getHeatMapData():
    varx = request.args['varX']
    vary = request.args['varY']
    varz = request.args['varZ']

    df = df_global    
    dict = {}
    
    for i in df.index:
        key_str = df[varx][i] + ":" + df[vary][i]
        if key_str in dict:
            dict[key_str] += df[varz][i]
        else:
            dict[key_str] = df[varz][i]
        
    print(dict)
    values_json = {"x_axis": varx, "y_axis": vary, "data":[]}
    for key, value in dict.items():
        keys = key.split(':')
        print(keys)
        values_json['data'].append({"group": keys[0], "variable": keys[1], "value": value})
    
    json_data = json.dumps(values_json, default=np_encoder)
    print(json_data)
    return json_data