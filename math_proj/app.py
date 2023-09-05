from flask import Flask, request, jsonify,render_template
from flask_cors import CORS
import algos.new_simplex as ns
import algos.gauss_elim as gau
import numpy as np


app = Flask(__name__)
#Set up Flask to bypass CORS at the front end:</strong>
cors = CORS(app)


def simplex_algo(data):
    #print("DATA: ",data[0],data[1],data[2])
    s = ns.main(data[0],data[1],data[2]) # type: ignore
    return s

def gauss_algo(data):
    s = gau.main(data)
    return s


@app.route('/simplex')
def simplex():  
    return render_template('simplex.html')

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/gauss')
def gauss():  
    return render_template('gauss.html')

@app.route('/simplex_solve', methods=["POST"])
def postSimplex():
    
    data = request.get_json()
    data = jsonify(data)
    res = simplex_algo(data.json)
   
    return res

@app.route('/gau_solve', methods=["POST"])
def postGauss():
    
    data = request.get_json()
    print(f'\n\ndata pass : {data}\n\n')
    l = len(data)
    for i in range(l):
        for j in range(l+1):
            data[i][j] = float(data[i][j])
    print(f'\n\ndata pass : {data}\n\n')
    
    res = gauss_algo(data)
    
   
    return res
    
#Run the app:
if __name__ == "__main__":
    app.run(debug=True)
    
