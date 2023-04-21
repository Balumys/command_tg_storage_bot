from datetime import datetime
from db import Base, Customer, Orders, Storage, Box
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///database.db')
Session = sessionmaker(bind=engine)

""" SOME QUERIES """


def get_customer_id(user_id):
    session = Session()
    tg_id = session.query(Customer.customer_id).filter_by(customer_id=user_id).one_or_none()
    session.close()
    return tg_id[0] if tg_id is not None else None


def get_stored_boxes(customer_id):
    session = Session()
    boxes = session.query(Box).join(Orders).filter(Orders.customer_id == customer_id).all()
    boxes_list = ['У Вас на хранении:']
    for box in boxes:
        boxes_list.append(f'Коробка *{box.size}* срок хранения до *{datetime.date(box.order.expired_at)}*')
    session.close()
    return '\n'.join(boxes_list)


def add_customer(first_name, last_name):
    session = Session()
    customer = Customer(name=f"{first_name} {last_name}", email='some_two@mail.com', phone='+79000000')
    session.add(customer)
    session.commit()
    session.close()


def get_storage_addresses():
    session = Session()
    addresses = [row[0] for row in session.query(Storage.address).all()]
    return '\n'.join(addresses)
