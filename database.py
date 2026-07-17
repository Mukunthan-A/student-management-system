import psycopg2
from psycopg2.extensions import connection
from config import DATABASE

_connection: connection = None


def connect() -> connection:
    """Establishes and returns a connection to the PostgreSQL database.

    If a connection already exists and is open, it returns the existing one.
    """
    global _connection

    if _connection is None or _connection.closed != 0:
        try:
            _connection = psycopg2.connect(**DATABASE)
        except psycopg2.DatabaseError as e:
            print(f"Error connecting to the database: {e}")
            raise e

    return _connection


def close() -> None:
    """Closes the active database connection if it is open."""
    global _connection

    if _connection is not None and _connection.closed == 0:
        _connection.close()
        _connection = None 