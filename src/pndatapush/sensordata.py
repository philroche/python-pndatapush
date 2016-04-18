from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import column_property
from sqlalchemy import select, func

Base = declarative_base()


class SensorDataPushState(Base):
    __tablename__ = 'sensordatapushstate'

    id = Column(Integer, Sequence('data_id_seq'), primary_key=True)
    timestamp = Column(Text, nullable=False)
    consumer = Column(String, index=True, nullable=False)
    sent = Column(Boolean, index=True, default=False)
    attempts = Column(Integer, default=0)

    sensordata_id = Column(Integer, ForeignKey('sensordata.id'))
    sensordata = relationship("SensorData", back_populates="consumers")

    def __repr__(self):
        return "<SensorDataPushState(id='%d', deviceid='%s', timestamp='%s', consumer='%s', sent='%s')>" % (
            self.id, self.sensordata.deviceid, self.timestamp, self.consumer, self.sent)

class SensorData(Base):
    __tablename__ = 'sensordata'

    id = Column(Integer, Sequence('data_id_seq'), primary_key=True)
    timestamp = Column(Text, nullable=False)
    deviceid = Column(String, index=True, nullable=False)
    payload = Column(String, nullable=False)

    sent = Column(Boolean, index=True, default=False)

    #count for how many have not been sent
    notsent_count = column_property(
            select([func.count(SensorDataPushState.id)]).
            where(and_(SensorDataPushState.sent == False, SensorDataPushState.sensordata_id == id)).
            correlate_except(SensorDataPushState)
    )

    consumers = relationship("SensorDataPushState", order_by=SensorDataPushState.id, back_populates="sensordata")

    def __repr__(self):
        return "<SensorData(id='%d', deviceid='%s', timestamp='%s', payload='%s', sent='%s')>" % (
            self.id, self.deviceid, self.timestamp, self.payload, self.sent)

