#!/usr/bin/python3

import requests
import sys
import time

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
       # Check if the latest data on the Solax Cloud server is recent. 
       # If older than 5 minutes, do not push data to Domoticz, so no stale data is recorded in Domoticz during night time.
       # This assumes Solax Cloud data is updated every 5 minutes and a crontab is running this script every 5 minutes as well!
       lastupdatetime = alldata['result'][0]['lastUpdateTimes']
       print("Last update time: %s"%lastupdatetime)
       if time.mktime(time.strptime(lastupdatetime, '%Y-%m-%d %H:%M:%S'))-time.time()<-300: # older than 5 minutes                                                                                                        $
           print("Last update time more than 5 minutes ago: %s"%lastupdatetime)
           sys.exit(0)
       # Push all values to Domoticz
       for key, domidx in fields.items():
           value = alldata['result'][0][key]
           if 'Yield' in key:
               value = "%.0f"%(1000*float(value)) # convert kWh counters to Wh
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

