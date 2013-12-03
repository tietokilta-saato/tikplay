import sqlalchemy
from json import loads


with open('tikplay.conf', 'r') as conf:
    configuration = loads(conf.readlines())

db = sqlalchemy.create_engine(configuration['db'])
Base = sqlalchemy.ext.declarative.declarative_base()
db.session = sqlalchemy.orm.sessionmaker(bind=db)()
