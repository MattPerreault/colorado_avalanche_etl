# WIP: Colorado Avalanche Data Processing Framework


## Goal
The goal of this project is to create a data processing framework to populate a PostgreSQL DB that powers an analytics dashboard for the Colorado Avalanche. Go AVS!


**Note** This project is powered by a free NHL API. See [this gitlab repo for API documentation](https://gitlab.com/dword4/nhlapi) Shout out to [@dw0rd4](https://twitter.com/dw0rd4)
You can also visit the [OpenAPI3.0](https://swagger.io/docs/specification/about/) spec at this [git hub repo](https://github.com/erunion/sport-api-specifications/tree/master/nhl) maintained by

### Copyright
 > *NHL and the NHL Shield are registered trademarks of the National Hockey League. NHL and NHL team marks are the property of the NHL and its teams. © NHL 2021. All Rights Reserved.*

## Setup

0. Install python3.9
1. Create a python virtualenv
2. Install requirements:

```sh
From project root
make -C deps 
```
## Run Command
From /src
```sh
$ python Executor.py
```

## Project Structure
```
colroado_avalanche_etl
├── src/
    ├── configuration/
        └── config files.
    ├── extract/
        └── All python data source extract code.
    ├── test/
        └── All unit tests.
    └── Runner.py
             
``` 

## Test
Run individual unit test from test/
```sh
$ python <TEST_FILE>.py
```