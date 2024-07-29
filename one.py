import requests
from datetime import datetime, timedelta


class FlightPriceFetcher:
    def __init__(self, origin_destination_pairs, flights_per_pair=5, overall_flights=20):
        self.origin_destination_pairs = origin_destination_pairs
        self.flights_per_pair = flights_per_pair
        self.overall_flights = overall_flights
        self.all_prices = []

    def fetch_low_fare_information(self, origin, destination):
         # Calculate the next day's date
        next_day = datetime.now() + timedelta(days=1)
        outbound_date = next_day.strftime("%Y%m%d")  # Format the date as YYYYMMDD

        url = "https://www.condor.com/tca/rest/pl/vacancies/lowFareInformation"
        params = {
            'origin': origin,
            'destination': destination,
            'outboundDate': outbound_date,
            'numberOfFlightDays': '31',
            'currency': 'EUR',
            'oneway': 'true',
            'adults': '1',
            'isOutbound': 'true'
        }
        headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'en-US,en;q=0.9',
            # Include other necessary headers from your curl request
        }
        
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to fetch data for {origin} to {destination}")
            return None

    def print_lowest_prices_for_pair(self, origin, destination, flights):
        print(f"{self.flights_per_pair} lowest prices for {origin} to {destination}:")
        for flight in flights[:self.flights_per_pair]:
            print(f"Date: {flight['date']}, Price: {flight['price']/100:.2f} EUR")

    def fetch_and_print_all(self):
        for origin, destination in self.origin_destination_pairs:
            result = self.fetch_low_fare_information(origin, destination)
            if result and 'data' in result and len(result['data']) > 0:
                flights = [flight for sublist in result['data'] for flight in sublist]
                sorted_flights = sorted(flights, key=lambda x: x['price'])
                self.print_lowest_prices_for_pair(origin, destination, sorted_flights)
                
                # Extend each flight info with origin and destination before adding to all_prices
                for flight in sorted_flights[:self.flights_per_pair]:
                    flight['origin'] = origin
                    flight['destination'] = destination
                    self.all_prices.append(flight)
        
        # Print overall lowest prices from all requests
        self.print_overall_lowest_prices()

    def print_overall_lowest_prices(self):
        all_prices_sorted = sorted(self.all_prices, key=lambda x: x['price'])
        print(f"\n{self.overall_flights} overall lowest prices from all requests:")
        for flight in all_prices_sorted[:self.overall_flights]:
            print(f"Origin: {flight['origin']}, Destination: {flight['destination']}, Date: {flight['date']}, Price: {flight['price']/100:.2f} EUR")



origin_destination_pairs = [
    ('WRO', 'PUJ'),
    ('WAW', 'PUJ'),
    ('GDN', 'PUJ'),
    ('KRK', 'PUJ'),
    ('POZ', 'PUJ'),
    ('KTW', 'PUJ'),
    ('FRA', 'PUJ'),
    ('BER', 'PUJ'),
    ('MUC', 'PUJ'),
    ('LUX', 'PUJ'),
    ('PRG', 'PUJ'),
    ('DRS', 'PUJ'),
    ('LEJ', 'PUJ'),
#    ('BRE', 'PUJ'),
    ('HAM', 'PUJ'),
    ('HAJ', 'PUJ'),
    ('GWT', 'PUJ'),
    ('NUE', 'PUJ'),
    ('STR', 'PUJ'),
    ('ZRH', 'PUJ'),
    ('DUS', 'PUJ'),
    ('FMO', 'PUJ'),
    ('VNO', 'PUJ'),
    ('GRZ', 'PUJ'),
    ('INN', 'PUJ'),
    ('SZG', 'PUJ'),
    ('VIE', 'PUJ'),
    ('BUD', 'PUJ'),
    ('BSL', 'PUJ')
]

fetcher = FlightPriceFetcher(origin_destination_pairs)
fetcher.fetch_and_print_all()


origin_destination_pairs = [
    ('PUJ','WRO'), 
    ('PUJ','WAW'), 
    ('PUJ','GDN'), 
    ('PUJ','KRK'), 
    ('PUJ','POZ'), 
    ('PUJ','KTW'),
    ('PUJ','FRA'),
    ('PUJ','BER'),
    ('PUJ','MUC'),
    ('PUJ','LUX'),
    ('PUJ','PRG'),
    ('PUJ','DRS'),
    ('PUJ','LEJ'),
    ('PUJ','BRE'),
    ('PUJ','HAM'),
    ('PUJ','HAJ'),
    ('PUJ','GWT'),
    ('PUJ','NUE'),
    ('PUJ','STR'),
    ('PUJ','ZRH'),
    ('PUJ','DUS'),
    ('PUJ','FMO'),
    ('PUJ','VNO'),
    ('PUJ','GRZ'),
    ('PUJ','INN'),
    ('PUJ','SZG'),
    ('PUJ','VIE'),
    ('PUJ','BUD'),
    ('PUJ','BSL')
]

fetcher = FlightPriceFetcher(origin_destination_pairs)
fetcher.fetch_and_print_all()

origin_destination_pairs = [
    ('CLO','WRO'), 
    ('CLO','WAW'), 
    ('CLO','GDN'), 
    ('CLO','KRK'), 
    ('CLO','POZ'), 
    ('CLO','KTW')
]

fetcher = FlightPriceFetcher(origin_destination_pairs)
#fetcher.fetch_and_print_all()

origin_destination_pairs = [
    ('BOG','WRO'), 
    ('BOG','WAW'), 
    ('BOG','GDN'), 
    ('BOG','KRK'), 
    ('BOG','POZ'), 
    ('BOG','KTW')
]

fetcher = FlightPriceFetcher(origin_destination_pairs)
#fetcher.fetch_and_print_all()
