from db import *
import requests as rq
from bs4 import BeautifulSoup as bs
from multiprocessing.dummy import Pool as ThreadPool

global Foe
Address = 'http://www.4icu.org'
Target = 'http://www.4icu.org/cn/chinese-universities.htm'
Strongbox = 'strongbox/'
Foe = 0
tp = ThreadPool(10)

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
	return session.query(Furtum).filter(Furtum.touch == False).limit(10).all()

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