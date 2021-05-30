from flask import Flask, Response
from prometheus_client import Histogram, generate_latest, Gauge
import requests
import json


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

# Get list of cities from the config file
def get_city_from_config():
    """
    
    """
    city_url = []
    with open('config.json') as config_file:
        cities = json.load(config_file)
        for city in cities["city_code"]:
            print(city)
            st=city.split(".")
            current_url='http://www.bom.gov.au/fwo/{}/{}.json'.format(st[0],city)
            city_url.append(current_url)
    return city_url


# Get json data from urls
def get_data_from_bom(my_url):
    header = { 'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36 Edg/90.0.818.66'}
    result = requests.get(my_url, headers=header)
    data = result.text
    parsed = json.loads(data)
    return parsed

# Create route 
@prometheus_app.route('/metrics', methods=['GET'])
#Get data into Gauge and Histogram
def get_data():

    # Work for every city in the list
    for url in get_city_from_config():

        # Get Parsed json data
        parsed = get_data_from_bom(url)

        # GAUGE
        # Get latest temprature for Gauge
        p = parsed['observations']['data'][0]
        current_temprature.labels(p['name']).set(p["air_temp"])

        # Histogram
        # Get all the temprature frequencies for Histogram
        for d in parsed['observations']['data']:
            temprature_frequency.labels((d["name"])).observe((d["air_temp"]))
    
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

############################# SERVER #################################
prometheus_app.run(host='0.0.0.0', port='8888')