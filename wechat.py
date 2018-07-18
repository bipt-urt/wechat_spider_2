#coding:utf-8
import subprocess 
import re
from urllib import request
from urllib import parse
import os
import time
import sys
import csv
from http import cookiejar
import json
import jsonpath
import random
import qrcode_terminal
import os.path
import hashlib

friend_RemarkName = {}
friend_NickName = {}
user_groups = []

e_headers = ['名字','备注名字','签名','性别','省份','城市']
headers = {
	'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0'
}
try:

	url = 'https://login.wx.qq.com/jslogin?appid=wx782c26e4c19acffb&redirect_uri=https://login.weixin.qq.com/cgi-bin/mmwebwx-bin/webwxnewloginpage&fun=new&lang=zh_CN&_=1530078655980'
	html = request.urlopen(url)
	mybytes = html.read()
	mybytes = str(mybytes,encoding = "utf-8")
	pm = re.findall(r"\"\w+==\"", mybytes)
	uuid = pm[0]
	uuid = uuid[1:-1]


	qrcode_terminal.draw('https://login.weixin.qq.com/l/'+ uuid)
	print('-'*12 + "请扫码登录" + '-'*12)
	while(1):
		urlogin = "https://login.wx2.qq.com/cgi-bin/mmwebwx-bin/login?loginicon=true&uuid=" + uuid + "&tip=0&r=-1224738251&_=1530233069169"
		html_Login = request.urlopen(urlogin)
		loginCode = re.findall(r"\d\d\d", html_Login.read().decode('utf-8'))
		if loginCode[0] == '201':
			print('-'*12 + "扫码成功"+ '-'*12)
			print('-'*10 +"请在手机点击登录" + '-'*9)
		elif loginCode[0] == '200':
			print('-'*12 +"登录成功" + '-'*12)
			break
	urlogin = "https://login.wx2.qq.com/cgi-bin/mmwebwx-bin/login?loginicon=true&uuid=" + uuid + "&tip=0&r=-1224738251&_=1530233069169"
	html_Login = request.urlopen(urlogin)
	loginURL = html_Login.read().decode('utf-8')[38:-2]			

	cookie = cookiejar.CookieJar()
	#利用urllib.request库的HTTPCookieProcessor对象来创建cookie处理器,也就CookieHandler
	handler=request.HTTPCookieProcessor(cookie)
	#通过CookieHandler创建opener
	opener = request.build_opener(handler)
	#此处的open方法打开网页
	opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0'),
		('Host', 'wx.qq.com'),
		('Accept', 'application/json, text/plain, */*'),
		('Accept-Language', 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2'),
		('Referer', 'https://wx.qq.com/'),
		('DNT', '1')]
	request.install_opener(opener)
	
	response1 = request.urlopen(loginURL)

	html_Login_all = request.urlopen(loginURL+'&fun=new')
	html_Login_text = html_Login_all.read().decode('utf-8')
	html_Login_skey = re.findall(r'<skey>.*</skey>',html_Login_text)
	html_Login_skey = html_Login_skey[0][6:-7]
	html_Login_ticket = re.findall(r"<pass_ticket>.*</pass_ticket>", html_Login_text)
	html_Login_ticket = html_Login_ticket[0][13:-14]
	wxsid = re.findall(r"<wxsid>.*</wxsid>", html_Login_text)
	wxsid = wxsid[0][7:-8]
	uin = re.findall(r"<wxuin>.*</wxuin>", html_Login_text)
	uin = uin[0][7:-8]

	urlFreiend = "https://wx2.qq.com/cgi-bin/mmwebwx-bin/webwxgetcontact?r=1530085335160&seq=0&skey=" + html_Login_skey
	html_Login = request.Request(urlFreiend)

	
	get_response = request.urlopen(html_Login)

	FreJson = json.loads(get_response.read().decode('utf-8'))
	get_comment = jsonpath.jsonpath(FreJson,"$.MemberList[*]")
	for i in range(len(get_comment)):
		list1 = []
		#print(get_comment[i]["AttrStatus"][])
		if (get_comment[i]["AttrStatus"] > 0):
			
			friend_RemarkName[get_comment[i]["RemarkName"]] = get_comment[i]["UserName"]
			friend_NickName[get_comment[i]["NickName"]] = get_comment[i]["UserName"]

			get_comment[i]["NickName"] = re.sub(r'<span class=".*"></span>','', get_comment[i]["NickName"])
			if ('&amp;' in get_comment[i]["NickName"]):
				get_comment[i]["NickName"]=get_comment[i]["NickName"].replace('&amp;', "&")
			list1.append(get_comment[i]["NickName"])
			list1.append(get_comment[i]["RemarkName"])
			list1.append(get_comment[i]["Signature"])

			if (get_comment[i]["Sex"] == 1):
				list1.append('男')
			elif (get_comment[i]["Sex"] == 2):
				list1.append('女')
			else:
				list1.append('其他')

			list1.append(get_comment[i]["Province"] + get_comment[i]["City"])
			with open('friends.csv','a+') as file:
				file_csv = csv.writer(file)
				file_csv.writerow(list1)
		
	#获取群组
		URL_groups = 'https://wx2.qq.com/cgi-bin/mmwebwx-bin/webwxbatchgetcontact?type=ex&r=1530753509208&lang=zh_CN&pass_ticket=' + html_Login_ticket
	#获取用户名字
	userUrl = "https://wx2.qq.com/cgi-bin/mmwebwx-bin/webwxinit?r=-1591857714&lang=zh_CN&pass_ticket=" + html_Login_ticket
	value_sd = {
		"BaseRequest":{
			"Uin":uin,
			"Sid":wxsid,
			"Skey":html_Login_skey,
			"DeviceID":"e594131889876990"
		}
	}
	data = json.dumps(value_sd)
	data1=bytes(data,'utf8').replace(b' ',b'')
	
	html_user1 = request.Request(userUrl,data1)
	get_response = request.urlopen(html_user1)
	user_info = jsonpath.jsonpath(json.loads(get_response.read().decode('utf-8')),"$.User[*]")
	user_name = user_info[1]
	user_sig = user_info[2]
	subprocess.call("clear")
	print(user_info[2] + '已登录')
	
	
	#发送信息
	print('-----------')
	sendMURl = "https://wx2.qq.com/cgi-bin/mmwebwx-bin/webwxsendmsg?lang=zh_CN&pass_ticket=" + html_Login_ticket
	Id = random.random()
	send_to_friends_name = input("请输入联系人名字:")
	if send_to_friends_name in friend_RemarkName:
		flag = 1
		ToUserName = friend_RemarkName[send_to_friends_name]
	elif send_to_friends_name in friend_NickName:
		flag = 1
		ToUserName = friend_NickName[send_to_friends_name]
	else:
		flag = 0
		print('没找到此联系人')

	if (flag):
		print(ToUserName)
		mass = input("请输入发送的消息：")
		ClientId = str(Id)[2:] + '1'
		values = {
			"BaseRequest":{
				"Uin":uin,
				"Sid":wxsid,
				"Skey":html_Login_skey,
				"DeviceID":"e999788905479540"},
				"Msg":{
					"Type":1,
					"Content":mass,
					"FromUserName":user_name,
					"ToUserName":ToUserName,
					"LocalID":ClientId,
					"ClientMsgId":ClientId
					},
				"Scene":0
			}
		send_data = json.dumps(values,ensure_ascii=False)
		send_bytes = bytes(send_data,'utf-8').replace(b' ',b'')
		
		html_send = request.Request(sendMURl,send_bytes)
		get_response = request.urlopen(html_send)


	#查看消息
	check_message = 'https://webpush.wx2.qq.com/cgi-bin/mmwebwx-bin/synccheck?r=1530687540372&skey=' + html_Login_skey + '&sid=' + wxsid +'&uin=' + uin + '&deviceid=e220664692368841&synckey=1_675110709%7C2_675111211%7C3_675110715%7C11_675110554%7C201_1530687488%7C1000_1530680522%7C1001_1530680594&_=1530687399698'
	get_message = request.urlopen(check_message)
	response = get_message.read().decode('utf-8')
	response = response[-4:-1]
	if(response == '"0"'):
		print('暂无新消息')
	elif(response == '"2"'):
		print('hehe')

	#发送图片
	send_image_temp = 'https://file.wx2.qq.com/cgi-bin/mmwebwx-bin/webwxuploadmedia?f=json'
	wxMessage = input("图片路径:\n")
	if os.path.isfile(wxMessage) == False:
		print("发送图片不存在")
	else:
		pass


except:
	print("网络链接失败")

