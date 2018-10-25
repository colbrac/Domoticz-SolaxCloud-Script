import requests

myusername = '123'
mypassword = '123'
solaxsite = 'www.solaxcloud.com:6080'
tokenurl = 'http://'+solaxsite+'/proxy//login/login?password='+mypassword+'&userName='+myusername+'&userType=5'
mysiteurl = 'http://'+solaxsite+'/proxy//mysite/mySite'

tokendata = requests.post(tokenurl).json()
if tokendata['success']:
  #print("It Works.. My tokenID is "+tokendata['result']['tokenId'])
  #print("It Works.. My userID is "+tokendata['result']['userId'])
  tokenanduser= {
    'tokenId': tokendata['result']['tokenId'],
    'userId': tokendata['result']['userId'],
    }
  mysitedata = requests.post(mysiteurl, data=tokenanduser).json()
  if mysitedata['success']:
    #deze result bestaat uit een array (zie json resultaat)
    #print("It Works... My siteID is "+str(mysitedata['result'][0]['siteId']))
    alldataurl = 'http://'+solaxsite+'/proxy//mysite/getInverterInfo?siteId='+str(mysitedata['result'][0]['siteId'])+'&tokenId='+tokendata['result']['tokenId']
    alldata = requests.post(alldataurl).json()
    if alldata['success']:
      print("It Works... now eat my dataaaaaaaa")
      print(alldata)
    else:
     print("Invalid siteid")
  else:
    print("Invalid token or user")
else:
  print("Invalid credentials")


