from typing import Optional
import discord
from discord.ext import commands

class UtilCog(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
    
    @commands.command(name="ping", aliases=["핑"])
    async def ping(self, ctx: commands.Context):
        text = ""
        if ctx.channel.type != discord.ChannelType.private:
            text += f"`이 서버의 Shard ID: {ctx.guild.shard_id}`\n"
        text += "```"
        for shard in self.bot.shards.values():
            text += f"Shard#{shard.id}: {int(shard.latency*1000)}ms\n"
        text += "```"
        embed = discord.Embed(title="Pong! :ping_pong: ", description=text, color=discord.Color.red())
        await ctx.send(embed=embed)
    @commands.command(name="reply")
    async def reply(self, ctx: commands.Context, loop_num: int=10, *, message=None):
        if message != None:
            for i in range(loop_num):
                await ctx.send(message)
        else:
            await ctx.send("메시지를 적어주세요.")

def setup(bot):
    bot.add_cog(UtilCog(bot))