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


def get_customer_orders(customer_id):
    session = Session()
    orders = session.query(Orders).filter(Orders.customer_id == customer_id).all()
    order_list = []
    for order in orders:
        order_list.append(
            f'Заказ №{order.id} коробка {order.box.size},'
            f' срок хранения до {datetime.datetime.date(order.expired_at)}'
        )
    session.close()
    return order_list


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
    session.close()
    return '\n'.join(addresses)


def create_order(customer_id, box_size, period, is_delivery):
    session = Session()
    periods = {
        1: datetime.timedelta(days=30),
        3: datetime.timedelta(days=90),
        6: datetime.timedelta(days=180),
        12: datetime.timedelta(days=365)
    }
    created_at = datetime.datetime.now().date()
    expired_at = created_at + periods[period]
    box_id = session.query(Box).filter(Box.size == box_size).first().id

    order = Orders(
        created_at=created_at,
        expired_at=expired_at,
        is_delivery=is_delivery,
        price=500,
        customer_id=customer_id,
        box_id=box_id,
        period=period,
    )
    session.add(order)
    session.commit()
    session.close()


def get_customer_phone(customer_id):
    session = Session()
    phone = session.query(Customer.phone).filter(Customer.customer_id == customer_id).scalar()
    session.close()
    return phone


def get_last_customer_order(customer_id):
    session = Session()
    order = session.query(Orders).filter(Orders.customer_id == customer_id).all()[-1]
    context = {
        'order_id': order.id,
        'created_at': order.created_at,
        'expired_at': order.expired_at,
        'box_size': order.box.size,
        'is_delivery': order.is_delivery,
    }
    session.close()
    return context


def delete_order_by_id(order_id):
    session = Session()
    order = session.query(Orders).filter(Orders.id == order_id).one()
    session.delete(order)
    session.commit()
    session.close()


def get_expiration_date(customer_id):
    session = Session()
    orders = session.query(Orders).filter_by(customer_id=customer_id).all()
    session.close()
    return orders
