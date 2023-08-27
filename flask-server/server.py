import os
from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import pickle
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
import io
import base64
import matplotlib.pyplot as plt

from analysis import city, round, date, vertical

app = Flask(__name__)
CORS(app)

SECRET_KEY = base64.b64encode(os.urandom(32)).decode('utf-8')
app.config['SECRET_KEY'] = SECRET_KEY

model = pickle.load(open("model.pkl", "rb"))

@app.route("/submit", methods=['POST'])
def predict():
    data = request.get_json()
    a = int(data['cat_industry_group'])
    b = int(data['cat_country_code'])
    p = int(data['cat_funding_rounds'])
    c = int(data['cat_diff_funding_year'])
    d = int(data['cat_total_investment'])
    e = int(data['cat_venture'])
    f = int(data['cat_seed'])
    g = int(data['cat_debt_financing'])
    h = int(data['cat_angel'])
    i = int(data['cat_private_equity'])
    j = int(data['cat_round_A'])
    k = int(data['cat_round_B'])
    l = int(data['cat_round_C'])
    m = int(data['cat_round_D'])
    n = int(data['cat_round_E'])
    o = int(data['cat_round_F'])

    sample_data = {'cat_industry_group': a,
        'cat_country_code': b,
        'cat_funding_rounds': p,
        'cat_diff_funding_year': c,
        'cat_total_investment': d,
        'cat_venture': e,
        'cat_seed': f,
        'cat_debt_financing': g,
        'cat_angel': h,
        'cat_private_equity': i,
        'cat_round_A':  j,
        'cat_round_B': k,
        'cat_round_C':  l,
        'cat_round_D':  m,
        'cat_round_E': n,
        'cat_round_F':  o
       }
    sample = pd.DataFrame(sample_data, index=[0])

    prediction = model.predict(sample)

    if(d==0):#correlation matrix
        prediction_value = 0
    elif((e==3 and f==1 and g==1 and h==1 and i==1) and (d == 1 or d==2)):
        prediction_value = 2
    else:
        prediction_value = int(prediction[0])

    return jsonify({
        'prediction': prediction_value
    })

@app.route("/analyse", methods=['POST'])
def analyse():

    graphs = {}

    investor_name = request.json.get('investorName')

    city(investor=investor_name)
    img1 = io.BytesIO()
    plt.savefig(img1, format='png')
    img1.seek(0)
    graph_url1 = base64.b64encode(img1.getvalue()).decode()
    graphs['graph1'] = f'data:image/png;base64,{graph_url1}'

    round(investor=investor_name)
    img2 = io.BytesIO()
    plt.savefig(img2, format='png')
    img2.seek(0)
    graph_url2 = base64.b64encode(img2.getvalue()).decode()
    graphs['graph2'] = f'data:image/png;base64,{graph_url2}'

    date(investor=investor_name)
    img3 = io.BytesIO()
    plt.savefig(img3, format='png')
    img3.seek(0)
    graph_url3 = base64.b64encode(img3.getvalue()).decode()
    graphs['graph3'] = f'data:image/png;base64,{graph_url3}'

    vertical(investor=investor_name)
    img4 = io.BytesIO()
    plt.savefig(img4, format='png')
    img4.seek(0)
    graph_url4 = base64.b64encode(img4.getvalue()).decode()
    graphs['graph4'] = f'data:image/png;base64,{graph_url4}'

    return jsonify(graphs)

if __name__ == "__main__":
    app.run(debug=True)