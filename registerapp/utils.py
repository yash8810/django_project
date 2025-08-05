from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
import logging
from dotenv import load_dotenv
import os
from argon2 import PasswordHasher  # Import the PasswordHasher from argon2-cffi

# Load environment variables from the .env file
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Load the DATABASE_URL from environment variables
DATABASE_URL = os.getenv('DATABASE_URL')

if not DATABASE_URL:
    raise ValueError("Error: DATABASE_URL is not set in the environment variables.")

# Database connection setup
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

# Automatically reflect the tables in the database
metadata = MetaData()
metadata.reflect(bind=engine)

# Initialize the PasswordHasher for Argon2
ph = PasswordHasher()

# Function to insert a record into any table
def insert_record(table_name, data):
    if not table_name or not data:
        return "Error: Missing table name or data."

    try:
        # Reflect the table from the database
        table = metadata.tables.get(table_name)
        if table is None:
            return f"Error: Table '{table_name}' not found in the database."

        # Create the insert statement dynamically
        insert_stmt = table.insert().values(**data)
        logger.debug(f"Insert Statement: {insert_stmt}")  # Log the insert statement

        # Create a session and execute the insert statement
        SessionLocal = Session()
        with SessionLocal.begin():  # Ensure the session is committed and closed correctly
            result = SessionLocal.execute(insert_stmt)
            logger.debug(f"Insert Result: {result.inserted_primary_key}")  # Log inserted primary key

        return f"Record inserted successfully with ID: {result.inserted_primary_key}"

    except IntegrityError as e:
        logger.error(f"Integrity error: {str(e)}")  # Log specific integrity errors like duplicate key
        return f"Integrity error: {str(e)}"
    
    except SQLAlchemyError as e:
        logger.error(f"SQLAlchemy error: {str(e)}")  # Log the general SQLAlchemy error
        return f"Database error: {str(e)}"
    
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")  # Log any other unexpected errors
        return f"An unexpected error occurred: {str(e)}"

