from sqlalchemy import Column, Float, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchey.orm import sessionmaker
from sqlalchemy import create_engine

Base = declarative_base()


#User class 
class User(Base):
  """

  """
  __tablename__ = 'user'
  id = Column(Integer, primary_key=True)
  first_name = Column(String(250))
  last_name = Column(String(250))
  password = Column(String(20))
  email = Column(String(250))
  status = Column(String)
  address = Column(String)




# appointment class
class Appointments(Base):
  """
  """
  __tablename__ = 'appointments'
  id = Column(Integer, primary_key=True)
  customer_id = Column(Integer, ForeignKey(user.id))
  status = Column(String)
  vehicle_id = Column(Integer, ForeignKey(vehicle.id))
  date_of_appointment = Column(String)
  date_of_completion = Column(String)
  detailer_assigned_id = Column(Integer, ForeignKey(user.id))
  price = Column(Float)



# Vehicle
class Vehicle(Base):
  """
  """
  __tablename__ = 'vehicle'
  id = Column(Integer, primary_key=True)
  user_id = Column(Integer, ForeignKey(user.id))
  make = Column(String)
  model = Column(String)
  year = Column(Integer)
  color = Column(String)

# Vehicle before and after images
class VehicleImages(Base):
  """
  """
  __tablename__ = 'vehicleimages'
  id = Column(Integer, primary_key=True)
  vehicle_id = Column(Integer, ForeignKey(vehicle.id))
  image = Column(String)
  Job_id = Column(Integer, ForeignKey(appointments.id))
  before_or_after = Column(String)
  remarks = Column(String)


engine = create_engine('sqlite:///detailers.db')
Base.metadata.bind = engine
Db = sessionmaker(bind=engine)
Base.metadata.create_all()
session = DB()
