import typer
from typing import Tuple, Optional
import requests
from requests.exceptions import Timeout, HTTPError
import click_spinner
import sys

app = typer.Typer()

class TaxiSearch:
    """A simple wrapper for querying the BookingGo Taxi API
    
    TaxiSearch exposes methods which enable querying the BookingGo
    Taxi API, results can either be returned by stdout reporting
    or as JSON for use in conjunction with an API
    """

    def __init__(self, n_passengers):
        self.base_url = "https://techtest.rideways.com/"
        self.suppliers = ["dave", "eric", "jeff"]
        self.max_passengers = {
            "STANDARD": 4,
            "EXECUTIVE": 4,
            "LUXURY": 4,
            "PEOPLE_CARRIER": 6,
            "LUXURY_PEOPLE_CARRIER": 6,
            "MINIBUS": 16
        }
        self.n_passengers = n_passengers
        self.results = {}

    
    def car_suitable(self, car_type):
        return self.max_passengers[car_type] >= self.n_passengers

    # Filter response by removing un-suitable car types
    def filter_response(self, response): 
        data = response.json()["options"]
        filtered = [service for service in data if self.car_suitable(service["car_type"])]
        return filtered

    def update_results(self, response, supplier):
        for service in self.filter_response(response):
            car_type = service["car_type"]
            price = service["price"]
            # Checking if a service has already been recorded for the car_type
            service_present = (car_type in self.results.keys())
            # If a service is not available or the service is cheaper update the results
            if not(service_present) or self.results[car_type]["price"] > price:
                self.results[car_type] = {"supplier": supplier, "price": price}

    def fetch_results(self, request_params):
        for supplier in self.suppliers:
            with click_spinner.spinner():
                supplier = supplier.capitalize()
                typer.secho(f"Contacting {supplier}...", fg=typer.colors.CYAN)
                # Make a request to the supplier api (timeout after 2 seconds)
                try:
                    response = requests.get(self.base_url + supplier, params=request_params, timeout = 2)                
                    # If the request has been successful filter the response and find the cheapest service
                    if response.ok:
                        self.update_results(response, supplier) 
                    else:
                        typer.secho(f"{supplier} could not be reached", fg=typer.colors.YELLOW)
                except Timeout:
                    typer.secho(f"{supplier} could not be reached", fg=typer.colors.YELLOW)
                except Exception:
                    typer.secho(f"Connection error", fg=typer.colors.RED)

        return self.results

    def fetch_api_results(self, request_params):
        for supplier in self.suppliers:  
            supplier = supplier.capitalize()
            # Make a request to the supplier api (timeout after 2 seconds)
            try:
                response = requests.get(self.base_url + supplier, params=request_params, timeout = 2)                
                # If the request has been successful filter the response and find the cheapest service
                if response.ok:
                    self.update_results(response, supplier) 
            except Timeout:
                pass
        return self.results


def display_search_values(pickup, dropoff, n):
    typer.secho("----------- Searching -----------", fg=typer.colors.GREEN)
    typer.secho(f"Pickup: {pickup}", fg=typer.colors.BRIGHT_BLUE)
    typer.secho(f"Dropoff: {dropoff}", fg=typer.colors.BRIGHT_BLUE)
    if (n != 0): typer.secho(f"Number of passengers: {n}", fg=typer.colors.BRIGHT_BLUE)
    typer.secho("---------------------------------", fg=typer.colors.GREEN)

@app.command()
def search(pickup: Tuple[float, float], dropoff: Tuple[float, float], 
           n_passengers: int = typer.Argument(0), json: bool = False):
    # Build the request params from the pickup and dropoff locations
    request_params = {
        "pickup": pickup,
        "dropoff": dropoff
    }

    # Change the output depending on the json flag
    if(json):
        print(TaxiSearch(n_passengers).fetch_api_results(request_params))
    else:
        display_search_values(pickup, dropoff, n_passengers)
        results = TaxiSearch(n_passengers).fetch_results(request_params)
        typer.secho("-----------  Results  -----------", fg=typer.colors.GREEN)
        for car_type, service in results.items():
            supplier = service["supplier"]
            price = service["price"]
            typer.secho(f"{car_type} - {supplier} - {price} ", fg=typer.colors.BLUE)
        typer.secho("---------------------------------", fg=typer.colors.GREEN)

@app.command()
def display_apilist():
    print("Displaying API list")
    print(["dave", "eric", "jeff"])

if __name__ == "__main__":
    app()
