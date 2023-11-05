from flask import Flask, request, jsonify
from infer import get_inference


app = Flask(__name__)

# Dummy user data (replace with your user database or authentication logic)
users = {
    'user1': 'password1',
    'user2': 'password2',
}

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if username in users and users[username] == password:
        return jsonify({'message': 'Login successful'})
    else:
        return jsonify({'message': 'Login failed'}, 401)

@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    print(data)
    username = data.get("username")
    email = data.get("email")  # Retrieve the "email" field from the JSON data
    password = data.get("password")
    
    if username in users:
        return jsonify({'message': 'Username already exists'}, 400)
    else:
        users[username] = {'password': password, 'email': email}  # Store username, password, and email
        return jsonify({'message': 'Sign-up successful'})

    

@app.route('/logout', methods=['POST'])
def logout():
    # Implement your logout logic here (e.g., token or session invalidation)
    return jsonify({'message': 'Logout successful'})

@app.route('/predict', methods=['POST'])
def predict():
    # Retrieve input data from the request
    data = request.get_json()
    day = data['day']
    people = data['people']

    # Call the inference function to get predictions
    predictions = get_inference(day, people)

    # Create a response dictionary
    response = {'predictions': predictions}

    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True)
