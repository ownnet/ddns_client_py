#!/usr/bin/python
#-*-coding:utf-8-*-

import requests
import json
import time
import hashlib

class Api():
    __error_code = 0;
    __last_error_func = '';
    
    server_url = '';
    ip = '';
    token_code = '';
    
    def __init__(self,server_url):
        self.server_url = server_url;
        
    def isJson(self,json_str):
        try:
            json.loads(json_str);
        except ValueError:
            return False;
        return True;
    
    def get(self,func,params = ''):
        r = requests.get(self.server_url + func,params = params);
        content = r.content.decode('utf-8');
        if self.isJson(content):
            return json.loads(content);
        else:
            #当返回值以'error'开头，则表示查询结果出错，error_code置1
            if content.find('error') == 0:
                self.__error_code = 1;
                self.__last_error_func = func;
            return content;
            
    def post(self,func,data):
        r = requests.post(self.server_url + func, data = data);
        content = r.content.decode('utf-8');
        if self.isJson(content):
            return json.loads(content);
        else:
            #当返回值以'error'开头，则表示查询结果出错，error_code置1
            if content.find('error') == 0:
                self.__error_code = 1;
                self.__last_error_func = func;
            return content;
    
#API封装
    
    def getip(self):
        self.ip = self.get('getip');
        return self.ip;
    
    def gettime(self):
        return self.get('gettime');
    
    def getUserInfo(self,token):
        params = {'token':token};
        return self.get('getuserinfo', params);
        
    def getDomainInfo(self,token,domain):
        params = {'token':token,'domian':domain};
        return self.get('getdomaininfo', params);
    
    def getAuthCode(self,token,domain):
        params = {'token':token,'domian':domain};
        return self.get('getauthcode', params);
    
    def getDomainList(self,token):
        params = {'token':token};
        return self.get('getdomainlist', params);

    def update(self,domain,ip,domain_auth_code,time_offset):
        server_time = int(time.time()) + int(time_offset);
        time_auth_code =  hashlib.md5((str(int(server_time/30)) + str(domain_auth_code)).encode('utf-8')).hexdigest();
        
        data = {'auth':time_auth_code,
                'ip':ip,
                'domain':domain};
        return self.post('update?version=safe', data);
    
    def updateByUserName(self,domain,ip,user,password):
        params = {
                  'version':'username',
                  'domain':domain,
                  'ip':ip,
                  'username':user,
                  'password':password
                  };
        return self.get('update', params);
    
    def updateByAuthCode(self,domain,ip,domain_auth_code):
        params = {
                  'version':'authcode',
                  'domain':domain,
                  'ip':ip,
                  'auth_code':domain_auth_code
                  };
        return self.get('update', params);
    
    def auth(self,username,password):
        data = {'username':username,
                'password':password};
        self.token_code = self.post('auth', data)            
        return self.token_code;
    
    def keepAlive(self,token):
        data = {'token':token};
        return self.post('keepalive', data);
    
    def test(self):
        #self.auth('admin', 'admin')
        #r= self.get('getuserinfo',{'token':self.token_code})
        #r = self.getUserInfo(self.token_code)
        #print(r)
        x = self.update('domain.com', '127.0.0.1', '12456464');
        print(x)
        
            

if __name__ == "__main__":
    #Api(server_url = 'http://127.0.0.1/ddnsweb/yii/web/api/').test();
    x = Api('http://127.0.0.1/ddnsweb/yii/web/api/').update('test.com', '192.168.1.1', '16ca5e665781426e3731c10f8eca7571', 0)
    print(x)