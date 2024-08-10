import httpx
from numpy import Infinity
import asyncio
import schedule
import time
from itertools import islice
from schedule_machine.chrono import Timers,Chronograph


timers_container = Timers()



quantity = 15  #quantity
x = 635 #Near  by

finalLTPAfter10Up =  0
instrument_key = ""
finalData = {}
finalLTPLOS15 = 0
isByu = False
isValueSetFirst = True
isFirst = 0
stopLOSE = 0
currentLTP = 0

proFit = 0.44
stopL = 0.20

test = 1


call_finalLTPAfter10Up =  0
call_instrument_key = ""
call_finalData = {}
call_finalLTPLOS15 = 0
call_isByu = False
call_isValueSetFirst = True
call_isFirst = 0
call_stopLOSE = 0
call_currentLTP = 0
call_order_id = 0

call_proFit = 2.65
call_stopL = 1.25

# url = 'https://api.upstox.com/v2/option/chain?instrument_key=NSE_INDEX|Nifty 50&expiry_date=2024-05-16'     #25
url = 'https://api.upstox.com/v2/option/chain?instrument_key=NSE_INDEX|Nifty Bank&expiry_date=2024-06-05'   #15
# url = 'https://api.upstox.com/v2/option/chain?instrument_key=NSE_INDEX|Nifty Fin Service&expiry_date=2024-05-14'  #40
# url = 'https://api.upstox.com/v2/option/chain?instrument_key=BSE_INDEX|SENSEX&expiry_date=2024-05-31'        #10
# url = 'https://api.upstox.com/v2/option/chain?instrument_key=NSE_INDEX|NIFTY MID SELECT&expiry_date=2024-06-03'  #75

authorization = 'Bearer eyJ0eXAiOiJKV1QiLCJrZXlfaWQiOiJza192MS4wIiwiYWxnIjoiSFMyNTYifQ.eyJzdWIiOiJKQzUzMTgiLCJqdGkiOiI2NjU5NDUzMmYzYjQ3MTM1MWJiZGQ4MTEiLCJpc011bHRpQ2xpZW50IjpmYWxzZSwiaWF0IjoxNzE3MTI2NDUwLCJpc3MiOiJ1ZGFwaS1nYXRld2F5LXNlcnZpY2UiLCJleHAiOjE3MTcxOTI4MDB9.XA81IeNAm2_XTvydMqCDTzAOqi1Q2T-45mZ7mIKVe1Y'

async def placeOrderApiCall(data):
    global finalLTPAfter10Up
    global call_order_id
    finalLTPAfter10Up = 1
    # return

    url = 'https://api.upstox.com/v2/order/place'
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': authorization,
    }
  
    print("byu new -- ",data)
    try:
         async with httpx.AsyncClient() as client:
            response = await client.post(url,json=data, headers=headers)
            print('Response Code:', response.status_code)
            print('Response Body:', response.json())
            data = response.json()
            print(response.json())
            if data['status'] == 'success':
                print()
                call_order_id = data['data']['order_id']
                finalLTPAfter10Up=1
            else:
                print("------ORDER ERROR ------")

    except Exception as e:
        # Handle exceptions
        print('Error on Byu:', str(e))

async def placeOrderApiCallSell(data):
    global finalLTPAfter10Up
    finalLTPAfter10Up = 0
    url = 'https://api.upstox.com/v2/order/place'
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': authorization,
    }
    print("sell new -- ",data)
    try:
         async with httpx.AsyncClient() as client:
            response = await client.post(url,json=data, headers=headers)
            print('Response Code:', response.status_code)
            print('Response Body:', response.json())
            data = response.json()
            print(response.json())
            if data['status'] == 'success':
                print()
                finalLTPAfter10Up=1
            else:
                print("------ORDER ERROR ------")

    except Exception as e:
        # Handle exceptions
        print('Error on Sell:', str(e))


def getClosest(data,key) :
    difference = 0
    bestIndex = 0
    bestDifference = Infinity
    i = 0
    cur = 0
    bodyWeight=0

    indices = range(len(data))
    for i in indices:
        cur = data[i]
        bodyWeight = cur[key]['market_data']['ltp']
        # print(x)
        # print(bodyWeight)
        complex_number = (x - bodyWeight)

        difference = abs(complex_number)
        if difference < bestDifference:
            bestDifference = difference
            bestIndex = i
    # print(data[bestIndex])
    return data[bestIndex]
    print(data[bestIndex])

def getClosest2(data1,data2) :
    
    difference1 = abs(x-data1['call_options']['market_data']['ltp'])
    difference2 = abs(x-data2['put_options']['market_data']['ltp'])

    if difference1 < difference2:
        return {'value':"call_options",'data':data1}
    else:
        return {'value':"put_options",'data':data2}
   
