import discord
from discord.ext import commands

cmds={}

class CC(commands.Cog):
    def __init__(self,bot):
        self.bot=bot

    @discord.app_commands.command(name="addcmd")
    async def add(self,i,name:str,text:str):
        cmds[name]=text
        await i.response.send_message("追加")

    @commands.Cog.listener()
    async def on_message(self,m):
        if m.content in cmds:
            await m.channel.send(cmds[m.content])

async def setup(bot):
    await bot.add_cog(CC(bot))
