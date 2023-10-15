# Authored by Cem Kaya & Baha Mert Ersoy  


import json
import requests as req
from flask_cors import CORS
from flask import Flask, render_template  
#from flask_sqlalchemy import SQLAlchemy
#from sqlalchemy import null


app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
  return render_template('index.html')


@app.route('/park1')
def park1():  
    # READ FROM DATABASE 
    retjs ={}   
    retjs["park1_palce1"] = True   # names are placehoders
    retjs["park1_palce2"] = False  # names are placehoders 
    return json.dumps(retjs)



#################################################
if __name__ == '__main__':  #python interpreter assigns "__main__" to the file you run
  
  app.run(debug=True)
  

