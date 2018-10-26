#!/usr/bin/python3

import requests
import json
import sys

myusername = '1'
mypassword = '1'
idxwatt = '22'
idxkwh = '21'
solaxsite = 'www.solaxcloud.com:6080'
tokenurl = 'http://'+solaxsite+'/proxy//login/login?password='+mypassword+'&userName='+myusername+'&userType=5'
mysiteurl = 'http://'+solaxsite+'/proxy//mysite/mySite'

try:
  tokendata = requests.post(tokenurl).json()
  tokenanduser= {
    'tokenId': tokendata['result']['tokenId'],
    'userId': tokendata['result']['userId'],
    }
  try:
    mysitedata = requests.post(mysiteurl, data=tokenanduser).json()
    alldataurl = 'http://'+solaxsite+'/proxy//mysite/getInverterInfo?siteId='+str(mysitedata['result'][0]['siteId'])+'&tokenId='+tokendata['result']['tokenId']
    try:
      alldata = requests.post(alldataurl).json()
      ##Watt
      current = alldata['result'][0]['pv1Current']+alldata['result'][0]['pv2Current']
      domurl = 'http://192.168.0.157:80/json.htm?type=command&param=udevice&nvalue=0&idx='+idxwatt+'&svalue='+str(current)
      requests.get(domurl)
    except requests.exceptions.RequestException as e:
      print(e)
      sys.exit(1)
  except requests.exceptions.RequestException as e:
    print(e)
    sys.exit(1)
except requests.exceptions.RequestException as e:
  print(e)
  sys.exit(1)
