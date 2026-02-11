import discord,random
from discord.ext import commands
from db import get_user,update_user

class Levels(commands.Cog):
    def __init__(self,bot):
        self.bot=bot

    @commands.Cog.listener()
    async def on_message(self,m):
        if m.author.bot: return
        xp,lv,coins=get_user(m.guild.id,m.author.id)
        xp+=random.randint(5,10)

        need=lv*100
        if xp>=need:
            lv+=1
            await m.channel.send(f"{m.author.mention} Lv{lv}!")

        update_user(m.guild.id,m.author.id,xp,lv)

async def setup(bot):
    await bot.add_cog(Levels(bot))
