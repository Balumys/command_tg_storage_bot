import datetime

from db import Customer, Orders, Storage, Box
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from environs import Env


env = Env()
env.read_env()
db_path = env('DB_PATH')
engine = create_engine(f'sqlite:///{db_path}')
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
            f'№{order.id} бокс {order.box.size}, '
            f'до {datetime.datetime.date(order.expired_at)}'
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


def create_order(customer_id, box_size, period, is_delivery, status_id):
    session = Session()
    periods = {
        1: datetime.timedelta(days=30),
        3: datetime.timedelta(days=90),
        6: datetime.timedelta(days=180),
        12: datetime.timedelta(days=365)
    }
    price_per_month = {
        'S': 1000,
        'M': 2000,
        'L': 3000,
        'XL': 4000
    }
    created_at = datetime.datetime.now().date()
    expired_at = created_at + periods[period]
    if box_size != 'Unknown':
        price = price_per_month[box_size] * period
    else:
        price = 0

    box_id = session.query(Box).filter(Box.size == box_size).first().id

    order = Orders(
        created_at=created_at,
        expired_at=expired_at,
        is_delivery=is_delivery,
        price=price,
        customer_id=customer_id,
        box_id=box_id,
        period=period,
        status_id=status_id
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
        'box_size': order.box.size if order.box.size != 'Unknown' else 'Будет уточнен',
        'price': order.price if order.box.size != 'Unknown' else 'Будет уточнен',
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


def is_customer_exist(customer_id):
    session = Session()
    customer = session.query(Customer).filter_by(customer_id=customer_id).first()
    if customer.phone:
        return customer
    else:
        return False
