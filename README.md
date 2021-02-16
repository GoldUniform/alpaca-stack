# AlpacaStack

AlpacaStack is an open source, docker-compose based stack of resources that interact with the Alpaca Trading API. Prometheus stores real time metric data, Grafana dashboards visualize the data, and MySQL is used to store asset and sector information.

The custom metrics exporters are written in Python.

<img width="1006" alt="screenshot" src="https://raw.githubusercontent.com/GoldUniform/alpaca-stack/master/screenshot.png">

## Launching

Rename `config_sample.yml` to `config.yml` and add your Alpaca API keys. Once you have done that, running the stack is as easy as `$ docker-compose up -d`

## Services

- [Prometheus](http://localhost:9090)
- [Grafana](http://localhost:3000)
- [AlertManager](http://localhost:9093)
- MySQL
- Account Exporter
- Position Exporter

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details