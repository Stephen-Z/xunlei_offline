# -*- coding: utf-8 -*-
import urllib
import requests
import Cookie
from PIL import Image
from StringIO import StringIO
import json
import time
import ast
import os

class Offline(object):
    """docstring for Offline"""
    def __init__(self):
        self.verifynum=1;
        cookiefile=open('cookies.txt','rb')
        cookiestr=str(cookiefile.read())
        cookiefile.close()
        cookiestr=cookiestr.replace('\n','')
        cookiestr=cookiestr.replace(';','\n')
        cookiefile2=open('cookiesf.txt','wb')
        cookiefile2.write(cookiestr)
        cookiefile2.close()
        localcookie=open('cookiesf.txt','rb')
        self.cookiedict={}
        for line in localcookie:
            k, v = line.strip().split('=')
            self.cookiedict[k.strip()] = v.strip()
        localcookie.close()
        self.userid=self.cookiedict['userid']
        self.gdriveid=self.cookiedict['gdriveid']

    def gettime(self):
        t=time.time()
        t=t*1000
        t='%i' %t
        return t

    def getverifycode(self):
        verifycodeurl='http://verify2.xunlei.com/image'
        if(self.verifynum==1):
            self.verifynum=2
        else:
            self.verifynum=1;
        vparams={'t':'MVA','cachetime':self.gettime()}
        result=requests.get(verifycodeurl,cookies=self.cookiedict,params=vparams)
        vcookiestr=str(result.cookies)
        startpoint=vcookiestr.find('VERIFY_KEY')
        endpoint=vcookiestr.find('for')
        a,b=vcookiestr[startpoint:endpoint].split('=')
        vcookie={}
        vcookie[a.strip()]=b.strip()
        self.cookiedict.update({'VERIFY_KEY':vcookie['VERIFY_KEY']})
        i=Image.open(StringIO(result.content))
        i.save('verifycode{0}.png'.format(self.verifynum))
        return 'verifycode{0}.png'.format(self.verifynum)

    def taskcheck(self,downloadurl):
        taskcheckurl='http://dynamic.cloud.vip.xunlei.com/interface/task_check'
        commiturl='http://dynamic.cloud.vip.xunlei.com/interface/task_commit'
        tasklisturl='http://dynamic.cloud.vip.xunlei.com/interface/showtask_unfresh'
        checkparams={'callback':'queryCid','url':downloadurl,'interfrom':'task'}
        check_result=requests.get(taskcheckurl,params=checkparams,cookies=self.cookiedict)
        check_result.encoding='utf-8'
        print check_result.content
        print
        check_resultstr=str(check_result.content).replace("'",'')
        self.check_resultlist=[s.strip() for s in check_resultstr[10:-1].split(',')]

    def taskcommit(self,downloadurl,vcode):
        commiturl='http://dynamic.cloud.vip.xunlei.com/interface/task_commit'
        check_resultlist=self.check_resultlist
        commitparams={'callback':'ret_task','uid':self.userid,'cid':check_resultlist[0],'gcid':check_resultlist[1],'size':check_resultlist[2],'t':check_resultlist[4],'url':downloadurl,'verify_code':vcode}
        commit_result=requests.get(commiturl,params=commitparams,cookies=self.cookiedict)
        commit_result.encoding='utf-8'
        commit_resultstr=str(commit_result.content)
        print commit_result.content
        print
        startpoint=commit_resultstr.find('(')
        commit_resultlist=[s.strip() for s in commit_resultstr[startpoint+1:-1].split(',')]
        return commit_resultlist

    def getofflineurl(self,taskid):
        tasklisturl='http://dynamic.cloud.vip.xunlei.com/interface/showtask_unfresh'
        tasklistparams={'callback':'jsonp'+self.gettime(),'type_id':4,'page':1,'tasknum':30,'p':1,'interfrom':'task'}
        tasklist_result=requests.get(tasklisturl,params=tasklistparams,cookies=self.cookiedict)
        tasklist_result.encoding='utf-8'
        tasklist_resultstr=str(tasklist_result.content)
        startpoint=tasklist_resultstr.find('(')
        tasklist_resultstr=tasklist_resultstr[startpoint+1:-1]
        #print tasklist_resultstr
        tasklist_dict=json.loads(tasklist_resultstr)
        for task in tasklist_dict['info']['tasks']:
            task['id']=task['id'].encode('utf-8','ignore')
            print task['id']
            if(task['id']==taskid[1:-1]):
                return task['lixian_url']
            else:
                return '0'
