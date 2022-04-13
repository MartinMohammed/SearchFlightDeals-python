from datetime import datetime, timedelta

from data_manager import DataManager
from flight_search import FlightSearch
from notification_manager import NotificationManager
from user_manager import UserManager


def compare_and_send():
    # if flight is not None than it is a FlightData Object else it is a flight_search Object
    # if flightData object we can access the flight data attributes like price
    if float(flight.price) < float(destination["lowestPrice"]):
        print(f"Low price alert! Only {flight.price}Euro to fly from "
              f"{flight.origin_city}-{flight.origin_airport} to {flight.destination_city}-"
              f"{flight.destination_airport}, from {flight.out_date} to {flight.return_date}.")
        # send email by notification_manager (message as parameter)
        # ----------------------- SEND TO ALL NEWSLETTER USER ----------------------- #
        # giving notification_manager user_list to send the messages
        notification_manager.user_list = user_manager.all_user
        notification_manager.send_email_to_all(
            message=f"Low price alert! Only {flight.price}Euro to fly from {flight.origin_city}-"
                    f"{flight.origin_airport} to {flight.destination_city}-{flight.destination_airport}, from "
                    f"{flight.out_date} to {flight.return_date}."
        )


user_manager = UserManager()
data_manager = DataManager()
sheet_data = data_manager.get_destination_data()
flight_search = FlightSearch()
notification_manager = NotificationManager()

# -------------------- GET USER DATA FOR NEWSLETTER [ADDING] (Cheap FLIGHTS) -------------------- #
print("Welcome to SouthPole Tux's Flight Club."
      "\nWe find the best flight deals and email you.")

user_first_name = input("What is your first name? ")
user_last_name = input("What is your last name? ")
user_email = input("What is your email? ").lower()
# adding user (dict) to object attribute  (where the class is "managing")
user_manager.new_user = {
    "firstName": user_first_name,
    "lastName": user_last_name,
    "email": user_email
}
user_manager.add_user()
print(f"{user_first_name} is in the club! ")

print("Connection closed abruptly")

# ----------------------- SEARCHING CHEAP FLIGHTS ----------------------- #
# FRA --> frankfurt airport
ORIGIN_CITY_IATA = "LON"

# if in sheet data the first dataset has an empty column at iataCode,
# but we're only looking in the first row --> vulnerable for error when sheet
# has got new entry without iata code
if sheet_data[0]["iataCode"] == "":
    # please fill all rows with the iata code of the city
    for row in sheet_data:
        # sheet data gets updated
        row["iataCode"] = flight_search.get_destination_code(row["city"])
    # the destination data (class attribute) of data_manager gets updated
    data_manager.destination_data = sheet_data
    # now update the google sheet
    data_manager.update_destination_codes()

tomorrow = datetime.now() + timedelta(days=1)
six_month_from_today = datetime.now() + timedelta(days=(6 * 30))

# ---------------- Find flight.price < desitnation.price  &  Send Flights ---------- #
# sheet_data = list of dictionaries (flights)
for destination in sheet_data:
    # for each destination we create a flight object
    # if there is no flight found it will return None value
    flight = flight_search.check_flights(
        # ----------------------------- CHANGEABLE PARAMETERS ----------------------------- #
        ORIGIN_CITY_IATA,
        # from the sheet
        destination["iataCode"],
        from_time=tomorrow,
        to_time=six_month_from_today,
        # maximal stopovers
    )
    # for each flight we call the price, but we can also have none value flights
    # continue means skip that loop and go further
    if flight is None:
        continue
    else:
        # if flight is not None than it is a FlightData Object else it is a flight_search Object
        # if flightData object we can access the flight data attributes like price
        if float(flight.price) < float(destination["lowestPrice"]):
            print(f"Low price alert! Only {flight.price}Euro to fly from "
                  f"{flight.origin_city}-{flight.origin_airport} to {flight.destination_city}-"
                  f"{flight.destination_airport}, from {flight.out_date} to {flight.return_date}.")
            # send email by notification_manager (message as parameter)
            # ----------------------- SEND TO ALL NEWSLETTER USER ----------------------- #
            # giving notification_manager user_list to send the messages
            notification_manager.user_list = user_manager.all_user
            if flight.stop_overs == 0:
                notification_manager.send_email_to_all(
                    message=f"Low price alert! Only {flight.price}Euro to fly from {flight.origin_city}-"
                            f"{flight.origin_airport} to {flight.destination_city}-{flight.destination_airport}, from "
                            f"{flight.out_date} to {flight.return_date}."
                            f"\nwith {flight.stop_overs} Stop overs"
                )
            else:
                message = f"Low price alert! Only {flight.price}Euro to fly from {flight.origin_city}-"
                f"{flight.origin_airport} to {flight.destination_city}-{flight.destination_airport}, from "
                f"{flight.out_date} to {flight.return_date}."
                f"\nwith {flight.stop_overs} Stop overs via "
                f"{flight.via_city}"
