import pyrebase
import json
import datetime
from collections import OrderedDict
#firebase connection
config = {
    "apiKey": "AIzaSyAANcKn2DbtmdEJzJq9xkcM_G-sgxv9ac8",
    "authDomain": "paynpark-a72b6.firebaseapp.com",
    "databaseURL": "https://paynpark-a72b6.firebaseio.com",
    "storageBucket": "paynpark-a72b6.appspot.com",
    "serviceAccount": "/home/pi/Desktop/PayNPark-Daemon/firebase/PayNPark-31d19785cc09.json"
}
firebase = pyrebase.initialize_app(config)

#firebase authentication
auth=firebase.auth()
user = auth.sign_in_with_email_and_password("PayNPark-Daemon@gmail.com", "projectapas4")

db=firebase.database()
#### Retrival ka code

# all_agents = db.child("scanned_plate").get(user['idToken']).val()
# dictlist=[]
# dct=OrderedDict(all_agents)
# for u_key, data in dct.iteritems():
#     temp=[str(data["Name"]),str(data["Value"])]
#     dictlist.append(temp)
# print dictlist


##### Put in firebase

t= {"Name": datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S"), "Value":"MH27AG5992"}
db.child("scanned_plate").push(t,user['idToken'])