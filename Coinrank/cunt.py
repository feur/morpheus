import time
import argparse
from urllib2 import Request, urlopen
import json


def GetEntry():
    
    parser = argparse.ArgumentParser(description='Agent trading for pair')
    
    parser.add_argument('-c', '--alt',
                        action='store',  # tell to store a value
                        dest='currency',  # use `paor` to access value
                        help='Alt-coin')
    parser.add_argument('-t', '--type',
                        action='store',  # tell to store a value
                        dest='type',  # use `paor` to access value
                        help='Margin or Normal')
       
    action = parser.parse_args()
    return action



class Pair(object):
    
    def __init__(self,exchange,pairname):
        self.exchange = exchange
        self.pair = pairname
        #self.exchange_fee = fee
        self.close = 0
        self.high = 0
        self.low = 0
        self.vol = 0
        self.ask = 0
        self.bid = 0
 
        
        
    def GetTicker(self,headers):
        
        values = """
            {
                "exchange_code": "%s",
                "exchange_market": "%s"
            }
        """ % (self.exchange, self.pair)
         
        time.sleep(1)
        request = Request('https://api.coinigy.com/api/v1/ticker', data=values, headers=headers)
        response = urlopen(request).read()
        info = json.loads(response)
        
        if (len(info['data']) != 0):
            data = info['data'][0]
            self.close = float(data['last_trade'])
            self.high = float(data['high_trade'])
            self.low = float(data['low_trade'])
            self.vol = float(data['current_volume'])
            self.ask = float(data['ask'])
            self.bid = float(data['bid'])
 
    
def CheckPairTypeExist(pairname,PairDic):
    
    x = 0
    
    if len(PairDic) == 0:
        x = 0
    else:
        for i in PairDic:
            if pairname == i:
                x = 1
    
    return x
    
def FindHighestVolumeForEachCunt(pairname,PairIndex):
    y = 0
    x = 0
    
    for i in range (0,len(PairIndex)):
        if (PairIndex[i].pair == pairname and PairIndex[i].vol > y ):
            y = PairIndex[i].vol
            x = i
            
    print("Pair: %s best at %s ....  ask = %.9f, bid = %.9f, h =%.9f, l=%.9f, c = %.9f, v = %.9f") % (pairname,
         PairIndex[x].exchange,PairIndex[x].ask,PairIndex[x].bid,PairIndex[x].high,PairIndex[x].low,PairIndex[x].close,PairIndex[x].vol)
    

       
   
##-----------------------------------------
    
entry = GetEntry() 
currency = entry.currency
trading_type = int(entry.type)

print("Building Cunt Index......")
print("so many cunts so little time...")
print("_____________________________________________________________________________________________________________________________________")

headers = {
  'Content-Type': 'application/json',
  'X-API-KEY': 'ee0a8d21b3934ef595bc4dc13b864956',
  'X-API-SECRET': 'e2a87c2c18489d04ce63cb8c946a3eda'
}

PairIndex = []
PairDic = []

normal_exchange = ["BINA","BIND","BITF","BITS","BLEU","BTCM","BTHM","BTRX","BXTH","CBNK","CCEX","CCJP","CONE","CPIA","CXIO","EXMO",
            "FLYR","GATE","GDAX","GMNI","GOLD","HITB","HUBI","ITBT","KBIT","KRKN","KUCN","LAKE","LIQU","LIVE","MATE","MERC","OKEX",
            "OKFT","YOBT","PLNX"]

margin_exchange = ["BMEX","BITF","HUBI","POLO","KRKN"]

if (trading_type == 0):
    exchange = normal_exchange
elif (trading_type == 1):
    exchange = margin_exchange



for e in exchange:
    #exchange = i["exch_code"]
    #fee = i["exch_fee"]
    values = """
    {
     "exchange_code": "%s"
     }
    """ % (e)
    
    request = Request('https://api.coinigy.com/api/v1/markets', data=values, headers=headers)
    time.sleep(1)
    response = urlopen(request).read()
    info = json.loads(response)
    print("| Exchange ----- %s") %(e)
    #print("|")
    data = info['data']
    for i in data:
        if currency in i['mkt_name']:
            pairname = i['mkt_name']
            
            ##register new pairtypes
            if (CheckPairTypeExist(pairname,PairDic) == 0): #check if pairtype allready exists
                PairDic.append(pairname) ##if not add in new pairtype
            
            x = Pair(e,pairname) 
            x.GetTicker(headers)
            #print("| Pair %s , ask = %.9f, bid = %.9f, h =%.9f, l=%.9f, c = %.9f, v = %.9f ") % (x.pair,x.ask,x.bid,x.high,x.low,x.close,x.vol)                  
            PairIndex.append(x)
            
print("_____________________________________________________________________________________________________________________________________")
print("")
   
for i in PairDic:
    FindHighestVolumeForEachCunt(i,PairIndex)



