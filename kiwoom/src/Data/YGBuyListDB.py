# -*- coding: utf-8 -*-
import sqlite3
import sys,os
sys.path.append('../')
sys.path.append('../DB')
import DBSet
import time,datetime
import pandas as pd


class YGGetDbData(DBSet.DBSet):
    
    def getCodeNameForReaReg(self):
        '''초기 실시간데이터받기용 쿼리'''
        query = 'select StockCode,BUYSELL from '+self.BuyListTable
        self.cursor.execute(query)
        dd = self.cursor.fetchall()
        yy=[]
        for index in range(len(dd)) :
            code = dd[index][0]
            buysell=dd[index][1]
            arry = code,buysell
            yy.append(arry)
        return pd.DataFrame(yy,columns=['Code','BuySell'])
    
    def setProperties(self,dbName='../../Sqlite3/BuyList.db',table='BuyList'):
        super().setProperties(dbName,table)
        
        
#     def updateRelativeCode(self,Code,relative,pastMinute):
    def updateRelativeCode(self,Code,relative,timeVal):
#         tim = datetime.datetime.now()
#         hour = str(tim.hour)
#         minute = str(pastMinute)
#         foTime = hour+minute
        foTime = str(timeVal[0])
        
        info = str(relative)
        query = 'update '+self.BuyListRelativeTable+' set "'+foTime+ '" = '+str(info)+' where StockCode = '+str(Code)
        
        self.cursor.execute(query)
        self.conn.commit()
        
    def updateVolumeCode(self,Code,Rotate,timeVal):
        
        info = str(timeVal[1])
        foTime = str(timeVal[0])
        
        query = 'update '+self.BuyListVolumeRotateTable+' set "'+foTime+ '" = '+str(info)+' where StockCode = '+str(Code)
#         print(query)
        self.cursor.execute(query)
        self.conn.commit()
    
    def updateBuy(self,code):
        
        code = str(code)
        query = 'update '+self.BuyListTable+' set "BUYSELL"="B" where StockCode = '+code
        self.cursor.execute(query)
        self.conn.commit()
    
    def buyStock(self,code,time,CurrPrice):
        '''update BuyList set '900'=0 where StockCode = 19210'''
        price=CurrPrice
        query = 'update '+self.BuyListTable+' set "'+ str(time) +'" ='+str(price)+', "BUYSELL"="Y"  where StockCode = '+str(code)
        self.cursor.execute(query)
        self.conn.commit()
        
    def updateSell(self,code):
        code = str(code)
        query = 'update '+self.BuyListTable+' set "BUYSELL"="S" where StockCode = '+code
        self.cursor.execute(query)
        self.conn.commit()
        
    def sellStock(self,code,time,CurrPrice):
        price=CurrPrice
        query = 'update '+self.BuyListTable+' set "'+ str(time) +'" ='+str(price)+', "BUYSELL"="N"  where StockCode = '+str(code)
        self.cursor.execute(query)
        self.conn.commit()
        
    def getEndCode(self):
        query = 'select StockCode from '+self.BuyListTable+' where "BUYSELL"="Y"'
        self.cursor.execute(query)
        dd = self.cursor.fetchall()
        yy=[]
        for index in range(len(dd)):
            code=dd[index][0]
            yy.append(code)
        return pd.DataFrame(yy,columns=['Code'])
    
    def getBuySell(self):
#         query = 'select BUYSELL from '+self.BuyListTable+' where StockCode = "'+code+'"'
        query = 'select StockCode,BUYSELL from '+self.BuyListTable
        
        self.cursor.execute(query)
        dd = self.cursor.fetchall()
        
        arw=[]
        for i in range(len(dd)):
            if dd[i][1] =="B":
                arw.append(dd[i])
            elif dd[i][1] =="S":
                arw.append(dd[i])
        return arw
    
    def insertGold(self,code,name):
        
        try:
#             sql = 'insert into '+self.BuyListTable+' (StockCode) values("'+str(code)+'");'
            
            sql = self.insertGoldQuery.format(tableName=self.BuyListTable,StockCode=str(code),StockName=str(name))
            self.cursor.execute(sql)
            
            sql = self.insertGoldQuery.format(tableName=self.BuyListVolumeRotateTable,StockCode=str(code),StockName=str(name))
#             sql = 'insert into '+self.BuyListVolumeRotateTable+' (StockCode) values("'+str(code)+'");'
            self.cursor.execute(sql)
            sql = self.insertGoldQuery.format(tableName=self.BuyListRelativeTable,StockCode=str(code),StockName=str(name))
#             sql = 'insert into '+self.BuyListRelativeTable+' (StockCode) values("'+str(code)+'");'
            self.cursor.execute(sql)
            
            self.conn.commit()
            
        except Exception:
            
            self.tracebackLog()
    
    
if __name__ == '__main__':
    cp =YGGetDbData()
    cp.insertGold('000222')
#     DB = '../../Sqlite3/BuyList'+str(datetime.datetime.today().date())+'.db'
    DB = cp.BuyListDBToday
    table = cp.BuyListTable
    print(DB,table)
    cp.setProperties(DB,table)
    
    yy = cp.getCodeNameForReaReg()
#     print(yy['BuySell'])
#     cp.buyStock(98120, 903,236200)
#     cp.updateVolumeCode(227950, 3820,932)
#     cp.sellStock(19210, 930,12000)
#     print(cp.getEndCode())
#     print(yy['Code'][0])
    dd = cp.getBuySell()
    for i in range(len(dd)):
        print(str(dd[i][1]))