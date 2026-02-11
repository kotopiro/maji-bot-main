import discord,random
from discord.ext import commands
from db import get_user,update_user

class Eco(commands.Cog):
    def __init__(self,bot):
        self.bot=bot

    @discord.app_commands.command(name="daily")
    async def daily(self,i):
        xp,lv,c=get_user(i.guild.id,i.user.id)
        c+=200
        update_user(i.guild.id,i.user.id,coins=c)
        await i.response.send_message("200コイン")

    @discord.app_commands.command(name="gamble")
    async def gamble(self,i,amount:int):
        xp,lv,c=get_user(i.guild.id,i.user.id)
        if amount>c:
            await i.response.send_message("不足")
            return
        if random.random()<0.5:
            c+=amount
            msg="勝ち"
        else:
            c-=amount
            msg="負け"
        update_user(i.guild.id,i.user.id,coins=c)
        await i.response.send_message(msg)

async def setup(bot):
    await bot.add_cog(Eco(bot))
