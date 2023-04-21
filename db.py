import datetime

from sqlalchemy import create_engine, ForeignKey, Column, String, Integer, DateTime, Float, Boolean
from sqlalchemy.orm import relationship, declarative_base

engine = create_engine('sqlite:///database.db', echo=True)
Base = declarative_base()


class Customer(Base):
    __tablename__ = 'customers'

    customer_id = Column(Integer, primary_key=True, unique=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100))
    address = Column(String(250))
    phone = Column(String(20))
    orders = relationship('Orders', back_populates='customer', cascade='all, delete')

    def __repr__(self):
        return f"({self.customer_id} {self.name})"


class Orders(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.datetime.now())
    expired_at = Column(DateTime)  # This should be calc
    price = Column(Integer, nullable=False)  # This should be calc
    is_delivery = Column(Boolean, nullable=False)

    customer_id = Column(Integer, ForeignKey(Customer.customer_id, ondelete='CASCADE'))
    customer = relationship('Customer', back_populates='orders', cascade='all, delete')

    box_id = Column(Integer, ForeignKey('box.id', ondelete='CASCADE'))
    box = relationship('Box', uselist=False, back_populates='order', cascade='all, delete')

    def __repr__(self):
        return f"({self.order_id} {self.customer_id} expired at {self.expired_at})"


class Storage(Base):
    __tablename__ = 'storage'

    id = Column(Integer, primary_key=True)
    address = Column(String(250), nullable=False)
    # area = Column(Float)  # WE DON'T NEED THIS NOW
    # free_space = Column(Float)  # WE DON'T NEED THIS NOW

    def __repr__(self):
        return f"({self.id} {self.free_space})"


class Box(Base):
    __tablename__ = 'box'

    id = Column(Integer, primary_key=True)
    state = Column(String, nullable=False)
    size = Column(String, nullable=False)
    price = Column(Float)
    storage_id = Column(Integer, ForeignKey(Storage.id))

    order = relationship('Orders', back_populates='box')

    def __repr__(self):
        return f"({self.size} {self.id} {self.state})"


Base.metadata.create_all(bind=engine)
