import urllib2
import os
from threading import Thread
from datetime import datetime
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from sensordata import SensorData, Base, SensorDataPushState
from utils import get_or_create


def active_internet_connection():
    try:
        # TODO add a way to configure which IP address to use.
        # 85.91.7.19 is one of the IP-addresses for google.ie
        response = urllib2.urlopen('http://85.91.7.19', timeout=1)
        return True
    except urllib2.URLError as err:
        pass
    return False

DEFAULT_DB_PATH = 'sqlite:///%s/sensordata.db' % os.path.dirname(os.path.realpath(__file__))

class Offline(object):
    session = null
    engine = null
    payload_consumers = []
    dbpath = null

    def __init__(self, payload_consumers=[], dbpath=DEFAULT_DB_PATH):
        self.dbpath = dbpath
        self.payload_consumers = payload_consumers

        self.engine = create_engine(self.dbpath,
                                    echo=False)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()
        self.createdb()  # Create the database if it doesn't exist

        # start a thread that loops through all unsent messages and pushes to all configured consumers
        self.start_push_thread()

    def save(self, deviceid, payload):
        payloadobj = SensorData(deviceid=str(deviceid), timestamp=str(datetime.utcnow()), payload=str(payload))
        self.session.add(payloadobj)
        self.session.commit()

    def get_dbath(self):
        return self.dbpath

    def createdb(self):
        # Create the database if it doesn't exist
        Base.metadata.create_all(self.engine, checkfirst=True)

    def start_push_thread(self):
        thread = Thread(target=self.push_unsent_payloads)
        thread.daemon = True
        thread.start()

    def push_unsent_payloads(self):
        # we need to create our own session here as we're running in a new thread
        local_session = self.Session()
        while True:  # Infinite loop while parent process is working
            # check if internet access
            if active_internet_connection():

                unsent_payloads = local_session.query(SensorData).filter(not_(SensorData.sent == len(self.payload_consumers)))
                for payload in unsent_payloads:
                    # print('Pushing [%d] %s (%s) to all consumers' % (payload.id, str(payload.payload), str(payload.timestamp)))
                    for consumer in self.payload_consumers:
                        consumer_obj = consumer()
                        consumer_obj.push(payload.deviceid, payload.timestamp, payload.payload)

                        consumer_push_state, created = get_or_create(local_session, SensorDataPushState, defaults={'timestamp':str(datetime.utcnow())}, sensordata_id=payload.id, consumer=str(consumer_obj.name))
                        consumer_push_state.timestamp = str(datetime.utcnow())
                        consumer_push_state.sent = True

                        local_session.add(consumer_push_state)
                        local_session.commit()

