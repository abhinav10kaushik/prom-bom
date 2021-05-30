from flask import Flask, Response
from prometheus_client import Histogram, generate_latest, Gauge


########## Flask ###############
# Create an instance of flask for Prometheus application
prometheus_app = Flask(__name__)

# Text format
CONTENT_TYPE_LATEST = str('text/plain; version=0.0.4; charset=utf-8')


###### Prometheus Client #######
# Initialise GAUGE 
current_temprature = Gauge( 'current_temprature', 'Current Temparature of City', ['city'] , unit='Celcius')

# Initialise HISTOGRAM
temprature_frequency  = Histogram('temprature_frequency',  'Frequency of temprature occurance', ['city'] , buckets=(-10.0, -5.0, 0.0, 5.0 , 10.0, 15.0, 20, 25, 30) )



# Create route 
@prometheus_app.route('/metrics', methods=['GET'])
#Get data into Gauge and Histogram
def get_data():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

############################# SERVER #################################
prometheus_app.run(host='0.0.0.0', port='8888')