# Part 1

## Introduction
The console application for part one is developed using the Python CLI framework [Typer](https://typer.tiangolo.com/). Typer provides a quick way of building console applications with Python, eliminating alot of the boilerplate code needed to handle command line arguments. Following on from this if incorrect arguments are passed to the program suitable error messages are provided by default.

## Requirements

- Python - 3.6.*
- requests - 2.22.0 
- typer
- colorama
- click_spinner

The project dependencies can be found in the requirements.txt file and can be installed with pip using the following commands:

```
cd BookingGo-part1
pip install -r requirements.txt
```

Note: this requires python version >= 3.6

## Running the script
In order to search the BookingGo API the TaxiSearch CLI exposes a search command which takes 5 parameters, the parameters are *pickup_lat*, *pickup_lng*, *dropoff_lat*, *dropoff_lng* and *max_passengers*. In addition to this the empty flag (--) must be passed as an additional parameter to tell typer that arguments in the form `-x` should be treated as negative numbers and not flags. An example search command along with the output produced can be seen below. In addition to the base 5 paramaters the `--json` flag can be passed which converts the output into a json format, this will be interfaced with the REST API in part 2.

```
python TaxiSearch.py search -- 51.470020 -0.454295 51.507351 -0.127758 5
```

![Example output](res/p1-output.gif)

## Testing
The tests can be run using the following command:

```
python TaxiSearchTest.py
```

# Part 2

## Introduction

The REST API for part 2 is built using [Express](https://expressjs.com/) the [Node.js](https://nodejs.org/en/) web framework. The request params are parsed and passed to the `TaxiSearch.py` script with the `--json` flag enabled. The output of the script is then returned as the result. The `child_process` module allows direct execution of shell commands, this is potentially vulnerable to code injection attacks. In order to prevent such attacks all paramaters are parsed into floats using `parseFloat` which returns `NaN` for none float values. So for any potentially dangerous parameters an error is returned and no shell execution is performed.

## Requirements

- [Node.js](https://nodejs.org/en/)

## Installation

```
npm install
```

## Starting the server
```
node index.js
```

### Example call

http://localhost:3000/api/search/?pickup=45.5,46.8&dropoff=-45.3,45.2&n_passengers=4 


## Testing

In order to test the API I used the [jest](https://jestjs.io/) and [supertest](https://github.com/visionmedia/supertest) libraries

The tests can be run with the following command:

```
npm test
```