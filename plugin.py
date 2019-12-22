#!/usr/bin/python3

import requests
import sys

##edit these entries
domoticzip = ''
myusername = ''
mypassword = ''

#dummies in domoticz
idxdcwatt = '27'
idxdcwatt1 = '28'
idxdcwatt2 = '29'
idxvoltage1 = '25'
idxvoltage2 = '26'
idxCur1 = '30'
idxCur2 = '31'
idxyieldtoday = '32'
idxpac1 = '33'
idxpac2 = '34'
idxpac3 = '35'
idxpactot = '36'
idxtemp = '37'

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
       domurl = 'http://'+domoticzip+':80/json.htm?type=command&param=udevice&nvalue=0&idx='+idxCur1+'&svalue='+str(alldata['result'][0]['pv1Current'])
       requests.get(domurl)
       ##pv2Current in A
       domurl = 'http://'+domoticzip+':80/json.htm?type=command&param=udevice&nvalue=0&idx='+idxCur2+'&svalue='+str(alldata['result'][0]['pv2Current'])
       requests.get(domurl)
       ##powerdc1+powerdc2 in Watt
       domurl = 'http://'+domoticzip+':80/json.htm?type=command&param=udevice&nvalue=0&idx='+idxdcwatt+'&svalue='+str(alldata['result'][0]['powerdc1']+alldata['result'][0]['powerdc2'])
       requests.get(domurl)
       ##powerdc1 in Watt
       domurl = 'http://'+domoticzip+':80/json.htm?type=command&param=udevice&nvalue=0&idx='+idxdcwatt1+'&svalue='+str(alldata['result'][0]['powerdc1'])
       requests.get(domurl)
       ##powerdc2 in Watt
       domurl = 'http://'+domoticzip+':80/json.htm?type=command&param=udevice&nvalue=0&idx='+idxdcwatt2+'&svalue='+str(alldata['result'][0]['powerdc2'])
       requests.get(domurl)
       ##pv1Voltage in Volts
       domurl = 'http://'+domoticzip+':80/json.htm?type=command&param=udevice&nvalue=0&idx='+idxvoltage1+'&svalue='+str(alldata['result'][0]['pv1Voltage'])
       requests.get(domurl)
       ##pv2Voltage in Volts
       domurl = 'http://'+domoticzip+':80/json.htm?type=command&param=udevice&nvalue=0&idx='+idxvoltage2+'&svalue='+str(alldata['result'][0]['pv2Voltage'])
       requests.get(domurl)
       ##totalYield in KWH (use counter)
       domurl = 'http://'+domoticzip+':80/json.htm?type=command&param=udevice&nvalue=0&idx='+idxyieldtoday+'&svalue='+str(alldata['result'][0]['totalYield'])
       requests.get(domurl)
       ##Phase1 return
       domurl = 'http://'+domoticzip+':80/json.htm?type=command&param=udevice&nvalue=0&idx='+idxpac1+'&svalue='+str(alldata['result'][0]['pac1'])
       requests.get(domurl)
       ##Phase2 return
       domurl = 'http://'+domoticzip+':80/json.htm?type=command&param=udevice&nvalue=0&idx='+idxpac2+'&svalue='+str(alldata['result'][0]['pac2'])
       requests.get(domurl)
       ##Phase3 return
       domurl = 'http://'+domoticzip+':80/json.htm?type=command&param=udevice&nvalue=0&idx='+idxpac3+'&svalue='+str(alldata['result'][0]['pac3'])
       requests.get(domurl)
       ##Gridreturn total
       domurl = 'http://'+domoticzip+':80/json.htm?type=command&param=udevice&nvalue=0&idx='+idxpactot+'&svalue='+str(alldata['result'][0]['gridPower'])
       requests.get(domurl)
       ##temp
       domurl = 'http://'+domoticzip+':80/json.htm?type=command&param=udevice&nvalue=0&idx='+idxtemp+'&svalue='+str(alldata['result'][0]['temperature'])
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

