import requests
import json
import os
from abc import ABCMeta, abstractmethod


class PushDataBase(object):
    __metaclass__ = ABCMeta

    # TODO - add property 'name' for use with logging

    # TODO - add property on whether or not to check if push was successful before marking as sent

    # TODO - add abstract method for checking whether the push was successful.

    @abstractmethod
    def push(self, sensordata):
        pass


class PNPushData(PushDataBase):
    name = 'Pervasive Nation'
    max_retries = 20

    def push(self, sensordata):
        print('Pushing [%d] %s data to PN %s with timestamp %s' % (sensordata.id, str(sensordata.deviceid), str(sensordata.payload), str(sensordata.timestamp)))
        payload = {"payload": str(sensordata.payload)}

        headers = {"Authorization": "Bearer %s" % os.environ.get('PERVASIVENATION_AUTHTOKEN', None)}
        #url = 'https://api.pervasivenation.com'
        url = 'http://127.0.0.1:8000/publish'
        try:
            r = requests.post(url, data=json.dumps(payload), headers=headers)
            if r.status_code == 200:
                return True
            elif r.status_code == 401:
                print('Authorization token is incorrect or not set. '
                      'Use environment variable PERVASIVENATION_AUTHTOKEN to set token.')
                return False
        except requests.ConnectionError as conn_error:
            print('There was a connection error connecting to Pervasive Nation.')
        return False
