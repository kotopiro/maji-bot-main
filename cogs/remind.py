import discord,asyncio
from discord.ext import commands

class Remind(commands.Cog):
    def __init__(self,bot):
        self.bot=bot

    @discord.app_commands.command(name="remind")
    async def remind(self,i,minutes:int,msg:str):
        await i.response.send_message("セットOK")

        await asyncio.sleep(minutes*60)
        await i.followup.send(f"⏰ {msg}")

async def setup(bot):
    await bot.add_cog(Remind(bot))
