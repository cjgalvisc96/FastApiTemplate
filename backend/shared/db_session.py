from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

_default_session_factory = sessionmaker(
    bind=create_engine('mysql://user:password@server'),
)
