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
    This function is to get the city code from the config file 
    and forms a url based on the code that can be used to fetch data 
    from Bureau of Meteorology.

    No argument need to pass any argument here as this function only reads on config.json file.
    If you want to add any city, please update the city_code list in config file.

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
    """
    This function is to get data from Bureau of Meteorology and parse it as json out application.
    URL to fetch data from BOM is passed as an argument.

    There is a User-Agent header sent with the request otherwise BOM returns Unauthorised Response

    """
    header = { 'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36 Edg/90.0.818.66'}
    result = requests.get(my_url, headers=header)
    data = result.text
    parsed = json.loads(data)
    return parsed

# Create route 
@prometheus_app.route('/metrics', methods=['GET'])
#Get data into Gauge and Histogram
def get_data():
    """
    This function get triggered whenever '/metrics' path is hit on this application's server.

    First, it clears the temprature frequency histogram buckets so that values doesn't get added
    up everytime the this function is called.

    Then, For every city provided in the config file the data is fetched and parsed into 'p'.

    Gauge - current_temprature:
    current_temprature is set as the first object of 'data' since the data coming from BOM is sorted
    based on the latest time.

    Histogram - temprature_frequency:
    temprature_frequency is observed by going through all the data objects in the parsed data fetched
    from BOM. Observed tempratures are placed in the following buckets.
    buckets=(-10.0, -5.0, 0.0, 5.0 , 10.0, 15.0, 20, 25, 30)
    All of these buckets are set as 'le' -> less or equal

    """

    # Have to clear the temprature_frequecy, otherwise it histogram keeps adding the value on every request made.
    temprature_frequency.clear()
    
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