#!usr/bin/env python
#_*_ coding:utf-8 _*_


'''
功能要求：
- 额度15000
- 可以提现，手续费5%
- 记录消费流水
- 支持每月账单查询
- 提供还款借口
'''
import time
import json
import getpass
import functools



def check(name):
    filename1 = 'message.json'
    with open(filename1,'rb') as f:
        s =f.read()
        c = json.loads(s)
        if c.has_key(name):
            pass
        else:
            raise ValueError('请注册')

class PersonalMoney(object):
    def __init__(self,name,money=15000):
        self.name = name
        self.money = money
        self.message = {}
        self.record = {}
    def register(self):
        self.message=self._loads('message.json','rb')
        self.message[self.name]={'initMoney':self.money, '剩余金额':15000}
        self._dumps(self.message,'message.json')
        self._loads(str(self.name)+'_record.json','wb',True)

    def _dumps(self, data,filename):
        dumpsdata = json.dumps(data)
        with open(filename,'wb') as f:
            f.write(dumpsdata)
            f.close()

    def _loads(self,jsonfile,filetype='rb',newuser = False):
        if newuser:
            with open(jsonfile,filetype) as f:
                f.write('{"时间":"操作"}')
                f.close()
        else:
            with open(jsonfile,filetype) as f:
                a = f.read()
                s = json.loads(a)
                f.close()
                return s

    def getCash(self, money, ratio = 0.05):
        #需要将交易记录和人员信息和金额区分开
        check(self.name)
        filename1 = 'message.json'
        filname2 = str(self.name) + '_record.json'
        message=self._loads(filename1)
        print message
        self.record = self._loads(filname2)
        last_money = message[self.name][u'剩余金额']
        last_money = last_money - money*(ratio+1)
        if last_money<=0:
            print '剩余金额不足，请充值！'
            return 0
        else:
            Time = time.strftime("%Y-%m-%d %X", time.localtime())
            print "提取现金：",money, "剩余金额：", last_money
            message[self.name][u'剩余金额']= last_money
            self._dumps(message,filename1)
            self.record[Time] = '提取%d'% money
            self._dumps(self.record, filname2)
    def getMonthRecord(self, month):
        check(self.name)
        filename = str(self.name) + '_record.json'
        record = self._loads(filename)
        for i in record:
            if month in i:
                print i,record[i]
    def payback(self,money):
        check(self.name)
        filename1 = 'message.json'
        filename2 = str(self.name)+'_record.json'
        message = self._loads(filename1)
        record = self._loads(filename2)
        message[self.name][u'剩余金额'] = money+message[self.name][u'剩余金额']
        Time = time.strftime("%Y-%m-%d %X", time.localtime())
        record[Time]='存款%d'%money
        print Time,record[Time]
        self._dumps(message,filename1)
        self._dumps(record,filename2)

    def login(self):
        f = self._loads('message.json')
        print '输入你的用户名：'
        if f.has_key(self.name):
            print '登陆已完成'
            pass
        else:raise ValueError('请注册')


if __name__=='__main__':
    username = 'ss'
    a = PersonalMoney('ss10').getCash(100)
    b = PersonalMoney('ss10').getMonthRecord('2016-12')
    c = PersonalMoney('ss10').payback(0)