async def getPer(ltp,pers,add):
    percentV = lambda x : x/100
    percentV10 = percentV(pers)
    percent10 = ltp*percentV10
    if add == True:
        return ltp+round(percent10, 2)
    else:
        return ltp-round(percent10, 2)


async def getChainApiCall():
    global call_finalLTPAfter10Up
    global call_instrument_key
    global call_finalData
    global call_finalLTPLOS15
    global call_isFirst
    global call_stopLOSE
    global call_currentLTP
    global call_isValueSetFirst
    global call_isByu

    global test
   
    #for one time run
    # if test == 0:
    #     print('-------on ddone-----')
    #     return

    headers = {
        'Accept': 'application/json',
        'Authorization': authorization
    }
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)
            print(response.status_code)
            if response.status_code == 200:
                    data = response.json()
                    if data['status'] == 'success':
                        print("-------Call---------")
                        print("call_finalLTPAfter10Up : ",call_finalLTPAfter10Up)
                        # print(len(data['data']))
                        if call_isValueSetFirst == True:
                            p1 = getClosest(data['data'],"call_options")
                            call_finalData = {'value':"call_options",'data':p1}
                            print(call_finalData)
                            ltpType = call_finalData['value']
                            ltp = call_finalData['data'][ltpType]['market_data']['ltp']
                            call_instrument_key = call_finalData['data'][ltpType]['instrument_key']
                            call_currentLTP = round(call_finalData['data'][ltpType]['market_data']['ltp'],2)
                            # finalLTP10 =  await getPer(ltp,10,True)
                            call_finalLTPLOS15 =  await getPer(ltp,proFit,True)
                            call_stopLOSE =  await getPer(ltp,stopL,False)
                            print("ltp : ",ltp)
                            print("call_finalLTPLOS15 : ",call_finalLTPLOS15)
                            call_isValueSetFirst = False
                            buffrerPrice = call_finalLTPLOS15+3
                            orderData = {
                                'quantity': quantity,
                                'product': 'D',
                                'validity': 'DAY',
                                'price': round(buffrerPrice, 0),
                                'tag': 'string',
                                'instrument_token': call_instrument_key,
                                'order_type': 'SL',
                                'transaction_type': 'BUY',
                                'disclosed_quantity': 0,
                                'trigger_price':round(call_finalLTPLOS15, 0) ,
                                'is_amo': False,
                            }
                            print('---New Order---')
                            call_finalLTPAfter10Up = 1
                            await placeOrderApiCall(orderData)

                        
                        print('call_currentLTP : ',call_currentLTP)
                        c_or_p = call_finalData['value']
                        newPriceData=[x for x in data['data'] if x[c_or_p]['instrument_key'] == call_instrument_key]
                        newLTP = newPriceData[0][c_or_p]['market_data']['ltp']
                        # call_finalLTPLOS15 =  await getPer(newLTP,proFit,True)

                        print('newLTP : ',newLTP)
                        print('call_finalLTPLOS15 : ',call_finalLTPLOS15)
                        print('close_price : ',newPriceData[0]['strike_price'])
                        print('call_stopLOSE : ',call_stopLOSE)

                        if call_isValueSetFirst == False:
                            openOrderResponse = await client.get('https://api.upstox.com/v2/order/details?order_id='+call_order_id, headers=headers)
                            openData = openOrderResponse.json()
                            if openData['status'] == 'success':
                                print('openData')
                                if openData['data']['status'] == 'complete':
                                    print('opne to complete order')
                                    if round(newLTP, 2) > round(call_finalLTPLOS15, 2):
                                        print('------ New value ++++-----')
                                        l = round(newLTP, 2) - round(call_currentLTP, 2)
                                        call_currentLTP = round(newLTP, 2)
                                        call_finalLTPLOS15 =  round(newLTP, 2)
                                        call_stopLOSE =  round(call_stopLOSE, 2) + l

                                    if round(call_stopLOSE, 2) > round(newLTP, 2):
                                        print('------Sell-----')
                                        call_isByu=False
                                        call_isValueSetFirst = True
                                        orderData = {
                                                'quantity': quantity,
                                                'product': 'D',
                                                'validity': 'DAY',
                                                'price': 0,
                                                'tag': 'string',
                                                'instrument_token': call_instrument_key,
                                                'order_type': 'MARKET',
                                                'transaction_type': 'SELL',
                                                'disclosed_quantity': 0,
                                                'trigger_price': 0,
                                                'is_amo': False,
                                            }
                                        test = 0

                                        await placeOrderApiCallSell(orderData)
                                    


                    else:
                        print('----No Data----')
            # print(response.json[0])
       
    except Exception as e:
        # Handle exceptions
        print('Error:  main ', str(e))


