from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base

m_Base = declarative_base()
m_engine = create_engine('mysql+pymysql://root:w;@localhost:3306/sthief?charset=utf8&use_unicode=0',pool_size=100)
m_Session = sessionmaker()
m_Session.configure(bind=m_engine)
m_session = m_Session()

class Uni(m_Base):
	__tablename__ = 'universities'
	id = Column(Integer, primary_key=True)
	code = Column(Integer)
	name = Column(Text)
	english_name = Column(Text)
	goverment = Column(Text)
	city = Column(Text)
	level = Column(Text)
	note = Column(Text)