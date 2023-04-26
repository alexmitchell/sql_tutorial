#!/usr/bin/env python3

import sqlalchemy as sqla

engine = sqla.create_engine("sqlite+pysqlite:///:memory:", echo=True)

################################################################################
# Table objects
################################################################################

# The MetaData object stores references to all the table objects in the DB
# Generally there is only one MetaData object per application, but more than 
# one is allowed too. Tables in a MetaData collection can be refer to Tables in 
# other collections, but it's generally a bad idea. Best practice is that 
# Tables that are related should be in the same MetaData object. 
metadata_obj = sqla.MetaData()

user_table = sqla.Table(
        "user_account",
        metadata_obj,
        sqla.Column("id", sqla.Integer, primary_key=True),
        sqla.Column("name", sqla.String(30)),
        sqla.Column("fullname", sqla.String()),
        )

address_table = sqla.Table(
        "address",
        metadata_obj,
        sqla.Column('id', sqla.Integer, primary_key=True),
        sqla.Column('user_id', sqla.ForeignKey('user_account.id'), nullable=False),
        sqla.Column('email_address', sqla.String, nullable=False)
        )

metadata_obj.create_all(engine)

################################################################################
# (ORM) Declarative Base
################################################################################

class Base(sqla.DeclarativeBase):
    # This class maps Python objects to SQL DB. It creates its own MetaData 
    # object too by default
    pass

Base.metdadata

