from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base

m_Base = declarative_base()
m_engine = create_engine('mysql+pymysql://root:w;@localhost:3306/sthief?charset=utf8&use_unicode=0',pool_recycle=3600)
m_Session = scoped_session(sessionmaker(bind=m_engine))
m_s_l = []
for i in range(10):
	m_s_l.append(m_Session())
	m_Session.remove()

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
	overview = Column(Text)
	logo = Column(Text)
	address = Column(Text)
	phone = Column(Text)
	fax = Column(Text)
	website_url = Column(Text)
	website_image = Column(Text)
	acronym = Column(Text)
	country_rank = Column(Text)
	world_rank = Column(Text)
	wikipedia_url = Column(Text)
