# Domoticz-SolaxCloud-Plugin

SolaxCloud Scraper as a cronjob.. No idea how to make a plugin for domoticz yet

Make virtual sensors and add them to the script

https://i.imgur.com/NhlCXFl.png

===============================================================================================================

- Edit solax.py with the credentials for your domoticz installation.
- Create virtual sensors for the data you want to retain. (see solax.py and the screenshot for the idx's)
- Place script in a directory ie: /opt/solax/
- Make a cronjob with sudo crontab -e 
- add the following to the crontab: */1 * * * * /usr/bin/python3 /opt/solax/solax.py

Now every minute data wil be drawn from solaxcloud to Domoticz.
