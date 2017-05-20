#encoding:utf8
from db import *
from mdb import *
import requests as rq
from bs4 import BeautifulSoup as bs
from multiprocessing.dummy import Pool as ThreadPool
import logging
import imghdr
import os,re

Address = 'http://www.4icu.org'
Target = Address+'/cn/chinese-universities.htm'
Strongbox = 'strongbox/'
tp = ThreadPool(10)
Logobox = 'logobox/'
Website_img_box = 'website_img/'


def belt_jar():
	jar = p_session.query(Furtum).filter(Furtum.touch == False).limit(10).all()
	for i,v in enumerate(jar):
		v.mdb_session = m_s_l[i]
	return jar

def rain_name(pro):
	return pro.find(itemprop="alternateName").get_text()

def rain_jar(sen,pro):
	return sen.query(Uni).filter(Uni.name == pro).first()

def log(pro):
	logger =logging.getLogger("rain")
	logger.info(pro)

def rain_english_name(pro):
	return pro.find("h1",itemprop="name").get_text()

def rain_logo(pro,name):
	l = pro.find(itemprop="logo").get('src')
	t = name.replace(' ','-').lower()+"-logo"+GetFileNameAndExt(l)[1]
	img_down(Address+l,Logobox,t)
	return t

def rain_address(pro):
	return pro.find(itemprop="address").select(".borderless tr td")[0].get_text().replace("\n"," ")

def rain_phone(pro):
	return pro.find(itemprop="telephone").get_text()

def rain_fax(pro):
	return pro.find(itemprop="faxNumber").get_text()

def rain_website_url(pro):
	return pro.find(itemprop="url").get('href')

def rain_website_image(pro,name):
	l = pro.select(".borderless .img-responsive")[0].get('src')
	t = name.replace(' ','-').lower()+"-website"+GetFileNameAndExt(l)[1]
	img_down(Address+l,Website_img_box,t)
	return t

def rain_acronym(pro):
	return pro.find('abbr').get_text()

def rain_country_rank(pro):
	return pro.select(".center-block .text-right")[0].get_text()

def rain_world_rank(pro):
	return pro.select(".center-block .text-right")[1].get_text()

def rain_wikipedia_url(pro):
	t = pro.find_all(itemprop="sameAs",rel="nofollow")
	for i in t:
		if 'wikipedia' in i.get('href'):
			return i.get('href')
	return None

def rain_overview(pro):
	return pro.find(itemprop="description").get_text()

def img_down(pro,add,name):
	r = rq.get(pro,stream=True)
	with open(add+name,'wb') as f:
		for i in r.iter_content(chunk_size=1024):
			if i:
				f.write(i)
				f.flush()
		f.close()

def GetFileNameAndExt(filename):
	 (filepath,tempfilename) = os.path.split(filename);
	 (shotname,extension) = os.path.splitext(tempfilename);
	 return shotname,extension

def rain_shot(pro):
	try:
		with open(Strongbox+pro.name+".html") as f:
			r = f.read()
	except Exception as e:
		log(e)
		print('第{}条数据出错'.format(pro.id))
	else:
		b = bs(r,'lxml')
		try:
			cn = rain_name(b)
			print('正在修改{}'.format(cn))
			tar = rain_jar(pro.mdb_session,cn)
			print('{}数据查询成功'.format(cn))
		except Exception as e:
			print(e)
			print('{}.不存在'.format(cn))
		else:
			try:
				if tar:
					tar.english_name = rain_english_name(b)
					tar.overview = rain_overview(b)
					tar.logo = rain_logo(b,tar.english_name)
					tar.address = rain_address(b)
					tar.phone = rain_phone(b)
					tar.fax = rain_fax(b)
					tar.website_url = rain_website_url(b)
					tar.website_image = rain_website_image(b,tar.english_name)
					try:
						tar.acronym = rain_acronym(b)
					except Exception as e:
						print("无简写")
					tar.country_rank = rain_country_rank(b)
					tar.world_rank = rain_world_rank(b)
					tar.wikipedia_url = rain_wikipedia_url(b)
					print('{}.修改成功'.format(cn))
			except Exception as e:
				print(e)
				log(e)
				print('{}修改失败'.format(cn))
			else:
				pass
			finally:
				pass
		finally:
			pro.touch = True
	finally:
		if tar:
			pro.mdb_session.flush()
			pro.mdb_session.commit()

def rain():
	while belt_jar():
		tp.map(rain_shot,belt_jar())
		p_session.flush()
		p_session.commit()


rain()

