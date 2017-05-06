from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
engine = create_engine('postgres:///sthief')
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()
metadata = MetaData(engine)

target = Table('furtum',metadata,
	Column('id',Integer,autoincrement=True,primary_key = True),
	Column('href',Text),
	Column('name',Text),
	Column('touch',Boolean),
	Column('createdate',DateTime(timezone=True)))

metadata.create_all(engine)
conn = engine.connect()

class Furtum(Base):
	__tablename__ = 'furtum'
	id = Column(Integer, primary_key=True)
	name = Column(Text)
	href = Column(Text)
	touch = Column(Boolean)
	createdate = Column(DateTime(timezone=True), default=func.now())