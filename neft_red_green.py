import requests


def getRedGreen():
        
    # Construct the full URL
    # url = "https://api.upstox.com/v2/historical-candle/intraday/NSE_INDEX|Nifty 50/1minute"    #for same day only
    url = "https://api.upstox.com/v2/historical-candle/NSE_INDEX|Nifty 50/1minute/2024-08-10/2023-08-09"    #for same day only

    print('Here 4')
    # Send the GET request
    response = requests.get(url)
    print('Here 4')
    print(response.status_code)
    # Check for a successful response
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        x = len(data['data']['candles'][0])
        if x > 0:
            first_candle_open = data['data']['candles'][0][1]
            first_candle_close = data['data']['candles'][0][4]

            if first_candle_close >  first_candle_open:
                return "green"
            else:
                return "red"

    else:
        print(f"Failed to retrieve data. Status code: {response.status_code}")
        print(f"Response: {response.text}")
        return ""  

callFun = getRedGreen()
print(callFun)


