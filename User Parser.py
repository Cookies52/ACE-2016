import pywikibot
import requests
import json
import time
import sys
import time
from calendar import timegm
from pywikibot import data

site = pywikibot.Site('en', 'wikipedia')

def getToken():
    api_call = pywikibot.data.api.Request(action="query", meta="tokens", site=site) #query API for token
    csrf = api_call.submit()["query"]["tokens"]["csrftoken"]
    if(csrf == "+\\"): #blank token, shows editing logged out (which we don't want!)
       sys.exit("Error - Not logged in, or no token retrieved!")
    else: #return valid token
        return csrf
    
def checkLast(username):
    r = pywikibot.data.api.Request(
                site=site,
                action = "query",
                list = ["usercontribs"],
                uclimit = 1,
                ucend = '2016-11-27T00:00:00Z', # midnight 27/11/2016
                ucprop="timestamp",
                ucuser = username
                ).submit()
    print(r['query']['usercontribs'])
    if len(r["query"]["usercontribs"]) > 0:
        return True
    else:
        return False
    
with open("user_lst.txt", encoding="utf8") as fp:
    working_list = []
    return_list = []
    for user in fp:
        if len(working_list) == 50:
            ##send
            print(working_list)
            user_qry = pywikibot.data.api.Request(
                site=site,
                action = "query",
                list = ["users"],
                usprop = ["registration","editcount"],
                ususers = working_list
            )

            ret = user_qry.submit()
            
            print(user_qry)
            print(ret)
            
            for u in ret['query']['users']:
                print(u)
                try:
                    if u['editcount'] >= 150 and timegm(time.strptime(u['registration'], "%Y-%m-%dT%H:%M:%SZ")) <= 20171128000000:
                        if checkLast(u['name']):
                            return_list.append(u['name'])
                except KeyError:
                    pass
            working_list = []
            outfile = open("out.txt", mode="a", encoding="utf8")
            for n in return_list:
                print(n)
                outfile.write("{{#target:User:"+n+"}}\n")
            print(return_list)
            outfile.close()
            sys.exit(0)
        else:
            if user != ' ' and user != '':
                working_list.append(user.strip("\n"))
            
            
            
