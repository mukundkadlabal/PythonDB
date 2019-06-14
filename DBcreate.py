# -*- coding: utf-8 -*-
"""
Created on Fri Jun 15 17:23:00 2019

@author: 91961
"""

from sqlalchemy import Column,Integer, String, Float,Date, Boolean, create_engine, exc, orm, MetaData, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
Base=declarative_base()
class Login(Base):
	__tablename__="login"
	user=Column(String(10), primary_key=True)
	password=Column(String(10))
	isfaculty=Column(Integer)
	def __init__(self,user,password,isfaculty):
		self.user= user
		self.password= password
		self.isfaculty= isfaculty
	def __str__(self):
		return self.user+"|"+self.password+"|"+str(self.isfaculty)

class Faculty(Base):
	__tablename__="faculty"
	cname=Column(String(10), primary_key=True)
	fac=Column(String(10))
	def __init__(self,cname,fac):
		self.cname= cname
		self.fac= fac
	def __str__(self):
		return self.cname+"|"+self.fac


class Perc(Base):
	__tablename__="perc"
	studname=Column(String(10), primary_key=True)
	course=Column(String(10), primary_key=True)
	perc=Column(String(10))
	def __init__(self,studname,course,perc):
		self.studname= studname
		self.course= course
		self.perc= perc
	def __str__(self):
		return self.studname+"|"+self.course+"|"+str(self.perc)

class Stud(Base):
	__tablename__="stud"
	studname=Column(String(10), primary_key=True)
	courses=Column(String(10), primary_key=True)	
	def __init__(self,studname,courses):
		self.studname= studname
		self.courses= courses
	def __str__(self):
		return self.studname+"|"+self.courses


class Attend(Base):
	__tablename__="attend"
	studname=Column(String(10), primary_key=True)
	course=Column(String(10), primary_key=True)	
	date=Column(Date, primary_key=True)
	present=Column(Integer)
	def __init__(self,studname,courses,date,present):
		self.studname= studname
		self.course= courses
		self.date= date
		self.present= present
	def __str__(self):
		return self.studname+"|"+self.course+"|"+str(self.date)+"|"+str(self.present)


def addlogin(name,password,isfaculty):
	engine=create_engine("sqlite:///as1.db")
	engine.connect()
	session= sessionmaker(bind=engine)()
	userrow = Login(name,password,isfaculty)
	session.add(userrow)

	session.commit()


def displogin():
	engine=create_engine("sqlite:///as1.db")
	engine.connect()
	session= sessionmaker(bind=engine)()
	result=[r for r in session.query(Login).all()]
	list1=[]
	for i in result:
		list1.append((i.user,i.password,i.isfaculty))
	return list1


def check(uname,password):
	engine=create_engine("sqlite:///as1.db")
	engine.connect()
	session= sessionmaker(bind=engine)()
	result=[r for r in session.query(Login).all()]
	list1=[]
	usernotthere=True
	match=False	
	for i in result:
		if i.user==uname:
			usernottthere=False
		if i.user==uname and i.password==password:
			match=True
	if(match==True and usernottthere==False):
		return 0
	elif(usernotthere==False and match==False):
		return 2
	else:
		return 1
				

def getstudforcourses(cname):
	engine=create_engine("sqlite:///as1.db")
	engine.connect()
	session= sessionmaker(bind=engine)()
	result=[r for r in session.query(Stud).all()]
	list1=[]
	for i in result:
		if(i.courses==cname):
			list1.append(i.studname)
	return list1


def inserperc(studname,course,perc):
	engine=create_engine("sqlite:///as1.db")
	engine.connect()
	session= sessionmaker(bind=engine)()
	print(studname,course,perc)	
	result=[r for r in session.query(Perc).all()]
	presentss=False	
	for i in result:
		if(i.studname==studname and i.course==course):
			i.perc=perc
			try:
				session.commit()
			except:
				print("Try Again")
				session.rollback()			
			presentss=True
	if(presentss==False):
		userrow = Perc(studname,course,perc)
		session.add(userrow)
		try:
			session.commit()
		except:
			print("Try Again")
			session.rollback()
	
from sqlalchemy.sql import func
def getper(uname,course):
	engine=create_engine("sqlite:///as1.db")
	engine.connect()
	session= sessionmaker(bind=engine)()

	result=[r for r in session.query(Attend).all()]
	list1=[]
	att=0
	for i in result:
		if(i.course==course):
			list1.append(i.date)
	for i in result:
			if(i.studname==uname and i.course==course and i.present==1):
				att+=1	
	maxim=max(list1)
	minim=min(list1)
	subdays=(maxim-minim).days+1
	return att/subdays

def getpercrows(uname):
	engine=create_engine("sqlite:///as1.db")
	engine.connect()
	session= sessionmaker(bind=engine)()
	result=[r for r in session.query(Perc).all()]
	list1=[]
	for i in result:
		if(i.studname==uname):
			list1.append((i.studname,i.course,i.perc))
	return list1


def dispfaculty():
	engine=create_engine("sqlite:///as1.db")
	engine.connect()
	session= sessionmaker(bind=engine)()

	result=[r for r in session.query(Faculty).all()]
	for i in result:
		print(i)
def displogpar(name,password):
	engine=create_engine("sqlite:///as1.db")
	engine.connect()
	session= sessionmaker(bind=engine)()
	result=[r for r in session.query(Login).all()]
	for i in result:
		if(i.user==name and i.password==password):
			return(i.user,i.password,i.isfaculty)

def markattendance(name,courses,date):
	engine=create_engine("sqlite:///as1.db")
	engine.connect()
	session= sessionmaker(bind=engine)()
	result=[r for r in session.query(Attend).all()]
	presentss=False
	for i in result:
		if(i.studname==name and i.course==courses and i.date==date):
			if(i.present==0):
				i.present=1
			else:
				i.present=0
			try:
				session.commit()
			except:
				print("Try Again")
				session.rollback()			
			presentss=True
	if(presentss==False):
		userrow = Attend(name,courses,date,1)
		session.add(userrow)
		try:
			session.commit()
		except:
			print("Try Again")
			session.rollback()
			

def checkattend(name,course,date):
	engine=create_engine("sqlite:///as1.db")
	engine.connect()
	session= sessionmaker(bind=engine)()
	result=[r for r in session.query(Attend).all()]
	list1=[]
	for i in result:
		if(i.studname==name and i.course==course and i.date==date):
			return(i.present)
	return 0



def getcoursesfac(fac):
	engine=create_engine("sqlite:///as1.db")
	engine.connect()
	session= sessionmaker(bind=engine)()
	result=[r for r in session.query(Faculty).all()]
	list1=[]
	for i in result:
		if(i.fac==fac):
			list1.append(i.cname)
	return list1

def getallcourses():
	engine=create_engine("sqlite:///as1.db")
	engine.connect()
	session= sessionmaker(bind=engine)()
	result=[r for r in session.query(Faculty).all()]
	list1=[]
	for i in result:
		list1.append(i.cname)
	return list1


def addcoursefac(cname,fac):
	engine=create_engine("sqlite:///as1.db")
	engine.connect()
	session= sessionmaker(bind=engine)()
	userrow = Faculty(cname,fac)
	session.add(userrow)
	try:
		session.commit()
	except:
		print("Try Again")
		session.rollback()



def addcoursestud(studname,courses):
	engine=create_engine("sqlite:///as1.db")
	engine.connect()
	session= sessionmaker(bind=engine)()
	userrow = Stud(studname,courses)
	session.add(userrow)
	try:
		session.commit()
	except:
		print("Try Again")
		session.rollback()
