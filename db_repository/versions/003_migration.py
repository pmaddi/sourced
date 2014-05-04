from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
post = Table('post', pre_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('body', String),
    Column('timestamp', DateTime),
    Column('user_id', Integer),
)

role = Table('role', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String(length=80)),
    Column('description', String(length=255)),
)

roles_users = Table('roles_users', post_meta,
    Column('user_id', Integer),
    Column('role_id', Integer),
)

user = Table('user', pre_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('nickname', String),
    Column('email', String),
    Column('role', SmallInteger),
)

user = Table('user', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('email', String(length=255)),
    Column('password', String(length=255)),
    Column('active', Boolean),
    Column('confirmed_at', DateTime),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['post'].drop()
    post_meta.tables['role'].create()
    post_meta.tables['roles_users'].create()
    pre_meta.tables['user'].columns['nickname'].drop()
    pre_meta.tables['user'].columns['role'].drop()
    post_meta.tables['user'].columns['active'].create()
    post_meta.tables['user'].columns['confirmed_at'].create()
    post_meta.tables['user'].columns['password'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['post'].create()
    post_meta.tables['role'].drop()
    post_meta.tables['roles_users'].drop()
    pre_meta.tables['user'].columns['nickname'].create()
    pre_meta.tables['user'].columns['role'].create()
    post_meta.tables['user'].columns['active'].drop()
    post_meta.tables['user'].columns['confirmed_at'].drop()
    post_meta.tables['user'].columns['password'].drop()
