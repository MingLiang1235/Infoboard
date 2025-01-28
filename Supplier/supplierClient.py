#!/usr/bin/python3
# -*- coding:utf-8 -*-
#=====================================================================
#   FileName:  supplierClient.py 
#   Purpose:  Socket Supplier Client Windows Version (More complex than client 1).
#   Version:  0.0.1
#   Author:  Jishan                  
#   Email:  unicoder@sohu.com
#   Date:  2024-12-01 23:36  Modify-Date:  2024-12-01 23:36
#=====================================================================
import socket
import struct
from time import sleep
from helper import genValue, getHostFromConfig, getConnectString, DataType
import clientMeter

index = 1

def get_func(func, arg):  # 函数式编程
	return func(arg)

def msg_init(host):
	# GROUP_NO 一台机器可以有多个NO，表示不同种类的信息。TYPE是该种类的信息的说明。DESC则是让人类能理解的说明。
	# 本信息是用于向服务器注册的。
	#msg = "|SUPPLIER|INIT|GROUP_NO|1|GROUP_TYPE|CPU|cpu|mem|tem|"  
	msg = "|SUPPLIER|INIT|" + host + "|1|cpu|mem|tem|"  # msgtype is 1.(SUPPLIER)
	return msg

def msg_data(msg_type):
	global index
	str1 = index
	sleep(1)
	str2 = index
	sleep(1)
	str3 = index
	msg = "|DATA|" + msg_type + "|" + str(str1) + "|" + str(str2) + "|" + str(str3) + "|"
	index += 1
	return msg 
	
def msg_data_test(arg):
	str1 = genValue()
	sleep(1)
	str2 = genValue()
	sleep(1)
	str3 = genValue()
	msg = "|DATA|" + arg + "|" + str1 + "|" + str2 + "|" + str3 + "|"
	return msg 

def talk(clientSocket, client_msg):
	if not client_msg:
		return
	msg_len = struct.pack('i', len(client_msg.encode('utf-8')))  # bit stream, i为有符号整数，4个字节。所以信息长度不可超出4个字节。
	print(msg_len)
	clientSocket.send(msg_len + client_msg.encode("utf-8"))
	# recv data:
	server_msg = clientSocket.recv(1024).decode('utf-8')
	print("Msg from server is : %s" % server_msg)
	
def start_client():

	host_attr = getHostFromConfig()

	if not host_attr:
		return -1


	# 客户端如果连接着时服务端关闭了，则客户端再次发信息会被“远程主机强迫关闭”，
	# 如果客户端试图连接一个未开启服务端的主机，则“目标主机积极拒绝，无法连接”。
	# Config clientSocket
	clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	# connection require
	# clientSocket.connect(('127.0.0.1', 10001))
	dicConnectStr = getConnectString()
	clientSocket.connect((dicConnectStr['url'], dicConnectStr['port']))
	

	talk(clientSocket, msg_init(host_attr['name']))

	# talk(clientSocket, '|COMSUMER|INIT|GROUP_NO|1|GROUP_TYPE|CPU|cpu|mem|tem|')  # tEST  when case is |comsumer|.

	# talk(clientSocket, '|COMSUMER|DATA|1|2|3|')


	# Below selfs versa will communication by this connect looply:
	while True: 
		sleep(5)
		
		msg_type = '1'  # class help.DataType.PCState.value = 1
		# client_msg = msg_data('1')
		client_msg = "|DATA|" + msg_type + "|" + clientMeter.invoke_meter()

		if not client_msg:  # null message will hang up server versus.
			continue
		# send data
		talk(clientSocket, client_msg)
		
		#client_msg = get_msg_to_send_func(get_msg_to_send_client, 'NoArg')


		# msg_len = struct.pack('i', len(client_msg.encode('utf-8')))  # bit stream
		# print(msg_len)
		# #msg_len = str(len(client_msg.encode('utf-8'))).encode('utf-8')
		# #clientSocket.send(msg_len)
		# clientSocket.send(msg_len + client_msg.encode("utf-8"))
		
		# # recv data
		# server_msg = clientSocket.recv(1024).decode('utf-8')
		# print("Msg from server is : %s" % server_msg)

	# close clientSocket
	clientSocket.close()

if __name__ == '__main__':
	start_client()
