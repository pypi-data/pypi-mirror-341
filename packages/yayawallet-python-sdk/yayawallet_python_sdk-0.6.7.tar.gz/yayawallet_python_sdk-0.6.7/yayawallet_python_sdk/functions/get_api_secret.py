import psycopg2
from psycopg2 import pool
import os

class DatabaseConnection:
    _connection_pool = None

    @classmethod
    def initialize_pool(cls):
        if cls._connection_pool is None:
            try:
                cls._connection_pool = psycopg2.pool.SimpleConnectionPool(
                    minconn=1,
                    maxconn=10,
                    host=os.environ.get('POSTGRES_HOST'),
                    database=os.environ.get('POSTGRES_DB'),
                    user=os.environ.get('POSTGRES_USER'),
                    password=os.environ.get('POSTGRES_PASSWORD'),
                    port=os.environ.get('POSTGRES_PORT')
                )
            except Exception as e:
                print(f"Error creating connection pool: {e}")
                raise

    @classmethod
    def get_connection(cls):
        if cls._connection_pool is None:
            cls.initialize_pool()
        return cls._connection_pool.getconn()

    @classmethod
    def return_connection(cls, connection):
        cls._connection_pool.putconn(connection)

    @classmethod
    def close_all_connections(cls):
        if cls._connection_pool:
            cls._connection_pool.closeall()

def get_api_secret(api_key=None):
    connection = None
    try:
        connection = DatabaseConnection.get_connection()
        cursor = connection.cursor()

        if api_key is None:
            # Get default API secret
            query = """
            SELECT secret FROM api_key 
            WHERE is_default = TRUE 
            LIMIT 1
            """
            cursor.execute(query)
        else:
            # Get specific API secret
            query = """
            SELECT secret FROM api_key 
            WHERE key = %s
            LIMIT 1
            """
            cursor.execute(query, (api_key,))
        
        result = cursor.fetchone()
        return result[0] if result else None

    except Exception as e:
        print(f"Error fetching API secret: {e}")
        return None
    finally:
        if connection:
            DatabaseConnection.return_connection(connection)