from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

_default_session_factory = sessionmaker(
    bind=create_engine('mysql://user:password@server'),
)