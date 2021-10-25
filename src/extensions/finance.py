import discord
from discord.ext import commands
import api, config
import FinanceDataReader as fdr

async def getFinanceCode(name):
    df_krx = fdr.StockListing('KRX')
    name = df_krx[df_krx['Name']==name]
    symbol = name.iloc[0, 0]
    return symbol

class FinanceCog(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.command(name="finance", aliases=["주식", "stock"])
    async def finance(self, ctx: commands.Context, finance_code=None):
        if finance_code != None:
                if type(int(finance_code))==int and len(finance_code)==6: # 주식 코드 라면
                    code = finance_code
                    data = await api.finance_request(code=code)
                    if data["error"]==False:
                        embed = discord.Embed(title=f"{code}의 주식 정보", description=data, color=discord.Color.random())
                        embed.set_image(url=f"https://ssl.pstatic.net/imgfinance/chart/item/area/day/{code}.png")
                        await ctx.send(embed=embed)
                    else:
                        await ctx.send(embed=discord.Embed(title="알수 없는 주식 코드입니다!", description=f"{finance_code}에 맞는 주식 코드를 찾지 못했습니다!", color=discord.Color.red()))
                else:
                    await ctx.send(embed=discord.Embed(title="알수 없는 주식 코드입니다!", description="제가 알수 없는 주식 코드네요..", color=discord.Color.red()))
        else:
            await ctx.send(embed=discord.Embed(title="Error", description=":x: 주식 이름을 적어주세요!", color=discord.Color.red()))
    @commands.command(name="finance_code", aliases=["주식코드", "stock_code"])
    async def finance_code(self, ctx:commands.Context, name=None):
        if name != None:
            msg = await ctx.send(embed=discord.Embed(title="열심히 주식 코드를 찾는중..", color=discord.Color.random()))
            try:
                code = await getFinanceCode(name)
                await msg.edit(embed=discord.Embed(title=f"{name}의 주식 코드", description=f"주식 코드: **{code}**\n주식 정보가 궁금하시다면 **{config.PREFIX[0]}주식 {code}**를 사용해주세요!", color=discord.Color.random()))
            except:
                await msg.edit(embed=discord.Embed(title="찾을 수 없는 주식 이름입니다.", color=discord.Color.red()))
        else:
            await ctx.send("주식 이름을 적어주세요.")


def setup(bot):
    bot.add_cog(FinanceCog(bot))    