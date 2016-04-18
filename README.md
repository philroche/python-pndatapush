# pndatapush
Python module to push data to the Pervasive Nation IoT network. It saves data locally until there is internet access. 

#To install

`pip install pndatapush`

#To run an example

`python examples/gatherdata.py`

#To add to your project
Create an instance of the Offline class.

`offline = Offline(payload_consumers=[PNPushData]) #PNPushData is a data consumer class. see pnpushdata.pushdata.PNPushData`

Then when sensor data is received save the data

`offline.save('12456', 30.00) #save(self, deviceid, payload):`


#TODO
pushdata.py
(7, 7) # TODO - add property 'name' for use with logging
(9, 7) # TODO - add property on whether or not to check if push was successful before marking as sent
(11, 7) # TODO - add abstract method for checking whether the push was successful.
(23, 11) # TODO this needs to push to AWS IoT HTTPS API