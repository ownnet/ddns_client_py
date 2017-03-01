#!/usr/bin/python
#-*-coding:utf-8-*-

import configparser
import time
from Api import Api

class Base():
    api = '';
    config = '';
    
    def __init__(self):
        self.config = configparser.ConfigParser();
        self.config.read('conf.ini', 'utf-8');
        
        self.api = Api(server_url = self.config.get('base','server_url'));

        today_first_run = self.config.get('runtime','today_first_run');
        date_day = time.strftime('%d',time.localtime(int(today_first_run)));
        #若不是本日首次运行，执行时间戳更新操作
        if date_day != time.strftime('%d',time.localtime(time.time())):
            self.config.set('runtime','today_first_run',str(int(time.time())));
            self.updateTimeOffset();
            
    def __del__(self):
        self.config.write(open('conf.ini','w'))
        
    def updateTimeOffset(self):
        server_time = int(self.api.gettime());
        local_time = int(time.time());
        
        time_offset = str(server_time - local_time);
        self.config.set('safe','time_offset',time_offset);
        
    def setUserName(self,user):
        self.config.set('username','user',user);
    
    def setPassword(self,password):
        self.config.set('username','password',password);
        
    def getConfig(self,sec,opt):
        return self.config.get(sec,opt);
        
    def update(self,ip = '',domain='',update_type = '',domain_auth_code = '',user = '',password = ''):
        local_time = str(int(time.time()));
        last_domain = self.config.get('runtime','domain');     


        if ip == '':
            ip = self.api.getip();
        else:
            self.config.set('runtime','ip',ip);
        if update_type == '':
            update_type = self.config.get('base','update_type');
        else:
            self.config.set('base','update_type',update_type);

        if domain == '':
            domain = self.config.get('runtime','domain');
        else:
            self.config.set('runtime','domain',domain);
            
        if domain_auth_code == '':
            domain_auth_code = self.config.get('runtime','auth_code');
        else:
            self.config.set('runtime','auth_code',domain_auth_code);
        
        if user == '':
            user = self.config.get('username','user');
        else:
            self.config.set('username','user',user);
        if password == '':
            password = self.config.get('username','password');
        else:
            self.config.set('username','password',password);
          
        on_error = self.config.get('runtime','on_error');
        #当上次操作没有发生错误，ip未改变，上次更新与本次更新的域名相同时，不执行更新操作
        if self.config.get('runtime','ip') == ip and on_error == '0' and last_domain == domain:
            #ip未发生变化,且上一次操作未发生错误，不触发更新
            self.config.set('runtime','last_check',local_time);
            return True;
        else:
            self.config.set('runtime','last_check',local_time);
            self.config.set('runtime','last_update',local_time);
            self.config.set('runtime','ip',ip);
        
            if update_type == 'safe':
                time_offset = self.config.get('safe','time_offset');
                rst = self.api.update(domain, ip, domain_auth_code,time_offset);
                
                if rst == 'success':
                    self.config.set('runtime','on_error','0');
                else:
                    self.config.set('runtime','on_error','1');
                    
                return rst;
            elif update_type == 'username':
                user = self.config.get('username','user');
                password = self.config.get('username','password');
                rst = self.api.updateByUserName(domain, ip, user, password);
                
                if rst == 'success':
                    self.config.set('runtime','on_error','0');
                else:
                    self.config.set('runtime','on_error','1');
                
                return rst
            
            elif update_type == 'authcode':
                rst = self.api.updateByAuthCode(domain, ip, domain_auth_code);
                
                if rst == 'success':
                    self.config.set('runtime','on_error','0');
                else:
                    self.config.set('runtime','on_error','1');
               
                return rst;
            else:
                return 'error:unknown_type';
                
        
if __name__ == "__main__":
    x = Base().getConfig('runtime', 'domain');
    print(x)