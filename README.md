# Domoticz-SolaxCloud-Plugin

SolaxCloud Scraper as a cronjob.

Make virtual sensors and add them to the script

https://i.imgur.com/NhlCXFl.png

===============================================================================


- Edit solax.py with the credentials for your domoticz installation.  
  domoticzip = '' (the ip domoticz is using)  
  myusername = '' (the username for the solax coud)  
  mypassword = '' (the password for the solax cloud)  
- Create virtual sensors for the data you want to retain. (see solax.py and the screenshot for the idx's)  
  
  Dummies in domoticz shortlist (number = idx in domoticz)  
  idxdcwatt = '27'      (dummy watt total (group1+group2))  
  idxdcwatt1 = '28'     (dummy watt group1)  
  idxdcwatt2 = '29'     (dummy watt group2)  
  idxvoltage1 = '25'    (dummy voltage group1)  
  idxvoltage2 = '26'    (dummy voltage group2)  
  idxCur1 = '30'        (dummy current group1)  
  idxCur2 = '31'        (dummy current group2)  
  idxyieldtoday = '32'  (dummy kwh meter total yield (use rfxmeter))  
  idxpac1 = '33'        (dummy phase1 return watt)  
  idxpac2 = '34'        (dummy phase2 return watt)  
  idxpac3 = '35'        (dummy phase3 return watt)  
  idxpactot = '36'      (dummy all phases watt)  
  idxtemp = '37'        (dummy inverter temperature)  

- Place script in a directory ie: /opt/solax/  
- Make a cronjob with sudo crontab -e   
- add the following to the crontab: */1 * * * * /usr/bin/python3 /opt/solax/solax.py  

Now every minute data wil be drawn from solaxcloud to Domoticz.  
