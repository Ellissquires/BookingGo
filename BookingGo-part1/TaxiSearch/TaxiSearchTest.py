import unittest
from TaxiSearch import TaxiSearch
from requests.models import Response
from unittest.mock import Mock

class TaxiSearchTest(unittest.TestCase):
    
    def test_update_results(self):
        """
        Test that the results are sucessfully updated when a service becomes
        available
        """

        max_passengers = 5
        search = TaxiSearch(max_passengers)

        response = Mock(spec=Response)
        response.json.return_value = {
            "supplier_id": "ERIC",
            "pickup": "51.470020,-0.454295",
            "dropoff": "51.00000,1.0000",
            "options": [
                { "car_type": "STANDARD",
                  "price": 671808 },
                { "car_type": "MINIBUS",
                  "price": 10 }
            ]
        }
        
        search.update_results(response, "ERIC")
        expected = {'MINIBUS': {'price': 10, 'supplier': 'ERIC'}}
        self.assertEqual(search.results, expected)

    def test_update_results_with_cheapest(self):
        """
        Test that the results are sucessfully updated when a service with a cheaper
        price is found
        """

        max_passengers = 5
        search = TaxiSearch(max_passengers)

        search.results = {'MINIBUS': {'price': 11, 'supplier': 'DAVE'}}

        response = Mock(spec=Response)
        response.json.return_value = {
            "supplier_id": "ERIC",
            "pickup": "51.470020,-0.454295",
            "dropoff": "51.00000,1.0000",
            "options": [
                { "car_type": "STANDARD",
                  "price": 671808 },
                { "car_type": "MINIBUS",
                  "price": 10 }
            ]
        }
        
        search.update_results(response, "ERIC")
        expected = {'MINIBUS': {'price': 10, 'supplier': 'ERIC'}}
        self.assertEqual(search.results, expected)
    
    def test_filter_response(self):
        """
        Test that it filters a repsponse based on the max
        passenger number correctly
        """

        # Creating a mock response
        response = Mock(spec=Response)
        response.json.return_value = {
            "supplier_id": "DAVE",
            "pickup": "51.470020,-0.454295",
            "dropoff": "51.00000,1.0000",
            "options": [
                { "car_type": "STANDARD",
                  "price": 671808 },
                { "car_type": "EXECUTIVE",
                  "price": 375545 },
                { "car_type": "LUXURY",
                  "price": 583438 },
                { "car_type": "MINIBUS",
                  "price": 37456 },
            ]
        }

        max_passengers = 5
        result = TaxiSearch(max_passengers).filter_response(response)
        expected = [{'car_type': 'MINIBUS', 'price': 37456}]
        self.assertEqual(result, expected) 

if __name__ == '__main__':
    unittest.main()



