import requests

SHEETY_USERS_ENDPOINT = "SHEETY_ENDPOINT"


class UserManager:
    # a UserManager add the new user of newsletter to google spreadsheet
    def __init__(self):
        # it will get user from main.py
        self.new_user = None
        # to get all user and save them into self.all_user object attribute
        self.all_user = self.get_user_all_user()
        # it will get values from user input (first name, last name, email)

    def add_user(self):
        # it should only add user if he is not in all_user (spreadsheet)
        # for the post request
        all_user_email = [user_in_all["email"]
                          for user_in_all in self.all_user]
        # data for each user to add post into spreadsheet
        if self.new_user["email"] not in all_user_email:
            # post new user to user spreadsheet
            requests.post(
                url=SHEETY_USERS_ENDPOINT,
                json={
                    "user": self.new_user
                }
            )
        else:
            print("user is already in sheet! ")
        print(f"Added all users: Done")

    # this code will be executed when a new user is getting added
    def get_user_all_user(self):
        response = requests.get(url=SHEETY_USERS_ENDPOINT)
        data = response.json()["users"]
        # but data in {"users": ...} format
        return data
