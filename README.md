[![Python v3.8+](https://img.shields.io/badge/Python-v3.8%2B-blue)](https://www.python.org/downloads)
[![codecov](https://codecov.io/gh/GabrielMartinMoran/TFI_UNTREF-web_api/branch/master/graph/badge.svg?token=7Q49AKV8DW)](https://codecov.io/gh/GabrielMartinMoran/TFI_UNTREF-web_api)

# Trabajo Final Integrador - Ingeniería en Computación - UNTREF

## Prototipo de medidor de consumo eléctrico y de prendido / apagado de energía eléctrica en ambientes controlados

## Web API

### Setting up the project

1. Install python or configure a virtual environment in the computer.
2. Install python dependencies specified in `requirements.txt`:

```shell
pip install -r requirements.txt
```

### Running the code
1. Run the PostgreSQL database (docker and docker-compose are required):
```shell
docker-compose up -d postgres
```
1. Run the python script `run.py`. 

### Running the tests
1. Run the script `run_tests.sh`.

