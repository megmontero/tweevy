from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
news = Table('news', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('url', String(length=400)),
    Column('image', String(length=400)),
    Column('rank', Integer),
    Column('title', String(length=200)),
    Column('tags', String(length=400)),
    Column('desc', String(length=400)),
    Column('interval', String(length=20)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['news'].columns['interval'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['news'].columns['interval'].drop()
