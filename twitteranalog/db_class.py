import sys
import MySQLdb as mydb
from pymongo import MongoClient
from datetime import datetime, timedelta
import re
import uuid
from operator import itemgetter
import redis
import pickle
from bson.code import Code
import user_generator

red = redis.StrictRedis(host='localhost', port=6379, db=0)


def getTags(string):
    tags = []
    words = string.split()
    for word in words:
        if word[0] == '#':
            word = " ".join(re.findall("[_a-zA-Z]+", word))
            tags.append(word)
    return tags


class SQL:
    host = 'localhost'
    db_user_name = 'root'
    password = '852456aaa'
    db_name = 'twitter'

    def isLogin(self, request):
        con = None

        user_id = 0
        try:
            con = mydb.connect(self.host, self.db_user_name, self.password, self.db_name);
            cur = con.cursor()
            cur.execute("""SELECT * FROM users""")
            users = cur.fetchall()
            for user in users:
                if str(user[1]) == str(request.POST["username"]) and str(user[2]) == str(request.POST["password"]):
                    user_id = int(user[0])
        except mydb.Error, e:

            print "Error %d: %s" % (e.args[0], e.args[1])
            sys.exit(1)

        finally:
            if con:
                con.close()
        return user_id

    def canSignUp(self, request):
        con = None
        username = request.POST["username"]
        try:
            con = mydb.connect(self.host, self.db_user_name, self.password, self.db_name);
            cur = con.cursor()
            cur.execute("""SELECT user_name FROM users;""");
            users = cur.fetchall()
        except mydb.Error, e:
            print "Error %d: %s" % (e.args[0], e.args[1])
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
            con = mydb.connect(self.host, self.db_user_name, self.password, self.db_name);
            cur = con.cursor()

            cur.execute("""INSERT INTO users(user_name, password, role, country) VALUES (%s, %s, %s, %s);""",
                        (inserted_username, inserted_password, inserted_role, inserted_country))
            con.commit()

        except mydb.Error, e:

            print "Error %d: %s" % (e.args[0], e.args[1])
            sys.exit(1)

        finally:
            if con:
                con.close()

    def getUsername(self, id):
        con = None
        try:
            con = mydb.connect(self.host, self.db_user_name, self.password, self.db_name);
            cur = con.cursor()
            cur.execute("""SELECT user_name FROM users WHERE id=%s;""", id);
            result = cur.fetchall()
        except mydb.Error, e:
            print "Error %d: %s" % (e.args[0], e.args[1])
            sys.exit(1)
        finally:
            if con:
                con.close()
        return result[0][0]

    def getUserContinent(self, id):
        con = None
        try:
            con = mydb.connect(self.host, self.db_user_name, self.password, self.db_name);
            cur = con.cursor()
            cur.execute(
                """SELECT continent.id FROM users JOIN countries ON users.country=countries.id JOIN continent ON countries.continent_id=continent.id WHERE users.id=%s;""",
                str(id));
            result = cur.fetchall()
        except mydb.Error, e:
            print "Error %d: %s" % (e.args[0], e.args[1])
            sys.exit(1)
        finally:
            if con:
                con.close()
        return int(result)

    def getUserCountry(self, id):
        con = None
        try:
            con = mydb.connect(self.host, self.db_user_name, self.password, self.db_name);
            cur = con.cursor()
            cur.execute(
                """SELECT countries.name FROM users JOIN countries ON users.country=countries.id WHERE users.id=%s;""",
                id);
            result = cur.fetchall()
        except mydb.Error, e:
            print "Error %d: %s" % (e.args[0], e.args[1])
            sys.exit(1)
        finally:
            if con:
                con.close()
        return result[0][0]

    def getCountries(self):
        con = None
        try:
            con = mydb.connect(self.host, self.db_user_name, self.password, self.db_name);
            cur = con.cursor()
            cur.execute("""SELECT id, name FROM countries""")
            countries = cur.fetchall()
        except mydb.Error, e:
            print "Error %d: %s" % (e.args[0], e.args[1])
            sys.exit(1)
        finally:
            if con:
                con.close()
        return countries

    def getContinents(self):
        con = None
        try:
            con = mydb.connect(self.host, self.db_user_name, self.password, self.db_name)
            cur = con.cursor()
            cur.execute("""SELECT id, name FROM continent""")
            continents = cur.fetchall()
        except mydb.Error, e:
            print "Error %d: %s" % (e.args[0], e.args[1])
            sys.exit(1)
        finally:
            if con:
                con.close()
        return continents


