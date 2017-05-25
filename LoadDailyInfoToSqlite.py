
# coding: utf-8

# In[1]:

import sqlite3,csv,os,sys
import requests,csv
from datetime import  timedelta
import datetime,time

def InsertStockToSQLite(rows):
    conn = sqlite3.connect('stock.db')
    c = conn.cursor()

    # Create table
    c.execute('''create table if not exists StockDaily  (TradeDate int,ID TEXT,Name TEXT,Amount int, Open NUMERIC,High NUMERIC,Low NUMERIC,Close NUMERIC, CDP NUMERIC,AH NUMERIC,NH NUMERIC,NL NUMERIC,AL NUMERIC, PRIMARY KEY(TradeDate,ID))''')
    conn.commit()
    #Insert
    c.executemany('INSERT OR REPLACE INTO StockDaily VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)', rows)
    conn.commit()
    conn.close()

d=sys.argv[1]
#today = datetime.date.today()
today=datetime.date(year=int(d[0:4]), month=int(d[4:6]), day=int(d[6:8]))
dates = []
dates.append(today)

#twse

#headers={"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
#"Accept-Encoding":"gzip, deflate",
#"Accept-Language":"zh-TW,zh;q=0.8,en-US;q=0.6,en;q=0.4",
#"Cache-Control":"max-age=0",
#"Connection":"keep-alive",
#"Content-Length":"54",
#"Content-Type":"application/x-www-form-urlencoded",
#"Cookie":"__utmt=1; __utma=145556017.1896910337.1493995678.1493995678.1493995678.1; __utmb=145556017.32.9.1493998652070; __utmc=145556017; __utmz=145556017.1493995678.1.1.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided)",
#"Host":"www.tse.com.tw",
#"Origin":"http://www.tse.com.tw",
#"Referer":"http://www.tse.com.tw/ch/trading/exchange/MI_INDEX/MI_INDEX.php",
#"Upgrade-Insecure-Requests":"1",
#"User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36"}
for d in dates:
    dstring=d.strftime("%Y%m%d")
    url = 'http://www.tse.com.tw/exchangeReport/MI_INDEX?response=csv&date='+dstring+'&type=ALLBUT0999'
	#payload = {"response":"csv","date":dstring,"type":"ALLBUT0999"}
    r = requests.get(url)
    #print(r.content)
	#filename=d.strftime("%Y%m%d")+".csv"
    reader = list(csv.reader(str(r.content.decode('cp950')).split('\n'), delimiter=','))
    #print(reader[2])
    firstIndex=0
    lastIndex=0
    Outputs=[]
    for i in range(len(reader)):
        row=reader[i]
        if(len(row)>0):
            row[0]=row[0].strip('=').strip('\"').strip()
            #row[0]=row[0].strip('\"')
            #row[0]=row[0].strip()
            #print(row[0])
            if(row[0]=='0050'):
                firstIndex=i
            if(row[0]=='9958'):
                lastIndex=i
        #print("%s-%s-%s"%(file,firstIndex,lastIndex))
    for stock in reader[firstIndex:lastIndex+1]:
        TradeDate=d.strftime("%Y%m%d")
        ID=stock[0]
        Name=stock[1].strip('=').strip('\"').strip()
        Amount=stock[2].replace(",",'').strip('=').strip('\"').strip()
        if(stock[5].replace(",",'').strip('=').strip('\"').strip()=="--"):
            Open=0
        else:
            Open=float(stock[5].replace(",",'').strip('=').strip('\"').strip())
        if(stock[6].replace(",",'').strip('=').strip('\"').strip()=="--"):
            High=0
        else:
            High=float(stock[6].replace(",",'').strip('=').strip('\"').strip())
        if(stock[7].replace(",",'').strip('=').strip('\"').strip()=="--"):
             Low=0
        else:
             Low=float(stock[7].replace(",",'').strip('=').strip('\"').strip())
        if(stock[8].replace(",",'').strip('=').strip('\"').strip()=="--"):
             Close=0
        else:
             Close=float(stock[8].replace(",",'').strip('=').strip('\"').strip())        
        CDP=round(((Close*2)+High+Low)/4.0,2)
        AH=round(CDP+(High-Low),2)
        NH=round((CDP*2)-Low,2)
        NL=round((CDP*2)-High,2)
        AL=round(CDP-(High-Low),2)
        #print((TradeDate,ID,Name,Amount,Open,High,Low,Close,CDP,AH,NH,NL,AL))
        Outputs.append((TradeDate,ID,Name,Amount,Open,High,Low,Close,CDP,AH,NH,NL,AL))
    #print(Outputs)
    InsertStockToSQLite(Outputs)

#tpex
for d in dates:
    dstring=str(d.year-1911)+'/'+str(d.month).zfill(2)+'/'+str(d.day).zfill(2)
    url="http://www.tpex.org.tw/web/stock/aftertrading/otc_quotes_no1430/stk_wn1430_download.php?l=zh-tw&d="+dstring+"&se=EW&s=0,asc,0"
    r=requests.get(url)
    filename=d.strftime("%Y%m%d")+".csv"
    reader = list(csv.reader(str(r.content.decode('cp950')).split('\n'), delimiter=','))
    #print(reader[2])
    firstIndex=0
    lastIndex=0
    Outputs=[]
    for i in range(len(reader)):
        row=reader[i]
        if(len(row)>0):
            row[0]=row[0].strip('=').strip('\"').strip()
            #row[0]=row[0].strip('\"')
            #row[0]=row[0].strip()
            #print(row[0])
            if(row[0]=='006201'):
                firstIndex=i
            if(row[0]=='9962'):
                lastIndex=i
        #print("%s-%s-%s"%(file,firstIndex,lastIndex))
    for stock in reader[firstIndex:lastIndex+1]:
        TradeDate=d.strftime("%Y%m%d")
        ID=stock[0]
        Name=stock[1].strip()
        Amount=int(stock[7].replace(",",'').strip('\"').strip())
        if(stock[4].replace(",",'').strip('\"').strip()=="----"):
            Open=0
        else:
            Open=float(stock[4].replace(",",'').strip('\"').strip())

        if(stock[5].replace(",",'').strip('\"').strip()=="----"):
            High=0
        else:
            High=float(stock[5].replace(",",'').strip('\"').strip())

        if(stock[6].replace(",",'').strip('\"').strip()=="----"):
            Low=0
        else:
            Low=float(stock[6].replace(",",'').strip('\"').strip())

        if(stock[2].replace(",",'').strip('\"').strip()=="----"):
            Close=0
        else:
            Close=float(stock[2].replace(",",'').strip('\"').strip())        
        CDP=round(((Close*2)+High+Low)/4.0,2)
        AH=round(CDP+(High-Low),2)
        NH=round((CDP*2)-Low,2)
        NL=round((CDP*2)-High,2)
        AL=round(CDP-(High-Low),2)
        #print((TradeDate,ID,Name,Amount,Open,High,Low,Close,CDP,AH,NH,NL,AL))
        Outputs.append((TradeDate,ID,Name,Amount,Open,High,Low,Close,CDP,AH,NH,NL,AL))
    #print(Outputs)
    InsertStockToSQLite(Outputs)


# In[ ]:



