from datetime import date


class User:
    id = 0
    password = ""
    country = ""
    birthday = date
    email = ""
    first_name = ""
    last_name = ""
    info = ""
    username = ""
    twits = []
    followings = []
    followers = []


    def __init__(self, user):
        self.username = user['username']
        self.password = user['password']
        self.email = user['email']
        self.first_name = user['first_name']
        self.last_name =  user['last_name']

