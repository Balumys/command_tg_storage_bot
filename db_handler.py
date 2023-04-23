import datetime

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
    session.close()
    return orders


def add_customer(first_name, user_id):
    session = Session()
    customer = Customer(name=first_name, customer_id=user_id)
    session.add(customer)
    session.commit()
    session.close()


def add_phone_to_customer(customer_id, phone):
    session = Session()
    customer = session.query(Customer).filter(Customer.customer_id == customer_id).first()
    customer.phone = phone
    session.add(customer)
    session.commit()
    session.close()


def add_email_to_customer(customer_id, email):
    session = Session()
    customer = session.query(Customer).filter(Customer.customer_id == customer_id).first()
    customer.email = email
    session.add(customer)
    session.commit()
    session.close()


def add_address_to_customer(customer_id, address):
    session = Session()
    customer = session.query(Customer).filter(Customer.customer_id == customer_id).first()
    customer.address = address
    session.add(customer)
    session.commit()
    session.close()


def get_storage_address():
    session = Session()
    addresses = [row[0] for row in session.query(Storage.address).all()]
    return '\n'.join(addresses)


def create_order(customer_id, box_size, period, is_delivery):
    session = Session()
    periods = {
        1: datetime.timedelta(days=30),
        3: datetime.timedelta(days=90),
        6: datetime.timedelta(days=180),
        12: datetime.timedelta(days=365)
    }
    created_at = datetime.datetime.now()
    expired_at = created_at + periods[period]
    order = Orders(
        created_at=created_at,
        expired_at=expired_at,
        is_delivery=is_delivery,
        price=500,
        customer_id=customer_id,
        box_id=session.query(Box).filter(Box.size == box_size).first().id,
        period=period,
    )
    session.add(order)
    session.commit()
    session.close()
    return order
