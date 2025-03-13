from flask import Flask, request, jsonify, render_template
import pickle
import numpy as np

# Load the trained model
with open("fish_species_classifier.pkl", "rb") as model_file:
    model = pickle.load(model_file)

# Define species mapping
species_mapping = {0: "Perch", 1: "Parkki", 2: "Bream", 3: "Roach", 4: "Pike", 5: "Smelt", 6: "Whitefish"}

# Flask App
app = Flask(__name__, template_folder="Ttemplates")

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        features = np.array([[data['Weight'], data['Length1'], data['Length2'], data['Length3'], data['Height'], data['Width']]])
        
        prediction = model.predict(features)
        probabilities = model.predict_proba(features)

        species_name = species_mapping[int(prediction[0])]
        confidence = round(np.max(probabilities) * 100, 2)

        return jsonify({"Predicted Species": species_name, "Confidence": confidence})
    
    except Exception as e:
        return jsonify({"Error": str(e)})

if __name__ == '__main__':
    app.run(debug=True)