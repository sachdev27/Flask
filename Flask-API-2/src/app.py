from flask import Flask,render_template, request, redirect,jsonify


app = Flask(__name__)

@app.route("/")
def index():
    return jsonify({"message":"Hello World!"})



if __name__ == "__main__":
    app.run(debug=True)
    
    
# export FLASK_ENV=development
# export FLASK_APP=app
# Even if we dont use jsonify , In Flask Python Dict is directly mapped to JSON