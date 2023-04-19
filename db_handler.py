from db import Base, Customer, Orders, Storage, Box
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///database.db')
Session = sessionmaker(bind=engine)

""" SOME QUERIES """


def add_customer(first_name, last_name):
    session = Session()
    customer = Customer(name=f"{first_name} {last_name}", email='some_two@mail.com', phone='+79000000')
    session.add(customer)
    session.commit()
    session.close()