async def getChainApiPut():
    global finalLTPAfter10Up
    global instrument_key
    global finalData
    global finalLTPLOS15
    global isFirst
    global stopLOSE
    global currentLTP
    global isValueSetFirst
    global isByu


    headers = {
        'Accept': 'application/json',
        'Authorization': authorization
    }
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)
            print(response.status_code)
            if response.status_code == 200:
                    data = response.json()
                    if data['status'] == 'success':
                        print("-------Put---------")
                        # print(len(data['data']))
                        if isValueSetFirst == True:
                            p1 = getClosest(data['data'],"call_options")
                            p2 = getClosest(data['data'],"put_options")
                            print("p2 ---  : ",p2)

                            finalData = {'value':"put_options",'data':p2}
                            # finalData = getClosest2(p2,p2)
                            # print(finalData)
                            ltpType = finalData['value']
                            ltp = finalData['data'][ltpType]['market_data']['ltp']
                            instrument_key = finalData['data'][ltpType]['instrument_key']
                            currentLTP = round(finalData['data'][ltpType]['market_data']['ltp'],2)

                            # finalLTP10 =  await getPer(ltp,10,True)
                            finalLTPLOS15 =  await getPer(ltp,proFit,True)
                            stopLOSE =  await getPer(ltp,stopL,False)
                            print("ltp : ",ltp)
                            isValueSetFirst = False

                        # print('finalData : ',finalData)
                        print('currentLTP : ',currentLTP)
                        c_or_p = finalData['value']
                        newPriceData=[x for x in data['data'] if x[c_or_p]['instrument_key'] == instrument_key]
                        newLTP = newPriceData[0][c_or_p]['market_data']['ltp']
                        print('newLTP : ',newLTP)
                        print('finalLTPLOS15 : ',finalLTPLOS15)
                        print('close_price : ',newPriceData[0]['strike_price'])
                        
                        print('stopLOSE : ',stopLOSE)

                        
                        if isByu == False: #if value 10% then isByu true
                            if round(finalLTPLOS15, 2) < newLTP:
                                print('------Buy-----')
                                stopLOSE =  await getPer(newLTP,stopL,False)
                                isByu=True
                                orderData = {
                                    'quantity': 80,
                                    'product': 'D',
                                    'validity': 'DAY',
                                    'price': 0,
                                    'tag': 'string',
                                    'instrument_token': instrument_key,
                                    'order_type': 'MARKET',
                                    'transaction_type': 'BUY',
                                    'disclosed_quantity': 0,
                                    'trigger_price': 0,
                                    'is_amo': False,
                                }
                                print('---New Order---')
                                finalLTPAfter10Up = 1
                                await placeOrderApiCall(orderData)

                        if isByu == True:
                            if round(newLTP, 2) > round(finalLTPLOS15, 2):
                                print('------ New value ++++-----')
                                currentLTP = round(newLTP, 2)
                                finalLTPLOS15 =  round(newLTP, 2)
                                stopLOSE =  await getPer(newLTP,stopL,False)


                            if round(stopLOSE, 2) > round(newLTP, 2):
                                print('------Sell-----')
                                isByu=False
                                isValueSetFirst = True
                                orderData = {
                                        'quantity': quantity,
                                        'product': 'D',
                                        'validity': 'DAY',
                                        'price': 0,
                                        'tag': 'string',
                                        'instrument_token': instrument_key,
                                        'order_type': 'MARKET',
                                        'transaction_type': 'SELL',
                                        'disclosed_quantity': 0,
                                        'trigger_price': 0,
                                        'is_amo': False,
                                    }
                                await placeOrderApiCallSell(orderData)

                    else:
                        print('----No Data----')
            # print(response.json[0])
       
    except Exception as e:
        # Handle exceptions
        print('Error:  main ', str(e))



# asyncio.run(getChainApiCall())

# def apiCall():
#     newfeature2 =  asyncio.run(getChainApiCall());
#     newfeature3 =  asyncio.run(getChainApiPut());

def job():
    # newfeature =  asyncio.run(apiCall())# print(f.read())
    newfeature2 =  asyncio.run(getChainApiCall());
    # newfeature3 =  asyncio.run(getChainApiPut());


timers_container.create_timer('every poll', job)
# timers_container.create_timer('every second', hello_function)


chrono = Chronograph(timers_container.timer_jobs, 'US/Pacific')

print('sdasd')

# schedule.every(1).seconds.do(job)

# while True:
#     schedule.run_pending()
#     time.sleep(1)

# p = lambda x : x/100
# p20 = p(10)
# print(150*p20)
# minV = getClosest(320)
# print(minV['Body Weight'])