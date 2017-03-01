#!/usr/bin/python
#-*-coding:utf-8-*-

import sys,getopt
import time
from Base import Base

class ConsoleApp():
    once = False;
    domain = '';
    user = '';
    password = '';
    ip = '';
    type = '';
    domain_auth_code = '';
    base = '';
    
    def __init__(self,argv):
        self.base = Base();
        self.type = self.base.getConfig('base', 'update_type');
    
    def main(self):
        try:
            opts, args = getopt.getopt(sys.argv[1:], "1hvd:u:p:i:t:c:", 
                                       ["help", "version", "domain=", "user=", "password=" , "ip=", "type=", "domain-auth-code="]);
        except getopt.GetoptError:  
            self.usage();
            sys.exit(1);
            
        if not opts :
            self.usage();
            sys.exit(0);
            
        for name,value in opts:
            if name in ("-h","--help"):
                self.usage();
                sys.exit(0);
            if name in ("-v","--version"):
                self.version();
                sys.exit(0);

            if name in ('-1'):
                self.once = True;
            if name in ("-d","--domain"):
                self.domain = value;
            if name in ("-u","--user"):
                self.user = value;
            if name in ("-p","--password"):
                self.password = value;
            if name in ("-i","--ip"):
                self.ip = value;
            if name in ("-t","--type"):
                self.type = value;
            if name in ("-c","--domain-auth-code"):
                self.domain_auth_code = value;
        
        if self.once:
            self.updateDomain();
        else:
            while True:
                self.updateDomain();
                time.sleep(1800);
    
    def version(self):
        print("Version 0.1");
        
    def usage(self):
        print("Usage: python3 console.py [options]")
        print("Options and arguments:")
        print("-h,--help:      print this message")
        print("-v,--version:   print the version")
        print("-1:             run once")
        
        print("-u,--user:      the username you want to use")
        print("-p,--password:  the password of the username")
        print("-d,--domain:    which domain you want to update")
        print("-i,--ip:        specify ip replace automatic acquisition")
        print("-t,--type:      choose one of [safe,username,authcode]")
        print("-c,--domain-auth-code:  the auth code of the domain")
        print("")
        print("Example:")
        print("There is a user 'admin' with password 'admin' has a domain 'test.com', the auth_code of the domain is '16ca5e665781426e3731c10f8eca7571', \
there are three kind of update type:")
        print("python3 console.py -1 -t safe -d test.com -c 16ca5e665781426e3731c10f8eca7571")
        print("python3 console.py -1 -t authcode -d test.com -c 16ca5e665781426e3731c10f8eca7571")
        print("python3 console.py -1 -t username -d test.com -u admin -p admin")
        
        
    def updateDomain(self):
        rst = self.base.update(self.ip, self.domain, self.type, self.domain_auth_code, self.user, self.password);
        logtime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        if rst == True:
            print(logtime + ": IP Not Change,Do nothing")
        else:
            if rst == 'success':
                print(logtime + ':Update Success, Type->' + self.type);
            else:
                print(logtime + ':Error occur-> ' + rst);
    
    
if __name__ == "__main__":
    ConsoleApp(sys.argv).main();
