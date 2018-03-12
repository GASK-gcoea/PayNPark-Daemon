#!/usr/bin/env python
import beanstalkc
import time
import json
beanstalk = beanstalkc.Connection(host='localhost', port=11300)
beanstalk.watch('alprd')
while True:
	job = beanstalk.reserve(timeout=0)
        if job is not None:
                decoded= json.loads(job.body)
                _plate = decoded['results'][0]['plate']
                _uuid = decoded['uuid']
                epoch = decoded['epoch_time']
                _date = time.strftime('%Y-%m-%d',time.localtime(epoch/1000))
                _time = time.strftime('%H:%M:%S',time.localtime(epoch/1000))
                _location = decoded['site_id']
                _camera = decoded['camera_id']
                print(_plate,_uuid,epoch,_date,_time,_location,_camera)

                job.delete()
	else:
		break
exit()
