# ============================================================
# SQLAlchemy Shop Database Assignment
# ============================================================

# --------------------------------------------------
# Part 1: Setup - Imports, Engine, Base, and Session
# --------------------------------------------------
from sqlalchemy import (
    create_engine, Column, Integer, String, Float, Boolean, ForeignKey, func
)
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

# Create an SQLite database engine (creates shop.db in the current directory)
engine = create_engine("sqlite:///shop.db", echo=False)

# Base class that all ORM models will inherit from
Base = declarative_base()

# Session factory bound to our engine
Session = sessionmaker(bind=engine)


# --------------------------------------------------
# Part 2: Define Tables and Relationships
# --------------------------------------------------

class User(Base):
    """Represents a customer in the shop."""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)

    # One user can have many orders
    orders = relationship("Order", back_populates="user")

    def __repr__(self):
        return f"<User(id={self.id}, name='{self.name}', email='{self.email}')>"


class Product(Base):
    """Represents an item available for purchase."""
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)

    # One product can appear in many orders
    orders = relationship("Order", back_populates="product")

    def __repr__(self):
        return f"<Product(id={self.id}, name='{self.name}', price={self.price})>"


class Order(Base):
    """Represents a purchase linking a user to a product."""
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    shipped = Column(Boolean, nullable=False, default=False)  # Bonus: shipment status

    # Relationships back to User and Product
    user = relationship("User", back_populates="orders")
    product = relationship("Product", back_populates="orders")

    def __repr__(self):
        return (
            f"<Order(id={self.id}, user='{self.user.name}', "
            f"product='{self.product.name}', qty={self.quantity}, "
            f"shipped={self.shipped})>"
        )


# --------------------------------------------------
# Part 3: Create All Tables
# --------------------------------------------------
# This issues CREATE TABLE statements for every model that extends Base
Base.metadata.create_all(engine)
print("Tables created successfully.\n")


# --------------------------------------------------
# Part 4: Insert Sample Data
# --------------------------------------------------
session = Session()

# Create 2 users
user1 = User(name="Alice Johnson", email="alice@example.com")
user2 = User(name="Bob Smith", email="bob@example.com")

session.add_all([user1, user2])
session.commit()  # Commit so users get their IDs assigned

# Create 3 products
product1 = Product(name="Laptop", price=999.99)
product2 = Product(name="Headphones", price=49.99)
product3 = Product(name="Keyboard", price=79.99)

session.add_all([product1, product2, product3])
session.commit()

# Create 4 orders with varying quantities and shipment statuses
order1 = Order(user_id=user1.id, product_id=product1.id, quantity=1, shipped=True)
order2 = Order(user_id=user1.id, product_id=product2.id, quantity=2, shipped=False)
order3 = Order(user_id=user2.id, product_id=product3.id, quantity=3, shipped=True)
order4 = Order(user_id=user2.id, product_id=product1.id, quantity=1, shipped=False)

session.add_all([order1, order2, order3, order4])
session.commit()
print("Sample data inserted.\n")


# --------------------------------------------------
# Part 5: Queries, Update, and Delete
# --------------------------------------------------

# 5a. Query all users
print("=== All Users ===")
for u in session.query(User).all():
    print(f"  {u}")

# 5b. Query all products
print("\n=== All Products ===")
for p in session.query(Product).all():
    print(f"  {p}")

# 5c. Query all orders showing user name and product name
print("\n=== All Orders ===")
for o in session.query(Order).all():
    print(f"  Order #{o.id}: {o.user.name} ordered {o.quantity}x {o.product.name} "
          f"(shipped={o.shipped})")

# 5d. Update a product price (change Headphones price to 39.99)
headphones = session.query(Product).filter_by(name="Headphones").first()
old_price = headphones.price
headphones.price = 39.99
session.commit()
print(f"\n=== Price Update ===")
print(f"  Updated '{headphones.name}' price: ${old_price} -> ${headphones.price}")

# 5e. Delete a user by ID (delete user with id=2)
user_to_delete = session.query(User).filter_by(id=2).first()
if user_to_delete:
    # Remove that user's orders first to avoid foreign key issues
    session.query(Order).filter_by(user_id=user_to_delete.id).delete()
    print(f"\n=== Delete User ===")
    print(f"  Deleting user: {user_to_delete}")
    session.delete(user_to_delete)
    session.commit()
    print("  User deleted successfully.")


# --------------------------------------------------
# Part 6 (Bonus): Advanced Queries
# --------------------------------------------------

# 6a. Query all unshipped orders
print("\n=== Unshipped Orders ===")
unshipped = session.query(Order).filter_by(shipped=False).all()
if unshipped:
    for o in unshipped:
        print(f"  Order #{o.id}: {o.user.name} - {o.product.name} (qty={o.quantity})")
else:
    print("  No unshipped orders found.")

# 6b. Count total orders per user
print("\n=== Total Orders Per User ===")
order_counts = (
    session.query(User.name, func.count(Order.id).label("total_orders"))
    .join(Order)
    .group_by(User.id)
    .all()
)
for name, count in order_counts:
    print(f"  {name}: {count} order(s)")

# Clean up the session
session.close()
print("\nDone!")
