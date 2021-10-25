import asyncio
import aiohttp
from datetime import datetime
from urllib import parse
from ast import literal_eval 

async def finance_request(code, start=datetime.now().strftime("%Y%m%d"), end=datetime.now().strftime("%Y%m%d")):
    async with aiohttp.ClientSession() as session:
        param = {'symbol':code, 'requestType':1, 'startTime':start, 'endTime':end, 'timeframe':"day"}  
        param = parse.urlencode(param)
        async with session.get(f"https://api.finance.naver.com/siseJson.naver?{param}") as rp:
            response = await rp.text()
            response = literal_eval(response.strip())
            if len(response) == 2:
                data = {"error":False}
                for i in range(len(response[0])):
                    data[response[0][i]] = response[1][i]
                return data
            else:
                data = {"error":True}

print(asyncio.get_event_loop().run_until_complete(finance_request("1212121")))