#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Test for SQLAlchemy, Alembic, sqlalchemy-continuum
"""
from __future__ import unicode_literals, division, absolute_import, \
    print_function
from sqlalchemy import Table, Column, Integer, String, Boolean, DateTime,\
    Sequence, ForeignKey, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy_continuum import make_versioned

make_versioned()

Base = declarative_base(metadata=MetaData(schema='continuum'))


customer_roles_table = Table('customer_roles', Base.metadata,
                             Column('customerid', Integer,
                                    ForeignKey('customers.id'),
                                    primary_key=True),
                             Column('roleid', Integer,
                                    ForeignKey('roles.id'),
                                    primary_key=True))


class Customer(Base):
    """Customer account."""
    __versioned__ = {}
    __tablename__ = 'customers'

    id = Column(Integer, Sequence('customers_id_seq'), primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    _password = Column('password', String, nullable=False)
    active = Column(Boolean, default=True)
    deleted = Column(Boolean, default=False)
    roles = relationship('Role', secondary=customer_roles_table)


class Role(Base):
    """Role definition."""
    __versioned__ = {}
    __tablename__ = 'roles'

    id = Column(Integer, Sequence('roles_id_seq'), primary_key=True)
    name = Column(String, nullable=False)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        if self.id:
            return "<Role({0}, {1})>".format(self.id, self.name)
        else:
            return "<Role({0})>".format(self.name)

import sqlalchemy as sa
sa.orm.configure_mappers()