import os, sys, time
from flask import Flask, request, render_template
sys.path.append('/usr/local/lib/python3.6/site-packages/zaif_client')
from zaif_client.public import Public
from zaif_client.trade import Trade

client = Public(public_key='', private_key='')
client_trade = Trade(public_key='', private_key='')

count_buy = 0
count_sell = 0
last_price = 0.0
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    global last_price

    info_account = info_buy = info_sell =  info_cancel = ''
    if request.method == 'GET':
        if request.args.get('account_info'):
            info_account = account_info()
#           last_price = info_account['last_price']
            res = "getinfo_ok"
        elif request.args.get('buy_order'):
            info_buy = buy_order()
            res = "buy_ok"
#            info_account = account_info()
        elif request.args.get('sell_order'):
            info_sell = sell_order()
            res = "sell_ok"
#            info_account = account_info()
        elif request.args.get('cancel_order'):
            info_cancel = cancel_order()
            res = "cancel_ok"
#            info_account = account_info()     
    return render_template('index.html', account_info=info_account, buy_info=info_buy, sell_info=info_sell, cancel_info=info_cancel)

def cancel_order():  
    status_code = 0
    success = 0
    active_order_id = 0
    while status_code != 200 or success != 1:   
        response = client_trade.active_orders()
        status_code = response.status_code
        success = response.json()['success']
        if success == 1:
            active_orders = response.json()['return']
            if active_orders.keys():
                active_order_id = int(list(active_orders.keys())[0])
    if active_order_id == 0:
        return '[cancel_info]none order to cancel'
        
    status_code = 0
    success = 0
    while status_code != 200 or success != 1:   
        response = client_trade.cancel_order(order_id=active_order_id)
        status_code = response.status_code
        success = response.json()['success']
        
    return '[cancel_ok]the existed order canceled'
    
def account_info():
    global last_price
    status_code = 0
    success = 0
    while status_code != 200 or success != 1:
        response = client_trade.get_info2()
        status_code = response.status_code
        success = response.json()['success']
        if success == 1:
            funds_jpy = response.json()['return']['funds']['jpy']
            funds_btc = response.json()['return']['funds']['btc']
    status_code = 0
    success = 0
    while status_code != 200:
        response = client.last_price(currency_pair='btc_jpy') 
        status_code = response.status_code
        last_price = response.json()['last_price']
        
    info = f"[get_info2_ok]funds_btc:{funds_btc},funds_jpy:{funds_jpy},last_price:{last_price}"
    return info

def buy_order():
    global count_buy
    global last_price
    count_buy += 1
    status_code = 0
    success = 0
#    while status_code != 200:
#        response = client.last_price(currency_pair='btc_jpy') 
#        status_code = response.status_code
#        last_price = response.json()['last_price']

    while status_code != 200 or success != 1:
        response = client_trade.get_info2()
        status_code = response.status_code
        success = response.json()['success']
        if success == 1:
            funds_jpy = response.json()['return']['funds']['jpy']

    amount = funds_jpy/last_price
    order_amount = float(int(amount*10000.0)/10000.0)
    order_price = int(last_price)
    status_code = 0
    success = 0
    open_order_id = 1

    while status_code != 200 or success != 1:   
        response = client_trade.trade(currency_pair='btc_jpy', action='bid', price=order_price, amount=order_amount)
        status_code = response.status_code
        if status_code == 200:
            success = response.json()['success']
            if success == 1:
                open_order_id = response.json()['return']['order_id']
    print(f"[info]buy_order listed")
    
    while open_order_id != 0:
        response = client_trade.get_info2()
        if response.status_code == 200:
            success = response.json()['success']
            if success == 1:
                open_order_id = response.json()['return']['open_orders']   
        time.sleep(0.5)
    print(f"[info]buy_order matched")

    return f"[buy_ok] #{count_buy} funds_jpy:{funds_jpy} order_price:{order_price} order_amount:{order_amount}"

def sell_order():
    global count_sell
    global last_price    
    count_sell += 1
    status_code = 0
    success = 0
#    while status_code != 200:
#        response = client.last_price(currency_pair='btc_jpy') 
#        status_code = response.status_code
#        last_price = response.json()['last_price']
    
    while status_code != 200 or success != 1:
        response = client_trade.get_info2()
        status_code = response.status_code
        success = response.json()['success']
        if success == 1:
            funds_btc = response.json()['return']['funds']['btc']
    
    amount = funds_btc
    order_amount = float(int(amount*10000.0)/10000.0)
    order_price = int(last_price)
    status_code = 0
    success = 0
    open_order_id = 1
        
    while status_code != 200 or success != 1:   
        response = client_trade.trade(currency_pair='btc_jpy', action='ask', price=order_price, amount=order_amount)
        status_code = response.status_code
        if status_code == 200:
            success = response.json()['success']
            if success == 1:
                open_order_id = response.json()['return']['order_id']
    print(f"[info]sell_order listed")

    while open_order_id != 0:
        response = client_trade.get_info2()
        if response.status_code == 200:
            success = response.json()['success']
            if success == 1:
                open_order_id = response.json()['return']['open_orders']   
        time.sleep(0.5)
    print(f"[info]sell_order matched")

    return f"[sell_ok] #{count_sell} funds_btc:{funds_btc} order_price:{order_price} order_amount:{order_amount}"
  
if __name__ == '__main__':
    app.run(host="localhost", debug=True)
