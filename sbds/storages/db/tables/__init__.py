# -*- coding: utf-8 -*-
from sqlalchemy import MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


metadata = MetaData()
Base = declarative_base(metadata=metadata)
Session = sessionmaker()

from .core import Block
from .synthesized import Account
from .synthesized import PostAndComment
from .synthesized import Post
from .synthesized import Comment
from .synthesized import Link
from .synthesized import Image
from .synthesized import Tag

from .tx import TxBase
from .tx import TxAccountCreate
from .tx import TxAccountRecover
from .tx import TxAccountUpdate
from .tx import TxAccountWitnessProxy
from .tx import TxAccountWitnessVote
from .tx import TxComment
from .tx import TxCommentsOption
from .tx import TxConvert
from .tx import TxCustom
from .tx import TxDeleteComment
from .tx import TxFeed
from .tx import TxLimitOrder
from .tx import TxPow
from .tx import TxTransfer
from .tx import TxVote
from .tx import TxWithdrawVestingRoute
from .tx import TxWithdraw
from .tx import TxWitnessUpdate

import sbds.storages.db.events


def init_tables(engine, metadata, checkfirst=True):
    """Create any missing tables on the database"""
    metadata.create_all(bind=engine, checkfirst=checkfirst)


def reset_tables(engine, metadata):
    """Drop and then create tables on the database"""

    # use unadulterated MetaData to avoid errors due to ORM classes
    # being inconsistent with existing tables
    from sqlalchemy import MetaData
    _metadata = MetaData()
    _metadata.reflect(bind=engine)
    _metadata.drop_all(bind=engine)

    # use ORM clases to define tables to create
    init_tables(engine, metadata)

def test_connection(engine):
    from sqlalchemy import MetaData
    _metadata = MetaData()

    try:
        _metadata.reflect(bind=engine)
        table_count = len(_metadata.tables)
        url = engine.url
        return url, table_count
    except Exception as e:
        return False, e

