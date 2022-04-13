import requests

from flight_data import FlightData

TEQUILA_ENDPOINT = "ENDPOINT"
TEQUILA_API_KEY = "API_KEY"
# About @TEQUILA Kiwi API
"""
What is tequliia api 
Kiwi Flights is a Czech online travel technology company, which was founded in 2012 by Oliver
Dlouhý and Jozef Képesi. The Kiwi Flight API also provides a fare aggregator, a metasearch
engine and airline ticket booking, and ground transportation.

The APIs you will have access to are the ones we use ourselves for our own business. We are successfully 
building one of the most comprehensive transportation content databases in the world. And we are
leveraging our powerful caching technology — guaranteeing the best possible compromise of search API 
comprehensiveness, scalability, speed, and accuracy you could find. 
"""


class FlightSearch:
    # if destination code of sheet is empty we will find
    def get_destination_code(self, city_name):
        location_endpoint = f"{TEQUILA_ENDPOINT}/locations/query"
        headers = {"apikey": TEQUILA_API_KEY}
        # query to get the particular IATA code of the city
        query = {"term": city_name, "location_types": "city"}
        response = requests.get(url=location_endpoint,
                                headers=headers, params=query)
        results = response.json()["locations"]
        # the iata code
        code = results[0]["code"]
        return code

    # giving some parameters - checking if in general there exist flight from A to B
    def check_flights(self, origin_city_code, destination_city_code, from_time, to_time):
        headers = {"apikey": TEQUILA_API_KEY}
        # ----------------------------- CHANGEABLE PARAMETERS ----------------------------- #
        query = {
            "fly_from": origin_city_code,
            "fly_to": destination_city_code,
            # strftime to format the dates to dd/mm/YY
            "date_from": from_time.strftime("%d/%m/%Y"),
            "date_to": to_time.strftime("%d/%m/%Y"),
            # how long stay minimum and maximal
            "nights_in_dst_from": 7,
            "nights_in_dst_to": 28,
            # --> round == switch for oneway/round flights search (only for flight pay)
            "flight_type": "round",
            # --> it returns the cheapest flights to every city covered by the to parameter
            "one_for_city": 1,
            # --> direct Flights
            "max_stopovers": 0,
            "curr": "EUR"
        }
        response = requests.get(
            url=f"{TEQUILA_ENDPOINT}/v2/search",
            headers=headers,
            params=query
        )
        try:
            # data is a list of dictionary, and we're checking if there are any flights
            # found for the destination each dic in list represents a flight to destination
            data = response.json()["data"][0]
        # if we did not found any flights we now search for flight with 1 maximal stopover
        except IndexError:
            # we code here we've found no flights (list is empty)
            # due international travel disruptions - pandemic
            print(f"No flights found for {destination_city_code}.")
            """
            Here is a big problem: When there is no flights found for destination_city_code 
            the flight object will be None. So when we later want to access the attribute variables of flight search 
            we cannot 
            """
            query["max_stopovers"] = 1
            response2 = requests.get(
                url=f"{TEQUILA_ENDPOINT}/v2/search",
                headers=headers,
                params=query
            )
            try:
                # look if there are any flights in response 2
                data2 = response2.json()["data"][0]
            except IndexError:
                # we code here we've found no flights (list is empty)
                # due international travel disruptions - pandemic
                print(f"no alternatives for {destination_city_code}")
                return None
            # found alternative flight with one stopover
            else:
                print(f"found alternative for {destination_city_code}: ")
                flight_data2 = FlightData(
                    price=data2["price"],
                    # information about the flight route
                    origin_city=data2["route"][0]["cityFrom"],
                    origin_airport=data2["route"][0]["flyFrom"],
                    destination_city=data2["route"][0]["cityTo"],
                    destination_airport=data2["route"][0]["flyTo"],
                    # split because the time is in a weird format (T22 == o clock)
                    # [0] --> local departure from FRA [1] --> local departure from dest airport
                    out_date=data2["route"][0]["local_departure"].split("T")[
                        0],
                    return_date=data2["route"][1]["local_departure"].split("T")[
                        0],
                    stop_overs=1,
                    # it is the stop city
                    via_city=data2["route"][0]["cityTo"]
                )
                print(
                    f"{flight_data2.destination_city}: {flight_data2.price}Euro via {flight_data2.via_city}")
                return flight_data2
        else:
            # when everything worked create FlightData object (passing attributes)
            flight_data1 = FlightData(
                price=data["price"],
                # information about the flight route
                origin_city=data["route"][0]["cityFrom"],
                origin_airport=data["route"][0]["flyFrom"],
                destination_city=data["route"][0]["cityTo"],
                destination_airport=data["route"][0]["flyTo"],
                # split because the time is in a weird format (T22 == o clock)
                # [0] --> local departure from FRA [1] --> local departure from dest airport
                out_date=data["route"][0]["local_departure"].split("T")[0],
                return_date=data["route"][1]["local_departure"].split("T")[0]
                # stop_overs=[]
            )
            # it will only be printed when there is a flight found for destination city code
            print(f"{flight_data1.destination_city}: {flight_data1.price}Euro")
            # return flight_data foreach destination in sheet data
            return flight_data1
