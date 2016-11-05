import sys
import MySQLdb as mydb
import xml.etree.ElementTree as ET
import pymongo
from pymongo import MongoClient


class Login:

    host = 'localhost'
    db_user_name = 'root'
    password = '852456aaa'
    db_name = 'twitter'

    def isLogin(self, request):
        con = None

        print 'I am in Login class'
        user_id = None

        print request.POST["password"]
        print request.POST["username"]

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

        # inserted_date = str(request["date"])
        # inserted_id = str(request["employee_id"])
        #
        # try:
        #     con = mydb.connect( self.host, self.db_user_name, self.password, self.db_name);
        #     cur = con.cursor()
        #     cur.execute("""INSERT INTO Visiting(employee_id, visit_date) VALUES (%s, %s);""", (inserted_id, inserted_date))
        #     con.commit()
        #
        # except mydb.Error, e:
        #
        #     print "Error %d: %s" % (e.args[0],e.args[1])
        #     sys.exit(1)
        #
        # finally:
        #     if con:
        #         con.close()


