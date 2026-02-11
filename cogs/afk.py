import discord
from discord.ext import commands

afk={}

class AFK(commands.Cog):
    def __init__(self,bot):
        self.bot=bot

    @discord.app_commands.command(name="afk")
    async def setafk(self,i,msg:str="離席"):
        afk[i.user.id]=msg
        await i.response.send_message("AFK設定")

    @commands.Cog.listener()
    async def on_message(self,m):
        if m.author.id in afk:
            del afk[m.author.id]
            await m.channel.send("AFK解除")

        for u in m.mentions:
            if u.id in afk:
                await m.channel.send(f"{u.name} AFK: {afk[u.id]}")

async def setup(bot):
    await bot.add_cog(AFK(bot))
