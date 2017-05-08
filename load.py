from db import *
from mdb import *
import requests as rq
from bs4 import BeautifulSoup as bs
from multiprocessing.dummy import Pool as ThreadPool

global Foe
Address = 'http://www.4icu.org'
Target = 'http://www.4icu.org/cn/chinese-universities.htm'
Strongbox = 'strongbox/'
Foe = 0
Iit = 0
tp = ThreadPool(20)

def furtum_jar(a,b):
	return Furtum(
		href = a,
		name = b,
		touch = False
		)

def add(a):
	session.add(a)
	session.commit()

def belt_loading():
	r = rq.get(Target)
	b = bs(r.text,'lxml')
	t = b.select('.table-hover .lead')
	for pro in t:
		h = Address + pro.get('href')
		n = pro.get_text().lower().replace(' ','-')
		bullet = furtum_jar(h,n)
		add(bullet)

def belt_jar():
	return session.query(Furtum).filter(Furtum.touch == False).limit(20).all()

def shot(pro):
	global Foe
	n = pro.name
	h = pro.href
	try:
		r = rq.get(h)
	except Exception as e:
		print('第{}条数据出错'.format(pro.id))
	else:
		with open(Strongbox+n+'.html','w') as f:
			f.write(r.text)
		print('第{}条数据已经成功爬取'.format(pro.id))
		orderly(pro)
	finally:
		Foe +=1
		if Foe == 10:
			session.flush()
			session.commit()
			Foe = 0

def orderly(pro):
	pro.touch = True

def fire():
	while len(session.query(Furtum).filter(Furtum.touch == False).all()) > 0:
		tp.map(shot, belt_jar())
	session.flush()
	session.commit()


def rain_name(pro):
	return pro.find(itemprop="alternateName").get_text()

def rain_english_name(pro):
	return pro.find("h1",itemprop="name").get_text()

def rain_jar(pro):
	return m_session.query(Uni).filter(Uni.name == pro).first()

def rain_shot(pro):
	global Foe
	global Iit
	try:
		r = rq.get(pro.href)
	except Exception as e:
		print('第{}条数据出错'.format(pro.id))
	else:
		b = bs(r.text,'lxml')
		try:
			cn = rain_name(b)
			print('正在修改{}'.format(cn))
			tar = rain_jar(cn)
			print('{}数据查询成功'.format(cn))
		except Exception as e:
			print(e)
			print('{}.不存在'.format(cn))
		else:
			try:
				print(tar)
				if tar:
					tar.english_name = rain_english_name(b)
					print('{}.修改成功'.format(cn))
			except Exception as e:
				print('{}.english name修改失败'.format(cn))
			else:
				pass
			finally:
				pass
		finally:
			orderly(pro)
	finally:
		Foe += 1
		Iit += 1
		print('{}条数据正常\n'.format(Iit))
		if Foe == 10:
			session.flush()
			session.commit()
			if tar:
				m_session.flush()
				m_session.commit()
			Foe = 0

def rain():
	while len(session.query(Furtum).filter(Furtum.touch == False).all()) > 0:
		tp.map(rain_shot,belt_jar())
	session.commit()
	m_session.commit()

rain()
# a = m_session.query(Uni).filter(Uni.name == '安徽文达信息工程学院').first()
# if a:
# 	print('fuck')
# b = m_session.query(Uni).filter(Uni.name == '安徽三联学院').first()