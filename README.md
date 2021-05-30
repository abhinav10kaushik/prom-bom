# prom-bom
Temperature metric reporter for Prometheus

Run Prometheus with this BOM metrics endpoint

```
docker run -p 9090:9090 -v $PWD/prometheus.yml:/etc/prometheus/prometheus.yml prom/prometheus
```