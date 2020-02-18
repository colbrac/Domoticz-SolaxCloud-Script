#!/usr/bin/python3

import requests
import sys

##edit these entries
domoticzip = '' # format: IP:PORT
myusername = '' # for Solax site
mypassword = '' # for Solax site

#dummies in domoticz, fill in the ID's as listed per Virtual sensor in Domoticz
fields = {
'pv1Voltage': 24, 
'pv1Current': 25, 
'powerdc1': 32, 
'gridPower': 33, 
'vac1': 27, 
'iac1': 28, 
'fac1': 34, 
'temperature': 23, 
'totalYield': 31, 
'todayYield': 30
} 

##Solaxstuff do not touch!##
solaxsite = 'www.solaxcloud.com:6080'
tokenurl = 'http://'+solaxsite+'/proxy//login/login?password='+mypassword+'&userName='+myusername+'&userType=5'
mysiteurl = 'http://'+solaxsite+'/proxy//mysite/mySite'

#Login and get token and userid
try:
 if not myusername:
  print ("Username is empty")
  sys.exit(1)
 elif not mypassword:
  print ("Password is empty")
  sys.exit(1)
 else:
#  print ("You entered: ["+myusername+"]")
#  print ("You entered: ["+mypassword+"]")
  tokendata = requests.post(tokenurl).json()
  if not tokendata['success']:
    print(tokendata['exception'])
    sys.exit(1)
  else:
   tokenanduser= {
     'tokenId': tokendata['result']['tokenId'],
     'userId': tokendata['result']['userId'],
    }
  #use token and userid to get siteid
  try:
    mysitedata = requests.post(mysiteurl, data=tokenanduser).json()
#    print(mysitedata)
    if not mysitedata['success']:
     print(mysitedata['exception'])
     sys.exit(1)
    else:
     alldataurl = 'http://'+solaxsite+'/proxy//mysite/getInverterInfo?siteId='+str(mysitedata['result'][0]['siteId'])+'&tokenId='+tokendata['result']['tokenId']
    #use site id and token, get the data, and post it to domoticz
    try:
      alldata = requests.post(alldataurl).json()
      if not mysitedata['success']:
       print(mysitedata['exception'])
       sys.exit(1)
      else:
       # Push all values to Domoticz
       for key, domidx in fields.items():
           value = alldata['result'][0][key]
           domurl = 'http://'+domoticzip+'/json.htm?type=command&param=udevice&nvalue=0&idx={}&svalue={}'.format(domidx, value)
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

