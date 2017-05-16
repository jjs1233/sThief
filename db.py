from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base

p_Base = declarative_base()
p_engine = create_engine('postgres:///sthief')
p_Session = scoped_session(sessionmaker(bind=p_engine))
p_session = p_Session()
p_Session.remove()
p_s_l = []
for i in range(10):
	p_s_l.append(p_Session())
	p_Session.remove()

class Furtum(p_Base):
	__tablename__ = 'furtum'
	id = Column(Integer, primary_key=True)
	name = Column(Text)
	href = Column(Text)
	touch = Column(Boolean)
	logo_url = Column(Text)
	website_img_url = Column(Text)
	createdate = Column(DateTime(timezone=True), default=func.now())