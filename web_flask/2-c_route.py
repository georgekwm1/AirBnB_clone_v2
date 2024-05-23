#!/usr/bin/python3

""" 
script that starts a Flask web application:
"""


from flask import Flask

app = Flask(__name__)

@app.route('/', strict_slashes=False)
def hello_hbnb():
    """
    Returns a string response for the root route
    """
    return "Hello HBNB!"

@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """
    Returns a string response for the hbnb route
    """
    return "HBNB"

@app.route('/c/<text>', strict_slashes=False)
def c_text(text):
    """
    Returns a string response for the c route
    """
    # Replace underscores with spaces
    text = text.replace('_', ' ')
    return f"C {text}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)