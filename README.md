# Prom-bom
Temperature metric reporter for Prometheus

This application reports following

```
Endpoint - /metric

Gauge : current_temperature_Celcius
(Current temperature of city with units in Celcius)

Histogram : temperature_frequency_bucket
buckets=(-10.0, -5.0, 0.0, 5.0 , 10.0, 15.0, 20, 25, 30)
(Frequency of occurance of temperature in above buckets)

```

_____________

This application is created on `Python 3.8.5`

Packages and their versions used are specified in the requirements.txt file. 

These packages can be installed by using folloing pip command

```
pip install -r requirement.txt
```

### Config file:

Please append the config file with city code from BOM like in below example format.

```
    {
        "city_code": [
         "IDT60701.95967" , <Some-other-city-code>
        ]
    }
```
____

## Run

1.  Python metric server

If all packages in requirements.txt have been installed properly.
Following command should start a flask development server.

```
python3 app.py
```
Above server will will tell what url and port it is running on.



2.  Prometheus container

If you want to test these metrics on Prometheus docker container, Updated above url into the prometheus.yml file.
and launch prometheus docker with following command

```
docker run -p 9090:9090 -v $PWD/prometheus.yml:/etc/prometheus/prometheus.yml prom/prometheus
```