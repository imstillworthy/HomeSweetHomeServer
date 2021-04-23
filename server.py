from flask import Flask, request, jsonify
import util
from flask_pymongo import PyMongo
from flask_cors import CORS,cross_origin
app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb+srv://yash:yash1234@collab.g1ws0.mongodb.net/house?retryWrites=true&w=majority"
mongo = PyMongo(app)
CORS(app)

@app.route('/',methods=['GET','POST'])
@cross_origin()
def homeroute():
    response= jsonify({
        'name':'yash'
    })
    return response

@app.route('/sell',methods=['POST'])
@cross_origin()
def add_home():
    request_data = request.get_json()
    price=float(request_data['price'])
    total_sqft = float(request_data['sqft'])
    location = request_data['location']
    bhk = int(request_data['bhk'])
    desc=request_data['desc']
    mongo.db.home.insert_one({
        'location':location,
        'price':price,
        'bhk':bhk,
        'sqft':total_sqft,
        'desc':desc
    })
    return jsonify({'msg':'success'})


@app.route('/get_location_names', methods=['GET'])
@cross_origin()
def get_location_names():
    response = jsonify({
        'locations': util.get_location_names()  # Populate locations to the frontend
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/predict_home_price', methods=['POST','GET'])
@cross_origin()
def predict_home_price():
    request_data = request.get_json()
    print(request_data)
    total_sqft = float(request_data['sqft'])
    location = request_data['location']
    bhk = int(request_data['bhk'])
    bath = int(request_data['nobath'])
    # print(location,bhk,bath,total_sqft)
    response = jsonify({
        # populate the estimated price to the frontend
        'estimated_price': util.get_estimated_price(location, total_sqft, bhk, bath)
    })
    print(util.get_estimated_price(location, total_sqft, bhk, bath))
    # response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/getproperty', methods=['GET'])
@cross_origin()
def propertydetails():
    data = mongo.db.home.find()
    result = [{
        'location': home['location'],
        'price':home['price'],
        'bhk':home['bhk']} 
        for home in data]
    response = jsonify(result)
    # response.headers.add('Access-Control-Allow-Origin', '*')
    return response


if __name__ == "__main__":
    print("Starting Python Flask Server For Home Price Prediction...")
    util.load_saved_artifacts()
    app.run()