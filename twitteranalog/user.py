
class User:
    id = 0

    def __init__(self, user):
        self.id = user['id']
        self.username = user['username']
        self.username = user['first_name'] + user['last_name']
        self.email = user['email']

