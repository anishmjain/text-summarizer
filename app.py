import requests
from flask import Flask,render_template,url_for
from flask import request as req
from dotenv import load_dotenv
import os
api_token = os.getenv('API_TOKEN')

app = Flask(__name__)

load_dotenv()

host = os.getenv('FLASK_RUN_HOST', '127.0.0.1')
port = int(os.getenv('FLASK_RUN_PORT', 5000))




@app.route("/",methods=["GET","POST"])
def Index():
    return render_template("index.html")

@app.route("/Summarize",methods=["GET","POST"])
def Summarize():
    if req.method== "POST":
        API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
        headers = {"Authorization": "Bearer ${api_token}"}

        data=req.form["data"]

        maxL=int(req.form["maxL"])
        minL=maxL//4
        def query(payload):
            response = requests.post(API_URL, headers=headers, json=payload)
            return response.json()

        output = query({
            "inputs":data,
            "parameters":{"min_length":minL,"max_length":maxL},
        })[0]
        
        return render_template("index.html",result=output["summary_text"])
    else:
        return render_template("index.html")
    

if __name__ == '__main__':
    app.debug = True
    app.run(host=host, port=port)