#!/usr/bin/python

import beanstalkc
import pyrebase
import json
import datetime
from collections import OrderedDict
from pprint import pprint
# beanstalk connection
beanstalk = beanstalkc.Connection(host='localhost', port=11300)

TUBE_NAME='alprd'
print beanstalk.tubes()
try:
    pprint(beanstalk.stats_tube(TUBE_NAME))
except beanstalkc.CommandFailed:
    print "Tube doesn't exist"
# Watch the "alprd" tube
beanstalk.watch(TUBE_NAME)
#firebase connection
config = {
    "apiKey": "AIzaSyAANcKn2DbtmdEJzJq9xkcM_G-sgxv9ac8",
    "authDomain": "paynpark-a72b6.firebaseapp.com",
    "databaseURL": "https://paynpark-a72b6.firebaseio.com",
    "storageBucket": "paynpark-a72b6.appspot.com",
    "serviceAccount": "/home/pi/Desktop/PayNPark-Daemon/firebase/PayNPark-31d19785cc09.json"
}
firebase = pyrebase.initialize_app(config)
db=firebase.database()
#firebase authentication
auth=firebase.auth()
user = auth.sign_in_with_email_and_password("projectapas@gmail.com", "projectapas4")


plate_number=[]
i=0
while True:
    # Wait for a second to get a job. If there is a job, process it and delete it from the queue.
    # If not, return to sleep.
    now= datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")
    job = beanstalk.reserve(timeout=1.0)
    if job is None:
        print "No plates available right now, waiting...", i
        i+=1
    else:
        print "Found a plate!"
        plates_info = json.loads(job.body)
        # Print all the info about this plate
        if 'data_type' not in plates_info:
            print "This shouldn't be here... all OpenALPR data should have a data_type"
        elif plates_info['data_type'] == 'alpr_results':
            print "This is a plate result"
        elif plates_info['data_type'] == 'alpr_group':
            for key in plates_info:
                if key == "best_plate_number":
                    # pprint (plates_info)
                    flag=0
                    print plates_info[key]
                    plate_number.append(plates_info[key])
                    #### Retrival ka code
                    all_agents = db.child("users").get(user['idToken']).val()
                    dictlist=[]
                    dct=OrderedDict(all_agents)
                    for u_key, data in dct.iteritems():
                        if(str(data["plate_number"])==plates_info[key]):
                            flag=1
                            print str(data["name"])
                            t={"Timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S"),"Number_plate": plates_info[key],"Name":data["name"]}
                            db.child("log").push(t,user['idToken'])
                    if(flag==0):
                    ##### Put in firebase
                        t = {"Name": now, "Value": str(plates_info[key])}
                        db.child("scanned_plate").push(t, user['idToken'])
                    print "This is a group result"
        elif plates_info['data_type'] == 'heartbeat':
            print "This is a heartbeat"
        # Delete the job
        job.delete()