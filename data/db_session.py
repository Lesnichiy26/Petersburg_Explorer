import os

import sqlalchemy as sa
import sqlalchemy.ext.declarative as dec
import sqlalchemy.orm as orm
from sqlalchemy.orm import Session

SqlAlchemyBase = dec.declarative_base()

__factory = None


def global_init():
    global __factory

    if __factory:
        return

    if 'DATABASE_URL' in os.environ:
        database_url = os.environ['DATABASE_URL']

    print(f"Подключение к базе данных по адресу {database_url}")

    engine = sa.create_engine(database_url,
                              connect_args={'sslmode': 'require'},
                              pool_size=20,
                              echo=True)

    __factory = orm.sessionmaker(bind=engine)

    SqlAlchemyBase.metadata.create_all(engine)


def create_session() -> Session:
    global __factory
    return __factory()
