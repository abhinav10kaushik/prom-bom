from flask import Flask

# Create an instance of flask for Prometheus application
app = Flask(__name__)

@app.route('/a')
def get_data():
    return "Prometheus App"

app.run(host='0.0.0.0', port='8888')