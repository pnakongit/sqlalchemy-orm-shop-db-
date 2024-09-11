import datetime
import re
import enum

from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    ForeignKey,
    func,
    DECIMAL,
    Text,
    DateTime,
    Enum,
)

from sqlalchemy.orm import (
    sessionmaker,
    relationship,
    DeclarativeBase,
    validates
)


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(20), unique=True, nullable=False)
    email = Column(String(50), unique=True, nullable=False)

    cart = relationship("Cart", back_populates="user", uselist=False, cascade="all, delete-orphan")
    orders = relationship("Order", back_populates="user")

    @validates('username')
    def validate_username(self, key, username):
        if len(username) < 5 or len(username) > 20:
            raise ValueError('Username must be between 5 and 20 characters')
        return username

    @validates('email')
    def validate_email(self, key, email) -> email:
        print(key)
        if not re.match("[^@]+@[^@]+\.[^@]+", email):
            raise ValueError('Provided email is not an email address')
        return email

    def __repr__(self) -> str:
        return f"User: {self.username}"


class Cart(Base):
    __tablename__ = 'carts'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    user = relationship('User', back_populates='cart', single_parent=True)
    cart_items = relationship('CartItem', back_populates='cart', cascade='all, delete-orphan')

    def __repr__(self) -> str:
        return f"Cart: {self.id}"


class Order(Base):
    class OrderType(enum.Enum):
        NEW = 0
        DONE = 1
        CANCELLED = 2

    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', back_populates='orders')
    created = Column(DateTime, default=datetime.datetime.utcnow)
    status = Column(Enum(OrderType), default=OrderType.NEW)
    order_items = relationship('OrderItem', back_populates='order')

    def __repr__(self) -> str:
        return f"Order: {self.id}"


class ItemAbstract(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True)
    quantity = Column(Integer, nullable=False)


class CartItem(ItemAbstract):
    __tablename__ = 'cart_items'

    cart_id = Column(Integer, ForeignKey('carts.id'), nullable=False)
    cart = relationship('Cart', back_populates='cart_items')
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    product = relationship('Product', back_populates='cart_items')

    def __repr__(self):
        return f"CartItem: {self.id}"


class OrderItem(ItemAbstract):
    __tablename__ = 'order_items'
    order_id = Column(Integer, ForeignKey('orders.id'), nullable=False)
    order = relationship('Order', back_populates='order_items')
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    product = relationship('Product', back_populates='order_items')

    def __repr__(self):
        return f"OrderItem: {self.id}"


class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    name = Column(String(20), unique=True, nullable=False)
    products = relationship('Product', back_populates='category')

    def __repr__(self) -> str:
        return f"Category: {self.name}"


class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    name = Column(String(20), unique=True, nullable=False)
    price = Column(DECIMAL(precision=20, scale=2), nullable=False)
    quantity = Column(Integer, nullable=False)
    description = Column(Text, nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)
    category = relationship('Category', back_populates='products')

    order_items = relationship('OrderItem', back_populates='product')
    cart_items = relationship('CartItem', back_populates='product')

    def __repr__(self) -> str:
        return f"Product: {self.name}"


engine = create_engine("sqlite:///project.db", echo=True)

Base.metadata.create_all(engine)
