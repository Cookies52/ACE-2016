import pywikibot
import pywikibot
import requests
import json
import csv
import time
import sys
import os
import login
from pywikibot import data
################################################################################################################################################################################
##ACE2016 MassMessage List Script
##Author: Mdann52
##Licence: https://creativecommons.org/licenses/by-sa/4.0/
#This is a basic script, based on pywikibot, that takes a list of 'spamlists', and queues MassMessages to them. It will only send a new batch if the existing queue is below 50.
#
#
#Any questions, please send them to https://en.wikipedia.org/wiki/User talk:Mdann52
#################################################################################################################################################################################

def getToken():
    api_call = pywikibot.data.api.Request(action="query", meta="tokens") #query API for token
    csrf = api_call.submit()["query"]["tokens"]["csrftoken"]
    if(csrf == "+\\"): #blank token, shows editing logged out (which we don't want!)
       sys.exit("Error - Not logged in, or no token retrieved!")
    else: #return valid token
        return csrf


site = pywikibot.Site('en', 'wikipedia')

stats_query = pywikibot.data.api.Request(site=site, action='query', meta='siteinfo', siprop='statistics')
queued_messages = stats_query.submit()['query']['statistics']['queued-massmessages']

index = 2 #page 1 is for testing reasons only


while index < 40:
    if queued_message < 50:
        #then send!

        ##Define what page to get from
        list_source = "User:Mdann52 bot/spamlist/" + index

        ##define subject etc.
        message_subject = "[[WP:ACE2016|ArbCom Elections 2016]]: Voting now open!"

        #API query to send
        send_message = pywikibot.data.api.Request(site=site, action='massmessage', spamlist=list_source, subject=message_subject, message="{{subst:Wikipedia:Arbitration Committee Elections December 2016/MassMessage}}", token = getToken())
        response = send_message.submit()
        print(response)
    else:
        #wait 60s before retrying
        time.sleep(60)
    

