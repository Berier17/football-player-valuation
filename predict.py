import pickle
from flask import Flask, request, jsonify

# 1. CONFIGURATION
model_file = 'model.bin'

# 2. LOAD THE MODEL
# meaningful error message if model.bin is missing
try:
    with open(model_file, 'rb') as f_in:
        # CRITICAL: We load the Tuple (dv, model)
        # This gives us the "Translator" (dv) and the "Brain" (model)
        dv, model = pickle.load(f_in)
except FileNotFoundError:
    print(f"Error: {model_file} not found. Run train.py first!")
    exit()

# 3. CREATE THE APP
app = Flask('player_valuation')

@app.route('/predict', methods=['POST'])
def predict():
    # Receive the player data as JSON
    player = request.get_json()
    
    # Transform: Turn "Arsenal" into numbers using the loaded Vectorizer
    X = dv.transform([player])
    
    # Predict: Get the price
    y_pred = model.predict(X)[0]
    
    # Return the result
    result = {
        'predicted_value_euros': float(y_pred),
        'message': f"Estimated Value: €{y_pred:,.0f}"
    }
    
    return jsonify(result)

if __name__ == "__main__":
    # Run the server on port 9696
    app.run(debug=True, host='0.0.0.0', port=9696)