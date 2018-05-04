# -*- coding: utf-8 -*-

from sqlalchemy import BigInteger
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKeyConstraint
from sqlalchemy import Index
from sqlalchemy import Integer
from sqlalchemy import Numeric
from sqlalchemy import SmallInteger
from sqlalchemy import Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import text

from ... import Base
from ....enums import asset_types_enum
from ....enums import operation_types_enum
from ....field_handlers import accounts_field
from ....field_handlers import amount_field
from ....field_handlers import amount_symbol_field


class FillConvertRequestVirtualOperation(Base):
    """

    Steem Blockchain Example
    ======================




    """

    __tablename__ = 'sbds_op_virtual_fill_convert_requests'
    __table_args__ = (
        ForeignKeyConstraint(
            ['owner'], ['sbds_meta_accounts.name'],
            deferrable=True,
            initially='DEFERRED',
            use_alter=True),

        # not yet supported Index('block_num', 'transaction_num',
        # 'operation_num','op_virtual', unique=True),
        Index(
            'ix_sbds_sbds_op_virtual_fill_convert_requests_unique',
            'block_num',
            'transaction_num',
            'operation_num',
            text("MD5('raw')"),
            unique=True),
        Index(
            'ix_sbds_op_virtual_fill_convert_requests_accounts',
            'accounts',
            postgresql_using='gin',
            postgresql_ops={'accounts': 'jsonb_path_ops'}))

    _id = Column(BigInteger, autoincrement=True, primary_key=True)
    block_num = Column(Integer, nullable=False)
    transaction_num = Column(SmallInteger, nullable=False)
    operation_num = Column(SmallInteger, nullable=False)
    timestamp = Column(DateTime(timezone=False))
    trx_id = Column(Text, nullable=False)
    accounts = Column(JSONB)
    raw = Column(JSONB)

    owner = Column(Text, nullable=True)  # steem_type:account_name_type
    requestid = Column(Numeric)  # steem_type:uint32_t
    amount_in = Column(Numeric(20, 6), nullable=False)  # steem_type:asset
    amount_in_symbol = Column(
        asset_types_enum, nullable=False)  # steem_type:asset
    amount_out = Column(Numeric(20, 6), nullable=False)  # steem_type:asset
    amount_out_symbol = Column(
        asset_types_enum, nullable=False)  # steem_type:asset
    operation_type = Column(operation_types_enum, nullable=False, default='')

    _fields = dict(
        amount_in=lambda x: amount_field(x.get('amount_in'), num_func=float),  # steem_type:asset
        amount_in_symbol=lambda x: amount_symbol_field(x.get('amount_in')),  # steem_type:asset
        amount_out=lambda x: amount_field(x.get('amount_out'), num_func=float),  # steem_type:asset
        amount_out_symbol=lambda x: amount_symbol_field(x.get('amount_out')),  # steem_type:asset
        accounts=lambda x: accounts_field(x, 'fill_convert_request'),
    )

    _account_fields = frozenset([
        'owner',
    ])
