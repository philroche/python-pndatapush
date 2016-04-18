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
        # TODO this needs to push to AWS IoT HTTPS API
        print('Pushing [%d] %s data to PN %s with timestamp %s' % (sensordata.id, str(sensordata.deviceid), str(sensordata.payload), str(sensordata.timestamp)))
        return True