class Mongo:

    port = 27100
    # port = 27017

    def get_user_info(self, username):
        client = MongoClient('localhost', self.port)
        # client = MongoClient('localhost', 27017)
        db = client.twitter
        users = db.users
        user = users.find_one({"role": "user", "username": username})
        return user
        # for user in users.find_one({"role": "user", "username": username}):
        #     if user['username'] == username:
        #         return user

    def add_user(self, username, continent):
        client = MongoClient('localhost', self.port)
        db = client.twitter
        users = db.users
        users.insert_one({'username': username, "role": "user", 'first_name': '', 'last_name': '', 'email': '',
                          'photo': '', 'info': '', 'followers': [], 'followings': [], 'twits': [],
                          'date_of_birthday': '', 'continent': continent, 'hide': 0, 'blocked': 0})

    def update_profile(self, request, username):
        client = MongoClient('localhost', self.port)
        db = client.twitter
        users = db.users
        user = users.find_one({'username': username})
        # print type(request.POST['birthday'])
        hide = 0
        if request.POST.get('is_hide'):
            hide = 1
        users.update({'username': username}, {'$set':
                                                  {'first_name': request.POST['firstName'],
                                                   'last_name': request.POST['lastName'],
                                                   'email': request.POST['email'],
                                                   'info': request.POST['info'],
                                                   'hide': hide,
                                                   'date_of_birthday': datetime.strptime(request.POST['birthday'],
                                                                                         '%Y-%m-%d'),
                                                   }}, upsert=False, multi=True)
        new_first_name = request.POST['firstName']
        new_last_name = request.POST['lastName']
        prev_first_name = user.get('first_name')
        prev_last_name = user.get('last_name')
        hash_data = red.hgetall('users')
        if hash_data:
            keys = hash_data.keys()
            for key in keys:
                if prev_first_name != new_first_name:
                    if str(key).lower() == str(new_first_name).lower():
                        print 'Clear "users" redis'
                        red.hdel('users', key)
                    if str(key).lower() == str(prev_first_name).lower():
                        print 'Clear "users" redis'
                        red.hdel('users', key)
                if prev_last_name != new_last_name:
                    if str(key).lower() == str(new_last_name).lower():
                        print 'Clear "users" redis'
                        red.hdel('users', key)
                    if str(key).lower() == str(prev_last_name).lower():
                        print 'Clear "users" redis'
                        red.hdel('users', key)

    def add_twit(self, username, header, content, hide):
        client = MongoClient('localhost', self.port)
        db = client.twitter
        users = db.users
        posted_date = datetime.strptime(str(datetime.now().strftime("%Y-%m-%d %H:%M")), '%Y-%m-%d %H:%M')
        tags = getTags(content)
        id = uuid.uuid1()
        twit = {'id': id,
                'header': header,
                'content': content,
                'posted_date': posted_date,
                'liked': [],
                'tags': tags,
                'hide': hide
                }
        users.update({'username': username}, {'$push': {'twits': twit}}, upsert=False, multi=True)

        hash_data = red.hgetall('twits')
        print hash_data
        if hash_data:
            keys = hash_data.keys()
            for key in keys:
                if key in tags:
                    print 'Clear "twits" redis'
                    red.hdel('twits', key)

    def user_search(self, name):
        data = red.hget('users', name)
        if data:
            print 'loaded from cache'
            return pickle.loads(data)
        result = []
        client = MongoClient('localhost', self.port)
        db = client.twitter
        users = db.users
        for user in users.find({"role": "user", 'first_name': re.compile(name, re.IGNORECASE)}).limit(20):
            result.append(user)
        for user in users.find({"role": "user", 'last_name': re.compile(name, re.IGNORECASE)}).limit(20):
            if not self.is_already_in_array(user, result):
                result.append(user)
        print 'loaded from mongo'
        red.hset('users', name, pickle.dumps(result))
        return result

    def is_already_in_array(self, user, users):
        for current_user in users:
            if current_user['username'] == user['username']:
                return True
        return False

    def twits_search(self, hashtag):
        data = red.hget('twits', hashtag)
        if data:
            print 'loaded from cache'
            return pickle.loads(data)
        result = []
        client = MongoClient('localhost', self.port)
        db = client.twitter
        users = db.users
        for user in users.find({"role": "user"}):
            for twit in user['twits']:
                if hashtag in twit['tags']:
                    twit['author'] = user['username']
                    result.append(twit)
        result = sorted(result, key=itemgetter('posted_date'), reverse=True)
        print 'loaded from mongo'
        red.hset('twits', hashtag, pickle.dumps(result))
        return result

    def get_userinfo_by_twit_id(self, id):
        client = MongoClient('localhost', self.port)
        db = client.twitter
        users = db.users
        for user in users.find({"role": "user"}):
            for twit in user['twits']:
                if str(id) == str(twit['id']):
                    return user

    def get_user_info_by_id(self, id):
        client = MongoClient('localhost', self.port)
        db = client.twitter
        users = db.users
        for user in users.find({"role": "user"}):
            if str(id) == str(user['_id']):
                return user

    def follow(self, logged_user, user):
        client = MongoClient('localhost', self.port)
        db = client.twitter
        users = db.users
        for u in users.find({"role": "user"}):
            if u['username'] == logged_user:
                print 'find logged user'
                users.update({'username': logged_user}, {'$push': {'followings': user}}, upsert=False, multi=True)
        for u in users.find({"role": "user"}):
            if u['username'] == user:
                print 'find unlogged user'
                users.update({'username': user}, {'$push': {'followers': logged_user}}, upsert=False, multi=True)

    def unfollow(self, logged_user, user):
        client = MongoClient('localhost', self.port)
        db = client.twitter
        users = db.users
        for u in users.find({"role": "user"}):
            if u['username'] == logged_user:
                users.update({'username': logged_user}, {'$pull': {'followings': user}}, upsert=False, multi=True)
        for u in users.find({"role": "user"}):
            if u['username'] == user:
                users.update({'username': user}, {'$pull': {'followers': logged_user}}, upsert=False, multi=True)

    def get_user_followers(self, username):
        result = []
        client = MongoClient('localhost', self.port)
        db = client.twitter
        users = db.users
        for user in users.find({"role": "user"}):
            if username == user['username']:
                for follower in user['followers']:
                    result.append(self.get_user_info(follower))
        return result

    def get_user_followings(self, username):
        result = []
        client = MongoClient('localhost', self.port)
        db = client.twitter
        users = db.users
        for user in users.find({"role": "user"}):
            if username == user['username']:
                for following in user['followings']:
                    result.append(self.get_user_info(following))
        return result

    def get_user_followings_usernames(self, username):
        result = []
        client = MongoClient('localhost', self.port)
        # client = MongoClient('localhost', 27017)
        db = client.twitter
        users = db.users
        for user in users.find({"role": "user"}):
            if username == user['username']:
                for following in user['followings']:
                    result.append(self.get_user_info(following)['username'])
        return result

    def feed(self, username):
        result = []
        client = MongoClient('localhost', self.port)
        db = client.twitter
        users = db.users
        for user in users.find({"role": "user"}):
            if user['username'] == username:
                for following in user['followings']:
                    current_following = self.get_user_info(following)
                    for twit in current_following['twits']:
                        twit['author'] = current_following['username']
                        result.append(twit)
        result = sorted(result, key=itemgetter('posted_date'), reverse=True)
        return result

    def get_twit_tags_by_id(self, twit_id):
        client = MongoClient('localhost', self.port)
        db = client.twitter
        users = db.users
        for user in users.find({"role": "user"}):
            for twit in user['twits']:
                if str(twit_id) == str(twit['id']):
                    return twit['tags']

    def like(self, twit_id, username):
        client = MongoClient('localhost', self.port)
        db = client.twitter
        users = db.users
        for user in users.find({"role": "user"}):
            for twit in user['twits']:
                if str(twit_id) == str(twit['id']):
                    if username in twit['liked']:
                        users.update({'username': user['username'], 'twits.id': twit['id']},
                                     {'$pull': {'twits.$.liked': username}}, upsert=False, multi=True)
                    else:
                        users.update({'username': user['username'], 'twits.id': twit['id']},
                                     {'$push': {'twits.$.liked': username}}, upsert=False, multi=True)

        hash_data = red.hgetall('twits')
        if hash_data:
            keys = hash_data.keys()
            for key in keys:
                if key in self.get_twit_tags_by_id(twit_id):
                    print 'Clear "twits" redis'
                    red.hdel('twits', key)

    def get_popular_tags(self):
        rows = []
        client = MongoClient('localhost', self.port)
        db = client.twitter

        map = Code("function map(){"
                   "for(var i = 0; i < this.twits.length; i++) {"
                   "for(var j = 0; j < this.twits[i].tags.length; j++) {"
                   "key = this.twits[i].tags[j];"
                   "value = 1;"
                   "emit(key, value);"
                   "}"
                   "}"
                   "}")
        reduce = Code("function reduce(key, values) {"
                      "var sum = 0;"
                      "for(var i in values) {"
                      "sum += values[i];"
                      "}"
                      "return sum;"
                      "}")

        result = db.users.map_reduce(map, reduce, "tags")

        for element in result.find().sort('value', -1).limit(10):
            rows.append({'tag': element['_id'], 'value': int(element['value'])})
        return rows

    def get_last_week_twits(self):
        rows = []
        client = MongoClient('localhost', self.port)
        db = client.twitter
        users = db.users
        week_ago = datetime.now() - timedelta(days=7)
        for user in users.find({"role": "user"}):
            for twit in user['twits']:
                if twit['posted_date'] > week_ago:
                    rows.append(twit['posted_date'])
        return len(rows)

    def get_last_month_twits(self):
        rows = []
        client = MongoClient('localhost', self.port)
        db = client.twitter
        users = db.users
        week_ago = datetime.now() - timedelta(days=30)
        for user in users.find({"role": "user"}):
            for twit in user['twits']:
                if twit['posted_date'] > week_ago:
                    rows.append(twit['posted_date'])
        return len(rows)

    def get_most_active_users(self):
        result = []
        client = MongoClient('localhost', self.port)
        db = client.twitter
        rows = db.users.aggregate([
            {"$unwind": "$twits"},
            {'$group': {'_id': "$username", 'twits': {"$push": "$twits"}, 'twit_count': {'$sum': 1}}},
            {'$sort': {'twit_count': -1}},
            {'$limit': 5}])
        for row in rows:
            result.append({'user': row['_id'], 'twits_count': row['twit_count']})
        return result

    def get_most_popular_users(self):
        result = []
        client = MongoClient('localhost', self.port)
        db = client.twitter
        rows = db.users.aggregate([
            {"$unwind": "$followers"},
            {'$group': {'_id': "$username", 'followers': {"$push": "$followers"}, 'followers_count': {'$sum': 1}}},
            {'$sort': {'followers_count': -1}},
            {'$limit': 5}])
        for row in rows:
            result.append({'user': row['_id'], 'followers_count': row['followers_count']})
        return result

    def get_suspicious_users(self):
        result = []
        client = MongoClient('localhost', self.port)
        db = client.twitter
        users = db.users
        admin = users.find_one({"role": "admin"})
        for suspicious_user in admin['suspicious_users']:
            result.append(self.get_user_info(suspicious_user))
        return result

    def get_blocked_users(self):
        result = []
        client = MongoClient('localhost', self.port)
        db = client.twitter
        users = db.users
        admin = users.find_one({"role": "admin"})
        for suspicious_user in admin['blocked_users']:
            result.append(self.get_user_info(suspicious_user))
        return result

    def add_admin(self):
        client = MongoClient('localhost', self.port)
        db = client.twitter
        users = db.users
        users.insert_one({'username': "taras", "role": "admin", "blocked_users": [], "suspicious_users": [],
                          "twits": [], "continent": 3})

    def get_blocked_users_usernames(self):
        result = []
        client = MongoClient('localhost', self.port)
        db = client.twitter
        users = db.users
        admin = users.find_one({"role": "admin"})
        for suspicious_user in admin['blocked_users']:
            result.append(self.get_user_info(suspicious_user)['username'])
        return result

    def block_user(self, username):
        client = MongoClient('localhost', self.port)
        db = client.twitter
        users = db.users
        users.update({'username': username}, {'$set': {'blocked': 1}}, upsert=False, multi=True)
        users.update({'role': 'admin'}, {'$push': {'blocked_users': username}}, upsert=False, multi=True)
        if username in users.find_one({'role': 'admin'})['suspicious_users']:
            users.update({'role': 'admin'}, {'$pull': {'suspicious_users': username}}, upsert=False, multi=True)

    def unblock_user(self, username):
        client = MongoClient('localhost', self.port)
        db = client.twitter
        users = db.users
        users.update({'username': username}, {'$set': {'blocked': 0}}, upsert=False, multi=True)
        users.update({'role': 'admin'}, {'$pull': {'blocked_users': username}}, upsert=False, multi=True)

    def set_user_as_reliable(self, username):
        client = MongoClient('localhost', self.port)
        db = client.twitter
        users = db.users
        users.update({'role': 'admin'}, {'$pull': {'suspicious_users': username}}, upsert=False, multi=True)

    def report(self, username):
        client = MongoClient('localhost', self.port)
        db = client.twitter
        users = db.users
        if username not in users.find_one({'role': 'admin'})['suspicious_users']:
            users.update({'role': 'admin'}, {'$push': {'suspicious_users': username}}, upsert=False, multi=True)

    def random_user(self, username, cont, email):
        client = MongoClient('localhost', self.port)
        db = client.twitter
        users = db.users
        first_name = user_generator.getFirstName()
        last_name = user_generator.getLastName()
        info = 'I am ' + username
        birthday = datetime.strptime(str(user_generator.getBirthDate()), '%Y-%m-%d')
        twits = [user_generator.get_twit(), user_generator.get_twit(), user_generator.get_twit()]
        users.insert_one({'username': username, "role": "user", 'first_name': first_name, 'last_name': last_name,
                          'email': email,
                          'photo': '', 'info': info, 'followers': [], 'followings': [], 'twits': twits,
                          'date_of_birthday': birthday, 'continent': cont, 'hide': 0, 'blocked': 0}, )
