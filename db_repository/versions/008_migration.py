from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
user = Table('user', pre_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('nickname', String),
    Column('email', String),
    Column('role', SmallInteger),
    Column('password', String),
)

user = Table('user', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String(length=64)),
    Column('email', String(length=120)),
    Column('password', String(length=15)),
    Column('role', SmallInteger, default=ColumnDefault(0)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['user'].columns['nickname'].drop()
    post_meta.tables['user'].columns['name'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['user'].columns['nickname'].create()
    post_meta.tables['user'].columns['name'].drop()
