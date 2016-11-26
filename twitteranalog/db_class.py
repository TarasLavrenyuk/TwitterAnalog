import sys
import MySQLdb as mydb
from pymongo import MongoClient
from datetime import datetime
from datetime import date
import re

def getTags(string):
    tags = []
    words = string.split()
    for word in words:
        print word
        if word[0] == '#':
            word = " ".join(re.findall("[a-zA-Z]+", word))
            tags.append(word)
    return tags

class SQL:
    host = 'localhost'
    db_user_name = 'root'
    password = '852456aaa'
    db_name = 'twitter'


    def isLogin(self, request):
        con = None

        print 'I am in Login class'
        user_id = 0
        try:
            con = mydb.connect( self.host, self.db_user_name, self.password, self.db_name);
            cur = con.cursor()
            cur.execute("""SELECT * FROM users""")
            users = cur.fetchall()
            print users
            for user in users:
                if str(user[1]) == str(request.POST["username"]) and str(user[2]) == str(request.POST["password"]):
                    print user
                    user_id = int(user[0])
        except mydb.Error, e:

            print "Error %d: %s" % (e.args[0],e.args[1])
            sys.exit(1)

        finally:
            if con:
                con.close()
        return user_id

    def canSignUp(self, request):
        con = None
        username = request.POST["username"]
        try:
            con = mydb.connect( self.host, self.db_user_name, self.password, self.db_name);
            cur = con.cursor()
            cur.execute("""SELECT user_name FROM users;""");
            users = cur.fetchall()
        except mydb.Error, e:
            print "Error %d: %s" % (e.args[0],e.args[1])
            sys.exit(1)
        finally:
            if con:
                con.close()
        for user in users:
            if username == user[0]:
                return False
        return True

    def signUp(self, request):
        if request.POST["password"] != request.POST["passwordr"]:
            return

        inserted_username = request.POST["username"]
        inserted_password = request.POST["password"]
        inserted_role = 'user'
        inserted_country = request.POST["country"]

        print inserted_username
        print inserted_password

        try:
            con = mydb.connect( self.host, self.db_user_name, self.password, self.db_name);
            cur = con.cursor()

            cur.execute("""INSERT INTO users(user_name, password, role, country) VALUES (%s, %s, %s, %s);""",
                        (inserted_username, inserted_password, inserted_role, inserted_country))
            con.commit()

        except mydb.Error, e:

            print "Error %d: %s" % (e.args[0],e.args[1])
            sys.exit(1)

        finally:
            if con:
                con.close()

    def getUsername(self, id):
        con = None
        try:
            con = mydb.connect( self.host, self.db_user_name, self.password, self.db_name);
            cur = con.cursor()
            cur.execute("""SELECT user_name FROM users WHERE id=%s;""", id);
            result = cur.fetchall()
        except mydb.Error, e:
            print "Error %d: %s" % (e.args[0],e.args[1])
            sys.exit(1)
        finally:
            if con:
                con.close()
        return result[0][0]

    def getUserContinent(self, id):
        con = None
        try:
            con = mydb.connect( self.host, self.db_user_name, self.password, self.db_name);
            cur = con.cursor()
            cur.execute("""SELECT continent.id FROM users JOIN countries ON users.country=countries.id JOIN continent ON countries.continent_id=continent.id WHERE users.id=%s;""", str(id));
            result = cur.fetchall()
        except mydb.Error, e:
            print "Error %d: %s" % (e.args[0],e.args[1])
            sys.exit(1)
        finally:
            if con:
                con.close()
        return int(result)

    def getUserCountry(self, id):
        con = None
        try:
            con = mydb.connect( self.host, self.db_user_name, self.password, self.db_name);
            cur = con.cursor()
            cur.execute("""SELECT countries.name FROM users JOIN countries ON users.country=countries.id WHERE users.id=%s;""", id);
            result = cur.fetchall()
        except mydb.Error, e:
            print "Error %d: %s" % (e.args[0],e.args[1])
            sys.exit(1)
        finally:
            if con:
                con.close()
        return result[0][0]

    def getCountries(self):
        con = None
        try:
            con = mydb.connect( self.host, self.db_user_name, self.password, self.db_name);
            cur = con.cursor()
            cur.execute("""SELECT id, name FROM countries""")
            countries = cur.fetchall()
        except mydb.Error, e:
            print "Error %d: %s" % (e.args[0],e.args[1])
            sys.exit(1)
        finally:
            if con:
                con.close()
        return countries

    def getContinents(self):
        con = None
        try:
            con = mydb.connect( self.host, self.db_user_name, self.password, self.db_name);
            cur = con.cursor()
            cur.execute("""SELECT id, name FROM continent""")
            continents = cur.fetchall()
        except mydb.Error, e:
            print "Error %d: %s" % (e.args[0],e.args[1])
            sys.exit(1)
        finally:
            if con:
                con.close()
        return continents

class Mongo:

    def get_user_info(self, username):
        client = MongoClient('localhost', 27017)
        db = client.twitter
        users = db.users
        for user in users.find():
            if user['username'] == username:
                return user

    def add_user(self, username, continent):
        client = MongoClient('localhost', 27017)
        db = client.twitter
        users = db.users
        users.insert_one({'username' : username, 'first_name' : '', 'last_name' : '','email' : '',
                          'photo' : '', 'info' : '', 'followers' : [], 'followings' : [], 'twits' : [],
                          'date_of_birthday' : '', 'continent' : continent})

    def update_profile(self, request, username):
        client = MongoClient('localhost', 27017)
        db = client.twitter
        users = db.users
        users.update({ 'username' : username }, {'$set':
                                             { 'first_name' : request.POST['firstName'] ,
                                               'last_name' : request.POST['lastName'],
                                               'email' : request.POST['email'],
                                               'info' : request.POST['info'],
                                               'date_of_birthday' : datetime.strptime(request.POST['birthday'], '%Y-%m-%d'),
                                               }})

    def add_twit(self, username, header, content, file):
        client = MongoClient('localhost', 27017)
        db = client.twitter
        users = db.users
        posted_date = datetime.strptime(str(date.today()), '%Y-%m-%d')
        tags = getTags(content)
        twit = {'header' : header,
                'content' : content,
                'posted_date' : posted_date,
                'liked' : [],
                'tags' : tags
                }
        users.update({ 'username' : username }, {'$push': { 'twits': twit}})
        pass

    def user_search(self, name):
        result = []
        client = MongoClient('localhost', 27017)
        db = client.twitter
        users = db.users
        for user in users.find({'first_name': re.compile(name, re.IGNORECASE)}):
            result.append(user)
        for user in users.find({'last_name': re.compile(name, re.IGNORECASE)}):
            if not self.isAlreadyInArray(user, result):
                result.append(user)
        return result

    def isAlreadyInArray(self, user, users):
        for current_user in users:
            if current_user['username'] == user['username']:
                return True
        return False