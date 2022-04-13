import smtplib

# sending account
MY_EMAIL = "EMAIL_ACCOUNT"
PASSWORD = "PASSWORD_EMAIL_ACCOUNT"
GMAIL_HOST_URL = "smtp.gmail.com"


class NotificationManager:
    # as parameter --> flight data object of the flight
    def __init__(self):
        # for now, it will stay empty, but it will get assigned vlaue from
        # user manager get all user return
        # each user in a dict
        self.user_list = []

    def send_email_to_all(self, message):
        for user in self.user_list:
            with smtplib.SMTP(GMAIL_HOST_URL) as connection:
                connection.starttls()
                connection.login(user=MY_EMAIL, password=PASSWORD)
                connection.sendmail(
                    from_addr=MY_EMAIL,
                    to_addrs=user["email"],
                    msg=message
                )
        print("Send Mail to everyone: Done")
