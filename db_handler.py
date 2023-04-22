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


# def get_stored_boxes(customer_id):
#     session = Session()
#     boxes = session.query(Box).join(Orders).filter(Orders.customer_id == customer_id).all()
#     boxes_list = ['У Вас на хранении:']
#     for box in boxes:
#         boxes_list.append(f'Коробка *{box.size}* срок хранения до *{datetime.date(box.orders[0].expired_at)}*')
#     session.close()
#     return '\n'.join(boxes_list)


def get_customer_orders(customer_id):
    session = Session()
    orders = session.query(Orders).filter(Orders.customer_id == customer_id).all()
    # boxes = ['У Вас на хранении:']
    # for order in orders:
    #     boxes.append(f'Коробка {order.box.size}, срок хранения {order.expired_at}')
    session.close()
    return orders


def add_customer(first_name, user_id):
    session = Session()
    customer = Customer(name=first_name, customer_id=user_id)
    session.add(customer)
    session.commit()
    session.close()


def get_storage_addresses():
    session = Session()
    addresses = [row[0] for row in session.query(Storage.address).all()]
    return '\n'.join(addresses)


def create_order():
    pass