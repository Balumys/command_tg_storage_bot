from db import Base, Customer, Orders, Storage, Box
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///database.db')
Session = sessionmaker(bind=engine)

""" SOME QUERIES """


def get_customer_id(user_id):
    session = Session()
    tg_id = session.query(Customer.customer_id).filter_by(customer_id=user_id).one_or_none()
    return tg_id


def add_customer(first_name, last_name):
    session = Session()
    customer = Customer(name=f"{first_name} {last_name}", email='some_two@mail.com', phone='+79000000')
    session.add(customer)
    session.commit()
    session.close()


def get_storage_addresses():
    session = Session()
    addresses = [row[0] for row in session.query(Storage.address).all()]
    return addresses
