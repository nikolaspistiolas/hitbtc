import time
import queue
from hitbtc import HitBTC
import pymongo
import copy
import datetime
cl = pymongo.MongoClient('localhost',27017)
db = cl['hitbtc']
col = db['btcusd']

c = HitBTC()
c.start()  # start the websocket connection
time.sleep(2)  # Give the socket some time to connect
c.subscribe_book(symbol='BTCUSD') # Subscribe to ticker data for the pair ETHBTC

def update(data,old_data):
    for i in data[2]['ask']:
        for j in range(len(old_data['ask'])):
            if float(i['price']) == old_data['ask'][j]['price']:
                if float(i['size']) == 0:
                    if j == 0:
                        old_data['ask'] = old_data['ask'][1:]
                    else:
                        old_data['ask'] = old_data['ask'][:j] + old_data['ask'][j+1:]
                else:
                    if float(i['size']) == 0:
                        print('ERROR')
                    old_data['ask'][j]['size'] = float(i['size'])
                break
            elif float(i['price']) < old_data['ask'][j]['price']:# and float(i['size'])!=0:
                old_data['ask'] = old_data['ask'][:j] + [{'price':float(i['price']),'size':float(i['size'])}] + old_data['ask'][j:]
                break
    for i in data[2]['bid']:
        for j in range(len(old_data['bid'])):
            if float(i['price']) == old_data['bid'][j]['price']:
                if float(i['size']) == 0:
                    if j == 0:
                        old_data['bid'] = old_data['bid'][1:]
                    else:
                        old_data['bid'] = old_data['bid'][:j] + old_data['bid'][j + 1:]
                else:
                    if float(i['size']) == 0:
                        print('ERROR')
                    old_data['bid'][j]['size'] = float(i['size'])
                break
            elif float(i['price']) > old_data['bid'][j]['price']:# and float(i['size'])!=0:
                old_data['bid'] = old_data['bid'][:j] +  [{'price':float(i['price']),'size':float(i['size'])}] + old_data['bid'][j:]
                break
    return old_data

def create(data):
    ret = {'ask':[],'bid':[]}
    for i in data[2]['ask']:
        ret['ask'].append({'price':float(i['price']),'size':float(i['size'])})
    for i in data[2]['bid']:
        ret['bid'].append({'price':float(i['price']),'size':float(i['size'])})
    return ret

def handle_rec(data,old_data=None):
    if data[0] == 'snapshotOrderbook':
        return create(data)
    elif data[0] == 'updateOrderbook':
        return update(data,old_data)
old = {}

while True:
    try:
        data = c.recv()

        old = handle_rec(data,old)
        #print(old)
        try:
            t = data[2]['timestamp']
            t = time.mktime(datetime.datetime.strptime(t.split('.')[0],"%Y-%m-%dT%H:%M:%S").timetuple()) + float('0.'+t.split('.')[1][:-1])
            col.insert({'_id':t,'ask':old['ask'][:80],'bid':old['bid'][:80]})

        except:
            pass
    except queue.Empty:
        continue

    # process data from websocket
    ...

c.stop()