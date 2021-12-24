import os

from sqlalchemy import (
    Column,
    DateTime,
    Integer,
    MetaData,
    String,
    Table,
    create_engine
)
from sqlalchemy.sql import func

from databases import Database

DATABASE_URL = os.getenv("postgresql://riwhsptnyormqw:4968cefd626fdb958741475384c319b99d3628734b182c9c2f50077a2f87d4e5@ec2-3-248-87-6.eu-west-1.compute.amazonaws.com:5432/d4q71til8sh0an")

# SQLAlchemy
engine = create_engine("postgresql://riwhsptnyormqw:4968cefd626fdb958741475384c319b99d3628734b182c9c2f50077a2f87d4e5@ec2-3-248-87-6.eu-west-1.compute.amazonaws.com:5432/d4q71til8sh0an")
metadata = MetaData()
notes = Table(
    "notes",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("title", String(50)),
    Column("description", String(50)),
    Column("created_date", DateTime, default=func.now(), nullable=False),
)

# databases query builder
database = Database(DATABASE_URL)