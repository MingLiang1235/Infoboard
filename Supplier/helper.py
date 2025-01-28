#!/usr/bin/python3
# -*- coding:utf-8 -*-
#=====================================================================
#   FileName:  helper.py 
#   Purpose:  Utilities helping other programmes.
#   Version:  1.0
#   Author:  Jishan                  
#   Email:  unicoder@sohu.com
#   Date:  2024-08-04 23:36  Modify-Date:  2024-08-04 23:36
#=====================================================================

from random import seed, choice
from datetime import datetime
from configobj import ConfigObj
from enum import Enum
#import multiprocessing
#import multiprocessing.pool
#from basicFIFO import FIFO
#from . import NoDaemonProcess

id = 0
alphabet = ['1','2','3','4','5','6','7','8','9','10','20','30','40','50']
configFile = "config.ini"  # test: "test.ini"
server_ip = '127.0.0.1'
server_port = 10001

#class NoDaemonProcess(multiprocessing.Process):
	# make 'daemon' attribute always return False

#	def _get_daemon(self):
#		return False
#	def _set_daemon(self, value):
#		pass
#	daemon = property(_get_daemon, _set_daemon)

# We sub-class multiprocessing.pool.Pool instead of multiprocessing.Pool
# because the latter is only a wrapper function, not a proper class.	
#class NoDaemonProcessPool(multiprocessing.pool.Pool):  # Error:  3.12.6 CAN NOT RUN IT.(Maybe other version also can't)
#	def __init__(self, processes = 1):
#		super(NoDaemonProcessPool, self).__init__()
#	Process = NoDaemonProcess

# ------------------------------------------------------------
# Class my Exception
# ------------------------------------------------------------
class CantGetMsg(Exception):
	def __init__(self, message):
		self.message = message
 
	def __str__(self):
		return self.message

class CantGetCorrectMsgType(Exception):
	def __init__(self, message):
		self.message = message
 
	def __str__(self):
		return self.message

class ConnectIssue(Exception):
	def __init__(self, message):
		self.message = message
 
	def __str__(self):
		return self.message
		
class RegistError(Exception):
	def __init__(self, message):
		self.message = message
 
	def __str__(self):
		return self.message
 
# # 使用自定义异常的例子
# def divide(x, y):
#		if y == 0:
#			raise CantGetMsgLen("除数不能为0")
#		return x / y

# ------------------------------------------------------------
# Singleton
# ------------------------------------------------------------
def singleton(cls):
	instances = {}
	def get_instance(*args, **kwargs):
		if cls not in instances:
			instances[cls] = cls(*args, **kwargs)
		return instances[cls]
	return get_instance

#@singleton                    # Pool的多进程Singleton是不好使的。
#class FIFOCache(FIFO):
#	def __init__(self):
#		#self.Regist = []
#		pass

# ------------------------------------------------------------
# Enume
# ------------------------------------------------------------
class HostType(Enum):
    SUPPLIER = 1  # HostType.SUPPLIER.name == 'SUPPLIER'
    CONSUMER = 2  # HostType.CONSUMER.value == 2

class DataType(Enum):
	PCState = 1
	Recoder = 2
	Weather = 3
	Other = 4

class ConsumerComm(Enum):
	PreGetDestHosts = 101
	GetData = 102
	ReAskInit = 103

class ConsumerErro(Enum):
	CantGetHost = 404
	
class SupplierErro(Enum):
	CantService = 502
# ------------------------------------------------------------
# Config file
# ------------------------------------------------------------
def initConfig(sections):
	config = ConfigObj(configFile, encoding='UTF8')
	for sect in sections:
		config[sect] = {}

	config.write()

def setConfig(section, name, value):
	config = ConfigObj(configFile, encoding='UTF8')
	if section in config:
		config[section][name] = value
	else:
		config[section] = {}
		config[section][name] = value
	config.write()

def getConfig(section, name):
	config = ConfigObj(configFile, encoding='UTF8')
	
	value = None
	if (section in config) and (name in config[section]):
		value = config[section][name]
	return value

def getHostFromConfig():  # Return is like {'name':'hostname', 'roles':['role1','role2']}
	config = ConfigObj(configFile, encoding='UTF8')
	
	dic = {}
	section = 'Host'
	names = ('name', 'roles')
	for name in names:
		if (section in config) and (name in config[section]):
			if name == 'name':
				dic['name'] = config[section][name]
			elif name == 'roles':
				# rs = [r for r in config[section][name].split(',') if r != '']  # No need it. ConfigObj automatic parse it to list.
				dic['roles'] = config[section][name]

	if 'name' in dic:
		print("Host: " + str(dic))
		return dic
	else:
		print("Can't get Host.")
		return None
		
def getDestHostFromConfig():  # Return is like {'name':'destHostName'}
	config = ConfigObj(configFile, encoding='UTF8')
	dic = {}
	section = 'DEST_Host'
	name = 'supplier'
	if (section in config) and (name in config[section]):
		dic['name'] = config[section][name]
		print('DEST_Host:', str(dic))
		return dic
	else:
		print("Can't get DEST_Host.")
		return None

# ------------------------------------------------------------
# out: dict:  dic['url'] string, dic['port'] int. Or None.
# ------------------------------------------------------------
def getConnectString():
	config = ConfigObj(configFile, encoding='UTF8')
	print("In getConnectStr, below:")
	dic = {}
	section = 'CONNECT'
	if (section in config) and ('url' in config[section]) and ('port' in config[section]):
		dic['url'] = config[section]['url']	
		dic['port'] = int(config[section]['port'])
		print("Getted connectStr.")
		return dic
	else:
		print("Can not get connectStr.")
		return None

def getHostFromList():
	f = open("HostID.lst", "r")
	line = f.readline()
	#lst = line.split(',')
	print("Hosts: " + str(line.strip()))
	return line.strip()

def setHosts():
	pass

#----------
# sections = ["Host", "DEST_Host"]
# initConfig(sections)
#----------


def genValue(length=20):
	''' This is for test. '''
	global alphabet
	seed(datetime.now().microsecond)
	string = '0'
	string = choice(alphabet)
	# for i in range(length):
	#  	string = choice(alphabet)
	return string

def getNewId():
	global id
	id += 1
	return id



	# TODO:   enume  INIT class (MSG class)
