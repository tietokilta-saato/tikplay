import sqlalchemy
import sqlalchemy.ext.declarative
import sqlalchemy.orm

# TODO: Convert to class, dependency injection for configuration
configuration = {"db": "sqlite://"}

db = sqlalchemy.create_engine(configuration['db'])
Base = sqlalchemy.ext.declarative.declarative_base()
session = sqlalchemy.orm.sessionmaker(bind=db)()
