import discord
from discord.ext import commands
from bs4 import BeautifulSoup
import warnings
from urllib.request import URLError
from urllib.request import HTTPError
from urllib.request import urlopen
from urllib.request import Request, urlopen
import FinanceDataReader as fdr
import re

app = commands.Bot(command_prefix="!") # command_prefix에 자신이 원하는 접두사를 적어주세요 ex)!주식
token = "" # 봇의 토큰을 적어주세요.
app.remove_command("help")
game = "" # 자신이 원하는 상태 메시지를 적어주세요.

def stock_code(stock_name): # 주식 이름을 주면 주식 코드를 주는 함수
    df_krx = fdr.StockListing('KRX')
    name = df_krx[df_krx['Name']==stock_name]
    symbol = name.iloc[0, 0]
    return symbol

@app.event()
async def on_ready():
    print("Start Discord Bot")
    print(app.user.name)
    print(app.user.id)
    print(app.user)
    print("Made By Jung Ji-Hyo (cord)")
    await app.change_presence(status=discord.Status.online, activity=discord.Game(game))
    print("==================")

@app.command() # 주식 디스코드 봇 작동
async def 주식(ctx, stock_name=None):
    if stock_name is not None:
        try:
            code = stock_code(stock_name)
            embed = discord.Embed(colour=discord.Colour.red())
            embed.set_author(name=f"{stock_name}({code})의 주식 정보를 가져오는중..")
            msg = await ctx.send(embed=embed)
            url = f'https://finance.naver.com/item/sise.nhn?code={code}'
            html = urlopen(url)
            bs = BeautifulSoup(html, 'html.parser')

            price = bs.find('strong', {'class':'tah p11'}, {'id':'_nowVal'}).text.split('</span>')
            price = ''.join(price)

            rate = bs.find('strong', {'id':'_rate'}).text.split('</span>')
            rate = '\n'.join(rate)
            rate = rate.replace('\n', '')
            rate = rate.replace('\t', '')

            compared = bs.find('strong', {'id':'_diff'}).text.split('</span>')
            compared = '\n'.join(compared)
            compared = compared.replace('\n', '')
            compared = compared.replace('\t', '')

            if bs.find('em', {'class':'bu_p bu_pdn'}):
                check = '🔻'
                compared = compared.replace('하락', '')
            else:
                check = '🔺'
                compared = compared.replace('상승', '')

            sell = bs.find('span', {'id':'_quant'}).text.split('</span>')
            sell = '\n'.join(sell)
            sell = sell.replace('\n', '')
            sell = sell.replace('\t', '')

            amount = bs.find('span', {'id':'_amount'}).text.split('</span>')
            amount = '\n'.join(amount)
            amount = amount.replace('\n', '')
            amount = amount.replace('\t', '')

            embed = discord.Embed(colour=discord.Colour.green())
            embed.set_author(name=f"{stock_name} ({code})", url=f'https://finance.naver.com/item/sise.nhn?code={code}')
            embed.add_field(name="현재가", value=price)
            embed.add_field(name="전일대비", value=f"{check}{compared}")
            embed.add_field(name="등락률", value=rate)
            embed.add_field(name="거래량", value=sell)
            embed.add_field(name="거래대금(백만)", value=amount)
            embed.set_thumbnail(url=f"https://ssl.pstatic.net/imgfinance/chart/item/area/day/{code}.png")
            embed.set_image(url=f"https://ssl.pstatic.net/imgfinance/chart/item/area/day/{code}.png")
            await msg.edit(embed=embed)

        except Exception as e:
            embed = discord.Embed(colour=discord.Colour.red())
            embed.add_field(name="Error", value=e)
            await ctx.send(embed=embed)

app.run(token)
