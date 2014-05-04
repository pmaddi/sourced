from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
role = Table('role', pre_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String),
    Column('description', String),
)

roles_users = Table('roles_users', pre_meta,
    Column('user_id', Integer),
    Column('role_id', Integer),
)

user = Table('user', pre_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('email', String),
    Column('active', Boolean),
    Column('confirmed_at', DateTime),
    Column('password', String),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['role'].drop()
    pre_meta.tables['roles_users'].drop()
    pre_meta.tables['user'].drop()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['role'].create()
    pre_meta.tables['roles_users'].create()
    pre_meta.tables['user'].create()
