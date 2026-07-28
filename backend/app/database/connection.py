# Builtin
import os
from urllib.parse import urlparse

# Third-party
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def db_connection():
    # Railway provides DATABASE_URL
    database_url = os.getenv("DATABASE_URL")
    
    if database_url:
        # Parse the URL
        result = urlparse(database_url)
        
        return psycopg2.connect(
            host=result.hostname,
            dbname=result.path[1:],
            user=result.username,
            password=result.password,
            port=result.port
        )
    else:
        # Fallback to individual variables (for local development)
        host = os.getenv("DB_HOST")
        dbname = os.getenv("DB_NAME")
        user = os.getenv("DB_USER")
        password = os.getenv("DB_PASSWORD")
        port = os.getenv("DB_PORT")
        
        return psycopg2.connect(
            host=host,
            dbname=dbname,
            user=user,
            password=password,
            port=port,
        )
