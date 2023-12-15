import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from faker import Faker

# Load environment variables
load_dotenv()

# Database connection settings from environment variables
DB_HOST = os.getenv("DB_HOST")
DB_DATABASE = os.getenv("DB_DATABASE")
DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")

# Connection string
connect_args={'ssl':{'fake_flag_to_enable_tls': True}}
conn_string = (
    f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/{DB_DATABASE}")
engine = create_engine(conn_string)
fake = Faker()

def insert_fake_data(engine, num_records=100):
    # Start a connection
    with engine.connect() as connection:
        
        # Insert fake data into patient_info
        for _ in range(num_records):
            first_name = fake.first_name()
            last_name = fake.last_name()
            date_of_birth = fake.date_of_birth(minimum_age=10, maximum_age=90)
            
            # Use text() to represent the SQL string
            query = text(
                """
                INSERT INTO patient_info (first_name, last_name, date_of_birth)
                VALUES (:first_name, :last_name, :date_of_birth)
                """
            )
            
            # Execute the query with bound parameters
            connection.execute(query, {
                'first_name': first_name,
                'last_name': last_name,
                'date_of_birth': date_of_birth
            })

        # Commit the changes
        connection.commit()
    print('It worked')    
insert_fake_data(engine, 100)
    