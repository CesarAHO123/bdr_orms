from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy.exc
import sqlite3

# SQLAlchemy setup
Base = sqlalchemy.orm.declarative_base()
engine = create_engine('sqlite:///example.db')  # Use SQLite as the database engine
# Define a User model using SQLAlchemy
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)

# Create tables
Base.metadata.create_all(engine)

# SQLAlchemy Query Example
def sqlalchemy_example():
    Session = sessionmaker(bind=engine)
    session = Session()
    # Create a new user
    new_user = User(name="Alice")
    session.add(new_user)
    session.commit()
    # Retrieve a user
    retrieved_user = session.query(User).filter_by(name="Alice").first()
    print("SQLAlchemy: Retrieved User -", retrieved_user.name)
    # Update user name
    retrieved_user.name = "Alicia"
    session.commit()
    updated_user = session.query(User).filter_by(name="Alicia").first()
    print("SQLAlchemy: Updated User -", updated_user.name)
    session.close()

# Raw SQL Query Example
def raw_sql_query_example():
    conn = sqlite3.connect('example.db')
    cursor=conn.cursor()
    # Create a new user using raw SQL
    try:
        cursor.execute("INSERT INTO users (name) VALUES ('Bob')")
    except sqlalchemy.exc.IntegrityError:
        print("Raw SQL: User with this name already exists")
    # Retrieve a user using raw SQL
    result = cursor.execute("SELECT * FROM users WHERE name = 'Bob'")
    retrieved_user = result.fetchone()
    if retrieved_user:
        print("Raw SQL: Retrieved User -", retrieved_user[1])
    # Update user name using raw SQL
    cursor.execute("UPDATE users SET name = 'Robert' WHERE name = 'Bob'")
    updated_result = cursor.execute("SELECT * FROM users WHERE name = 'Robert'")
    updated_user = updated_result.fetchone()
    if updated_user:
        print("Raw SQL: Updated User -", updated_user[1])
    conn.close()

if __name__ == "__main__":
    sqlalchemy_example() 
    raw_sql_query_example() 