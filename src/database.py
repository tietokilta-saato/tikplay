import sqlalchemy
import json


with open('tikplay.conf', 'r') as conf:
    configuration = json.loads(conf.readlines())

db = sqlalchemy.create_engine(configuration['db'])
Base = sqlalchemy.ext.declarative.declarative_base()
db.session = sqlalchemy.orm.sessionmaker(bind=db)()
