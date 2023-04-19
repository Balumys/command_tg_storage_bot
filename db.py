import datetime

from sqlalchemy import create_engine, ForeignKey, Column, String, Integer, DateTime, Float
from sqlalchemy.orm import relationship, declarative_base

engine = create_engine('sqlite:///database.db', echo=True)
Base = declarative_base()


class Customer(Base):
    __tablename__ = 'customers'

    customer_id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    address = Column(String(250))
    phone = Column(String(20), nullable=False)
    orders = relationship('Orders', backref='customers')

    def __repr__(self):
        return f"({self.customer_id} {self.name})"


class Orders(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.datetime.now(), nullable=False)
    expired_at = Column(DateTime, nullable=False)  # This should be calc
    customer_id = Column(Integer, ForeignKey(Customer.customer_id))
    boxes = relationship("Box", backref='order')
    price = Column(Integer, nullable=False)  # This should be calc
    is_delivery = Column(Integer, nullable=False)  # 1 if yes, 0 in not

    def __repr__(self):
        return f"({self.order_id} {self.customer_id} expired at {self.expired_at})"


class Storage(Base):
    __tablename__ = 'storage'

    id = Column(Integer, primary_key=True)
    address = Column(String(250), nullable=False)
    area = Column(Float)
    free_space = Column(Float)  # This should be calc

    def __repr__(self):
        return f"({self.id} {self.free_space})"


class Box(Base):
    __tablename__ = 'box'

    id = Column(Integer, primary_key=True)
    state = Column(String, nullable=False)
    size = Column(String, nullable=False)
    price = Column(Float)
    storage_id = Column(Integer, ForeignKey(Storage.id))
    order_id = Column(Integer, ForeignKey(Orders.id))

    def __repr__(self):
        return f"({self.size} {self.id} {self.state})"


Base.metadata.create_all(bind=engine)
