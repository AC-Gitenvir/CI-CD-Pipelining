from flask import Flask, jsonify, request

app = Flask(__name__)

# 1. Home route
@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Flask App!"})

# 2. Add two numbers
@app.route('/add', methods=['GET'])
def add():
    a = int(request.args.get('a', 0))
    b = int(request.args.get('b', 0))
    return jsonify({"result": a + b})

# 3. Greet a user
@app.route('/greet/<username>', methods=['GET'])
def greet(username):
    return jsonify({"message": f"Hello, {username}!"})

# 4. Check if number is even
@app.route('/iseven/<int:num>', methods=['GET'])
def is_even(num):
    return jsonify({"number": num, "is_even": num % 2 == 0})

if __name__ == "__main__":
    app.run(debug=True)