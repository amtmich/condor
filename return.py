import requests

class CondorLowFare:
    def __init__(self, origin, destination, outboundDate, numberOfFlightDays, currency="EUR", isOutbound=True):
        self.origin = origin
        self.destination = destination
        self.outboundDate = outboundDate
        self.numberOfFlightDays = numberOfFlightDays
        self.currency = currency
        self.isOutbound = isOutbound
        self.url = "https://www.condor.com/tca/rest/pl/vacancies/lowFareInformation"
        self.headers = {
            "sec-ch-ua": 'Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
            "Accept": "application/json, text/plain, */*",
            "Referer": "https://www.condor.com/pl",
            "sec-ch-ua-mobile": "?0",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            "sec-ch-ua-platform": 'Windows'
        }

    def get_low_fare_information(self):
        params = {
            "origin": self.origin,
            "destination": self.destination,
            "outboundDate": self.outboundDate,
            "numberOfFlightDays": self.numberOfFlightDays,
            "currency": self.currency,
            "isOutbound": str(self.isOutbound).lower()
        }
        response = requests.get(self.url, headers=self.headers, params=params)
        return response.json()

    def get_cheapest_flight_summary(self):
        data = self.get_low_fare_information()["data"]

        # Function to get the 5 cheapest flights from a list of flights
        def get_cheapest_flights(flights):
            return sorted(flights, key=lambda x: x["price"])[:5]

        # Get the cheapest flights from both sets
        cheapest_set_1 = get_cheapest_flights(data[0])
        cheapest_set_2 = get_cheapest_flights(data[1])

        # Get the cheapest flight from each set
        cheapest_flight_1 = cheapest_set_1[0]
        cheapest_flight_2 = cheapest_set_2[0]

        total_cheapest_price = cheapest_flight_1['price'] + cheapest_flight_2['price']

        return {
            "origin": self.origin,
            "destination": self.destination,
            "date_1": cheapest_flight_1['date'],
            "date_2": cheapest_flight_2['date'],
            "price_1": cheapest_flight_1['price'],
            "price_2": cheapest_flight_2['price'],
            "total_price": total_cheapest_price,
            "cheapest_set_1": cheapest_set_1,
            "cheapest_set_2": cheapest_set_2,
            "count_1": len(data[0]),
            "count_2": len(data[1])
        }

def format_price(price, currency="EUR"):
    return f"{price // 100}.{price % 100:02d} {currency}"

# Example usage:
if __name__ == "__main__":
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
        ('HAM', 'PUJ'),
        ('HAJ', 'PUJ'),
#        ('GWT', 'PUJ'),
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

    summaries = []

    for origin, destination in origin_destination_pairs:
        print(f"\nFetching data for Origin: {origin}, Destination: {destination}")
        condor = CondorLowFare(origin=origin, destination=destination, outboundDate="20240524", numberOfFlightDays=19)
        summary = condor.get_cheapest_flight_summary()
        summaries.append(summary)

        # Print the count of flights in each set
        print(f"\nCount of flights in the first set: {summary['count_1']}")
        print(f"Count of flights in the second set: {summary['count_2']}")

        # Print the 5 cheapest flights from the first set
        print("\nCheapest flights from the first set:")
        for flight in summary["cheapest_set_1"]:
            formatted_price = format_price(flight['price'])
            print(f"Date: {flight['date']}, Price: {formatted_price}, Compartment: {flight['compartment']}, Offer: {flight['offer']}")

        # Print the 5 cheapest flights from the second set
        print("\nCheapest flights from the second set:")
        for flight in summary["cheapest_set_2"]:
            formatted_price = format_price(flight['price'])
            print(f"Date: {flight['date']}, Price: {formatted_price}, Compartment: {flight['compartment']}, Offer: {flight['offer']}")

        print("\n" + "="*50 + "\n")

    # Sort summaries by total price
    summaries.sort(key=lambda x: x["total_price"])

    # Print sorted summaries
    print("\nSummary of the cheapest flights from both sets in ascending order of total price:")
    for summary in summaries:
        formatted_total_price = format_price(summary["total_price"])
        formatted_price_1 = format_price(summary["price_1"])
        formatted_price_2 = format_price(summary["price_2"])
        print(f"Origin: {summary['origin']}, Destination: {summary['destination']}, "
              f"Date from set 1: {summary['date_1']}, Price: {formatted_price_1}, "
              f"Date from set 2: {summary['date_2']}, Price: {formatted_price_2}, "
              f"Total Price: {formatted_total_price}")
