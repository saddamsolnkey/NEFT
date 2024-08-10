import requests

url = "https://www.nseindia.com/api/live-analysis-variations?index=loosers"



headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
print('here')

response = requests.get(url, headers=headers)
print('here 22')

response.raise_for_status()
response.cookies
# response = requests.get(url, headers=headers)
print('here 1')
print(response.content)

